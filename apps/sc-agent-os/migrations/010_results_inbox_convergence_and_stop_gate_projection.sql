-- Migration 010: Results Inbox + convergence ledger + safe stop-gate projection
--
-- Raw worker receipts remain immutable evidence. This migration adds a separate
-- DCS-facing delivery/convergence layer so completed work is readable without
-- hunting through Supabase/GitHub, and projects active v7_worker stop-gates into
-- the exposed dcse_cp schema without exposing the v7_worker schema itself.

begin;

-- ---------------------------------------------------------------------------
-- 1. Safe stop-gate projection for unattended workers
-- ---------------------------------------------------------------------------
create or replace view dcse_cp.active_stop_gates as
select gate_id, task_id, agent_id, gate_type, description,
       requires_dcs_approval, approval_deadline, raised_at
from v7_worker.stop_gate
where approved_at is null;

comment on view dcse_cp.active_stop_gates is
  'Read-only projection of unresolved v7_worker stop gates for service-role worker checks. The v7_worker schema itself remains unexposed through PostgREST.';

revoke all on dcse_cp.active_stop_gates from public, anon, authenticated;
grant select on dcse_cp.active_stop_gates to service_role;

-- ---------------------------------------------------------------------------
-- 2. Convergence ledger (separate from raw assignment result_payload)
-- ---------------------------------------------------------------------------
create table if not exists dcse_cp.agent_task_convergences (
  id uuid primary key default gen_random_uuid(),
  task_id uuid not null references dcse_cp.agent_tasks(id) on delete cascade,
  convergence_version integer not null,
  created_by_agent_id uuid references dcse_cp.agent_registry(id),
  summary text not null,
  usable_draft text,
  consensus jsonb not null default '[]'::jsonb,
  conflicts jsonb not null default '[]'::jsonb,
  missing_evidence jsonb not null default '[]'::jsonb,
  recommended_disposition text,
  source_event_ids uuid[] not null default '{}'::uuid[],
  source_assignment_ids uuid[] not null default '{}'::uuid[],
  source_artifact_refs jsonb not null default '[]'::jsonb,
  runtime_surface text references dcse_cp.runtime_surface_registry(runtime_surface),
  runtime_instance text,
  created_at timestamptz not null default now(),
  unique(task_id, convergence_version)
);

comment on table dcse_cp.agent_task_convergences is
  'Immutable convergence artifacts derived from raw worker receipts. A convergence never overwrites an assignment result; later synthesis creates a new version.';

revoke all on dcse_cp.agent_task_convergences from public, anon, authenticated;
grant select, insert on dcse_cp.agent_task_convergences to service_role;

