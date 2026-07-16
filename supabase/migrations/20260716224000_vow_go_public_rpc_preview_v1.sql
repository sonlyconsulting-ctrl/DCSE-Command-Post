-- Vow & Go governed browser mediation.
-- Keeps family_core and family_vow_go out of the exposed-schema list.
-- The browser calls only authenticated public RPC functions; RLS remains authoritative.

do $guard$
begin
  if not exists (select 1 from pg_namespace where nspname = 'family_core') then
    raise exception 'Required schema family_core is missing';
  end if;
  if not exists (select 1 from pg_namespace where nspname = 'family_vow_go') then
    raise exception 'Required schema family_vow_go is missing';
  end if;
  if to_regclass('family_core.product_instances') is null
     or to_regclass('family_core.product_memberships') is null then
    raise exception 'Required family_core product tables are missing';
  end if;
end
$guard$;

create table if not exists family_vow_go.wedding_profiles (
  product_instance_id uuid primary key references family_core.product_instances(id) on delete cascade,
  couple_names text not null,
  wedding_date timestamptz,
  hero_video_path text,
  ebook_url text,
  created_by uuid references auth.users(id),
  updated_by uuid references auth.users(id),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.wedding_tasks (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  title text not null,
  description text,
  due_date date,
  priority text not null default 'standard',
  status text not null default 'open' check (status in ('open','in_progress','blocked','done','completed')),
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.wedding_media (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  uploaded_by uuid not null references auth.users(id),
  storage_path text not null unique,
  media_kind text not null check (media_kind in ('photo','video')),
  moderation_status text not null default 'pending' check (moderation_status in ('pending','approved','rejected','private')),
  curated boolean not null default false,
  alt_text text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.guestbook_entries (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  submitted_by uuid not null references auth.users(id),
  display_name text not null,
  message text not null,
  moderation_status text not null default 'pending' check (moderation_status in ('pending','approved','rejected','private')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.wedding_notifications (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  title text not null,
  body text not null,
  audience text not null default 'admins' check (audience in ('admins','wedding_party','all_guests')),
  status text not null default 'draft' check (status in ('draft','scheduled','sent','cancelled')),
  scheduled_for timestamptz,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table family_vow_go.wedding_settings add column if not exists ebook_url text;

create index if not exists wedding_tasks_product_due_idx on family_vow_go.wedding_tasks(product_instance_id, due_date);
create index if not exists wedding_media_product_moderation_idx on family_vow_go.wedding_media(product_instance_id, moderation_status, created_at desc);
create index if not exists guestbook_product_moderation_idx on family_vow_go.guestbook_entries(product_instance_id, moderation_status, created_at desc);
create index if not exists wedding_notifications_product_created_idx on family_vow_go.wedding_notifications(product_instance_id, created_at desc);

alter table family_vow_go.wedding_profiles enable row level security;
alter table family_vow_go.wedding_tasks enable row level security;
alter table family_vow_go.wedding_media enable row level security;
alter table family_vow_go.guestbook_entries enable row level security;
alter table family_vow_go.wedding_notifications enable row level security;

revoke usage on schema family_core from anon;
revoke usage on schema family_vow_go from anon;
grant usage on schema family_core to authenticated;
grant usage on schema family_vow_go to authenticated;
grant usage on type family_core.product_role to authenticated;

grant select on family_core.product_instances, family_core.product_memberships to authenticated;
grant select, insert, update, delete on
  family_vow_go.wedding_profiles,
  family_vow_go.wedding_settings,
  family_vow_go.wedding_tasks,
  family_vow_go.wedding_events,
  family_vow_go.vendors,
  family_vow_go.budget_items,
  family_vow_go.guests,
  family_vow_go.wedding_media,
  family_vow_go.guestbook_entries,
  family_vow_go.music_items,
  family_vow_go.external_integrations,
  family_vow_go.content_chapters,
  family_vow_go.wedding_notifications,
  family_vow_go.admin_feedback
to authenticated;
revoke all on all tables in schema family_vow_go from anon;

create or replace function public.vow_go_uuid_from_text(p_value text)
returns uuid
language plpgsql
immutable
security invoker
set search_path = ''
as $$
begin
  return p_value::uuid;
exception
  when invalid_text_representation then
    return null;
end
$$;

create or replace function public.vow_go_current_role(p_product_instance_id uuid)
returns text
language sql
stable
security invoker
set search_path = ''
as $$
  select pm.role::text
  from family_core.product_memberships pm
  where pm.user_id = (select auth.uid())
    and pm.product_instance_id = p_product_instance_id
    and pm.status = 'active'
  limit 1
$$;

create or replace function public.vow_go_safe_url(p_url text, p_kind text default 'https')
returns boolean
language sql
immutable
security invoker
set search_path = ''
as $$
  select case
    when p_url is null or btrim(p_url) = '' then true
    when p_url !~* '^https://[^[:space:]]+$' then false
    when p_kind = 'drive' then p_url ~* '^https://(drive|docs)\.google\.com/'
    when p_kind = 'dropbox' then p_url ~* '^https://([a-z0-9-]+\.)?dropbox\.com/'
    when p_kind = 'spotify' then p_url ~* '^https://([a-z0-9-]+\.)?spotify\.com/'
    when p_kind = 'pandora' then p_url ~* '^https://([a-z0-9-]+\.)?pandora\.com/'
    when p_kind = 'apple_music' then p_url ~* '^https://music\.apple\.com/'
    when p_kind = 'youtube' then p_url ~* '^https://(([a-z0-9-]+\.)?youtube\.com/|youtu\.be/)'
    else true
  end
$$;

revoke execute on function public.vow_go_uuid_from_text(text) from public, anon;
revoke execute on function public.vow_go_current_role(uuid) from public, anon;
revoke execute on function public.vow_go_safe_url(text, text) from public, anon;
grant execute on function public.vow_go_uuid_from_text(text) to authenticated;
grant execute on function public.vow_go_current_role(uuid) to authenticated;
grant execute on function public.vow_go_safe_url(text, text) to authenticated;

do $drop_legacy$
declare
  t text;
begin
  foreach t in array array[
    'wedding_settings','wedding_events','vendors','budget_items','guests',
    'music_items','external_integrations','content_chapters'
  ] loop
    execute format('drop policy if exists %I_member_select on family_vow_go.%I', t, t);
    execute format('drop policy if exists %I_admin_insert on family_vow_go.%I', t, t);
    execute format('drop policy if exists %I_admin_update on family_vow_go.%I', t, t);
    execute format('drop policy if exists %I_admin_delete on family_vow_go.%I', t, t);
  end loop;
end
$drop_legacy$;

do $admin_tables$
declare
  t text;
begin
  foreach t in array array['wedding_tasks','vendors','budget_items','guests','external_integrations'] loop
    execute format('drop policy if exists %I_admin_select on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_admin_select on family_vow_go.%I for select to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))',
      t, t
    );
    execute format('drop policy if exists %I_admin_insert on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_admin_insert on family_vow_go.%I for insert to authenticated with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))',
      t, t
    );
    execute format('drop policy if exists %I_admin_update on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_admin_update on family_vow_go.%I for update to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[])) with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))',
      t, t
    );
    execute format('drop policy if exists %I_owner_delete on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_owner_delete on family_vow_go.%I for delete to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'']::family_core.product_role[]))',
      t, t
    );
  end loop;
end
$admin_tables$;

drop policy if exists wedding_profiles_member_select on family_vow_go.wedding_profiles;
create policy wedding_profiles_member_select
on family_vow_go.wedding_profiles for select to authenticated
using (family_core.is_product_member(product_instance_id));

drop policy if exists wedding_profiles_admin_insert on family_vow_go.wedding_profiles;
create policy wedding_profiles_admin_insert
on family_vow_go.wedding_profiles for insert to authenticated
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists wedding_profiles_admin_update on family_vow_go.wedding_profiles;
create policy wedding_profiles_admin_update
on family_vow_go.wedding_profiles for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists wedding_settings_member_select on family_vow_go.wedding_settings;
create policy wedding_settings_member_select
on family_vow_go.wedding_settings for select to authenticated
using (family_core.is_product_member(product_instance_id));

drop policy if exists wedding_settings_admin_insert on family_vow_go.wedding_settings;
create policy wedding_settings_admin_insert
on family_vow_go.wedding_settings for insert to authenticated
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists wedding_settings_admin_update on family_vow_go.wedding_settings;
create policy wedding_settings_admin_update
on family_vow_go.wedding_settings for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

do $visible_tables$
declare
  t text;
  visibility_column text;
begin
  foreach t in array array['wedding_events','content_chapters'] loop
    execute format('drop policy if exists %I_scoped_select on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_scoped_select on family_vow_go.%I for select to authenticated using (
        family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[])
        or (
          family_core.is_product_member(product_instance_id)
          and (
            visibility = ''all_guests''
            or (visibility = ''wedding_party'' and public.vow_go_current_role(product_instance_id) in (''wedding_party'',''guardian''))
          )
        )
      )',
      t, t
    );
    execute format('drop policy if exists %I_admin_insert on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_admin_insert on family_vow_go.%I for insert to authenticated with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))',
      t, t
    );
    execute format('drop policy if exists %I_admin_update on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_admin_update on family_vow_go.%I for update to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[])) with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))',
      t, t
    );
    execute format('drop policy if exists %I_owner_delete on family_vow_go.%I', t, t);
    execute format(
      'create policy %I_owner_delete on family_vow_go.%I for delete to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'']::family_core.product_role[]))',
      t, t
    );
  end loop;
end
$visible_tables$;

drop policy if exists music_items_member_select on family_vow_go.music_items;
create policy music_items_member_select
on family_vow_go.music_items for select to authenticated
using (family_core.is_product_member(product_instance_id));

drop policy if exists music_items_admin_insert on family_vow_go.music_items;
create policy music_items_admin_insert
on family_vow_go.music_items for insert to authenticated
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists music_items_admin_update on family_vow_go.music_items;
create policy music_items_admin_update
on family_vow_go.music_items for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists notifications_scoped_select on family_vow_go.wedding_notifications;
create policy notifications_scoped_select
on family_vow_go.wedding_notifications for select to authenticated
using (
  family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
  or (
    family_core.is_product_member(product_instance_id)
    and (
      audience = 'all_guests'
      or (audience = 'wedding_party' and public.vow_go_current_role(product_instance_id) in ('wedding_party','guardian'))
    )
  )
);

drop policy if exists notifications_admin_insert on family_vow_go.wedding_notifications;
create policy notifications_admin_insert
on family_vow_go.wedding_notifications for insert to authenticated
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists notifications_admin_update on family_vow_go.wedding_notifications;
create policy notifications_admin_update
on family_vow_go.wedding_notifications for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists wedding_media_scoped_select on family_vow_go.wedding_media;
create policy wedding_media_scoped_select
on family_vow_go.wedding_media for select to authenticated
using (
  family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
  or uploaded_by = (select auth.uid())
  or (
    moderation_status = 'approved'
    and family_core.is_product_member(product_instance_id)
    and coalesce((select ws.media_mode from family_vow_go.wedding_settings ws where ws.product_instance_id = wedding_media.product_instance_id), 'moderated') <> 'private'
  )
);

drop policy if exists wedding_media_member_insert on family_vow_go.wedding_media;
create policy wedding_media_member_insert
on family_vow_go.wedding_media for insert to authenticated
with check (family_core.is_product_member(product_instance_id) and uploaded_by = (select auth.uid()));

drop policy if exists wedding_media_admin_update on family_vow_go.wedding_media;
create policy wedding_media_admin_update
on family_vow_go.wedding_media for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

drop policy if exists wedding_media_owner_delete on family_vow_go.wedding_media;
create policy wedding_media_owner_delete
on family_vow_go.wedding_media for delete to authenticated
using (
  uploaded_by = (select auth.uid())
  or family_core.has_product_role(product_instance_id, array['owner','couple_admin']::family_core.product_role[])
);

drop policy if exists guestbook_scoped_select on family_vow_go.guestbook_entries;
create policy guestbook_scoped_select
on family_vow_go.guestbook_entries for select to authenticated
using (
  family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
  or submitted_by = (select auth.uid())
  or (
    moderation_status = 'approved'
    and family_core.is_product_member(product_instance_id)
    and coalesce((select ws.guestbook_mode from family_vow_go.wedding_settings ws where ws.product_instance_id = guestbook_entries.product_instance_id), 'moderated') <> 'private'
  )
);

drop policy if exists guestbook_member_insert on family_vow_go.guestbook_entries;
create policy guestbook_member_insert
on family_vow_go.guestbook_entries for insert to authenticated
with check (family_core.is_product_member(product_instance_id) and submitted_by = (select auth.uid()));

drop policy if exists guestbook_admin_update on family_vow_go.guestbook_entries;
create policy guestbook_admin_update
on family_vow_go.guestbook_entries for update to authenticated
using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]))
with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]));

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'family-wedding-private',
  'family-wedding-private',
  false,
  104857600,
  array['image/jpeg','image/png','image/webp','image/heic','video/mp4','video/quicktime']
)
on conflict (id) do update
set public = false,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists vow_go_private_upload on storage.objects;
create policy vow_go_private_upload
on storage.objects for insert to authenticated
with check (
  bucket_id = 'family-wedding-private'
  and public.vow_go_uuid_from_text((storage.foldername(name))[1]) is not null
  and family_core.is_product_member(public.vow_go_uuid_from_text((storage.foldername(name))[1]))
  and (
    (storage.foldername(name))[2] = 'guest-pending'
    or (
      (storage.foldername(name))[2] = 'hero'
      and family_core.has_product_role(
        public.vow_go_uuid_from_text((storage.foldername(name))[1]),
        array['owner','couple_admin','planner']::family_core.product_role[]
      )
    )
  )
);

