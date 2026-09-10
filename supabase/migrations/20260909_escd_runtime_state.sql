-- ESCD runtime state migration candidate
-- Task: DCSE-ESCD-001-RUNTIME-001
-- Status: CANDIDATE. Do not apply to production without release approval.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
GRANT USAGE ON SCHEMA dcse_cp TO authenticated;

CREATE TABLE IF NOT EXISTS dcse_cp.escd_jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_key text NOT NULL UNIQUE,
    request_id text UNIQUE,
    title text NOT NULL,
    purpose text,
    status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','running','waiting_approval','completed','failed','cancelled','archived')),
    requires_approval boolean NOT NULL DEFAULT false,
    exit_criteria_met boolean NOT NULL DEFAULT false,
    actionable boolean NOT NULL DEFAULT true,
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
    deadline timestamptz,
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    failure_detail text,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz
);

CREATE INDEX IF NOT EXISTS escd_jobs_status_idx ON dcse_cp.escd_jobs(status);
CREATE INDEX IF NOT EXISTS escd_jobs_updated_idx ON dcse_cp.escd_jobs(updated_at DESC);
CREATE INDEX IF NOT EXISTS escd_jobs_deadline_idx ON dcse_cp.escd_jobs(deadline) WHERE deadline IS NOT NULL;

CREATE TABLE IF NOT EXISTS dcse_cp.escd_job_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id uuid NOT NULL REFERENCES dcse_cp.escd_jobs(id) ON DELETE RESTRICT,
    event_type text NOT NULL,
    summary text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS escd_job_events_job_idx ON dcse_cp.escd_job_events(job_id, created_at DESC);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_approvals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id uuid NOT NULL REFERENCES dcse_cp.escd_jobs(id) ON DELETE RESTRICT,
    approval_type text NOT NULL,
    title text NOT NULL,
    description text,
    status text NOT NULL DEFAULT 'pending' CHECK (status IN ('proposed','pending','approved','rejected','expired','withdrawn','revoked')),
    requested_by_user_id uuid DEFAULT auth.uid(),
    requested_at timestamptz NOT NULL DEFAULT now(),
    decided_by_user_id uuid,
    decided_at timestamptz,
    decision_notes text
);
CREATE INDEX IF NOT EXISTS escd_approvals_job_idx ON dcse_cp.escd_approvals(job_id, requested_at DESC);
CREATE INDEX IF NOT EXISTS escd_approvals_pending_idx ON dcse_cp.escd_approvals(status) WHERE status = 'pending';

CREATE TABLE IF NOT EXISTS dcse_cp.escd_evidence (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_key text UNIQUE,
    job_id uuid REFERENCES dcse_cp.escd_jobs(id) ON DELETE RESTRICT,
    evidence_type text NOT NULL,
    title text NOT NULL,
    content text,
    reference_url text,
    reference_sha text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    actor_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS escd_evidence_job_idx ON dcse_cp.escd_evidence(job_id, created_at DESC);

CREATE TABLE IF NOT EXISTS dcse_cp.escd_briefing_acks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    principal_user_id uuid NOT NULL DEFAULT auth.uid(),
    acknowledged_through timestamptz NOT NULL,
    acknowledged_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (principal_user_id, acknowledged_through)
);
CREATE INDEX IF NOT EXISTS escd_briefing_acks_user_idx ON dcse_cp.escd_briefing_acks(principal_user_id, acknowledged_at DESC);

ALTER TABLE dcse_cp.escd_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_jobs FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_job_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_job_events FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_approvals FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_evidence FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_briefing_acks ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_briefing_acks FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_jobs_dcs_owner ON dcse_cp.escd_jobs;
CREATE POLICY escd_jobs_dcs_owner ON dcse_cp.escd_jobs FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());
DROP POLICY IF EXISTS escd_job_events_dcs_owner ON dcse_cp.escd_job_events;
CREATE POLICY escd_job_events_dcs_owner ON dcse_cp.escd_job_events FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());
DROP POLICY IF EXISTS escd_approvals_dcs_owner ON dcse_cp.escd_approvals;
CREATE POLICY escd_approvals_dcs_owner ON dcse_cp.escd_approvals FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());
DROP POLICY IF EXISTS escd_evidence_dcs_owner ON dcse_cp.escd_evidence;
CREATE POLICY escd_evidence_dcs_owner ON dcse_cp.escd_evidence FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());
DROP POLICY IF EXISTS escd_briefing_acks_dcs_owner ON dcse_cp.escd_briefing_acks;
CREATE POLICY escd_briefing_acks_dcs_owner ON dcse_cp.escd_briefing_acks FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner() AND principal_user_id = auth.uid());

GRANT SELECT, INSERT, UPDATE, DELETE ON dcse_cp.escd_jobs, dcse_cp.escd_job_events, dcse_cp.escd_approvals, dcse_cp.escd_evidence, dcse_cp.escd_briefing_acks TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_job_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    allowed boolean := false;
    latest_approval_status text;
    evidence_count integer := 0;
