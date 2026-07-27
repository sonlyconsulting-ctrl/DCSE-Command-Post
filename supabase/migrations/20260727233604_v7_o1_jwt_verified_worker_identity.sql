-- O1: per-worker authenticated identity.
-- Identity is derived ONLY from Supabase-verified app_metadata claims.
-- The app.worker_id GUC fallback is removed; it was client-settable.

create schema if not exists v7_worker_api;
revoke all on schema v7_worker_api from public;
grant usage on schema v7_worker_api to authenticated, service_role;

comment on schema v7_worker_api is
  'Worker-facing RPC surface. Every function derives the acting agent from the
   verified JWT app_metadata.agent_id claim. No function accepts an agent_id
   argument, so a caller cannot assert an identity it does not hold.';

create or replace function v7_worker_private.session_agent_id()
returns text language plpgsql stable security definer set search_path = '' as $$
declare v_claims jsonb; v_agent text;
begin
  begin
    v_claims := nullif(current_setting('request.jwt.claims', true), '')::jsonb;
  exception when others then
    return null;
  end;
  if v_claims is null then return null; end if;

  -- app_metadata is written only by the admin API / service role.
  -- user_metadata is self-writable and is deliberately NOT consulted.
  v_agent := v_claims -> 'app_metadata' ->> 'agent_id';
  if v_agent is null or v_agent = '' then return null; end if;
  return v_agent;
end $$;

comment on function v7_worker_private.session_agent_id() is
  'Returns the acting agent from the verified app_metadata.agent_id claim, or
   NULL. Never consults user_metadata or any client-settable GUC.';

create or replace function v7_worker_private.require_approved_agent()
returns v7_worker.agent_identity
language plpgsql stable security definer set search_path = '' as $$
declare v_agent text; v_row v7_worker.agent_identity%rowtype;
begin
  v_agent := v7_worker_private.session_agent_id();
  if v_agent is null then
    raise exception 'no verified agent identity on this session' using errcode = '42501';
  end if;

  select * into v_row from v7_worker.agent_identity where agent_id = v_agent;
  if not found then
    raise exception 'agent % is not registered', v_agent using errcode = '42501';
  end if;
  if v_row.status <> 'approved' then
    raise exception 'agent % is % and is not authorised to act', v_agent, v_row.status
      using errcode = '42501';
  end if;
  return v_row;
end $$;

create or replace function v7_worker_api.whoami()
returns table(agent_id text, status text, authorized_lanes text[], authorized_task_types text[])
language plpgsql stable security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();
  return query select v_row.agent_id, v_row.status, v_row.authorized_lanes, v_row.authorized_task_types;
end $$;

create or replace function v7_worker_api.heartbeat(
  p_status text, p_current_task_id text default null, p_current_lane text default null,
  p_model_version text default null, p_capabilities jsonb default '{}'::jsonb, p_metrics jsonb default null)
returns table(heartbeat_id bigint, recorded_at timestamptz)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();
  return query select * from v7_worker.send_heartbeat(
    v_row.agent_id, p_status, p_current_task_id, p_current_lane,
    null, null, p_model_version, p_capabilities, p_metrics);
end $$;

create or replace function v7_worker_api.claim_next_task(p_visibility_timeout_seconds integer default 1800)
returns table(queue_msg_id bigint, task_id text, lane text, task_type text,
              priority integer, runtime_packet jsonb, attempt_number integer)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();
  if p_visibility_timeout_seconds is null
     or p_visibility_timeout_seconds < 60 or p_visibility_timeout_seconds > 7200 then
    raise exception 'visibility timeout must be between 60 and 7200 seconds' using errcode = '22023';
  end if;
  return query select * from v7_worker.claim_next_task(v_row.agent_id, p_visibility_timeout_seconds);
end $$;