drop policy if exists vow_go_private_read on storage.objects;
create policy vow_go_private_read
on storage.objects for select to authenticated
using (
  bucket_id = 'family-wedding-private'
  and (
    (
      (storage.foldername(name))[2] = 'hero'
      and family_core.is_product_member(public.vow_go_uuid_from_text((storage.foldername(name))[1]))
    )
    or exists (
      select 1
      from family_vow_go.wedding_media wm
      where wm.storage_path = storage.objects.name
        and wm.product_instance_id = public.vow_go_uuid_from_text((storage.foldername(storage.objects.name))[1])
        and (
          wm.uploaded_by = (select auth.uid())
          or family_core.has_product_role(wm.product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[])
          or (
            wm.moderation_status = 'approved'
            and family_core.is_product_member(wm.product_instance_id)
            and coalesce((select ws.media_mode from family_vow_go.wedding_settings ws where ws.product_instance_id = wm.product_instance_id), 'moderated') <> 'private'
          )
        )
    )
  )
);

drop policy if exists vow_go_private_delete on storage.objects;
create policy vow_go_private_delete
on storage.objects for delete to authenticated
using (
  bucket_id = 'family-wedding-private'
  and (
    owner_id = (select auth.uid()::text)
    or family_core.has_product_role(
      public.vow_go_uuid_from_text((storage.foldername(name))[1]),
      array['owner','couple_admin']::family_core.product_role[]
    )
  )
);

