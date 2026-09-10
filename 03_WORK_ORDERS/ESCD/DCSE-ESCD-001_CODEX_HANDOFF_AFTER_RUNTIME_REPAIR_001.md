# Codex Handoff After ESCD Runtime Repair 001

**Task ID:** DCSE-ESCD-001-RUNTIME-001  
**Parent:** DCSE-ESCD-001  
**Branch:** `feature/escd-runtime-repair-001`  
**PR:** #72  
**Historical AG01 evidence:** `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`  
**Status:** READY FOR INDEPENDENT REVIEW, NOT RELEASE

## Resume rule

Start from the current remote branch head and inspect live GitHub state before modifying anything. Preserve the historical AG01 checkpoint and all accepted ESCD contracts. Do not reset, clean, mass-rename, merge, deploy, or apply production DDL as part of review.

## Current independent hardening delta

ChatGPT/DCSE controller performed a bounded follow-on review and repaired confirmed integrity gaps without changing the product architecture:

- future/regressive briefing acknowledgement is rejected
- completion no longer trusts request-body exit-criteria assertion
- runtime reads use deterministic tie breaks
- approvals are looked up by exact transition action key
- expired approvals fail closed
- approval records include action key, optional payload fingerprint, expiration, and conditions
- job status transitions write append-oriented history events
- approval status transitions write append-oriented history events
- RLS write checks bind provenance identities to the authenticated principal
- no service-role runtime dependency introduced

Review artifact:
`03_WORK_ORDERS/ESCD/DCSE-ESCD-001_CHATGPT_RUNTIME_REVIEW_DELTA_001.md`

## Required independent review

1. Re-run the complete ESCD pure-policy and runtime/security tests from the current remote head.
2. Compile/syntax-check all modified Python.
3. Review the candidate SQL migration for syntax, RLS behavior, trigger behavior, approval binding, event-history behavior, rollback, and dependency assumptions.
4. Adversarially test approval bypass, stale/expired approval, wrong action key, forged provenance identity, future/regressive briefing acknowledgement, client-asserted exit criteria, missing evidence, and invalid lifecycle transitions.
5. Confirm no Aegis hard-gate defect was reintroduced.
6. Confirm DCS Employment logic remains outside ESCD core.
7. Confirm DDNA production consumer cutover remains separate.
8. Verify the governed write path for setting persisted `exit_criteria_met`; if absent, keep completion fail-closed and disposition this as the next implementation requirement rather than weakening the gate.

## Known external blockers

- Vercel account has reached its daily deployment limit. Do not treat Vercel quota failures as ESCD code failures.
- Supabase Git Preview currently fails earlier in the repository migration chain because schema `family_vow_go` is missing. Do not repair unrelated historical migration architecture inside this ESCD review unless separately authorized.
- No GitHub Actions workflow currently executes this branch, so lack of CI evidence must remain explicit.

## Exit

Return one of:

- `REVIEW_PASS_READY_FOR_NEXT_TRANCHE`
- `REVIEW_FINDINGS_REPAIR_REQUIRED`
- `BLOCKED`

Do not use production-ready language without fresh evidence. Do not merge or deploy.

Structure Precedes Scale.
