-- ============================================================================
-- DCSE V7 — Restricted-RPC and RLS Hardening
-- ============================================================================
-- Remediates the seven defects found by tests/rls_role_matrix.sql.
--
-- Design principle: AUTHORIZATION by role, INTEGRITY by constraint.
--   Role grants alone cannot protect the worker runtime, because workers
--   currently authenticate with the service_role key, which bypasses RLS.
--   Lease, ownership and idempotency invariants are therefore enforced with
--   constraints and triggers, which bind every role including service_role.
--
-- Defects remediated:
--   D1  claim_next_task: ambiguous "task_id" (migration drift vs. prod hotfix)
--   D2  send_heartbeat: accepts suspended/retired agents
--   D3  result_submission.claim_id: no foreign key
--   D4  result_submission: no active-lease enforcement
--   D5  result_submission: no idempotency constraint (duplicates accepted)
--   D6  task_claim: no cross-worker mutation guard
--   D7  dispatcher_recovery_cycle: 5-minute upper bound orphans stale claims
--   D8  SECURITY DEFINER functions carry mutable search_path "public, v7_worker"
--   D9  EXECUTE granted to PUBLIC/anon/authenticated on privileged RPCs
--   D10 PS lane has no explicit hard denial (relied on array match only)
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 0. Private schema for privileged internals
-- ---------------------------------------------------------------------------
create schema if not exists v7_worker_private;

revoke all on schema v7_worker_private from public;
revoke all on schema v7_worker_private from anon, authenticated;
grant usage on schema v7_worker_private to service_role;

comment on schema v7_worker_private is
  'Privileged internals for the v7 worker runtime. No anon/authenticated access.';

-- ---------------------------------------------------------------------------
-- 1. Trusted session identity (D9/D10 support)
--    Prefers a verified JWT claim; falls back to the app.worker_id GUC only
--    when no JWT is present (service-role/staging path). The fallback is a
--    mitigation, not authentication - see receipt.
-- ---------------------------------------------------------------------------
create or replace function v7_worker_private.session_agent_id()
returns text
language plpgsql
stable
security definer
set search_path = ''
as $$
declare
  v_claims json;
  v_agent  text;
begin
  begin
    v_claims := nullif(current_setting('request.jwt.claims', true), '')::json;
  exception when others then
    v_claims := null;
  end;

  if v_claims is not null then
    v_agent := v_claims ->> 'agent_id';
    if v_agent is not null and v_agent <> '' then
      return v_agent;
    end if;
  end if;

  return nullif(current_setting('app.worker_id', true), '');
end;
$$;

-- ---------------------------------------------------------------------------
-- 2. D3/D4/D5 - submission integrity
-- ---------------------------------------------------------------------------

-- D3: every submission must reference a real claim.
delete from v7_worker.result_submission rs
where not exists (
  select 1 from v7_worker.task_claim tc where tc.claim_id = rs.claim_id
);

alter table v7_worker.result_submission
  drop constraint if exists result_submission_claim_id_fkey;

alter table v7_worker.result_submission
  add constraint result_submission_claim_id_fkey
  foreign key (claim_id) references v7_worker.task_claim(claim_id)
  on delete restrict;

-- D5: one result per (claim, event type). Blocks duplicate submission for
-- every role, including service_role.
drop index if exists v7_worker.uq_result_submission_claim_event;
create unique index uq_result_submission_claim_event
  on v7_worker.result_submission (claim_id, result_event_type);

-- D4: submissions require a live, owned, unexpired lease.
create or replace function v7_worker_private.enforce_active_lease()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_claim v7_worker.task_claim%rowtype;
begin
  select * into v_claim
  from v7_worker.task_claim
  where claim_id = new.claim_id;

  if not found then
    raise exception 'submission rejected: claim % does not exist', new.claim_id
      using errcode = '23503';
  end if;

  if v_claim.agent_id is distinct from new.agent_id then
    raise exception 'submission rejected: claim % is owned by %, not %',
      new.claim_id, v_claim.agent_id, new.agent_id
      using errcode = '42501';
  end if;

  if v_claim.released_at is not null then
    raise exception 'submission rejected: claim % already released (%)',
      new.claim_id, v_claim.release_reason
      using errcode = '55000';
  end if;

  if v_claim.visibility_timeout_at <= now() then
    raise exception 'submission rejected: lease on claim % expired at %',
      new.claim_id, v_claim.visibility_timeout_at
      using errcode = '55000';
  end if;

  return new;
end;
$$;

