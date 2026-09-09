# ESCD Runtime Repair 001 Report

**Task ID:** DCSE-ESCD-001-RUNTIME-001  
**Parent:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Branch:** `feature/escd-runtime-repair-001`  
**Source baseline:** `feature/aegis-executive-kernel` at `db7c1e7917cc4aa9e2b9788048ced43855f12090`  
**Historical AG01 checkpoint preserved:** `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`  
**Status:** READY FOR CODEX REVIEW, NOT RELEASED

## Preflight Validation

- Authority source: current DCSE v7.2 R5 operative designation and controlling controller as referenced by `DCSE_MANIFEST.yaml` and current runtime harmony directive.
- GitHub access: VERIFIED.
- Supabase access: VERIFIED for read-only inspection and authorization-boundary validation.
- Production mutation authority: NOT exercised.
- Secret exposure: NONE.
- PS exposure: NONE.
- Rollback: Git branch commits are reversible; database migration remains unapplied and includes rollback SQL.
- Release posture: candidate implementation only. No merge to main, production deployment, live ESCD DDL, Google OAuth provider change, or Android push claim.

## Live Supabase Findings Before Design

Read-only inspection of project `nevgdyfpxdaloacuutal` established:

- `dcse_cp` is the existing control schema with the active Agent OS/runtime tables.
- No `aegis` or `escd` base tables were present at inspection time.
- `dcse_cp.operator_accounts` already provides `user_id`, `email`, `active`, and `access_scope`.
- `dcse_cp.is_dcs_owner()` resolves authorization from `auth.uid()` against active operator accounts with `dcse_internal_dashboards` or `dcse_owner` scope.
- Existing `operator_accounts` RLS permits authenticated users to select only their own active record.

Read-only authorization tests against the existing live boundary returned:

1. `anon` access to `dcse_cp.operator_accounts`: denied at schema boundary.
2. `authenticated` with a non-operator JWT subject: 0 visible operator rows.
3. `authenticated` with the active DCS operator subject: 1 visible operator row.

These tests validate the existing DCS identity/RLS foundation. They do not claim the new ESCD tables are live because the new migration was deliberately not applied to production.

## 1. AG01 Preservation

PASS.

The AG01 checkpoint remains unchanged on `feature/aegis-antigravity-slice001` at `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`. The repair tranche was built on a new controller-created branch rather than rewriting AG historical evidence.

## 2. Authenticated API Boundary

PASS at candidate-code level.

Implemented:

- `apps/escd/runtime/auth.py`
- `apps/escd/runtime/repository.py`
- `apps/escd/api/index.py`

The repaired boundary:

- requires a bearer token;
- validates it through Supabase Auth `/auth/v1/user`;
- verifies the caller against the DCS operator boundary;
- uses the caller JWT plus anon key for PostgREST operations;
- deliberately removes service-role credentials from the ESCD request path;
- relies on `auth.uid()` and RLS for data authorization;
- fails closed when auth configuration or operator authorization is missing.

## 3. Approval and Evidence Completion Gates

PASS at policy/runtime/database-contract level.

Implemented in `apps/escd/runtime/service.py` and candidate migration:

- `waiting_approval -> completed` remains prohibited by the existing tested ESCD state graph;
- `waiting_approval -> running` requires an approved decision when approval is required;
- completion requires exit criteria plus at least one evidence reference;
- approval identity comes from authenticated `user_id`, not a client-supplied `decided_by` label;
- the database transition trigger independently repeats the critical transition, approval, evidence, and exit-criteria checks.

This creates defense in depth between policy code and persistence rules.

## 4. Safe Rendering

PASS at candidate-code level.

Implemented:

- `apps/escd/runtime/render.py`
- `apps/escd/web/index.html`

Persisted/user-controlled values are rendered with HTML escaping or DOM `textContent`. The new ESCD shell does not use `innerHTML` for persisted content.

## 5. Governed Next Best Action Integration

PASS at candidate-code level.

The historical Aegis eight-factor scorer is not promoted. `apps/escd/runtime/service.py` adapts persisted ESCD job fields into the existing tested `Item` model and calls the governed `rank_items()` policy implementation with the 10-factor ESCD weights and deterministic tie-break behavior.

User-facing terminology is **Next Best Action** rather than the ambiguous acronym.

## 6. Briefing Acknowledgement Repair

PASS at candidate-code level.

Briefing GET no longer advances its own comparison cursor. A separate `/api/escd/briefing/ack` operation persists acknowledgement state in `dcse_cp.escd_briefing_acks` after explicit client acknowledgement.

