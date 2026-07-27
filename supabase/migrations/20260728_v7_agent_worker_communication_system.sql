-- V7 Agent Worker Communication System
-- Autonomous model worker runtime with queue-based task dispatch,
-- worker identity/heartbeat tracking, and durable message handling.
--
-- Purpose: Enable persistent headless workers (Qwen Code, Claude Agent SDK, Codex)
-- to autonomously claim tasks, execute them, and write results back to Supabase
-- without manual human intervention for each task.

-- ============================================================================
-- 0. EXTENSIONS AND SCHEMAS
-- ============================================================================

-- Enable pgmq for durable queue support (visibility timeout, acknowledgment)
create extension if not exists pgmq with schema pgmq;

-- Create v7_worker schema for agent runtime infrastructure
create schema if not exists v7_worker;

comment on schema v7_worker is
  'DCSE V7 agent worker runtime: heartbeats, queue management, claims, leases.';

-- ============================================================================
-- 1. WORKER IDENTITY AND REGISTRATION
-- ============================================================================

-- Every persistent worker has a unique identity scoped by device and model.
-- Format: AGENT-{MODEL}-{SEQUENCE}@{DEVICE_ID}
-- Example: AGENT-QWEN-CODER-01@LAPTOP-74UF76GB
create table v7_worker.agent_identity (
  agent_id text primary key,
  agent_name text not null,
  model_family text not null check (model_family in ('qwen', 'claude', 'codex', 'deterministic')),
  device_id text not null,
  device_hostname text not null,
  deployment_env text not null default 'staging' check (deployment_env in ('staging', 'production', 'test')),
  authorized_lanes text[] not null default '{}'::text[],
  authorized_task_types text[] not null default '{}'::text[],
  approval_mode text not null default 'plan-only' check (approval_mode in
    ('read-only', 'plan-only', 'auto-edit', 'governed-approval', 'full-access')),
  max_concurrent_tasks integer not null default 1,
  max_wall_time_minutes integer not null default 30,
  max_session_turns integer not null default 30,
  max_attempts_per_task integer not null default 3,
  monthly_cost_limit_usd numeric(10,2) not null default 100.00,
  tool_allowlist jsonb not null default '[]'::jsonb,
  tool_denylist jsonb not null default '[]'::jsonb,
  status text not null default 'candidate' check (status in ('candidate', 'approved', 'suspended', 'retired')),
  registered_at timestamptz not null default now(),
  last_heartbeat_at timestamptz,
  updated_at timestamptz not null default now()
);

comment on table v7_worker.agent_identity is
  'Registry of persistent model workers. Format: AGENT-{MODEL}-{N}@{DEVICE}.
   Each worker has unique identity, approved lanes/task-types, permission mode, and cost limits.';

create index idx_v7_worker_agent_identity_status on v7_worker.agent_identity(status);
create index idx_v7_worker_agent_identity_model on v7_worker.agent_identity(model_family, status);
create index idx_v7_worker_agent_identity_device on v7_worker.agent_identity(device_id);
create index idx_v7_worker_agent_identity_lanes on v7_worker.agent_identity using gin(authorized_lanes);

alter table v7_worker.agent_identity enable row level security;

-- Workers access only their own identity; service-role can read all
create policy "workers_read_own_identity" on v7_worker.agent_identity
  for select to authenticated, anon
  using (agent_id = current_setting('app.worker_id', true)::text);

create policy "service_role_full_access" on v7_worker.agent_identity
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 2. WORKER HEARTBEAT AND HEALTH TRACKING
-- ============================================================================

-- Persistent heartbeat to track worker liveness and capability snapshot.
-- Workers poll tasks every N seconds and send heartbeat every M minutes.
create table v7_worker.heartbeat (
  heartbeat_id bigint generated always as identity primary key,
  agent_id text not null references v7_worker.agent_identity(agent_id) on delete cascade,
  current_task_id text,
  status text not null check (status in ('idle', 'claiming', 'running', 'uploading_result', 'error')),
  current_lane text,
  workspace_path text,
  branch_name text,
  model_version text not null,
  last_successful_claim_at timestamptz,
  last_error text,
  last_error_at timestamptz,
  capabilities jsonb not null default '{}'::jsonb,
  metrics jsonb not null default '{
    "tasks_claimed": 0,
    "tasks_completed": 0,
    "tasks_failed": 0,
    "total_wall_minutes": 0,
    "total_cost_usd": 0
  }'::jsonb,
  sent_at timestamptz not null default now()
);

