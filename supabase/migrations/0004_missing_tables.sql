-- Migration: 0004_missing_tables
-- GATE: DCS approval required before applying.
-- Purpose: Create the three tables identified as missing in the schema audit.
--
-- Column schemas below reflect DCSE governance assumptions; DCS must confirm
-- field names and types before this migration is run in production.

-- ─── ddna_extraction_runs ────────────────────────────────────────────────────
-- Tracks each execution of the DDNA extraction pipeline.

create table if not exists public.ddna_extraction_runs (
  id              uuid primary key default gen_random_uuid(),
  run_at          timestamptz not null default now(),
  triggered_by    text not null,           -- 'cron' | 'manual' | 'webhook'
  session_date    date,                    -- optional: date context for the run
  handoff_key     text,                    -- links back to dcse_ddna_signals
  status          text not null default 'pending'
                    check (status in ('pending', 'running', 'completed', 'failed')),
  artifact_id     uuid references public.pm_artifacts(id) on delete set null,
  error_message   text,
  duration_ms     integer,
  created_at      timestamptz not null default now()
);

alter table public.ddna_extraction_runs enable row level security;

create policy "service_role_all_extraction_runs"
  on public.ddna_extraction_runs
  as permissive for all
  to service_role
  using (true) with check (true);

-- ─── ai_agent_registry ───────────────────────────────────────────────────────
-- Canonical list of AI model agents authorised to write to DCSE tables.

create table if not exists public.ai_agent_registry (
  id              uuid primary key default gen_random_uuid(),
  agent_name      text not null unique,
  model_name      text not null,           -- e.g. 'claude-sonnet-4-6'
  role            text not null,           -- e.g. 'extractor' | 'reviewer' | 'planner'
  jwt_subject     text unique,             -- sub claim from provisioned JWT
  is_active       boolean not null default true,
  authorised_by   text,                    -- DCS approver identifier
  authorised_at   timestamptz,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

alter table public.ai_agent_registry enable row level security;

create policy "service_role_all_agent_registry"
  on public.ai_agent_registry
  as permissive for all
  to service_role
  using (true) with check (true);

-- authenticated agents may read their own registry entry
create policy "agent_read_own_registry"
  on public.ai_agent_registry
  as permissive for select
  to authenticated
  using (jwt_subject = (select auth.jwt() ->> 'sub'));

-- ─── realtime_state_sync ─────────────────────────────────────────────────────
-- Stores ephemeral broadcast-channel snapshots for realtime collaboration.
-- Rows are short-lived; a cleanup job should purge rows older than 24 hours.

create table if not exists public.realtime_state_sync (
  id              uuid primary key default gen_random_uuid(),
  channel_name    text not null,
  payload         jsonb not null default '{}',
  broadcast_at    timestamptz not null default now(),
  expires_at      timestamptz not null default (now() + interval '24 hours'),
  created_by      text                 -- agent_name from ai_agent_registry
);

alter table public.realtime_state_sync enable row level security;

create policy "service_role_all_realtime_sync"
  on public.realtime_state_sync
  as permissive for all
  to service_role
  using (true) with check (true);

create policy "authenticated_read_realtime_sync"
  on public.realtime_state_sync
  as permissive for select
  to authenticated
  using (expires_at > now());

-- Indexes for common access patterns
create index if not exists idx_ddna_runs_status         on public.ddna_extraction_runs (status);
create index if not exists idx_ddna_runs_handoff_key    on public.ddna_extraction_runs (handoff_key);
create index if not exists idx_agent_registry_active    on public.ai_agent_registry (is_active);
create index if not exists idx_realtime_expires_at      on public.realtime_state_sync (expires_at);
