-- Migration 009: extensible runtime-surface registry + dispatch admission view
--
-- Purpose:
--   1. Replace the Claude-only runtime_surface CHECK vocabulary with a governed
--      registry that can safely admit Claude, Qwen, Codex, and future runtimes.
--   2. Expose one read-only view the neutral Windows dispatcher can use to
--      determine whether a logical agent is presently eligible for autonomous
--      claim. Registry policy remains authoritative; the dispatcher fails closed.
--   3. Preserve the already-verified Claude Windows poller admission while Qwen
--      and Codex remain fail-closed until their host/runtime preflight succeeds.
--
-- Depends on migrations 007/008 from PR #46 (runtime identity columns/RPCs).

begin;

create table if not exists dcse_cp.runtime_surface_registry (
  runtime_surface text primary key,
  runtime_family text not null,
  polling_mode text not null check (polling_mode in ('scheduled','interactive','on_demand','legacy','controller')),
  can_claim boolean not null default false,
  description text not null,
  enabled boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

insert into dcse_cp.runtime_surface_registry(runtime_surface,runtime_family,polling_mode,can_claim,description)
values
  ('cli_windows_poller','claude','scheduled',true,'Legacy/canonical Claude Code Windows CLI poller surface'),
  ('claude_code_windows_cli','claude','scheduled',true,'Claude Code CLI invoked by the neutral Windows dispatcher'),
  ('remote_cloud_ccr','claude','interactive',false,'Claude Code remote/cloud interactive runtime'),
  ('chat_browser','claude','interactive',false,'Claude browser chat surface'),
  ('desktop_app','claude','interactive',false,'Claude desktop application surface'),
  ('qwen_windows_cli','qwen','scheduled',true,'Qwen Code CLI invoked headlessly by the neutral Windows dispatcher'),
  ('codex_windows_cli','openai','scheduled',true,'Codex CLI invoked non-interactively by the neutral Windows dispatcher'),
  ('controller_windows','dcse','controller',false,'Neutral DCSE dispatch controller; never owns task claims'),
  ('worker_v7','dcse','legacy',false,'Legacy v7_worker heartbeat surface'),
  ('unspecified','legacy','legacy',false,'Pre-runtime-identity compatibility surface')
on conflict(runtime_surface) do update set
  runtime_family=excluded.runtime_family,
  polling_mode=excluded.polling_mode,
  can_claim=excluded.can_claim,
  description=excluded.description,
  enabled=true,
  updated_at=now();

alter table dcse_cp.agent_heartbeats
  drop constraint if exists agent_heartbeats_runtime_surface_check;

alter table dcse_cp.agent_heartbeats
  drop constraint if exists agent_heartbeats_runtime_surface_fkey;

alter table dcse_cp.agent_heartbeats
  add constraint agent_heartbeats_runtime_surface_fkey
  foreign key (runtime_surface)
  references dcse_cp.runtime_surface_registry(runtime_surface)
  on update cascade
  on delete restrict;

comment on table dcse_cp.runtime_surface_registry is
  'Governed vocabulary for runtime surfaces. Logical agent role remains dcse_cp.agent_registry.agent_key; this table describes the execution surface, polling mode, and whether the surface class may claim tasks.';

-- Preserve the one runtime already proven on the Windows host. This is keyed by
-- agent_key, not generated UUID, and does not widen any lane/action permission.
update dcse_cp.agent_registry
set metadata = coalesce(metadata,'{}'::jsonb) || jsonb_build_object(
      'poller_eligible', true,
      'automatic_claim_eligible', true,
      'admission_status', 'VERIFIED_WINDOWS_POLLER',
      'verified_runtime_surface', 'claude_code_windows_cli'
    ),
    updated_at = now()
where agent_key='claude_code';

-- Qwen is intentionally NOT admitted here. The controller may run a bounded
-- preflight/admission-smoke worker while these restrictions remain in force.
update dcse_cp.agent_registry
set metadata = coalesce(metadata,'{}'::jsonb) || jsonb_build_object(
      'poller_eligible', false,
      'automatic_claim_eligible', false,
      'admission_status', 'HOST_HEARTBEAT_REQUIRED',
      'expected_runtime_surface', 'qwen_windows_cli'
    ),
    updated_at = now()
where agent_key='qwen_windows_cli';

-- Codex stays registered-but-dormant until its installed Windows CLI/sandbox
-- path is independently preflighted.
update dcse_cp.agent_registry
set metadata = coalesce(metadata,'{}'::jsonb) || jsonb_build_object(
      'poller_eligible', false,
      'automatic_claim_eligible', false,
      'admission_status', 'WINDOWS_PREFLIGHT_REQUIRED',
      'expected_runtime_surface', 'codex_windows_cli'
    ),
    updated_at = now()
where agent_key='codex';

create or replace view dcse_cp.autonomous_dispatch_admission as
select
  r.id as agent_id,
  r.agent_key,
  r.display_name,
  r.status as agent_status,
  r.authorized_lanes,
  r.allowed_actions,
  r.restricted_actions,
  r.metadata,
  coalesce((r.metadata->>'poller_eligible')::boolean, false) as metadata_poller_eligible,
  not ('automatic_task_claim' = any(coalesce(r.restricted_actions,'{}'::text[]))) as automatic_claim_allowed,
  not ('autonomous_polling' = any(coalesce(r.restricted_actions,'{}'::text[]))) as autonomous_polling_allowed,
  (
    r.status = 'active'
    and coalesce((r.metadata->>'poller_eligible')::boolean, false)
    and not ('automatic_task_claim' = any(coalesce(r.restricted_actions,'{}'::text[])))
    and not ('autonomous_polling' = any(coalesce(r.restricted_actions,'{}'::text[])))
  ) as admitted_for_autonomous_claim
from dcse_cp.agent_registry r;

comment on view dcse_cp.autonomous_dispatch_admission is
  'Fail-closed autonomous dispatch admission. An agent must be active, metadata.poller_eligible=true, and have neither automatic_task_claim nor autonomous_polling in restricted_actions.';

grant select on dcse_cp.runtime_surface_registry to service_role;
grant select on dcse_cp.autonomous_dispatch_admission to service_role;

commit;
