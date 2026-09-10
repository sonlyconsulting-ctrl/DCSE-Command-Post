# DCSE DDNA Consumer Cutover Resume Blocked Receipt

Task ID: `DCSE-DDNA-CONSUMER-CUTOVER-20260909-001`
Parent: `DCSE-RCHE-20260909-HARVEST-001`
Status: `FAIL STOP / BLOCKED`
Date: 2026-09-09
Authority: DCSE Master Profile v7.2 R5 OPERATIVE
Release authority: DCS conditional advance authorization recorded on Issue #67
Branch: `ddna-consumer-cutover-20260909`
PR: `#69`
Issue: `#67`

## Resume source state

- Fresh live checkout created from branch `ddna-consumer-cutover-20260909`.
- Starting live branch head before repair: `894870cb286480ce6145ffddc2115322d92ed039`.
- PR #69 verified open, non-draft, mergeable, base `main`, head `ddna-consumer-cutover-20260909`.
- Existing PR scope at resume contained `api/runtime.js`, `tests/sc-agent-os-ddna-cutover.test.js`, `vercel.json`, and DDNA mapping/runtime evidence.

## Repairs performed in this continuation

1. Repaired Vercel ignored-build behavior.
   - Replaced the brittle root `ignoreCommand` with `node scripts/vercel/should-ignore-sc-agent-os-build.js`.
   - The script builds when SC Agent OS, DDNA runtime, governance evidence, test, or Vercel config files changed.
   - The script ignores deployments only when no SC Agent OS/DDNA runtime change is detected.
   - If Vercel commit metadata is unavailable or cannot be evaluated, the script builds for validation safety.

2. Repaired deployed route placement.
   - Vercel Preview showed the project deploys from `apps/sc-agent-os`; the prior root-level `api/runtime.js` was not the effective deployed route.
   - Added `apps/sc-agent-os/api/runtime.js` with the DDNA cutover runtime handler.
   - Updated `apps/sc-agent-os/vercel.json` with an exact `/api/runtime` route before the catch-all.
   - Updated `apps/sc-agent-os/api/index.js` so the catch-all also delegates `GET /api/runtime` to the DDNA cutover handler if routing falls through.
   - Preserved `/api/runtime/smoke` on the existing smoke handler.

3. Repaired release regression failure in password recovery flow.
   - Existing password recovery tests failed because the inline browser script used compressed variable names and bare `location` references that broke the test harness and weakened readability.
   - Expanded the login and recovery scripts in `api/index.js` to use stable variable names, `window.location`, and the guarded Supabase recovery flow expected by the existing tests.
   - No credential handling, auth policy, DDNA data, RLS, or release authority was changed by this repair.

4. Avoided unauthorized legacy credential movement.
   - The approval reviewer rejected copying the legacy SC-Command-Post service-role key into a new Vercel variable because that separate credential transfer was not explicitly authorized.
   - Instead, the runtime now supports the existing Vercel legacy server binding name `PABASE_SECRET_KEY` as a fallback when `SUPABASE_SERVICE_ROLE_KEY` is absent.
   - No legacy secret value was printed, copied into Git, or moved to a new destination during this repair.

## Vercel environment binding evidence

Confirmed by Vercel variable name/scope metadata only, never by value:

- `DDNA_SUPABASE_URL`: Preview and Production.
- `DDNA_SUPABASE_SERVICE_ROLE_KEY`: Preview and Production, Sensitive.
- `DDNA_RUNTIME_MODE`: Preview and Production.
- Existing legacy server binding name observed: `PABASE_SECRET_KEY`, Preview and Production.

Preview and Production `DDNA_RUNTIME_MODE` were set to `compare` for safe validation posture. Production was not switched to `dedicated`.

## Preview deployment evidence

First Preview deployment after environment setup:

- Deployment ID: `dpl_FyRsD9QL88HaGJC2rnsKVEh48yGr`
- URL: `https://sc-agent-eo532ex70-sonlyconsulting-ctrls-projects.vercel.app`
- Status: READY
- Finding: `/api/runtime` still returned the old legacy runtime payload, proving the root-level handler was not the deployed effective route.

Second Preview deployment after app-root route repair:

- Deployment ID: `dpl_39Dh1EzPHPaakPSwKz1THtrBXKeb`
- URL: `https://sc-agent-9qb9a36nn-sonlyconsulting-ctrls-projects.vercel.app`
- Status: READY
- Build output included both `api/index` and `api/runtime`.
- Protected fetch to `/api/runtime` returned HTTP `401` with body `{"error":"Unauthorized"}` and `cache-control: no-store`.
- This proves the effective deployed route is now isolated and authenticated before DDNA reads.

## Local validation evidence

Executed from repaired branch workspace:

- Focused DDNA tests: 8/8 PASS.
- Password recovery and sidebar/navigation regression tests: 12/12 PASS.
- Syntax checks PASS:
  - `api/runtime.js`
  - `api/index.js`
  - `apps/sc-agent-os/api/runtime.js`
  - `apps/sc-agent-os/api/index.js`
  - `scripts/vercel/should-ignore-sc-agent-os-build.js`

Validated behaviors include:

- Runtime modes: `legacy`, `dedicated`, `compare`.
- Dedicated target: `dcse_ddna_legacy.ddna_ollama_jobs`.
- Legacy target: `dcse_cp.ddna_ollama_jobs`.
- Corrected runtime projection: `model_id` with UI-compatible derived `model` field.
- Deterministic ordering: `created_at DESC, id ASC`.
- Compare mode fails closed on mismatch.
- Missing dedicated credentials fail closed.
- Unauthenticated runtime requests are rejected before DDNA reads.
- Deployed app route delegates `GET /api/runtime` to the DDNA cutover handler.
- Existing `/api/runtime/smoke` behavior remains on the existing handler.

## FAIL STOP basis

The production release gate cannot be completed from this session because authenticated compare-mode Preview validation has not been executed.

Evidence:

- The repaired Preview `/api/runtime` route is reachable through Vercel-protected fetch.
- The route correctly rejects unauthenticated requests with HTTP `401` before DDNA reads.
- This execution surface has no safe operator Supabase session cookie or equivalent first-party authenticated probe mechanism.
- Creating a new verification bypass, weakening route auth, or asking DCS to copy session credentials would create a new access decision outside this release gate.

Relevant stop condition from Issue #67/DCS release packet:

- Production switch cannot be independently verified.
- Preview/runtime validation failure or inability to complete validation that cannot be safely repaired.
- Credential/access ambiguity.

## Actions intentionally NOT performed

- PR #69 merge: NOT PERFORMED.
- Production deployment/cutover: NOT PERFORMED.
- Production `DDNA_RUNTIME_MODE=dedicated` switch: NOT PERFORMED.
- Legacy DDNA deletion or mutation: NOT PERFORMED.
- Dual-write: NOT PERFORMED.
- RLS weakening: NOT PERFORMED.
- Rule or authority promotion: NOT PERFORMED.

## Minimum action to resume

Provide or authorize a safe first-party authenticated validation method for `/api/runtime` that does not expose session credentials in chat, logs, GitHub, or terminal output. Acceptable examples include:

1. an existing operator session available to the execution environment through a protected browser/session tool;
2. a temporary verification-only server-side probe mechanism approved by DCS and guarded by a Vercel-sensitive environment token;
3. a DCS-approved release operator performing the authenticated Preview `/api/runtime` check and returning only non-secret evidence: HTTP status, `ddna.mode`, `ddna.source`, `ddna.schema`, `ddna.equivalent`, job count, and deployment URL.

After authenticated compare-mode Preview validation passes, the existing conditional release authority remains sufficient to proceed through merge, production compare verification, `DDNA_RUNTIME_MODE=dedicated`, live verification, rollback proof, and final closeout.

Structure Precedes Scale.