BEGIN
    IF NEW.status = OLD.status THEN
        NEW.updated_at := now();
        RETURN NEW;
    END IF;

    allowed := CASE OLD.status
        WHEN 'queued' THEN NEW.status IN ('running','cancelled')
        WHEN 'running' THEN NEW.status IN ('waiting_approval','completed','failed','cancelled')
        WHEN 'waiting_approval' THEN NEW.status IN ('running','failed','cancelled')
        WHEN 'completed' THEN NEW.status = 'archived'
        WHEN 'failed' THEN NEW.status IN ('queued','archived')
        WHEN 'cancelled' THEN NEW.status = 'archived'
        ELSE false
    END;

    IF NOT allowed THEN
        RAISE EXCEPTION 'invalid_job_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
    END IF;

    SELECT a.status
      INTO latest_approval_status
      FROM dcse_cp.escd_approvals a
     WHERE a.job_id = OLD.id
     ORDER BY a.requested_at DESC, a.id DESC
     LIMIT 1;

    IF OLD.status = 'waiting_approval' AND NEW.status = 'running' AND OLD.requires_approval AND latest_approval_status IS DISTINCT FROM 'approved' THEN
        RAISE EXCEPTION 'approved_decision_required' USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status = 'completed' THEN
        SELECT count(*) INTO evidence_count FROM dcse_cp.escd_evidence e WHERE e.job_id = OLD.id;
        IF NOT NEW.exit_criteria_met THEN RAISE EXCEPTION 'exit_criteria_not_met' USING ERRCODE = 'check_violation'; END IF;
        IF evidence_count = 0 THEN RAISE EXCEPTION 'evidence_required' USING ERRCODE = 'check_violation'; END IF;
        IF OLD.requires_approval AND latest_approval_status IS DISTINCT FROM 'approved' THEN RAISE EXCEPTION 'approved_decision_required' USING ERRCODE = 'check_violation'; END IF;
        NEW.completed_at := COALESCE(NEW.completed_at, now());
    END IF;

    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_job_transition_guard ON dcse_cp.escd_jobs;
CREATE TRIGGER escd_job_transition_guard BEFORE UPDATE OF status ON dcse_cp.escd_jobs FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_job_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_job_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_job_transition() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_record_job_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO dcse_cp.escd_job_events (job_id, event_type, summary, metadata, actor_user_id)
        VALUES (
            NEW.id,
            'status_transition',
            format('Job status changed from %s to %s', OLD.status, NEW.status),
            jsonb_build_object('from_status', OLD.status, 'to_status', NEW.status),
            auth.uid()
        );
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_job_transition_event ON dcse_cp.escd_jobs;
CREATE TRIGGER escd_job_transition_event AFTER UPDATE OF status ON dcse_cp.escd_jobs FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_record_job_transition();
REVOKE ALL ON FUNCTION dcse_cp.escd_record_job_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_record_job_transition() TO authenticated;

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_briefing_ack()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE
    prior_ack timestamptz;
BEGIN
    IF NEW.principal_user_id IS DISTINCT FROM auth.uid() THEN
        RAISE EXCEPTION 'briefing_ack_principal_mismatch' USING ERRCODE = 'check_violation';
    END IF;
    IF NEW.acknowledged_through > now() THEN
        RAISE EXCEPTION 'briefing_ack_in_future' USING ERRCODE = 'check_violation';
    END IF;

    SELECT max(a.acknowledged_through)
      INTO prior_ack
      FROM dcse_cp.escd_briefing_acks a
     WHERE a.principal_user_id = NEW.principal_user_id
       AND a.id IS DISTINCT FROM NEW.id;

    IF prior_ack IS NOT NULL AND NEW.acknowledged_through < prior_ack THEN
        RAISE EXCEPTION 'briefing_ack_regression' USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS escd_briefing_ack_guard ON dcse_cp.escd_briefing_acks;
CREATE TRIGGER escd_briefing_ack_guard BEFORE INSERT OR UPDATE ON dcse_cp.escd_briefing_acks FOR EACH ROW EXECUTE FUNCTION dcse_cp.escd_validate_briefing_ack();
REVOKE ALL ON FUNCTION dcse_cp.escd_validate_briefing_ack() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_briefing_ack() TO authenticated;

/* ROLLBACK, only after explicit DCS authorization:
DROP TRIGGER IF EXISTS escd_briefing_ack_guard ON dcse_cp.escd_briefing_acks;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_briefing_ack();
DROP TRIGGER IF EXISTS escd_job_transition_event ON dcse_cp.escd_jobs;
DROP FUNCTION IF EXISTS dcse_cp.escd_record_job_transition();
DROP TRIGGER IF EXISTS escd_job_transition_guard ON dcse_cp.escd_jobs;
DROP FUNCTION IF EXISTS dcse_cp.escd_validate_job_transition();
DROP TABLE IF EXISTS dcse_cp.escd_briefing_acks;
DROP TABLE IF EXISTS dcse_cp.escd_evidence;
DROP TABLE IF EXISTS dcse_cp.escd_approvals;
DROP TABLE IF EXISTS dcse_cp.escd_job_events;
DROP TABLE IF EXISTS dcse_cp.escd_jobs;
*/
