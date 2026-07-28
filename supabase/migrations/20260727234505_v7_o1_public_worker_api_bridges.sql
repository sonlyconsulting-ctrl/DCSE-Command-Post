-- Workers reach the database over PostgREST, which only routes to exposed
-- schemas. v7_worker_api is deliberately not exposed, so these public bridges
-- are the reachable surface.
--
-- Safe to expose: every bridge delegates to a v7_worker_api function that
-- re-derives the acting agent from the verified app_metadata.agent_id claim and
-- rejects any caller lacking one. Granting to `authenticated` therefore grants
-- nothing to an ordinary user; it only lets an enrolled worker act as itself.

create or replace function public.v7_worker_whoami()
returns table(agent_id text, status text, authorized_lanes text[], authorized_task_types text[])
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.whoami();
$$;

create or replace function public.v7_worker_heartbeat(
  p_status text, p_current_task_id text default null, p_current_lane text default null,
  p_model_version text default null, p_capabilities jsonb default '{}'::jsonb, p_metrics jsonb default null)
returns table(heartbeat_id bigint, recorded_at timestamptz)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.heartbeat(
    p_status, p_current_task_id, p_current_lane, p_model_version, p_capabilities, p_metrics);
$$;

create or replace function public.v7_worker_claim_next_task(p_visibility_timeout_seconds integer default 1800)
returns table(claim_id bigint, queue_msg_id bigint, task_id text, lane text,
              task_type text, priority integer, runtime_packet jsonb,
              attempt_number integer, visibility_timeout_at timestamptz)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.claim_next_task(p_visibility_timeout_seconds);
$$;

create or replace function public.v7_worker_my_active_claims()
returns table(claim_id bigint, task_id text, lane text, task_type text,
              visibility_timeout_at timestamptz, attempt_number integer)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.my_active_claims();
$$;

create or replace function public.v7_worker_renew_claim(p_claim_id bigint, p_extend_seconds integer default 1800)
returns table(success boolean, new_timeout timestamptz)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.renew_claim(p_claim_id, p_extend_seconds);
$$;

create or replace function public.v7_worker_submit_result(
  p_claim_id bigint, p_event_type text, p_output jsonb, p_worker_session_id text default null)
returns table(submission_id bigint, submitted_at timestamptz)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.submit_result(p_claim_id, p_event_type, p_output, p_worker_session_id);
$$;

create or replace function public.v7_worker_release_claim(p_claim_id bigint, p_reason text)
returns table(success boolean, message text)
language sql security definer set search_path = '' as $$
  select * from v7_worker_api.release_claim(p_claim_id, p_reason);
$$;

do $g$
declare fn text;
begin
  foreach fn in array array[
    'public.v7_worker_whoami()',
    'public.v7_worker_heartbeat(text,text,text,text,jsonb,jsonb)',
    'public.v7_worker_claim_next_task(integer)',
    'public.v7_worker_my_active_claims()',
    'public.v7_worker_renew_claim(bigint,integer)',
    'public.v7_worker_submit_result(bigint,text,jsonb,text)',
    'public.v7_worker_release_claim(bigint,text)'
  ] loop
    execute format('revoke all on function %s from public, anon', fn);
    execute format('grant execute on function %s to authenticated, service_role', fn);
  end loop;
end $g$;
