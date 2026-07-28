-- B4 step 1 prerequisite: the result bridge must be tested in an environment
-- containing BOTH v7_worker and dcse_cp. The preview branch carried only
-- v7_worker, and production DDL is forbidden, so dcse_cp is mirrored here.
--
-- Faithful subset of the production dcse_cp contract: same enum types, same
-- NOT NULL columns, same event_type CHECK, same foreign keys. The bridge is
-- therefore exercised against the real constraints, not a permissive stand-in.
-- This also closes O2 (bridge retest in a combined-schema environment).

create schema if not exists dcse_cp;

do $t$
begin
  if not exists (select 1 from pg_type t join pg_namespace n on n.oid=t.typnamespace
                 where n.nspname='dcse_cp' and t.typname='lane_code') then
    create type dcse_cp.lane_code as enum ('DCSE','PS','SC','SS','TSL','TRIBUNAL','DDNA','RAG','SYSTEM');
  end if;
  if not exists (select 1 from pg_type t join pg_namespace n on n.oid=t.typnamespace
                 where n.nspname='dcse_cp' and t.typname='confidentiality_level') then
    create type dcse_cp.confidentiality_level as enum ('public_safe','internal','ps_confidential');
  end if;
end $t$;

create table if not exists dcse_cp.agent_registry (
  id uuid primary key default gen_random_uuid(),
  agent_label text not null unique,
  created_at timestamptz not null default now()
);

create table if not exists dcse_cp.agent_tasks (
  id uuid primary key default gen_random_uuid(),
  task_key text not null unique,
  title text not null,
  lane dcse_cp.lane_code not null default 'DCSE',
  confidentiality dcse_cp.confidentiality_level not null default 'internal',
  task_type text not null,
  priority integer not null default 3,
  status text not null default 'planned',
  assignment_mode text not null default 'single',
  input_refs jsonb not null default '[]'::jsonb,
  output_refs jsonb not null default '[]'::jsonb,
  policy_flags jsonb not null default '{}'::jsonb,
  dcs_decision_required boolean not null default false,
  review_required boolean not null default false,
  created_by_label text not null default 'system',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_cp.agent_task_events (
  id uuid primary key default gen_random_uuid(),
  task_id uuid not null references dcse_cp.agent_tasks(id) on delete cascade,
  event_type text not null check (event_type in
    ('created','assigned','started','completed','blocked','handoff',
     'parallel_dispatch','review','comment','decision','receipt','status_change')),
  from_agent_id uuid references dcse_cp.agent_registry(id) on delete set null,
  to_agent_id   uuid references dcse_cp.agent_registry(id) on delete set null,
  actor_label text not null default 'system',
  event_summary text not null,
  event_payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_agent_task_events_task on dcse_cp.agent_task_events(task_id, created_at desc);

alter table dcse_cp.agent_registry    enable row level security;
alter table dcse_cp.agent_tasks       enable row level security;
alter table dcse_cp.agent_task_events enable row level security;

do $p$
begin
  if not exists (select 1 from pg_policies where schemaname='dcse_cp' and tablename='agent_tasks' and policyname='service_role_full_access') then
    create policy service_role_full_access on dcse_cp.agent_tasks for all to service_role using (true) with check (true);
  end if;
  if not exists (select 1 from pg_policies where schemaname='dcse_cp' and tablename='agent_task_events' and policyname='service_role_full_access') then
    create policy service_role_full_access on dcse_cp.agent_task_events for all to service_role using (true) with check (true);
  end if;
  if not exists (select 1 from pg_policies where schemaname='dcse_cp' and tablename='agent_registry' and policyname='service_role_full_access') then
    create policy service_role_full_access on dcse_cp.agent_registry for all to service_role using (true) with check (true);
  end if;
end $p$;

revoke usage on schema dcse_cp from public, anon, authenticated;
grant usage on schema dcse_cp to service_role;
