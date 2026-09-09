# ESCD / AEGIS AG01 INDEPENDENT REVIEW 001

**Task ID:** DCSE-ESCD-001-REV-AG01-001  
**Parent:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Reviewer:** ChatGPT / DCSE controller  
**Review target:** `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`  
**Source branch:** `feature/aegis-antigravity-slice001`  
**Status:** REVIEW FINDINGS / HARD GATES PRESENT  
**Date:** 2026-09-09

## 1. Preflight

The target commit is verified in GitHub and contains the AG01 Aegis implementation checkpoint, tests, migration, and evidence documents. The review is against the immutable GitHub commit, not the prior Qwen workspace.

The Qwen assignment `DCSE-ESCD-001-QW01` was cancelled by DCS. Qwen's workspace did not contain the target repository/commit, so its blocked output is not implementation evidence for AG01.

## 2. Test execution result

AG's committed evidence reports:

`node --test tests/aegis-slice001.test.js`

with `28 passed / 0 failed`.

This review verifies the committed test source and AG evidence but does not claim an independent local rerun because the ChatGPT execution container cannot network-clone the repository and the GitHub connector is read/review oriented. Therefore:

- AG 28/28 result: VERIFIED AS WORKER EVIDENCE
- independent ChatGPT execution reproduction: NOT PERFORMED
- test quality: independently reviewed below

A green 28/28 suite does not satisfy ESCD release acceptance because multiple security, approval, state, and integration gaps are not exercised by the suite.

## 3. AG failure-classification review

| Failure | AG classification | Independent classification | Disposition |
|---|---|---|---|
| F1 Auth route mismatch | TEST_DEFECT | TEST_DEFECT, but auth requirement remains NOT COVERED | Agree on original failure only |
| F2 Mission route mismatch | TEST_DEFECT | TEST_DEFECT | Agree |
| F3 Briefing mock API shape | TEST_DEFECT | BOTH | Test mismatch existed, but actual scoring-to-briefing integration is also inconsistent |
| F4 scoring strictEqual | TEST_DEFECT | TEST_DEFECT | Agree |
| F5 viewport extraction | TEST_DEFECT | TEST_DEFECT | Agree, underlying viewport markup exists |
| F6 mobile extraction | TEST_DEFECT | TEST_DEFECT | Agree, responsive media rule exists |
| F7 focus extraction | TEST_DEFECT | TEST_DEFECT | Agree, focus-visible rule exists |
| F8 branding extraction | TEST_DEFECT | TEST_DEFECT | Agree, required palette/font tokens exist |
| F9 stale job properties | BOTH | BOTH | Agree, but deterministic clock coverage remains insufficient |
| F10 reproducibility strictEqual | TEST_DEFECT | TEST_DEFECT | Agree on equality assertion, but true reproducibility is still incomplete because the engine reads the live clock internally |

## 4. P0 findings

### P0-01 Unauthenticated privileged API boundary

The server loads `SUPABASE_SERVICE_ROLE_KEY` and uses that key for all PostgREST operations. The API router contains no request authentication or DCS principal verification before session, mission, job, approval, evidence, briefing, NBA, notification, or health handlers run.

The service-role path therefore bypasses database RLS by design while the application layer supplies no compensating authorization gate.

Impact if deployed: callers reaching the endpoint can invoke privileged reads/writes without proving DCS identity.

Required disposition: REPAIR before any migration apply, preview deployment with real data, or connector/runtime integration.

### P0-02 Approval bypass and forged decision authority

The generic job transition state machine allows `waiting_approval -> completed`. The API transition handler does not require an approved approval record before accepting `completed`.

The SPA also renders a waiting-approval job action that calls `transitionJob(jobId, 'completed')` rather than the approval decision endpoint.

Separately, the approval endpoint accepts `decided_by` from request input and defaults it to `DCS`, without verified principal binding.

Impact: approval can be bypassed or represented as a DCS decision without evidence of DCS authorization.

Required disposition: SUPERSEDE with current ESCD autonomy/approval rule set or REPAIR to an equivalent deterministic gate. Hard release gate.