create or replace function v7_worker_api.renew_claim(p_claim_id bigint, p_extend_seconds integer default 1800)
returns table(success boolean, new_timeout timestamptz)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype; v_claim v7_worker.task_claim%rowtype; v_new timestamptz;
begin
  v_row := v7_worker_private.require_approved_agent();
  select * into v_claim from v7_worker.task_claim
   where claim_id = p_claim_id and agent_id = v_row.agent_id for update;
  if not found then
    raise exception 'claim % not found for agent %', p_claim_id, v_row.agent_id using errcode = '42501';
  end if;
  if v_claim.released_at is not null then
    raise exception 'claim % already released', p_claim_id using errcode = '55000';
  end if;
  v_new := now() + make_interval(secs => p_extend_seconds);
  update v7_worker.task_claim set visibility_timeout_at = v_new, lease_expires_at = v_new
   where claim_id = p_claim_id;
  return query select true, v_new;
end $$;

create or replace function v7_worker_api.submit_result(
  p_claim_id bigint, p_event_type text, p_output jsonb, p_worker_session_id text default null)
returns table(submission_id bigint, submitted_at timestamptz)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype; v_claim v7_worker.task_claim%rowtype; v_id bigint; v_at timestamptz;
begin
  v_row := v7_worker_private.require_approved_agent();
  select * into v_claim from v7_worker.task_claim
   where claim_id = p_claim_id and agent_id = v_row.agent_id;
  if not found then
    raise exception 'claim % not found for agent %', p_claim_id, v_row.agent_id using errcode = '42501';
  end if;
  insert into v7_worker.result_submission
    (task_id, claim_id, agent_id, submission_status, result_event_type, result_output, worker_session_id)
  values
    (v_claim.task_id, p_claim_id, v_row.agent_id, 'pending', p_event_type, p_output, p_worker_session_id)
  returning result_submission.submission_id, result_submission.submission_attempted_at into v_id, v_at;
  return query select v_id, v_at;
end $$;

create or replace function v7_worker_api.release_claim(p_claim_id bigint, p_reason text)
returns table(success boolean, message text)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();
  return query select * from v7_worker.release_task_claim(p_claim_id, v_row.agent_id, p_reason);
end $$;

create or replace function v7_worker.bind_agent_identity(p_agent_id text, p_user_id uuid)
returns table(success boolean, message text)
language plpgsql security definer set search_path = '' as $$
begin
  if not exists (select 1 from v7_worker.agent_identity where agent_id = p_agent_id) then
    return query select false, 'agent not registered: ' || p_agent_id; return;
  end if;
  if not exists (select 1 from auth.users where id = p_user_id) then
    return query select false, 'auth user not found'; return;
  end if;
  update auth.users
     set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
                             || jsonb_build_object('agent_id', p_agent_id)
   where id = p_user_id;
  return query select true, 'bound ' || p_agent_id || ' to auth user';
end $$;

revoke all on function v7_worker_private.session_agent_id() from public, anon, authenticated;
revoke all on function v7_worker_private.require_approved_agent() from public, anon, authenticated;
revoke all on function v7_worker.bind_agent_identity(text, uuid) from public, anon, authenticated;
grant execute on function v7_worker.bind_agent_identity(text, uuid) to service_role;

revoke all on function v7_worker_api.whoami() from public, anon;
revoke all on function v7_worker_api.heartbeat(text,text,text,text,jsonb,jsonb) from public, anon;
revoke all on function v7_worker_api.claim_next_task(integer) from public, anon;
revoke all on function v7_worker_api.renew_claim(bigint,integer) from public, anon;
revoke all on function v7_worker_api.submit_result(bigint,text,jsonb,text) from public, anon;
revoke all on function v7_worker_api.release_claim(bigint,text) from public, anon;

grant execute on function v7_worker_api.whoami() to authenticated, service_role;
grant execute on function v7_worker_api.heartbeat(text,text,text,text,jsonb,jsonb) to authenticated, service_role;
grant execute on function v7_worker_api.claim_next_task(integer) to authenticated, service_role;
grant execute on function v7_worker_api.renew_claim(bigint,integer) to authenticated, service_role;
grant execute on function v7_worker_api.submit_result(bigint,text,jsonb,text) to authenticated, service_role;
grant execute on function v7_worker_api.release_claim(bigint,text) to authenticated, service_role;
