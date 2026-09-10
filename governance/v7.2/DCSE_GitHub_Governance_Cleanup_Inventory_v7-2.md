# DCSE GitHub Governance Cleanup Inventory v7.2

**Task ID:** DCSE-V72-GOV-SYNC-20260910  
**Version:** v7.2  
**Status:** ACTIVE INVENTORY  
**Authority:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Scope:** D20, v7.2 Master/Profile governance, doctrine routing, DDNA, GitHub/Supabase/Tribunal source relationships  
**Poller implementation:** EXCLUDED and parked under ESCD Issue #78  

## 1. Purpose

Identify duplicate, stale, superseded, historical, or potentially removable governance artifacts and branches without deleting anything during this synchronization transaction.

Disposition vocabulary:

- **KEEP_ACTIVE**: current operative/routing artifact.
- **KEEP_HISTORICAL**: retain for provenance/audit.
- **SUPERSEDED**: no longer controlling, but preserve until dependency cleanup is complete.
- **DELETE_CANDIDATE**: likely removable from the active tree after dependency/reference verification.
- **REVIEW_RETIRE**: branch or artifact requires compare/reference/open-PR review before retirement.
- **UNKNOWN**: insufficient evidence.

## 2. File Inventory

| Item | Current Role | Finding | Disposition | Preconditions Before Removal |
|---|---|---|---|---|
| `governance/v7.2/source/doctrines/D20_Product_Assembly_Methodology_v7-2.md` | promoted D20 v7.2 | current Reuse Before Redesign doctrine | KEEP_ACTIVE | none |
| `governance/v7.2/doctrines/D20_Product_Assembly_Methodology.md` | prior v7.2 sidecar from PR #77 | duplicate active-looking D20 location created during earlier synchronization error | DELETE_CANDIDATE | verify no runtime/registry/manifest/open-PR dependency remains, then remove from active tree while preserving Git history |
| `governance/v7.1/source/doctrines/D20_Product_Assembly_Methodology.md` | historical source | v7.0 candidate source and lineage | KEEP_HISTORICAL / SUPERSEDED | do not delete until source lineage and historical audits no longer depend on path |
| `governance/v7.2/source/doctrines/D16_DDNA_Governance_v7-2.md` | promoted DDNA governance | current source/knowledge/authority/retrieval separation | KEEP_ACTIVE | none |
| `governance/v7.1/source/doctrines/D16_DDNA_Governance.md` | historical source | v6.9 pending-approval metadata, older local-path persistence rules | KEEP_HISTORICAL / SUPERSEDED | preserve extraction-method lineage and historical references |
| `governance/v7.2/source/doctrines/D22_Source_Authority_Runtime_Distribution_v7-2.md` | promoted persistence/source doctrine | current controlling source/persistence routing | KEEP_ACTIVE | none |
| `governance/v7.1/source/doctrines/D22_Source_Authority_Runtime_Distribution.md` | historical source | older v7.0 candidate source | KEEP_HISTORICAL / SUPERSEDED | preserve source lineage |
| `governance/v7.1/doctrines/D22_Source_Authority_Runtime_Distribution.md` | v7.1 routed projection | still referenced by older machine/runtime artifacts | SUPERSEDED / REVIEW_RETIRE | update all operative manifest/runtime references first; confirm no active workflow hard-codes this path |
| `governance/v7.2/source/registry/DCSE_Doctrine_Index_v7-2.md` | promoted v7.2 index | current doctrine routing index for this synchronization | KEEP_ACTIVE | none |
| `governance/v7.1/source/registry/DCSE_Doctrine_Index_v6.9.md` | historical source index | filename/header/version and local v6.9 links are stale for current runtime | KEEP_HISTORICAL / SUPERSEDED | preserve lineage; remove from active runtime routes before any archive action |
| `governance/v7.1/source/doctrines/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md` | designated operative R5 controller artifact | controlling historical exact-byte artifact under later DCS designation | KEEP_ACTIVE | never rename/delete merely for filename normalization because exact artifact identity and hash are authority evidence |
| `governance/v7.2/DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md` | operative designation | binds R5 exact artifact to DCS authority | KEEP_ACTIVE | none |
| `governance/v7.2/DCSE_Master_Profile_Authority_Synchronization_v7-2.md` | current controlled evolution record | binds Sept. 10 promoted deltas to R5 lineage | KEEP_ACTIVE | none |
| `DCSE_MANIFEST.yaml` | machine routing index | updated in this transaction to v7.2 D22/D16/D20/index/sync routes | KEEP_ACTIVE | verify after merge |
| `governance/v7.1/V7_1_CANONICAL_GOVERNANCE_PACKAGE_MANIFEST_20260803.md` | historical v7.1 package | prior authority package evidence | KEEP_HISTORICAL | no deletion |
| `governance/v7.1/DCSE_Master_Profile_v7.1.md` | historical controller | predecessor lineage | KEEP_HISTORICAL | no deletion |
| `tribunal/v7/GOVERNANCE_STRUCTURAL_AUDIT_REPORT.md` and PR39 variant | historical evidence | references older paths by design | KEEP_HISTORICAL | evidence should not be rewritten to simulate current state |

## 3. Branch Inventory Requiring Later Review

The following branch families were observed and should be compared to `main`, checked for open PRs and unique commits, then classified before deletion:

- `agent/centralize-v72-master-profiles`
- `agent/v7-doctrine-finalization`
- `agent/v7.1-zone-integrity-remediation`
- `agent/v71-master-profile-rc3-manual`
- `agent/v72-r5-operative-cutover`
- `chatgpt/v7-foundation-runtime-compiler`
- `chatgpt/v7-runtime-compiler-mvp`
- `chatgpt/v7.1-dispatch-assignment-fix-20260806`
- `chatgpt/v7.1-runtime-adoption-20260806`
- `chatgpt/v7.1-universal-dispatch-controller-20260807`
- `chatgpt/v7.2-poller-communication-recovery-20260808`
- `claude/project-v7-1-setup-l2t95z`
- `claude/v7-1-poller-result-access-ui-fix`
- `claude/v7-2-r4-code-review-xty5lt`
- `governance/v7.1-accountable-nonstoppage-correction`
- `governance/v7.1-nonstoppage-lifecycle-fix`
- `governance/v7.1-owned-product-harness`
- `governance/v7.1-promotion-metadata-reconciliation`
- `governance/v7.2-d20-reuse-before-redesign`
- `governance/v7.2-master-profile-controller`
- `governance/v7.2-v72-operative-designation`
- `v7.0`

Current transaction branch `governance/v7.2-authority-sync-20260910` is **KEEP_UNTIL_MERGED**.

No branch in this inventory is authorized for deletion solely because it is old. Required retirement evidence is: merged/contained status, no unique required commits, no open PR dependency, no operative runtime dependency, and no unresolved authority/provenance reference.

## 4. Immediate Cleanup Priority After This Transaction

1. Remove or convert the duplicate D20 sidecar only after the new canonical v7.2 path is merged, registered in Supabase, and all active references point to it.
2. Update remaining active machine-readable/runtime references from older v7.1 D22/index locations to promoted v7.2 paths.
3. Preserve historical v7.1 source and Tribunal evidence as lineage rather than deleting history.
4. Review old branches in batches using compare-to-main and open-PR checks before retirement.

## 5. Stop Boundary

This file is an inventory and classification artifact only. **No files or branches were deleted by item 3.** Destructive cleanup is a separate controlled execution after dependency and provenance verification.