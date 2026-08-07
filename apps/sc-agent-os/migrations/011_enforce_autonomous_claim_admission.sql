-- Migration 011: enforce autonomous runtime admission at the claim boundary.
--
-- The Windows controller/worker are defense-in-depth policy clients, but the
-- database must remain authoritative. A non-admitted runtime cannot claim a
-- task even if a client mis-parses the admission view. The only exception is
-- the explicitly flagged Qwen admission smoke task.

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
  v_admitted boolean := false;
  v_smoke boolean := false;
begin
  select id into v_agent_id from dcse_cp.agent_registry where agent_key = p_agent_key;
  select id into v_task_id from dcse_cp.agent_tasks where task_key = p_task_key;

  if v_agent_id is null or v_task_id is null then
    return jsonb_build_object('ok', false, 'error', 'agent_or_task_not_found');
  end if;

  select admitted_for_autonomous_claim
    into v_admitted
  from dcse_cp.autonomous_dispatch_admission
  where agent_key = p_agent_key;

  select coalesce((policy_flags->>'runtime_admission_smoke')::boolean, false)
    into v_smoke
  from dcse_cp.agent_tasks
  where id = v_task_id;

  if not coalesce(v_admitted,false) then
    if not (p_agent_key = 'qwen_windows_cli' and coalesce(v_smoke,false)) then
      return jsonb_build_object('ok', false, 'error', 'runtime_not_admitted', 'agent_key', p_agent_key);
    end if;
  end if;

  select id into v_assignment_id
  from dcse_cp.agent_task_assignments
  where agent_id = v_agent_id and task_id = v_task_id
  limit 1;

  if v_assignment_id is null then
    return jsonb_build_object('ok', false, 'error', 'assignment_not_found');
  end if;

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

  perform dcse_cp.agent_heartbeat(
    p_agent_key, p_task_key, 'working', '{}'::jsonb, 'assignment claimed',
    p_runtime_surface, p_runtime_instance, p_host, p_session_id
  );

  insert into dcse_cp.agent_task_events(
    task_id, event_type, from_agent_id, actor_label, event_summary, event_payload
  ) values (
    v_task_id, 'started', v_agent_id, p_agent_key,
    p_agent_key || ' claimed assignment for ' || p_task_key,
    jsonb_build_object('assignment_id', v_assignment_id, 'runtime_surface', p_runtime_surface, 'runtime_instance', p_runtime_instance)
  );

  return jsonb_build_object('ok', true, 'assignment_id', v_assignment_id, 'task_key', p_task_key, 'agent_key', p_agent_key, 'status', 'running');
end;
$function$;

commit;
