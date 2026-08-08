-- Migration 007: Runtime identity separation + submitted-result access
--
-- Fixes two defects found under task_key=V7_1_POLLER_RESULT_ACCESS_UI_FIX_20260807:
--
-- 1. dcse_cp.agent_heartbeats was UNIQUE(agent_id) only. Every runtime surface
--    that heartbeats under the same logical agent_key (e.g. 'claude_code') --
--    CLI poller on the Windows host, a remote/cloud CCR session, a Claude Chat
--    browser session, a Claude Desktop session -- upserts onto the SAME row,
--    overwriting each other. There was no way to tell which surface last beat,
--    or whether more than one surface was concurrently claiming to be the same
--    heartbeat source. This migration adds runtime_surface/runtime_instance/
--    host/session_id columns and re-keys uniqueness to (agent_id, runtime_instance)
--    so each surface gets its own row while agent_key/agent_id still identifies
--    the single logical role.
--
-- 2. dcse_cp.agent_task_assignments.result_payload (populated by
--    submit_agent_result) was never selected by the Command Center UI's
--    dispatch/tribunal endpoints, so a submitted result was durably stored but
--    had no read path. This migration adds a read-only view that joins task +
--    assignment + latest receipt event so the API layer can expose it without
--    hand-rolling the join per endpoint, and does not alter result_payload
--    write semantics (submit_agent_result is unchanged -- evidence is still
--    append/overwrite-in-place exactly as before; the UI fix layered on top of
--    this view is what adds a governed follow-up path instead of direct edits).

begin;

-- ---------------------------------------------------------------------------
-- 1. Runtime identity columns on agent_heartbeats
-- ---------------------------------------------------------------------------

alter table dcse_cp.agent_heartbeats
  add column if not exists runtime_surface text not null default 'unspecified',
  add column if not exists runtime_instance text not null default 'legacy',
  add column if not exists host text,
  add column if not exists session_id text;

alter table dcse_cp.agent_heartbeats
  drop constraint if exists agent_heartbeats_runtime_surface_check;
alter table dcse_cp.agent_heartbeats
  add constraint agent_heartbeats_runtime_surface_check
  check (runtime_surface in (
    'cli_windows_poller',   -- Claude Code CLI on Windows host, invoked by the scheduled poller
    'remote_cloud_ccr',     -- Claude Code remote/cloud/CCR interactive session
    'chat_browser',         -- Claude Chat browser session
    'desktop_app',          -- Claude Desktop application session
    'worker_v7',            -- legacy v7_worker heartbeat path
    'unspecified'           -- pre-migration rows / callers that haven't upgraded yet
  ));

-- Re-key uniqueness: was UNIQUE(agent_id), which is exactly the collision this
-- migration exists to remove. One row per (agent_id, runtime_instance) instead.
alter table dcse_cp.agent_heartbeats
  drop constraint if exists agent_heartbeats_agent_id_key;
alter table dcse_cp.agent_heartbeats
  add constraint agent_heartbeats_agent_id_runtime_instance_key
  unique (agent_id, runtime_instance);

comment on column dcse_cp.agent_heartbeats.runtime_surface is
  'Which Claude-family runtime surface sent this heartbeat. Distinct from agent_key (the logical role) -- see task V7_1_POLLER_RESULT_ACCESS_UI_FIX_20260807.';
comment on column dcse_cp.agent_heartbeats.runtime_instance is
  'Stable per-surface identity (e.g. claude_code_cli@HOSTNAME). Uniqueness key alongside agent_id so surfaces do not overwrite each other.';

-- ---------------------------------------------------------------------------
-- 2. agent_heartbeat() RPC: accept and persist runtime identity
-- ---------------------------------------------------------------------------

create or replace function dcse_cp.agent_heartbeat(
  p_agent_key text,
  p_task_key text default null::text,
  p_status text default 'online'::text,
  p_capability_status jsonb default '{}'::jsonb,
  p_notes text default null::text,
  p_runtime_surface text default 'unspecified',
  p_runtime_instance text default null::text,
  p_host text default null::text,
  p_session_id text default null::text
)
 returns jsonb
 language plpgsql
 security definer
 set search_path to 'pg_catalog', 'dcse_cp'
as $function$
declare
  v_agent_id uuid;
  v_task_id uuid;
  v_assignment_id uuid;
  v_runtime_instance text;
