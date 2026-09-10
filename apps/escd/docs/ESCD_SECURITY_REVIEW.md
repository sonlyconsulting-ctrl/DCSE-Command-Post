# ESCD SECURITY REVIEW

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Scope:** Workflow orchestration + operator UI candidate

## Candidate security result

PASS for the WORKFLOW-004 candidate scope, subject to final deployed-browser and live-integration validation.

## Preserved controls

- existing caller Supabase JWT and DCS operator authorization boundary remains the runtime entry gate
- no normal workflow path uses a service-role secret
- workflow persistence is protected by candidate RLS and least-privilege grants
- template identity/version is immutable after use through versioned records and fingerprint conflict detection
- child templates cannot weaken parent approval, evidence, security or rollback controls
- template presence alone does not authorize execution
- approved templates still require a governed ESCD job binding for executable workflow state
- A4 prohibited steps cannot execute
- approval-required steps require an approved, unexpired approval on the same governed job with exact `workflow_step:<step_id>` binding
- evidence-required completion fails closed without evidence references
- workflow events remain append-oriented
- the operator UI exposes state and controls but does not create a parallel bypass around API/database authority
- external Gmail, Calendar, publish, spending, destructive and credential operations remain outside autonomous workflow execution

## Held/unverified

- DDNA integration is held pending Codex
- production DDL and deploy are not authorized
- deployed browser authorization and real-session state propagation remain to be proven
- live connector write behavior is not claimed
- production rollback execution is not yet rehearsed

## Release implication

A green backend gate is necessary but not sufficient for final product release. Final security acceptance must include the authenticated operator UI against the deployed candidate so route protection, browser token handling, approval surfaces, errors and evidence visibility are exercised through the real product path.

Current disposition: `CANDIDATE SECURITY PASS / FINAL RELEASE SECURITY PENDING`.
