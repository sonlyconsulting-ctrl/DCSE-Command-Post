-- ============================================================================
-- DCSE V7.1 — Capture production hot-fix: claim_agent_assignment TOCTOU repair
-- ============================================================================
-- Same defect category as D11 in 20260727231413_v7_capture_prod_hotfixes_and_
-- search_path.sql: this function was patched directly against the live
-- nevgdyfpxdaloacuutal project (CREATE OR REPLACE, no migration file, no PR,
-- no review) during work on task V7_1_ACTION_1_POLLER_HARDENING. A receipt
-- posted to dcse_cp.agent_task_events at 2026-08-03T04:46:06Z described the
-- fix; verified against the live function definition via
-- pg_get_functiondef() on 2026-08-03 and found to match that description
-- exactly. Capturing it here so preview == production == fresh deployment,
-- and so the fix is versioned and reviewable going forward.
--
-- Original defect: the SELECT that located the assignment row and the
-- UPDATE that claimed it were two separate statements, so two concurrent
-- callers could both pass the SELECT and both believe they had claimed the
-- same dcse_cp.agent_task_assignments row (classic TOCTOU).
--
-- Fix: the UPDATE itself is now the atomicity boundary — it only succeeds
-- when status is not already 'running' or 'completed', and the RPC checks
-- `if not found` on that UPDATE rather than trusting the earlier SELECT.
--
-- This migration is a no-op against the current live database (the function
-- already matches this definition); it exists purely to bring the tracked
-- schema back in sync with reality per this task's own test_before_patch /
-- production_changes:false policy, which the original hotfix bypassed.
-- ============================================================================

create or replace function dcse_cp.claim_agent_assignment(p_agent_key text, p_task_key text)
returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog', 'dcse_cp'
as $function$
declare
  v_agent_id uuid;
  v_task_id uuid;
  v_assignment_id uuid;
begin
  select id into v_agent_id from dcse_cp.agent_registry where agent_key = p_agent_key;
  select id into v_task_id from dcse_cp.agent_tasks where task_key = p_task_key;

  if v_agent_id is null or v_task_id is null then
    return jsonb_build_object('ok', false, 'error', 'agent_or_task_not_found');
  end if;

  select id into v_assignment_id
  from dcse_cp.agent_task_assignments
  where agent_id = v_agent_id and task_id = v_task_id
  limit 1;

  if v_assignment_id is null then
    return jsonb_build_object('ok', false, 'error', 'assignment_not_found');
  end if;

  -- Atomic claim: only succeeds if not already running/completed. Prevents the
  -- prior TOCTOU gap where two concurrent callers could both pass the SELECT
  -- above and both "claim" the same assignment.
  update dcse_cp.agent_task_assignments
  set status = 'running', updated_at = now()
  where id = v_assignment_id
    and status is distinct from 'running'
    and status is distinct from 'completed';

  if not found then
    return jsonb_build_object('ok', false, 'error', 'already_claimed_or_terminal');
  end if;

  update dcse_cp.agent_tasks
  set status = 'running', updated_at = now()
  where id = v_task_id
    and status in ('assigned','queued');

  perform dcse_cp.agent_heartbeat(p_agent_key, p_task_key, 'working', '{}'::jsonb, 'assignment claimed');

  insert into dcse_cp.agent_task_events(task_id, event_type, from_agent_id, actor_label, event_summary, event_payload)
  values(v_task_id, 'started', v_agent_id, p_agent_key, p_agent_key || ' claimed assignment for ' || p_task_key, jsonb_build_object('assignment_id', v_assignment_id));

  return jsonb_build_object('ok', true, 'assignment_id', v_assignment_id, 'task_key', p_task_key, 'agent_key', p_agent_key, 'status', 'running');
end;
$function$;
