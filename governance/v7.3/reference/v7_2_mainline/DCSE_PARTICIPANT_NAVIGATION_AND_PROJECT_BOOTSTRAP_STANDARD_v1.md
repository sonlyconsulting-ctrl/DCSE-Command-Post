# DCSE v7.2 Participant Navigation and Project Bootstrap Standard v1

**Status:** OPERATIVE - DCS Level 0 directed 2026-09-15  
**Task:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02 / navigation reconciliation  
**Authority:** DCS Level 0  
**Lane:** DCSE / ALL  
**Canonical governance repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Authority branch:** `main`

## 1. Master-Profile-First invariant

Every DCSC participant with authorized project access SHALL begin with:

`governance/v7.2/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`

The Master Profile is the Navigator/Conductor. It establishes the controller, authority model, lane boundaries, runtime-context model, and governance architecture. No participant may treat `00_START_HERE.md`, `DCSE_MANIFEST.yaml`, a project README, a model memory, a database record, or a product repository as higher authority.

`DCSE_MANIFEST.yaml` remains a machine locator and routing index only.

## 2. Universal governance bootstrap sequence

After reading the Master Profile, participants SHALL follow this sequence:

1. **Operative designation**  
   `governance/v7.2/DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md`
2. **Authority synchronization record**  
   `governance/v7.2/DCSE_Master_Profile_Authority_Synchronization_v7-2.md`
3. **Navigation and package front door**  
   `governance/v7.2/00_START_HERE.md`
4. **Doctrine index**  
   `governance/v7.2/registry/DCSE_Doctrine_Index_v7-2.md`
5. **Universal onboarding and access standard**  
   `governance/v7.2/UNIVERSAL_AGENT_ONBOARDING_AND_ACCESS_STANDARD_v7-2.md`
6. **Source authority and persistence routing**  
   D22
7. **Doctrine/task runtime router**  
   D21
8. **AI/model/agent orchestration**  
   D03 when delegation, model routing, tools, or specialist panels are involved
9. **Reserved stop-gates**  
   `governance/v7.2/DCS_LEVEL_0_RESERVED_STOP_GATES_v7-2.md`
10. **Platform execution profile**  
    GitHub, Vercel, Supabase, or other routed platform standard
11. **Task-specific doctrine/methodology** selected by D21
12. **Project repository bootstrap**
13. **Task/product files and assets**
14. **Validation, evidence, reconciliation, closeout**

## 3. Governance repo before product repo

Participants SHALL resolve constitutional and routing controls in the Command Post governance repository before using a product repository.

Sequence:

`MASTER PROFILE -> GOVERNANCE NAVIGATION -> ONBOARDING/ACCESS -> D22 -> D21 -> D03/STOP-GATES/PLATFORM CONTROLS -> PROJECT REPOSITORY -> PROJECT MANIFEST -> TASK FILES -> ASSETS -> EXECUTION`

A product repository does not create governance authority.

## 4. Project repository minimum contract

Every governed product/project repository SHOULD expose a root-level `DCSE_PROJECT_MANIFEST.yaml` or equivalent canonical project manifest containing:

- project/product identity;
- owning entity and lane;
- parent DCSE governance version;
- canonical repository;
- default/production branch;
- project purpose and destination;
- project instructions;
- applicable doctrine/methodology references;
- access profile;
- task/work-order location;
- asset manifest location;
- runtime/deployment surfaces;
- environment-variable names without secret values;
- data/storage dependencies;
- validation commands/checks;
- release/promotion gate;
- rollback/recovery reference;
- Tribunal/evidence destination;
- current status and supersession lineage.

Until a project manifest exists, participants SHALL derive these fields during preflight and mark the project bootstrap PARTIAL rather than inventing them.

## 5. Task file route

Once the project manifest is resolved, task execution loads only the Minimum Effective Context:

1. active Task ID/work order;
2. exact product/task source files;
3. task-routed doctrine/methodology;
4. project architecture and interface contracts;
5. product start declaration and gate state;
6. required assets and asset manifest;
7. applicable test/evidence criteria.

Historical or unrelated repository content is not automatically loaded.

## 6. Media asset architecture

GitHub is the canonical **control/index** surface for governed media workflows, but is not the default warehouse for every large binary.

### 6.1 GitHub stores

- asset manifests;
- source/control metadata;
- hashes and byte sizes;
- small reference images/icons where repository health is unaffected;
- scripts, prompts, captions, transcripts, shot lists, timelines, project files appropriate for Git;
- Git LFS pointer files where LFS is deliberately selected;
- rights/license/release metadata;
- canonical object-storage references;
- derived-output lineage.

### 6.2 Object storage stores

High-resolution or frequently changing:

- video;
- audio;
- image sequences;
- source recordings;
- intermediate renders;
- large design exports;
- model input/output binaries;
- packaged deliverables when binary storage is preferable.

The preferred DCSE pattern is a governed private object-storage bucket with RLS or equivalent authorization. Access may be provided to authorized agents through scoped APIs, authenticated downloads, or time-limited signed URLs. Secret/service credentials SHALL NOT be passed to models.

### 6.3 GitHub size rule

Ordinary Git SHOULD NOT be used as the default home for large media. Files over GitHub's ordinary repository limits require Git LFS or an external object store. Repository health, clone cost, churn, and history growth must be considered before committing binaries.

### 6.4 Media asset manifest

Each product containing workflow media SHOULD maintain a machine-readable manifest such as:

`assets/DCSE_MEDIA_ASSET_MANIFEST.json`

Required fields per asset:

- asset_id;
- project/task ID;
- title/purpose;
- media_type;
- canonical_storage;
- canonical_uri/path;
- git_lfs_oid if applicable;
- sha256;
- byte_size;
- mime_type;
- duration/dimensions when applicable;
- entity/lane;
- classification;
- source/provenance;
- creator/provider;
- rights/license/release status;
- public-release status;
- model/agent access class;
- derived_from;
- version;
- validation status;
- created/updated date.

## 7. "Accessible by all" rule

"All participants" means all **authorized participants whose task and lane permit the asset**, not anonymous/public access.

- public media may use public delivery only after public-release approval;
- internal media uses authenticated access;
- confidential/protected media uses private storage and task/role-bound access;
- PS-origin media remains isolated and SHALL NOT enter general DCSE product storage without explicit authorization and sanitization.

## 8. Asset retrieval contract for agents

An agent receiving a media workflow SHALL be given:

1. asset manifest reference;
2. authorized asset IDs;
3. scoped retrieval mechanism;
4. expected hashes/metadata;
5. permitted transformations;
6. output destination;
7. retention/deletion rule;
8. evidence requirements.

If the agent cannot retrieve the binary through an authenticated supported surface, it SHALL report access as unavailable rather than fabricate asset access.

Before any product/media build, resolve the `DCSE Product Start Gate and Build Declaration Standard v1`. Missing required brand/persona/current-image/background/source assets or unresolved release-target URL/destination SHALL trigger `DCS_E_PRODUCT_START_ESCALATION`.

## 9. Repository handoff

After governance bootstrap, the participant moves to the designated project repository and SHALL verify:

- exact repository full name;
- branch/ref;
- project manifest;
- current task/work order;
- source files;
- asset manifest;
- dependencies;
- current commit;
- local/runtime drift;
- exit criteria.

## 10. Completion

A task is not COMPLETE merely because the participant found governance or product files. Completion requires the task-specific evidence required by D21, D22, the applicable platform profile, and the project manifest.

**Structure Precedes Scale. Master Profile Precedes Routing. Routing Precedes Project Execution.**
