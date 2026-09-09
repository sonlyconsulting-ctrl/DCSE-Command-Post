# ESCD QWEN AG01 REVIEW ADJUDICATION 001

**Task ID:** DCSE-ESCD-001-ADJ-QW01  
**Parent:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Adjudicator:** ChatGPT / DCSE controller  
**Qwen review target:** `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`  
**Current repair branch:** `feature/escd-runtime-repair-001`  
**Status:** ADJUDICATED / QWEN FINDINGS PARTIALLY ACCEPTED

## 1. Executive disposition

Qwen successfully reproduced the AG01 28/28 test result and correctly validated several historical test repairs. That is useful corroborating evidence for the narrow proposition that the committed AG01 test suite passes.

Qwen's broader conclusion that AG01 is technically sound with no P0/P1 defects is NOT accepted. It conflicts with verified code behavior and with the current ESCD security/authority contract.

The current controlling implementation direction remains the repaired ESCD runtime candidate on `feature/escd-runtime-repair-001`, not the historical AG01 checkpoint.

## 2. Accepted Qwen findings

Accepted:

- 28/28 historical AG01 tests pass at the target checkpoint.
- Most original AG test failures were test defects.
- Responsive shell, branding, viewport, focus-visible styles, rollback text, and several route declarations exist.
- Explicit scoring tie-breaks were absent in historical AG01.
- Live RLS behavior was not proven by AG01's original static test suite.
- Actual mobile-device rendering and production deployment remained unverified.
- AG01 is appropriate as historical input for Codex reconciliation, not as a direct production release.

## 3. Rejected Qwen security conclusion: service role plus RLS

Qwen states the absence of per-request user validation is acceptable if RLS is configured and characterizes authorization bypass risk as low.

That conclusion is incorrect for AG01's architecture.

AG01 loads `SUPABASE_SERVICE_ROLE_KEY` and uses it for server-side PostgREST requests. Service-role requests bypass RLS. Therefore the existence of RLS policies does not protect an unauthenticated caller who can invoke the server route. The server must authenticate and authorize the caller before using privileged database authority.

AG01 contains no such request identity gate before privileged handlers. This is a P0 authority/security defect if the endpoint were deployed with live privileged credentials.

The repaired ESCD runtime candidate removes the service-role dependency from the normal request path and verifies DCS identity before user-JWT-scoped PostgREST access.

## 4. Rejected Qwen approval conclusion

Qwen characterizes approval bypass risk as low and states the approval route relies on RLS.

Verified AG01 behavior contradicts that conclusion:

- generic job transition allows `waiting_approval -> completed`;
- the waiting-approval UI action calls direct job completion;
- job completion does not require an approved matching approval record;
- `decided_by` is supplied by the request and defaults to `DCS` without verified principal binding.

This is a hard approval-authority defect under current ESCD rules. The repaired candidate blocks this path and requires verified approval plus evidence/exit criteria before consequential completion.

## 5. Rejected Qwen determinism conclusion

Qwen states the scoring engine has no time-dependent operations and is deterministic.

Historical `scoreJob()` calls `new Date()` internally for deadline and staleness calculations. Identical business inputs evaluated across a time boundary can produce different results. Back-to-back test equality is not proof of deterministic reproducibility.

Current ESCD Next Best Action logic uses explicit deterministic factors and governed tie-breaks. The historical eight-factor Aegis scorer is not controlling.

## 6. Rejected Qwen briefing conclusion

Qwen accepts the historical briefing integration as verified.

Verified code contract mismatch exists:

- historical `getNextBestAction()` returns the scored job object directly;
- historical `deriveBriefing()` expects `nextBestAction.job` plus separate `score` and `reason` properties;
- the API passes the scoring result directly into briefing derivation.

Thus the Next Best Action section can be empty despite an actionable result.

Additionally, historical briefing GET advances `last_briefing_at`, meaning a refresh can move the comparison cursor without explicit DCS acknowledgement. Both behaviors were repaired in the ESCD runtime candidate.

## 7. Rejected Qwen evidence/idempotency sufficiency

AG01's passing tests do not prove:

- evidence-backed completion;
- trustworthy evidence provenance;
- durable audit/event recording;
- logical request idempotency;
- real RLS access matrix;
- unauthorized API rejection;
- concurrent transition safety.

A UNIQUE generated job key is not equivalent to idempotency. Static regex presence of RLS/approval strings is not behavioral enforcement evidence.

## 8. Supabase/RLS live evidence after AG01

Subsequent read-only live checks against the existing `dcse_cp` authorization foundation established:

- anonymous access to `dcse_cp` is denied;
- an authenticated non-DCS subject sees zero active operator rows;
- the active DCS operator subject sees one operator row;
- `dcse_cp.is_dcs_owner()` is backed by `operator_accounts`, `auth.uid()`, active status, and approved access scopes.

This validates the existing Command Post identity/RLS foundation. It does not retroactively validate AG01's service-role API boundary.

## 9. Current controlling status

The 1-9 runtime repair/reconciliation tranche is implemented on:

`feature/escd-runtime-repair-001`

Draft PR:

`#72 ESCD runtime repair 001: auth, approval/evidence gates, RLS candidate, Next Best Action integration`

The repair candidate includes:

- authenticated DCS API boundary;
- user-JWT-scoped PostgREST path;
- approval/evidence/exit-criteria hard gates;
- safe persisted-content rendering;
- governed ESCD Next Best Action adapter;
- explicit briefing acknowledgement;
- candidate `dcse_cp.escd_*` persistence/RLS migration;
- adversarial runtime/security tests;
- AG01 reconciliation evidence.

Current status remains:

`READY_FOR_CODEX_REVIEW`

## 10. Codex instruction

Codex should treat Qwen's 28/28 reproduction as corroborating historical test evidence, but should NOT adopt Qwen's no-P0/P1 security conclusion.

Codex should review the repaired ESCD runtime candidate in PR #72 against the operative ESCD contracts and independently challenge:

1. authentication and DCS principal binding;
2. RLS and PostgREST JWT behavior;
3. approval/evidence completion gates;
4. persistence transition constraints;
5. safe rendering;
6. Next Best Action integration;
7. briefing acknowledgement semantics;
8. adversarial tests;
9. Aegis-to-ESCD reconciliation decisions.

## 11. Terminal disposition

`QWEN_REVIEW_PARTIALLY_ACCEPTED`

Historical test reproduction: ACCEPTED.  
No-P0/P1 security conclusion: REJECTED.  
Current repair/codex handoff status: `READY_FOR_CODEX_REVIEW`.
