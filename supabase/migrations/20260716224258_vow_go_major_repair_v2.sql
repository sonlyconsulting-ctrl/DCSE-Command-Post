-- Vow & Go major repair: modular modes, engagement-scoped operational CRUD,
-- invitations, reusable templates, audit history, and governed browser RPCs.
-- Additive only. No production data is deleted and RLS remains authoritative.

alter table family_vow_go.wedding_settings
  add column if not exists product_mode text not null default 'experience_only',
  add column if not exists planner_theme text not null default 'refined_dark',
  add column if not exists couple_theme text not null default 'romantic_light',
  add column if not exists guest_theme text not null default 'coastal_celebration',
  add column if not exists module_toggles jsonb not null default '{}'::jsonb;

do $constraints$
begin
  if not exists (select 1 from pg_constraint where conname = 'wedding_settings_product_mode_check') then
    alter table family_vow_go.wedding_settings add constraint wedding_settings_product_mode_check
      check (product_mode in ('experience_only','coordination','full_command_center'));
  end if;
  if not exists (select 1 from pg_constraint where conname = 'wedding_settings_planner_theme_check') then
    alter table family_vow_go.wedding_settings add constraint wedding_settings_planner_theme_check
      check (planner_theme in ('refined_dark','romantic_light','coastal_celebration'));
  end if;
  if not exists (select 1 from pg_constraint where conname = 'wedding_settings_couple_theme_check') then
    alter table family_vow_go.wedding_settings add constraint wedding_settings_couple_theme_check
      check (couple_theme in ('refined_dark','romantic_light','coastal_celebration'));
  end if;
  if not exists (select 1 from pg_constraint where conname = 'wedding_settings_guest_theme_check') then
    alter table family_vow_go.wedding_settings add constraint wedding_settings_guest_theme_check
      check (guest_theme in ('refined_dark','romantic_light','coastal_celebration'));
  end if;
end
$constraints$;

create table if not exists family_core.platform_administrators (
  user_id uuid primary key references auth.users(id) on delete cascade,
  platform_role text not null check (platform_role in ('platform_owner','support_admin')),
  status text not null default 'active' check (status in ('active','suspended','revoked')),
  created_at timestamptz not null default now()
);

create or replace function family_core.is_platform_owner()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from family_core.platform_administrators pa
    where pa.user_id = (select auth.uid())
      and pa.platform_role = 'platform_owner'
      and pa.status = 'active'
  )
$$;

revoke execute on function family_core.is_platform_owner() from public, anon;
grant execute on function family_core.is_platform_owner() to authenticated;

create table if not exists family_vow_go.workspace_records (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  collection text not null check (collection in (
    'tasks','checklists','vendors','contracts','budget','payments','guests','party','events',
    'travel','hotels','measurements','fittings','notifications','communications','announcements',
    'music','media','story','external_links','faqs','feedback','guide','polls','itineraries'
  )),
  title text not null,
  record_data jsonb not null default '{}'::jsonb,
  status text not null default 'active',
  visibility text not null default 'admins' check (visibility in ('admins','wedding_party','participants','all_guests','public','private','moderated')),
  archived_at timestamptz,
  archived_by uuid references auth.users(id),
  created_by uuid not null references auth.users(id),
  updated_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (jsonb_typeof(record_data) = 'object')
);

create table if not exists family_vow_go.record_activity (
  id bigint generated always as identity primary key,
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  record_id uuid not null references family_vow_go.workspace_records(id) on delete cascade,
  action text not null check (action in ('created','updated','archived','restored','deleted','status_changed','imported','exported')),
  actor_id uuid references auth.users(id),
  details jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);

create table if not exists family_vow_go.engagement_invitations (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  token_hash text not null unique,
  invitation_role text not null check (invitation_role in ('guest_viewer','guest_participant','trusted_contributor','couple_collaborator')),
  guest_id uuid references family_vow_go.guests(id) on delete set null,
  invited_email text,
  expires_at timestamptz not null,
  accepted_at timestamptz,
  revoked_at timestamptz,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  check (length(token_hash) >= 64)
);

create table if not exists family_vow_go.reusable_templates (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references auth.users(id) on delete cascade,
  template_type text not null check (template_type in ('task','checklist','vendor_category','timeline','notification','faq','onboarding','workflow')),
  name text not null,
  template_data jsonb not null default '{}'::jsonb,
  is_archived boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (jsonb_typeof(template_data) = 'object'),
  check (not (template_data ?| array['guest_data','private_notes','measurements','media','contracts','financial_records','dietary_information','accessibility_information','private_messages','credentials']))
);

create table if not exists family_vow_go.feedback_delivery (
  feedback_id uuid primary key references family_vow_go.admin_feedback(id) on delete cascade,
  confirmation_id text not null unique,
  delivery_status text not null default 'pending' check (delivery_status in ('pending','sent','failed','not_configured')),
  provider_message_id text,
  attempted_at timestamptz,
  delivered_at timestamptz
);

