-- DCSE Command Post — Additive Personas Migration
-- Applies to: public.personas (nevgdyfpxdaloacuutal)
-- Strategy: additive only — no existing columns modified or dropped
-- Gate: DCS Authority authorization required before applying
-- Date: 2026-07-15

BEGIN;

-- Lifecycle state column (DCSE governed, parallel to legacy status)
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS dcse_lifecycle text
    CHECK (dcse_lifecycle IN ('draft','candidate','review','approved','active','suspended','superseded','archived'))
    DEFAULT 'draft' NOT NULL;

-- Privacy classification
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS privacy_class text
    CHECK (privacy_class IN ('public','internal','family','protected','classified'))
    DEFAULT 'internal' NOT NULL;

-- Child-safety flag (family product gating)
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS child_safe boolean DEFAULT false NOT NULL;

-- Identity mask flag — when true, no personal names, photos, or identifiers
-- Required for SNTY and ASP personas per DCSE privacy directive
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS identity_mask boolean DEFAULT false NOT NULL;

-- Family product flag — gates content visible to minors
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS family_product boolean DEFAULT false NOT NULL;

-- DCSE authority lane (finer than entity_lane)
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS dcs_lane text
    CHECK (dcs_lane IN ('dcs','sc','dcs-e','ss','family','internal'));

-- DCS approval tracking
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS approved_by text;

ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS approved_at timestamptz;

-- Governance note (free text, audit trail)
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS governance_note text;

-- Product link array (FK-by-reference to products)
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS product_refs text[] DEFAULT '{}' NOT NULL;

-- Agent limit enforcement flags
ALTER TABLE public.personas
  ADD COLUMN IF NOT EXISTS agent_promote_locked boolean DEFAULT true NOT NULL;

COMMENT ON COLUMN public.personas.dcse_lifecycle IS
  'DCSE governed lifecycle: draft > candidate > review > approved > active. Superseded and archived are terminal.';

COMMENT ON COLUMN public.personas.identity_mask IS
  'When true: no personal names, photos, or identifiable attributes may appear in any artifact referencing this persona. Required for SNTY and ASP.';

COMMENT ON COLUMN public.personas.agent_promote_locked IS
  'Agents may not promote a persona. This flag enforces the agent limit at application layer.';

COMMIT;
