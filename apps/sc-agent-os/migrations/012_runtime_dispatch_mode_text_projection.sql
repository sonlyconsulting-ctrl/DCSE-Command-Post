-- Migration 012: expose text-only runtime dispatch mode for Windows controller.
--
-- The controller should not need to interpret PostgREST boolean values or
-- construct boolean filters. Supabase remains authoritative and returns a
-- simple text mode: normal (admitted) or preflight (not admitted).

begin;

create or replace view dcse_cp.autonomous_dispatch_runtime_state as
select
  agent_key,
  coalesce(metadata->>'admission_status', 'UNSPECIFIED') as admission_status,
  case when admitted_for_autonomous_claim then 'normal' else 'preflight' end as dispatch_mode
from dcse_cp.autonomous_dispatch_admission;

revoke all on dcse_cp.autonomous_dispatch_runtime_state from public, anon, authenticated;
grant select on dcse_cp.autonomous_dispatch_runtime_state to service_role;

commit;
