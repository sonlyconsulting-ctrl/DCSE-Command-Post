# ESCD Current-Head Validation Queue

**Task ID:** DCSE-ESCD-001  
**PR:** #72  
**Branch:** `feature/escd-runtime-repair-001`  
**Verified head:** `d8d74d83d22dcc319049df594091d7e435cd0368`  
**Status:** REVIEW GATE

## Scope lock

Validate the current assistant-core repair. Do not restart discovery, restore superseded Aegis behavior, add DCS Employment logic, bundle DDNA production cutover, repair unrelated historical migrations, or perform production release.

## Pass 1

- run complete ESCD pure-policy tests
- run current runtime/security tests
- compile/syntax-check modified Python
- inspect candidate SQL syntax and dependencies
- verify authenticated/unauthenticated RLS behavior on an approved non-production target if available
- verify deterministic NBA and runtime ordering
- verify persisted briefing acknowledgement semantics
- verify job and approval event history

## Pass 2

Adversarially prove rejection of:

- unauthorized principal access
- service-role dependency in normal request path
- client-asserted exit-criteria completion
- completion without evidence
- wrong-action approval reuse
- expired/stale approval reuse
- forged provenance actor/requester IDs
- future or regressive briefing acknowledgement
- invalid state transitions
- unsafe persisted-content rendering

## Required disposition before next tranche

The persisted `exit_criteria_met` field now fails closed. A governed verification write path must be implemented and tested before the full completion journey can pass. Do not weaken this gate to satisfy a happy-path test.

## External blockers to isolate, not absorb

- Vercel daily deployment quota exhaustion
- Supabase Git Preview historical migration failure on missing `family_vow_go` schema
- no branch GitHub Actions workflow currently provides current-head CI evidence

## Exit

`REVIEW_PASS_READY_FOR_NEXT_TRANCHE`, `REVIEW_FINDINGS_REPAIR_REQUIRED`, or `BLOCKED`.

Structure Precedes Scale.
