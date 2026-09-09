# ESCD FAILURE AND RECOVERY MODEL

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Principle

Failure must become inspectable state, not hidden retries or optimistic completion. Recovery should preserve evidence and avoid duplicate side effects.

## Failure classes

- **F1 Input/Data:** missing, malformed, stale, contradictory, or insufficient source data.
- **F2 Connector:** unavailable, auth expired, permission denied, timeout, rate limit.
- **F3 Execution:** tool/model/runtime error, test failure, invalid output.
- **F4 Authorization:** approval missing/expired/rejected or autonomy class mismatch.
- **F5 Security/Governance:** secret exposure risk, RLS failure, protected-lane conflict, authority conflict.
- **F6 External Side Effect Uncertain:** send/write/deploy may have occurred but confirmation is absent.
- **F7 Dependency:** waiting on person/system/event.

## Recovery rules

1. Record failure event with exact stage, source, error class, attempted action, and evidence.
2. Determine whether retry is safe and idempotent.
3. Use bounded retries only for transient F2/F3 cases.
4. Never retry an uncertain external side effect until actual target state is checked.
5. F4 routes to APPROVAL/WAITING.
6. F5 hard-stops execution and escalates.
7. F7 routes to WAITING/WATCH with explicit trigger.
8. After retry budget exhaustion, create a concise blocker with smallest required action.

## Retry contract

Retry policy records max attempts, backoff, idempotency key, last error, next attempt, and terminal condition. Retry counters survive restart.

## Recovery after restart

On startup, reconcile jobs left in `running` against executor evidence. Do not automatically mark them failed or rerun. Classify as completed, failed, waiting, or uncertain based on evidence.

## Rollback

Consequential workflows should define rollback/reversal where technically possible before execution. Rollback itself is an action subject to authorization and evidence.

## Dead-letter handling

Repeatedly failing jobs leave active execution and enter a review/dead-letter state with source payload reference, errors, retry history, and proposed remediation. They do not silently disappear.

## Acceptance

Test connector timeout, auth expiration, model failure, approval expiry, RLS denial, uncertain send, interrupted process, duplicate retry, restart recovery, dead-letter routing, and rollback evidence.