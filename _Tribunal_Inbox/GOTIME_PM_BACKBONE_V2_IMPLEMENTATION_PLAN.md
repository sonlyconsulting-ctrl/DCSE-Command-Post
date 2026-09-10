# Implementation Plan v2: Command Post GoTime PM Backbone

**Supersedes:** the original AG implementation plan (`GoTime AG implementation_plan.md`, uploaded 2026-07-02).
**Status:** Corrected sequencing per DCS redirect order, informed by the completed Schema Reconciliation (Phase A) and RLS Policy Draft (Phase B).

## What changed from v1, and why

v1 proposed 8 new models and 5 new enums as a greenfield build. The reconciliation found that **6 of the 8 models and 2 of the 5 enums already exist, live, in production** (`pm_projects`, `pm_workstreams`, `pm_tasks`, `pm_blockers`, `pm_model_handoffs`, `pm_artifacts`, `cp_lanes`) — applied via raw SQL migrations that were never pulled into Prisma. v1 would have built a parallel, duplicate PM system next to one that already exists. v2 reverse-engineers the existing tables into Prisma and builds only what's genuinely missing.

v1 also proposed two intake routes (`from-tribunal`, `from-markdown`) writing directly into work orders, with PS protection handled only as "redacted titles" at the app layer. v2 routes both through a quarantine table with mandatory leakage scanning before anything reaches a work order — see `GOTIME_PM_BACKBONE_LEAKAGE_SCAN_SPEC.md`.

v2 also surfaces a pre-existing, GoTime-independent security gap found during RLS research: the existing `pm_*` tables' `authenticated_select` policies have no lane filter (`USING (true)`) — any authenticated user can currently read PS-lane project/task rows. This gets fixed as part of Phase A execution below, regardless of whether the rest of GoTime proceeds.

## Goal (unchanged from v1)

A Project/Task Management backbone for GoTime, DCS Employment, and PS planning inside `dcse-command-post` (Prisma/Supabase) and `DCSE_ASSET_PORTAL_APP` (Next.js), replacing manual copy/paste coordination with a `/cp/gotime` surface.

## User Review Required

> [!IMPORTANT]
> **Database schema changes (revised):** Reverse-engineer 6 existing `pm_*` tables + `cp_lanes`/`cp_entities` into Prisma with typed fields; add 1 genuinely new table (`pm_milestones`); extend 1 existing table (`pm_artifacts` for Deliverable semantics); add 3 genuinely new enums (`DcseWorkStatus`, `DcseAgentRole`, `DcseGateType`) codified from vocabulary already in production use. Do NOT create `DcseLane` or `DcseClassification` — reuse `cp_lanes` and `DcseConfidentiality`.
>
> **PS Firewall (revised):** RLS-enforced, not app-layer-only. `authenticated` role gets zero read access to any row with `lane_code = 'PS'`, enforced at the database level, matching the existing `routing_log` dual-layer pattern (table CHECK + RLS). Raw intake goes through mandatory leakage scanning before any work order is created — see Leakage Scan Spec.

---

## Phase A: Schema Reconciliation Execution

*(The report itself — `GOTIME_PM_BACKBONE_SCHEMA_RECONCILIATION.md` — is already complete. This phase is executing what it found.)*

1. Reverse-engineer into `schema.prisma`, with proper typed fields and real `@relation` pairs (this schema currently has zero relations anywhere — a deliberate improvement, not matching existing drift): `pm_projects` → `Project`, `pm_workstreams` → `WorkOrder`, `pm_tasks` → `Task`, `pm_blockers` → `Blocker`, `pm_model_handoffs` → `AgentAssignment`, `cp_lanes`, `cp_entities`.
2. Extend `pm_artifacts` (not a new model) with `deliverable_flag`, `acceptance_status`, `accepted_at`, `accepted_by` for Deliverable semantics.
3. Add new `pm_milestones` table per the RLS draft.
4. Add `DcseWorkStatus` enum seeded from the 9 values already live in `pm_tasks.status` usage. Add `DcseAgentRole` enum seeded from the existing documented model-role vocabulary — this touches production rows in `pm_tasks.model_role` and `pm_model_handoffs.from_model`/`to_model`, so it needs a value-mapping/backfill step, not a pure additive migration. Add `DcseGateType`, and evaluate collapsing `pm_tasks`'s three gate-related booleans (`stop_gate_flag`, `validation_required`, `opus_validation_required`) into it.
5. Model `TribunalReceipt` as an `AuditLog` specialization (`actionName = 'TRIBUNAL_RECEIPT'`, JSONB payload matching the existing `tribunal_receipts/*.json` file shape) rather than a new table, unless a concrete reason emerges to split it out.
6. **Fix the pre-existing gap**: add `lane_code != 'PS'` to every `{pm_table}_authenticated_select` policy (see RLS draft Part 3) — this is required regardless of GoTime's fate.

**Deliverable:** updated `schema.prisma` (not yet migrated), migration SQL reflecting items 1-6 above.
**Gate:** DCS review of the diff before `prisma migrate dev` runs against the live database.

## Phase B: PS Firewall Database Policy — Execution

*(Draft is done — `GOTIME_PM_BACKBONE_RLS_POLICY_DRAFT.sql`. This phase applies it.)*

