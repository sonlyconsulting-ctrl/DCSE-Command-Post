-- ============================================================================
-- DCSE V7 — Capture production hot-fixes + complete search_path lockdown
-- ============================================================================
-- Second half of the RLS hardening work. Split from the restricted-RPC
-- migration so that each locally-tracked file corresponds 1:1 with a version
-- recorded in supabase_migrations.schema_migrations on the preview branch.
--
-- Remediates: D11 (production hot-fixes never captured in migrations)
--             D8-residual (three SECURITY DEFINER functions still carrying
--                          the mutable search_path "public, v7_worker")
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 9. D11 - capture production hot-fixes that were never migrated
--     Production was patched in place for both of these; the repo migrations
--     still carried the defective definitions, so any fresh deployment
--     reintroduced them. Captured here so preview == production == fresh.
-- ---------------------------------------------------------------------------

-- dcse_cp.agent_task_events.id is a UUID; a bigint column cannot hold it.
alter table v7_worker.result_submission
  alter column dc_event_id type text using dc_event_id::text;

drop function if exists v7_worker.acknowledge_result_processed(bigint, bigint);

create or replace function v7_worker.acknowledge_result_processed(
  p_submission_id bigint,
  p_dc_event_id text
)
returns table(success boolean, message text)
language plpgsql
security definer
set search_path = ''
as $$
begin
  update v7_worker.result_submission
    set submission_status = 'acked',
        submission_acked_at = now(),
        dc_event_id = p_dc_event_id
  where submission_id = p_submission_id;

  if not found then
    return query select false, 'Submission not found';
    return;
  end if;

  return query select true, 'Result acknowledged and linked to dcse_cp event';
end;
$$;

-- ---------------------------------------------------------------------------
-- 10. D8 completion - remaining SECURITY DEFINER functions get empty search_path
-- ---------------------------------------------------------------------------
create or replace function v7_worker.check_pending_stop_gates()
returns table(pending_gates integer)
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_gate_count integer;
begin
  select count(*) into v_gate_count
  from v7_worker.stop_gate
  where approved_at is null
    and raised_at < now() - interval '2 hours'
    and requires_dcs_approval = true;

  return query select v_gate_count;
end;
$$;

create or replace function v7_worker.result_bridge_invoke()
returns text
language plpgsql
security definer
set search_path = ''
as $$
begin
  return 'bridge_cycle_queued';
exception when others then
  return 'bridge_cycle_error: ' || sqlerrm;
end;
$$;

revoke all on function v7_worker.acknowledge_result_processed(bigint, text) from public, anon, authenticated;
revoke all on function v7_worker.check_pending_stop_gates() from public, anon, authenticated;
revoke all on function v7_worker.result_bridge_invoke() from public, anon, authenticated;

grant execute on function v7_worker.acknowledge_result_processed(bigint, text) to service_role;
grant execute on function v7_worker.check_pending_stop_gates() to service_role;
grant execute on function v7_worker.result_bridge_invoke() to service_role;