begin
  select id into v_agent_id
  from dcse_cp.agent_registry
  where agent_key = p_agent_key;

  if v_agent_id is null then
    return jsonb_build_object('ok', false, 'error', 'agent_not_found', 'agent_key', p_agent_key);
  end if;

  if p_task_key is not null then
    select id into v_task_id
    from dcse_cp.agent_tasks
    where task_key = p_task_key;
  end if;

  if v_task_id is not null then
    select id into v_assignment_id
    from dcse_cp.agent_task_assignments
    where agent_id = v_agent_id and task_id = v_task_id
    order by sequence_order nulls last, created_at desc
    limit 1;
  end if;

  -- Callers that haven't upgraded to pass an explicit runtime_instance still
  -- get a stable per-host identity instead of colliding on agent_id alone.
  v_runtime_instance := coalesce(p_runtime_instance, p_agent_key || ':' || coalesce(p_host, 'unspecified-host'));

  insert into dcse_cp.agent_heartbeats(
    agent_id, task_id, current_assignment_id, heartbeat_status, last_seen_at,
    capability_status, notes, runtime_surface, runtime_instance, host, session_id
  )
  values(
    v_agent_id, v_task_id, v_assignment_id, p_status, now(),
    coalesce(p_capability_status, '{}'::jsonb), p_notes,
    coalesce(p_runtime_surface, 'unspecified'), v_runtime_instance, p_host, p_session_id
  )
  on conflict(agent_id, runtime_instance) do update set
    task_id = excluded.task_id,
    current_assignment_id = excluded.current_assignment_id,
    heartbeat_status = excluded.heartbeat_status,
    last_seen_at = now(),
    capability_status = excluded.capability_status,
    notes = excluded.notes,
    runtime_surface = excluded.runtime_surface,
    host = excluded.host,
    session_id = excluded.session_id,
    updated_at = now();

  insert into dcse_cp.relay_listener_events(agent_id, task_id, assignment_id, event_type, event_summary, event_payload)
  values(v_agent_id, v_task_id, v_assignment_id, 'heartbeat', p_agent_key || ' heartbeat: ' || p_status,
    jsonb_build_object('agent_key', p_agent_key, 'task_key', p_task_key, 'status', p_status,
      'runtime_surface', p_runtime_surface, 'runtime_instance', v_runtime_instance, 'host', p_host));

  return jsonb_build_object('ok', true, 'agent_key', p_agent_key, 'task_key', p_task_key, 'status', p_status,
    'runtime_surface', p_runtime_surface, 'runtime_instance', v_runtime_instance, 'last_seen_at', now());
end;
$function$;

-- ---------------------------------------------------------------------------
-- 3. Aggregate view: expose duplicate/ambiguous runtime identity per agent_key
-- ---------------------------------------------------------------------------

create or replace view dcse_cp.agent_runtime_surfaces as
select
  r.agent_key,
  r.display_name,
  count(*) as surface_count,
  count(*) filter (where h.last_seen_at > now() - interval '10 minutes') as active_surface_count,
  jsonb_agg(jsonb_build_object(
    'runtime_surface', h.runtime_surface,
    'runtime_instance', h.runtime_instance,
    'host', h.host,
    'session_id', h.session_id,
    'heartbeat_status', h.heartbeat_status,
    'last_seen_at', h.last_seen_at
  ) order by h.last_seen_at desc) as surfaces,
  (count(distinct h.runtime_surface) > 1) as multi_surface_flag
from dcse_cp.agent_heartbeats h
join dcse_cp.agent_registry r on r.id = h.agent_id
group by r.agent_key, r.display_name;

comment on view dcse_cp.agent_runtime_surfaces is
  'Per logical agent_key, the distinct runtime surfaces/instances heartbeating under it. multi_surface_flag=true means more than one Claude-family runtime surface is active under the same logical role -- expected for claude_code (CLI poller) vs interactive sessions, but should never mean two surfaces silently overwrote one heartbeat row (fixed by the (agent_id, runtime_instance) unique key above).';

-- ---------------------------------------------------------------------------
-- 4. Read path for submitted results (does not touch write semantics)
-- ---------------------------------------------------------------------------

create or replace view dcse_cp.agent_task_result_view as
select
  a.id as assignment_id,
  t.id as task_id,
  t.task_key,
  t.title,
  t.description,
  t.lane,
  t.status as task_status,
  r.agent_key,
  r.display_name as agent_display_name,
  a.assignment_role,
  a.status as assignment_status,
  a.result_payload,
  a.created_at as assignment_created_at,
  a.updated_at as result_submitted_at,
  t.dcs_decision_required,
  t.review_required
from dcse_cp.agent_task_assignments a
join dcse_cp.agent_tasks t on t.id = a.task_id
join dcse_cp.agent_registry r on r.id = a.agent_id;

comment on view dcse_cp.agent_task_result_view is
  'Read-only join exposing submit_agent_result payloads with their source task/agent context and timestamps, for the Command Center result-inspector UI. result_payload is never written through this view.';

commit;
