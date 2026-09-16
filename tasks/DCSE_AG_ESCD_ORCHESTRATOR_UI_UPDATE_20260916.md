# AG Execution Packet: ESCD Orchestrator Directives + Bounded UI/UX Update

**Task ID:** DCSE-AG-ESCD-RUNTIME-UI-20260916-01  
**Lane / Entity:** SC / DCSE  
**Executor:** Anti-Gravity, Junior DBA / delegated executor  
**Authority:** DCS Level 0 direction; v7.2 runtime controls  
**Mode:** MODIFY existing ESCD. Do not rebuild or re-theme.

## 1. Required source load

Read current canonical/working v7.2 sources:
- `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`
- `execution/DCSE_RUNTIME_DIRECTIVE_CAPTURE_AND_ESCD_ROUTING_STANDARD_v1.md`
- `web/DCSE_SC_SS_SHARED_SITE_CHROME_STANDARD_v1.md`
- `DCSE_Runtime_Harmony_Task_Traceability_and_Navigable_Closeout_v7-2.md`
- D21 / D22
- current ESCD runtime/UI implementation
- current `public.items`, `pm_tasks`, `pm_artifacts`, `pm_decisions`, `pm_risks`, `pm_blockers` contracts

Do not infer schema changes.

## 2. Directive behavior to expose

ESCD must support the Orchestrator contract:

`CLASSIFY -> SEARCH -> EXISTING/NEW -> UPDATE/LINK or CREATE -> RETURN EVIDENCE`

Allowed result states:
- `EXISTING_UPDATED`
- `EXISTING_LINKED`
- `NEW_CREATED`
- `BLOCKED`

Matching order:
1. exact task code/Task ID;
2. exact artifact/source key;
3. exact GitHub/external evidence identity;
4. normalized title + project/lane/entity;
5. semantic similarity -> REVIEW when uncertain.

Do not silently merge ambiguous records.

## 3. Bounded UI/UX changes

Preserve the current ESCD visual system unless a defect blocks these functions.

Add/confirm on task/knowledge detail surfaces:

### Identity / routing
- Task/object ID;
- object type;
- lane;
- entity;
- priority;
- lifecycle/status;
- existing-vs-new resolution;
- originating directive/source.

### Evidence navigation
Clickable evidence/JUMP references when present:
- GitHub issue;
- GitHub commit/path;
- Supabase/runtime record;
- Tribunal;
- deployment/review URL;
- related doctrine/standard;
- rollback/history.

### Relationships
- parent task/project;
- related/child tasks;
- related knowledge/assets;
- duplicate/link relationship;
- superseded-by where applicable.

### Synchronization state
Display compact state such as:
- GitHub: linked/unlinked;
- ESCD/PM: linked;
- DDNA: registered/not registered;
- RAG: chunks / embeddings / retrieval-evaluated;
- runtime/deployment evidence state.

Do not imply authority from a green sync badge.

### Work vs knowledge
Provide clear filtering or grouping for:
- ToDo/Task;
- Idea;
- Asset/Evidence;
- DCSE governance/knowledge.

Do not create duplicate tables merely for presentation.

## 4. Directive Capture surface

Add a compact internal-only way to see:
- active Level 0 express directive;
- canonical v7.2 path;
- operational effect;
- related executable rule status;
- ESCD sync state;
- unresolved implementation item.

This may be a filtered view rather than a new page if current ESCD supports it.

## 5. DDNA / RAG status

For registered learning items expose when available:
- source registered;
- chunk count;
- embedded count;
- retrieval evaluation status;
- authority class;
- sensitivity/lane.

Current Persona Atlas orchestration wrap should display:
- source registered;
- 10 chunks;
- 0 embeddings until that changes;
- phase2a_test;
- observed evidence, not doctrine authority.

## 6. Bulk media capture integration

Do not build a full media manager in this pass.

Add a task/evidence entry and, if ESCD already has an appropriate workflow-launch affordance, expose the bulk media tool:
- `scripts/dcse_media_codebase_bulk_capture.py`
- config template under `governance/v7.2/media/`

Expected outputs:
- JSON manifest;
- CSV manifest;
- duplicate groups;
- code-consumption references;
- staged-copy states.

If no safe existing launch mechanism exists, show the tool/evidence link only. Do not invent privileged local execution from the web UI.

## 7. Current queue to reconcile

Ensure these are visible and deduplicated:
- CTJ Family Completion;
- DDNA/RAG embed + retrieval evaluation;
- Persona Estate Reconciliation;
- Claude Design runtime/CLI/MCP gap analysis;
- Creative Asset Architecture;
- Short-Video Orchestration at Scale;
- Acceptance Completeness Gate;
- Bulk Media + Codebase Capture;
- DCS Employment Proactive Targeted Restart;
- Persona Atlas Test 2 reuse candidate.

## 8. Non-scope / stop gates

AG shall not:
- redesign ESCD;
- independently alter RLS/access/security;
- create new secrets/credential paths;
- weaken auth;
- create new schemas without CTO/Sr DBA approval;
- promote candidate rules;
- publish public UI;
- expose PS/protected material.

If the existing schema cannot support a required field without architecture work, report:
`BLOCKED_SCHEMA_DECISION_REQUIRED`
with exact field/use case.

## 9. Validation

Minimum tests:
1. exact Task ID finds existing record;
2. new Task ID creates one record only;
3. repeated same intake updates/links rather than duplicates;
4. semantic near-match remains REVIEW, not auto-merge;
5. evidence links render/navigate;
6. work vs knowledge filters function;
7. directive status appears without implying promotion;
8. DDNA/RAG counts reflect live state;
9. mobile/desktop layout remains usable;
10. no console errors;
11. no PS/secret leakage.

## 10. Closeout evidence

Return:
- changed files/commit;
- review/deployment URL if available;
- before/after screenshots;
- tests;
- exact ESCD records updated/created;
- any schema blocker;
- unresolved findings;
- rollback path.

Target:
`ESCD_ORCHESTRATOR_RUNTIME_UI_READY_FOR_DCS_REVIEW`
