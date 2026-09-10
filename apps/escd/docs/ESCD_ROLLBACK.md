# ESCD ROLLBACK PLAN

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Scope:** Workflow orchestration + operator UI candidate

## Current posture

No production migration, deployment or merge is authorized. The current rollback boundary is therefore branch-level and candidate-database only.

## Branch rollback

If WORKFLOW-004 must be withdrawn before release:

1. Preserve the current validated branch SHA and evidence.
2. Revert only the workflow orchestration/UI commits or restore the last validated Executive/PA checkpoint.
3. Do not rewrite or delete prior runtime evidence/history.
4. Re-run the ESCD Review Gate after the revert.

## Candidate database rollback

The workflow candidate migrations must not be applied to production without explicit DCS release authorization. In a disposable validation database, rollback may drop workflow-specific tables/triggers/functions only after confirming no unrelated state depends on them.

The workflow persistence boundary includes the workflow template, instance, step and event objects introduced for WORKFLOW-004. The exact rollback SQL must be reviewed against the applied migration set at release time rather than assuming a stale object list.

## UI rollback

The operator workflow surface is additive to the existing ESCD interface. If a release candidate fails browser validation, revert the workflow UI changes together with their API/runtime dependencies rather than leaving a visible control surface pointed at missing workflow endpoints.

## Production release condition

A production rollback plan is not considered proven until a non-production deployed candidate has completed an authenticated browser journey, migration apply, representative workflow execution/proposal path, and rollback rehearsal. DDNA remains outside this rollback scope while held for Codex.

Current disposition: `ROLLBACK PLAN DEFINED / PRODUCTION REHEARSAL PENDING`.
