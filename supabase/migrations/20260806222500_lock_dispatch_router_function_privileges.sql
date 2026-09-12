-- Restrict V7.1 dispatch-router helpers to their intended execution surfaces.
-- auto_route_cp_dispatch_task() is trigger-only and must not be callable through
-- PostgREST. route_task_assignment() is service-role only for controlled repair
-- and reconciliation operations.

revoke all on function dcse_cp.auto_route_cp_dispatch_task() from public;
revoke all on function dcse_cp.auto_route_cp_dispatch_task() from anon;
revoke all on function dcse_cp.auto_route_cp_dispatch_task() from authenticated;
revoke all on function dcse_cp.auto_route_cp_dispatch_task() from service_role;

revoke all on function dcse_cp.route_task_assignment(uuid, text) from public;
revoke all on function dcse_cp.route_task_assignment(uuid, text) from anon;
revoke all on function dcse_cp.route_task_assignment(uuid, text) from authenticated;
grant execute on function dcse_cp.route_task_assignment(uuid, text) to service_role;
