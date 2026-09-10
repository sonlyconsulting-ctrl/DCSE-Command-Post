-- ESCD runtime integrity patch candidate
-- Task: DCSE-ESCD-001-RUNTIME-001
-- Status: CANDIDATE. Requires 20260909_escd_runtime_state.sql first.
-- Do not apply to production without release approval.

-- Authoritative history/evidence are append-oriented. Jobs are lifecycle-managed,
-- approvals are decision-updatable, and delete is not a normal runtime operation.
REVOKE ALL ON dcse_cp.escd_jobs FROM authenticated;
GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_jobs TO authenticated;

REVOKE ALL ON dcse_cp.escd_job_events FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_job_events TO authenticated;

REVOKE ALL ON dcse_cp.escd_approvals FROM authenticated;
GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_approvals TO authenticated;

REVOKE ALL ON dcse_cp.escd_evidence FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_evidence TO authenticated;

REVOKE ALL ON dcse_cp.escd_briefing_acks FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_briefing_acks TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_approval_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    allowed boolean := false;
BEGIN
    -- Material approval binding is immutable after creation. A changed action,
    -- payload/version fingerprint, scope/conditions, requester, or expiry needs
    -- a new approval record rather than mutation of an existing decision.
    IF NEW.job_id IS DISTINCT FROM OLD.job_id
       OR NEW.approval_type IS DISTINCT FROM OLD.approval_type
       OR NEW.action_key IS DISTINCT FROM OLD.action_key
       OR NEW.payload_fingerprint IS DISTINCT FROM OLD.payload_fingerprint
       OR NEW.title IS DISTINCT FROM OLD.title
       OR NEW.description IS DISTINCT FROM OLD.description
       OR NEW.conditions IS DISTINCT FROM OLD.conditions
       OR NEW.requested_by_user_id IS DISTINCT FROM OLD.requested_by_user_id
       OR NEW.requested_at IS DISTINCT FROM OLD.requested_at
       OR NEW.expires_at IS DISTINCT FROM OLD.expires_at THEN
        RAISE EXCEPTION 'approval_binding_immutable' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status = OLD.status THEN
        IF NEW.decided_by_user_id IS DISTINCT FROM OLD.decided_by_user_id
           OR NEW.decided_at IS DISTINCT FROM OLD.decided_at THEN
            RAISE EXCEPTION 'approval_decision_immutable_without_transition' USING ERRCODE = 'check_violation';
        END IF;
        RETURN NEW;
    END IF;

    allowed := CASE OLD.status
        WHEN 'proposed' THEN NEW.status IN ('pending','withdrawn')
        WHEN 'pending' THEN NEW.status IN ('approved','rejected','expired','withdrawn')
        WHEN 'approved' THEN NEW.status = 'revoked'
        ELSE false
    END;

    IF NOT allowed THEN
        RAISE EXCEPTION 'invalid_approval_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status IN ('approved','rejected') THEN
        IF NEW.decided_by_user_id IS DISTINCT FROM auth.uid() OR NEW.decided_at IS NULL THEN
            RAISE EXCEPTION 'authenticated_approval_decision_required' USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    IF OLD.status = 'pending' AND OLD.expires_at IS NOT NULL AND OLD.expires_at <= now()
       AND NEW.status IN ('approved','rejected') THEN
        RAISE EXCEPTION 'approval_expired' USING ERRCODE = 'check_violation';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_approval_update_guard ON dcse_cp.escd_approvals;
CREATE TRIGGER escd_approval_update_guard
BEFORE UPDATE ON dcse_cp.escd_approvals
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_approval_update();

REVOKE ALL ON FUNCTION dcse_cp.escd_validate_approval_update() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_approval_update() TO authenticated;

/* ROLLBACK, only after explicit DCS authorization:
DROP TRIGGER IF EXISTS escd_approval_update_guard ON dcse_cp.escd_approvals;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_approval_update();
-- Privilege rollback should restore the immediately preceding reviewed grant state,
-- not assume broad CRUD. Record that state before any authorized production apply.
*/
