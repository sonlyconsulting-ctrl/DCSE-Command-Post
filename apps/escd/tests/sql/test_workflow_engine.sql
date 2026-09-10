\set ON_ERROR_STOP on
SET ROLE authenticated;
SET "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';

INSERT INTO dcse_cp.escd_jobs (id, job_key, title, status, requires_approval)
VALUES ('aaaaaaaa-0000-0000-0000-000000000001','workflow-job-1','Workflow orchestration CI job','queued',false);

INSERT INTO dcse_cp.escd_workflow_templates (
 id,template_id,version,name,status,template_type,purpose,scope,supported_context_types,definition,effective_controls,definition_fingerprint,provenance
) VALUES (
 '10000000-0000-0000-0000-000000000001','BASE-REVIEW','1.0.0','Base Review','approved','REVIEW','Review governed target','general',
 '["project","general"]'::jsonb,'{"steps":["inspect","decide"]}'::jsonb,
 '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
 'wf-template-parent-fingerprint','["contract:workflow-template-schema"]'::jsonb
);

DO $$ BEGIN BEGIN
 INSERT INTO dcse_cp.escd_workflow_templates (template_id,version,name,status,template_type,purpose,scope,supported_context_types,definition,parent_template_id,parent_template_version,effective_controls,definition_fingerprint,provenance)
 VALUES ('CHILD-WEAK','1.0.0','Weak Child','candidate','REVIEW','test','general','["project"]'::jsonb,'{}'::jsonb,'BASE-REVIEW','1.0.0','{"approval_required":false,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,'wf-child-weak-fingerprint','["test:source"]'::jsonb);
 RAISE EXCEPTION 'weakened_child_control_was_not_blocked';
 EXCEPTION WHEN check_violation THEN NULL; END; END $$;

INSERT INTO dcse_cp.escd_workflow_templates (
 id,template_id,version,name,status,template_type,purpose,scope,supported_context_types,definition,parent_template_id,parent_template_version,effective_controls,definition_fingerprint,provenance
) VALUES (
 '10000000-0000-0000-0000-000000000002','CHILD-REVIEW','1.0.0','Child Review','approved','REVIEW','Review ESCD project','project','["project"]'::jsonb,
 '{"steps":["inspect","decide"]}'::jsonb,'BASE-REVIEW','1.0.0','{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
 'wf-child-valid-fingerprint','["github:issue-70"]'::jsonb
);

INSERT INTO dcse_cp.escd_workflow_instances (
 id,instance_key,template_id,template_version,template_fingerprint,template_type,context_type,context_ref,bindings,status,source_refs,evidence_refs,effective_controls,execution_authorized,job_id
) VALUES (
 '20000000-0000-0000-0000-000000000000','workflow-plan-only','CHILD-REVIEW','1.0.0','wf-child-valid-fingerprint','REVIEW','project','project:escd-plan','{"target":"ESCD"}'::jsonb,'planned','["github:issue-70"]'::jsonb,'[]'::jsonb,
 '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,false,NULL
);

DO $$ BEGIN
 BEGIN UPDATE dcse_cp.escd_workflow_instances SET execution_authorized=true WHERE id='20000000-0000-0000-0000-000000000000'; RAISE EXCEPTION 'self_escalation_not_blocked'; EXCEPTION WHEN check_violation THEN NULL; END;
 BEGIN UPDATE dcse_cp.escd_workflow_instances SET status='running' WHERE id='20000000-0000-0000-0000-000000000000'; RAISE EXCEPTION 'jobless_execution_not_blocked'; EXCEPTION WHEN check_violation THEN NULL; END;
END $$;

INSERT INTO dcse_cp.escd_workflow_instances (
 id,instance_key,template_id,template_version,template_fingerprint,template_type,context_type,context_ref,bindings,status,source_refs,evidence_refs,effective_controls,execution_authorized,job_id
) VALUES (
 '20000000-0000-0000-0000-000000000001','workflow-instance-1','CHILD-REVIEW','1.0.0','wf-child-valid-fingerprint','REVIEW','project','project:escd','{"target":"ESCD"}'::jsonb,'planned','["github:issue-70"]'::jsonb,'[]'::jsonb,
 '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,true,'aaaaaaaa-0000-0000-0000-000000000001'
);

DO $$ BEGIN BEGIN
 UPDATE dcse_cp.escd_workflow_instances SET job_id=NULL WHERE id='20000000-0000-0000-0000-000000000001';
 RAISE EXCEPTION 'workflow_job_binding_mutation_not_blocked'; EXCEPTION WHEN check_violation THEN NULL; END; END $$;

INSERT INTO dcse_cp.escd_workflow_steps (
 id,instance_id,step_id,sequence_no,dependencies,action_type,instruction,input_refs,output_contract,executor,autonomy_class,approval_required,verification_method,evidence_required,failure_route,next_step_on_success,next_step_on_failure,status
) VALUES
('30000000-0000-0000-0000-000000000001','20000000-0000-0000-0000-000000000001','inspect',1,'[]'::jsonb,'REVIEW','Inspect target','["target"]'::jsonb,'{"required":["findings"]}'::jsonb,'assistant','A0_AUTO',false,'source_reconciliation',true,'stop_with_evidence','decide',NULL,'pending'),
('30000000-0000-0000-0000-000000000002','20000000-0000-0000-0000-000000000001','decide',2,'["inspect"]'::jsonb,'DECIDE','Prepare decision','["findings"]'::jsonb,'{"required":["recommendation"]}'::jsonb,'assistant','A3_APPROVAL_REQUIRED',true,'dcs_confirmed',true,'waiting_approval',NULL,NULL,'pending');

UPDATE dcse_cp.escd_workflow_instances SET status='running' WHERE id='20000000-0000-0000-0000-000000000001';
UPDATE dcse_cp.escd_workflow_steps SET status='ready' WHERE id='30000000-0000-0000-0000-000000000001';
UPDATE dcse_cp.escd_workflow_steps SET status='running',attempt_count=1 WHERE id='30000000-0000-0000-0000-000000000001';

DO $$ BEGIN BEGIN
 UPDATE dcse_cp.escd_workflow_steps SET status='completed' WHERE id='30000000-0000-0000-0000-000000000001';
 RAISE EXCEPTION 'evidence_gate_not_blocked'; EXCEPTION WHEN check_violation THEN NULL; END; END $$;
UPDATE dcse_cp.escd_workflow_steps SET status='completed',evidence_refs='["evidence:inspect-pass"]'::jsonb WHERE id='30000000-0000-0000-0000-000000000001';
UPDATE dcse_cp.escd_workflow_steps SET status='waiting_approval' WHERE id='30000000-0000-0000-0000-000000000002';

DO $$ BEGIN BEGIN
 UPDATE dcse_cp.escd_workflow_steps SET status='running' WHERE id='30000000-0000-0000-0000-000000000002';
 RAISE EXCEPTION 'a3_without_approval_not_blocked'; EXCEPTION WHEN check_violation THEN NULL; END; END $$;

INSERT INTO dcse_cp.escd_approvals (id,job_id,approval_type,action_key,title,status,decided_by_user_id,decided_at)
VALUES ('bbbbbbbb-0000-0000-0000-000000000001','aaaaaaaa-0000-0000-0000-000000000001','workflow_step','workflow_step:decide','Approve workflow decision step','approved',auth.uid(),now());

UPDATE dcse_cp.escd_workflow_steps SET approval_id='bbbbbbbb-0000-0000-0000-000000000001' WHERE id='30000000-0000-0000-0000-000000000002';
UPDATE dcse_cp.escd_workflow_steps SET status='running',attempt_count=1 WHERE id='30000000-0000-0000-0000-000000000002';
UPDATE dcse_cp.escd_workflow_steps SET status='completed',evidence_refs='["evidence:decision-pass"]'::jsonb WHERE id='30000000-0000-0000-0000-000000000002';
UPDATE dcse_cp.escd_workflow_instances SET status='completed',evidence_refs='["evidence:inspect-pass","evidence:decision-pass"]'::jsonb WHERE id='20000000-0000-0000-0000-000000000001';

DO $$ BEGIN
 IF NOT EXISTS (SELECT 1 FROM dcse_cp.escd_workflow_events WHERE instance_id='20000000-0000-0000-0000-000000000001' AND event_type='workflow_status_transition' AND metadata->>'to_status'='completed') THEN RAISE EXCEPTION 'workflow_completion_event_missing'; END IF;
 BEGIN EXECUTE 'UPDATE dcse_cp.escd_workflow_events SET summary=''tampered'''; RAISE EXCEPTION 'history_mutation_not_blocked'; EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 BEGIN EXECUTE 'UPDATE dcse_cp.escd_workflow_templates SET name=''tampered'' WHERE template_id=''BASE-REVIEW'''; RAISE EXCEPTION 'template_mutation_not_blocked'; EXCEPTION WHEN insufficient_privilege THEN NULL; END;
END $$;
RESET ROLE;
