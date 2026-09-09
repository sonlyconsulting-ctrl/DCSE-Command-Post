# ESCD ACCEPTANCE TEST MATRIX

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Release rule

No ESCD tranche is accepted by narrative assertion. Evidence must demonstrate the requirement against the implemented surface. Overall target remains >=95/100 with no failed security, governance, authority, data-integrity, or rollback hard gate.

## Test domains

| Domain | Required evidence |
|---|---|
| Identity/Auth | authorized principal access, backup identity behavior if implemented, unauthorized denial |
| Persistence | task/job/approval/session state survives reload/restart |
| RLS/Security | cross-principal denial, server-side secrets, view/RPC review, no browser privileged key |
| Intake/Dedupe | duplicate source items link without losing provenance |
| Task lifecycle | valid transitions, invalid transition rejection, history retained |
| Jobs | queue/run/waiting approval/complete/fail/cancel/archive behavior |
| NBA | deterministic repeated results, ties, blocked routing, DCS override, revenue relevance |
| Briefing | correct delta since acknowledgement, empty state, completion evidence, blockers |
| Approvals | no bypass, approve/reject/defer/expire, exact action scope preserved |
| Evidence | consequential action linked to receipt/source/result |
| Employment | opportunity intake through submission/follow-up with unsupported claim rejection |
| Notifications | dedupe, escalation, acknowledgement, failed delivery, no false delivery claims |
| Routines | idempotent run, duplicate trigger, pause, missed run, failure/recovery |
| Connectors | unavailable, stale, permission denied, source conflict, correct routing |
| Failure recovery | bounded retry, uncertain side effect check, dead-letter/review, restart reconciliation |
| UI/Accessibility | desktop/mobile, keyboard/focus, error/empty/loading, readable responsive layout |
| Command Post reuse | existing capabilities reused without duplicating/weakening governance |
| DDNA boundary | governed reads; candidate contribution cannot self-promote |
| Regression | SC Agent OS/Command Post behaviors touched by implementation remain valid |
| Rollback | documented and reproducible rollback/checkpoint for material changes |

## Two-pass discipline

### Pass 1: functional/integration
Run syntax/build, unit/component, persistence, state transitions, auth/RLS, connector abstraction, jobs, approvals, evidence, and main happy-path integrations. Repair every P0/P1/security/governance defect.

### Pass 2: adversarial/E2E/regression
Run desktop/mobile journeys, reload/restart, duplicate/idempotency, stale jobs, permission escalation, approval bypass attempts, uncertain writes, failure/retry/recovery, regression, and rollback proof.

## Required end-to-end journeys

1. Capture a pin -> dedupe/classify -> task -> NBA -> complete -> evidence -> briefing.
2. Employment opportunity -> fit -> package draft -> DCS approval -> submission receipt -> follow-up watch.
3. Delegated internal job -> run -> fail transiently -> bounded retry -> verified completion.
4. Consequential action -> approval -> reject -> ensure no execution.
5. Connector unavailable -> preserve state -> route WAITING/WATCH -> recover.
6. Session reload -> briefing delta remains based on persisted acknowledgement cursor.
7. DDNA candidate -> provenance -> candidate state -> verify no authority promotion.

## Defect severity

- P0: security/authority/data-loss/secret/protected-lane or destructive uncontrolled behavior. Hard fail.
- P1: core workflow broken, approval bypass, persistence failure, materially wrong NBA/briefing. Hard fail until repaired.
- P2: important but bounded functional/usability defect. Must be dispositioned before release.
- P3: cosmetic/non-material backlog candidate.

## Evidence package

Each tranche closeout records commit SHA, changed files, tests/commands, pass/fail counts, defects repaired/open, security/RLS result, rollback reference, VERIFIED/LIKELY/UNKNOWN, and release score.