-- DCSE-DDNA dedicated normalized schema
-- Target project: uutpzaiqymyufljdgdaa
-- Applied live on 2026-09-09 through governed Supabase tooling.
-- This file is stored under supabase/ddna/migrations intentionally so existing
-- SC-Command-Post migration automation does not treat it as an operations-project migration.

create schema if not exists dcse_ddna;
create schema if not exists dcse_ddna_legacy;

create table if not exists dcse_ddna.authority_registry (
  id uuid primary key default gen_random_uuid(),
  authority_key text not null unique,
  controller_family text not null,
  artifact_name text not null,
  artifact_sha256 text not null,
  revision_identity text,
  authority_state text not null,
  readiness_state text,
  effective_date date,
  issuing_authority text not null,
  designation_source text not null,
  designation_blob_sha text,
  runtime_sync_state text not null default 'pending',
  notes text,
  metadata jsonb not null default '{}'::jsonb,
  recorded_at timestamptz not null default now()
);

create table if not exists dcse_ddna.source_artifacts (
  id uuid primary key default gen_random_uuid(),
  source_key text not null unique,
  task_id text,
  project_name text,
  entity text not null,
  lane text not null,
  source_type text not null,
  source_title text not null,
  source_path text,
  source_hash_sha256 text,
  authority_class text not null default 'unknown',
  authority_status text not null default 'unsynchronized',
  canonical_relationship text,
  sensitivity text not null default 'internal',
  harvest_eligibility text not null default 'eligible',
  content_text text,
  content_json jsonb,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  ingested_at timestamptz not null default now()
);