create or replace function public.vow_go_context()
returns jsonb
language plpgsql
stable
security invoker
set search_path = ''
as $$
declare
  v_membership jsonb;
  v_product_id uuid;
begin
  select jsonb_build_object(
           'product_instance_id', pi.id,
           'title', pi.title,
           'product_type', pi.product_type,
           'status', pi.status,
           'role', pm.role::text
         ),
         pi.id
  into v_membership, v_product_id
  from family_core.product_memberships pm
  join family_core.product_instances pi on pi.id = pm.product_instance_id
  where pm.user_id = (select auth.uid())
    and pm.status = 'active'
    and pi.product_type = 'vow_go'
  order by pi.id
  limit 1;

  if v_product_id is null then
    return jsonb_build_object('membership', null);
  end if;

  return jsonb_build_object(
    'membership', v_membership,
    'profile', (select to_jsonb(p) from family_vow_go.wedding_profiles p where p.product_instance_id = v_product_id limit 1),
    'settings', (select to_jsonb(s) from family_vow_go.wedding_settings s where s.product_instance_id = v_product_id limit 1),
    'tasks', coalesce((select jsonb_agg(to_jsonb(t) order by t.due_date nulls last, t.created_at) from family_vow_go.wedding_tasks t where t.product_instance_id = v_product_id), '[]'::jsonb),
    'guests', coalesce((select jsonb_agg(to_jsonb(g) order by g.display_name) from family_vow_go.guests g where g.product_instance_id = v_product_id), '[]'::jsonb),
    'vendors', coalesce((select jsonb_agg(to_jsonb(v) order by v.category, v.name) from family_vow_go.vendors v where v.product_instance_id = v_product_id), '[]'::jsonb),
    'budget', coalesce((select jsonb_agg(to_jsonb(b) order by b.created_at) from family_vow_go.budget_items b where b.product_instance_id = v_product_id), '[]'::jsonb),
    'events', coalesce((select jsonb_agg(to_jsonb(e) order by e.starts_at nulls last) from family_vow_go.wedding_events e where e.product_instance_id = v_product_id), '[]'::jsonb),
    'media', coalesce((select jsonb_agg(to_jsonb(m) order by m.created_at desc) from family_vow_go.wedding_media m where m.product_instance_id = v_product_id), '[]'::jsonb),
    'guestbook', coalesce((select jsonb_agg(to_jsonb(gb) order by gb.created_at desc) from family_vow_go.guestbook_entries gb where gb.product_instance_id = v_product_id), '[]'::jsonb),
    'chapters', coalesce((select jsonb_agg(to_jsonb(c) order by c.sort_order, c.created_at) from family_vow_go.content_chapters c where c.product_instance_id = v_product_id), '[]'::jsonb),
    'music', coalesce((select jsonb_agg(to_jsonb(mi) order by mi.sort_order, mi.created_at) from family_vow_go.music_items mi where mi.product_instance_id = v_product_id), '[]'::jsonb),
    'integrations', coalesce((select jsonb_agg(to_jsonb(i) order by i.provider, i.label) from family_vow_go.external_integrations i where i.product_instance_id = v_product_id and i.is_active), '[]'::jsonb),
    'notifications', coalesce((select jsonb_agg(to_jsonb(n) order by n.created_at desc) from family_vow_go.wedding_notifications n where n.product_instance_id = v_product_id), '[]'::jsonb)
  );
