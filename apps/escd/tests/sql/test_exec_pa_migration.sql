\set ON_ERROR_STOP on

SET ROLE authenticated;
SET "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';

INSERT INTO dcse_cp.escd_projects (
  id, project_key, title, objective, source_refs
) VALUES (
  '10000000-0000-0000-0000-000000000001',
  'ci-project-1',
  'CI ESCD project',
  'Validate integrated executive and PA state',
  '["source:project"]'::jsonb
);

INSERT INTO dcse_cp.escd_items (
  id, item_key, title, status, task_class, context, project_id,
  source_system, source_id, normalized_intent, source_refs
) VALUES (
  '20000000-0000-0000-0000-000000000001',
  'ci-item-1',
  'CI executive item',
  'captured',
  'CAPTURE',
  'general',
  '10000000-0000-0000-0000-000000000001',
  'test',
  'source-1',
  'validate executive item',
  '["source:item:1"]'::jsonb
);

DO $$
DECLARE v_creator uuid;
BEGIN
  SELECT created_by_user_id INTO v_creator
  FROM dcse_cp.escd_items
  WHERE id = '20000000-0000-0000-0000-000000000001';
  IF v_creator IS DISTINCT FROM auth.uid() THEN
    RAISE EXCEPTION 'item_creator_not_bound_to_principal';
  END IF;
END $$;

-- Item lifecycle must match the pre-existing policy graph and emit history.
UPDATE dcse_cp.escd_items
SET status = 'triaged'
WHERE id = '20000000-0000-0000-0000-000000000001';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_item_events
    WHERE item_id = '20000000-0000-0000-0000-000000000001'
      AND event_type = 'status_transition'
      AND metadata->>'from_status' = 'captured'
      AND metadata->>'to_status' = 'triaged'
  ) THEN
    RAISE EXCEPTION 'item_transition_event_missing';
  END IF;
END $$;

UPDATE dcse_cp.escd_items
SET status = 'waiting'
WHERE id = '20000000-0000-0000-0000-000000000001';

DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_items
    SET status = 'planned'
    WHERE id = '20000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'waiting_to_planned_drift_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

UPDATE dcse_cp.escd_items
SET status = 'active', actionable = true
WHERE id = '20000000-0000-0000-0000-000000000001';

-- Source provenance can be extended without deleting existing source refs.
UPDATE dcse_cp.escd_items
SET source_refs = '["source:item:1","source:item:2"]'::jsonb
WHERE id = '20000000-0000-0000-0000-000000000001';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_items
    WHERE id = '20000000-0000-0000-0000-000000000001'
      AND source_refs ? 'source:item:1'
      AND source_refs ? 'source:item:2'
  ) THEN
    RAISE EXCEPTION 'source_provenance_merge_failed';
  END IF;
END $$;

INSERT INTO dcse_cp.escd_decisions (
  id, decision_key, item_id, question, facts, unknowns, alternatives,
  tradeoffs, recommendation, decision, evidence_refs, source_refs
) VALUES (
  '30000000-0000-0000-0000-000000000001',
  'ci-decision-1',
  '20000000-0000-0000-0000-000000000001',
  'Proceed with candidate validation?',
  '["tests exist"]'::jsonb,
  '[]'::jsonb,
  '["proceed","hold"]'::jsonb,
  '["speed","risk"]'::jsonb,
  'proceed',
  'proceed',
  '["evidence:test"]'::jsonb,
  '["source:decision"]'::jsonb
);

INSERT INTO dcse_cp.escd_contact_contexts (
  id, context_key, contact_ref, display_name, provenance_refs, confidence_status
) VALUES (
  '40000000-0000-0000-0000-000000000001',
  'ci-contact-1',
  'contacts:1',
  'Example Person',
  '["contacts:1","gmail:thread:1"]'::jsonb,
  'verified'
);

INSERT INTO dcse_cp.escd_routines (
  id, routine_key, version, mission, purpose, trigger_type, trigger_spec,
  autonomy_class, source_refs, action_template, expected_evidence, failure_policy,
  escalation_class
) VALUES (
  '50000000-0000-0000-0000-000000000001',
  'ci-routine-1',
  1,
  'general',
  'Daily executive review',
  'time',
  '{"schedule":"daily"}'::jsonb,
  'A1_AUTO_LOG',
  '["source:routine"]'::jsonb,
  '{"operation":"REVIEW"}'::jsonb,
  '["receipt"]'::jsonb,
  '{"max_attempts":2}'::jsonb,
  'N1'
);

-- Runtime state may pause a routine, but changing its immutable configuration requires a new version.
UPDATE dcse_cp.escd_routines
SET paused = true
WHERE id = '50000000-0000-0000-0000-000000000001';

DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_routines
    SET purpose = 'silently changed purpose'
    WHERE id = '50000000-0000-0000-0000-000000000001';
    RAISE EXCEPTION 'routine_configuration_mutation_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

INSERT INTO dcse_cp.escd_notification_intents (
  id, notification_key, notification_class, source_event_ref, item_id,
  reason, channel, state, payload
) VALUES (
  '60000000-0000-0000-0000-000000000001',
  'ci-notification-1',
  'N2',
  'event:1',
  '20000000-0000-0000-0000-000000000001',
  'meaningful_change',
  'in_app',
  'created',
  '{"test":true}'::jsonb
);

-- Candidate tranche stores notification intent only and must not claim delivery.
DO $$
BEGIN
  BEGIN
    INSERT INTO dcse_cp.escd_notification_intents (
      notification_key, notification_class, source_event_ref, reason, channel, state
    ) VALUES (
      'ci-notification-false-delivery',
      'N1',
      'event:2',
      'test',
      'android_push',
      'delivered'
    );
    RAISE EXCEPTION 'false_notification_delivery_state_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

-- Append-oriented provenance/decision/notification records are not mutable by normal runtime callers.
DO $$
BEGIN
  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_item_events SET summary = ''tampered''';
    RAISE EXCEPTION 'item_event_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_decisions SET decision = ''changed'' WHERE decision_key = ''ci-decision-1''';
    RAISE EXCEPTION 'decision_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_contact_contexts SET display_name = ''changed'' WHERE context_key = ''ci-contact-1''';
    RAISE EXCEPTION 'contact_context_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_notification_intents SET reason = ''changed'' WHERE notification_key = ''ci-notification-1''';
    RAISE EXCEPTION 'notification_intent_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_items WHERE id = ''20000000-0000-0000-0000-000000000001''';
    RAISE EXCEPTION 'item_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

-- Cross-principal inserts fail even though the owner policy itself is true in this isolated harness.
DO $$
BEGIN
  BEGIN
    INSERT INTO dcse_cp.escd_projects (
      project_key, title, source_refs, created_by_user_id
    ) VALUES (
      'ci-project-wrong-principal',
      'Wrong principal',
      '["source:wrong"]'::jsonb,
      '99999999-9999-9999-9999-999999999999'
    );
    RAISE EXCEPTION 'cross_principal_project_insert_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

RESET ROLE;
