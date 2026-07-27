-- Defect O1-D2: the token endpoint called v7_worker.verify_worker_enrollment
-- through PostgREST, but v7_worker is not an exposed API schema (deliberately).
-- Every request failed with verification_failed.
--
-- Fix: a thin wrapper in public, which PostgREST does expose, executable ONLY by
-- service_role. anon and authenticated are explicitly revoked, so exposing the
-- name costs nothing: unauthorised callers cannot execute it.

create or replace function public.v7_verify_worker_enrollment(
  p_agent_id text, p_enrollment_secret text)
returns table(valid boolean, reason text, auth_email text)
language plpgsql security definer set search_path = '' as $$
begin
  return query select * from v7_worker.verify_worker_enrollment(p_agent_id, p_enrollment_secret);
end;
$$;

revoke all on function public.v7_verify_worker_enrollment(text, text) from public, anon, authenticated;
grant execute on function public.v7_verify_worker_enrollment(text, text) to service_role;

comment on function public.v7_verify_worker_enrollment(text, text) is
  'PostgREST-reachable bridge to v7_worker.verify_worker_enrollment. service_role only.';