comment on table v7_worker.heartbeat is
  'One-per-worker heartbeat snapshot. Sent every poll cycle (~15s).
   Tracks liveness, current task, metrics, errors, capability snapshot.';

create index idx_v7_worker_heartbeat_agent on v7_worker.heartbeat(agent_id, sent_at desc);
create index idx_v7_worker_heartbeat_status on v7_worker.heartbeat(status);
create index idx_v7_worker_heartbeat_recent on v7_worker.heartbeat(sent_at desc);

alter table v7_worker.heartbeat enable row level security;

create policy "workers_read_own_heartbeat" on v7_worker.heartbeat
  for select to authenticated, anon
  using (agent_id = current_setting('app.worker_id', true)::text);

create policy "service_role_full_access" on v7_worker.heartbeat
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 3. WORKER TASK QUEUE AND CLAIMS (pgmq-based durability)
-- ============================================================================

-- Claim record: worker has leased this task and will complete within visibility_timeout
create table v7_worker.task_claim (
  claim_id bigint generated always as identity primary key,
  queue_msg_id bigint not null,
  task_id text not null,
  agent_id text not null references v7_worker.agent_identity(agent_id),
  lane text not null,
  task_type text not null,
  claimed_at timestamptz not null default now(),
  visibility_timeout_at timestamptz not null,
  lease_expires_at timestamptz not null,
  attempt_number integer not null default 1,
  worker_session_id text,
  worker_model_version text,
  released_at timestamptz,
  release_reason text,
  acked_at timestamptz
);

comment on table v7_worker.task_claim is
  'Lease record when worker claims a task from the queue.
   Visibility timeout expires if worker crashes; lease tracks attempt count and session.
   Worker acks only after writing result to dcse_cp.agent_task_events.';

create index idx_v7_worker_task_claim_agent on v7_worker.task_claim(agent_id, claimed_at desc);
create index idx_v7_worker_task_claim_task on v7_worker.task_claim(task_id);
create index idx_v7_worker_task_claim_expiry on v7_worker.task_claim(lease_expires_at);
create index idx_v7_worker_task_claim_timeout on v7_worker.task_claim(visibility_timeout_at)
  where released_at is null;

alter table v7_worker.task_claim enable row level security;

create policy "workers_read_own_claims" on v7_worker.task_claim
  for select to authenticated, anon
  using (agent_id = current_setting('app.worker_id', true)::text);

create policy "service_role_full_access" on v7_worker.task_claim
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 4. QUEUE MESSAGE WRAPPER (pgmq integration)
-- ============================================================================

-- Wrapper around pgmq.queue_name to expose a worker-facing message interface.
-- pgmq handles durability, visibility timeout, and acknowledgment.
-- This table bridges v7_bootstrap.tasks and the worker claim lifecycle.
create table v7_worker.queue_message (
  msg_id bigint not null primary key,
  queue_name text not null default 'dcse_agent_tasks',
  task_id text not null,
  lane text not null,
  task_type text not null,
  priority integer not null default 5,
  runtime_packet jsonb not null,
  created_at timestamptz not null default now(),
  read_count integer not null default 0,
  enqueued_at timestamptz not null default now(),
  last_claimed_by text,
  last_claim_at timestamptz,
  dead_lettered_at timestamptz,
  dead_letter_reason text
);

comment on table v7_worker.queue_message is
  'Message wrapper for pgmq durability. Each message holds a runtime_packet
   with task input, acceptance_criteria, and expected outputs.
   Workers claim via pgmq.read(), then record claim in task_claim table.';

create index idx_v7_worker_queue_message_task on v7_worker.queue_message(task_id);
create index idx_v7_worker_queue_message_lane on v7_worker.queue_message(lane);
create index idx_v7_worker_queue_message_priority on v7_worker.queue_message(priority desc, enqueued_at asc);
create index idx_v7_worker_queue_message_claimed on v7_worker.queue_message(last_claim_at desc)
  where dead_lettered_at is null;

alter table v7_worker.queue_message enable row level security;

create policy "workers_read_eligible_messages" on v7_worker.queue_message
  for select to authenticated, anon
  using (
    dead_lettered_at is null
    and lane = any(
      (select authorized_lanes from v7_worker.agent_identity
       where agent_id = current_setting('app.worker_id', true)::text)
    )
  );

