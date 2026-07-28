-- B3: one-call enrollment. Codifies the O1-D3 fix: auth users created by raw
-- SQL must have GoTrue's token columns set to '' rather than NULL, or the
-- password grant fails with a scan error. Doing this by hand is error-prone,
-- so it lives in a function.
--
-- service_role only. The plaintext secret is never stored; provision_worker_credential
-- keeps only a bcrypt hash.

create or replace function v7_worker.enroll_worker(
  p_agent_id text, p_email text, p_enrollment_secret text)
returns table(success boolean, message text, auth_user_id uuid)
language plpgsql security definer set search_path = '' as $$
declare v_uid uuid; v_existing uuid; v_res record;
begin
  if p_enrollment_secret is null or length(p_enrollment_secret) < 24 then
    return query select false, 'enrollment secret must be at least 24 characters', null::uuid; return;
  end if;
  if not exists (select 1 from v7_worker.agent_identity where agent_id = p_agent_id) then
    return query select false, 'agent not registered: ' || p_agent_id, null::uuid; return;
  end if;

  select id into v_existing from auth.users where email = p_email;
  if v_existing is not null then
    delete from auth.identities where user_id = v_existing;
    delete from auth.users where id = v_existing;
  end if;

  v_uid := gen_random_uuid();

  insert into auth.users (
    instance_id, id, aud, role, email, encrypted_password,
    email_confirmed_at, created_at, updated_at,
    raw_app_meta_data, raw_user_meta_data, is_sso_user, is_anonymous,
    confirmation_token, recovery_token, email_change_token_new,
    email_change_token_current, email_change, phone_change,
    phone_change_token, reauthentication_token
  ) values (
    '00000000-0000-0000-0000-000000000000', v_uid, 'authenticated', 'authenticated',
    p_email, extensions.crypt(p_enrollment_secret, extensions.gen_salt('bf', 10)),
    now(), now(), now(),
    jsonb_build_object('provider','email','providers', jsonb_build_array('email')),
    '{}'::jsonb, false, false,
    '', '', '', '', '', '', '', ''      -- GoTrue cannot scan NULL into these
  );

  insert into auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at)
  values (v_uid::text, v_uid,
          jsonb_build_object('sub', v_uid::text, 'email', p_email, 'email_verified', true),
          'email', now(), now(), now());

  select * into v_res from v7_worker.provision_worker_credential(p_agent_id, v_uid, p_enrollment_secret);
  if not v_res.success then
    return query select false, v_res.message, null::uuid; return;
  end if;

  return query select true, 'enrolled ' || p_agent_id, v_uid;
end $$;

revoke all on function v7_worker.enroll_worker(text, text, text) from public, anon, authenticated;
grant execute on function v7_worker.enroll_worker(text, text, text) to service_role;

comment on function v7_worker.enroll_worker(text, text, text) is
  'Creates the auth principal for an agent and binds it. Sets GoTrue token
   columns to empty strings, which raw SQL inserts otherwise leave NULL and
   break the password grant. Stores only a bcrypt hash of the secret.';
