-- Migration: 001_aegis_schema.sql
-- Description: Core schema for Aegis Executive Kernel

-- 1. Create Schema
CREATE SCHEMA IF NOT EXISTS aegis;
GRANT USAGE ON SCHEMA aegis TO authenticated, service_role;

-- 2. Functions
CREATE OR REPLACE FUNCTION aegis.is_dcs_principal()
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  RETURN dcse_cp.is_dcs_owner();
END;
$$;

REVOKE EXECUTE ON FUNCTION aegis.is_dcs_principal() FROM anon, public;

CREATE OR REPLACE FUNCTION aegis.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

REVOKE EXECUTE ON FUNCTION aegis.set_updated_at() FROM anon, public;

-- 3. Tables

-- aegis.principals
CREATE TABLE IF NOT EXISTS aegis.principals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    display_name TEXT NOT NULL,
    primary_email TEXT NOT NULL UNIQUE,
    linked_emails TEXT[] DEFAULT '{}',
    auth_provider TEXT DEFAULT 'google',
    supabase_user_id UUID UNIQUE,
    role TEXT DEFAULT 'owner' CHECK (role IN ('owner','delegate','viewer')),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.principals ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.principals FORCE ROW LEVEL SECURITY;

CREATE POLICY "principals_owner_all" ON aegis.principals
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_principals
BEFORE UPDATE ON aegis.principals
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- aegis.missions
CREATE TABLE IF NOT EXISTS aegis.missions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    mission_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT '🏢',
    priority INTEGER DEFAULT 50 CHECK (priority BETWEEN 1 AND 100),
    status TEXT DEFAULT 'active' CHECK (status IN ('active','paused','archived')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.missions ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.missions FORCE ROW LEVEL SECURITY;

CREATE POLICY "missions_owner_all" ON aegis.missions
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_missions
BEFORE UPDATE ON aegis.missions
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- aegis.executive_sessions
CREATE TABLE IF NOT EXISTS aegis.executive_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    principal_id UUID REFERENCES aegis.principals(id) NOT NULL,
    session_start TIMESTAMPTZ DEFAULT now() NOT NULL,
    session_end TIMESTAMPTZ,
    last_briefing_at TIMESTAMPTZ,
    context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.executive_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.executive_sessions FORCE ROW LEVEL SECURITY;

CREATE POLICY "executive_sessions_owner_all" ON aegis.executive_sessions
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_executive_sessions
BEFORE UPDATE ON aegis.executive_sessions
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- aegis.jobs
CREATE TABLE IF NOT EXISTS aegis.jobs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    mission_id UUID REFERENCES aegis.missions(id),
    title TEXT NOT NULL,
    purpose TEXT,
    priority INTEGER DEFAULT 50 CHECK (priority BETWEEN 1 AND 100),
    executor TEXT,
    status TEXT DEFAULT 'queued' CHECK (status IN ('queued','running','waiting_approval','completed','failed','cancelled','archived')),
    provenance TEXT,
    requires_approval BOOLEAN DEFAULT false,
    evidence_refs JSONB DEFAULT '[]',
    failure_detail TEXT,
    deadline TIMESTAMPTZ,
    revenue_relevance NUMERIC(3,2) DEFAULT 0 CHECK (revenue_relevance BETWEEN 0 AND 1),
    dcs_override INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    completed_at TIMESTAMPTZ
);

ALTER TABLE aegis.jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.jobs FORCE ROW LEVEL SECURITY;

CREATE POLICY "jobs_owner_all" ON aegis.jobs
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_jobs
BEFORE UPDATE ON aegis.jobs
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- aegis.job_events
CREATE TABLE IF NOT EXISTS aegis.job_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_id UUID REFERENCES aegis.jobs(id) NOT NULL,
    event_type TEXT NOT NULL,
    actor TEXT DEFAULT 'aegis',
    summary TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.job_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.job_events FORCE ROW LEVEL SECURITY;

CREATE POLICY "job_events_owner_all" ON aegis.job_events
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

-- aegis.approvals
CREATE TABLE IF NOT EXISTS aegis.approvals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_id UUID REFERENCES aegis.jobs(id) NOT NULL,
    approval_type TEXT NOT NULL CHECK (approval_type IN ('external_send','publish','spending','deploy','destructive','credential_change','evidence_delete','irreversible')),
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected','expired')),
    requested_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    decided_at TIMESTAMPTZ,
    decided_by TEXT,
    decision_notes TEXT,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.approvals FORCE ROW LEVEL SECURITY;