create policy "service_role_full_access" on v7_worker.queue_message
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 5. WORKER RESULT SUBMISSION (bridge to dcse_cp)
-- ============================================================================

-- Capture worker submission before writing to dcse_cp.agent_task_events
-- Allows audit trail and retry tracking independent of main event log
create table v7_worker.result_submission (
  submission_id bigint generated always as identity primary key,
  task_id text not null,
  claim_id bigint not null,
  agent_id text not null references v7_worker.agent_identity(agent_id),
  submission_status text not null check (submission_status in ('pending', 'acked', 'failed', 'retrying')),
  result_event_type text not null,
  result_output jsonb not null,
  worker_session_id text,
  submission_attempted_at timestamptz not null default now(),
  submission_acked_at timestamptz,
  retries integer not null default 0,
  last_error text,
  dc_event_id bigint
);

comment on table v7_worker.result_submission is
  'Worker result buffer. Worker writes result here, then submits to dcse_cp.agent_task_events.
   If dcse_cp write fails, retry loop uses this record to replay.
   Decouple worker session lifetime from result durability.';

create index idx_v7_worker_result_submission_task on v7_worker.result_submission(task_id);
create index idx_v7_worker_result_submission_agent on v7_worker.result_submission(agent_id);
create index idx_v7_worker_result_submission_status on v7_worker.result_submission(submission_status);
create index idx_v7_worker_result_submission_pending on v7_worker.result_submission(submission_attempted_at)
  where submission_status in ('pending', 'retrying');

alter table v7_worker.result_submission enable row level security;

create policy "workers_write_own_results" on v7_worker.result_submission
  for all to authenticated, anon
  using (agent_id = current_setting('app.worker_id', true)::text)
  with check (agent_id = current_setting('app.worker_id', true)::text);

create policy "service_role_full_access" on v7_worker.result_submission
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 6. DEAD LETTER AND RETRY POLICY
-- ============================================================================

-- Dead-letter record: task exhausted retries or hit policy violation
create table v7_worker.dead_letter (
  dead_letter_id bigint generated always as identity primary key,
  task_id text not null,
  queue_msg_id bigint,
  lane text not null,
  task_type text not null,
  reason text not null,
  attempts integer not null default 0,
  last_claim_by text,
  last_error_message text,
  policy_violated text,
  requires_manual_escalation boolean not null default true,
  escalated_to_cp boolean not null default false,
  escalated_at timestamptz,
  moved_at timestamptz not null default now(),
  runtime_packet jsonb
);

comment on table v7_worker.dead_letter is
  'Tasks that exhausted retries, hit cost/time limits, raised Stop-Gate,
   or triggered a policy violation. Requires manual review or escalation to CP.';

create index idx_v7_worker_dead_letter_task on v7_worker.dead_letter(task_id);
create index idx_v7_worker_dead_letter_lane on v7_worker.dead_letter(lane);
create index idx_v7_worker_dead_letter_reason on v7_worker.dead_letter(reason);
create index idx_v7_worker_dead_letter_escalation on v7_worker.dead_letter(escalated_to_cp, moved_at desc);

alter table v7_worker.dead_letter enable row level security;

create policy "service_role_full_access" on v7_worker.dead_letter
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 7. WORKER COST AND RUNTIME TRACKING
-- ============================================================================

-- Per-worker and per-task cost tracking to enforce limits
create table v7_worker.cost_ledger (
  ledger_id bigint generated always as identity primary key,
  agent_id text not null references v7_worker.agent_identity(agent_id),
  task_id text,
  billing_period date not null,
  event_type text not null check (event_type in ('api_call', 'session_start', 'session_end', 'token_usage', 'manual_adjustment')),
  cost_usd numeric(10, 4) not null,
  units integer,
  unit_type text,
  metadata jsonb,
  recorded_at timestamptz not null default now()
);

comment on table v7_worker.cost_ledger is
  'Cost tracking per agent per billing period. Used to enforce monthly_cost_limit_usd.
   Captures API calls, session costs, token usage, and manual adjustments.';

create index idx_v7_worker_cost_ledger_agent_period on v7_worker.cost_ledger(agent_id, billing_period);
create index idx_v7_worker_cost_ledger_period on v7_worker.cost_ledger(billing_period);

