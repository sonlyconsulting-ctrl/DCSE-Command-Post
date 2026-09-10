\set ON_ERROR_STOP on

SET ROLE authenticated;
SET "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';

-- Parent template establishes non-weakening controls.
INSERT INTO dcse_cp.escd_workflow_templates (
  id, template_id, version, name, status, template_type, purpose, scope,
  supported_context_types, definition, effective_controls,
  definition_fingerprint, provenance
) VALUES (
  '10000000-0000-0000-0000-000000000001',
  'BASE-REVIEW', '1.0.0', 'Base Review', 'approved', 'REVIEW',
  'Review a governed target', 'general', '["project","general"]'::jsonb,
  '{"steps":["inspect"]}'::jsonb,
  '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
  'wf-template-parent-fingerprint', '["contract:workflow-template-schema"]'::jsonb
);

-- Child templates cannot weaken parent controls.
DO $$
BEGIN
  BEGIN
    INSERT INTO dcse_cp.escd_workflow_templates (
      template_id, version, name, status, template_type, purpose, scope,
      supported_context_types, definition, parent_template_id, parent_template_version,
      effective_controls, definition_fingerprint, provenance
    ) VALUES (
      'CHILD-WEAK', '1.0.0', 'Weak Child', 'candidate', 'REVIEW', 'test', 'general',
      '["project"]'::jsonb, '{}'::jsonb, 'BASE-REVIEW', '1.0.0',
      '{"approval_required":false,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
      'wf-child-weak-fingerprint', '["test:source"]'::jsonb
    );
    RAISE EXCEPTION 'weakened_child_control_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

-- Valid child can preserve or strengthen controls.
INSERT INTO dcse_cp.escd_workflow_templates (
  id, template_id, version, name, status, template_type, purpose, scope,
  supported_context_types, definition, parent_template_id, parent_template_version,
  effective_controls, definition_fingerprint, provenance
) VALUES (
  '10000000-0000-0000-0000-000000000002',
  'CHILD-REVIEW', '1.0.0', 'Child Review', 'approved', 'REVIEW',
  'Review ESCD project', 'project', '["project"]'::jsonb,
  '{"steps":["inspect"]}'::jsonb, 'BASE-REVIEW', '1.0.0',
  '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
  'wf-child-valid-fingerprint', '["github:issue-70"]'::jsonb
);

INSERT INTO dcse_cp.escd_workflow_instances (
  id, instance_key, template_id, template_version, template_fingerprint,
  template_type, context_type, context_ref, bindings, status, source_refs,
  evidence_refs, effective_controls, execution_authorized
) VALUES (
  '20000000-0000-0000-0000-000000000001',
  'workflow-instance-1', 'CHILD-REVIEW', '1.0.0', 'wf-child-valid-fingerprint',
  'REVIEW', 'project', 'project:escd', '{"target":"ESCD"}'::jsonb,
  'planned', '["github:issue-70"]'::jsonb, '[]'::jsonb,
  '{"approval_required":true,"evidence_required":true,"security_required":true,"rollback_required":true}'::jsonb,
  false
);

-- Runtime cannot self-escalate execution authority.
DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_workflow_instances
    SET execution_authorized = true
    WHERE id = '20000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'workflow_authority_self_escalation_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

-- Template binding is immutable on an instance.
DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_workflow_instances
    SET template_version = '2.0.0'
    WHERE id = '20000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'workflow_template_binding_mutation_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

INSERT INTO dcse_cp.escd_workflow_steps (
  id, instance_id, step_id, sequence_no, dependencies, action_type, instruction,
  input_refs, output_contract, executor, autonomy_class, approval_required,
  verification_method, evidence_required, failure_route, next_step_on_success,
  next_step_on_failure, status
) VALUES (
  '30000000-0000-0000-0000-000000000001',
  '20000000-0000-0000-0000-000000000001', 'inspect', 1, '[]'::jsonb,
  'REVIEW', 'Inspect target', '["target"]'::jsonb, '{"required":["findings"]}'::jsonb,
  'assistant', 'A0_AUTO', false, 'source_reconciliation', true,
  'stop_with_evidence', NULL, NULL, 'pending'
);

-- Step contract fields are immutable after instantiation.
DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_workflow_steps
    SET autonomy_class = 'A3_APPROVAL_REQUIRED'
    WHERE id = '30000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'workflow_step_contract_mutation_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

-- Invalid workflow shortcut is blocked while steps are incomplete.
DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_workflow_instances
    SET status = 'completed', evidence_refs = '["evidence:test"]'::jsonb
    WHERE id = '20000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'workflow_completion_with_incomplete_steps_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

UPDATE dcse_cp.escd_workflow_instances
SET status = 'running'
WHERE id = '20000000-0000-0000-0000-000000000001';

UPDATE dcse_cp.escd_workflow_steps
SET status = 'ready'
WHERE id = '30000000-0000-0000-0000-000000000001';
UPDATE dcse_cp.escd_workflow_steps
SET status = 'running', attempt_count = 1
WHERE id = '30000000-0000-0000-0000-000000000001';

-- Evidence-required step cannot complete without evidence.
DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_workflow_steps
    SET status = 'completed'
    WHERE id = '30000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'workflow_step_without_evidence_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

UPDATE dcse_cp.escd_workflow_steps
SET status = 'completed', evidence_refs = '["evidence:inspect-pass"]'::jsonb
WHERE id = '30000000-0000-0000-0000-000000000001';

UPDATE dcse_cp.escd_workflow_instances
SET status = 'completed', evidence_refs = '["evidence:inspect-pass"]'::jsonb
WHERE id = '20000000-0000-0000-0000-000000000001';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_workflow_events
    WHERE instance_id = '20000000-0000-0000-0000-000000000001'
      AND event_type = 'workflow_status_transition'
      AND metadata->>'to_status' = 'completed'
  ) THEN
    RAISE EXCEPTION 'workflow_completion_event_missing';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_workflow_events
    WHERE instance_id = '20000000-0000-0000-0000-000000000001'
      AND step_id = 'inspect'
      AND event_type = 'workflow_step_transition'
      AND metadata->>'to_status' = 'completed'
  ) THEN
    RAISE EXCEPTION 'workflow_step_completion_event_missing';
  END IF;
END $$;

-- Append-oriented history cannot be altered by the runtime principal.
DO $$
BEGIN
  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_workflow_events SET summary = ''tampered''';
    RAISE EXCEPTION 'workflow_event_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_workflow_events';
    RAISE EXCEPTION 'workflow_event_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_workflow_templates SET name = ''tampered'' WHERE template_id = ''BASE-REVIEW''';
    RAISE EXCEPTION 'workflow_template_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

RESET ROLE;