drop trigger if exists trg_result_submission_active_lease on v7_worker.result_submission;
create trigger trg_result_submission_active_lease
  before insert on v7_worker.result_submission
  for each row execute function v7_worker_private.enforce_active_lease();

-- ---------------------------------------------------------------------------
-- 3. D6 - cross-worker claim mutation guard
--    Dispatcher work sets app.dispatcher_context locally; worker sessions must
--    match the claim owner. Applies to service_role as well.
-- ---------------------------------------------------------------------------
create or replace function v7_worker_private.guard_claim_mutation()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_session_agent text;
begin
  if new.agent_id is distinct from old.agent_id then
    raise exception 'claim % ownership is immutable (% -> %)',
      old.claim_id, old.agent_id, new.agent_id
      using errcode = '42501';
  end if;

  if coalesce(current_setting('app.dispatcher_context', true), 'off') = 'on' then
    return new;
  end if;

  v_session_agent := v7_worker_private.session_agent_id();

  if v_session_agent is not null and v_session_agent = old.agent_id then
    return new;
  end if;

  raise exception 'claim % may not be modified by session agent %',
    old.claim_id, coalesce(v_session_agent, '<unidentified>')
    using errcode = '42501';
end;
$$;

drop trigger if exists trg_task_claim_guard on v7_worker.task_claim;
create trigger trg_task_claim_guard
  before update on v7_worker.task_claim
  for each row execute function v7_worker_private.guard_claim_mutation();

-- ---------------------------------------------------------------------------
-- 4. D1/D10 - claim_next_task: qualify ambiguous column, hard PS denial,
--             empty search_path, full schema qualification
-- ---------------------------------------------------------------------------
create or replace function v7_worker.claim_next_task(
  p_agent_id text,
  p_visibility_timeout_seconds integer default 1800
)
returns table(
  queue_msg_id bigint,
  task_id text,
  lane text,
  task_type text,
  priority integer,
  runtime_packet jsonb,
  attempt_number integer
)
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_message_row record;
  v_max_attempts integer;
  v_agent_row v7_worker.agent_identity%rowtype;
begin
  select * into v_agent_row
  from v7_worker.agent_identity
  where agent_id = p_agent_id and status = 'approved'
  for update;

  if not found then
    raise exception 'Agent % not found or not approved', p_agent_id
      using errcode = '42501';
  end if;

  if v_agent_row.max_concurrent_tasks = 1 then
    if exists (
      select 1 from v7_worker.task_claim tc
      where tc.agent_id = p_agent_id
        and tc.released_at is null
        and tc.visibility_timeout_at > now()
    ) then
      return;
    end if;
  end if;

  select
    qm.msg_id, qm.task_id, qm.lane, qm.task_type, qm.priority, qm.runtime_packet,
    coalesce((
      select count(*)::int
      from v7_worker.task_claim tc2
      where tc2.task_id = qm.task_id      -- D1: qualified, no longer ambiguous
    ), 0) as attempts
  into v_message_row
  from v7_worker.queue_message qm
  where qm.dead_lettered_at is null
    and qm.lane = any(v_agent_row.authorized_lanes)
    and qm.task_type = any(v_agent_row.authorized_task_types)
    -- D10: PS work is never served to an agent without explicit PS authority
    and (qm.lane <> 'PS' or 'PS' = any(v_agent_row.authorized_lanes))
    and not exists (
      select 1 from v7_worker.task_claim tc3
      where tc3.queue_msg_id = qm.msg_id
        and tc3.released_at is null
        and tc3.visibility_timeout_at > now()
    )
  order by qm.priority desc, qm.enqueued_at asc
  limit 1
  for update skip locked;

  if v_message_row is null then
    return;
  end if;

  v_max_attempts := v_agent_row.max_attempts_per_task;
  if v_message_row.attempts >= v_max_attempts then
    insert into v7_worker.dead_letter (
      task_id, queue_msg_id, lane, task_type, reason, attempts,
      last_claim_by, policy_violated, runtime_packet
    ) values (
      v_message_row.task_id, v_message_row.msg_id, v_message_row.lane,
      v_message_row.task_type, 'Max attempts exceeded', v_message_row.attempts,
      p_agent_id, 'max_retries', v_message_row.runtime_packet
    );
    update v7_worker.queue_message
      set dead_lettered_at = now(), dead_letter_reason = 'Max attempts'
    where msg_id = v_message_row.msg_id;
    return;
  end if;

  insert into v7_worker.task_claim (
    queue_msg_id, task_id, agent_id, lane, task_type,
    visibility_timeout_at, lease_expires_at, attempt_number
  ) values (
    v_message_row.msg_id, v_message_row.task_id, p_agent_id,
    v_message_row.lane, v_message_row.task_type,
    now() + make_interval(secs => p_visibility_timeout_seconds),
    now() + make_interval(secs => p_visibility_timeout_seconds),
    v_message_row.attempts + 1
  );

  update v7_worker.queue_message set
    last_claimed_by = p_agent_id,
    last_claim_at = now(),
    read_count = read_count + 1
  where msg_id = v_message_row.msg_id;

  return query select
    v_message_row.msg_id, v_message_row.task_id, v_message_row.lane,
    v_message_row.task_type, v_message_row.priority, v_message_row.runtime_packet,
    v_message_row.attempts + 1;