alter table v7_worker.cost_ledger enable row level security;

create policy "workers_read_own_costs" on v7_worker.cost_ledger
  for select to authenticated, anon
  using (agent_id = current_setting('app.worker_id', true)::text);

create policy "service_role_full_access" on v7_worker.cost_ledger
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 8. STOP-GATE AND APPROVAL OVERRIDE
-- ============================================================================

-- Stop-Gate: block execution, request manual approval, escalate decision
create table v7_worker.stop_gate (
  gate_id bigint generated always as identity primary key,
  task_id text not null,
  agent_id text not null,
  gate_type text not null check (gate_type in ('security', 'privacy', 'policy_violation', 'manual_hold', 'cost_overrun', 'deadline_exceeded')),
  description text not null,
  requires_dcs_approval boolean not null default true,
  approval_deadline timestamptz,
  approver_id text,
  approved_at timestamptz,
  approval_decision text check (approval_decision in ('approved', 'rejected', 'modify_and_retry')),
  approval_notes text,
  raised_at timestamptz not null default now()
);

comment on table v7_worker.stop_gate is
  'Block execution pending manual approval. Used for security, privacy, policy, cost, deadline.
   DCS approval resolves gate; worker resumes or abandons task based on decision.';

create index idx_v7_worker_stop_gate_task on v7_worker.stop_gate(task_id);
create index idx_v7_worker_stop_gate_pending on v7_worker.stop_gate(raised_at desc)
  where approved_at is null;

alter table v7_worker.stop_gate enable row level security;

create policy "service_role_full_access" on v7_worker.stop_gate
  for all to service_role
  using (true)
  with check (true);

-- ============================================================================
-- 9. HELPER FUNCTIONS FOR WORKER OPERATIONS
-- ============================================================================

-- Claim next eligible task from queue
-- Returns the runtime_packet and queue_msg_id for the worker to execute
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
set search_path = public, v7_worker
as $$
declare
  v_message_row record;
  v_attempt_count integer;
  v_max_attempts integer;
  v_agent_row record;
begin
  -- Verify agent exists and is approved
  select * into v_agent_row from v7_worker.agent_identity
  where agent_id = p_agent_id and status = 'approved'
  for update;

  if v_agent_row is null then
    raise exception 'Agent % not found or not approved', p_agent_id;
  end if;

  -- Check agent is not already running task
  if v_agent_row.max_concurrent_tasks = 1 then
    if exists(
      select 1 from v7_worker.task_claim
      where agent_id = p_agent_id and released_at is null
        and visibility_timeout_at > now()
    ) then
      return; -- no rows: agent has active lease
    end if;
  end if;

  -- Read next highest-priority message from queue where agent is authorized for lane
  select
    qm.msg_id, qm.task_id, qm.lane, qm.task_type, qm.priority, qm.runtime_packet,
    coalesce((select count(*)::int from v7_worker.task_claim where task_id = qm.task_id), 0) as attempts
  into v_message_row
  from v7_worker.queue_message qm
  where qm.dead_lettered_at is null
    and qm.lane = any(v_agent_row.authorized_lanes)
    and qm.task_type = any(v_agent_row.authorized_task_types)
    and not exists(
      select 1 from v7_worker.task_claim tc
      where tc.queue_msg_id = qm.msg_id
        and tc.released_at is null
        and tc.visibility_timeout_at > now()
    )
  order by qm.priority desc, qm.enqueued_at asc
  limit 1
  for update skip locked;

  if v_message_row is null then
    return; -- no eligible messages
  end if;

  -- Validate attempt count hasn't exceeded max
  v_max_attempts := v_agent_row.max_attempts_per_task;
  if v_message_row.attempts >= v_max_attempts then
    -- Move to dead letter
    insert into v7_worker.dead_letter (
      task_id, queue_msg_id, lane, task_type, reason, attempts, last_claim_by, policy_violated, runtime_packet
    ) values (
      v_message_row.task_id, v_message_row.msg_id, v_message_row.lane, v_message_row.task_type,
      'Max attempts exceeded', v_message_row.attempts, p_agent_id, 'max_retries', v_message_row.runtime_packet
    );
    update v7_worker.queue_message set dead_lettered_at = now(), dead_letter_reason = 'Max attempts'
    where msg_id = v_message_row.msg_id;
    return; -- no rows
  end if;

  -- Record claim with visibility timeout
  insert into v7_worker.task_claim (
    queue_msg_id, task_id, agent_id, lane, task_type,
    visibility_timeout_at, lease_expires_at, attempt_number
  ) values (
    v_message_row.msg_id, v_message_row.task_id, p_agent_id, v_message_row.lane, v_message_row.task_type,
    now() + (p_visibility_timeout_seconds || ' seconds')::interval,
    now() + (p_visibility_timeout_seconds || ' seconds')::interval,
    v_message_row.attempts + 1
  );

  -- Update queue message to reflect claim
  update v7_worker.queue_message set
    last_claimed_by = p_agent_id,
    last_claim_at = now(),
    read_count = read_count + 1
  where msg_id = v_message_row.msg_id;

  -- Return result to worker
  return query select
    v_message_row.msg_id, v_message_row.task_id, v_message_row.lane,
    v_message_row.task_type, v_message_row.priority, v_message_row.runtime_packet,
    v_message_row.attempts + 1;
