-- ESCD integrated Executive Stream + Personal Assistant state candidate
-- Task: DCSE-ESCD-001-EXEC-PA-003
-- Status: CANDIDATE. Do not apply to production without release approval.

CREATE TABLE IF NOT EXISTS dcse_cp.escd_projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_key text NOT NULL UNIQUE,
    title text NOT NULL,
    objective text,
    status text NOT NULL DEFAULT 'active' CHECK (status IN ('planned','active','waiting','completed','cancelled','archived')),
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_items (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    item_key text NOT NULL UNIQUE,
    title text NOT NULL,
    summary text,
    status text NOT NULL DEFAULT 'captured' CHECK (status IN ('captured','triaged','planned','active','waiting','watch','approval','completed','cancelled','archived')),
    task_class text NOT NULL DEFAULT 'CAPTURE' CHECK (task_class IN ('CAPTURE','TRIAGE','PLAN','MAKE','FIX','DO','DECIDE','APPROVE','COMMUNICATE','RESEARCH','DCSE','ROUTINE','MONITOR','REVIEW','RELEASE','ARCHIVE')),
    context text NOT NULL DEFAULT 'general',
    project_id uuid REFERENCES dcse_cp.escd_projects(id) ON DELETE RESTRICT,
    dependency_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    approval_class text,
    actionable boolean NOT NULL DEFAULT false,
    blocked boolean NOT NULL DEFAULT false,
    external_dependency boolean NOT NULL DEFAULT false,
    future_trigger boolean NOT NULL DEFAULT false,
    missing_approval boolean NOT NULL DEFAULT false,
    explicit_hold boolean NOT NULL DEFAULT false,
    mission_priority numeric(5,2) NOT NULL DEFAULT 0 CHECK (mission_priority BETWEEN 0 AND 100),
    explicit_priority numeric(5,2) NOT NULL DEFAULT 0 CHECK (explicit_priority BETWEEN 0 AND 100),
    urgency numeric(5,2) NOT NULL DEFAULT 0 CHECK (urgency BETWEEN 0 AND 100),
    revenue_relevance numeric(5,2) NOT NULL DEFAULT 0 CHECK (revenue_relevance BETWEEN 0 AND 100),
    unblock_value numeric(5,2) NOT NULL DEFAULT 0 CHECK (unblock_value BETWEEN 0 AND 100),
    consequence numeric(5,2) NOT NULL DEFAULT 0 CHECK (consequence BETWEEN 0 AND 100),
    aging numeric(5,2) NOT NULL DEFAULT 0 CHECK (aging BETWEEN 0 AND 100),
    effort_efficiency numeric(5,2) NOT NULL DEFAULT 0 CHECK (effort_efficiency BETWEEN 0 AND 100),
    strategic_leverage numeric(5,2) NOT NULL DEFAULT 0 CHECK (strategic_leverage BETWEEN 0 AND 100),
    dcs_override numeric(5,2) NOT NULL DEFAULT 0 CHECK (dcs_override BETWEEN 0 AND 100),
    due_at timestamptz,
    source_system text NOT NULL,
    source_id text NOT NULL,
    normalized_intent text NOT NULL,
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz
);

