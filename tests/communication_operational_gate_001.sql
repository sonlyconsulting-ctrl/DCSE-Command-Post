-- DCSE Communication Operational Gate 001
-- Read-only certification query. Synthetic SC-safe task execution is queued separately.

with hb as (
  select agent_id, status, current_task_id, sent_at,
         now() - sent_at as age
  from v7_worker.heartbeat
  where agent_id = 'AGENT-CLAUDE-REVIEWER-01@PRODUCTION'
  order by sent_at desc limit 1
), claims as (
  select claim_id, task_id, agent_id, claimed_at, acked_at, released_at
  from v7_worker.task_claim
  where agent_id = 'AGENT-CLAUDE-REVIEWER-01@PRODUCTION'
  order by claimed_at desc limit 1
), results as (
  select submission_id, task_id, agent_id, submission_status,
         submission_attempted_at, submission_acked_at, dc_event_id
  from v7_worker.result_submission
  where agent_id = 'AGENT-CLAUDE-REVIEWER-01@PRODUCTION'
  order by submission_attempted_at desc limit 1
)
select
  (select age < interval '45 seconds' from hb) as gate_01_live_heartbeat,
  exists(select 1 from claims) as gate_02_claim_exists,
  exists(select 1 from results) as gate_03_result_exists,
  (select submission_acked_at is not null from results) as gate_04_result_acked,
  (select dc_event_id is not null from results) as gate_05_bridge_event_mapped,
  (select task_id from claims) = (select task_id from results) as gate_06_task_correlation,
  (select agent_id from hb) = (select agent_id from claims) as gate_07_identity_correlation,
  (select agent_id from claims) = (select agent_id from results) as gate_08_result_identity_correlation,
  (select released_at is not null or acked_at is not null from claims) as gate_09_claim_closed,
  now() as certified_at;
