# DCSE-DDNA Database Migration Receipt

**Status:** IMPLEMENTATION EVIDENCE / INTERNAL
**Date:** 2026-09-09
**Task:** `DCSE-RCHE-20260909-EMP-HARVEST-001`
**Execution Surface:** Supabase + GitHub

## 1. Authority verification

Verified controlling authority in `sonlyconsulting-ctrl/DCSE-Command-Post`:

- Designation: `governance/v7.2/DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md`
- Artifact: `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`
- Artifact SHA-256: `2d6afe04be2f65f8d56d6b4b26c81e254e04171e3c94a40023b56b9236de36ae`
- Revision identity: `7.2.0-CANDIDATE-R5`
- Authority state: `OPERATIVE`
- Readiness: `READY_WITH_FINDINGS`
- DCS effective designation date: 2026-08-08

The embedded candidate label is preserved as build-stage provenance. The later DCS operative designation controls authority. Runtime/deployment synchronization remains separately observable.

## 2. Supabase projects

### Dedicated governed DDNA destination

- Project: `DCSE-DDNA`
- Project ID: `uutpzaiqymyufljdgdaa`

### Legacy operations source

- Project: `SC-Command-Post`
- Project ID: `nevgdyfpxdaloacuutal`
- Historical DDNA location: `dcse_cp.ddna_*`

No destructive cutover was performed.

## 3. Live migrations applied to DCSE-DDNA

The following DDNA migrations were applied live:

1. `20260909092317 establish_dcse_ddna_core_and_legacy_migration`
2. `20260909092704 add_dcse_ddna_legacy_snapshot_registry`
3. `20260909093110 add_dcse_ddna_authority_registry`
4. `20260909093358 index_dcse_ddna_foreign_keys`

Pre-existing project migrations were not modified.

## 4. Normalized schemas established

### `dcse_ddna`

- `authority_registry`
- `source_artifacts`
- `extraction_runs`
- `extraction_items`
- `characteristics`
- `rules`
- `rule_conflicts`
- `rule_tests`
- `batch_metrics`
- `provenance_links`
- `artifact_registry`
- `legacy_import_snapshots`

### `dcse_ddna_legacy`

Compatibility preservation tables were created for:

- `ddna_source_queue`
- `ddna_extraction_runs`
- `ddna_characteristics`
- `ddna_model_comparisons`
- `ddna_ollama_jobs`

These tables do not themselves confer authority on historical records.

## 5. Employment RCHE material inserted

Current accessible DCS Employment pilot material was inserted or registered with verified provenance/hashes.

Current normalized record counts after this migration wave:

- Authority records: 1
- Source artifacts: 6
- Employment extraction runs: 1
- Employment DDNA characteristics/controls/patterns: 25
- Employment seed + learned candidate rules: 25
- Employment rule conflicts: 5
  - Open: 4
  - Resolved: 1
- Batch metric records: 1
- RCHE artifact registry records: 4
- Legacy import snapshot records: 3

`rule_tests`, `extraction_items`, and `provenance_links` remain structurally available but are not populated from local-only RCHE files that were not accessible to this runtime.

## 6. Employment pilot evidence registered

Pilot technical metrics recorded:

- Source count: 12
- Processed source count: 12
- RAG chunks: 44
- Facts: 9
- Characteristics: 18
- Patterns: 7
- Rule candidates evaluated: 25
- Rules tested into local candidate corpus: 21
- Seed-rule recovery: 15/15
- Conflicts preserved: 9
- Rejected candidates: 3
- Duplicate merges: 0
- Forward test pass rate: 1.0
- Backward test pass rate: 1.0
- Rules-fired pass rate: 1.0
- PS leakage: `PASS_NONE_DETECTED`
- Secret leakage: `PASS_NONE_DETECTED`
- Regression: `NO_MATERIAL_REGRESSION`

Registered local RCHE evidence hashes:

