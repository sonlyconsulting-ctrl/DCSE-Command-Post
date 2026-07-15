# Schema Inspection Report
**Date:** 2026-07-15
**Project:** nevgdyfpxdaloacuutal (DCSE Command Post Supabase)
**Conducted by:** Claude Code agent (read-only)

---

## Tables Inspected

### public.personas (37 rows)
| Column | Type | Default | Null |
|--------|------|---------|------|
| id | uuid | gen_random_uuid() | NO |
| persona_id | varchar | | NO |
| code | varchar | | NO |
| display_name | varchar | | NO |
| short_label | varchar | | YES |
| tagline | varchar | | YES |
| description | text | | YES |
| segment | varchar | | YES |
| primary_intent | text | | YES |
| audience_age_min | integer | | YES |
| audience_age_max | integer | | YES |
| ai_fluency | varchar | | YES |
| time_profile | varchar | | YES |
| primary_channels | text[] | '{}' | YES |
| offers_fit | text | | YES |
| onboarding_path | text | | YES |
| entity_lane | text | 'SS' | NO |
| status | text | 'Draft' | NO |
| release_posture | text | 'Internal' | NO |
| voice_profile | jsonb | '{}' | NO |
| metadata | jsonb | '{}' | NO |
| created_at | timestamptz | now() | NO |
| updated_at | timestamptz | now() | NO |

**RLS:** authenticated SELECT where release_posture IN ('Internal','Review','Public'); service_role ALL

**DCSE Fields Missing:** dcse_lifecycle, privacy_class, child_safe, identity_mask, family_product, dcs_lane, approved_by, approved_at, governance_note, product_refs, agent_promote_locked

---

### public.assets (7 rows)
| Column | Type | Default | Null |
|--------|------|---------|------|
| id | uuid | gen_random_uuid() | NO |
| created_at | timestamptz | now() | YES |
| updated_at | timestamptz | now() | YES |
| source_id | uuid | | YES |
| external_id | text | | YES |
| asset_type | text | | YES |
| url | text | | YES |
| metadata | jsonb | | YES |
| payload | jsonb | | YES |

**RLS:** authenticated SELECT all; service_role ALL

**DCSE Fields Missing:** dcse_state, asset_name, asset_label, persona_fk, product_ref, module_ref, privacy_class, child_safe, dcs_lane, governance_tags, approved_by, approved_at, approval_note, deployed_at, deployment_ref, tribunal_pr_url, agent_approve_locked, agent_deploy_locked

---

### public.persona_modules (7 rows)
Full structure present: id, persona_id (FK), module_code, series_number, part_number, part_suffix, title, subtitle, description, tier, status, topics[], domains[], score_tracks[], outcomes[], content (jsonb), sort_order, created_at, updated_at

**RLS:** authenticated SELECT filtered by persona.release_posture (excludes 'PS' lane); service_role ALL

---

### public.products (303 rows)
**RLS:** anon SELECT all (public read)

---

## Persona Coverage for Required 6

| Persona | Code | Exists | persona_id | Notes |
|---------|------|--------|------------|-------|
| SHY/CRYS | shy_crs | YES (P-202) | P-202 | SC lane, also P-116 (crystalshy, SS lane) |
| SJL | sjl | YES (P-021) | P-021 | SS lane |
| SASH | sash | NO | | Needs seed |
| SNTY | snty | NO | | Needs seed, identity_mask=true |
| ASP | asp | NO | | Needs seed, identity_mask=true |
| DCS/SC/DCS-E | dcs / sc_operator / dcs_e | NO | | Needs seed |

---

## Migration Requirements

1. `001_dcse_personas_additive.sql` — 11 additive columns to personas
2. `002_dcse_assets_additive.sql` — 17 additive columns + 1 RLS policy to assets
3. `003_dcse_persona_seeds.sql` — 6 INSERT rows (idempotent via WHERE NOT EXISTS)

**All migrations are additive. No existing columns modified or dropped.**
**Gate: DCS Authority authorization required before applying any migration.**