CREATE POLICY "approvals_owner_all" ON aegis.approvals
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_approvals
BEFORE UPDATE ON aegis.approvals
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- aegis.evidence
CREATE TABLE IF NOT EXISTS aegis.evidence (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_id UUID REFERENCES aegis.jobs(id),
    evidence_type TEXT NOT NULL CHECK (evidence_type IN ('receipt','commit','migration','test_result','security_scan','approval_record','deployment','artifact','screenshot','manual_note')),
    title TEXT NOT NULL,
    content TEXT,
    reference_url TEXT,
    reference_sha TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.evidence FORCE ROW LEVEL SECURITY;

CREATE POLICY "evidence_owner_all" ON aegis.evidence
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

-- aegis.next_actions
CREATE TABLE IF NOT EXISTS aegis.next_actions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_id UUID REFERENCES aegis.jobs(id) NOT NULL,
    composite_score NUMERIC(10,4) DEFAULT 0,
    score_components JSONB DEFAULT '{}' NOT NULL,
    reason_summary TEXT,
    computed_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.next_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.next_actions FORCE ROW LEVEL SECURITY;

CREATE POLICY "next_actions_owner_all" ON aegis.next_actions
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

-- aegis.notifications
CREATE TABLE IF NOT EXISTS aegis.notifications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    principal_id UUID REFERENCES aegis.principals(id),
    channel TEXT DEFAULT 'in_app' CHECK (channel IN ('in_app','email','push_android')),
    title TEXT NOT NULL,
    body TEXT,
    priority TEXT DEFAULT 'normal' CHECK (priority IN ('low','normal','high','urgent')),
    job_id UUID REFERENCES aegis.jobs(id),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending','delivered','read','dismissed','failed')),
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

ALTER TABLE aegis.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE aegis.notifications FORCE ROW LEVEL SECURITY;

CREATE POLICY "notifications_owner_all" ON aegis.notifications
FOR ALL TO authenticated USING (dcse_cp.is_dcs_owner()) WITH CHECK (dcse_cp.is_dcs_owner());

CREATE TRIGGER set_updated_at_notifications
BEFORE UPDATE ON aegis.notifications
FOR EACH ROW EXECUTE FUNCTION aegis.set_updated_at();

-- Seed Data

INSERT INTO aegis.missions (mission_key, title, description, priority)
VALUES 
    ('dcs_enterprise', 'DCS Enterprise', 'Core enterprise operations and strategy', 90),
    ('dcs_employment', 'DCS Employment', 'Employment tracking and job search operations', 85)
ON CONFLICT (mission_key) DO NOTHING;

INSERT INTO aegis.principals (display_name, primary_email, linked_emails)
VALUES (
    'DCS Principal',
    'sonlyconsulting@gmail.com',
    '{"dseado01@gmail.com"}'
)
ON CONFLICT (primary_email) DO NOTHING;

/*
=========================
ROLLBACK SECTION
=========================

DROP TRIGGER IF EXISTS set_updated_at_notifications ON aegis.notifications;
DROP TRIGGER IF EXISTS set_updated_at_approvals ON aegis.approvals;
DROP TRIGGER IF EXISTS set_updated_at_jobs ON aegis.jobs;
DROP TRIGGER IF EXISTS set_updated_at_executive_sessions ON aegis.executive_sessions;
DROP TRIGGER IF EXISTS set_updated_at_missions ON aegis.missions;
DROP TRIGGER IF EXISTS set_updated_at_principals ON aegis.principals;

DROP TABLE IF EXISTS aegis.notifications;
DROP TABLE IF EXISTS aegis.next_actions;
DROP TABLE IF EXISTS aegis.evidence;
DROP TABLE IF EXISTS aegis.approvals;
DROP TABLE IF EXISTS aegis.job_events;
DROP TABLE IF EXISTS aegis.jobs;
DROP TABLE IF EXISTS aegis.executive_sessions;
DROP TABLE IF EXISTS aegis.missions;
DROP TABLE IF EXISTS aegis.principals;

DROP FUNCTION IF EXISTS aegis.set_updated_at();
DROP FUNCTION IF EXISTS aegis.is_dcs_principal();

DROP SCHEMA IF EXISTS aegis CASCADE;
*/
