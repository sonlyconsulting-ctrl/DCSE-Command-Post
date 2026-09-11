# DCSE v7.2 Governance - START HERE

**Purpose:** Single front door for the operative v7.2 governance package.  
**Controller:** `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`  
**Doctrine Root:** `doctrines/`  
**Doctrine Set:** D01 through D22  
**Registry:** `registry/DCSE_Doctrine_Index_v7-2.md`  
**Machine Manifest:** `V7_2_CANONICAL_GOVERNANCE_PACKAGE_MANIFEST.json`

## Startup Route

1. Read the operative R5 Master Profile.
2. Read the v7.2 Doctrine Index.
3. Use D22 to verify canonical source identity and distribution state.
4. Use D21 to classify the task and load only the required doctrine subset.
5. Load D03 for model/agent orchestration when delegation or model routing is involved.
6. Apply onboarding, stop-gates, project instructions, and task-specific methods as routed.
7. Record DCL/evidence and closeout under D21/D04.

No ordinary v7.2 task should need to search v7.1 or v6.9 folders to locate its controlling doctrine. Historical folders remain lineage/evidence only.

## Canonical Doctrine Directory

| ID | File | Package state |
|---|---|---|
| D01 | `doctrines/D01_Forward_Thinking_v7-2.md` | carried_forward |
| D02 | `doctrines/D02_Forward_Backward_Chaining_v7-2.md` | carried_forward |
| D03 | `doctrines/D03_AI_Orchestration_v7-2.md` | promoted |
| D04 | `doctrines/D04_Command_Post_Communications_v7-2.md` | promoted |
| D05 | `doctrines/D05_Baseline_Promotion_v7-2.md` | promoted |
| D06 | `doctrines/D06_File_System_v7-2.md` | promoted |
| D07 | `doctrines/D07_Campaign_Governance_v7-2.md` | carried_forward |
| D08 | `doctrines/D08_Voice_Tone_v7-2.md` | carried_forward |
| D09 | `doctrines/D09_Brand_Identity_v7-2.md` | carried_forward |
| D10 | `doctrines/D10_Persona_Assets_v7-2.md` | carried_forward |
| D11 | `doctrines/D11_HTML_Wix_App_v7-2.md` | carried_forward |
| D12 | `doctrines/D12_Video_Media_v7-2.md` | carried_forward |
| D13 | `doctrines/D13_DART_Core_v7-2.md` | ps_route_only |
| D14 | `doctrines/D14_DART_PS_Protected_v7-2.md` | ps_route_only |
| D15 | `doctrines/D15_Database_Administration_v7-2.md` | promoted |
| D16 | `doctrines/D16_DDNA_Governance_v7-2.md` | promoted |
| D17 | `doctrines/D17_DART_Universal_Methodology_v7-2.md` | carried_forward |
| D18 | `doctrines/D18_Media_Production_Pipeline_v7-2.md` | carried_forward |
| D19 | `doctrines/D19_Visual_Creation_Pipeline_v7-2.md` | carried_forward |
| D20 | `doctrines/D20_Product_Assembly_Methodology_v7-2.md` | promoted |
| D21 | `doctrines/D21_Doctrine_Runtime_Engine_v7-2.md` | active_projection |
| D22 | `doctrines/D22_Source_Authority_Runtime_Distribution_v7-2.md` | promoted |

**PS routing:** D13 and D14 are present for completeness but SHALL load only on an authorized PS route. Their presence in this package does not authorize protected content access.

## Required Associated Controls

- `DCSE_MANIFEST.yaml` at repository root
- `registry/DCSE_Doctrine_Index_v7-2.md`
- `UNIVERSAL_AGENT_ONBOARDING_AND_ACCESS_STANDARD_v7-2.md`
- `DCS_LEVEL_0_RESERVED_STOP_GATES_v7-2.md`
- `ZONE_INDEX.v7.2.json`
- `project-instructions/DCSE_COMMAND_POST_PROJECT_INSTRUCTIONS_v7_2_FINAL.md`
- `dcs_express_directives.v7.2.json`
- `DCSE_V7_2_BOUNDED_INDEPENDENT_AUTHORITY_RULE_FOUNDRY_DIRECTION_20260911.md`
- `DCSE_Runtime_Harmony_Task_Traceability_and_Navigable_Closeout_v7-2.md`

## Working Capability Modules

Governed capability modules may live beneath v7.2 without becoming doctrine merely by existence. The following September 11 modules are active canonical capability modules under DCS-DIR-20260911-001 following PR #83 merge:

- `rule-foundry/DCSE_V7_2_RULE_GENERATION_AND_EXECUTABLE_BASELINE_STANDARD.md`
- `rule-foundry/DCSE_RULE_SCHEMA_v1.json`
- `rule-foundry/DCSE_DDNA_RULE_EXTRACTION_PROFILE_v1.md`
- `rule-foundry/DCSE_CONTENT_AND_ARTIFACT_GENERATION_STANDARD_v1.md`
- `rule-foundry/DCSE_CONTENT_ARTIFACT_RULESET_v1.json`
- `architecture/DCSE_CREATIVE_INTELLIGENCE_COMMERCE_ROUTER_v1.md`

Current implementation profile:

- `implementations/DCSE_SIX_PRODUCT_SEQUENTIAL_PARALLEL_PRODUCTION_PROFILE_20260911.md`

These remain subordinate to the Master Profile and routed doctrine. The Creative Router architecture is approved but remains runtime UNSYNCHRONIZED until implementation/security/runtime evidence exists.

## Compatibility Mirror

`source/doctrines/` and `source/registry/` are temporary compatibility/lineage mirrors for older references. They are not the normal v7.2 startup route. CI verifies mirror equality while they remain present.

## Navigation Rule

**Current governance lives under `governance/v7.2/`. Historical governance remains available for lineage but SHALL NOT be used as the normal startup path.**
