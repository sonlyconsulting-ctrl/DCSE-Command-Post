-- DCSE V7.1 dispatch-to-assignment correction
--
-- Problem: CP Dispatch inserted dcse_cp.agent_tasks rows, while pollers consume
-- dcse_cp.agent_task_assignments through get_agent_inbox(). Tasks therefore
-- remained planned and invisible to every poller.
--
-- Correction:
--   1. Create the child assignment row for an explicitly assigned task.
--   2. For an unassigned single-agent CP Dispatch task, select only a live,
--      lane-authorized, capability-compatible unattended poller.
--   3. Leave tasks pending when no eligible runtime exists. Never invent a
--      heartbeat, bypass PS, or route DCS-reserved decisions.
--
-- Rollback:
--   DROP TRIGGER IF EXISTS trg_route_cp_dispatch_task ON dcse_cp.agent_tasks;
--   DROP FUNCTION IF EXISTS dcse_cp.auto_route_cp_dispatch_task();
--   DROP FUNCTION IF EXISTS dcse_cp.route_task_assignment(uuid, text);

create or replace function dcse_cp.route_task_assignment(
  p_task_id uuid,
  p_preferred_agent_key text default null
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, dcse_cp
as $function$
declare
  v_task dcse_cp.agent_tasks%rowtype;
  v_agent_id uuid;
  v_agent_key text;
  v_assignment_id uuid;
  v_routing_source text;
begin
  select *
    into v_task
  from dcse_cp.agent_tasks
  where id = p_task_id
  for update;

  if not found then
    return jsonb_build_object('ok', false, 'error', 'task_not_found', 'task_id', p_task_id);
  end if;

  select a.id
    into v_assignment_id
  from dcse_cp.agent_task_assignments a
  where a.task_id = p_task_id
  order by a.created_at asc
  limit 1;

  if v_assignment_id is not null then
    return jsonb_build_object(
      'ok', true,
      'status', 'assignment_already_exists',
      'task_key', v_task.task_key,
      'assignment_id', v_assignment_id
    );
  end if;

  if v_task.confidentiality::text = 'ps_confidential' then
    insert into dcse_cp.agent_task_events(
      task_id, event_type, actor_label, event_summary, event_payload
    ) values (
      p_task_id,
      'routing_blocked',
      'V7.1 Dispatch Router',
      'Automatic routing blocked by PS confidentiality firewall',
      jsonb_build_object('reason', 'ps_confidential', 'task_key', v_task.task_key)
    );
    return jsonb_build_object('ok', false, 'error', 'ps_firewall', 'task_key', v_task.task_key);
  end if;

  if v_task.dcs_decision_required then
    insert into dcse_cp.agent_task_events(
      task_id, event_type, actor_label, event_summary, event_payload
    ) values (
      p_task_id,
      'routing_blocked',
      'V7.1 Dispatch Router',
      'Automatic routing blocked because DCS decision is required',
      jsonb_build_object('reason', 'dcs_decision_required', 'task_key', v_task.task_key)
    );
    return jsonb_build_object('ok', false, 'error', 'dcs_decision_required', 'task_key', v_task.task_key);
  end if;

  if p_preferred_agent_key is not null then
    select r.id, r.agent_key
      into v_agent_id, v_agent_key
    from dcse_cp.agent_registry r
    where r.agent_key = p_preferred_agent_key
      and r.status = 'active'
      and v_task.lane::text = any(r.authorized_lanes)
    limit 1;
    v_routing_source := 'preferred_agent';
  elsif v_task.assigned_agent_id is not null then
    select r.id, r.agent_key
      into v_agent_id, v_agent_key
    from dcse_cp.agent_registry r
    where r.id = v_task.assigned_agent_id
      and r.status = 'active'
      and v_task.lane::text = any(r.authorized_lanes)
    limit 1;
    v_routing_source := 'task_assigned_agent';
  elsif v_task.assignment_mode = 'single' then
    select r.id, r.agent_key
      into v_agent_id, v_agent_key
    from dcse_cp.agent_registry r
    join dcse_cp.agent_heartbeats h on h.agent_id = r.id
    where r.status = 'active'
      and v_task.lane::text = any(r.authorized_lanes)
      and h.last_seen_at >= now() - interval '3 minutes'
      and h.heartbeat_status in ('online', 'working', 'idle')
      and h.capability_status ->> 'poller' = 'active'
      and not ('automatic_task_claim' = any(coalesce(r.restricted_actions, array[]::text[])))
      and not ('autonomous_polling' = any(coalesce(r.restricted_actions, array[]::text[])))
      and (
        (v_task.task_type = 'build' and r.allowed_actions && array['code_build','backend_build','frontend_build','implementation','repo_work','repository_reconstruction']::text[])
        or (v_task.task_type = 'review' and r.allowed_actions && array['code_review','integration_review','review','qa','security_review','tsl_code_review']::text[])
        or (v_task.task_type = 'qa' and r.allowed_actions && array['tests','qa','code_review','integration_review']::text[])
        or (v_task.task_type = 'github' and r.allowed_actions && array['github_action','repo_work','branch_creation','pr_creation','commit','public_push']::text[])
        or (v_task.task_type = 'database' and r.allowed_actions && array['database_action','query','migration','schema','task_registry','db_audit']::text[])
        or (v_task.task_type = 'tribunal' and r.allowed_actions && array['receipt','chronology','decision_log','conflict_detection']::text[])
        or (v_task.task_type = 'rag' and r.allowed_actions && array['rag_action','source_excavation','inventory_analysis']::text[])
        or (v_task.task_type = 'synthesis' and r.allowed_actions && array['synthesis','strategy']::text[])
        or (v_task.task_type = 'monitor' and r.allowed_actions && array['activity_report','monitor']::text[])
      )
    order by h.last_seen_at desc, r.agent_key asc
    limit 1;
    v_routing_source := 'capability_live_poller';
  end if;

  if v_agent_id is null then
    insert into dcse_cp.agent_task_events(
      task_id, event_type, actor_label, event_summary, event_payload
    ) values (
      p_task_id,
      'routing_pending',
      'V7.1 Dispatch Router',
      'No eligible live poller found; task remains planned',
      jsonb_build_object(
        'task_key', v_task.task_key,
        'lane', v_task.lane::text,
        'task_type', v_task.task_type,
        'assignment_mode', v_task.assignment_mode,
        'preferred_agent_key', p_preferred_agent_key
      )
    );
    return jsonb_build_object(
      'ok', false,
      'error', 'no_eligible_live_poller',
      'task_key', v_task.task_key,
      'status', v_task.status
    );
  end if;

  insert into dcse_cp.agent_task_assignments(
    task_id, agent_id, assignment_role, sequence_order, status
  ) values (
    p_task_id, v_agent_id, 'executor', 1, 'assigned'
  )
  on conflict (task_id, agent_id, assignment_role) do nothing
  returning id into v_assignment_id;

  if v_assignment_id is null then
    select id
      into v_assignment_id
    from dcse_cp.agent_task_assignments
    where task_id = p_task_id
      and agent_id = v_agent_id
      and assignment_role = 'executor';
  end if;

  update dcse_cp.agent_tasks
  set assigned_agent_id = v_agent_id,
      status = case when status = 'planned' then 'assigned' else status end,
      updated_at = now()
  where id = p_task_id;

  insert into dcse_cp.agent_task_events(
    task_id, event_type, to_agent_id, actor_label, event_summary, event_payload
  ) values (
    p_task_id,
    'assigned',
    v_agent_id,
    'V7.1 Dispatch Router',
    'Task assigned to ' || v_agent_key || ' through ' || v_routing_source,
    jsonb_build_object(
      'task_key', v_task.task_key,
      'agent_key', v_agent_key,
      'assignment_id', v_assignment_id,
      'routing_source', v_routing_source,
      'lane', v_task.lane::text,
      'task_type', v_task.task_type
    )
  );

  return jsonb_build_object(
    'ok', true,
    'task_key', v_task.task_key,
    'agent_key', v_agent_key,
    'assignment_id', v_assignment_id,
    'status', 'assigned',
    'routing_source', v_routing_source
  );
end;
$function$;

create or replace function dcse_cp.auto_route_cp_dispatch_task()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, dcse_cp
as $function$
begin
  if new.created_by_label = 'CP Dispatch'
     and new.status in ('planned', 'assigned') then
    perform dcse_cp.route_task_assignment(new.id, null);
  end if;
  return new;
end;
$function$;

drop trigger if exists trg_route_cp_dispatch_task on dcse_cp.agent_tasks;
create trigger trg_route_cp_dispatch_task
after insert on dcse_cp.agent_tasks
for each row
execute function dcse_cp.auto_route_cp_dispatch_task();

revoke all on function dcse_cp.route_task_assignment(uuid, text) from public;
grant execute on function dcse_cp.route_task_assignment(uuid, text) to service_role;