### P0-03 Unauthenticated evidence creation and evidence credibility

The evidence creation endpoint is exposed through the same unauthenticated service-role API and permits callers to create evidence records and linked job events.

Impact: evidence presence cannot be trusted as proof of execution/authority.

Required disposition: REPAIR. Evidence creation must carry verified actor/source provenance and consequence-appropriate verification.

### P0-04 Stored-XSS path in executive UI under current API boundary

Job titles, approval titles, event summaries, and related data are concatenated into HTML strings and assigned through `innerHTML` without demonstrated escaping/sanitization. Job/evidence input is accepted through privileged API endpoints.

With P0-01 present, an external caller could potentially persist markup/script-like content that the executive SPA later renders.

Required disposition: REPAIR by safe DOM rendering or robust escaping, plus authentication/input validation.

## 5. P1 findings

### P1-01 Briefing NBA integration contract mismatch

`getNextBestAction()` returns the scored job object directly. `deriveBriefing()` checks `nextBestAction.job` and then reads `nextBestAction.score` / `reason`.

The API passes the scoring result directly into `deriveBriefing()`.

Result: the briefing's highest-value-next-action section can remain empty even when the NBA endpoint has an actionable result.

Required disposition: REPAIR or SUPERSEDE with current ESCD briefing/NBA contracts.

### P1-02 Briefing cursor mutates on GET rather than acknowledgement

The briefing API updates `last_briefing_at` whenever briefing data is fetched. Current ESCD requires change detection to use persisted acknowledgement/checkpoint state; page refresh must not reset the comparison window.

Impact: opening/refetching the briefing can advance the cursor before DCS acknowledges it and can suppress information on subsequent refresh.

Required disposition: SUPERSEDE/REPAIR.

### P1-03 Completion can occur without evidence

The generic transition handler marks a running or waiting-approval job completed and writes `completed_at` without requiring linked evidence, verified exit criteria, or approval evidence.

This conflicts with current ESCD requirements that consequential completion be evidence-backed and that execution not be inferred from status alone.

Required disposition: SUPERSEDE/REPAIR.

### P1-04 Audit/event write failures are swallowed

Creation, transition, approval, and evidence-linked event writes use `.catch(() => {})` in several places. Primary action success can therefore be returned while the audit/event record failed.

Impact: operational truth can diverge from evidence/history.

Required disposition: REPAIR with transactional/compensating behavior or explicit PARTIAL/FAILED result.

### P1-05 Deterministic NBA is not fully deterministic

`scoreJob()` reads `new Date()` internally for urgency and staleness. Identical logical inputs evaluated at different instants can produce different component values and scores. Current tests call the function back-to-back and therefore do not prove clock-independent reproducibility.

`rankJobs()` sorts only by composite score. Equal scores depend on incoming array order, which is not a governed tie-break contract.

Required disposition: SUPERSEDE with current ESCD deterministic evaluator or REPAIR using injected evaluation time plus explicit tie breaks.

### P1-06 State-model inconsistency around `blocked`

Scoring and briefing code treat `blocked` as a valid job status, and tests create blocked jobs. The SQL `jobs.status` CHECK and API transition state machine do not include `blocked`.

Impact: a behavior heavily referenced by NBA/briefing cannot exist as persisted state under the migration.

Required disposition: RECONCILE against current ESCD WAITING/WATCH/BLOCKED semantics.

### P1-07 RLS test does not prove per-table RLS behavior

Test 10 loops over table names but applies the same global regex for `ENABLE ROW LEVEL SECURITY` each time. It does not verify each named table has RLS or exercise authorized/unauthorized SELECT/INSERT/UPDATE/DELETE.

The API uses service role, so successful server calls would not prove RLS either.

Required disposition: replace with migration-level structural checks plus real database access-matrix tests before any release claim.

### P1-08 Approval-bypass test is syntactic, not behavioral

Test 18 checks only that strings such as `requires_approval`, `approval_type`, and `approved/rejected` appear in the source. It does not attempt a prohibited completion or unauthorized approval and therefore misses P0-02.

Required disposition: add adversarial behavior tests.

