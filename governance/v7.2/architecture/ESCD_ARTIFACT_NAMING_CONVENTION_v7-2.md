# ESCD Artifact Naming Convention v7.2

**Status:** CANDIDATE  
**Authority context:** DCSE v7.2  
**Scope:** ESCD artifacts, runtime records, build receipts, test evidence, branches, and handoffs

## Canonical rule

New ESCD artifacts SHALL use:

`ESCD_<DOMAIN>_<ARTIFACT>_<RUNTIME-VERSION>_V7_2_<STATE>_<YYYYMMDD>.<ext>`

Examples:

- `ESCD_MVP_ORCHESTRATOR_0_6_1_V7_2_BUILD_RECEIPT_20260917.md`
- `ESCD_MVP_PROVIDER_BINDINGS_0_6_1_V7_2_OPERATIVE_20260917.md`
- `ESCD_CF_RECOVERY_0_6_1_V7_2_HANDOFF_20260917.md`
- `ESCD_TEST_MVP_CONTRACT_0_6_1_V7_2_VALIDATION_20260917.md`

## Version separation

- **Runtime/product version:** ESCD MVP version, for example `0.6.1`.
- **Governance version:** DCSE authority floor, now `v7.2`.
- These values SHALL NOT be collapsed into one version number.
- A runtime upgrade does not automatically promote governance status.
- A governance upgrade does not automatically change runtime behavior.

## Branch naming

New ESCD branches SHOULD use:

`<lane>/<purpose>/escd-<runtime-version>-v7.2-<YYYYMMDD>`

Examples:

- `baseline/escd-mvp-0.6.1-v7.2-20260917`
- `feature/escd-orchestrator-0.6.1-v7.2-20260917`
- `fix/escd-runtime-repair-0.6.1-v7.2-20260917`

Existing branches are historical identifiers and SHALL NOT be renamed solely for cosmetic consistency. New commits, receipts, and handoffs SHALL use the v7.2 form.

## Compatibility and migration

Existing names such as `ESCD_MVP_006`, `ESCD_MVP_006_BUILD_RECEIPT`, and `ESCD_MVP_0_6` remain historical aliases. Do not delete or silently rename them. When an existing artifact is revised, preserve its original path where traceability requires it and add the v7.2 designation in the revision record or a new superseding artifact.

## Required metadata

Every new ESCD artifact SHOULD include:

- Task ID
- Runtime version
- `DCSE_GOVERNANCE_VERSION: v7.2`
- Lifecycle state
- Source branch and commit
- Evidence references
- Supersedes/derives-from relationship where applicable
- Validation status
- Handoff ID where applicable

## Example header

```yaml
artifact_id: ESCD-MVP-ORCHESTRATOR-0.6.1-V7.2-20260917
runtime_version: 0.6.1
governance_version: v7.2
lifecycle: CANDIDATE
source_branch: baseline/escd-mvp-0.6.1-v7.2-20260917
validation: PENDING
```

## Control boundary

This convention governs ESCD naming and metadata. It does not place SC/CTJ creative assets, image prompts, brand images, or generator-specific instructions inside the ESCD conversation-flow state.