end;
$$;

-- Send worker heartbeat (liveness + metrics snapshot)
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
set search_path = public, v7_worker
as $$
declare
  v_new_id bigint;
  v_metrics jsonb;
begin
  -- Verify agent exists
  if not exists(select 1 from v7_worker.agent_identity where agent_id = p_agent_id) then
    raise exception 'Agent % not found', p_agent_id;
  end if;

  -- Update agent last_heartbeat_at
  update v7_worker.agent_identity set last_heartbeat_at = now() where agent_id = p_agent_id;

  -- Use provided metrics or fetch from ledger
  if p_metrics is null then
    select jsonb_build_object(
      'tasks_claimed', coalesce((select count(*) from v7_worker.task_claim where agent_id = p_agent_id), 0),
      'tasks_completed', coalesce((select count(*) from v7_worker.result_submission where agent_id = p_agent_id and submission_status = 'acked'), 0),
      'tasks_failed', coalesce((select count(*) from v7_worker.dead_letter where last_claim_by = p_agent_id), 0),
      'total_cost_usd', coalesce((select sum(cost_usd)::numeric(10,2) from v7_worker.cost_ledger where agent_id = p_agent_id), 0)
    ) into v_metrics;
  else
    v_metrics := p_metrics;
  end if;

  -- Insert heartbeat record
  insert into v7_worker.heartbeat (
    agent_id, current_task_id, status, current_lane, workspace_path, branch_name,
    model_version, capabilities, metrics
  ) values (
    p_agent_id, p_current_task_id, p_status, p_current_lane, p_workspace_path, p_branch_name,
    coalesce(p_model_version, ''), p_capabilities, v_metrics
  )
  returning heartbeat.heartbeat_id, heartbeat.sent_at into v_new_id, return query select v_new_id, heartbeat.sent_at;
end;
$$;

-- Release/acknowledge a task claim (worker completed or released)
create or replace function v7_worker.release_task_claim(
  p_claim_id bigint,
  p_agent_id text,
  p_reason text
)
returns table(success boolean, message text)
language plpgsql
security definer
set search_path = public, v7_worker
as $$
declare
  v_claim v7_worker.task_claim%rowtype;
begin
  -- Fetch and verify claim ownership
  select * into v_claim from v7_worker.task_claim
  where claim_id = p_claim_id and agent_id = p_agent_id
  for update;

  if v_claim is null then
    return query select false, 'Claim not found or agent mismatch';
    return;
  end if;

  if v_claim.released_at is not null then
    return query select false, 'Claim already released';
    return;
  end if;

  -- Release the claim
  update v7_worker.task_claim set
    released_at = now(),
    release_reason = p_reason
  where claim_id = p_claim_id;

  -- If reason is failure/timeout, visibility timeout expires and queue resets
  if p_reason in ('timeout', 'error', 'worker_crash') then
    update v7_worker.queue_message set read_count = read_count + 1
    where msg_id = v_claim.queue_msg_id;
  end if;

  return query select true, 'Claim released: ' || p_reason;
end;
$$;

-- ============================================================================
-- 10. RLS HELPERS AND GRANTS
-- ============================================================================

-- Grant v7_worker schema access to service role only (initial policy)
revoke all on schema v7_worker from public, anon, authenticated;
revoke all on all tables in schema v7_worker from public, anon, authenticated;
revoke all on all sequences in schema v7_worker from public, anon, authenticated;

