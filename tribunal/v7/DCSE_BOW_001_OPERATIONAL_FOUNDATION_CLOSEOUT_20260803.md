# BOW-001 Operational Foundation Closeout and Remediation Plan

**Task:** `V7_1_BOW_001_OPERATIONAL_FOUNDATION`  
**Recorded state:** Completed  
**Operational disposition:** `APPROVE_WITH_CORRECTIONS`  
**Purpose:** Establish a governed, observable, recoverable poller foundation without creating a replacement poller.

## Verified result

- The disabled Windows scheduled task was identified as the initial root cause while its trigger remained intact.
- The existing poller was restored and produced live Supabase heartbeat evidence.
- A bounded claim and dispatch cycle completed.
- Commit `e012b098063db05019ee29f0ab7d096ab444e661` supplied the baseline evidence.
- PR #30 merged into the V7.1 governance branch at `0b15bb300b7b7788bb936b69846acbde51be89f7`.
- Review `BOW-001-INDEPENDENT-20260803-CODEX` returned `APPROVE` with confidence `0.97`.
- The accepted rollback disables the scheduled task while preserving logs and evidence.

## Corrections required

Later operation exposed conditions not resolved by the first successful cycle:

- overlapping poller processes;
- rejected scheduler triggers while a prior execution remained active;
- stale child heartbeat despite parent scheduler activity;
- exhausted or invalid provider authentication;
- restrictive task allowlisting;
- incomplete capability-based reassignment.

The follow-up hardening task passed 19 of 19 sandbox tests. PR #35 at `917b3cd8e11a5bdd4eb95a020dc8db83b6cdc389` remains a draft and has not been activated on the Windows host.

## Build plan

1. Reconcile PR #35 with the active governance branch.
2. Enforce one active poller instance with an atomic lease or host mutex.
3. Separate parent scheduler heartbeat, child process heartbeat, and task-result receipt.
4. Replace named-model routing with verified capability and credential routing.
5. Preserve bounded allowlists as policy data rather than temporary hardcoded restrictions.
6. Add provider-failure classification, retry ceiling, reassignment, and terminal evidence.
7. Preserve rollback scripts and logs outside the active process directory.

## Test plan

- Run the existing 19 sandbox tests.
- Prove two overlapping triggers produce one active worker.
- Prove an unavailable provider causes bounded reassignment without duplicate execution.
- Prove stale child heartbeat is detected while parent heartbeat remains fresh.
- Prove a failed task cannot submit a success receipt.
- Prove task idempotency across restart and recovery.
- Run a sustained host test covering multiple scheduler cycles and at least one controlled failure.

## Fix and validation loop

Failed tests create bounded correction tasks linked to the failing assertion. Corrections repeat only the affected tests plus the full regression suite. Chat statements, heartbeat rows, and assignment records cannot substitute for output artifacts and successful receipts.

## Approval and promotion gate

BOW-001 operational hardening is promotable only when:

- PR #35 or its governed successor is reconciled;
- host tests prove clean single-instance behavior;
- credentials recover or reassign without false completion;
- parent and child health signals are distinct;
- rollback succeeds;
- GitHub and Supabase identify the same tested commit and receipt;
- an independent reviewer validates the reconciled evidence.

## Lessons learned

- One successful cycle proves bounded function, not sustained reliability.
- Scheduler liveness and worker success are separate states.
- Provider availability must not become a program-wide stoppage.
- A poller should dispatch only to capabilities that have verified execution access.

## Current gate

**Audit and initial repair complete. Production poller hardening remains pending host activation and validation.**
