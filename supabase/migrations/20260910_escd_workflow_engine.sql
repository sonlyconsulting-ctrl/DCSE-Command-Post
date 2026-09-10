-- ESCD reusable workflow engine candidate
-- Task: DCSE-ESCD-001-WORKFLOW-004
-- Status: CANDIDATE. Do not apply to production without release approval.

CREATE TABLE IF NOT EXISTS dcse_cp.escd_workflow_templates (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id text NOT NULL,
    version text NOT NULL,
    name text NOT NULL,
    status text NOT NULL CHECK (status IN ('draft','candidate','approved','superseded','archived')),
    template_type text NOT NULL CHECK (template_type IN ('MAKE','FIX','REVIEW','RELEASE','MONITOR','ROUTINE','RESEARCH','COMMUNICATE','DECIDE','DO')),
    purpose text NOT NULL,
    scope text NOT NULL,
    supported_context_types jsonb NOT NULL DEFAULT '[]'::jsonb,
    definition jsonb NOT NULL,
    parent_template_id text,
    parent_template_version text,
    effective_controls jsonb NOT NULL DEFAULT '{}'::jsonb,
    definition_fingerprint text NOT NULL,
    provenance jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (template_id, version),
    UNIQUE (definition_fingerprint)
);

CREATE INDEX IF NOT EXISTS escd_workflow_templates_type_idx
    ON dcse_cp.escd_workflow_templates(template_type, status, template_id, version);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_workflow_instances (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_key text NOT NULL UNIQUE,
    template_id text NOT NULL,
    template_version text NOT NULL,
    template_fingerprint text NOT NULL,
    template_type text NOT NULL CHECK (template_type IN ('MAKE','FIX','REVIEW','RELEASE','MONITOR','ROUTINE','RESEARCH','COMMUNICATE','DECIDE','DO')),
    context_type text NOT NULL CHECK (context_type IN ('product','project','asset','system','document','person','event','general')),
    context_ref text NOT NULL,
    bindings jsonb NOT NULL DEFAULT '{}'::jsonb,
    status text NOT NULL DEFAULT 'planned' CHECK (status IN ('planned','running','waiting_approval','waiting','failed','completed','cancelled','archived')),
    current_step_id text,
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    effective_controls jsonb NOT NULL DEFAULT '{}'::jsonb,
    execution_authorized boolean NOT NULL DEFAULT false,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    FOREIGN KEY (template_id, template_version)
        REFERENCES dcse_cp.escd_workflow_templates(template_id, version) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS escd_workflow_instances_status_idx
    ON dcse_cp.escd_workflow_instances(status, updated_at DESC, id ASC);
CREATE INDEX IF NOT EXISTS escd_workflow_instances_context_idx
    ON dcse_cp.escd_workflow_instances(context_type, context_ref);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_workflow_steps (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_id uuid NOT NULL REFERENCES dcse_cp.escd_workflow_instances(id) ON DELETE RESTRICT,
    step_id text NOT NULL,
    sequence_no integer NOT NULL CHECK (sequence_no > 0),
    dependencies jsonb NOT NULL DEFAULT '[]'::jsonb,
    action_type text NOT NULL,
    instruction text NOT NULL,
    input_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    output_contract jsonb NOT NULL DEFAULT '{}'::jsonb,
    executor text NOT NULL,
    autonomy_class text NOT NULL CHECK (autonomy_class IN ('A0_AUTO','A1_AUTO_LOG','A2_PROPOSE','A3_APPROVAL_REQUIRED','A4_PROHIBITED')),
    approval_required boolean NOT NULL DEFAULT false,
    verification_method text NOT NULL,
    evidence_required boolean NOT NULL DEFAULT false,
    failure_route text NOT NULL,
    next_step_on_success text,
    next_step_on_failure text,
    status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','ready','running','waiting_approval','waiting','completed','failed','skipped','cancelled')),
    approval_id uuid REFERENCES dcse_cp.escd_approvals(id) ON DELETE RESTRICT,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (instance_id, step_id),
    UNIQUE (instance_id, sequence_no)
);

CREATE INDEX IF NOT EXISTS escd_workflow_steps_instance_idx
    ON dcse_cp.escd_workflow_steps(instance_id, sequence_no, step_id);
CREATE INDEX IF NOT EXISTS escd_workflow_steps_status_idx
    ON dcse_cp.escd_workflow_steps(status, instance_id, sequence_no);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_workflow_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_id uuid NOT NULL REFERENCES dcse_cp.escd_workflow_instances(id) ON DELETE RESTRICT,
    step_id text,
    event_type text NOT NULL,
    summary text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    evidence_ref text,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS escd_workflow_events_instance_idx
    ON dcse_cp.escd_workflow_events(instance_id, created_at DESC, id DESC);

ALTER TABLE dcse_cp.escd_workflow_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_templates FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_instances ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_instances FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_steps FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_workflow_events FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_workflow_templates_dcs_owner ON dcse_cp.escd_workflow_templates;
CREATE POLICY escd_workflow_templates_dcs_owner ON dcse_cp.escd_workflow_templates
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

DROP POLICY IF EXISTS escd_workflow_instances_dcs_owner ON dcse_cp.escd_workflow_instances;
CREATE POLICY escd_workflow_instances_dcs_owner ON dcse_cp.escd_workflow_instances
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

DROP POLICY IF EXISTS escd_workflow_steps_dcs_owner ON dcse_cp.escd_workflow_steps;
CREATE POLICY escd_workflow_steps_dcs_owner ON dcse_cp.escd_workflow_steps
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

DROP POLICY IF EXISTS escd_workflow_events_dcs_owner ON dcse_cp.escd_workflow_events;
CREATE POLICY escd_workflow_events_dcs_owner ON dcse_cp.escd_workflow_events
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND actor_user_id = auth.uid());

