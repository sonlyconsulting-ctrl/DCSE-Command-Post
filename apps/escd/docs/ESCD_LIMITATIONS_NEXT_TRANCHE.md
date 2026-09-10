# ESCD LIMITATIONS AND NEXT TRANCHE

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Status:** WORKFLOW ORCHESTRATION CANDIDATE CLOSEOUT

## Completed in this tranche

`DCSE-ESCD-001-WORKFLOW-004` is complete at candidate level with both the reusable workflow engine and operator-facing workflow UI.

The candidate includes:

- workflow template registry/versioning
- workflow instance binding to exact template identity and fingerprint
- all ten planned workflow types
- controlled inheritance without weakening parent controls
- step autonomy, approval, evidence, dependency, failure and recovery fields
- governed-job binding before workflow execution authority
- action-scoped approval binding for approval-required steps
- evidence-gated completion
- append-oriented workflow history
- authenticated workflow API and candidate routing
- workflow list/detail/instantiate UI in the Executive Assistant surface
- dedicated operational workflow UI for bounded workflow and step lifecycle actions
- responsive and accessibility-oriented states

## Current deliberate limitations

These are release dependencies or deliberately held capabilities, not silently completed work:

- no production Supabase migration has been applied
- no production deployment has occurred
- no PR merge has occurred
- no live authenticated browser E2E journey has yet been executed against a deployed ESCD candidate
- no live database persistence test has been performed against the intended authorized ESCD deployment target
- Gmail and Calendar consequential writes remain approval-gated and are not claimed operational from repository tests
- Android/mobile delivery is not claimed without device/runtime evidence
- broader connector availability/staleness/recovery behavior requires provider-backed release validation where applicable

## DDNA hold

The next planned DDNA candidate-interface tranche is **HELD FOR CODEX** by DCS direction.

Do not:

- substitute another implementation path for the held DDNA work
- perform the dedicated DDNA production consumer cutover
- represent DDNA integration as release-validated
- bundle DDNA changes into workflow or release-validation work while the hold remains active

When Codex is available, resume from the preserved DDNA checkpoint under its controlling task/issues rather than reconstructing the work.

## Release-validation requirement

Final ESCD release validation is not justified by backend and static UI tests alone.

Before `READY_FOR_DCS_RELEASE`, validation must include an actual deployed, authenticated browser journey that exercises the ESCD Executive Assistant and Workflows surfaces against the authorized persistence target. Where final claims depend on Gmail, Calendar, notifications, files or device/mobile behavior, the relevant source-native/provider journey must also be evidenced.

The final release gate must therefore distinguish:

1. repository candidate validation: currently PASS
2. deployed authenticated UI/database validation: NOT YET PERFORMED
3. provider/device integration validation: NOT YET COMPLETE
4. DDNA integrated validation: HELD FOR CODEX
5. explicit DCS production release authorization: NOT YET REQUESTED

## Current exit

`READY_FOR_NEXT_TRANCHE / DDNA_HELD_FOR_CODEX`

Until the hold is released, ESCD can continue only with already-planned non-DDNA verification/preparation that does not falsely claim live release readiness or cross a production gate.
