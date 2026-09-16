
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
    when 'CLAIMED' then new.state in ('INTERPRETING','CANCELLED','FAILED')
    when 'INTERPRETING' then new.state in ('PLANNING','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'PLANNING' then new.state in ('EXECUTING','RESPONDING','WAITING_USER','ESCALATED','REFUSED','CANCELLED','FAILED')
    when 'EXECUTING' then new.state in ('VERIFYING','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'VERIFYING' then new.state in ('EXECUTING','RESPONDING','WAITING_USER','ESCALATED','REFUSED','CANCELLED','FAILED')
    when 'RESPONDING' then new.state in ('COMPLETE','WAITING_USER','ESCALATED','CANCELLED','FAILED')
    when 'WAITING_USER' then new.state in ('REQUESTED','CLAIMED','CANCELLED','FAILED')
    when 'ESCALATED' then new.state in ('REQUESTED','CLAIMED','CANCELLED','REFUSED','FAILED')
    else false
  end;

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

create or replace function dcse_cp.escd_submit_operation_turn(
  p_conversation_id uuid,
  p_request_turn_id uuid,
  p_request_text text,
  p_provider_preference text default null,
  p_request_payload jsonb default '{}'::jsonb
)
returns dcse_cp.escd_operation_turns
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_uid uuid := auth.uid();
  v_row dcse_cp.escd_operation_turns;
begin
  if auth.role()<>'service_role' and not dcse_cp.is_dcs_owner() then
    raise exception 'dcs_owner_required';
  end if;

  if auth.role()<>'service_role' and v_uid is null then
    raise exception 'authenticated_user_required';
  end if;

  if not exists (
    select 1 from dcse_cp.conversations c
    where c.id=p_conversation_id
      and (
        auth.role()='service_role'
        or c.created_by=v_uid
        or c.created_by is null
      )
  ) then
    raise exception 'conversation_not_accessible';
  end if;

  if p_request_turn_id is not null and not exists (
    select 1 from dcse_cp.conversation_turns ct
    where ct.id=p_request_turn_id and ct.conversation_id=p_conversation_id
  ) then
    raise exception 'request_turn_not_in_conversation';
  end if;

  insert into dcse_cp.escd_operation_turns(
    conversation_id,request_turn_id,requested_by_user_id,request_text,
    request_payload,provider_preference,state,stage,control_state
  ) values (
    p_conversation_id,p_request_turn_id,
    case
      when auth.role()='service_role'
      then coalesce(
        (select created_by from dcse_cp.conversations where id=p_conversation_id),
        (select user_id from dcse_cp.operator_accounts where active=true order by created_at limit 1)
      )
      else v_uid
    end,
    p_request_text,
    coalesce(p_request_payload,'{}'::jsonb),
    nullif(btrim(p_provider_preference),''),
    'REQUESTED','INGRESS','ORCHESTRATOR'
  )
  returning * into v_row;

  insert into dcse_cp.escd_operation_events(
    turn_id,event_type,stage,direction,actor_type,actor_ref,payload,evidence_refs
  ) values (
    v_row.id,'REQUEST_RECEIVED','INGRESS','REQUEST','USER',
    coalesce(v_uid::text,'service_role'),
    jsonb_build_object(
      'request_text',p_request_text,
      'provider_preference',p_provider_preference,
      'conversation_id',p_conversation_id::text,
      'request_turn_id',p_request_turn_id::text
    ) || coalesce(p_request_payload,'{}'::jsonb),
    '[]'::jsonb
  );

  return v_row;
end;
$$;

revoke all on function dcse_cp.escd_submit_operation_turn(uuid,uuid,text,text,jsonb)
from public,anon;
grant execute on function dcse_cp.escd_submit_operation_turn(uuid,uuid,text,text,jsonb)
to authenticated,service_role;

create or replace function dcse_cp.escd_user_control_turn(
  p_turn_key text,
  p_action text,
  p_response_text text default null
)
returns dcse_cp.escd_operation_turns
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_uid uuid := auth.uid();
  v_row dcse_cp.escd_operation_turns;
  v_action text := lower(btrim(coalesce(p_action,'')));
begin
  select * into v_row
  from dcse_cp.escd_operation_turns t
  where t.turn_key=p_turn_key
    and (
      auth.role()='service_role'
      or (dcse_cp.is_dcs_owner() and t.requested_by_user_id=v_uid)
    )
  for update;

  if not found then raise exception 'turn_not_accessible'; end if;

  if v_action='stop' then
    if v_row.state in ('COMPLETE','REFUSED','FAILED','CANCELLED') then
      return v_row;
    end if;

    update dcse_cp.escd_operation_turns
    set state='CANCELLED',
        error_code='cancelled_by_dcs'
    where id=v_row.id
    returning * into v_row;

    insert into dcse_cp.escd_operation_events(
      turn_id,event_type,stage,direction,actor_type,actor_ref,control_state,payload,evidence_refs
    ) values (
      v_row.id,'STATE_CHANGE','TERMINAL','INTERNAL','USER',
      coalesce(v_uid::text,'service_role'),'COMPLETE',
      jsonb_build_object('action','stop','result','CANCELLED'),
      '[]'::jsonb
    );

    return v_row;
  end if;

  if v_action='continue' then
    if v_row.state not in ('WAITING_USER','ESCALATED') then
      raise exception 'turn_not_resumable:%',v_row.state;
    end if;

    insert into dcse_cp.escd_operation_events(
      turn_id,event_type,stage,direction,actor_type,actor_ref,control_state,payload,evidence_refs
    ) values (
      v_row.id,'USER_CONTINUE','PRECONDITION','RETURN','USER',
      coalesce(v_uid::text,'service_role'),'RETURN_TO_ORCHESTRATOR',
      jsonb_build_object('response',coalesce(p_response_text,'Proceed')),
      '[]'::jsonb
    );

    update dcse_cp.escd_operation_turns
    set state='REQUESTED',
        stage='PRECONDITION',
        control_state='ORCHESTRATOR',
        claimed_by_worker_key=null,
        lease_expires_at=null,
        heartbeat_at=null,
        error_code=null
    where id=v_row.id
    returning * into v_row;

    return v_row;
  end if;

  raise exception 'invalid_turn_action';
end;
$$;

revoke all on function dcse_cp.escd_user_control_turn(text,text,text)
from public,anon;
grant execute on function dcse_cp.escd_user_control_turn(text,text,text)
to authenticated,service_role;

create or replace function dcse_cp.escd_operation_turn_snapshot(
  p_turn_key text
)
returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_turn jsonb;
  v_events jsonb;
begin
  select to_jsonb(t) into v_turn
  from dcse_cp.escd_operation_turns t
  where t.turn_key=p_turn_key
    and (
      auth.role()='service_role'
      or (dcse_cp.is_dcs_owner() and t.requested_by_user_id=auth.uid())
    );

  if v_turn is null then raise exception 'turn_not_accessible'; end if;

  select coalesce(jsonb_agg(to_jsonb(e) order by e.created_at),'[]'::jsonb)
  into v_events
  from dcse_cp.escd_operation_events e
  join dcse_cp.escd_operation_turns t on t.id=e.turn_id
  where t.turn_key=p_turn_key;

  return jsonb_build_object('turn',v_turn,'events',v_events);
end;
$$;

revoke all on function dcse_cp.escd_operation_turn_snapshot(text) from public,anon;
grant execute on function dcse_cp.escd_operation_turn_snapshot(text)
to authenticated,service_role;

