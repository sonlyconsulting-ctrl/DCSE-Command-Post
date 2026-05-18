-- Migration: 0003_rls_model_activity_log
-- GATE: DCS approval required before applying.
-- Purpose: Enable RLS on model_activity_log; restrict writes to service-role,
--          restrict reads to admin/DCS roles only.
--
-- model_activity_log is an audit table. Allowing arbitrary INSERT undermines
-- audit integrity; allowing arbitrary SELECT leaks operational metadata.

alter table public.model_activity_log enable row level security;

-- Only service-role may write (INSERT) audit rows
create policy "service_role_insert_activity_log"
  on public.model_activity_log
  as permissive
  for insert
  to service_role
  with check (true);

-- service-role may also read (for tooling/dashboards running as service-role)
create policy "service_role_select_activity_log"
  on public.model_activity_log
  as permissive
  for select
  to service_role
  using (true);

-- DCS admin role may read — create this role in Supabase dashboard and assign
-- to DCS operator accounts before enabling this policy.
-- Uncomment after the 'dcse_admin' role has been provisioned:
--
-- create policy "dcse_admin_read_activity_log"
--   on public.model_activity_log
--   as permissive
--   for select
--   to dcse_admin
--   using (true);

-- No other roles may SELECT, INSERT, UPDATE, or DELETE.
