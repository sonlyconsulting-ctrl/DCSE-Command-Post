-- ESCD minimal MVP Task/Idea persistence candidate
-- Task: DCSE-ESCD-001-MVP-006
-- Additive subset of the reviewed ESCD Executive/PA state model.
-- CANDIDATE ONLY. Do not apply to production without explicit DCS authorization.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
GRANT USAGE ON SCHEMA dcse_cp TO authenticated;

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

ALTER TABLE dcse_cp.escd_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_projects FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_items FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_projects_dcs_owner ON dcse_cp.escd_projects;
CREATE POLICY escd_projects_dcs_owner ON dcse_cp.escd_projects FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

DROP POLICY IF EXISTS escd_items_dcs_owner ON dcse_cp.escd_items;
CREATE POLICY escd_items_dcs_owner ON dcse_cp.escd_items FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

REVOKE ALL ON dcse_cp.escd_projects, dcse_cp.escd_items FROM authenticated;
GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_projects, dcse_cp.escd_items TO authenticated;

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
        WHEN 'triaged' THEN NEW.status IN ('planned','active','waiting','watch','approval','cancelled')
        WHEN 'planned' THEN NEW.status IN ('active','waiting','watch','approval','cancelled')
        WHEN 'active' THEN NEW.status IN ('waiting','watch','approval','completed','cancelled')
        WHEN 'waiting' THEN NEW.status IN ('active','watch','approval','cancelled')
        WHEN 'watch' THEN NEW.status IN ('active','waiting','approval','cancelled')
        WHEN 'approval' THEN NEW.status IN ('active','waiting','cancelled')
        WHEN 'completed' THEN NEW.status = 'archived'
        WHEN 'cancelled' THEN NEW.status = 'archived'
        ELSE false
    END;
    IF NOT allowed THEN
        RAISE EXCEPTION 'invalid_item_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
    END IF;
    IF NEW.status = 'completed' THEN NEW.completed_at := COALESCE(NEW.completed_at, now()); END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_item_transition_guard ON dcse_cp.escd_items;
CREATE TRIGGER escd_item_transition_guard BEFORE UPDATE OF status ON dcse_cp.escd_items
FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_item_transition();

REVOKE ALL ON FUNCTION dcse_cp.escd_validate_item_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_item_transition() TO authenticated;

-- Rollback, only with explicit authorization:
-- DROP TABLE IF EXISTS dcse_cp.escd_items;
-- DROP TABLE IF EXISTS dcse_cp.escd_projects;
