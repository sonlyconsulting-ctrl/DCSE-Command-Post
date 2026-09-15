-- dcse-classification: INTERNAL_SERVER_ONLY
-- task-id: DCSE-SUPABASE-HARDENING-20260915-001
-- rollback: do not disable RLS; restore only a proven service-role grant if required

alter table dcse_cp.runtime_host_registry enable row level security;
revoke all privileges on table dcse_cp.runtime_host_registry from public, anon, authenticated;
grant select, insert, update, delete on table dcse_cp.runtime_host_registry to service_role;
