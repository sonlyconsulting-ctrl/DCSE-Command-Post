# DCSE-DDNA Database Operating Instructions

**Status:** IMPLEMENTATION CONTROL / INTERNAL
**Effective Date:** 2026-09-09
**Authority:** DCSE Master Profile v7.2 R5, OPERATIVE by DCS designation dated 2026-08-08
**Task:** `DCSE-RCHE-20260909-EMP-HARVEST-001`

## Purpose

Establish the dedicated Supabase project `DCSE-DDNA` (`uutpzaiqymyufljdgdaa`) as the governed normalized persistence surface for DDNA extraction, RAG/DDNA harvest evidence, RCHE candidate rules, provenance, conflicts, testing, batch metrics, and artifact integrity records.

The operational Supabase project `SC-Command-Post` (`nevgdyfpxdaloacuutal`) remains a legacy source and compatibility surface while existing consumers are migrated and independently tested. This instruction does not authorize destructive removal of legacy tables or an untested application cutover.

## Authority

The controlling controller is `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`, artifact SHA-256 `2d6afe04be2f65f8d56d6b4b26c81e254e04171e3c94a40023b56b9236de36ae`, designated OPERATIVE by DCS in `governance/v7.2/DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md`.

The controller artifact's embedded candidate label is build-stage provenance. The later DCS operative designation controls authority. Runtime and deployment synchronization remain separately observable states.

## Database routing

### Governed normalized destination

Write new DDNA/RCHE normalized records to the private `dcse_ddna` schema in `DCSE-DDNA`.

Core tables:

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

### Legacy preservation

Historical DDNA tables in `SC-Command-Post.dcse_cp` remain source records until consumer migration is complete. Exact-shape preservation tables exist under `DCSE-DDNA.dcse_ddna_legacy` for controlled migration/reconciliation.

No historical result is promoted merely because it is copied.

## Authority and status control

DDNA extraction may produce Facts, Characteristics, Patterns, and Rule Candidates. These classes must remain distinct.

Rule lifecycle:

`Candidate -> Tested -> Approved -> Active -> Superseded -> Retired`

Automated extraction or migration may assign Candidate, Tested, Hold, Reject, Merge, Duplicate, or Conflict where supported by evidence. It may not independently create Approved or Active authority.

Explicit DCS correction carries greater candidate weight than model inference. Duplicate copies of one origin event do not count as independent corroboration.

## Provenance requirement

Every normalized source and derived item must preserve enough lineage to answer:

- where the information originated;
- whether it was copied or summarized;
- which source/version supplied it;
- what authority state applied;
- whether contradictory evidence exists;
- whether a later artifact superseded it.

Use `origin_event_id`, `derived_from`, `copied_to`, `summarized_from`, and `promoted_into` where applicable.

## Protected data

PS-protected content must not enter shared DDNA/Employment corpora. Policy references to PS controls are not themselves PS content and must not cause false-positive leakage findings.

Do not store passwords, private keys, service-role keys, API secrets, connection strings, MFA material, recovery codes, or other credentials in GitHub or DDNA content records.

## Private-by-default posture

The `dcse_ddna` and `dcse_ddna_legacy` schemas are private-by-default. RLS is enabled as defense in depth. No anonymous or authenticated client grants are established by this implementation. Service-role access is reserved for authorized server/tool execution.

Any future Data API exposure requires an explicit access design, least-privilege grants, RLS policies, and validation before release.

## Employment RCHE reference implementation

The DCS Employment pilot is the first validated RCHE implementation. Its task ID is `DCSE-RCHE-20260909-EMP-HARVEST-001`.

The technical pilot reached Batch 3 stabilization with:

- 12 of 12 available sources processed
- 44 RAG chunks
- 9 facts
- 18 characteristics
- 7 patterns
- 25 rule candidates evaluated
- 21 rules tested into the local candidate corpus
- 15 of 15 seed rules recovered
- 9 conflicts preserved
- 3 rejected candidates
- no material regression
- no PS leakage detected
- no secret leakage detected

The local full ChatGPT account export remains a future reconciliation source. Its absence does not invalidate the completed technical pilot, but new evidence must be reconciled rather than assumed equivalent.

## Compatibility rule

Do not redirect or disable existing `SC-Command-Post` DDNA consumers merely because the dedicated database exists. Code that still reads or writes `dcse_cp.ddna_*` requires an explicit migration packet, test evidence, rollback path, and human release gate.

## Execution sequence for future harvests

`Source Inventory -> Authority/Lane Classification -> RAG -> DDNA Extraction -> Fact/Characteristic/Pattern/Rule Candidate Separation -> RCHE Admission -> Forward Test -> Backward Test -> Rules Fired Test -> Conflict/Duplicate Review -> Candidate Corpus -> Regression -> Human Promotion Gate`

## Standing model/tool preflight

Before substantive work, state the recommended execution surface/model and ChatGPT thinking mode for the task. Model duty is task-specific and dynamic. A builder should not be the sole certifier of a material governed output.

## Stop gates

Stop for material authority conflict, PS exposure, credential requirement, destructive/irreversible operation, external release, or attempted promotion to governing authority without authorization. Routine parsing defects, duplicates, deterministic test failures, and repairable implementation defects are not stop conditions.

Structure Precedes Scale.
