-- ESCD Multi-Model Conversation Continuity & Response Governance Schema Candidate
-- Task ID: DCSE-ESCD-CONTINUITY-001
-- Candidate DDL for dedicated conversation state and immutable turn history.
-- CANDIDATE ONLY. Do not apply to production without explicit DCS authorization.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
GRANT USAGE ON SCHEMA dcse_cp TO authenticated;

-- 1. Canonical ESCD Conversations
CREATE TABLE IF NOT EXISTS dcse_cp.escd_conversations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id text NOT NULL UNIQUE,
    title text NOT NULL DEFAULT 'New Conversation',
    active_provider text NOT NULL DEFAULT 'openai',
    active_model text NOT NULL DEFAULT 'gpt-5.6-sol',
    active_entity_lane text NOT NULL DEFAULT 'DCSE',
    active_project_id text,
    current_goal text,
    confirmed_decisions jsonb NOT NULL DEFAULT '[]'::jsonb,
    pinned_facts jsonb NOT NULL DEFAULT '[]'::jsonb,
    superseded_facts jsonb NOT NULL DEFAULT '[]'::jsonb,
    open_questions jsonb NOT NULL DEFAULT '[]'::jsonb,
    state jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS escd_conversations_user_idx ON dcse_cp.escd_conversations(created_by_user_id);
CREATE INDEX IF NOT EXISTS escd_conversations_updated_idx ON dcse_cp.escd_conversations(updated_at DESC);

-- 2. Canonical ESCD Conversation Turns
CREATE TABLE IF NOT EXISTS dcse_cp.escd_conversation_turns (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id text NOT NULL REFERENCES dcse_cp.escd_conversations(conversation_id) ON DELETE CASCADE,
    seq integer NOT NULL,
    user_message text NOT NULL,
    assistant_response text NOT NULL,
    provider text NOT NULL,
    model text NOT NULL,
    entity_lane text NOT NULL DEFAULT 'DCSE',
    project_task text,
    evidence_classification text NOT NULL DEFAULT 'ASSUMPTION',
    retrieved_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    authority_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_escd_turns_conv_seq UNIQUE (conversation_id, seq)
);

CREATE INDEX IF NOT EXISTS escd_turns_conv_idx ON dcse_cp.escd_conversation_turns(conversation_id, seq ASC);

-- 3. Row Level Security Policies
ALTER TABLE dcse_cp.escd_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_conversations FORCE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_conversation_turns ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_conversation_turns FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_conversations_dcs_owner ON dcse_cp.escd_conversations;
CREATE POLICY escd_conversations_dcs_owner ON dcse_cp.escd_conversations FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND created_by_user_id = auth.uid());

DROP POLICY IF EXISTS escd_turns_dcs_owner ON dcse_cp.escd_conversation_turns;
CREATE POLICY escd_turns_dcs_owner ON dcse_cp.escd_conversation_turns FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner());

REVOKE ALL ON dcse_cp.escd_conversations, dcse_cp.escd_conversation_turns FROM authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON dcse_cp.escd_conversations, dcse_cp.escd_conversation_turns TO authenticated;
