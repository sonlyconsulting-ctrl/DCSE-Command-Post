\set ON_ERROR_STOP on

SET ROLE authenticated;
SET "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';

-- Foundation sanity: RLS-authenticated principal can create only its own runtime rows.
INSERT INTO dcse_cp.escd_jobs (
  id, job_key, title, status, requires_approval
) VALUES (
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'ci-job-1',
  'CI runtime integrity job',
  'queued',
  false
);

DO $$
DECLARE v_creator uuid;
BEGIN
  SELECT created_by_user_id INTO v_creator
  FROM dcse_cp.escd_jobs
  WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
  IF v_creator IS DISTINCT FROM auth.uid() THEN
    RAISE EXCEPTION 'job_creator_not_bound_to_principal';
  END IF;
END $$;

-- Job lifecycle transition must create append-oriented history.
UPDATE dcse_cp.escd_jobs
SET status = 'running'
WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_job_events
    WHERE job_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
      AND event_type = 'status_transition'
      AND metadata->>'from_status' = 'queued'
      AND metadata->>'to_status' = 'running'
  ) THEN
    RAISE EXCEPTION 'job_transition_event_missing';
  END IF;
END $$;

-- Material approval binding cannot be mutated in place.
INSERT INTO dcse_cp.escd_approvals (
  id, job_id, approval_type, action_key, payload_fingerprint, title, status
) VALUES (
  'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'material_action',
  'job_transition:completed',
  'sha256:test-payload-v1',
  'Approve completion',
  'pending'
);

DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_approvals
    SET action_key = 'job_transition:running'
    WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
    RAISE EXCEPTION 'approval_binding_mutation_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN
      NULL;
  END;
END $$;

-- A valid pending approval can be decided by the authenticated principal.
UPDATE dcse_cp.escd_approvals
SET status = 'approved',
    decided_by_user_id = auth.uid(),
    decided_at = now()
WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_job_events
    WHERE job_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
      AND event_type = 'approval_transition'
      AND metadata->>'approval_id' = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
      AND metadata->>'action_key' = 'job_transition:completed'
      AND metadata->>'to_status' = 'approved'
  ) THEN
    RAISE EXCEPTION 'approval_transition_event_missing';
  END IF;
END $$;

-- Expired approvals cannot be approved after expiration.
INSERT INTO dcse_cp.escd_approvals (
  id, job_id, approval_type, action_key, title, status, expires_at
) VALUES (
  'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbc',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'material_action',
  'job_transition:running',
  'Expired approval',
  'pending',
  now() - interval '1 minute'
);

DO $$
BEGIN
  BEGIN
    UPDATE dcse_cp.escd_approvals
    SET status = 'approved',
        decided_by_user_id = auth.uid(),
        decided_at = now()
    WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbc';
    RAISE EXCEPTION 'expired_approval_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN
      NULL;
  END;
END $$;

-- Evidence and briefing acknowledgements are insertable but immutable to runtime callers.
INSERT INTO dcse_cp.escd_evidence (
  id, evidence_key, job_id, evidence_type, title, content
) VALUES (
  'cccccccc-cccc-cccc-cccc-cccccccccccc',
  'ci-evidence-1',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'test_evidence',
  'CI evidence',
  'immutable test evidence'
);

INSERT INTO dcse_cp.escd_briefing_acks (
  id, acknowledged_through
) VALUES (
  'dddddddd-dddd-dddd-dddd-dddddddddddd',
  now() - interval '1 minute'
);

DO $$
BEGIN
  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_job_events SET summary = ''tampered''';
    RAISE EXCEPTION 'job_event_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_evidence WHERE id = ''cccccccc-cccc-cccc-cccc-cccccccccccc''';
    RAISE EXCEPTION 'evidence_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_briefing_acks SET acknowledged_through = now()';
    RAISE EXCEPTION 'briefing_ack_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_approvals WHERE id = ''bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb''';
    RAISE EXCEPTION 'approval_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_jobs WHERE id = ''aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa''';
    RAISE EXCEPTION 'job_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

RESET ROLE;
