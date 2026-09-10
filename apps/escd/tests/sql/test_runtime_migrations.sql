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

-- Persisted exit verification must be evidence-bound, append-only, and derive completion eligibility.
INSERT INTO dcse_cp.escd_job_verifications (
  id, verification_key, job_id, evidence_id, outcome, verification_method, notes
) VALUES (
  'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
  'ci-verification-1',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'cccccccc-cccc-cccc-cccc-cccccccccccc',
  'verified',
  'test_result',
  'CI verification passed'
);

DO $$
DECLARE v_exit boolean;
BEGIN
  SELECT exit_criteria_met INTO v_exit
  FROM dcse_cp.escd_jobs
  WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
  IF v_exit IS DISTINCT FROM true THEN
    RAISE EXCEPTION 'verified_outcome_did_not_derive_exit_criteria';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_job_events
    WHERE job_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
      AND event_type = 'exit_criteria_verification'
      AND metadata->>'verification_id' = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'
      AND metadata->>'evidence_id' = 'cccccccc-cccc-cccc-cccc-cccccccccccc'
      AND metadata->>'outcome' = 'verified'
  ) THEN
    RAISE EXCEPTION 'verification_event_missing';
  END IF;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_job_verifications SET notes = ''tampered'' WHERE id = ''eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee''';
    RAISE EXCEPTION 'verification_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_job_verifications WHERE id = ''eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee''';
    RAISE EXCEPTION 'verification_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

-- Evidence from a different job cannot verify this job, and a non-running job cannot be verified.
INSERT INTO dcse_cp.escd_jobs (
  id, job_key, title, status, requires_approval
) VALUES (
  'ffffffff-ffff-ffff-ffff-ffffffffffff',
  'ci-job-2',
  'CI queued job',
  'queued',
  false
);

INSERT INTO dcse_cp.escd_evidence (
  id, evidence_key, job_id, evidence_type, title, content
) VALUES (
  'cccccccc-cccc-cccc-cccc-cccccccccccd',
  'ci-evidence-2',
  'ffffffff-ffff-ffff-ffff-ffffffffffff',
  'test_evidence',
  'Second CI evidence',
  'different job evidence'
);

DO $$
BEGIN
  BEGIN
    INSERT INTO dcse_cp.escd_job_verifications (
      verification_key, job_id, evidence_id, outcome, verification_method
    ) VALUES (
      'ci-verification-wrong-evidence',
      'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      'cccccccc-cccc-cccc-cccc-cccccccccccd',
      'verified',
      'test_result'
    );
    RAISE EXCEPTION 'cross_job_evidence_verification_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;

  BEGIN
    INSERT INTO dcse_cp.escd_job_verifications (
      verification_key, job_id, evidence_id, outcome, verification_method
    ) VALUES (
      'ci-verification-queued-job',
      'ffffffff-ffff-ffff-ffff-ffffffffffff',
      'cccccccc-cccc-cccc-cccc-cccccccccccd',
      'verified',
      'test_result'
    );
    RAISE EXCEPTION 'queued_job_verification_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

-- Verified running job can now complete using persisted derived exit criteria and existing evidence.
UPDATE dcse_cp.escd_jobs
SET status = 'completed'
WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dcse_cp.escd_jobs
    WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
      AND status = 'completed'
      AND completed_at IS NOT NULL
      AND exit_criteria_met = true
  ) THEN
    RAISE EXCEPTION 'verified_job_completion_failed';
  END IF;

  BEGIN
    INSERT INTO dcse_cp.escd_job_verifications (
      verification_key, job_id, evidence_id, outcome, verification_method
    ) VALUES (
      'ci-verification-after-complete',
      'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      'cccccccc-cccc-cccc-cccc-cccccccccccc',
      'verified',
      'test_result'
    );
    RAISE EXCEPTION 'terminal_job_verification_was_not_blocked';
  EXCEPTION
    WHEN check_violation THEN NULL;
  END;
END $$;

RESET ROLE;
