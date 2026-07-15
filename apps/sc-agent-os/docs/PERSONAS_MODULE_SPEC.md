# Personas Module Specification
**Version:** 1.0
**Date:** 2026-07-15
**Status:** Candidate — Awaiting DCS authorization for Supabase apply

---

## Purpose

The Personas module is the central relationship spine of the DCSE Command Post. Every product, module, asset, task, approval, and tribunal artifact traces back to a persona.

`Persona → Product → Module → Asset → Task → Approval → Deployment → Tribunal`

---

## Lifecycle States

| State | Description | Transition |
|-------|-------------|------------|
| draft | Initial registration | → candidate |
| candidate | Under active development | → review |
| review | Submitted for DCS review | → approved, → suspended |
| approved | DCS approved — not yet active | → active |
| active | Actively referenced in products | → suspended, → superseded |
| suspended | Temporarily paused | → active, → archived |
| superseded | Replaced by newer version | terminal |
| archived | Retired | terminal |

Agents may NOT advance a persona from any state to approved or active. Only DCS Authority can.

---

## Registered Personas (Required 6)

### SHY/CRYS (shy_crs, P-202)
- **Lane:** SC
- **Segment:** Lifestyle / Travel / Social
- **Status:** Review (existing)
- **DCSE Lifecycle:** candidate (on migration apply)
- **Privacy:** internal
- **Child Safe:** false
- **Identity Mask:** false
- **Notes:** Two records exist (P-116 crystalshy SS, P-202 shy_crs SC). P-202 is the canonical SC lane record.

### SASH (sash, P-SASH)
- **Lane:** SC
- **Segment:** Lifestyle / Family / Organization
- **Status:** Draft
- **DCSE Lifecycle:** candidate
- **Privacy:** internal
- **Child Safe:** false
- **Family Product:** true
- **Identity Mask:** false
- **Notes:** Seed required. Connects to SC GovOS family product suite.

### SNTY (snty, P-SNTY)
- **Lane:** SC
- **Status:** Draft
- **DCSE Lifecycle:** draft
- **Privacy:** protected
- **Identity Mask:** TRUE
- **Rule:** No personal names, photos, or identifiers in any artifact. DCS authorization required before any content is associated.

### SJL (sjl, P-021)
- **Lane:** SS
- **Segment:** Youth / Independence / Life Transition
- **Status:** Review (existing)
- **DCSE Lifecycle:** review
- **Privacy:** internal
- **Notes:** Existing record. Has persona_modules defined. baller4life reference product.

### ASP (asp, P-ASP)
- **Lane:** SC
- **Status:** Draft
- **DCSE Lifecycle:** draft
- **Privacy:** protected
- **Identity Mask:** TRUE
- **Rule:** No personal names, photos, or identifiers in any artifact. DCS authorization required before any content is associated.

### DCS / SC / DCS-E
- **DCS Authority (P-DCS):** DCSE lane, active, classified, is_authority=true
- **SC Operator (P-SC):** SC lane, active, internal
- **DCS-E Extended (P-DCS-E):** DCSE lane, candidate, classified
- **Notes:** These are governance and operational personas, not audience personas.

---

## Agent Limits (Enforced)

Agents may NOT:
- Approve their own output for a persona
- Promote a persona (change lifecycle to approved/active)
- Publish child content under a persona
- Change privacy_class on a persona
- Override identity_mask=true

---

## API Endpoints

### GET /api/personas
Returns persona registry filtered by dcs_lane and privacy_class.
Requires: SUPABASE_SERVICE_ROLE_KEY env var on Vercel.

Query params: `lane` (dcs/sc/ss/family), `lifecycle` (state filter)

### GET /api/personas/:code
Returns single persona with modules list.

---

## Required Output Documents (cross-reference)
See: SCHEMA_INSPECTION_REPORT.md, ASSETS_MODULE_SPEC.md, ROLE_ACCESS_MATRIX.md, PRIVACY_CONTROLS.md, GOVERNANCE_GATES.md
