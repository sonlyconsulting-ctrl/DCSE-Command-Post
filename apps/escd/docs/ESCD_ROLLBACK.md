# ESCD ROLLBACK

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Status:** DOCUMENTED / NOT EXECUTED AGAINST PRODUCTION

## Current safety fact

No production ESCD migration, deployment or PR merge was performed in this tranche. The workflow implementation remains a candidate branch change. Rollback therefore means repository-level reversion of the workflow tranche only, not destructive database rollback.

## Repository rollback boundary

`WORKFLOW-004` is additive to the previously validated ESCD runtime and Executive/PA candidate. If this tranche is rejected before release, revert only the workflow-specific changes introduced after the completed Executive/PA checkpoint. Do not reset or discard the previously validated authentication, approval, evidence, briefing, job-verification, Executive Stream or PA work.

Workflow-specific additions include:

- `apps/escd/runtime/workflow_engine.py`
- `apps/escd/runtime/workflow_repository.py`
- `apps/escd/runtime/workflow_api.py`
- `apps/escd/api/workflow_index.py`
- `api/escd.py`
- workflow UI changes in `apps/escd/web/index.html`
- `apps/escd/web/workflows.html`
- workflow tests and UI-surface regression tests
- `supabase/migrations/20260910_escd_workflow_engine.sql`
- `supabase/migrations/20260910_escd_workflow_authority_patch.sql`
- specific candidate ESCD routing additions in `vercel.json`
- workflow additions to `.github/workflows/escd-review.yml`

## Candidate database rollback boundary

The workflow migrations are not authorized for production application. If they are later applied to an authorized non-production or production target, rollback must first inventory dependent workflow records and preserve evidence.

Candidate workflow objects include:

- `escd_workflow_templates`
- `escd_workflow_instances`
- `escd_workflow_steps`
- `escd_workflow_events`
- workflow indexes, RLS policies and lifecycle/authority triggers associated with those objects
- governed-job binding column/index added by the authority patch

Do not drop workflow objects after data exists without explicit destructive-action authorization and an evidence-preservation plan.

## Runtime/UI rollback

The previously validated ESCD Executive/PA endpoints and UI remain the known-good predecessor surface. A later deployment rollback should restore the previously accepted ESCD route/UI revision and remove workflow-specific routes without changing authentication, DDNA state, Employment boundaries or unrelated deployment configuration.

## Verification after any future rollback

Re-run the ESCD review gate, confirm the expected branch/commit, verify workflow routes and objects match the selected rollback checkpoint, confirm no unrelated ESCD or DDNA changes were altered, and preserve a rollback receipt.
