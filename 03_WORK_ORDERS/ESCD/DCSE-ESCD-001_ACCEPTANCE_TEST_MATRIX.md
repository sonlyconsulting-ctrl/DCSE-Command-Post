# ESCD ACCEPTANCE TEST MATRIX

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Release rule

No ESCD tranche is accepted by narrative assertion. Evidence must demonstrate the requirement against the implemented surface. Overall target remains >=95/100 with no failed security, governance, authority, data-integrity, or rollback hard gate.

DCS Employment is excluded from ESCD core acceptance and is governed separately under `DCS-EMPLOYMENT-BUILD-001`.

## Test domains

| Domain | Required evidence |
|---|---|
| Identity/Auth | authorized principal access, linked identity behavior if implemented, unauthorized denial |
| Persistence | task/job/approval/session state survives reload/restart |
| RLS/Security | cross-principal denial, server-side secrets, view/RPC review, no browser privileged key |
| Intake/Dedupe | duplicate source items link without losing provenance |
| Task lifecycle | valid transitions, invalid transition rejection, history retained |
| Jobs | queue/run/waiting approval/complete/fail/cancel/archive behavior |
| NBA | deterministic repeated results, ties, blocked routing, DCS override, factor transparency |
| Briefing | correct delta since acknowledgement, empty state, completion evidence, blockers |
| Approvals | no bypass, approve/reject/defer/expire, exact action scope preserved |
| Evidence | consequential action linked to receipt/source/result |
| Calendar | overlap/buffer conflicts, no silent commitment changes, meeting-prep behavior |
| Communications | triage, dedupe, draft behavior, no unapproved external send |
| Person Context | provenance, source separation, no sensitive inference |
| Workflow Templates | valid type/version/step contract, inheritance does not weaken controls |
| MAKE/FIX/RELEASE | distinct gates, baselines, regression/rollback, release approval |
| Notifications | dedupe, escalation, acknowledgement, failed delivery, no false delivery claims |
| Routines | idempotent run, duplicate trigger, pause, missed run, failure/recovery |
| Connectors | unavailable, stale, permission denied, source conflict, correct routing |
| Failure recovery | bounded retry, uncertain side effect check, dead-letter/review, restart reconciliation |
| Mobile | pending-until-ack, consequence confirmation, evidence-backed completion |
| DDNA boundary | governed reads; candidate contribution cannot self-promote |
| Regression | SC Agent OS/Command Post behaviors touched by implementation remain valid |
| Rollback | documented and reproducible rollback/checkpoint for material changes |

## Pure policy layer test gate

Before persistence/runtime integration, the deterministic ESCD policy layer must prove:

- rule IDs unique
- rule-set registry valid
- NBA weights total 100 percent
- autonomy A0-A4 behavior
- queue routing and state transition validity
- source precedence/conflict preservation
- calendar/communications/person-context rules
- workflow-template and MAKE/FIX/RELEASE controls
- bounded retry/recovery rules
- notification/routine/mobile rules
- DDNA candidate-only boundary
- completion/evidence rules

Current pure policy evidence is recorded in `apps/escd/docs/ESCD_POLICY_TEST_REPORT.md`.

## Two-pass discipline

### Pass 1: functional/integration
Run syntax/build, unit/component, persistence, state transitions, auth/RLS, connector abstraction, jobs, approvals, evidence, and main happy-path integrations. Repair every P0/P1/security/governance defect.

### Pass 2: adversarial/E2E/regression
Run desktop/mobile journeys, reload/restart, duplicate/idempotency, stale jobs, permission escalation, approval bypass attempts, uncertain writes, failure/retry/recovery, regression, and rollback proof.

## Required end-to-end journeys

1. Capture a pin -> dedupe/classify -> task -> NBA -> complete -> evidence -> briefing.
2. Communication -> triage -> draft/proposal -> approval when consequential -> verified send/write receipt when authorized.
3. Calendar event set -> conflict detection -> proposed resolution -> no silent external modification.
4. Delegated internal job -> run -> fail transiently -> bounded retry -> verified completion.
5. Consequential action -> approval -> reject -> ensure no execution.
6. Connector unavailable -> preserve state -> route WAITING/WATCH -> recover.
7. Session reload -> briefing delta remains based on persisted acknowledgement cursor.
8. MAKE/FIX workflow -> validation -> test evidence -> RELEASE remains separately gated.
9. DDNA candidate -> provenance -> candidate state -> verify no authority promotion.

## Defect severity

- P0: security/authority/data-loss/secret/protected-lane or destructive uncontrolled behavior. Hard fail.
- P1: core workflow broken, approval bypass, persistence failure, materially wrong NBA/briefing. Hard fail until repaired.
- P2: important but bounded functional/usability defect. Must be dispositioned before release.
- P3: cosmetic/non-material backlog candidate.

## Evidence package

Each tranche closeout records commit SHA, changed files, tests/commands, pass/fail counts, defects repaired/open, security/RLS result, rollback reference, VERIFIED/LIKELY/UNKNOWN, and release score.
