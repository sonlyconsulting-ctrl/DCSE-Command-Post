-- B4: replace the placeholder result_bridge_invoke() with a working bridge.
--
-- Two defects had to be fixed for the bridge to be correct at all:
--   B4-D1  No task-id resolution. v7_worker keys tasks by TEXT; dcse_cp requires
--          a UUID with an FK to dcse_cp.agent_tasks. Both production submissions
--          had been written against the SAME hard-coded task UUID regardless of
--          their differing worker task keys. Resolution is now by natural key:
--          dcse_cp.agent_tasks.task_key = result_submission.task_id.
--   B4-D2  No event-type mapping. dcse_cp.agent_task_events.event_type has a
--          CHECK constraint; worker types like 'architecture_review',
--          'needs_review' and 'handoff_ready' would all have been rejected.
--
-- Bridging runs in SQL rather than as an HTTP callout from pg_cron. A callout
-- would require the service-role key to be stored in the database for pg_net to
-- authenticate, which is a worse posture than doing the work in-process. The
-- Edge Function remains deployed for external invocation.

create table if not exists v7_worker.bridge_receipt (
  receipt_id bigint generated always as identity primary key,
  cycle_started_at timestamptz not null default now(),
  processed integer not null default 0,
  failed integer not null default 0,
  skipped integer not null default 0,
  duration_ms integer,
  detail jsonb not null default '{}'::jsonb
);
alter table v7_worker.bridge_receipt enable row level security;
do $p$ begin
  if not exists (select 1 from pg_policies where schemaname='v7_worker' and tablename='bridge_receipt') then
    create policy service_role_full_access on v7_worker.bridge_receipt for all to service_role using (true) with check (true);
  end if;
end $p$;

create or replace function v7_worker_private.map_event_type(p_worker_event text)
returns text language sql immutable set search_path = '' as $$
  select case lower(coalesce(p_worker_event,''))
    when 'completed'           then 'completed'
    when 'blocked'             then 'blocked'
    when 'started'             then 'started'
    when 'assigned'            then 'assigned'
    when 'handoff_ready'       then 'handoff'
    when 'handoff'             then 'handoff'
    when 'needs_review'        then 'review'
    when 'review'              then 'review'
    when 'architecture_review' then 'review'
    when 'validation'          then 'review'
    when 'error'               then 'blocked'
    when 'status_change'       then 'status_change'
    when 'decision'            then 'decision'
    when 'comment'             then 'comment'
    else 'receipt'
  end;
$$;

create or replace function v7_worker.bridge_pending_results(p_limit integer default 10)
returns table(processed integer, failed integer, skipped integer, duration_ms integer, receipt_id bigint)
language plpgsql security definer set search_path = '' as $$
declare
  v_start timestamptz := clock_timestamp();
  v_sub record; v_task_uuid uuid; v_event_id uuid;
  v_processed integer := 0; v_failed integer := 0; v_skipped integer := 0;
  v_detail jsonb := '[]'::jsonb; v_receipt bigint;
begin
  for v_sub in
    select * from v7_worker.result_submission
    where submission_status = 'pending'
    order by submission_attempted_at asc
    limit greatest(1, least(coalesce(p_limit,10), 100))
  loop
    begin
      if v_sub.dc_event_id is not null then
        v_skipped := v_skipped + 1;
        v_detail := v_detail || jsonb_build_object('submission_id', v_sub.submission_id, 'outcome', 'skipped_already_bridged');
        continue;
      end if;

      if v_sub.task_id is null or v_sub.result_event_type is null then
        raise exception 'missing task_id or result_event_type';
      end if;

      select t.id into v_task_uuid from dcse_cp.agent_tasks t where t.task_key = v_sub.task_id;
      if v_task_uuid is null then
        raise exception 'no dcse_cp.agent_tasks row with task_key = %', v_sub.task_id;
      end if;

      insert into dcse_cp.agent_task_events
        (task_id, event_type, actor_label, event_summary, event_payload)
      values (
        v_task_uuid,
        v7_worker_private.map_event_type(v_sub.result_event_type),
        v_sub.agent_id,
        format('Worker %s submitted: %s', v_sub.agent_id, v_sub.result_event_type),
        jsonb_build_object(
          'submission_id', v_sub.submission_id, 'claim_id', v_sub.claim_id,
          'agent_id', v_sub.agent_id, 'worker_session_id', v_sub.worker_session_id,
          'worker_event_type', v_sub.result_event_type, 'worker_task_key', v_sub.task_id,
          'result_output', v_sub.result_output)
      )
      returning id into v_event_id;

      update v7_worker.result_submission
         set submission_status='acked', submission_acked_at=now(),
             dc_event_id=v_event_id::text, last_error=null
       where submission_id = v_sub.submission_id;

      v_processed := v_processed + 1;
      v_detail := v_detail || jsonb_build_object(
        'submission_id', v_sub.submission_id, 'outcome', 'acked',
        'dc_event_id', v_event_id, 'dcse_task_id', v_task_uuid,
        'mapped_event_type', v7_worker_private.map_event_type(v_sub.result_event_type));

    exception when others then
      v_failed := v_failed + 1;
      update v7_worker.result_submission
         set submission_status='failed', last_error=sqlerrm, retries=retries+1
       where submission_id = v_sub.submission_id;
      v_detail := v_detail || jsonb_build_object('submission_id', v_sub.submission_id, 'outcome','failed','error',sqlerrm);
    end;
  end loop;

  insert into v7_worker.bridge_receipt (cycle_started_at, processed, failed, skipped, duration_ms, detail)
  values (v_start, v_processed, v_failed, v_skipped,
          (extract(epoch from (clock_timestamp() - v_start))*1000)::integer,
          jsonb_build_object('submissions', v_detail))
  returning bridge_receipt.receipt_id into v_receipt;

  return query select v_processed, v_failed, v_skipped,
                      (extract(epoch from (clock_timestamp() - v_start))*1000)::integer, v_receipt;
end $$;

create or replace function v7_worker.result_bridge_invoke()
returns text language plpgsql security definer set search_path = '' as $$
declare r record;
begin
  select * into r from v7_worker.bridge_pending_results(25);
  return format('bridge_cycle: processed=%s failed=%s skipped=%s duration_ms=%s receipt=%s',
                r.processed, r.failed, r.skipped, r.duration_ms, r.receipt_id);
exception when others then
  return 'bridge_cycle_error: ' || sqlerrm;
end $$;

revoke all on function v7_worker.bridge_pending_results(integer) from public, anon, authenticated;
revoke all on function v7_worker_private.map_event_type(text) from public, anon, authenticated;
grant execute on function v7_worker.bridge_pending_results(integer) to service_role;

comment on function v7_worker.result_bridge_invoke() is
  'Runs a real bridging cycle: v7_worker.result_submission -> dcse_cp.agent_task_events.
   Resolves the dcse task by task_key, maps worker event types onto the dcse_cp
   CHECK set, is idempotent per submission, and writes a bridge_receipt.';
