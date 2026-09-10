# ESCD TEST PASS 2

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Pass:** Adversarial / regression for workflow orchestration candidate  
**Status:** PASS WITH DECLARED RELEASE-LEVEL LIMITATIONS

## Adversarial controls exercised

The exact-head review suite verifies or statically enforces:

- existing Executive/PA queue, provenance, approval, evidence and completion controls remain green
- all ten planned workflow template types are accepted by the same schema contract
- duplicate step identifiers are rejected
- secret-like template/step content is rejected
- `A3_APPROVAL_REQUIRED` steps cannot omit the approval requirement
- `A4_PROHIBITED` steps cannot define a successful advancement path or run
- child workflow templates cannot weaken inherited approval, evidence, security or rollback controls
- template and instance fingerprints are deterministic
- workflow instances pin exact template ID, version and fingerprint
- approved templates without a governed ESCD job remain plan-only
- runtime workflow authority cannot self-escalate from false to true
- workflow job binding cannot be mutated after instance creation
- workflow and step shortcut transitions are rejected
- dependency readiness is deterministic
- approval-required steps remain blocked until the exact `workflow_step:<step_id>` approval is effective for the same governed job
- expired, wrong-job or wrong-action approval cannot authorize the step at the database layer
- evidence-required steps cannot complete without evidence
- evidence-required workflows cannot complete with unfinished steps or missing evidence
- workflow event history is append-oriented and cannot be modified by the normal authenticated runtime principal
- workflow templates are append/version oriented and cannot be modified by the normal authenticated runtime principal
- workflow UI exposes template/version, status, context, governed job, execution authority, step state, autonomy, approvals, evidence, retry attempts, history and permitted next actions
- dedicated workflow operator UI exercises Start, Resume, Retry, Complete and bounded step transitions through the governed API surface
- candidate ESCD API routing is specific before the generic API fallback
- workflow-aware handler reuses the existing authenticated DCS operator boundary and does not introduce a service-role runtime path
- no DDNA runtime cutover or DCS Employment logic is bundled into this tranche

## Exact-head regression result

GitHub Actions run `34428703272` completed successfully on branch head `403bc9ecc1c01a44acf5e373a60f6b68b7b4926f` before evidence-only closeout commits.

Results:

- **181 Python tests passed**
- **10 subtests passed**
- ESCD Python/API compile: PASS
- isolated PostgreSQL 17 bootstrap: PASS
- full current candidate migration chain: PASS
- runtime SQL behavior: PASS
- Executive/PA SQL behavior: PASS
- structured source-link behavior: PASS
- workflow orchestration and authority behavior: PASS

## Limits of this pass

This is adversarial validation of the repository-level workflow candidate, including UI contract and API routing. It is not a production E2E certification.

Still required before final release validation can be justified:

- deployed authenticated browser execution of the actual ESCD UI
- live persistence validation against the authorized ESCD database target after production/pre-production migration approval
- live connector/provider journeys needed by the release matrix
- mobile/device checks where release claims depend on them
- final DDNA integration validation after the current Codex hold is released

No production migration, deployment or connector write was performed by this tranche.