create index if not exists workspace_records_product_collection_active_idx
  on family_vow_go.workspace_records(product_instance_id, collection, updated_at desc)
  where archived_at is null;
create index if not exists workspace_records_product_visibility_idx
  on family_vow_go.workspace_records(product_instance_id, visibility, collection);
create index if not exists workspace_records_data_gin_idx
  on family_vow_go.workspace_records using gin(record_data jsonb_path_ops);
create index if not exists record_activity_product_record_idx
  on family_vow_go.record_activity(product_instance_id, record_id, occurred_at desc);
create index if not exists invitations_product_expiry_idx
  on family_vow_go.engagement_invitations(product_instance_id, expires_at)
  where revoked_at is null;
create index if not exists templates_owner_type_idx
  on family_vow_go.reusable_templates(owner_user_id, template_type)
  where not is_archived;

alter table family_core.platform_administrators enable row level security;
alter table family_vow_go.workspace_records enable row level security;
alter table family_vow_go.record_activity enable row level security;
alter table family_vow_go.engagement_invitations enable row level security;
alter table family_vow_go.reusable_templates enable row level security;
alter table family_vow_go.feedback_delivery enable row level security;

drop policy if exists platform_administrators_self_select on family_core.platform_administrators;
create policy platform_administrators_self_select on family_core.platform_administrators
for select to authenticated using (user_id = (select auth.uid()));

drop policy if exists workspace_records_member_select on family_vow_go.workspace_records;
create policy workspace_records_member_select on family_vow_go.workspace_records
for select to authenticated using (family_core.is_product_member(product_instance_id));

drop policy if exists workspace_records_scoped_insert on family_vow_go.workspace_records;
create policy workspace_records_scoped_insert on family_vow_go.workspace_records
for insert to authenticated with check (
  created_by = (select auth.uid()) and updated_by = (select auth.uid()) and (
    family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
    or (public.vow_go_current_role(product_instance_id) = 'contributor' and collection in ('tasks','party','measurements','fittings','media','story','communications','feedback'))
  )
);

drop policy if exists workspace_records_scoped_update on family_vow_go.workspace_records;
create policy workspace_records_scoped_update on family_vow_go.workspace_records
for update to authenticated using (
  family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
  or (public.vow_go_current_role(product_instance_id) = 'contributor' and collection in ('tasks','party','measurements','fittings','media','story','communications','feedback'))
) with check (
  updated_by = (select auth.uid()) and (
    family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
    or (public.vow_go_current_role(product_instance_id) = 'contributor' and collection in ('tasks','party','measurements','fittings','media','story','communications','feedback'))
  )
);

drop policy if exists workspace_records_owner_delete on family_vow_go.workspace_records;
create policy workspace_records_owner_delete on family_vow_go.workspace_records
for delete to authenticated using (family_core.has_product_role(product_instance_id, array['owner']::family_core.product_role[]));

drop policy if exists record_activity_member_select on family_vow_go.record_activity;
create policy record_activity_member_select on family_vow_go.record_activity
for select to authenticated using (family_core.is_product_member(product_instance_id));
drop policy if exists record_activity_member_insert on family_vow_go.record_activity;
create policy record_activity_member_insert on family_vow_go.record_activity
for insert to authenticated with check (actor_id = (select auth.uid()) and family_core.is_product_member(product_instance_id));

drop policy if exists invitations_admin_all on family_vow_go.engagement_invitations;
create policy invitations_admin_all on family_vow_go.engagement_invitations
for all to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists templates_owner_all on family_vow_go.reusable_templates;
create policy templates_owner_all on family_vow_go.reusable_templates
for all to authenticated using (owner_user_id = (select auth.uid())) with check (owner_user_id = (select auth.uid()));

drop policy if exists feedback_delivery_submitter_select on family_vow_go.feedback_delivery;
create policy feedback_delivery_submitter_select on family_vow_go.feedback_delivery
for select to authenticated using (
  exists (select 1 from family_vow_go.admin_feedback af where af.id = feedback_id and (af.submitted_by = (select auth.uid()) or family_core.has_product_role(af.product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])))
);
drop policy if exists feedback_delivery_submitter_insert on family_vow_go.feedback_delivery;
create policy feedback_delivery_submitter_insert on family_vow_go.feedback_delivery
for insert to authenticated with check (
  exists (select 1 from family_vow_go.admin_feedback af where af.id = feedback_id and af.submitted_by = (select auth.uid()))
);
drop policy if exists feedback_delivery_submitter_update on family_vow_go.feedback_delivery;
create policy feedback_delivery_submitter_update on family_vow_go.feedback_delivery
for update to authenticated using (
  exists (select 1 from family_vow_go.admin_feedback af where af.id = feedback_id and af.submitted_by = (select auth.uid()))
) with check (
  exists (select 1 from family_vow_go.admin_feedback af where af.id = feedback_id and af.submitted_by = (select auth.uid()))
);