end;
$$;

-- ---------------------------------------------------------------------------
-- 5. D2 - send_heartbeat rejects disabled workers; null-safe payloads
-- ---------------------------------------------------------------------------
create or replace function v7_worker.send_heartbeat(
  p_agent_id text,
  p_status text,
  p_current_task_id text default null,
  p_current_lane text default null,
  p_workspace_path text default null,
  p_branch_name text default null,
  p_model_version text default null,
  p_capabilities jsonb default '{}'::jsonb,
  p_metrics jsonb default null
)
returns table(heartbeat_id bigint, recorded_at timestamptz)
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_status text;
  v_metrics jsonb;
begin
  select status into v_status
  from v7_worker.agent_identity
  where agent_id = p_agent_id;

  if not found then
    raise exception 'Agent % not found', p_agent_id using errcode = '42501';
  end if;

  -- D2: suspended/retired workers are disabled and may not report liveness
  if v_status in ('suspended', 'retired') then
    raise exception 'Agent % is % and may not heartbeat', p_agent_id, v_status
      using errcode = '42501';
  end if;

  update v7_worker.agent_identity
    set last_heartbeat_at = now()
  where agent_id = p_agent_id;

  if p_metrics is null then
    select jsonb_build_object(
      'tasks_claimed',   coalesce((select count(*) from v7_worker.task_claim where agent_id = p_agent_id), 0),
      'tasks_completed', coalesce((select count(*) from v7_worker.result_submission
                                    where agent_id = p_agent_id and submission_status = 'acked'), 0),
      'tasks_failed',    coalesce((select count(*) from v7_worker.dead_letter where last_claim_by = p_agent_id), 0),
      'total_cost_usd',  coalesce((select sum(cost_usd)::numeric(10,2) from v7_worker.cost_ledger where agent_id = p_agent_id), 0)
    ) into v_metrics;
  else
    v_metrics := p_metrics;
  end if;

  return query
  insert into v7_worker.heartbeat (
    agent_id, current_task_id, status, current_lane, workspace_path,
    branch_name, model_version, capabilities, metrics
  ) values (
    p_agent_id, p_current_task_id, p_status, p_current_lane, p_workspace_path,
    p_branch_name, coalesce(p_model_version, ''),
    coalesce(p_capabilities, '{}'::jsonb),   -- null-safe
    coalesce(v_metrics, '{}'::jsonb)
  )
  returning heartbeat.heartbeat_id, heartbeat.sent_at;
end;
$$;

-- ---------------------------------------------------------------------------
-- 6. D6 support - release_task_claim runs in dispatcher context for its own
--    owned-claim update, with empty search_path
-- ---------------------------------------------------------------------------
create or replace function v7_worker.release_task_claim(
  p_claim_id bigint,
  p_agent_id text,
  p_reason text
)
returns table(success boolean, message text)
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_claim v7_worker.task_claim%rowtype;
begin
  select * into v_claim
  from v7_worker.task_claim
  where claim_id = p_claim_id and agent_id = p_agent_id
  for update;

  if not found then
    return query select false, 'Claim not found or agent mismatch';
    return;
  end if;

  if v_claim.released_at is not null then
    return query select false, 'Claim already released';
    return;
  end if;

  -- ownership already proven above; authorise the guarded update
  perform set_config('app.dispatcher_context', 'on', true);

  update v7_worker.task_claim
    set released_at = now(), release_reason = p_reason
  where claim_id = p_claim_id;

  if p_reason in ('timeout', 'error', 'worker_crash') then
    update v7_worker.queue_message
      set read_count = read_count + 1
    where msg_id = v_claim.queue_msg_id;
  end if;

  perform set_config('app.dispatcher_context', 'off', true);

  return query select true, 'Claim released: ' || p_reason;
