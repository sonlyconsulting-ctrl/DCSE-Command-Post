# DCSE V7.1 Strict Runtime Rerun Plan for BOW-001 through BOW-004

Date: 2026-08-03  
Execution mode: MP-Full  
Authority: V7.1 only

## Baseline preservation

All original tasks, commits, pull requests, reports, receipts, poller logs, and Supabase rows become immutable Baseline Set A. They are not deleted, overwritten, or represented as V7.1-compliant. The new executions are Baseline Set B and use distinct task keys and output paths.

## Rerun set

| Rerun key | Purpose | Mandatory doctrine route | Conditional doctrine route | Explicit exclusion |
|---|---|---|---|---|
| V7_1_RERUN_BOW_001_STRICT_RUNTIME | poller hardening, single-instance execution, credential preflight, heartbeat, dispatch and recovery | D01,D02,D03,D04,D05,D06,D15,D17,D20,D21,D22 | none | D13,D14 |
| V7_1_RERUN_BOW_002_STRICT_RUNTIME | true CTJ audit and inventory, preserving the prior registry audit as separate usable baseline evidence | D01,D02,D03,D04,D05,D06,D07,D08,D09,D10,D11,D15,D16,D17,D20,D21,D22 | D12,D18,D19 when CTJ media or visual assets are in scope | D13,D14 |
| V7_1_RERUN_BOW_003_STRICT_RUNTIME | TSL production-readiness audit with retrievable evidence across architecture, code, database, auth, security, deployment, sports data, UX and commercial readiness | D01,D02,D03,D04,D05,D06,D07,D08,D09,D10,D11,D15,D16,D17,D20,D21,D22 | D12,D18,D19 for tested media or visual assets | D13,D14 |
| V7_1_RERUN_BOW_004_STRICT_RUNTIME | CTJ build, test and remediation planning from the validated BOW-002 audit, without duplicating the audit | D01,D02,D03,D04,D05,D06,D07,D08,D09,D10,D11,D15,D16,D17,D20,D21,D22 | D12,D18,D19 for implemented media or visual work | D13,D14 |

## Required execution path for every rerun

1. Authority and startup: load the V7.1 manifest and verify canonical branch and hashes.
2. Doctrine routing: run D21 DDR and create a DCL containing every doctrine considered, activated, excluded, and why.
3. Immutable baseline: link Baseline Set A without altering it.
4. Readiness Stop-Gate: verify access, credentials, single-instance runtime, target identity, required inputs, output paths and rollback plan.
5. Discovery: use D01, D02 and D17 to test both expected and adversarial conditions.
6. Bounded execution: perform only the declared BOW scope and record commands, database operations and file changes.
7. Testing: execute doctrine-specific tests plus negative, authorization, idempotency, schema and recovery tests where applicable.
8. Evidence: require nonempty retrievable artifacts, hashes, timestamps, heartbeat and delivery acknowledgement.
9. Independent validation: select by capability, preserve reviewer accountability, and fall back without stopping solely for model unavailability.
10. Pass-Gate: apply D05 and D20 phase criteria. Findings may be accepted only with named corrections, owner, deadline and risk disposition.
11. Promotion and rollback: reconcile GitHub, Supabase and runtime state, then emit promotion and rollback receipts.
12. Lessons learned: update the violation register and executable doctrine gaps without silently rewriting historical evidence.

## Non-stoppage rule

The poller automatically progresses routine work when the current phase receipt passes. It may retry transient failures and select another capable runtime. It stops only for a DCS-reserved decision, a security or destructive-action risk, missing authoritative input, failed integrity check, or an exhausted bounded retry policy. A named model being unavailable is a fallback event, not a Stop-Gate.

## Completion criteria

A BOW is complete only when:

- its DCL is complete;
- every required output exists and is nonempty;
- test results and source hashes are retrievable;
- review and gate receipts identify the accountable runtime;
- rollback is defined and tested where feasible;
- GitHub and Supabase states reconcile;
- the final disposition is PASS, PASS_WITH_CORRECTIONS, FAIL, or INSUFFICIENT_EVIDENCE;
- the next BOW is released automatically after a passing gate when dependencies are satisfied.

## Scope clarification

The earlier BOW-002 asset-registry reconciliation remains operationally useful as a baseline registry defect report. It does not satisfy the intended CTJ audit. Under this rerun set, BOW-002 performs the true CTJ audit and BOW-004 consumes that validated audit for build, test, fix and promotion planning.
