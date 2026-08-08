-- Migration 008: propagate runtime identity through claim/submit RPCs
--
-- Migration 007 added runtime_surface/runtime_instance/host/session_id to
-- dcse_cp.agent_heartbeat(), but claim_agent_assignment() and
-- submit_agent_result() each call agent_heartbeat() internally without those
-- params, so every "assignment claimed" / "result submitted" pulse fell back
-- to the default runtime_instance derivation (agent_key || ':' || host) --
-- diverging from the explicit runtime_instance the caller set on its own
-- heartbeat row, recreating a milder version of the same duplicate-identity
-- problem migration 007 fixed. This migration accepts the same optional
-- runtime identity params on both RPCs and threads them through.

begin;

create or replace function dcse_cp.claim_agent_assignment(
  p_agent_key text,
  p_task_key text,
  p_runtime_surface text default 'unspecified',
  p_runtime_instance text default null::text,
  p_host text default null::text,
  p_session_id text default null::text
)
 returns jsonb
 language plpgsql
 security definer
 set search_path to 'pg_catalog', 'dcse_cp'
as $function$
declare
  v_agent_id uuid;
  v_task_id uuid;
  v_assignment_id uuid;
begin
  select id into v_agent_id from dcse_cp.agent_registry where agent_key = p_agent_key;
  select id into v_task_id from dcse_cp.agent_tasks where task_key = p_task_key;

  if v_agent_id is null or v_task_id is null then
    return jsonb_build_object('ok', false, 'error', 'agent_or_task_not_found');
  end if;

  select id into v_assignment_id
  from dcse_cp.agent_task_assignments
  where agent_id = v_agent_id and task_id = v_task_id
  limit 1;

  if v_assignment_id is null then
    return jsonb_build_object('ok', false, 'error', 'assignment_not_found');
  end if;

  -- Atomic claim: only succeeds if not already running/completed.
  update dcse_cp.agent_task_assignments
  set status = 'running', updated_at = now()
  where id = v_assignment_id
    and status is distinct from 'running'
    and status is distinct from 'completed';

  if not found then
    return jsonb_build_object('ok', false, 'error', 'already_claimed_or_terminal');
  end if;

  update dcse_cp.agent_tasks
  set status = 'running', updated_at = now()
  where id = v_task_id
    and status in ('assigned','queued');

  perform dcse_cp.agent_heartbeat(p_agent_key, p_task_key, 'working', '{}'::jsonb, 'assignment claimed',
    p_runtime_surface, p_runtime_instance, p_host, p_session_id);

  insert into dcse_cp.agent_task_events(task_id, event_type, from_agent_id, actor_label, event_summary, event_payload)
  values(v_task_id, 'started', v_agent_id, p_agent_key, p_agent_key || ' claimed assignment for ' || p_task_key,
    jsonb_build_object('assignment_id', v_assignment_id, 'runtime_surface', p_runtime_surface, 'runtime_instance', p_runtime_instance));

  return jsonb_build_object('ok', true, 'assignment_id', v_assignment_id, 'task_key', p_task_key, 'agent_key', p_agent_key, 'status', 'running');
end;
$function$;

create or replace function dcse_cp.submit_agent_result(
  p_agent_key text,
  p_task_key text,
  p_result_payload jsonb,
  p_status text default 'completed'::text,
  p_runtime_surface text default 'unspecified',
  p_runtime_instance text default null::text,
  p_host text default null::text,
  p_session_id text default null::text
)
 returns jsonb
 language plpgsql
 security definer
 set search_path to 'pg_catalog', 'dcse_cp'
as $function$
declare
  v_agent_id uuid;
  v_task_id uuid;
  v_assignment_id uuid;
  v_remaining integer;
begin
  select id into v_agent_id from dcse_cp.agent_registry where agent_key = p_agent_key;
  select id into v_task_id from dcse_cp.agent_tasks where task_key = p_task_key;

  if v_agent_id is null or v_task_id is null then
    return jsonb_build_object('ok', false, 'error', 'agent_or_task_not_found');
  end if;

  select id into v_assignment_id
  from dcse_cp.agent_task_assignments
  where agent_id = v_agent_id and task_id = v_task_id
  limit 1;

  if v_assignment_id is null then
    return jsonb_build_object('ok', false, 'error', 'assignment_not_found');
  end if;

  update dcse_cp.agent_task_assignments
  set status = p_status,
      result_payload = coalesce(p_result_payload, '{}'::jsonb),
      updated_at = now()
  where id = v_assignment_id;

  insert into dcse_cp.agent_task_events(task_id, event_type, from_agent_id, actor_label, event_summary, event_payload)
  values(v_task_id, 'receipt', v_agent_id, p_agent_key, p_agent_key || ' submitted result for ' || p_task_key,
    jsonb_build_object('assignment_id', v_assignment_id, 'status', p_status, 'result_payload', p_result_payload,
      'runtime_surface', p_runtime_surface, 'runtime_instance', p_runtime_instance, 'host', p_host));

  select count(*) into v_remaining
  from dcse_cp.agent_task_assignments
  where task_id = v_task_id
    and status not in ('completed','submitted','blocked','failed');

  if v_remaining = 0 then
    update dcse_cp.agent_tasks
    set status = case when review_required or dcs_decision_required then 'awaiting_dcs' else 'completed' end,
        completed_at = case when review_required or dcs_decision_required then null else now() end,
        updated_at = now()
    where id = v_task_id;
  else
    update dcse_cp.agent_tasks
    set updated_at = now()
    where id = v_task_id;
  end if;

  perform dcse_cp.agent_heartbeat(p_agent_key, p_task_key, 'result_submitted', '{}'::jsonb, 'result submitted',
    p_runtime_surface, p_runtime_instance, p_host, p_session_id);

  return jsonb_build_object('ok', true, 'assignment_id', v_assignment_id, 'task_key', p_task_key, 'agent_key', p_agent_key, 'status', p_status, 'remaining_open_assignments', v_remaining);
end;
$function$;

commit;
