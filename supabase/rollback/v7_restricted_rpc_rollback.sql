-- ============================================================================
-- ROLLBACK for 20260729_v7_restricted_rpc_and_rls_hardening.sql
-- ============================================================================
-- Reverses the hardening in dependency-safe order. Every statement targets an
-- object created or altered by the forward migration; none touch pre-existing
-- v7_worker tables or data.
--
-- WARNING: applying this rollback restores defects D1-D11. It exists to
-- satisfy reversibility review, not as a recommended operation.
-- ============================================================================

-- 1. Integrity triggers (D4, D6)
drop trigger if exists trg_result_submission_active_lease on v7_worker.result_submission;
drop trigger if exists trg_task_claim_guard              on v7_worker.task_claim;

-- 2. Integrity constraints (D3, D5)
drop index      if exists v7_worker.uq_result_submission_claim_event;
alter table v7_worker.result_submission
  drop constraint if exists result_submission_claim_id_fkey;

-- 3. Private helpers (D6, D9)
drop function if exists v7_worker_private.enforce_active_lease();
drop function if exists v7_worker_private.guard_claim_mutation();
drop function if exists v7_worker_private.session_agent_id();
drop schema   if exists v7_worker_private cascade;

-- 4. Restore the permissive RPC surface (D8, D9)
--    Reinstates search_path = "public, v7_worker" and PUBLIC execute.
alter function v7_worker.claim_next_task(text, integer)              set search_path = public, v7_worker;
alter function v7_worker.send_heartbeat(text,text,text,text,text,text,text,jsonb,jsonb) set search_path = public, v7_worker;
alter function v7_worker.release_task_claim(bigint, text, text)      set search_path = public, v7_worker;
alter function v7_worker.dispatcher_recovery_cycle()                 set search_path = public, v7_worker;
alter function v7_worker.result_bridge_invoke()                      set search_path = public, v7_worker;
alter function v7_worker.check_pending_stop_gates()                  set search_path = public, v7_worker;

grant execute on function v7_worker.claim_next_task(text, integer)   to public, anon, authenticated;
grant execute on function v7_worker.send_heartbeat(text,text,text,text,text,text,text,jsonb,jsonb) to public, anon, authenticated;
grant execute on function v7_worker.release_task_claim(bigint,text,text) to public, anon, authenticated;

-- 5. Revert the production hot-fix capture (D11)
--    NOTE: dc_event_id currently holds UUID strings from dcse_cp. Reverting to
--    bigint will FAIL if any non-numeric value is present. Purge first, which
--    is why this step is listed last and is explicitly destructive.
-- update v7_worker.result_submission set dc_event_id = null;
-- alter table v7_worker.result_submission alter column dc_event_id type bigint using dc_event_id::bigint;
-- drop function if exists v7_worker.acknowledge_result_processed(bigint, text);