REVOKE ALL ON dcse_cp.escd_workflow_templates, dcse_cp.escd_workflow_instances, dcse_cp.escd_workflow_steps, dcse_cp.escd_workflow_events FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_workflow_templates TO authenticated;
GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_workflow_instances, dcse_cp.escd_workflow_steps TO authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_workflow_events TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_workflow_template_insert()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    parent_controls jsonb;
    control_name text;
BEGIN
    IF jsonb_array_length(COALESCE(NEW.provenance, '[]'::jsonb)) = 0 THEN
        RAISE EXCEPTION 'workflow_template_provenance_required' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.parent_template_id IS NOT NULL OR NEW.parent_template_version IS NOT NULL THEN
        IF NEW.parent_template_id IS NULL OR NEW.parent_template_version IS NULL THEN
            RAISE EXCEPTION 'workflow_parent_identity_incomplete' USING ERRCODE = 'check_violation';
        END IF;

        SELECT effective_controls INTO parent_controls
        FROM dcse_cp.escd_workflow_templates
        WHERE template_id = NEW.parent_template_id
          AND version = NEW.parent_template_version;

        IF parent_controls IS NULL THEN
            RAISE EXCEPTION 'workflow_parent_not_found' USING ERRCODE = 'foreign_key_violation';
        END IF;

        FOREACH control_name IN ARRAY ARRAY['approval_required','evidence_required','security_required','rollback_required'] LOOP
            IF COALESCE((parent_controls ->> control_name)::boolean, false)
               AND NOT COALESCE((NEW.effective_controls ->> control_name)::boolean, false) THEN
                RAISE EXCEPTION 'workflow_child_control_weakened:%', control_name USING ERRCODE = 'check_violation';
            END IF;
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_workflow_template_insert_guard ON dcse_cp.escd_workflow_templates;
CREATE TRIGGER escd_workflow_template_insert_guard
BEFORE INSERT ON dcse_cp.escd_workflow_templates
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_workflow_template_insert();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_workflow_template_insert() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_workflow_template_insert() TO authenticated;

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

DROP TRIGGER IF EXISTS escd_workflow_instance_update_guard ON dcse_cp.escd_workflow_instances;
CREATE TRIGGER escd_workflow_instance_update_guard
BEFORE UPDATE ON dcse_cp.escd_workflow_instances
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_workflow_instance_update();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_workflow_instance_update() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_workflow_instance_update() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_workflow_step_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    allowed boolean := false;
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

DROP TRIGGER IF EXISTS escd_workflow_step_update_guard ON dcse_cp.escd_workflow_steps;
CREATE TRIGGER escd_workflow_step_update_guard
BEFORE UPDATE ON dcse_cp.escd_workflow_steps
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_workflow_step_update();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_workflow_step_update() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_workflow_step_update() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_record_workflow_instance_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO dcse_cp.escd_workflow_events (instance_id, event_type, summary, metadata, actor_user_id)
        VALUES (
            NEW.id,
            'workflow_status_transition',
            format('Workflow changed from %s to %s', OLD.status, NEW.status),
            jsonb_build_object('from_status', OLD.status, 'to_status', NEW.status),
            auth.uid()
        );
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_workflow_instance_transition_event ON dcse_cp.escd_workflow_instances;
CREATE TRIGGER escd_workflow_instance_transition_event
AFTER UPDATE OF status ON dcse_cp.escd_workflow_instances
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_record_workflow_instance_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_record_workflow_instance_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_record_workflow_instance_transition() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_record_workflow_step_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO dcse_cp.escd_workflow_events (instance_id, step_id, event_type, summary, metadata, actor_user_id)
        VALUES (
            NEW.instance_id,
            NEW.step_id,
            'workflow_step_transition',
            format('Workflow step %s changed from %s to %s', NEW.step_id, OLD.status, NEW.status),
            jsonb_build_object('from_status', OLD.status, 'to_status', NEW.status, 'attempt_count', NEW.attempt_count),
            auth.uid()
        );
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_workflow_step_transition_event ON dcse_cp.escd_workflow_steps;
CREATE TRIGGER escd_workflow_step_transition_event
AFTER UPDATE OF status ON dcse_cp.escd_workflow_steps
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_record_workflow_step_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_record_workflow_step_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_record_workflow_step_transition() TO authenticated;

/* ROLLBACK, only after explicit DCS authorization:
DROP TRIGGER IF EXISTS escd_workflow_step_transition_event ON dcse_cp.escd_workflow_steps;
DROP FUNCTION IF EXISTS dcse_cp.escd_record_workflow_step_transition();
DROP TRIGGER IF EXISTS escd_workflow_instance_transition_event ON dcse_cp.escd_workflow_instances;
DROP FUNCTION IF EXISTS dcse_cp.escd_record_workflow_instance_transition();
DROP TRIGGER IF EXISTS escd_workflow_step_update_guard ON dcse_cp.escd_workflow_steps;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_workflow_step_update();
DROP TRIGGER IF EXISTS escd_workflow_instance_update_guard ON dcse_cp.escd_workflow_instances;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_workflow_instance_update();
DROP TRIGGER IF EXISTS escd_workflow_template_insert_guard ON dcse_cp.escd_workflow_templates;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_workflow_template_insert();
DROP TABLE IF EXISTS dcse_cp.escd_workflow_events;
DROP TABLE IF EXISTS dcse_cp.escd_workflow_steps;
DROP TABLE IF EXISTS dcse_cp.escd_workflow_instances;
DROP TABLE IF EXISTS dcse_cp.escd_workflow_templates;
*/
