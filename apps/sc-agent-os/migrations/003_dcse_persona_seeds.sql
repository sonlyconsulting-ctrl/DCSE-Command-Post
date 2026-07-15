-- DCSE Persona Seeds — Missing Governed Personas
-- Applies to: public.personas (nevgdyfpxdaloacuutal)
-- Gate: DCS Authority authorization required before applying
-- Privacy rule: identity_mask=true for SNTY and ASP — no personal names
-- Date: 2026-07-15
-- Prerequisite: Migration 001 must be applied first

BEGIN;

-- SASH — SC Lane lifestyle/family persona
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe, family_product,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-SASH', 'sash', 'SASH', 'SASH',
  'Life in motion — organized, elevated, grounded',
  'Lifestyle / Family / Organization',
  'SC', 'Draft', 'Internal',
  'candidate', 'internal', false, true,
  'sc', false, true,
  '{"tone":"warm","pace":"measured","register":"personal-brand"}',
  '{"dcse_note":"SC lane family lifestyle persona. Connects to SC GovOS product suite.","created_by":"dcse_agent","requires_dcs_approval":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'sash');

-- SNTY — Identity-masked persona (no personal names per DCSE privacy directive)
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe, family_product,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-SNTY', 'snty', 'SNTY', 'SNTY',
  '[Identity masked — no personal descriptor]',
  '[Segment masked]',
  'SC', 'Draft', 'Internal',
  'draft', 'protected', false, false,
  'sc', true, true,
  '{"tone":"masked","pace":"masked","register":"masked"}',
  '{"dcse_note":"Identity-masked persona. No personal names, photos, or identifiers in any artifact. DCS authorization required before any content is associated.","identity_mask_reason":"privacy_directive","requires_dcs_approval":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'snty');

-- ASP — Identity-masked persona (no personal names per DCSE privacy directive)
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe, family_product,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-ASP', 'asp', 'ASP', 'ASP',
  '[Identity masked — no personal descriptor]',
  '[Segment masked]',
  'SC', 'Draft', 'Internal',
  'draft', 'protected', false, false,
  'sc', true, true,
  '{"tone":"masked","pace":"masked","register":"masked"}',
  '{"dcse_note":"Identity-masked persona. No personal names, photos, or identifiers in any artifact. DCS authorization required before any content is associated.","identity_mask_reason":"privacy_directive","requires_dcs_approval":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'asp');

-- DCS Authority — DCSE internal governance persona
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-DCS', 'dcs', 'DCS Authority', 'DCS',
  'Governance authority for the SC enterprise',
  'Internal / Governance',
  'DCSE', 'Active', 'Internal',
  'active', 'classified', false,
  'dcs', false, true,
  '{"tone":"directive","pace":"authoritative","register":"institutional","rule":"lead_constructively_no_dominating_contrast"}',
  '{"dcse_note":"DCS is the governance authority. Agents cannot approve output for this persona. D08 v6.9.1 voice rule applies.","requires_dcs_approval":false,"is_authority":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'dcs');

-- SC Operator — SC entity operator persona
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-SC', 'sc_operator', 'SC Operator', 'SC',
  'Strategic operator of the Sonly Consulting enterprise',
  'Internal / Operations',
  'SC', 'Active', 'Internal',
  'active', 'internal', false,
  'sc', false, true,
  '{"tone":"operator","pace":"decisive","register":"brand-authority"}',
  '{"dcse_note":"SC operator persona. Primary voice for Sonly Consulting brand materials.","requires_dcs_approval":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'sc_operator');

-- DCS-E Extended — DCSE enterprise extended authority
INSERT INTO public.personas (
  persona_id, code, display_name, short_label, tagline,
  segment, entity_lane, status, release_posture,
  dcse_lifecycle, privacy_class, child_safe,
  dcs_lane, identity_mask, agent_promote_locked,
  voice_profile, metadata
)
SELECT
  'P-DCS-E', 'dcs_e', 'DCS-E Extended', 'DCS-E',
  'Extended DCSE enterprise authority — cross-product governance',
  'Internal / Governance / Enterprise',
  'DCSE', 'Draft', 'Internal',
  'candidate', 'classified', false,
  'dcs-e', false, true,
  '{"tone":"directive","pace":"authoritative","register":"enterprise","rule":"lead_constructively_no_dominating_contrast"}',
  '{"dcse_note":"Extended DCS authority persona for cross-product and enterprise-level governance decisions.","requires_dcs_approval":true}'
WHERE NOT EXISTS (SELECT 1 FROM public.personas WHERE code = 'dcs_e');

COMMIT;
