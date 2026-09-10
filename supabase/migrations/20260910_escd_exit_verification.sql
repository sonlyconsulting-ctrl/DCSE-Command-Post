-- ESCD exit-criteria verification candidate
-- Task: DCSE-ESCD-001-RUNTIME-001
-- Status: CANDIDATE. Requires the ESCD runtime state and integrity migrations first.
-- Do not apply to production without release approval.

CREATE TABLE IF NOT EXISTS dcse_cp.escd_job_verifications (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_key text NOT NULL UNIQUE,
    job_id uuid NOT NULL REFERENCES dcse_cp.escd_jobs(id) ON DELETE RESTRICT,
    evidence_id uuid NOT NULL REFERENCES dcse_cp.escd_evidence(id) ON DELETE RESTRICT,
    outcome text NOT NULL CHECK (outcome IN ('verified','failed')),
    verification_method text NOT NULL CHECK (verification_method IN (
        'dcs_confirmed','tool_result','test_result','runtime_observation','source_reconciliation'
    )),
    verifier_user_id uuid NOT NULL DEFAULT auth.uid(),
    notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS escd_job_verifications_job_idx
ON dcse_cp.escd_job_verifications(job_id, created_at DESC, id DESC);

ALTER TABLE dcse_cp.escd_job_verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_job_verifications FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_job_verifications_dcs_owner ON dcse_cp.escd_job_verifications;
CREATE POLICY escd_job_verifications_dcs_owner
ON dcse_cp.escd_job_verifications
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND verifier_user_id = auth.uid());

REVOKE ALL ON dcse_cp.escd_job_verifications FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_job_verifications TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_job_verification()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    evidence_job_id uuid;
    current_job_status text;
BEGIN
    IF NEW.verifier_user_id IS DISTINCT FROM auth.uid() THEN
        RAISE EXCEPTION 'verification_principal_mismatch' USING ERRCODE = 'check_violation';
    END IF;

    SELECT e.job_id INTO evidence_job_id
    FROM dcse_cp.escd_evidence e
    WHERE e.id = NEW.evidence_id;

    IF evidence_job_id IS NULL OR evidence_job_id IS DISTINCT FROM NEW.job_id THEN
        RAISE EXCEPTION 'verification_evidence_job_mismatch' USING ERRCODE = 'check_violation';
    END IF;

    SELECT j.status INTO current_job_status
    FROM dcse_cp.escd_jobs j
    WHERE j.id = NEW.job_id;

    IF current_job_status IS NULL THEN
        RAISE EXCEPTION 'verification_job_not_found' USING ERRCODE = 'check_violation';
    END IF;

    IF current_job_status IN ('completed','cancelled','archived') THEN
        RAISE EXCEPTION 'verification_job_terminal' USING ERRCODE = 'check_violation';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_job_verification_guard ON dcse_cp.escd_job_verifications;
CREATE TRIGGER escd_job_verification_guard
BEFORE INSERT ON dcse_cp.escd_job_verifications
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_job_verification();

REVOKE ALL ON FUNCTION dcse_cp.escd_validate_job_verification() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_job_verification() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_apply_job_verification()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    UPDATE dcse_cp.escd_jobs
    SET exit_criteria_met = (NEW.outcome = 'verified'),
        updated_at = now()
    WHERE id = NEW.job_id;

    INSERT INTO dcse_cp.escd_job_events (
        job_id, event_type, summary, metadata, actor_user_id
    ) VALUES (
        NEW.job_id,
        'exit_criteria_verification',
        format('Exit criteria verification recorded as %s', NEW.outcome),
        jsonb_build_object(
            'verification_id', NEW.id,
            'verification_key', NEW.verification_key,
            'evidence_id', NEW.evidence_id,
            'outcome', NEW.outcome,
            'verification_method', NEW.verification_method
        ),
        auth.uid()
    );

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_job_verification_apply ON dcse_cp.escd_job_verifications;
CREATE TRIGGER escd_job_verification_apply
AFTER INSERT ON dcse_cp.escd_job_verifications
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_apply_job_verification();

REVOKE ALL ON FUNCTION dcse_cp.escd_apply_job_verification() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_apply_job_verification() TO authenticated;

/* ROLLBACK, only after explicit DCS authorization:
DROP TRIGGER IF EXISTS escd_job_verification_apply ON dcse_cp.escd_job_verifications;
DROP FUNCTION IF EXISTS dcse_cp.escd_apply_job_verification();
DROP TRIGGER IF EXISTS escd_job_verification_guard ON dcse_cp.escd_job_verifications;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_job_verification();
DROP TABLE IF EXISTS dcse_cp.escd_job_verifications;
*/