create table if not exists dcse_ddna.extraction_runs (
  id uuid primary key default gen_random_uuid(),
  run_key text not null unique,
  task_id text,
  project_name text,
  lane text not null,
  batch_number integer,
  run_type text not null,
  status text not null,
  source_count integer,
  processed_source_count integer,
  record_count integer,
  duplicate_count integer,
  error_count integer,
  authority_status text not null default 'unsynchronized',
  metadata jsonb not null default '{}'::jsonb,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists dcse_ddna.extraction_items (
  id uuid primary key default gen_random_uuid(),
  extraction_key text not null unique,
  extraction_run_id uuid references dcse_ddna.extraction_runs(id) on delete set null,
  source_artifact_id uuid references dcse_ddna.source_artifacts(id) on delete set null,
  source_locator text,
  record_type text not null check (record_type in ('fact','characteristic','pattern','rule_candidate','other')),
  statement text not null,
  normalized_statement text,
  entity text not null,
  domain text,
  confidence numeric,
  authority_weight numeric,
  evidence_refs jsonb not null default '[]'::jsonb,
  conflicts jsonb not null default '[]'::jsonb,
  supersession_state text,
  review_status text not null default 'observed',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists dcse_ddna.characteristics (
  id uuid primary key default gen_random_uuid(),
  characteristic_key text not null unique,
  extraction_run_id uuid references dcse_ddna.extraction_runs(id) on delete set null,
  source_artifact_id uuid references dcse_ddna.source_artifacts(id) on delete set null,
  entity text not null,
  lane text not null,
  dimension text not null,
  characteristic text not null,
  candidate_rule text,
  source_ref text,
  supporting_excerpt text,
  source_count integer not null default 1,
  extracting_model text,
  model_agreement jsonb not null default '{}'::jsonb,
  contradicting_evidence text,
  confidence_score numeric,
  status text not null default 'observed',
  ps_lock boolean not null default false,
  approved_by text,
  promotion_date timestamptz,
  rag_eligible boolean not null default false,
  rag_ingested_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_ddna.rules (
  id uuid primary key default gen_random_uuid(),
  rule_id text not null unique,
  rule_family text,
  entity text not null,
  domain text,
  scope text,
  title text,
  statement text not null,
  condition_text text,
  action_text text,
  exception_text text,
  priority integer,
  authority_level text,
  source_refs jsonb not null default '[]'::jsonb,
  evidence_refs jsonb not null default '[]'::jsonb,
  confidence numeric,
  status text not null,
  version text,
  supersedes text,
  conflicts_with jsonb not null default '[]'::jsonb,
  last_reviewed timestamptz,
  last_tested timestamptz,
  last_fired timestamptz,
  fire_count integer not null default 0,
  outcome_score numeric,
  promotion_authority text,
  authority_status text not null default 'unsynchronized',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_ddna.rule_conflicts (
  id uuid primary key default gen_random_uuid(),
  conflict_id text not null unique,
  entity text not null,
  topic text not null,
  source_a text,
  source_b text,
  disposition text not null,
  status text not null default 'open',
  authority_status text not null default 'unsynchronized',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists dcse_ddna.rule_tests (
  id uuid primary key default gen_random_uuid(),
  test_key text not null unique,
  rule_id text references dcse_ddna.rules(rule_id) on delete set null,
  test_type text not null check (test_type in ('forward','backward','rules_fired','regression','firewall','other')),
  batch_number integer,
  input_data jsonb not null default '{}'::jsonb,
  expected_data jsonb not null default '{}'::jsonb,
  actual_data jsonb not null default '{}'::jsonb,
  pass boolean,
  failure_reason text,
  metadata jsonb not null default '{}'::jsonb,
  tested_at timestamptz not null default now()
);

create table if not exists dcse_ddna.batch_metrics (
  id uuid primary key default gen_random_uuid(),
  batch_key text not null unique,
  task_id text,
  batch_number integer not null,
  status text not null,
  metrics jsonb not null default '{}'::jsonb,
  repairs jsonb not null default '[]'::jsonb,
  comparison_to_prior jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists dcse_ddna.provenance_links (
  id uuid primary key default gen_random_uuid(),
  origin_event_id text,
  source_key text,
  derived_from text,
  copied_to text,
  summarized_from text,
  promoted_into text,
  relationship_type text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists dcse_ddna.artifact_registry (
  id uuid primary key default gen_random_uuid(),
  artifact_key text not null unique,
  task_id text,
  artifact_type text not null,
  path text,
  filename text,
  sha256 text,
  byte_size bigint,
  status text not null,
  authority_status text not null default 'unsynchronized',
  git_commit_sha text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists dcse_ddna.legacy_import_snapshots (
  id uuid primary key default gen_random_uuid(),
  snapshot_key text not null unique,
  source_project_id text not null,
  source_schema text not null,
  source_table text not null,
  source_offset integer not null default 0,
  source_row_count integer not null,
  payload jsonb not null,
  ps_locked_rows integer not null default 0,
  status text not null default 'copied',
  metadata jsonb not null default '{}'::jsonb,
  imported_at timestamptz not null default now()
);

-- Defense-in-depth. These schemas are not intended for direct anonymous client use.
do $$
declare r record;
begin
  for r in select schemaname, tablename from pg_tables where schemaname in ('dcse_ddna','dcse_ddna_legacy') loop
    execute format('alter table %I.%I enable row level security', r.schemaname, r.tablename);
  end loop;
end $$;

grant usage on schema dcse_ddna, dcse_ddna_legacy to service_role;
grant select, insert, update, delete on all tables in schema dcse_ddna, dcse_ddna_legacy to service_role;

create index if not exists idx_source_artifacts_task on dcse_ddna.source_artifacts(task_id);
create index if not exists idx_source_artifacts_lane on dcse_ddna.source_artifacts(lane);
create index if not exists idx_extraction_items_type on dcse_ddna.extraction_items(record_type);
create index if not exists idx_rules_entity_status on dcse_ddna.rules(entity,status);
create index if not exists idx_conflicts_entity_status on dcse_ddna.rule_conflicts(entity,status);
create index if not exists idx_provenance_origin on dcse_ddna.provenance_links(origin_event_id);