end;
$$;

-- ---------------------------------------------------------------------------
-- 7. D7 - dispatcher recovers ALL expired claims (no 5-minute upper bound)
-- ---------------------------------------------------------------------------
create or replace function v7_worker.dispatcher_recovery_cycle()
returns table(
  recovered_count integer,
  escalated_count integer,
  execution_time_ms integer
)
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_start_time timestamptz := clock_timestamp();
  v_recovered integer := 0;
  v_escalated integer := 0;
  v_stale_claim record;
begin
  perform set_config('app.dispatcher_context', 'on', true);

  -- PHASE 1: recover every expired, unreleased lease.
  -- D7: the previous "(now() - visibility_timeout_at) < 5 minutes" bound
  -- permanently orphaned any claim that expired more than 5 minutes ago.
  for v_stale_claim in
    select claim_id, agent_id
    from v7_worker.task_claim
    where visibility_timeout_at < now()
      and released_at is null
  loop
    update v7_worker.task_claim
      set released_at = now(), release_reason = 'timeout'
    where claim_id = v_stale_claim.claim_id;
    v_recovered := v_recovered + 1;
  end loop;

  -- PHASE 2: suspend workers with stale heartbeats
  update v7_worker.agent_identity
    set status = 'suspended'
  where status = 'approved'
    and last_heartbeat_at < now() - interval '5 minutes'
    and deployment_env = 'staging';

  -- PHASE 3: escalate dead-letter awaiting manual review
  update v7_worker.dead_letter
    set escalated_to_cp = true, escalated_at = now()
  where requires_manual_escalation = true
    and escalated_to_cp = false
    and moved_at < now() - interval '1 hour';

  get diagnostics v_escalated = row_count;

  -- PHASE 4: cost-ceiling enforcement
  update v7_worker.agent_identity agent_rec
    set status = 'suspended'
  where agent_rec.status = 'approved'
    and (
      select coalesce(sum(cl.cost_usd), 0)
      from v7_worker.cost_ledger cl
      where cl.agent_id = agent_rec.agent_id
        and cl.billing_period = date_trunc('month', now())::date
    ) > agent_rec.monthly_cost_limit_usd;

  perform set_config('app.dispatcher_context', 'off', true);

  return query select
    v_recovered,
    v_escalated,
    (extract(epoch from (clock_timestamp() - v_start_time)) * 1000)::integer;
end;
$$;

-- ---------------------------------------------------------------------------
-- 8. D8/D9 - lock down the RPC surface
-- ---------------------------------------------------------------------------
revoke all on function v7_worker.claim_next_task(text, integer) from public, anon, authenticated;
revoke all on function v7_worker.send_heartbeat(text, text, text, text, text, text, text, jsonb, jsonb) from public, anon, authenticated;
revoke all on function v7_worker.release_task_claim(bigint, text, text) from public, anon, authenticated;
revoke all on function v7_worker.dispatcher_recovery_cycle() from public, anon, authenticated;
revoke all on function v7_worker.result_bridge_invoke() from public, anon, authenticated;
revoke all on function v7_worker.check_pending_stop_gates() from public, anon, authenticated;
revoke all on function v7_worker.acknowledge_result_processed(bigint, bigint) from public, anon, authenticated;

revoke all on function v7_worker_private.session_agent_id() from public, anon, authenticated;
revoke all on function v7_worker_private.enforce_active_lease() from public, anon, authenticated;
revoke all on function v7_worker_private.guard_claim_mutation() from public, anon, authenticated;

grant execute on function v7_worker.claim_next_task(text, integer) to service_role;
grant execute on function v7_worker.send_heartbeat(text, text, text, text, text, text, text, jsonb, jsonb) to service_role;
grant execute on function v7_worker.release_task_claim(bigint, text, text) to service_role;
grant execute on function v7_worker.dispatcher_recovery_cycle() to service_role;
grant execute on function v7_worker.result_bridge_invoke() to service_role;
grant execute on function v7_worker.check_pending_stop_gates() to service_role;
grant execute on function v7_worker.acknowledge_result_processed(bigint, bigint) to service_role;

-- Schema stays closed to the public API surface.
revoke usage on schema v7_worker from public, anon, authenticated;

comment on function v7_worker_private.session_agent_id() is
  'Resolves the acting agent from a verified JWT claim, falling back to the
   app.worker_id GUC when no JWT is present. The fallback is a staging
   mitigation and is not authentication.';