CREATE INDEX IF NOT EXISTS escd_items_status_idx ON dcse_cp.escd_items(status);
CREATE INDEX IF NOT EXISTS escd_items_due_idx ON dcse_cp.escd_items(due_at) WHERE due_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS escd_items_project_idx ON dcse_cp.escd_items(project_id) WHERE project_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS escd_items_source_idx ON dcse_cp.escd_items(source_system, source_id);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_item_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id uuid NOT NULL REFERENCES dcse_cp.escd_items(id) ON DELETE RESTRICT,
    event_type text NOT NULL,
    summary text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS escd_item_events_item_idx ON dcse_cp.escd_item_events(item_id, created_at DESC, id DESC);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_decisions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_key text NOT NULL UNIQUE,
    item_id uuid REFERENCES dcse_cp.escd_items(id) ON DELETE RESTRICT,
    question text NOT NULL,
    facts jsonb NOT NULL DEFAULT '[]'::jsonb,
    unknowns jsonb NOT NULL DEFAULT '[]'::jsonb,
    alternatives jsonb NOT NULL DEFAULT '[]'::jsonb,
    tradeoffs jsonb NOT NULL DEFAULT '[]'::jsonb,
    recommendation text,
    decision text,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    execution_evidence_ref text,
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_contact_contexts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    context_key text NOT NULL UNIQUE,
    contact_ref text NOT NULL,
    display_name text,
    organization text,
    role text,
    relationship_context text,
    active_commitments jsonb NOT NULL DEFAULT '[]'::jsonb,
    waiting_on_them jsonb NOT NULL DEFAULT '[]'::jsonb,
    they_are_waiting_on_dcs jsonb NOT NULL DEFAULT '[]'::jsonb,
    recent_interaction_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    next_follow_up_at timestamptz,
    communication_preferences jsonb NOT NULL DEFAULT '{}'::jsonb,
    important_dates jsonb NOT NULL DEFAULT '[]'::jsonb,
    notes text,
    provenance_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    confidence_status text NOT NULL DEFAULT 'unknown' CHECK (confidence_status IN ('verified','likely','unknown')),
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_routines (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    routine_key text NOT NULL,
    version integer NOT NULL DEFAULT 1 CHECK (version > 0),
    mission text NOT NULL,
    purpose text NOT NULL,
    trigger_type text NOT NULL CHECK (trigger_type IN ('time','event','condition')),
    trigger_spec jsonb NOT NULL DEFAULT '{}'::jsonb,
    autonomy_class text NOT NULL CHECK (autonomy_class IN ('A0_AUTO','A1_AUTO_LOG','A2_PROPOSE','A3_APPROVAL_REQUIRED','A4_PROHIBITED')),
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    action_template jsonb NOT NULL DEFAULT '{}'::jsonb,
    approval_required boolean NOT NULL DEFAULT false,
    expected_evidence jsonb NOT NULL DEFAULT '[]'::jsonb,
    failure_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
    escalation_class text NOT NULL DEFAULT 'N1' CHECK (escalation_class IN ('N0','N1','N2','N3','N4')),
    last_run_at timestamptz,
    next_run_at timestamptz,
    paused boolean NOT NULL DEFAULT false,
    cancelled boolean NOT NULL DEFAULT false,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (routine_key, version)
);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_notification_intents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    notification_key text NOT NULL UNIQUE,
    notification_class text NOT NULL CHECK (notification_class IN ('N0','N1','N2','N3','N4')),
    source_event_ref text NOT NULL,
    item_id uuid REFERENCES dcse_cp.escd_items(id) ON DELETE RESTRICT,
    reason text NOT NULL,
    channel text NOT NULL DEFAULT 'in_app',
    state text NOT NULL DEFAULT 'created' CHECK (state = 'created'),
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE dcse_cp.escd_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_projects FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_items FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_item_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_item_events FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_decisions FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_contact_contexts ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_contact_contexts FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_routines ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_routines FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_notification_intents ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_notification_intents FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_projects_dcs_owner ON dcse_cp.escd_projects;
CREATE POLICY escd_projects_dcs_owner ON dcse_cp.escd_projects FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());
DROP POLICY IF EXISTS escd_items_dcs_owner ON dcse_cp.escd_items;
CREATE POLICY escd_items_dcs_owner ON dcse_cp.escd_items FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());
DROP POLICY IF EXISTS escd_item_events_dcs_owner ON dcse_cp.escd_item_events;
CREATE POLICY escd_item_events_dcs_owner ON dcse_cp.escd_item_events FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND actor_user_id = auth.uid());
DROP POLICY IF EXISTS escd_decisions_dcs_owner ON dcse_cp.escd_decisions;
CREATE POLICY escd_decisions_dcs_owner ON dcse_cp.escd_decisions FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND actor_user_id = auth.uid());
DROP POLICY IF EXISTS escd_contact_contexts_dcs_owner ON dcse_cp.escd_contact_contexts;
CREATE POLICY escd_contact_contexts_dcs_owner ON dcse_cp.escd_contact_contexts FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND actor_user_id = auth.uid());
DROP POLICY IF EXISTS escd_routines_dcs_owner ON dcse_cp.escd_routines;
CREATE POLICY escd_routines_dcs_owner ON dcse_cp.escd_routines FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());
DROP POLICY IF EXISTS escd_notification_intents_dcs_owner ON dcse_cp.escd_notification_intents;
CREATE POLICY escd_notification_intents_dcs_owner ON dcse_cp.escd_notification_intents FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND actor_user_id = auth.uid());

