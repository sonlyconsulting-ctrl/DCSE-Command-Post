-- dcse-classification: INTERNAL_SERVER_ONLY
-- task-id: DCSE-SUPABASE-HARDENING-20260915-001
-- rollback: requires explicit DCS approval; never restore anonymous worker access

revoke usage on schema v7_worker from public, anon, authenticated;
revoke all privileges on all tables in schema v7_worker from public, anon, authenticated;
revoke all privileges on all sequences in schema v7_worker from public, anon, authenticated;
revoke execute on all functions in schema v7_worker from public, anon, authenticated;

alter default privileges for role postgres in schema v7_worker
  revoke all privileges on tables from public, anon, authenticated;
alter default privileges for role postgres in schema v7_worker
  revoke all privileges on sequences from public, anon, authenticated;
alter default privileges for role postgres in schema v7_worker
  revoke execute on functions from public, anon, authenticated;

grant usage on schema v7_worker to service_role;
grant all privileges on all tables in schema v7_worker to service_role;
grant all privileges on all sequences in schema v7_worker to service_role;
grant execute on all functions in schema v7_worker to service_role;

alter function v7_worker.claim_next_task(text, integer) set search_path = pg_catalog;
alter function v7_worker.release_task_claim(bigint, text, text) set search_path = pg_catalog;
alter function v7_worker.send_heartbeat(text, text, text, text, text, text, text, jsonb, jsonb)
  set search_path = pg_catalog;

revoke execute on function public.rls_auto_enable() from public, anon, authenticated;
