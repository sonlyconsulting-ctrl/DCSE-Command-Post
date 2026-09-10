-- ESCD workflow execution authority patch candidate
-- Task: DCSE-ESCD-001-WORKFLOW-004
-- Status: CANDIDATE. Requires 20260910_escd_workflow_engine.sql first.
-- Do not apply to production without release approval.

ALTER TABLE dcse_cp.escd_workflow_instances
    ADD COLUMN IF NOT EXISTS job_id uuid REFERENCES dcse_cp.escd_jobs(id) ON DELETE RESTRICT;
CREATE INDEX IF NOT EXISTS escd_workflow_instances_job_idx
    ON dcse_cp.escd_workflow_instances(job_id) WHERE job_id IS NOT NULL;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_workflow_instance_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    allowed boolean := false;
BEGIN
    IF NEW.instance_key IS DISTINCT FROM OLD.instance_key
       OR NEW.template_id IS DISTINCT FROM OLD.template_id
       OR NEW.template_version IS DISTINCT FROM OLD.template_version
       OR NEW.template_fingerprint IS DISTINCT FROM OLD.template_fingerprint
       OR NEW.template_type IS DISTINCT FROM OLD.template_type
       OR NEW.job_id IS DISTINCT FROM OLD.job_id
       OR NEW.context_type IS DISTINCT FROM OLD.context_type
       OR NEW.context_ref IS DISTINCT FROM OLD.context_ref
       OR NEW.bindings IS DISTINCT FROM OLD.bindings
       OR NEW.effective_controls IS DISTINCT FROM OLD.effective_controls
       OR NEW.created_by_user_id IS DISTINCT FROM OLD.created_by_user_id
       OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
        RAISE EXCEPTION 'workflow_instance_binding_immutable' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.execution_authorized AND NOT OLD.execution_authorized THEN
        RAISE EXCEPTION 'workflow_execution_authority_cannot_self_escalate' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status IS DISTINCT FROM OLD.status THEN
        allowed := CASE OLD.status
            WHEN 'planned' THEN NEW.status IN ('running','waiting_approval','waiting','cancelled')
            WHEN 'running' THEN NEW.status IN ('waiting_approval','waiting','failed','completed','cancelled')
            WHEN 'waiting_approval' THEN NEW.status IN ('running','waiting','cancelled')
            WHEN 'waiting' THEN NEW.status IN ('running','waiting_approval','failed','cancelled')
            WHEN 'failed' THEN NEW.status IN ('running','archived')
            WHEN 'completed' THEN NEW.status = 'archived'
            WHEN 'cancelled' THEN NEW.status = 'archived'
            ELSE false
        END;
        IF NOT allowed THEN
            RAISE EXCEPTION 'invalid_workflow_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    IF NEW.status = 'running' THEN
        IF NOT NEW.execution_authorized THEN
            RAISE EXCEPTION 'workflow_execution_not_authorized' USING ERRCODE = 'check_violation';
        END IF;
        IF NEW.job_id IS NULL THEN
            RAISE EXCEPTION 'workflow_governed_job_required' USING ERRCODE = 'check_violation';
        END IF;
        IF NOT EXISTS (
            SELECT 1 FROM dcse_cp.escd_jobs j
            WHERE j.id = NEW.job_id
              AND j.status IN ('queued','running','waiting_approval')
        ) THEN
            RAISE EXCEPTION 'workflow_governed_job_not_active' USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    IF NEW.status = 'completed' THEN
        IF EXISTS (
            SELECT 1 FROM dcse_cp.escd_workflow_steps s
            WHERE s.instance_id = OLD.id
              AND s.status NOT IN ('completed','skipped','cancelled')
        ) THEN
            RAISE EXCEPTION 'workflow_steps_incomplete' USING ERRCODE = 'check_violation';
        END IF;
        IF COALESCE((NEW.effective_controls ->> 'evidence_required')::boolean, false)
           AND jsonb_array_length(COALESCE(NEW.evidence_refs, '[]'::jsonb)) = 0 THEN
            RAISE EXCEPTION 'workflow_evidence_required' USING ERRCODE = 'check_violation';
        END IF;
        NEW.completed_at := COALESCE(NEW.completed_at, now());
    END IF;

    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_workflow_step_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    allowed boolean := false;
    workflow_job_id uuid;
    approval_status text;
    approval_expires_at timestamptz;
    approval_action_key text;
    approval_job_id uuid;
