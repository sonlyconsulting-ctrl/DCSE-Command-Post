-- DCSE / ESCD Orchestration Exchange v1
-- Supabase migration version applied to production: 20260914034207
-- Project: nevgdyfpxdaloacuutal (SC-Command-Post)
-- Purpose: durable operational turn state, return-control+payload ledger, and local/cloud orchestrator worker registry.

create table if not exists dcse_cp.escd_runtime_workers (
  worker_key text primary key,
  display_name text not null,
  runtime_type text not null default 'LOCAL_PYTHON'
    check (runtime_type in ('LOCAL_PYTHON','CLOUD_PYTHON','OTHER')),
  host_label text,
  capabilities text[] not null default '{}'::text[],
  status text not null default 'OFFLINE'
    check (status in ('OFFLINE','IDLE','BUSY','DEGRADED','DISABLED')),
  last_seen_at timestamptz,
  metadata jsonb not null default '{}'::jsonb
    check (jsonb_typeof(metadata) = 'object'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table dcse_cp.escd_runtime_workers is
'DCSE/ESCD runtime worker registry. Tracks local/cloud Python orchestrator workers; not a model registry.';

create table if not exists dcse_cp.escd_operation_turns (
  id uuid primary key default gen_random_uuid(),
  turn_key text not null unique default ('TURN-' || upper(substr(md5(gen_random_uuid()::text),1,12))),
  conversation_id uuid not null references dcse_cp.conversations(id) on delete restrict,
  request_turn_id uuid references dcse_cp.conversation_turns(id) on delete set null,
  response_turn_id uuid references dcse_cp.conversation_turns(id) on delete set null,
  requested_by_user_id uuid not null default auth.uid(),
  request_text text not null check (length(btrim(request_text)) > 0),
  request_payload jsonb not null default '{}'::jsonb
    check (jsonb_typeof(request_payload) = 'object'),
  operation_candidate jsonb not null default '{}'::jsonb
    check (jsonb_typeof(operation_candidate) = 'object'),
  final_response jsonb not null default '{}'::jsonb
    check (jsonb_typeof(final_response) = 'object'),
  state text not null default 'REQUESTED'
    check (state in (
      'REQUESTED','CLAIMED','INTERPRETING','PLANNING','EXECUTING',
      'VERIFYING','RESPONDING','WAITING_USER','ESCALATED',
      'COMPLETE','REFUSED','FAILED','CANCELLED'
    )),
  stage text not null default 'INGRESS'
    check (stage in ('INGRESS','PRECONDITION','EXECUTION','POSTCONDITION','AUDIT','RESPONSE','TERMINAL')),
  control_state text not null default 'ORCHESTRATOR'
    check (control_state in ('ORCHESTRATOR','WAITING_PROVIDER','WAITING_TOOL','WAITING_USER','TERMINAL')),
  provider_preference text,
  active_provider text,
  active_model text,
  claimed_by_worker_key text references dcse_cp.escd_runtime_workers(worker_key) on delete set null,
  lease_expires_at timestamptz,
  heartbeat_at timestamptz,
  attempt_count integer not null default 0 check (attempt_count >= 0),
  requires_user boolean not null default false,
  error_code text,
  terminal_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table dcse_cp.escd_operation_turns is
'Authoritative operational turn state for ESCD. Conversation may remain open; each operational turn must reach a defined terminal or WAITING_USER state.';

create table if not exists dcse_cp.escd_operation_events (
  id uuid primary key default gen_random_uuid(),
  turn_id uuid not null references dcse_cp.escd_operation_turns(id) on delete restrict,
  event_type text not null
    check (event_type in (
      'REQUEST_RECEIVED','PROVIDER_REQUEST','PROVIDER_RETURN',
      'TOOL_REQUEST','TOOL_RETURN','RULE_EVALUATION',
      'STATE_CHANGE','AUDIT','FINAL_RESPONSE','USER_CONTINUE','ERROR'
    )),
  stage text not null
    check (stage in ('INGRESS','PRECONDITION','EXECUTION','POSTCONDITION','AUDIT','RESPONSE','TERMINAL')),
  direction text not null default 'INTERNAL'
    check (direction in ('REQUEST','RETURN','INTERNAL')),
  actor_type text not null
    check (actor_type in ('USER','ORCHESTRATOR','PROVIDER','TOOL','AUDITOR','SYSTEM')),
  actor_ref text,
  control_state text
    check (control_state is null or control_state in (
      'RETURN_TO_ORCHESTRATOR','COMPLETE','NEEDS_TOOL','NEEDS_USER',
      'RETRY','ESCALATE','FAIL'
    )),
  payload jsonb not null default '{}'::jsonb
    check (jsonb_typeof(payload) = 'object'),
  evidence_refs jsonb not null default '[]'::jsonb
    check (jsonb_typeof(evidence_refs) = 'array'),
  correlation_key text,
  created_at timestamptz not null default now(),
  constraint escd_return_requires_control_and_payload
    check (
      direction <> 'RETURN'
      or (
        control_state is not null
        and payload <> '{}'::jsonb
      )
    )
);

comment on table dcse_cp.escd_operation_events is
'Append-only ESCD orchestration exchange ledger. Any RETURN event must carry both control and a non-empty payload.';

create index if not exists idx_escd_operation_turns_state_created
  on dcse_cp.escd_operation_turns(state, created_at);
create index if not exists idx_escd_operation_turns_conversation_created
  on dcse_cp.escd_operation_turns(conversation_id, created_at);
create index if not exists idx_escd_operation_turns_lease
  on dcse_cp.escd_operation_turns(lease_expires_at)
  where lease_expires_at is not null;
create index if not exists idx_escd_operation_events_turn_created
  on dcse_cp.escd_operation_events(turn_id, created_at);
create index if not exists idx_escd_runtime_workers_status_seen
  on dcse_cp.escd_runtime_workers(status, last_seen_at);

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
    when 'WAITING_USER' then new.state in ('CLAIMED','CANCELLED','FAILED')
    when 'ESCALATED' then new.state in ('CLAIMED','CANCELLED','REFUSED','FAILED')
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

drop trigger if exists trg_escd_operation_turn_transition on dcse_cp.escd_operation_turns;
create trigger trg_escd_operation_turn_transition
before update on dcse_cp.escd_operation_turns
for each row execute function dcse_cp.escd_validate_operation_turn_transition();

drop trigger if exists trg_escd_runtime_workers_updated_at on dcse_cp.escd_runtime_workers;
create trigger trg_escd_runtime_workers_updated_at
before update on dcse_cp.escd_runtime_workers
for each row execute function dcse_cp.touch_updated_at();

alter table dcse_cp.escd_runtime_workers enable row level security;
alter table dcse_cp.escd_operation_turns enable row level security;
alter table dcse_cp.escd_operation_events enable row level security;

drop policy if exists escd_runtime_workers_owner_select on dcse_cp.escd_runtime_workers;
create policy escd_runtime_workers_owner_select
on dcse_cp.escd_runtime_workers
for select to authenticated
using (dcse_cp.is_dcs_owner());

drop policy if exists escd_operation_turns_owner_select on dcse_cp.escd_operation_turns;
create policy escd_operation_turns_owner_select
on dcse_cp.escd_operation_turns
for select to authenticated
using (dcse_cp.is_dcs_owner() and requested_by_user_id = auth.uid());

drop policy if exists escd_operation_turns_owner_insert on dcse_cp.escd_operation_turns;
create policy escd_operation_turns_owner_insert
on dcse_cp.escd_operation_turns
for insert to authenticated
with check (
  dcse_cp.is_dcs_owner()
  and requested_by_user_id = auth.uid()
  and exists (
    select 1
    from dcse_cp.conversations c
    where c.id = conversation_id
      and (c.created_by = auth.uid() or c.created_by is null)
  )
);

drop policy if exists escd_operation_events_owner_select on dcse_cp.escd_operation_events;
create policy escd_operation_events_owner_select
on dcse_cp.escd_operation_events
for select to authenticated
using (
  dcse_cp.is_dcs_owner()
  and exists (
    select 1
    from dcse_cp.escd_operation_turns t
    where t.id = turn_id
      and t.requested_by_user_id = auth.uid()
  )
);

revoke all on dcse_cp.escd_runtime_workers from anon, authenticated;
grant select on dcse_cp.escd_runtime_workers to authenticated;
grant select, insert, update on dcse_cp.escd_runtime_workers to service_role;

revoke all on dcse_cp.escd_operation_turns from anon, authenticated;
grant select, insert on dcse_cp.escd_operation_turns to authenticated;
grant select, insert, update on dcse_cp.escd_operation_turns to service_role;

revoke all on dcse_cp.escd_operation_events from anon, authenticated;
grant select on dcse_cp.escd_operation_events to authenticated;
grant select, insert on dcse_cp.escd_operation_events to service_role;

create or replace function dcse_cp.escd_claim_next_turn(
  p_worker_key text,
  p_lease_seconds integer default 120
)
returns setof dcse_cp.escd_operation_turns
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_turn_id uuid;
begin
  if p_worker_key is null or btrim(p_worker_key) = '' then
    raise exception 'worker_key_required';
  end if;

  if p_lease_seconds < 15 or p_lease_seconds > 900 then
    raise exception 'lease_seconds_out_of_range';
  end if;

  if not exists (
    select 1 from dcse_cp.escd_runtime_workers w
    where w.worker_key = p_worker_key
      and w.status <> 'DISABLED'
  ) then
    raise exception 'worker_not_registered_or_disabled';
  end if;

  select t.id into v_turn_id
  from dcse_cp.escd_operation_turns t
  where t.state = 'REQUESTED'
  order by t.created_at asc
  for update skip locked
  limit 1;

  if v_turn_id is null then
    return;
  end if;

  update dcse_cp.escd_operation_turns
  set state = 'CLAIMED',
      stage = 'PRECONDITION',
      control_state = 'ORCHESTRATOR',
      claimed_by_worker_key = p_worker_key,
      lease_expires_at = now() + make_interval(secs => p_lease_seconds),
      heartbeat_at = now(),
      attempt_count = attempt_count + 1
  where id = v_turn_id;

  update dcse_cp.escd_runtime_workers
  set status = 'BUSY',
      last_seen_at = now()
  where worker_key = p_worker_key;

  return query
  select * from dcse_cp.escd_operation_turns where id = v_turn_id;
end;
$$;

revoke all on function dcse_cp.escd_claim_next_turn(text,integer) from public, anon, authenticated;
grant execute on function dcse_cp.escd_claim_next_turn(text,integer) to service_role;

create or replace function dcse_cp.escd_record_return(
  p_turn_id uuid,
  p_event_type text,
  p_stage text,
  p_actor_type text,
  p_actor_ref text,
  p_control_state text,
  p_payload jsonb,
  p_evidence_refs jsonb default '[]'::jsonb
)
returns uuid
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $$
declare
  v_event_id uuid;
begin
  if p_payload is null or p_payload = '{}'::jsonb then
    raise exception 'return_payload_required';
  end if;
  if p_control_state not in (
    'RETURN_TO_ORCHESTRATOR','COMPLETE','NEEDS_TOOL','NEEDS_USER',
    'RETRY','ESCALATE','FAIL'
  ) then
    raise exception 'invalid_return_control_state';
  end if;

  insert into dcse_cp.escd_operation_events(
    turn_id,event_type,stage,direction,actor_type,actor_ref,
    control_state,payload,evidence_refs
  )
  values(
    p_turn_id,p_event_type,p_stage,'RETURN',p_actor_type,p_actor_ref,
    p_control_state,p_payload,coalesce(p_evidence_refs,'[]'::jsonb)
  )
  returning id into v_event_id;

  return v_event_id;
end;
$$;

revoke all on function dcse_cp.escd_record_return(uuid,text,text,text,text,text,jsonb,jsonb)
from public, anon, authenticated;
grant execute on function dcse_cp.escd_record_return(uuid,text,text,text,text,text,jsonb,jsonb)
to service_role;