- Closeout SHA-256: `4B4DD8B718CCFC4CA08BE9A18592A9A93FD44ED5884613C7C1772645B58345FE`
- Validation SHA-256: `AA9B8F78193AA7CF53887F219C24BA6D1E6CBAE8F46CAF4F9CC848754095F44C`
- File manifest SHA-256: `D447DE7C9EA0BF6385E3750998EF1D6FA01CE4F340651EBB049F70A06391C7CB`
- Corpus v2 Candidate SHA-256: `F3A4322F8B2F1BE931C8BE0A8B4458ECE5760C6A390419A9F1A6843A03752F93`
- Local RCHE commit reported by Codex: `01388edb4b683d866c0e446293d3469e4363150e`

The local-only full RCHE artifact bodies were not available through this ChatGPT runtime. They were therefore registered by supplied verified hashes and metadata rather than falsely represented as copied bytes.

## 7. Authority reconciliation

Employment conflict `EMP-CON-004` was reconciled after direct GitHub verification of the DCS v7.2 R5 operative designation.

The Employment records now carry `operative_authority_verified` for controller authority. This does not mean every application, runtime, local checkout, or deployment surface is synchronized to the controller.

## 8. Legacy DDNA source inventory

Verified legacy records in `SC-Command-Post.dcse_cp`:

- `ddna_source_queue`: 129 rows
- `ddna_ollama_jobs`: 40 rows
- `ddna_characteristics`: 11 rows
- `ddna_extraction_runs`: 5 rows
- `ddna_model_comparisons`: 1 row

PS-lock scan of these legacy DDNA tables found zero PS-locked records in the checked queue, Ollama job, and characteristics tables.

Three controlled legacy snapshots were copied into the dedicated DDNA database for characteristics, extraction-run state, and model-comparison state.

### Physical migration limitation

The connected Supabase execution surface supports project-scoped SQL but does not provide a direct cross-project `COPY`/FDW/database-to-database transfer operation or database credentials. Consequently, the 129 queue rows and 40 Ollama-job rows, and exact full-field copies of all legacy tables, were not physically duplicated into `DCSE-DDNA` during this execution.

This is recorded as a migration boundary, not hidden as completion. The legacy records remain intact in `SC-Command-Post` and must remain authoritative for their historical physical state until an authenticated transfer mechanism performs an exact copy and verifies row/hash equivalence.

Existing consumers that reference `dcse_cp.ddna_*` were intentionally not redirected without dependency migration, regression testing, rollback evidence, and human release.

## 9. Security posture and advisor review

New DDNA tables are private-by-default:

- RLS enabled as defense in depth
- no anonymous/authenticated client access intentionally granted by this implementation
- service-role use reserved for authorized server/tool execution

Supabase advisor review identified inherited project findings outside this migration scope, including:

- pre-existing `vector` extension in `public`
- pre-existing SECURITY DEFINER functions callable by anonymous/authenticated roles
- pre-existing `v7_worker` RLS performance warnings

These were not modified because dependency impact was not assessed in this task.

The advisor originally identified five unindexed foreign keys in the new DDNA schema. Migration `index_dcse_ddna_foreign_keys` corrected all five. A subsequent advisor pass no longer reported the unindexed-foreign-key finding.

## 10. GitHub implementation record

Branch:

`dcse-ddna-dedicated-store-20260909`

Created/updated artifacts:

- `governance/v7.2/implementations/DCSE_DDNA_DATABASE_OPERATING_INSTRUCTIONS_20260909.md`
- `supabase/ddna/migrations/20260909_dcse_ddna_core.sql`
- `governance/v7.2/implementations/DCSE_DDNA_DATABASE_MIGRATION_RECEIPT_20260909.md`

The migration SQL is stored under `supabase/ddna/migrations/` intentionally so existing SC-Command-Post migration automation cannot accidentally apply this dedicated-database schema to the operations project.

## 11. Release posture

Technical status:

- Dedicated normalized DDNA schema: COMPLETE
- Employment seed/current accessible material insertion: COMPLETE FOR ACCESSIBLE INPUTS
- v7.2 R5 authority verification: COMPLETE
- Legacy data discovery and preservation: COMPLETE
- Exact legacy cross-project physical copy: PARTIAL / PENDING AUTHENTICATED TRANSFER
- Existing application consumer cutover: NOT RELEASED
- GitHub branch implementation record: COMPLETE
- Merge to main: HUMAN RELEASE GATE

No rule candidate was automatically promoted to governing authority.

Structure Precedes Scale.