grant select on family_core.platform_administrators to authenticated;
grant select, insert, update, delete on family_vow_go.workspace_records to authenticated;
grant select, insert on family_vow_go.record_activity to authenticated;
grant select, insert, update, delete on family_vow_go.engagement_invitations to authenticated;
grant select, insert, update, delete on family_vow_go.reusable_templates to authenticated;
grant select, insert, update on family_vow_go.feedback_delivery to authenticated;
grant usage, select on sequence family_vow_go.record_activity_id_seq to authenticated;
revoke all on family_core.platform_administrators, family_vow_go.workspace_records,
  family_vow_go.record_activity, family_vow_go.engagement_invitations,
  family_vow_go.reusable_templates, family_vow_go.feedback_delivery from anon;

create or replace function public.vow_go_record_action(p_action text, p_payload jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
volatile
security invoker
set search_path = ''
as $$
declare
  v_product_id uuid := public.vow_go_uuid_from_text(p_payload->>'product_instance_id');
  v_collection text := lower(btrim(p_payload->>'collection'));
  v_id uuid := public.vow_go_uuid_from_text(p_payload->>'id');
  v_values jsonb := coalesce(p_payload->'values', '{}'::jsonb);
  v_title text;
  v_visibility text;
  v_record family_vow_go.workspace_records;
begin
  if v_product_id is null then
    select pm.product_instance_id into v_product_id
    from family_core.product_memberships pm join family_core.product_instances pi on pi.id = pm.product_instance_id
    where pm.user_id = (select auth.uid()) and pm.status = 'active' and pi.product_type = 'vow_go'
    order by pm.created_at limit 1;
  end if;
  if v_product_id is null or not family_core.is_product_member(v_product_id) then
    raise exception using errcode = '42501', message = 'Active Vow & Go engagement membership required';
  end if;
  if v_collection not in ('tasks','checklists','vendors','contracts','budget','payments','guests','party','events','travel','hotels','measurements','fittings','notifications','communications','announcements','music','media','story','external_links','faqs','feedback','guide','polls','itineraries') then
    raise exception using errcode = '22023', message = 'Unsupported collection';
  end if;
  if jsonb_typeof(v_values) <> 'object' or pg_column_size(v_values) > 65536 then
    raise exception using errcode = '22023', message = 'Invalid or oversized record';
  end if;
  v_title := left(btrim(coalesce(v_values->>'title', v_values->>'name', v_values->>'item', v_values->>'question', v_values->>'participant', 'Record')), 300);
  v_visibility := case when v_values->>'visibility' in ('admins','wedding_party','participants','all_guests','public','private','moderated') then v_values->>'visibility' else 'admins' end;

  case lower(btrim(p_action))
    when 'upsert' then
      if v_id is null then
        insert into family_vow_go.workspace_records(product_instance_id,collection,title,record_data,status,visibility,created_by,updated_by)
        values(v_product_id,v_collection,v_title,v_values,coalesce(nullif(v_values->>'status',''),'active'),v_visibility,(select auth.uid()),(select auth.uid())) returning * into v_record;
        insert into family_vow_go.record_activity(product_instance_id,record_id,action,actor_id) values(v_product_id,v_record.id,'created',(select auth.uid()));
      else
        update family_vow_go.workspace_records set title=v_title,record_data=v_values,status=coalesce(nullif(v_values->>'status',''),status),visibility=v_visibility,updated_by=(select auth.uid()),updated_at=now()
        where id=v_id and product_instance_id=v_product_id returning * into v_record;
        if v_record.id is null then raise exception using errcode='P0002',message='Record not found or denied'; end if;
        insert into family_vow_go.record_activity(product_instance_id,record_id,action,actor_id) values(v_product_id,v_record.id,'updated',(select auth.uid()));
      end if;
    when 'archive' then
      update family_vow_go.workspace_records set archived_at=now(),archived_by=(select auth.uid()),updated_by=(select auth.uid()),updated_at=now() where id=v_id and product_instance_id=v_product_id returning * into v_record;
      insert into family_vow_go.record_activity(product_instance_id,record_id,action,actor_id) values(v_product_id,v_record.id,'archived',(select auth.uid()));
    when 'restore' then
      update family_vow_go.workspace_records set archived_at=null,archived_by=null,updated_by=(select auth.uid()),updated_at=now() where id=v_id and product_instance_id=v_product_id returning * into v_record;
      insert into family_vow_go.record_activity(product_instance_id,record_id,action,actor_id) values(v_product_id,v_record.id,'restored',(select auth.uid()));
    when 'delete' then
      delete from family_vow_go.workspace_records where id=v_id and product_instance_id=v_product_id and archived_at is not null returning * into v_record;
    else raise exception using errcode='22023',message='Unsupported record action';
  end case;
  return jsonb_build_object('ok',true,'id',v_record.id,'product_instance_id',v_product_id);
end
$$;

create or replace function public.vow_go_engagement_context(p_product_instance_id uuid)
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $$
  select jsonb_build_object(
    'membership', jsonb_build_object('product_instance_id',pi.id,'title',pi.title,'role',pm.role::text,'status',pm.status),
    'settings', (select to_jsonb(ws) from family_vow_go.wedding_settings ws where ws.product_instance_id=pi.id),
    'records', coalesce((select jsonb_agg(to_jsonb(wr) order by wr.updated_at desc) from family_vow_go.workspace_records wr where wr.product_instance_id=pi.id),'[]'::jsonb)
  )
  from family_core.product_instances pi join family_core.product_memberships pm on pm.product_instance_id=pi.id
  where pi.id=p_product_instance_id and pi.product_type='vow_go' and pm.user_id=(select auth.uid()) and pm.status='active'
$$;

revoke execute on function public.vow_go_record_action(text,jsonb) from public, anon;
revoke execute on function public.vow_go_engagement_context(uuid) from public, anon;
grant execute on function public.vow_go_record_action(text,jsonb) to authenticated;
grant execute on function public.vow_go_engagement_context(uuid) to authenticated;

create or replace function public.vow_go_feedback_submit(p_payload jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
volatile
security invoker
set search_path = ''
as $$
declare
  v_product_id uuid := public.vow_go_uuid_from_text(p_payload->>'product_instance_id');
  v_feedback_id uuid;
  v_confirmation text;
begin
  if v_product_id is null then
    select pm.product_instance_id into v_product_id
    from family_core.product_memberships pm join family_core.product_instances pi on pi.id=pm.product_instance_id
    where pm.user_id=(select auth.uid()) and pm.status='active' and pi.product_type='vow_go'
    order by pm.created_at limit 1;
  end if;
  if v_product_id is null or not family_core.is_product_member(v_product_id) then
    raise exception using errcode='42501',message='Active Vow & Go engagement membership required';
  end if;
  if length(btrim(coalesce(p_payload->>'subject',''))) < 3 or length(btrim(coalesce(p_payload->>'details',''))) < 3 then
    raise exception using errcode='22023',message='Feedback subject and details are required';
  end if;
  insert into family_vow_go.admin_feedback(product_instance_id,submitted_by,feedback_type,severity,subject,details,page_context)
  values(v_product_id,(select auth.uid()),case when p_payload->>'type' in ('bug','enhancement','question','content','privacy','other') then p_payload->>'type' else 'other' end,case when p_payload->>'severity' in ('low','normal','high','critical') then p_payload->>'severity' else 'normal' end,left(btrim(p_payload->>'subject'),180),left(btrim(p_payload->>'details'),5000),left(btrim(p_payload->>'page_context'),2048))
  returning id into v_feedback_id;
  v_confirmation := 'VG-' || upper(substr(replace(v_feedback_id::text,'-',''),1,10));
  insert into family_vow_go.feedback_delivery(feedback_id,confirmation_id) values(v_feedback_id,v_confirmation);
  return jsonb_build_object('feedback_id',v_feedback_id,'confirmation_id',v_confirmation);
end
$$;

create or replace function public.vow_go_feedback_delivery_update(p_feedback_id uuid,p_status text,p_provider_message_id text default null)
returns void
language sql
volatile
security invoker
set search_path = ''
as $$
  update family_vow_go.feedback_delivery
  set delivery_status = case when p_status in ('sent','failed','not_configured') then p_status else 'failed' end,
      provider_message_id = left(p_provider_message_id,500), attempted_at=now(), delivered_at=case when p_status='sent' then now() else null end
  where feedback_id=p_feedback_id
$$;

revoke execute on function public.vow_go_feedback_submit(jsonb) from public, anon;
revoke execute on function public.vow_go_feedback_delivery_update(uuid,text,text) from public, anon;
grant execute on function public.vow_go_feedback_submit(jsonb) to authenticated;
grant execute on function public.vow_go_feedback_delivery_update(uuid,text,text) to authenticated;

comment on table family_vow_go.workspace_records is 'Engagement-scoped operational records for modular Vow & Go features. Specialized legacy tables remain supported.';
comment on table family_vow_go.engagement_invitations is 'Invitation tokens are stored only as hashes and expire or revoke independently.';
comment on table family_vow_go.reusable_templates is 'Planner-reusable structures; check constraint rejects known personal-data keys.';