grant usage on schema v7_worker to service_role;
grant all on all tables in schema v7_worker to service_role;
grant all on all sequences in schema v7_worker to service_role;
grant all on all functions in schema v7_worker to service_role;

-- Workers can execute claim_next_task and send_heartbeat through service-role proxy
-- (The application layer calls via Supabase client with SET app.worker_id)
grant execute on function v7_worker.claim_next_task(text, integer) to authenticated, anon;
grant execute on function v7_worker.send_heartbeat(text, text, text, text, text, text, text, jsonb, jsonb) to authenticated, anon;
grant execute on function v7_worker.release_task_claim(bigint, text, text) to authenticated, anon;

-- ============================================================================
-- 11. INITIAL AGENT REGISTRY SEEDING (examples for testing)
-- ============================================================================

-- Example: Qwen Code worker
insert into v7_worker.agent_identity (
  agent_id, agent_name, model_family, device_id, device_hostname, authorized_lanes, authorized_task_types,
  approval_mode, max_concurrent_tasks, max_wall_time_minutes, max_session_turns, max_attempts_per_task,
  monthly_cost_limit_usd, status
) values (
  'AGENT-QWEN-CODER-01@LAPTOP-PRIMARY',
  'Qwen Build Worker (Primary)',
  'qwen',
  'LAPTOP-PRIMARY',
  'dev-machine-01.local',
  '{DCSE,RAG,DDNA,SYSTEM}'::text[],
  '{schema_generation,script,extraction,migration,implementation,repair}'::text[],
  'auto-edit',
  1,
  30,
  30,
  3,
  150.00,
  'candidate'
)
on conflict do nothing;

-- Example: Claude Agent worker
insert into v7_worker.agent_identity (
  agent_id, agent_name, model_family, device_id, device_hostname, authorized_lanes, authorized_task_types,
  approval_mode, max_concurrent_tasks, max_wall_time_minutes, max_session_turns, max_attempts_per_task,
  monthly_cost_limit_usd, status
) values (
  'AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY',
  'Claude Architecture Reviewer',
  'claude',
  'LAPTOP-PRIMARY',
  'dev-machine-01.local',
  '{DCSE,SC}'::text[],
  '{blueprint,architecture_review,doctrine_reconciliation,evaluation}'::text[],
  'plan-only',
  1,
  20,
  15,
  2,
  100.00,
  'candidate'
)
on conflict do nothing;

-- Example: Deterministic validator worker
insert into v7_worker.agent_identity (
  agent_id, agent_name, model_family, device_id, device_hostname, authorized_lanes, authorized_task_types,
  approval_mode, max_concurrent_tasks, max_wall_time_minutes, max_session_turns, max_attempts_per_task,
  monthly_cost_limit_usd, status
) values (
  'AGENT-DETERMINISTIC-VALIDATOR-01@LAPTOP-PRIMARY',
  'Deterministic Validation Worker',
  'deterministic',
  'LAPTOP-PRIMARY',
  'dev-machine-01.local',
  '{DCSE,SYSTEM}'::text[],
  '{validation,test_execution,schema_check,rls_test,acceptance_criteria}'::text[],
  'read-only',
  4,
  10,
  5,
  1,
  10.00,
  'candidate'
)
on conflict do nothing;

-- ============================================================================
-- 12. INTEGRATION BRIDGE: v7_worker -> dcse_cp
-- ============================================================================

-- NOTE: v7_worker tables operate independently but with functions to bridge
-- results back to dcse_cp.agent_tasks and dcse_cp.agent_task_events.
-- This allows v7_worker to handle queue durability and worker orchestration,
-- while dcse_cp maintains the canonical task and event audit log.
--
-- The bridge function is not created here; it belongs in the application layer
-- or a separate migration that connects the two schemas (v7_worker + dcse_cp).

comment on schema v7_worker is
  'DCSE V7 Agent Worker Runtime. Persistent headless workers claim tasks here,
   execute via Qwen Code/Claude Agent SDK/Codex, and write results back.
   Provides: heartbeat, queue claims with visibility timeout, cost tracking,
   stop-gates, dead-letter queue, and RLS-scoped worker identity.

   Integration: v7_worker holds queue+claims, dcse_cp holds canonical events.
   Bridge: application or cron pulls results from v7_worker.result_submission
   and writes to dcse_cp.agent_task_events, then acks in v7_worker.';
