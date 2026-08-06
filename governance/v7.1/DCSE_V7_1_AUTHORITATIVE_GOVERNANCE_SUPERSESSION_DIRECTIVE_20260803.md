---
dcse_zone: authority
dcse_authority_level: CANDIDATE
dcse_document_id: DCSE_V7_1_AUTHORITATIVE_GOVERNANCE_SUPERSESSION_DIRECTIVE_20260803
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: DCSE
dcse_required_approval: DCS_LEVEL_0_EXACT_DIFF
---

# DCSE V7.1 Governance Supersession Decision Record

## Purpose

This document records the August 3, 2026 DCS decision to supersede earlier DCSE governance versions with V7.1.

It is subordinate to `DCSE_Master_Profile_v7.1.md`. It does not independently define the authority hierarchy, runtime routing, source reconciliation, or promotion procedure.

## Recorded Decision

DCS Level 0 directed that DCSE V7.1 supersede V6.8, V6.9, V7.0, and earlier DCSE governance versions for current operations.

Earlier versions remain preserved as historical evidence, lineage, and lessons learned. They do not control where they conflict with a promoted V7.1 Master Profile or promoted V7.1 doctrine.

## Controlling Routes

- Constitutional entry point: `DCSE_Master_Profile_v7.1.md`
- Source authority and reconciliation: `doctrines/D22_Source_Authority_Runtime_Distribution.md`
- Runtime doctrine selection: `doctrines/D21_Doctrine_Runtime_Engine.md`
- Promotion and baseline controls: D05 as routed by the Master Profile

## Required Migration Effect

After promotion of the amended V7.1 package:

1. Active bootstrap sources must load the Master Profile first.
2. Legacy materials must be labeled `HISTORICAL_SUPERSEDED` or equivalent.
3. Legacy materials must be excluded from active routing unless the Master Profile or D21 expressly adopts their subject content.
4. Runtime registries must reference the canonical V7.1 paths, commit SHAs, content hashes, and promotion records.
5. Execution and evidence files must not declare constitutional or promoted authority.

## Acceptance Gate

Supersession is fully operational only when:

- the amended Master Profile is promoted for the exact diff;
- normalized D21 and D22 are promoted;
- active startup paths load the Master Profile first;
- DCSE-DDNA records the canonical paths and promotion states;
- scans find no active execution or evidence source claiming promoted authority;
- GitHub and runtime registry reconciliation is complete.

## Amendment Status

The August 3, 2026 DCS decision remains a verified source event. This rewritten record is a candidate representation of that decision and requires exact-diff review before replacing the prior artifact.