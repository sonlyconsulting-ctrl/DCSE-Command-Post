# ESCD CURRENT HEAD VALIDATION QUEUE

**Task ID:** DCSE-ESCD-001-WORKFLOW-004

## Current validation purpose

Validate the reusable workflow orchestration candidate and its operator-facing UI on the exact current branch head before release-validation preparation.

Required gate coverage:

- Python policy/runtime/workflow/UI-surface suite
- isolated PostgreSQL candidate migration chain
- runtime SQL behavior checks
- Executive/PA SQL behavior checks
- structured source-provenance checks
- workflow orchestration and authority checks

## Release boundary

A green repository gate proves candidate implementation integrity, not production release readiness. Final release validation must exercise the deployed authenticated ESCD UI through browser-visible workflow journeys and required live integrations.

DDNA is held pending Codex and is excluded from this gate. No DDNA completion may be inferred from WORKFLOW-004 evidence.

Current target: `EXACT_HEAD_GREEN -> READY_FOR_RELEASE_VALIDATION_PREP`.
