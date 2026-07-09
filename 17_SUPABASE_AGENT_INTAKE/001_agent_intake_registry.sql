-- DCSE Agent Intake Registry Supabase Migration v1
-- Date: 2026-07-08
-- Lane: SC / TI infrastructure
-- Purpose: Agent-accessible intake registry with public-read controls and PS exclusion.

create extension if not exists pgcrypto;

create table if not exists public.agent_intake_items (
  id uuid primary key default gen_random_uuid(),
  lane text not null check (lane in ('SC','TI','SS','DCS','PS','SC/TI')),
  title text not null,
  source_type text not null,
  source_url text,
  source_id text,
  github_path text,
  github_commit text,
  summary text,
  status text not null default 'queued',
  review_required boolean not null default true,
  promotion_gate text not null default 'review_required_before_public_use',
  public_read boolean not null default false,
  created_by text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.agent_reviews (
  id uuid primary key default gen_random_uuid(),
  intake_id uuid not null references public.agent_intake_items(id) on delete cascade,
  agent_name text not null,
  review_status text not null default 'draft',
  title_verification text,
  source_metadata jsonb,
  transcript_need text,
  website_strategy_relevance text,
  accessibility_ux_lessons text,
  risks text,
  recommendation text,
  full_review text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.agent_task_queue (
  id uuid primary key default gen_random_uuid(),
  task_name text not null,
  target_intake_id uuid references public.agent_intake_items(id) on delete cascade,
  assigned_agent text,
  instructions text not null,
  status text not null default 'queued',
  due_status text,
  public_read boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create or replace function public.set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_agent_intake_items_updated_at on public.agent_intake_items;
create trigger trg_agent_intake_items_updated_at
before update on public.agent_intake_items
for each row execute function public.set_updated_at();

drop trigger if exists trg_agent_reviews_updated_at on public.agent_reviews;
create trigger trg_agent_reviews_updated_at
before update on public.agent_reviews
for each row execute function public.set_updated_at();

drop trigger if exists trg_agent_task_queue_updated_at on public.agent_task_queue;
create trigger trg_agent_task_queue_updated_at
before update on public.agent_task_queue
for each row execute function public.set_updated_at();

create or replace view public.public_agent_intake_view as
select
  id,
  lane,
  title,
  source_type,
  source_url,
  source_id,
  github_path,
  github_commit,
  summary,
  status,
  review_required,
  promotion_gate,
  created_at,
  updated_at
from public.agent_intake_items
where public_read = true
  and lane <> 'PS';

create or replace view public.public_agent_task_view as
select
  q.id,
  q.task_name,
  q.target_intake_id,
  q.assigned_agent,
  q.instructions,
  q.status,
  q.due_status,
  q.created_at,
  q.updated_at,
  i.title as intake_title,
  i.source_type,
  i.source_url,
  i.source_id,
  i.github_path,
  i.github_commit,
  i.summary
from public.agent_task_queue q
join public.agent_intake_items i on i.id = q.target_intake_id
where q.public_read = true
  and i.public_read = true
  and i.lane <> 'PS';

alter table public.agent_intake_items enable row level security;
alter table public.agent_reviews enable row level security;
alter table public.agent_task_queue enable row level security;

-- Public read policies for safe non-PS records.
-- Supabase views above should be preferred for external agents.

drop policy if exists agent_intake_public_select on public.agent_intake_items;
create policy agent_intake_public_select
on public.agent_intake_items
for select
to anon
using (public_read = true and lane <> 'PS');

drop policy if exists agent_task_public_select on public.agent_task_queue;
create policy agent_task_public_select
on public.agent_task_queue
for select
to anon
using (public_read = true);

-- Reviews are not public by default. Agent review submission should be handled through
-- authenticated workflow, edge function, or service-role mediation.

comment on table public.agent_intake_items is 'DCSE agent-accessible intake registry. Public-read only for approved non-PS records.';
comment on table public.agent_reviews is 'Agent review outputs. Not public by default.';
comment on table public.agent_task_queue is 'Agent-readable task queue for intake review assignments.';