The briefing snapshot uses the existing tested `build_briefing_snapshot()` policy contract and persisted state.

## 7. Supabase/RLS Repair and Validation

PASS for design plus current-boundary validation. LIVE ESCD DDL REMAINS RELEASE-GATED.

Candidate migration:

`supabase/migrations/20260909_escd_runtime_state.sql`

It creates only namespaced `dcse_cp.escd_*` state objects rather than a duplicate orchestration schema:

- `escd_jobs`
- `escd_job_events`
- `escd_approvals`
- `escd_evidence`
- `escd_briefing_acks`

Controls include:

- RLS enabled and forced on every table;
- `dcse_cp.is_dcs_owner()` policies;
- DML granted only to `authenticated`;
- no service-role grant required for the application path;
- transition trigger with approval/evidence/exit hard gates;
- request/evidence uniqueness fields for idempotency support;
- explicit rollback block.

The migration was NOT applied to production, so production-table positive/negative tests are deferred to the controlled migration/release step.

## 8. Double-Test / Adversarial Pass

PASS for the runtime candidate code available in this execution surface.

Local validation performed against the exact new runtime logic:

- Python compile check: PASS.
- Runtime/security test suite: **15 passed, 0 failed**.

Coverage includes:

- bearer-token requirement;
- Supabase user validation;
- DCS operator authorization;
- approval-gated state recovery;
- direct waiting-approval completion rejection;
- evidence-backed completion;
- exit-criteria completion gate;
- authenticated approval actor binding;
- governed Next Best Action adapter;
- persisted-state briefing source;
- HTML/script escaping;
- no service-role API path;
- CORS origin allowlist rather than wildcard;
- no `innerHTML` persisted rendering;
- explicit briefing acknowledgement;
- RLS and database transition contract checks;
- no Employment seed or Aegis product identity in the new ESCD shell.

The prior pure policy tranche remains separately recorded at **105 passed, 0 failed**. This report does not fabricate a combined CI run because the current tool execution environment cannot clone GitHub directly for one physical all-branch test invocation.

## 9. Controlled Aegis to ESCD Reconciliation

COMPLETE for candidate architecture and code routing. Historical source remains preserved.

| AG01 element | Disposition | ESCD treatment |
|---|---|---|
| Aegis historical branch/checkpoint | REUSE AS EVIDENCE | Preserved unchanged |
| DCS visual palette/responsive concept | REUSE | Carried into safe ESCD shell |
| Inline `innerHTML` SPA pattern | SUPERSEDE | Safe DOM/text rendering |
| Service-role API pattern | SUPERSEDE | User JWT plus RLS |
| Aegis eight-factor scorer | SUPERSEDE | Tested ESCD Next Best Action policy |
| Aegis briefing concept | REPAIR/REUSE | Persisted-state snapshot plus explicit ack |
| Aegis approval flow | SUPERSEDE/REPAIR | Authenticated actor plus state/evidence hard gates |
| Standalone `aegis` schema proposal | SUPERSEDE | Candidate `dcse_cp.escd_*` persistence objects |
| AG test suite | REUSE AS HISTORICAL REGRESSION INPUT | New runtime adversarial tests added |
| DCS Employment mission | DEFER | Remains outside ESCD core |
| Google OAuth scaffold | DEFER EXTERNAL CONFIG | No unsupported completion claim |
| Android push stub | DEFER DEVICE TEST | No unsupported completion claim |

## Changed Candidate Files

- `apps/escd/runtime/auth.py`
- `apps/escd/runtime/repository.py`
- `apps/escd/runtime/service.py`
- `apps/escd/runtime/render.py`
- `apps/escd/api/index.py`
- `apps/escd/web/index.html`
- `apps/escd/tests/test_runtime_security.py`
- `supabase/migrations/20260909_escd_runtime_state.sql`

## Remaining Release Gates

These are intentionally NOT represented as implementation failures:

1. Independent Codex engineering/security review.
2. Controlled application of the candidate ESCD migration to a safe database target, followed by ESCD-table RLS positive/negative testing.
3. Google OAuth provider/runtime configuration and actual authenticated browser session test.
4. Android push/device testing when that later requirement is activated.
5. Production deployment/release approval.

## Exit

**READY_FOR_CODEX_REVIEW**

The requested 1-9 engineering repair/reconciliation tranche is complete at candidate-code/evidence level. The branch is not production-ready or released, and no release-gated external action has been silently performed.
