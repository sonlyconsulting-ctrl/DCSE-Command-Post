# DCSE DDNA Consumer Cutover Mapping

Task ID: `DCSE-DDNA-CONSUMER-CUTOVER-20260909-001`
Parent: `DCSE-RCHE-20260909-HARVEST-001`
Status: IN PROGRESS
Authority: DCSE Master Profile v7.2 R5 OPERATIVE
Release authority: DCS

## Purpose

Map current live DDNA consumers from the legacy SC-Command-Post persistence surface to the dedicated DCSE-DDNA project before any production cutover.

## Verified source state

GitHub default-branch search identified the following current references:

| Consumer | Current reference | Operation | Classification | Intended target | Cutover posture |
| --- | --- | --- | --- | --- | --- |
| `apps/sc-agent-os/api/index.js` runtime job queue | `dcse_cp.ddna_ollama_jobs` via Supabase REST with `schema=dcse_cp` and `Accept-Profile: dcse_cp` | GET recent jobs | READ, LIVE | `DCSE-DDNA.dcse_ddna_legacy.ddna_ollama_jobs` initially, because exact legacy shape is preserved there | Migrate through separate server-side DDNA connection and explicit rollback selector |
| `apps/sc-agent-os/api/index.js` runtime inventory | known table list includes `ddna_characteristics`, `ddna_extraction_runs`, `ddna_model_comparisons`, `ddna_ollama_jobs`, `ddna_source_queue` and labels them as `dcse_cp` | display/inventory only | INVENTORY/DISPLAY | Split legacy preservation inventory from normalized DDNA inventory; do not imply all DDNA tables remain in `dcse_cp` | Update after runtime mapping is implemented |
| `apps/sc-agent-os/docs/CRUD_COVERAGE_MATRIX.md` | `dcse_cp.ddna_ollama_jobs` | documentation of runtime path | DOCUMENTATION | Dedicated DDNA runtime path after validated cutover | Update with implementation PR |
| `apps/sc-agent-os/docs/PRODUCTION_VERSION_ALIGNMENT_REPORT.md` | `dcse_cp.ddna_ollama_jobs` marked LIVE | documentation of production alignment | DOCUMENTATION | Dedicated DDNA runtime path after validated cutover | Update with implementation PR |

## Dedicated project targets

Dedicated project: `DCSE-DDNA` (`uutpzaiqymyufljdgdaa`).

Preservation schema:
- `dcse_ddna_legacy.ddna_source_queue`
- `dcse_ddna_legacy.ddna_ollama_jobs`
- `dcse_ddna_legacy.ddna_characteristics`
- `dcse_ddna_legacy.ddna_extraction_runs`
- `dcse_ddna_legacy.ddna_model_comparisons`

Normalized governed schema:
- `dcse_ddna.authority_registry`
- `dcse_ddna.source_artifacts`
- `dcse_ddna.extraction_runs`
- `dcse_ddna.extraction_items`
- `dcse_ddna.characteristics`
- `dcse_ddna.rules`
- `dcse_ddna.rule_conflicts`
- `dcse_ddna.rule_tests`
- `dcse_ddna.batch_metrics`
- `dcse_ddna.provenance_links`
- `dcse_ddna.artifact_registry`
- `dcse_ddna.legacy_import_snapshots`

## Connection architecture

SC Agent OS currently uses general Supabase connection variables for the SC-Command-Post project. The DDNA cutover must not repoint those variables because non-DDNA consumers remain on the operations project.

Introduce a separate server-side DDNA connection path, using environment bindings conceptually equivalent to:
- `DDNA_SUPABASE_URL`
- `DDNA_SUPABASE_SERVICE_ROLE_KEY`
- `DDNA_RUNTIME_SCHEMA`
- `DDNA_RUNTIME_MODE`

No secret value may be committed, logged, embedded in browser-delivered HTML, issue text, PR text, or test fixtures.

`DDNA_RUNTIME_MODE` should support at minimum:
- `legacy`: use existing SC-Command-Post DDNA path
- `dedicated`: use DCSE-DDNA

A comparison/test mode may be implemented if it performs safe dual reads only. Do not dual-write production records without a separately proven idempotency/provenance design.

## Initial semantic mapping decision

The live SC Agent OS job queue is an operational view of the historical `ddna_ollama_jobs` shape. Because exact physical preservation has already been validated in `dcse_ddna_legacy.ddna_ollama_jobs`, the first cutover should use that preservation table rather than silently mapping the UI to normalized tables with different semantics.

Normalization into governed `dcse_ddna` structures is a separate consumer evolution step.

## Rollback

Rollback must be configuration-driven. Returning `DDNA_RUNTIME_MODE` to `legacy` must restore the pre-cutover endpoint without code rollback or source-table mutation.

The legacy source tables must remain intact during this task.

## Required validation

1. Validate dedicated project server-side credentials exist in target deployment environments without exposing values.
2. Verify dedicated REST/database access to `dcse_ddna_legacy.ddna_ollama_jobs` using the server-side execution path.
3. Compare the current legacy query result and dedicated query result for the same ordering, projection, and row limit.
4. Verify non-DDNA Agent OS calls continue to use SC-Command-Post.
5. Test `legacy` rollback mode.
6. Run static, unit/integration, and application build checks.
7. Scan exact diff and test/log artifacts for credentials and protected-lane leakage.
8. Record a validation receipt before production release.

## Runtime baseline finding

Vercel inspection on 2026-09-09 shows recent SC Agent OS deployments, including the PR #64 merge deployment, in `CANCELED` state. The inspected canceled merge deployment showed no build error/stderr/exit events. Cause remains UNKNOWN and must not be attributed to DDNA without evidence. Cutover validation therefore needs an explicit runtime-health baseline independent of the DDNA data-path comparison.

## Release gate

Implementation, preview/test deployment, dual-read validation, rollback proof, and evidence publication may proceed without further DCS interruption. The production DDNA runtime switch remains the material DCS release gate.

Structure Precedes Scale.
