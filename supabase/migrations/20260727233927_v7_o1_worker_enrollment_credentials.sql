-- Worker enrollment: binds an agent to an auth user and stores only a hash of
-- the enrollment secret. The plaintext secret is held by the worker and never
-- persisted server-side.

alter table v7_worker.agent_identity
  add column if not exists auth_user_id uuid,
  add column if not exists enrollment_secret_hash text,
  add column if not exists enrolled_at timestamptz;

create unique index if not exists uq_agent_identity_auth_user
  on v7_worker.agent_identity(auth_user_id) where auth_user_id is not null;

create or replace function v7_worker.provision_worker_credential(
  p_agent_id text, p_user_id uuid, p_enrollment_secret text)
returns table(success boolean, message text)
language plpgsql security definer set search_path = '' as $$
begin
  if p_enrollment_secret is null or length(p_enrollment_secret) < 24 then
    return query select false, 'enrollment secret must be at least 24 characters'; return;
  end if;
  if not exists (select 1 from v7_worker.agent_identity where agent_id = p_agent_id) then
    return query select false, 'agent not registered: ' || p_agent_id; return;
  end if;
  if not exists (select 1 from auth.users where id = p_user_id) then
    return query select false, 'auth user not found'; return;
  end if;

  update v7_worker.agent_identity
     set auth_user_id = p_user_id,
         enrollment_secret_hash = extensions.crypt(p_enrollment_secret, extensions.gen_salt('bf', 10)),
         enrolled_at = now()
   where agent_id = p_agent_id;

  update auth.users
     set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb)
                             || jsonb_build_object('agent_id', p_agent_id)
   where id = p_user_id;

  return query select true, 'provisioned ' || p_agent_id;
end $$;

create or replace function v7_worker.verify_worker_enrollment(p_agent_id text, p_enrollment_secret text)
returns table(valid boolean, reason text, auth_email text)
language plpgsql security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype; v_email text;
begin
  select * into v_row from v7_worker.agent_identity where agent_id = p_agent_id;
  if not found then return query select false, 'unknown agent', null::text; return; end if;
  if v_row.status <> 'approved' then
    return query select false, 'agent is ' || v_row.status, null::text; return;
  end if;
  if v_row.enrollment_secret_hash is null or v_row.auth_user_id is null then
    return query select false, 'agent not enrolled', null::text; return;
  end if;
  if v_row.enrollment_secret_hash <> extensions.crypt(p_enrollment_secret, v_row.enrollment_secret_hash) then
    return query select false, 'invalid enrollment secret', null::text; return;
  end if;

  select email into v_email from auth.users where id = v_row.auth_user_id;
  return query select true, 'ok', v_email;
end $$;

revoke all on function v7_worker.provision_worker_credential(text, uuid, text) from public, anon, authenticated;
revoke all on function v7_worker.verify_worker_enrollment(text, text) from public, anon, authenticated;
grant execute on function v7_worker.provision_worker_credential(text, uuid, text) to service_role;
grant execute on function v7_worker.verify_worker_enrollment(text, text) to service_role;

comment on function v7_worker.verify_worker_enrollment(text, text) is
  'bcrypt comparison of a presented enrollment secret. Returns the bound auth
   email so the token endpoint can broker a session. service_role only.';
