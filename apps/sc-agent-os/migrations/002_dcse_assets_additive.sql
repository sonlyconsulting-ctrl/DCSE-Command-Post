-- DCSE Command Post — Additive Assets Migration
-- Applies to: public.assets (nevgdyfpxdaloacuutal)
-- Strategy: additive only — existing columns (source_id, external_id, asset_type, url, metadata, payload) unchanged
-- Gate: DCS Authority authorization required before applying
-- Date: 2026-07-15

BEGIN;

-- DCSE lifecycle state (replaces/supplements asset_type for governance)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS dcse_state text
    CHECK (dcse_state IN ('discovered','inventoried','candidate','review','active','approved','deployed','superseded','archive','blocked','quarantined'))
    DEFAULT 'discovered' NOT NULL;

-- Human-readable name (asset_type is often a code)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS asset_name text;

-- Short label (for UI display)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS asset_label text;

-- Persona FK (nullable — some assets are persona-independent)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS persona_fk uuid REFERENCES public.personas(id) ON DELETE SET NULL;

-- Product reference (text, avoids hard FK to polymorphic products table)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS product_ref text;

-- Module reference (persona_modules link)
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS module_ref uuid REFERENCES public.persona_modules(id) ON DELETE SET NULL;

-- Privacy classification
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS privacy_class text
    CHECK (privacy_class IN ('public','internal','family','protected','classified'))
    DEFAULT 'internal' NOT NULL;

-- Child-safety gate
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS child_safe boolean DEFAULT false NOT NULL;

-- DCSE lane
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS dcs_lane text
    CHECK (dcs_lane IN ('dcs','sc','dcs-e','ss','family','internal'));

-- Governance tags
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS governance_tags text[] DEFAULT '{}' NOT NULL;

-- Approval tracking
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS approved_by text;

ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS approved_at timestamptz;

ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS approval_note text;

-- Deployment tracking
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS deployed_at timestamptz;

ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS deployment_ref text;

-- Tribunal PR reference
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS tribunal_pr_url text;

-- Agent limit enforcement
ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS agent_approve_locked boolean DEFAULT true NOT NULL;

ALTER TABLE public.assets
  ADD COLUMN IF NOT EXISTS agent_deploy_locked boolean DEFAULT true NOT NULL;

COMMENT ON COLUMN public.assets.dcse_state IS
  'DCSE governed lifecycle: discovered > inventoried > candidate > review > approved > deployed. Quarantined and blocked are holding states.';

COMMENT ON COLUMN public.assets.agent_approve_locked IS
  'Agents may not approve their own output. This flag enforces the agent limit at application layer.';

COMMENT ON COLUMN public.assets.agent_deploy_locked IS
  'Agents may not deploy assets. DCS authority required.';

-- RLS extension: add read policy for authenticated users
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE tablename='assets' AND policyname='assets_dcse_anon_public_read'
  ) THEN
    EXECUTE '
      CREATE POLICY assets_dcse_anon_public_read ON public.assets
        FOR SELECT TO anon
        USING (privacy_class = ''public'' AND dcse_state IN (''active'',''approved'',''deployed''))
    ';
  END IF;
END $$;

COMMIT;