### P1-09 Idempotency test does not test idempotency

Test 12 treats a UNIQUE `job_key` and `Date.now()` key generation as duplicate/idempotency proof. Repeated equivalent requests at different milliseconds create different keys and separate jobs. No idempotency key or source-dedupe contract is implemented.

Required disposition: SUPERSEDE/REPAIR under current ESCD dedupe/idempotency rules.

## 6. Likely / conditional runtime findings

### L-01 Custom PostgREST schema routing

The migration creates tables in schema `aegis`, while REST helpers request unqualified `/rest/v1/<table>` and do not show schema profile headers. Unless the Supabase/PostgREST runtime is configured with `aegis` as the active/default exposed profile, runtime calls may not address the intended schema.

Status: LIKELY integration defect, requires runtime configuration verification before classifying P1.

### L-02 Authenticated table grants

The migration grants schema USAGE to `authenticated` and service role but does not visibly grant table privileges to `authenticated`. This may be intentional if all access is mediated server-side, but it means the migration cannot yet be cited as proof of direct authenticated RLS access.

Status: REQUIRES runtime privilege inspection.

## 7. Test-quality findings

The 28 tests provide useful unit/static coverage for:

- module boot
- state-transition model as duplicated in test code
- scoring component presence
- staleness bands
- responsive markup/CSS tokens
- rollback text presence
- route declarations

They do NOT materially prove:

- authenticated DCS principal enforcement
- unauthorized rejection
- RLS access matrix
- service-role mediation safety
- approval bypass prevention
- evidence-backed completion
- event-history durability
- database persistence/restart behavior
- real PostgREST schema routing
- true idempotency/deduplication
- deterministic tie breaks
- briefing acknowledgment cursor behavior
- scoring-to-briefing integration
- stored-XSS resistance
- malformed body behavior across all routes
- concurrent/duplicate transitions

The suite is therefore PARTIAL, not a complete Pass 1 + Pass 2 release test set under current ESCD acceptance standards.

## 8. Required adversarial tests before reuse

1. `AUTH-001`: unauthenticated GET/POST to every `/api/aegis/*` route must fail closed.
2. `AUTH-002`: valid non-DCS authenticated identity must fail all privileged operations.
3. `APP-001`: `waiting_approval -> completed` without an approved matching approval record must fail.
4. `APP-002`: request-supplied `decided_by='DCS'` without verified DCS identity must fail.
5. `EVD-001`: completed consequential job without required evidence must fail.
6. `EVD-002`: failed event/audit write must prevent full-success response or emit explicit partial failure with reconciliation state.
7. `NBA-001`: inject fixed clock; same inputs and evaluation time must produce identical output.
8. `NBA-002`: equal composite scores must resolve through explicit deterministic tie-breaks.
9. `BRF-001`: actual `getNextBestAction()` output passed to `deriveBriefing()` must populate NBA.
10. `BRF-002`: GET/refresh without DCS acknowledgement must not advance briefing cursor.
11. `DB-001`: authorized and unauthorized access matrix for every exposed table.
12. `DB-002`: confirm REST calls address `aegis` schema and not similarly named public objects.
13. `IDEM-001`: same source/idempotency key submitted twice creates one logical job and preserves provenance.
14. `XSS-001`: persisted title/summary containing markup is rendered as text, not executable HTML.
15. `STATE-001`: persisted state model and executable state machine use identical allowed status vocabulary.
16. `CONC-001`: concurrent duplicate transitions cannot produce conflicting terminal states.

## 9. REUSE / REPAIR / REFACTOR / SUPERSEDE / DEFER

