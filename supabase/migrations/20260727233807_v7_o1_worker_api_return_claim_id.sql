-- Defect O1-D1: the worker API returned no claim_id, so a worker had no handle
-- to renew or submit against the lease it had just acquired. Workers have no
-- direct access to v7_worker.task_claim (by design), so the handle must come
-- back from the RPC itself. Found by role-matrix case 14.

drop function if exists v7_worker_api.claim_next_task(integer);

create or replace function v7_worker_api.claim_next_task(p_visibility_timeout_seconds integer default 1800)
returns table(claim_id bigint, queue_msg_id bigint, task_id text, lane text,
              task_type text, priority integer, runtime_packet jsonb,
              attempt_number integer, visibility_timeout_at timestamptz)
language plpgsql security definer set search_path = '' as $$
declare
  v_row v7_worker.agent_identity%rowtype;
  v_task record;
  v_claim v7_worker.task_claim%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();

  if p_visibility_timeout_seconds is null
     or p_visibility_timeout_seconds < 60 or p_visibility_timeout_seconds > 7200 then
    raise exception 'visibility timeout must be between 60 and 7200 seconds' using errcode = '22023';
  end if;

  select * into v_task from v7_worker.claim_next_task(v_row.agent_id, p_visibility_timeout_seconds);
  if v_task is null or v_task.task_id is null then
    return;
  end if;

  select * into v_claim from v7_worker.task_claim tc
  where tc.agent_id = v_row.agent_id and tc.queue_msg_id = v_task.queue_msg_id and tc.released_at is null
  order by tc.claim_id desc limit 1;

  return query select
    v_claim.claim_id, v_task.queue_msg_id, v_task.task_id, v_task.lane,
    v_task.task_type, v_task.priority, v_task.runtime_packet,
    v_task.attempt_number, v_claim.visibility_timeout_at;
end $$;

create or replace function v7_worker_api.my_active_claims()
returns table(claim_id bigint, task_id text, lane text, task_type text,
              visibility_timeout_at timestamptz, attempt_number integer)
language plpgsql stable security definer set search_path = '' as $$
declare v_row v7_worker.agent_identity%rowtype;
begin
  v_row := v7_worker_private.require_approved_agent();
  return query
  select tc.claim_id, tc.task_id, tc.lane, tc.task_type, tc.visibility_timeout_at, tc.attempt_number
  from v7_worker.task_claim tc
  where tc.agent_id = v_row.agent_id and tc.released_at is null and tc.visibility_timeout_at > now()
  order by tc.claim_id desc;
end $$;

revoke all on function v7_worker_api.claim_next_task(integer) from public, anon;
revoke all on function v7_worker_api.my_active_claims() from public, anon;
grant execute on function v7_worker_api.claim_next_task(integer) to authenticated, service_role;
grant execute on function v7_worker_api.my_active_claims() to authenticated, service_role;
