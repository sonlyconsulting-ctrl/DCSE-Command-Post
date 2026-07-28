-- B3 reference seed: registration of the real worker identities.
--
-- Enrollment secrets are NOT in this file and must never be committed. After
-- running this, enrol each agent on the durable host with an operator-supplied
-- secret of at least 24 characters:
--
--   select * from v7_worker.enroll_worker(
--     'AGENT-CLAUDE-REVIEWER-01@STAGING',
--     'claude-reviewer-01@workers.dcse',
--     '<operator supplied secret>');
--
-- The plaintext is never stored; only a bcrypt hash is kept.

insert into v7_worker.agent_identity
 (agent_id, agent_name, model_family, device_id, device_hostname, deployment_env,
  authorized_lanes, authorized_task_types, approval_mode,
  max_concurrent_tasks, max_wall_time_minutes, max_session_turns, max_attempts_per_task,
  monthly_cost_limit_usd, tool_allowlist, tool_denylist, status)
values
 ('AGENT-CLAUDE-REVIEWER-01@STAGING','Claude Reviewer','claude','STAGING','staging-host','staging',
  '{DCSE,SC}', '{architecture_review,evaluation,doctrine_reconciliation,blueprint}', 'governed-approval',
  1, 30, 30, 3, 50.00,
  '["read_files","search","analyze","comment"]'::jsonb,
  '["write_main","promote_persona","approve_own_output"]'::jsonb, 'approved'),

 ('AGENT-QWEN-BUILDER-01@STAGING','Qwen Coder','qwen','STAGING','staging-host','staging',
  '{DCSE,RAG,DDNA,SYSTEM}', '{schema_generation,script,extraction,migration,implementation,repair}', 'auto-edit',
  1, 45, 40, 3, 50.00,
  '["read_files","write_branch","run_tests","search"]'::jsonb,
  '["write_main","approve_own_output","production_ddl"]'::jsonb, 'approved'),

 ('AGENT-DETERMINISTIC-VALIDATOR-01@STAGING','Deterministic Validator','deterministic','STAGING','staging-host','staging',
  '{DCSE,SYSTEM}', '{validation,test_execution,schema_check,rls_test,acceptance_criteria}', 'read-only',
  1, 20, 15, 2, 10.00,
  '["read_files","run_tests","execute_sql_readonly"]'::jsonb,
  '["write_any","approve_own_output"]'::jsonb, 'approved'),

 ('AGENT-DISPATCHER-01@STAGING','Dispatcher / Recovery','deterministic','STAGING','staging-host','staging',
  '{SYSTEM}', '{dispatch,recovery,escalation}', 'plan-only',
  1, 10, 10, 1, 10.00,
  '["read_files","recover_claims","escalate_dead_letter"]'::jsonb,
  '["write_results","approve_own_output"]'::jsonb, 'approved')
on conflict (agent_id) do update set
  authorized_lanes      = excluded.authorized_lanes,
  authorized_task_types = excluded.authorized_task_types,
  approval_mode         = excluded.approval_mode,
  monthly_cost_limit_usd= excluded.monthly_cost_limit_usd,
  max_attempts_per_task = excluded.max_attempts_per_task,
  tool_allowlist        = excluded.tool_allowlist,
  tool_denylist         = excluded.tool_denylist,
  status                = excluded.status;

-- No worker is granted the PS lane.
