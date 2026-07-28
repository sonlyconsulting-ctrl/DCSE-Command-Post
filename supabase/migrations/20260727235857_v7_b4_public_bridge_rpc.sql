-- PostgREST-reachable entry point for the deployed v7-result-bridge Edge Function.
-- v7_worker is not an exposed schema, so the function reaches the bridge here.
-- service_role only.
create or replace function public.v7_run_result_bridge(p_limit integer default 25)
returns table(processed integer, failed integer, skipped integer, duration_ms integer, receipt_id bigint)
language plpgsql security definer set search_path = '' as $$
begin
  return query select * from v7_worker.bridge_pending_results(p_limit);
end $$;

revoke all on function public.v7_run_result_bridge(integer) from public, anon, authenticated;
grant execute on function public.v7_run_result_bridge(integer) to service_role;