-- ---------------------------------------------------------------------------
-- 3. Queue convergence whenever a new receipt arrives
-- ---------------------------------------------------------------------------
create table if not exists dcse_cp.task_convergence_queue (
  task_id uuid primary key references dcse_cp.agent_tasks(id) on delete cascade,
  status text not null default 'pending' check (status in ('pending','in_progress','completed','not_required')),
  reason text not null default 'new_receipt',
  latest_receipt_at timestamptz,
  first_queued_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

revoke all on dcse_cp.task_convergence_queue from public, anon, authenticated;
grant select, update on dcse_cp.task_convergence_queue to service_role;

create or replace function dcse_cp.queue_convergence_from_receipt()
returns trigger
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $function$
begin
  if new.event_type = 'receipt' then
    insert into dcse_cp.task_convergence_queue(task_id,status,reason,latest_receipt_at,first_queued_at,updated_at)
    values(new.task_id,'pending','new_receipt',new.created_at,now(),now())
    on conflict(task_id) do update set
      status='pending',
      reason='new_receipt',
      latest_receipt_at=excluded.latest_receipt_at,
      updated_at=now();
  end if;
  return new;
end;
$function$;

revoke all on function dcse_cp.queue_convergence_from_receipt() from public, anon, authenticated, service_role;

drop trigger if exists trg_queue_convergence_from_receipt on dcse_cp.agent_task_events;
create trigger trg_queue_convergence_from_receipt
after insert on dcse_cp.agent_task_events
for each row execute function dcse_cp.queue_convergence_from_receipt();

-- Backfill tasks that already have receipts so they show in Results Inbox.
insert into dcse_cp.task_convergence_queue(task_id,status,reason,latest_receipt_at,first_queued_at,updated_at)
select e.task_id,'pending','backfill_existing_receipt',max(e.created_at),now(),now()
from dcse_cp.agent_task_events e
where e.event_type='receipt'
group by e.task_id
on conflict(task_id) do nothing;

-- ---------------------------------------------------------------------------
-- 4. Record immutable convergence versions
-- ---------------------------------------------------------------------------
create or replace function dcse_cp.record_task_convergence(
  p_task_key text,
  p_actor_agent_key text,
  p_summary text,
  p_usable_draft text default null,
  p_consensus jsonb default '[]'::jsonb,
  p_conflicts jsonb default '[]'::jsonb,
  p_missing_evidence jsonb default '[]'::jsonb,
  p_recommended_disposition text default null,
  p_source_artifact_refs jsonb default '[]'::jsonb,
  p_runtime_surface text default 'unspecified',
  p_runtime_instance text default null
)
returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog','dcse_cp'
as $function$
declare
  v_task_id uuid;
  v_actor_id uuid;
  v_version integer;
  v_id uuid;
  v_event_ids uuid[];
  v_assignment_ids uuid[];
begin
  select id into v_task_id from dcse_cp.agent_tasks where task_key=p_task_key;
  select id into v_actor_id from dcse_cp.agent_registry where agent_key=p_actor_agent_key;
  if v_task_id is null then
    return jsonb_build_object('ok',false,'error','task_not_found');
  end if;
  if v_actor_id is null then
    return jsonb_build_object('ok',false,'error','actor_not_found');
  end if;

  select coalesce(max(convergence_version),0)+1 into v_version
  from dcse_cp.agent_task_convergences where task_id=v_task_id;

  select coalesce(array_agg(id order by created_at),'{}'::uuid[]) into v_event_ids
  from dcse_cp.agent_task_events where task_id=v_task_id and event_type='receipt';

  select coalesce(array_agg(id order by created_at),'{}'::uuid[]) into v_assignment_ids
  from dcse_cp.agent_task_assignments where task_id=v_task_id;

  insert into dcse_cp.agent_task_convergences(
    task_id,convergence_version,created_by_agent_id,summary,usable_draft,
    consensus,conflicts,missing_evidence,recommended_disposition,
    source_event_ids,source_assignment_ids,source_artifact_refs,
    runtime_surface,runtime_instance
  ) values (
    v_task_id,v_version,v_actor_id,p_summary,p_usable_draft,
    coalesce(p_consensus,'[]'::jsonb),coalesce(p_conflicts,'[]'::jsonb),
    coalesce(p_missing_evidence,'[]'::jsonb),p_recommended_disposition,
    v_event_ids,v_assignment_ids,coalesce(p_source_artifact_refs,'[]'::jsonb),
    p_runtime_surface,p_runtime_instance
  ) returning id into v_id;

  insert into dcse_cp.agent_task_events(task_id,event_type,from_agent_id,actor_label,event_summary,event_payload)
  values(v_task_id,'review',v_actor_id,p_actor_agent_key,
    p_actor_agent_key || ' recorded convergence v' || v_version || ' for ' || p_task_key,
    jsonb_build_object('convergence_id',v_id,'convergence_version',v_version,
      'recommended_disposition',p_recommended_disposition));

  insert into dcse_cp.task_convergence_queue(task_id,status,reason,latest_receipt_at,first_queued_at,updated_at)
  values(v_task_id,'completed','convergence_recorded',now(),now(),now())
  on conflict(task_id) do update set status='completed',reason='convergence_recorded',updated_at=now();

  return jsonb_build_object('ok',true,'convergence_id',v_id,'convergence_version',v_version,
    'task_key',p_task_key,'source_receipt_count',cardinality(v_event_ids));
end;
$function$;

revoke all on function dcse_cp.record_task_convergence(text,text,text,text,jsonb,jsonb,jsonb,text,jsonb,text,text)
  from public, anon, authenticated;
grant execute on function dcse_cp.record_task_convergence(text,text,text,text,jsonb,jsonb,jsonb,text,jsonb,text,text)
  to service_role;

-- ---------------------------------------------------------------------------
-- 5. DCS-facing Results Inbox view
-- ---------------------------------------------------------------------------
create or replace view dcse_cp.agent_results_inbox as
with assignment_rollup as (
  select
    a.task_id,
    count(*) as assignment_count,
    count(*) filter (where a.status in ('completed','submitted','blocked','failed','approved')) as terminal_assignment_count,
    jsonb_agg(jsonb_build_object(
      'assignment_id',a.id,
      'agent_key',r.agent_key,
      'display_name',r.display_name,
      'assignment_status',a.status,
      'result_payload',a.result_payload,
      'result_updated_at',a.updated_at
    ) order by a.created_at) as responses
  from dcse_cp.agent_task_assignments a
  join dcse_cp.agent_registry r on r.id=a.agent_id
  group by a.task_id
), receipt_rollup as (
  select
    e.task_id,
    count(*) as receipt_count,
    count(distinct coalesce(e.actor_label,'')) as responder_count,
    max(e.created_at) as latest_receipt_at,
    jsonb_agg(jsonb_build_object(
      'event_id',e.id,
      'actor_label',e.actor_label,
      'summary',e.event_summary,
      'payload',e.event_payload,
      'created_at',e.created_at
    ) order by e.created_at) as receipts
  from dcse_cp.agent_task_events e
  where e.event_type='receipt'
  group by e.task_id
), latest_convergence as (
  select distinct on (c.task_id)
    c.task_id,c.id as convergence_id,c.convergence_version,c.summary as convergence_summary,
    c.usable_draft,c.consensus,c.conflicts,c.missing_evidence,c.recommended_disposition,c.created_at as converged_at
  from dcse_cp.agent_task_convergences c
  order by c.task_id,c.convergence_version desc
)
select
  t.id as task_id,
  t.task_key,
  t.title,
  t.description,
  t.lane,
  t.status as task_status,
  t.review_required,
  t.dcs_decision_required,
  t.output_refs,
  coalesce(a.assignment_count,0) as assignment_count,
  coalesce(a.terminal_assignment_count,0) as terminal_assignment_count,
  coalesce(r.receipt_count,0) as receipt_count,
  coalesce(r.responder_count,0) as responder_count,
  r.latest_receipt_at,
  a.responses,
  r.receipts,
  q.status as convergence_status,
  q.reason as convergence_reason,
  c.convergence_id,
  c.convergence_version,
  c.convergence_summary,
  c.usable_draft,
  c.consensus,
  c.conflicts,
  c.missing_evidence,
  c.recommended_disposition,
  c.converged_at,
  (
    coalesce(q.status,'pending') <> 'completed'
    and coalesce(r.receipt_count,0) > 0
  ) as needs_convergence
from dcse_cp.agent_tasks t
left join assignment_rollup a on a.task_id=t.id
left join receipt_rollup r on r.task_id=t.id
left join dcse_cp.task_convergence_queue q on q.task_id=t.id
left join latest_convergence c on c.task_id=t.id
where coalesce(r.receipt_count,0) > 0;

comment on view dcse_cp.agent_results_inbox is
  'DCS-facing delivery view: raw responses/receipts plus latest convergence artifact and a needs_convergence flag. Source results are never overwritten.';

revoke all on dcse_cp.agent_results_inbox from public, anon, authenticated;
grant select on dcse_cp.agent_results_inbox to service_role;

commit;