1. Apply the `pm_milestones` and `gotime_intake_quarantine` table creation + RLS from the draft.
2. Apply the lane-scoping fix to all existing `pm_*` `authenticated_select` policies.
3. Run the verification queries from the draft's Part 4 — confirm zero rows with `lane_code = 'PS'` are visible to the `authenticated` role.
4. **Open question needing DCS input before this is final**: no existing mechanism distinguishes "PS-lane-authorized reviewer" from an ordinary authenticated user. Current draft defaults to "only service_role touches PS rows, full stop" — meaning even a legitimate PS-lane reviewer needs backend-mediated access, not direct dashboard queries. Confirm this is acceptable, or specify the intended auth mechanism (custom JWT claim, a `ps_reviewers` table, etc.) so the policy can be refined.

**Gate:** DCS review and answer to the open question above before migration runs.

## Phase C: Leakage Scanner — Execution

*(Spec is done — `GOTIME_PM_BACKBONE_LEAKAGE_SCAN_SPEC.md`. This phase implements it.)*

1. Build the scanner as middleware in front of `POST /api/work-orders/from-tribunal` and `POST /api/work-orders/from-markdown` — both routes write to `gotime_intake_quarantine`, never directly to a work order.
2. Implement the term-match logic and protected-name-list lookup per the spec.
3. Implement the 8 required test cases from the spec before this ships.
4. Wire the state-flow transitions (`RAW_INTAKE` → `LEAKAGE_SCAN_PENDING` → `FLAGGED_PS_HOLD` | `CLEARED_FOR_WORK_ORDER_DRAFT` → `DCS_REVIEW` → `WORK_ORDER_READY`).

**Gate:** all 8 test cases passing before any live intake is processed.

## Phase D: Dashboard Shell (mock/safe data only)

Unchanged in spirit from v1's Component 3, restricted per the redirect order:

1. Build `/cp/gotime` with the 8-tab layout (Projects, Work Orders, Tasks, Deliverables, Blockers, Agents, Receipts, Intake) using mock data or existing non-PS-lane records only.
2. Color coding as v1 proposed: red for STOP_GATE/CONFIDENTIAL_PS, amber for DCS_REVIEW/BLOCKED, green for APPROVED, blue/neutral otherwise.
3. Intake tab UI (paste box, file drop) may exist and call the quarantine endpoint, but must display quarantine status only — never raw intake content for anything flagged `FLAGGED_PS_HOLD`.
4. **Not permitted at this phase**: live DB write of raw Tribunal/markdown text into work orders, schema migration without review, production deployment, PS evidence ingestion in any visible dashboard view.

## Phase E: Tribunal Receipt

Covered by `TRIBUNAL_20260702_DCSE_CP_GOTIME_PM_BACKBONE_REDIRECT.json` (Phase F of the redirect order, produced alongside this plan).

---

## API Endpoints (revised from v1)

| Endpoint | v1 behavior | v2 behavior |
|---|---|---|
| `GET /api/projects` | List projects | Unchanged, but now reads from the reverse-engineered `Project` model (`pm_projects`) |
| `POST /api/projects` | Create a project | Unchanged |
| `GET /api/work-orders` | List work orders | Reads from `WorkOrder` (`pm_workstreams`) |
| `POST /api/work-orders` | Create directly | Unchanged for non-intake-sourced creation (manual entry still direct) |
| `PATCH /api/work-orders/:id` | Update status/gate/owner | Unchanged |
| `POST /api/work-orders/from-tribunal` | **Parsed Tribunal JSON directly into a work order** | Writes to `gotime_intake_quarantine` only. Never creates a work order directly. |
| `POST /api/work-orders/from-markdown` | **Parsed pasted notes directly into a work order** | Same — quarantine only |
| `GET /api/deliverables` | List deliverables | Reads from extended `pm_artifacts` |
| `PATCH /api/deliverables/:id` | Update scan status/path/hash | Unchanged |
| `POST /api/receipts` | Attach/create Tribunal receipt | Unchanged in shape; storage target per Phase A item 5 |
| **`POST /api/intake/scan`** *(new)* | — | Runs the leakage scanner against a quarantine record, transitions its status |
| **`POST /api/intake/:id/promote`** *(new)* | — | DCS-gated promotion from `CLEARED_FOR_WORK_ORDER_DRAFT`/`DCS_REVIEW` to an actual `WorkOrder`/`Task` row |

## Verification Plan (revised)

### Automated
- `npx prisma format` & `npx prisma validate`
- Seed script + query verification
- `npm run build` in `DCSE_ASSET_PORTAL_APP/apps/web`
- **New**: the 8 leakage-scanner test cases from the spec, run as an actual test suite, not manual verification
- **New**: RLS verification query confirming zero PS-lane rows visible under `authenticated` role (see RLS draft Part 4)

### Manual
- Load `/cp/gotime`, smoke test tabs
- Confirm PS records show redacted summaries only, no raw content, in every view
- Paste a known-PS-term test string into the intake area, confirm it lands in `FLAGGED_PS_HOLD` and never appears as a work order

## Priority order for this phase (per redirect order)

Schema Reconciliation → RLS Policy → Leakage Scanner → Intake Quarantine → Dashboard Shell → Tribunal Receipt. No production deployment, no live Supabase mutation, no automated PS-content persistence, no duplicate enum creation, until DCS clears each gate above.
