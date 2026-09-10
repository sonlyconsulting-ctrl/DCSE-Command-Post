# ESCD ROLLBACK

**Task ID:** DCSE-ESCD-001-EXEC-PA-003  
**Status:** DOCUMENTED / NOT EXECUTED AGAINST PRODUCTION

## Current safety fact

No production ESCD migration or deployment was performed in this tranche. The immediate rollback point is therefore the prior validated branch checkpoint `c281390a0cff8c02bc023c6392031c836c45df49` if the candidate tranche is rejected before release.

## Repository rollback boundary

The combined tranche is additive to the existing ESCD runtime branch. Rejection should revert only the commits/files introduced for `DCSE-ESCD-001-EXEC-PA-003`; it must not reset or discard the previously validated auth, approval, evidence, briefing or job-verification work.

## Candidate database rollback boundary

Each new migration contains or identifies rollback behavior. If these migrations are ever authorized for a non-production or production target, rollback must first inventory dependent records and preserve evidence. Candidate objects introduced in this tranche are:

- `escd_projects`
- `escd_items`
- `escd_item_events`
- `escd_decisions`
- `escd_contact_contexts`
- `escd_routines`
- `escd_notification_intents`
- `escd_item_sources`
- item transition and routine guards associated with those objects

Do not drop these objects after data exists without an explicit destructive-action authorization and evidence preservation plan.

## Runtime rollback

The prior ESCD job/briefing/approval endpoints remain structurally separate. A release rollback should restore the previously verified runtime revision and remove routing to the new Executive/PA endpoints without changing authentication or production DDNA state.

## Verification after any future rollback

Re-run the ESCD review gate, confirm the expected branch/commit, confirm no new tables/routes remain active beyond the selected rollback checkpoint, and preserve a rollback receipt.
