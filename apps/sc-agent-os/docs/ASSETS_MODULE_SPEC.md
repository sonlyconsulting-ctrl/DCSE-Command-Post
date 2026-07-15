# Assets Module Specification
**Version:** 1.0
**Date:** 2026-07-15
**Status:** Candidate — Awaiting DCS authorization for Supabase apply

---

## Purpose

The Assets module is the governed inventory of all SC/DCSE deliverables: web pages, documents, media, code modules, product links, and registered outputs. Every asset traces to a persona, product, or module and passes through the approval/tribunal gate before deployment.

---

## Lifecycle States

| State | Description |
|-------|-------------|
| discovered | Referenced but not formally registered |
| inventoried | Registered, metadata complete |
| candidate | Under active build |
| review | Submitted for DCS review |
| active | In use, not yet formally approved |
| approved | DCS approved |
| deployed | Live in production |
| superseded | Replaced by newer version |
| archive | Retired |
| blocked | Flagged, action required |
| quarantined | Isolated — potential PS or policy violation |

---

## Asset Types (from existing asset_type values)

- `url` — external link / product page
- `document` — governance doc, spec, report
- `code` — codebase module, script, function
- `media` — image, video, audio (PS Firewall applies)
- `schema` — database migration or schema definition
- `build` — deployed build artifact
- `dispatch` — dispatch packet
- `pr` — GitHub pull request / Tribunal entry

---

## Privacy Classification

| Class | Accessible by |
|-------|--------------|
| public | Anyone |
| internal | Authenticated DCSE operators |
| family | Family administrators + parents |
| protected | DCS Authority only (identity-masked personas) |
| classified | DCS Authority only |

Child-safe assets (child_safe=true) may only surface in family products where family_product=true on the parent persona.

---

## Agent Limits (Enforced)

Agents may NOT:
- Approve their own output (agent_approve_locked=true)
- Deploy assets (agent_deploy_locked=true)
- Change privacy_class
- Change dcse_state to approved/deployed
- Publish child content

---

## Relationship Spine

```
Persona (P-xxx)
  └── Product (product_ref)
        └── Module (module_ref → persona_modules)
              └── Asset (this table)
                    └── Task (pm_tasks)
                          └── Approval (dcse_audit_events)
                                └── Deployment (deployed_at, deployment_ref)
                                      └── Tribunal (tribunal_pr_url)
```

---

## API Endpoints

### GET /api/assets
Returns asset inventory. Requires SUPABASE_SERVICE_ROLE_KEY.
Query params: `persona` (persona code), `state` (dcse_state), `lane` (dcs_lane)

### GET /api/assets/:id
Returns single asset with full governance metadata.

---

## Current Assets (7 rows pre-migration)

The existing 7 rows use the legacy schema (source_id, external_id, asset_type, url). Post-migration these will gain DCSE governance columns with defaults.

Recommended first registration pass:
1. SC Agent OS v1.3 Vercel deployment
2. SC Landing Page trial build
3. DCSE Governance Doctrine (D01-D08)
4. Tribunal Relay GitHub repo
5. Command Post GitHub repo
6. SC GovOS RAG website (architecture)
7. Supabase SC Schema