BEGIN
    IF NEW.instance_id IS DISTINCT FROM OLD.instance_id
       OR NEW.step_id IS DISTINCT FROM OLD.step_id
       OR NEW.sequence_no IS DISTINCT FROM OLD.sequence_no
       OR NEW.dependencies IS DISTINCT FROM OLD.dependencies
       OR NEW.action_type IS DISTINCT FROM OLD.action_type
       OR NEW.instruction IS DISTINCT FROM OLD.instruction
       OR NEW.input_refs IS DISTINCT FROM OLD.input_refs
       OR NEW.output_contract IS DISTINCT FROM OLD.output_contract
       OR NEW.executor IS DISTINCT FROM OLD.executor
       OR NEW.autonomy_class IS DISTINCT FROM OLD.autonomy_class
       OR NEW.approval_required IS DISTINCT FROM OLD.approval_required
       OR NEW.verification_method IS DISTINCT FROM OLD.verification_method
       OR NEW.evidence_required IS DISTINCT FROM OLD.evidence_required
       OR NEW.failure_route IS DISTINCT FROM OLD.failure_route
       OR NEW.next_step_on_success IS DISTINCT FROM OLD.next_step_on_success
       OR NEW.next_step_on_failure IS DISTINCT FROM OLD.next_step_on_failure
       OR NEW.created_by_user_id IS DISTINCT FROM OLD.created_by_user_id
       OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
        RAISE EXCEPTION 'workflow_step_contract_immutable' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status IS DISTINCT FROM OLD.status THEN
        allowed := CASE OLD.status
            WHEN 'pending' THEN NEW.status IN ('ready','waiting_approval','waiting','cancelled')
            WHEN 'ready' THEN NEW.status IN ('running','waiting_approval','cancelled')
            WHEN 'running' THEN NEW.status IN ('waiting_approval','waiting','completed','failed','cancelled')
            WHEN 'waiting_approval' THEN NEW.status IN ('ready','running','waiting','cancelled')
            WHEN 'waiting' THEN NEW.status IN ('ready','running','failed','cancelled')
            WHEN 'failed' THEN NEW.status IN ('ready','cancelled')
            ELSE false
        END;
        IF NOT allowed THEN
            RAISE EXCEPTION 'invalid_workflow_step_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
        END IF;
    END IF;

    IF NEW.status = 'running' THEN
        SELECT i.job_id INTO workflow_job_id
        FROM dcse_cp.escd_workflow_instances i
        WHERE i.id = NEW.instance_id;

        IF workflow_job_id IS NULL THEN
            RAISE EXCEPTION 'workflow_governed_job_required' USING ERRCODE = 'check_violation';
        END IF;

        IF NEW.autonomy_class = 'A4_PROHIBITED' THEN
            RAISE EXCEPTION 'workflow_step_prohibited' USING ERRCODE = 'check_violation';
        END IF;

        IF NEW.approval_required OR NEW.autonomy_class = 'A3_APPROVAL_REQUIRED' THEN
            IF NEW.approval_id IS NULL THEN
                RAISE EXCEPTION 'workflow_step_approval_required' USING ERRCODE = 'check_violation';
            END IF;

            SELECT a.status, a.expires_at, a.action_key, a.job_id
              INTO approval_status, approval_expires_at, approval_action_key, approval_job_id
              FROM dcse_cp.escd_approvals a
             WHERE a.id = NEW.approval_id;

            IF approval_status IS NULL
               OR approval_status <> 'approved'
               OR (approval_expires_at IS NOT NULL AND approval_expires_at <= now())
               OR approval_job_id IS DISTINCT FROM workflow_job_id
               OR approval_action_key IS DISTINCT FROM format('workflow_step:%s', NEW.step_id) THEN
                RAISE EXCEPTION 'workflow_step_approval_not_effective' USING ERRCODE = 'check_violation';
            END IF;
        END IF;
    END IF;

    IF NEW.status = 'completed' AND NEW.evidence_required
       AND jsonb_array_length(COALESCE(NEW.evidence_refs, '[]'::jsonb)) = 0 THEN
        RAISE EXCEPTION 'workflow_step_evidence_required' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.attempt_count < OLD.attempt_count THEN
        RAISE EXCEPTION 'workflow_attempt_count_regression' USING ERRCODE = 'check_violation';
    END IF;

    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

/* ROLLBACK, only after explicit DCS authorization:
DROP INDEX IF EXISTS dcse_cp.escd_workflow_instances_job_idx;
ALTER TABLE dcse_cp.escd_workflow_instances DROP COLUMN IF EXISTS job_id;
-- Restore the immediately preceding reviewed function definitions from
-- 20260910_escd_workflow_engine.sql only as part of an authorized rollback.
*/
