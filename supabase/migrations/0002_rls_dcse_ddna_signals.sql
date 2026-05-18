-- Migration: 0002_rls_dcse_ddna_signals
-- GATE: DCS approval required before applying.
-- Purpose: Enable RLS on dcse_ddna_signals and add least-privilege policies.
--
-- dcse_ddna_signals holds per-session AI model signal data (sentiment, logic,
-- design, product, technical scores). Without RLS any authenticated caller can
-- read or write all rows, which violates DCSE data isolation requirements.

alter table public.dcse_ddna_signals enable row level security;

-- Service-role bypass (Supabase edge functions run as service-role)
create policy "service_role_all_ddna_signals"
  on public.dcse_ddna_signals
  as permissive
  for all
  to service_role
  using (true)
  with check (true);

-- Authenticated users may only read rows tied to their own session
create policy "authenticated_read_own_ddna_signals"
  on public.dcse_ddna_signals
  as permissive
  for select
  to authenticated
  using (
    -- handoff_key is expected to encode the owning user/session; adjust the
    -- column reference if the FK to auth.users is named differently.
    handoff_key = (select auth.uid()::text)
  );

-- No direct INSERT/UPDATE/DELETE for authenticated users — writes go via
-- the dcse_trigger_ddna_extraction edge function (service-role context).
