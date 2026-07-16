create table if not exists family_vow_go.wedding_settings (
  product_instance_id uuid primary key references family_core.product_instances(id) on delete cascade,
  wedding_date timestamptz,
  venue_name text,
  venue_location text,
  tagline text,
  hashtag text,
  countdown_background_url text,
  visual_transition_style text not null default 'cabo_to_hawaii',
  guestbook_mode text not null default 'moderated' check (guestbook_mode in ('public','moderated','private')),
  media_mode text not null default 'moderated' check (media_mode in ('public','moderated','private')),
  honeymoon_status text not null default 'future' check (honeymoon_status in ('future','announced','open','archived')),
  honeymoon_unlock_at timestamptz,
  updated_by uuid references auth.users(id),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.wedding_events (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  title text not null,
  event_type text not null default 'other',
  starts_at timestamptz,
  ends_at timestamptz,
  location_name text,
  location_address text,
  visibility text not null default 'all_guests' check (visibility in ('admins','wedding_party','all_guests')),
  notes text,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.vendors (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  category text not null,
  name text not null,
  contact_name text,
  email text,
  phone text,
  website text,
  status text not null default 'researching' check (status in ('researching','shortlisted','selected','contracted','paid','completed','cancelled')),
  quoted_amount numeric(12,2),
  contracted_amount numeric(12,2),
  deposit_amount numeric(12,2),
  balance_due numeric(12,2),
  balance_due_at date,
  special_requirements text,
  notes text,
  external_folder_url text,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.budget_items (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  category text not null,
  item_name text not null,
  estimated_amount numeric(12,2) not null default 0,
  committed_amount numeric(12,2) not null default 0,
  paid_amount numeric(12,2) not null default 0,
  due_at date,
  status text not null default 'planned' check (status in ('planned','quoted','committed','partially_paid','paid','cancelled')),
  vendor_id uuid references family_vow_go.vendors(id) on delete set null,
  notes text,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.guests (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  display_name text not null,
  email text,
  phone text,
  party_size smallint not null default 1 check (party_size between 1 and 20),
  rsvp_status text not null default 'pending' check (rsvp_status in ('pending','confirmed','declined','waitlisted')),
  dietary_needs text,
  accessibility_needs text,
  special_needs text,
  travel_status text,
  lodging_status text,
  wedding_party_role text,
  notes_private text,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists family_vow_go.music_items (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  provider text not null check (provider in ('spotify','pandora','apple_music','youtube','uploaded','other')),
  title text not null,
  artist text,
  url text,
  moment_type text not null default 'playlist',
  narrative_note text,
  sort_order integer not null default 0,
  is_featured boolean not null default false,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now()
);

create table if not exists family_vow_go.external_integrations (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  provider text not null check (provider in ('google_drive','dropbox','spotify','pandora','apple_music','google_maps','other')),
  label text not null,
  url text not null,
  purpose text,
  visibility text not null default 'admins' check (visibility in ('admins','wedding_party','all_guests')),
  is_active boolean not null default true,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  unique(product_instance_id, provider, label)
);

create table if not exists family_vow_go.content_chapters (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  chapter_key text not null,
  title text not null,
  narrative text,
  status text not null default 'draft' check (status in ('draft','published','locked','archived')),
  visibility text not null default 'all_guests' check (visibility in ('admins','wedding_party','all_guests')),
  unlock_at timestamptz,
  background_url text,
  sort_order integer not null default 0,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(product_instance_id, chapter_key)
);

create table if not exists family_vow_go.admin_feedback (
  id uuid primary key default gen_random_uuid(),
  product_instance_id uuid not null references family_core.product_instances(id) on delete cascade,
  submitted_by uuid not null references auth.users(id),
  feedback_type text not null check (feedback_type in ('bug','enhancement','question','content','privacy','other')),
  severity text not null default 'normal' check (severity in ('low','normal','high','critical')),
  subject text not null,
  details text not null,
  page_context text,
  status text not null default 'new' check (status in ('new','acknowledged','in_progress','resolved','closed')),
  created_at timestamptz not null default now()
);

create index if not exists wedding_events_product_starts_idx on family_vow_go.wedding_events(product_instance_id, starts_at);
create index if not exists vendors_product_category_idx on family_vow_go.vendors(product_instance_id, category);
create index if not exists budget_items_product_category_idx on family_vow_go.budget_items(product_instance_id, category);
create index if not exists guests_product_rsvp_idx on family_vow_go.guests(product_instance_id, rsvp_status);
create index if not exists music_items_product_sort_idx on family_vow_go.music_items(product_instance_id, sort_order);
create index if not exists external_integrations_product_idx on family_vow_go.external_integrations(product_instance_id);
create index if not exists content_chapters_product_sort_idx on family_vow_go.content_chapters(product_instance_id, sort_order);
create index if not exists admin_feedback_product_status_idx on family_vow_go.admin_feedback(product_instance_id, status);

alter table family_vow_go.wedding_settings enable row level security;
alter table family_vow_go.wedding_events enable row level security;
alter table family_vow_go.vendors enable row level security;
alter table family_vow_go.budget_items enable row level security;
alter table family_vow_go.guests enable row level security;
alter table family_vow_go.music_items enable row level security;
alter table family_vow_go.external_integrations enable row level security;
alter table family_vow_go.content_chapters enable row level security;
alter table family_vow_go.admin_feedback enable row level security;

do $policy$
declare t text;
begin
  foreach t in array array['wedding_settings','wedding_events','vendors','budget_items','guests','music_items','external_integrations','content_chapters'] loop
    execute format('drop policy if exists %I_member_select on family_vow_go.%I', t, t);
    execute format('create policy %I_member_select on family_vow_go.%I for select to authenticated using (family_core.is_product_member(product_instance_id))', t, t);
    execute format('drop policy if exists %I_admin_insert on family_vow_go.%I', t, t);
    execute format('create policy %I_admin_insert on family_vow_go.%I for insert to authenticated with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))', t, t);
    execute format('drop policy if exists %I_admin_update on family_vow_go.%I', t, t);
    execute format('create policy %I_admin_update on family_vow_go.%I for update to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[])) with check (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'',''planner'']::family_core.product_role[]))', t, t);
    execute format('drop policy if exists %I_admin_delete on family_vow_go.%I', t, t);
    execute format('create policy %I_admin_delete on family_vow_go.%I for delete to authenticated using (family_core.has_product_role(product_instance_id, array[''owner'',''couple_admin'']::family_core.product_role[]))', t, t);
  end loop;
end
$policy$;

drop policy if exists admin_feedback_submit on family_vow_go.admin_feedback;
create policy admin_feedback_submit on family_vow_go.admin_feedback for insert to authenticated with check (family_core.is_product_member(product_instance_id) and submitted_by = (select auth.uid()));

drop policy if exists admin_feedback_read_admin on family_vow_go.admin_feedback;
create policy admin_feedback_read_admin on family_vow_go.admin_feedback for select to authenticated using (family_core.has_product_role(product_instance_id, array['owner','couple_admin','planner']::family_core.product_role[]) or submitted_by = (select auth.uid()));

drop policy if exists admin_feedback_update_admin on family_vow_go.admin_feedback;
create policy admin_feedback_update_admin on family_vow_go.admin_feedback for update to authenticated using (family_core.has_product_role(product_instance_id, array['owner','couple_admin']::family_core.product_role[])) with check (family_core.has_product_role(product_instance_id, array['owner','couple_admin']::family_core.product_role[]));