end
$$;

create or replace function public.vow_go_action(
  p_action text,
  p_payload jsonb default '{}'::jsonb
)
returns jsonb
language plpgsql
volatile
security invoker
set search_path = ''
as $$
declare
  v_product_id uuid;
  v_role text;
  v_is_admin boolean;
  v_action text := lower(btrim(coalesce(p_action, '')));
  v_record_id uuid;
  v_url text;
begin
  select pi.id, pm.role::text
  into v_product_id, v_role
  from family_core.product_memberships pm
  join family_core.product_instances pi on pi.id = pm.product_instance_id
  where pm.user_id = (select auth.uid())
    and pm.status = 'active'
    and pi.product_type = 'vow_go'
  order by pi.id
  limit 1;

  if v_product_id is null then
    raise exception using errcode = '42501', message = 'No active Vow & Go product membership';
  end if;

  v_is_admin := v_role in ('owner','couple_admin','planner');

  if v_action in (
    'task_add','task_status','guest_add','vendor_add','budget_add','event_add',
    'chapter_add','music_add','notification_add','integrations_save','settings_save',
    'hero_register','media_moderate','guestbook_moderate'
  ) and not v_is_admin then
    raise exception using errcode = '42501', message = 'Bride, groom, or planner role required';
  end if;

  case v_action
    when 'task_add' then
      insert into family_vow_go.wedding_tasks (
        product_instance_id, title, description, due_date, priority, status, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'title'), 180),
        left(nullif(btrim(p_payload->>'description'), ''), 2000),
        nullif(p_payload->>'due_date', '')::date,
        coalesce(nullif(left(btrim(p_payload->>'priority'), 40), ''), 'standard'),
        'open',
        (select auth.uid())
      );

    when 'task_status' then
      v_record_id := public.vow_go_uuid_from_text(p_payload->>'id');
      update family_vow_go.wedding_tasks
      set status = case when p_payload->>'status' in ('open','in_progress','blocked','done','completed') then p_payload->>'status' else status end,
          updated_at = now()
      where id = v_record_id and product_instance_id = v_product_id;

    when 'guest_add' then
      insert into family_vow_go.guests (
        product_instance_id, display_name, email, rsvp_status, wedding_party_role,
        dietary_needs, accessibility_needs, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'display_name'), 180),
        left(nullif(btrim(p_payload->>'email'), ''), 320),
        case when p_payload->>'rsvp_status' in ('pending','confirmed','declined','waitlisted') then p_payload->>'rsvp_status' else 'pending' end,
        left(nullif(btrim(p_payload->>'wedding_party_role'), ''), 120),
        left(nullif(btrim(p_payload->>'dietary_needs'), ''), 300),
        left(nullif(btrim(p_payload->>'accessibility_needs'), ''), 300),
        (select auth.uid())
      );

    when 'vendor_add' then
      insert into family_vow_go.vendors (
        product_instance_id, name, category, status, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'name'), 180),
        left(btrim(p_payload->>'category'), 80),
        case when p_payload->>'status' in ('researching','shortlisted','selected','contracted','paid','completed','cancelled') then p_payload->>'status' else 'researching' end,
        (select auth.uid())
      );

    when 'budget_add' then
      insert into family_vow_go.budget_items (
        product_instance_id, category, item_name, estimated_amount, committed_amount, paid_amount, status, created_by
      ) values (
        v_product_id,
        coalesce(nullif(left(btrim(p_payload->>'category'), 80), ''), 'other'),
        left(btrim(p_payload->>'item_name'), 180),
        greatest(0, coalesce(nullif(p_payload->>'estimated_amount', '')::numeric, 0)),
        greatest(0, coalesce(nullif(p_payload->>'committed_amount', '')::numeric, 0)),
        0,
        'planned',
        (select auth.uid())
      );

    when 'event_add' then
      insert into family_vow_go.wedding_events (
        product_instance_id, title, event_type, starts_at, visibility, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'title'), 180),
        coalesce(nullif(left(btrim(p_payload->>'event_type'), 80), ''), 'other'),
        nullif(p_payload->>'starts_at', '')::timestamptz,
        case when p_payload->>'visibility' in ('admins','wedding_party','all_guests') then p_payload->>'visibility' else 'all_guests' end,
        (select auth.uid())
      );

    when 'chapter_add' then
      insert into family_vow_go.content_chapters (
        product_instance_id, chapter_key, title, narrative, status, visibility, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'chapter_key'), 180),
        left(btrim(p_payload->>'title'), 180),
        left(nullif(btrim(p_payload->>'narrative'), ''), 5000),
        'draft',
        case when p_payload->>'visibility' in ('admins','wedding_party','all_guests') then p_payload->>'visibility' else 'all_guests' end,
        (select auth.uid())
      );

    when 'music_add' then
      v_url := nullif(btrim(p_payload->>'url'), '');
      if not public.vow_go_safe_url(v_url, coalesce(nullif(p_payload->>'provider', ''), 'https')) then
        raise exception using errcode = '22023', message = 'Unsafe or unsupported music URL';
      end if;
      insert into family_vow_go.music_items (
        product_instance_id, provider, title, url, moment_type, narrative_note, created_by
      ) values (
        v_product_id,
        case when p_payload->>'provider' in ('spotify','pandora','apple_music','youtube','uploaded','other') then p_payload->>'provider' else 'other' end,
        left(btrim(p_payload->>'title'), 180),
        v_url,
        left(coalesce(nullif(btrim(p_payload->>'moment_type'), ''), 'playlist'), 80),
        left(nullif(btrim(p_payload->>'narrative_note'), ''), 1000),
        (select auth.uid())
      );

    when 'notification_add' then
      insert into family_vow_go.wedding_notifications (
        product_instance_id, title, body, audience, created_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'title'), 180),
        left(btrim(p_payload->>'body'), 2000),
        case when p_payload->>'audience' in ('admins','wedding_party','all_guests') then p_payload->>'audience' else 'admins' end,
        (select auth.uid())
      );

    when 'guestbook_submit' then
      insert into family_vow_go.guestbook_entries (
        product_instance_id, submitted_by, display_name, message, moderation_status
      ) values (
        v_product_id,
        (select auth.uid()),
        left(btrim(p_payload->>'display_name'), 80),
        left(btrim(p_payload->>'message'), 2000),
        'pending'
      );

    when 'guestbook_moderate' then
      v_record_id := public.vow_go_uuid_from_text(p_payload->>'id');
      update family_vow_go.guestbook_entries
      set moderation_status = case when p_payload->>'status' in ('approved','rejected','private') then p_payload->>'status' else moderation_status end,
          updated_at = now()
      where id = v_record_id and product_instance_id = v_product_id;

    when 'media_register' then
      if p_payload->>'storage_path' not like v_product_id::text || '/guest-pending/%' then
        raise exception using errcode = '22023', message = 'Invalid media path';
      end if;
      insert into family_vow_go.wedding_media (
        product_instance_id, uploaded_by, storage_path, media_kind, moderation_status, curated
      ) values (
        v_product_id,
        (select auth.uid()),
        left(p_payload->>'storage_path', 1024),
        case when p_payload->>'media_kind' = 'video' then 'video' else 'photo' end,
        case when v_is_admin then 'approved' else 'pending' end,
        v_is_admin
      );

    when 'hero_register' then
      if p_payload->>'storage_path' not like v_product_id::text || '/hero/%' then
        raise exception using errcode = '22023', message = 'Invalid hero path';
      end if;
      insert into family_vow_go.wedding_profiles (
        product_instance_id, couple_names, hero_video_path, created_by, updated_by
      ) values (
        v_product_id,
        coalesce((select couple_names from family_vow_go.wedding_profiles where product_instance_id = v_product_id), 'Vow & Go Couple'),
        left(p_payload->>'storage_path', 1024),
        (select auth.uid()),
        (select auth.uid())
      )
      on conflict (product_instance_id) do update
      set hero_video_path = excluded.hero_video_path,
          updated_by = excluded.updated_by,
          updated_at = now();

    when 'media_moderate' then
      v_record_id := public.vow_go_uuid_from_text(p_payload->>'id');
      update family_vow_go.wedding_media
      set moderation_status = case when p_payload->>'status' in ('approved','rejected','private') then p_payload->>'status' else moderation_status end,
          curated = p_payload->>'status' = 'approved',
          updated_at = now()
      where id = v_record_id and product_instance_id = v_product_id;

    when 'integrations_save' then
      v_url := nullif(btrim(p_payload->>'drive_url'), '');
      if not public.vow_go_safe_url(v_url, 'drive') then
        raise exception using errcode = '22023', message = 'Invalid Google Drive URL';
      end if;
      if v_url is not null then
        insert into family_vow_go.external_integrations (
          product_instance_id, provider, label, url, purpose, visibility, is_active, created_by
        ) values (
          v_product_id, 'google_drive', 'Google Drive planning files', v_url,
          'admin planning documents', 'admins', true, (select auth.uid())
        )
        on conflict (product_instance_id, provider, label) do update
        set url = excluded.url, is_active = true;
      end if;

      v_url := nullif(btrim(p_payload->>'dropbox_url'), '');
      if not public.vow_go_safe_url(v_url, 'dropbox') then
        raise exception using errcode = '22023', message = 'Invalid Dropbox URL';
      end if;
      if v_url is not null then
        insert into family_vow_go.external_integrations (
          product_instance_id, provider, label, url, purpose, visibility, is_active, created_by
        ) values (
          v_product_id, 'dropbox', 'Dropbox planning files', v_url,
          'admin planning documents', 'admins', true, (select auth.uid())
        )
        on conflict (product_instance_id, provider, label) do update
        set url = excluded.url, is_active = true;
      end if;

    when 'settings_save' then
      if not public.vow_go_safe_url(nullif(btrim(p_payload->>'countdown_background_url'), ''), 'https')
         or not public.vow_go_safe_url(nullif(btrim(p_payload->>'ebook_url'), ''), 'https') then
        raise exception using errcode = '22023', message = 'Settings URLs must use HTTPS';
      end if;

      insert into family_vow_go.wedding_settings (
        product_instance_id, wedding_date, countdown_background_url, ebook_url,
        honeymoon_status, guestbook_mode, media_mode, updated_by, updated_at
      ) values (
        v_product_id,
        nullif(p_payload->>'wedding_date', '')::timestamptz,
        nullif(btrim(p_payload->>'countdown_background_url'), ''),
        nullif(btrim(p_payload->>'ebook_url'), ''),
        case when p_payload->>'honeymoon_status' in ('future','announced','open','archived') then p_payload->>'honeymoon_status' else 'future' end,
        case when p_payload->>'guestbook_mode' in ('public','moderated','private') then p_payload->>'guestbook_mode' else 'moderated' end,
        case when p_payload->>'media_mode' in ('public','moderated','private') then p_payload->>'media_mode' else 'moderated' end,
        (select auth.uid()),
        now()
      )
      on conflict (product_instance_id) do update
      set wedding_date = excluded.wedding_date,
          countdown_background_url = excluded.countdown_background_url,
          ebook_url = excluded.ebook_url,
          honeymoon_status = excluded.honeymoon_status,
          guestbook_mode = excluded.guestbook_mode,
          media_mode = excluded.media_mode,
          updated_by = excluded.updated_by,
          updated_at = now();

      insert into family_vow_go.wedding_profiles (
        product_instance_id, couple_names, wedding_date, ebook_url, created_by, updated_by
      ) values (
        v_product_id,
        left(btrim(p_payload->>'couple_names'), 180),
        nullif(p_payload->>'wedding_date', '')::timestamptz,
        nullif(btrim(p_payload->>'ebook_url'), ''),
        (select auth.uid()),
        (select auth.uid())
      )
      on conflict (product_instance_id) do update
      set couple_names = excluded.couple_names,
          wedding_date = excluded.wedding_date,
          ebook_url = excluded.ebook_url,
          updated_by = excluded.updated_by,
          updated_at = now();

    when 'feedback_submit' then
      insert into family_vow_go.admin_feedback (
        product_instance_id, submitted_by, feedback_type, severity, subject, details, page_context
      ) values (
        v_product_id,
        (select auth.uid()),
        case when p_payload->>'feedback_type' in ('bug','enhancement','question','content','privacy','other') then p_payload->>'feedback_type' else 'other' end,
        case when p_payload->>'severity' in ('low','normal','high','critical') then p_payload->>'severity' else 'normal' end,
        left(btrim(p_payload->>'subject'), 180),
        left(btrim(p_payload->>'details'), 5000),
        left(nullif(btrim(p_payload->>'page_context'), ''), 2048)
      );

    else
      raise exception using errcode = '22023', message = 'Unsupported Vow & Go action';
  end case;

  return jsonb_build_object('ok', true, 'action', v_action);
end
$$;

revoke execute on function public.vow_go_context() from public, anon;
revoke execute on function public.vow_go_action(text, jsonb) from public, anon;
grant execute on function public.vow_go_context() to authenticated;
grant execute on function public.vow_go_action(text, jsonb) to authenticated;

comment on function public.vow_go_context() is
'Authenticated, product-derived Vow & Go review context. SECURITY INVOKER; all rows remain controlled by RLS.';

comment on function public.vow_go_action(text, jsonb) is
'Allowlisted Vow & Go mutation RPC. Product identity is derived from auth membership; callers cannot select another product.';