REVOKE ALL ON dcse_cp.escd_projects, dcse_cp.escd_items, dcse_cp.escd_item_events, dcse_cp.escd_decisions, dcse_cp.escd_contact_contexts, dcse_cp.escd_routines, dcse_cp.escd_notification_intents FROM authenticated;
GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_projects, dcse_cp.escd_items, dcse_cp.escd_routines TO authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_item_events, dcse_cp.escd_decisions, dcse_cp.escd_contact_contexts, dcse_cp.escd_notification_intents TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_item_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE allowed boolean := false;
BEGIN
    IF NEW.status = OLD.status THEN
        NEW.updated_at := now();
        RETURN NEW;
    END IF;

    allowed := CASE OLD.status
        WHEN 'captured' THEN NEW.status IN ('triaged','cancelled')
        WHEN 'triaged' THEN NEW.status IN ('planned','waiting','watch','approval','cancelled')
        WHEN 'planned' THEN NEW.status IN ('active','waiting','watch','approval','cancelled')
        WHEN 'active' THEN NEW.status IN ('waiting','watch','approval','completed','cancelled')
        WHEN 'waiting' THEN NEW.status IN ('planned','active','watch','approval','cancelled')
        WHEN 'watch' THEN NEW.status IN ('planned','active','waiting','approval','cancelled')
        WHEN 'approval' THEN NEW.status IN ('planned','active','waiting','cancelled')
        WHEN 'completed' THEN NEW.status = 'archived'
        WHEN 'cancelled' THEN NEW.status = 'archived'
        ELSE false
    END;

    IF NOT allowed THEN
        RAISE EXCEPTION 'invalid_item_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status = 'completed' THEN
        NEW.completed_at := COALESCE(NEW.completed_at, now());
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_item_transition_guard ON dcse_cp.escd_items;
CREATE TRIGGER escd_item_transition_guard BEFORE UPDATE OF status ON dcse_cp.escd_items FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_item_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_item_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_item_transition() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_record_item_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO dcse_cp.escd_item_events (item_id, event_type, summary, metadata, actor_user_id)
        VALUES (
            NEW.id,
            'status_transition',
            format('Item status changed from %s to %s', OLD.status, NEW.status),
            jsonb_build_object('from_status', OLD.status, 'to_status', NEW.status),
            auth.uid()
        );
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_item_transition_event ON dcse_cp.escd_items;
CREATE TRIGGER escd_item_transition_event AFTER UPDATE OF status ON dcse_cp.escd_items FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_record_item_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_record_item_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_record_item_transition() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_routine_update()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    IF NEW.routine_key IS DISTINCT FROM OLD.routine_key
       OR NEW.version IS DISTINCT FROM OLD.version
       OR NEW.mission IS DISTINCT FROM OLD.mission
       OR NEW.purpose IS DISTINCT FROM OLD.purpose
       OR NEW.trigger_type IS DISTINCT FROM OLD.trigger_type
       OR NEW.trigger_spec IS DISTINCT FROM OLD.trigger_spec
       OR NEW.autonomy_class IS DISTINCT FROM OLD.autonomy_class
       OR NEW.source_refs IS DISTINCT FROM OLD.source_refs
       OR NEW.action_template IS DISTINCT FROM OLD.action_template
       OR NEW.approval_required IS DISTINCT FROM OLD.approval_required
       OR NEW.expected_evidence IS DISTINCT FROM OLD.expected_evidence
       OR NEW.failure_policy IS DISTINCT FROM OLD.failure_policy
       OR NEW.escalation_class IS DISTINCT FROM OLD.escalation_class
       OR NEW.created_by_user_id IS DISTINCT FROM OLD.created_by_user_id
       OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
        RAISE EXCEPTION 'routine_configuration_immutable_create_new_version' USING ERRCODE = 'check_violation';
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_routine_update_guard ON dcse_cp.escd_routines;
CREATE TRIGGER escd_routine_update_guard BEFORE UPDATE ON dcse_cp.escd_routines FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_routine_update();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_routine_update() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_routine_update() TO authenticated;

/* ROLLBACK, only after explicit DCS authorization and only after dependent data review:
DROP TRIGGER IF EXISTS escd_routine_update_guard ON dcse_cp.escd_routines;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_routine_update();
DROP TRIGGER IF EXISTS escd_item_transition_event ON dcse_cp.escd_items;
DROP FUNCTION IF EXISTS dcse_cp.escd_record_item_transition();
DROP TRIGGER IF EXISTS escd_item_transition_guard ON dcse_cp.escd_items;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_item_transition();
DROP TABLE IF EXISTS dcse_cp.escd_notification_intents;
DROP TABLE IF EXISTS dcse_cp.escd_routines;
DROP TABLE IF EXISTS dcse_cp.escd_contact_contexts;
DROP TABLE IF EXISTS dcse_cp.escd_decisions;
DROP TABLE IF EXISTS dcse_cp.escd_item_events;
DROP TABLE IF EXISTS dcse_cp.escd_items;
DROP TABLE IF EXISTS dcse_cp.escd_projects;
*/
