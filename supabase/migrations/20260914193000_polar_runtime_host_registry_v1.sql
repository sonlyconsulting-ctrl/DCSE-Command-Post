
create table if not exists dcse_cp.runtime_host_registry (
  host_key text primary key,
  display_name text not null,
  host_label text,
  host_class text not null check (host_class in ('WORKSTATION','DESKTOP','SERVER','CLOUD_VM','OTHER')),
  os_family text not null,
  operating_mode text not null check (operating_mode in ('ON_DEMAND','BEST_EFFORT_24X7','ENTERPRISE_24X7')),
  availability_target text not null check (availability_target in ('ON_DEMAND','BEST_EFFORT_24X7','ENTERPRISE_24X7')),
  execution_eligible boolean not null default false,
  dispatch_eligible boolean not null default false,
  security_state text not null check (security_state in ('VERIFIED','CANDIDATE','HOLD_SECURITY','PLANNED','RETIRED')),
  routing_priority integer not null default 0 check (routing_priority >= 0),
  remote_access_mode text,
  notes text,
  enabled boolean not null default true,
  metadata jsonb not null default '{}'::jsonb check (jsonb_typeof(metadata)='object'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists runtime_host_registry_host_label_uq
  on dcse_cp.runtime_host_registry(host_label)
  where host_label is not null;

revoke all on dcse_cp.runtime_host_registry from anon, authenticated;
grant select, insert, update, delete on dcse_cp.runtime_host_registry to service_role;

insert into dcse_cp.runtime_host_registry(
  host_key, display_name, host_label, host_class, os_family,
  operating_mode, availability_target, execution_eligible, dispatch_eligible,
  security_state, routing_priority, remote_access_mode, notes, enabled, metadata
)
values
(
  'DCS-WIN11-PRIMARY','DCS Windows 11 Primary','LAPTOP-74UF76GB','WORKSTATION','Windows 11',
  'ON_DEMAND','ON_DEMAND',true,true,'VERIFIED',100,'ESCD_TO_SUPABASE_EXCHANGE',
  'Primary DCS/DCSE Polar host. Eligible while powered on and heartbeating. Mobile clients do not connect directly to this host; requests persist through Supabase.',
  true,
  jsonb_build_object(
    'role','primary_on_demand',
    'polar_alias','DCSE_Universal_Dispatch_Controller',
    'escd_worker_key','DCS-WINDOWS-OLLAMA-01',
    'phone_access','via_escd_and_supabase',
    'wake_behavior','scheduled_poller_when_host_awake'
  )
),
(
  'DCS-WIN8-SECONDARY-CANDIDATE','DCS Legacy Desktop Secondary Candidate',null,'DESKTOP','Windows 8/8.1 legacy',
  'BEST_EFFORT_24X7','BEST_EFFORT_24X7',false,false,'HOLD_SECURITY',50,'NONE_UNTIL_SECURITY_REVIEW',
  'Potential always-on secondary host only after OS/security remediation. Do not place production secrets or autonomous execution authority on the current legacy OS.',
  false,
  jsonb_build_object(
    'role','secondary_candidate',
    'required_before_enable',jsonb_build_array('supported_os','credential_hardening','host_identity','heartbeat_test','worker_acceptance_test')
  )
),
(
  'DCSE-POLAR-SERVER-01','DCSE Polar Enterprise Server Target',null,'SERVER','TBD supported server OS',
  'ENTERPRISE_24X7','ENTERPRISE_24X7',false,false,'PLANNED',200,'PRIVATE_NETWORK_OR_ZERO_TRUST',
  'Enterprise target for continuous Polar availability. Provider-neutral; may be local server, managed VM, or cloud VM after cost/security review.',
  false,
  jsonb_build_object(
    'role','enterprise_24x7_target',
    'rpo_rto_required',true,
    'monitoring_required',true,
    'automatic_restart_required',true
  )
)
on conflict (host_key) do update
set
  display_name=excluded.display_name,
  host_label=coalesce(excluded.host_label,dcse_cp.runtime_host_registry.host_label),
  host_class=excluded.host_class,
  os_family=excluded.os_family,
  operating_mode=excluded.operating_mode,
  availability_target=excluded.availability_target,
  execution_eligible=excluded.execution_eligible,
  dispatch_eligible=excluded.dispatch_eligible,
  security_state=excluded.security_state,
  routing_priority=excluded.routing_priority,
  remote_access_mode=excluded.remote_access_mode,
  notes=excluded.notes,
  enabled=excluded.enabled,
  metadata=dcse_cp.runtime_host_registry.metadata || excluded.metadata,
  updated_at=now();

create or replace view dcse_cp.runtime_host_status as
select
  h.host_key,
  h.display_name,
  h.host_label,
  h.host_class,
  h.os_family,
  h.operating_mode,
  h.availability_target,
  h.execution_eligible,
  h.dispatch_eligible,
  h.security_state,
  h.routing_priority,
  h.enabled,
  greatest(
    (select max(a.last_seen_at) from dcse_cp.agent_heartbeats a where h.host_label is not null and a.host=h.host_label),
    (select max(w.last_seen_at) from dcse_cp.escd_runtime_workers w where h.host_label is not null and w.host_label=h.host_label)
  ) as last_seen_at,
  case
    when h.security_state='HOLD_SECURITY' then 'HOLD_SECURITY'
    when h.security_state='PLANNED' then 'PLANNED'
    when not h.enabled then 'DISABLED'
    when greatest(
      (select max(a.last_seen_at) from dcse_cp.agent_heartbeats a where h.host_label is not null and a.host=h.host_label),
      (select max(w.last_seen_at) from dcse_cp.escd_runtime_workers w where h.host_label is not null and w.host_label=h.host_label)
    ) >= now()-interval '5 minutes' then 'ONLINE'
    else 'OFFLINE'
  end as effective_status,
  h.remote_access_mode,
  h.notes,
  h.metadata,
  h.updated_at
from dcse_cp.runtime_host_registry h;

revoke all on dcse_cp.runtime_host_status from anon, authenticated;
grant select on dcse_cp.runtime_host_status to service_role;

update dcse_cp.escd_runtime_workers
set metadata=coalesce(metadata,'{}'::jsonb) || jsonb_build_object(
      'host_key','DCS-WIN11-PRIMARY',
      'availability_class','ON_DEMAND',
      'routing_priority',100,
      'access_path','ESCD->Supabase->local worker',
      'host_execution_dependency',true
    ),
    updated_at=now()
where worker_key='DCS-WINDOWS-OLLAMA-01';
