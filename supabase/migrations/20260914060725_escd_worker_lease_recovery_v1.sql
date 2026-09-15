
create or replace function dcse_cp.escd_validate_operation_turn_transition()
returns trigger
language plpgsql
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  allowed boolean := false;
begin
  if new.state = old.state then
    new.updated_at := now();
    return new;
  end if;

  allowed := case old.state
    when 'REQUESTED' then new.state in ('CLAIMED','CANCELLED','FAILED')
    when 'CLAIMED' then new.state in ('INTERPRETING','REQUESTED','CANCELLED','FAILED')
    when 'INTERPRETING' then new.state in ('PLANNING','REQUESTED','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'PLANNING' then new.state in ('EXECUTING','REQUESTED','RESPONDING','WAITING_USER','ESCALATED','REFUSED','CANCELLED','FAILED')
    when 'EXECUTING' then new.state in ('VERIFYING','REQUESTED','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'VERIFYING' then new.state in ('EXECUTING','REQUESTED','RESPONDING','WAITING_USER','ESCALATED','REFUSED','CANCELLED','FAILED')
    when 'RESPONDING' then new.state in ('COMPLETE','REQUESTED','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'WAITING_USER' then new.state in ('REQUESTED','CLAIMED','CANCELLED','FAILED')
    when 'ESCALATED' then new.state in ('REQUESTED','CLAIMED','CANCELLED','REFUSED','FAILED')
    else false
  end;

  if new.state='REQUESTED'
     and old.state<>'WAITING_USER'
     and old.state<>'ESCALATED'
     and old.state<>'REQUESTED'
     and not (
       auth.role()='service_role'
       and old.lease_expires_at is not null
       and old.lease_expires_at <= now()
     )
  then
    allowed := false;
  end if;

  if not allowed then
    raise exception 'invalid_escd_turn_transition:%->%', old.state, new.state
      using errcode = 'check_violation';
  end if;

  if new.state = 'WAITING_USER' then
    new.requires_user := true;
    new.control_state := 'WAITING_USER';
  elsif new.state in ('COMPLETE','REFUSED','FAILED','CANCELLED') then
    new.requires_user := false;
    new.stage := 'TERMINAL';
    new.control_state := 'TERMINAL';
    new.terminal_at := coalesce(new.terminal_at, now());
  else
    new.requires_user := false;
  end if;

  new.updated_at := now();
  return new;
end;
$$;

create or replace function dcse_cp.escd_worker_heartbeat(
  p_worker_key text,
  p_turn_id uuid default null,
  p_lease_seconds integer default 120,
  p_status text default 'BUSY'
)
returns boolean
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
begin
  if auth.role()<>'service_role' then
    raise exception 'service_role_required';
  end if;

  if p_lease_seconds < 15 or p_lease_seconds > 900 then
    raise exception 'lease_seconds_out_of_range';
  end if;

  update dcse_cp.escd_runtime_workers
  set status=case
      when p_status in ('OFFLINE','IDLE','BUSY','DEGRADED','DISABLED') then p_status
      else 'BUSY'
    end,
    last_seen_at=now(),
    updated_at=now()
  where worker_key=p_worker_key
    and status<>'DISABLED';

  if not found then
    raise exception 'worker_not_registered_or_disabled';
  end if;

  if p_turn_id is not null then
    update dcse_cp.escd_operation_turns
    set heartbeat_at=now(),
        lease_expires_at=now()+make_interval(secs=>p_lease_seconds)
    where id=p_turn_id
      and claimed_by_worker_key=p_worker_key
      and state not in ('COMPLETE','REFUSED','FAILED','CANCELLED');
  end if;

  return true;
end;
$$;

revoke all on function dcse_cp.escd_worker_heartbeat(text,uuid,integer,text)
from public,anon,authenticated;
grant execute on function dcse_cp.escd_worker_heartbeat(text,uuid,integer,text)
to service_role;

create or replace function dcse_cp.escd_requeue_expired_turns(
  p_limit integer default 25
)
returns integer
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_count integer := 0;
  v_id uuid;
begin
  if auth.role()<>'service_role' then
    raise exception 'service_role_required';
  end if;

  for v_id in
    select id
    from dcse_cp.escd_operation_turns
    where state in ('CLAIMED','INTERPRETING','PLANNING','EXECUTING','VERIFYING','RESPONDING')
      and lease_expires_at is not null
      and lease_expires_at <= now()
    order by lease_expires_at
    for update skip locked
    limit greatest(1,least(coalesce(p_limit,25),200))
  loop
    update dcse_cp.escd_operation_turns
    set state='REQUESTED',
        stage='PRECONDITION',
        control_state='ORCHESTRATOR',
        claimed_by_worker_key=null,
        lease_expires_at=null,
        heartbeat_at=null,
        error_code='requeued_after_expired_lease'
    where id=v_id;

    insert into dcse_cp.escd_operation_events(
      turn_id,event_type,stage,direction,actor_type,actor_ref,payload,evidence_refs
    ) values (
      v_id,'STATE_CHANGE','PRECONDITION','INTERNAL','SYSTEM',
      'lease-recovery',
      jsonb_build_object('result','REQUESTED','reason','expired_worker_lease'),
      '[]'::jsonb
    );

    v_count := v_count + 1;
  end loop;

  return v_count;
end;
$$;

revoke all on function dcse_cp.escd_requeue_expired_turns(integer)
from public,anon,authenticated;
grant execute on function dcse_cp.escd_requeue_expired_turns(integer)
to service_role;