| Element | Classification | Reason |
|---|---|---|
| Zero-dependency Vercel serverless pattern | REUSE CANDIDATE | Proven repository pattern, but must inherit real auth/security mediation |
| DCS visual tokens/responsive shell | REUSE | Useful UI baseline; preserve accessibility and sanitize rendering |
| Job/event/evidence table concepts | REUSE/REFACTOR | Useful conceptual entities; reconcile with current ESCD state model and existing Command Post tables |
| `aegis` schema as separate permanent domain | DEFER/REVIEW | Avoid duplicate orchestration/state schemas until current `dcse_cp` reuse analysis is complete |
| 8-factor historical scoring engine | SUPERSEDE/REFACTOR | Current ESCD 54-rule/19-rule-set policy layer defines newer deterministic behavior and routing |
| Briefing formatter/render concepts | REUSE/REPAIR | Useful formatting, but NBA contract and acknowledgement semantics are wrong |
| Generic job transition handler | SUPERSEDE/REPAIR | Approval/evidence gates insufficient |
| Approval endpoint | SUPERSEDE/REPAIR | No verified principal binding, request can self-identify as DCS |
| Evidence endpoint | REPAIR | Provenance/auth verification absent |
| Service-role REST helper pattern | REFACTOR | Server-side placement is correct, but requires authenticated application gate, schema routing, and least-privilege review |
| Employment mission seed/surface | SUPERSEDE/DEFER | DCS Employment is separated from ESCD core |
| Android push stub | DEFER | Device/runtime proof remains later work |
| Google OAuth scaffold | REPAIR | Not merely dashboard configuration; application authorization boundary is not implemented in this checkpoint |
| Existing 28-test suite | REUSE AS BASELINE ONLY | Keep useful tests, add real behavioral/security/integration tests |

## 10. Evidence discrepancy

`ANTIGRAVITY_HANDOFF.md` embeds an earlier short commit SHA while the verified checkpoint is `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`. This is P3 traceability housekeeping caused by amending the commit after writing the handoff. The GitHub target commit is controlling for this review.

## 11. Verified / likely / unknown

### VERIFIED

- target commit exists and contains AG01 implementation/evidence
- API uses server-side service-role key for PostgREST
- no request authentication/principal check is present in the router/handlers reviewed
- CORS permits `*`
- `waiting_approval -> completed` is allowed by transition table
- SPA waiting-approval job action calls direct completion transition
- approval decision accepts request-provided `decided_by`
- evidence creation is exposed through same privileged API
- completion does not require evidence
- event writes can be swallowed on failure
- scoring uses live clock internally
- rank tie break is not explicit
- scoring/briefing support `blocked`, SQL/API state vocabulary does not
- briefing expects a different NBA object shape than scoring returns
- briefing GET updates `last_briefing_at`
- current test suite relies substantially on source-regex/static checks for auth/RLS/approval
- DCS Employment is seeded in historical Aegis but excluded from current ESCD core

### LIKELY

- custom-schema REST routing requires additional profile/runtime configuration
- stored XSS is exploitable if attacker-controlled text reaches current UI, especially while unauthenticated privileged API remains

### UNKNOWN / NOT YET VERIFIED

- live Supabase privileges and exposed-schema configuration
- Google OAuth provider/runtime identity linking
- real RLS behavior against deployed schema
- deployment behavior
- Android push
- production runtime interaction

## 12. Release decision

**AG01 historical checkpoint: NOT ACCEPTABLE FOR DEPLOYMENT OR DIRECT MERGE.**

It remains valuable implementation input. The UI shell, entity concepts, formatting, and some tests are reusable, but current security/authority hard gates require reconciliation before runtime integration.

## 13. Recommendation to Codex / next integration worker

Do not begin with cosmetic Aegis-to-ESCD rename.

Reconcile in this order:

1. adopt current ESCD rule/autonomy/state contracts as controlling behavior;
2. implement verified DCS authentication before any privileged server route;
3. replace approval/completion bypass paths;
4. require evidence-backed consequential completion;
5. repair audit/event failure semantics;
6. reconcile persisted state vocabulary/schema with ESCD and existing `dcse_cp` capabilities;
7. repair deterministic NBA clock/tie-break behavior or use the already-tested ESCD policy engine;
8. repair briefing NBA integration and acknowledgement cursor;
9. add safe rendering/input handling;
10. expand adversarial/RLS/integration tests;
11. only then perform controlled Aegis-to-ESCD refactor and persistence/runtime integration.

**Terminal status:** `REVIEW_FINDINGS_HARD_GATES`
