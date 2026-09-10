# ESCD SECURITY REVIEW

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Status:** PASS FOR CANDIDATE TRANCHE

## Security posture retained

- API continues to authenticate with the caller Supabase bearer JWT and authorize the DCS operator.
- Normal ESCD runtime remains user-scoped and does not introduce `SUPABASE_SERVICE_ROLE_KEY`.
- Workflow candidate tables use RLS and FORCE RLS.
- Principal-bound insert policies continue to use `auth.uid()`.
- Workflow event history and template definitions are append/version oriented for the normal authenticated runtime principal.
- Workflow template presence does not grant execution authority.
- Approved workflow templates remain plan-only unless the instance is bound to an existing governed ESCD job.
- Runtime cannot self-escalate `execution_authorized` from false to true.
- Workflow job, template, version, fingerprint and step-contract bindings are immutable after creation.
- Child workflow templates cannot weaken inherited approval, evidence, security or rollback controls.
- `A4_PROHIBITED` workflow steps cannot run.
- `A3_APPROVAL_REQUIRED` or otherwise approval-required workflow steps require an exact effective approval whose action key is `workflow_step:<step_id>` and whose job matches the workflow's governed job.
- Expired, wrong-action and wrong-job approvals fail closed at the database layer.
- Evidence-required steps and workflows cannot complete without required evidence.
- Candidate workflow UI actions call the governed authenticated API rather than a parallel privileged path.
- No DDNA runtime/cutover behavior or DCS Employment-specific logic was added.

## UI security posture

The workflow UI exposes operational state needed by DCS without embedding credentials or granting direct database access. It shows template/version, execution status, governed job, step autonomy, approval/evidence requirements, attempts and history. Consequential workflow actions remain subject to server-side and database-side authority enforcement. Client-side disabled buttons are usability controls only and are not treated as security boundaries.

## Regression protections

The complete suite continues to cover the earlier authorization, approval, evidence, briefing, provenance and completion controls while adding workflow-specific adversarial checks for:

- control weakening
- self-escalation
- jobless execution
- mutable version/job binding
- prohibited step execution
- approval bypass
- evidence bypass
- lifecycle shortcuts
- history/template mutation
- API routing regression
- workflow UI/backend disconnect

## Exact-head candidate evidence

GitHub Actions run `34428703272` passed on workflow/UI code head `403bc9ecc1c01a44acf5e373a60f6b68b7b4926f` before evidence-only documentation commits. It executed 181 Python tests plus 10 subtests and the complete isolated PostgreSQL behavior suite.

## Release caveat

This security review validates repository-level candidate behavior only. Production/pre-production RLS application, deployed browser authentication, live provider security boundaries and any device/mobile claims require separate release evidence before production use.
