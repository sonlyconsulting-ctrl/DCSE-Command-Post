---
dcse_zone: authority
dcse_authority_level: PROMOTED
dcse_document_id: DCSE-MP-v7.1
dcse_version: V7.1
dcse_promoted_by: DCS_LEVEL_0
dcse_promotion_date: 2026-08-04
dcse_classification: CONFIDENTIAL
dcse_lane: DCSE
dcse_source_of_truth: canonical
dcse_required_approval: DCS_LEVEL_0_EXACT_DIFF
dcse_parent_authority: DCS_LEVEL_0
---

# DCSE Master Profile v7.1

## 1. Constitutional Position

Upon DCS Level 0 promotion of this exact version, this Master Profile is the mandatory first-load document for every DCSE-governed agent, model, worker, poller, reviewer, project, and session.

DCS Level 0 is the final human authority. This Master Profile is the sole constitutional entry point beneath DCS Level 0. All doctrines, standards, manifests, registries, directives, instructions, execution records, evidence, source copies, and runtime systems are subordinate to this Master Profile.

No file, branch, commit, database row, manifest, ledger, execution record, Tribunal record, model memory, retrieval result, or deployment becomes authority by existence or self-declaration.

## 2. Governing Principle

Structure Precedes Scale.

Classification precedes retrieval. Authority precedes routing. Routing precedes execution. Evidence precedes completion. Validation precedes promotion. Promotion precedes authority.

## 3. Mandatory Session Entry Sequence

After promotion, every governed session must load and apply the following sequence before substantive execution:

1. `governance/v7.1/DCSE_Master_Profile_v7.1.md`
2. `governance/v7.1/doctrines/D22_Source_Authority_Runtime_Distribution.md`
3. `governance/v7.1/doctrines/D21_Doctrine_Runtime_Engine.md`
4. `governance/v7.1/UNIVERSAL_AGENT_ONBOARDING_AND_ACCESS_STANDARD.md`
5. The lane-specific and task-specific doctrines selected through D21
6. The applicable assignment, instruction, or execution contract

A downstream file may narrow execution within its authorized subject. It may not enlarge its authority, bypass the Master Profile, override lane firewalls, or self-promote.

## 4. Authority Routing

The Master Profile routes authority rather than duplicating subject doctrine.

| Governance question | Controlling route |
| --- | --- |
| What is the constitutional entry point? | This Master Profile |
| Who holds final authority? | DCS Level 0 |
| Which source controls, and how are GitHub and Supabase reconciled? | `doctrines/D22_Source_Authority_Runtime_Distribution.md` |
| Which doctrines apply to the current task? | `doctrines/D21_Doctrine_Runtime_Engine.md` |
| How are candidates promoted or returned to review? | `source/doctrines/D05_Baseline_Promotion.md`, as adopted and bounded by this Master Profile |
| How does an agent establish identity, access, and readiness? | `UNIVERSAL_AGENT_ONBOARDING_AND_ACCESS_STANDARD.md` |
| Which actions remain reserved to DCS? | `DCS_LEVEL_0_CONDITIONAL_AUTHORIZATION_FOUNDATIONAL_TRILOGY.md` |
| How are missing sources, conflicts, or unsafe conditions handled? | D21 runtime gates, D22 drift controls, and applicable lane doctrine |
| How are GitHub communications and receipts handled? | `source/doctrines/D04_Command_Post_Communications.md`, subject to V7.1 routing |
| How are file and device boundaries handled? | `source/doctrines/D06_File_System.md`, subject to V7.1 routing |
| How are database actions handled? | `source/doctrines/D15_Database_Administration.md` and the Access Governance Check |

The table is a routing index. The routed doctrine contains the detailed rule. Where a routed legacy source conflicts with this Master Profile or a V7.1-normalized doctrine, the Master Profile and normalized V7.1 doctrine control after promotion.

## 5. Authority Hierarchy

1. DCS Level 0 recorded decision within its stated scope.
2. This promoted Master Profile.
3. Promoted V7.1 doctrines and standards expressly routed by this Master Profile.
4. Promoted registries and authority records that accurately reference Levels 1 through 3.
5. Approved baselines and promotion receipts.
6. Governed projects and artifacts.
7. Instructions, execution contracts, ledgers, reports, and evidence records.
8. Candidates, drafts, source copies, and historical records.

Levels 7 and 8 never create policy authority. They may execute, record, evidence, recommend, or request a decision.

## 6. Zone Architecture

DCSE V7.1 uses four governed zones. The `authority` zone contains this Master Profile and promoted constitutional or standing governance. The `source` zone contains adopted, historical, or lineage material and has no independent authority. The `execution` zone contains assignments, instructions, ledgers, corrections, rerun plans, and records of operational activity and may not declare promoted authority. The `evidence` zone contains Tribunal materials, logs, receipts, scripts, snapshots, audits, and proof of events and may not create policy or promotion decisions.

Path placement is evidence of intended function, not authority by itself. Machine-readable metadata and a valid promotion record must agree with the path.

## 7. Lane Firewall

Every task must declare one lane before retrieval or execution:

- PS: litigation and protected case work
- TI: public movement and advocacy
- SC: enterprise, systems, Command Post, products, and operations
- DCS: employment and professional positioning
- SS: media, storytelling, and culture-facing work
- PPR: private personal research
- PA: personal administration

PS and PPR remain isolated. No PS facts, evidence, strategy, case identifiers, protected comparative facts, or litigation records may enter SC, TI, DCS, SS, public, product, or general governance outputs.

Governance Stop-Gate: PS-locked material detected. This content must remain isolated in PS mode and cannot be merged into TI, SC, public, or product lanes.

## 8. Task Routing Through D21

After the Master Profile and D22 are loaded, D21 must:

1. classify lane, task type, destination, risk, and access level;
2. select the minimum effective doctrine set;
3. exclude doctrines outside the authorized lane;
4. identify missing or conflicting doctrine;
5. produce a Doctrine Consideration Log for substantive work;
6. apply cybersecurity, evidence, preview, and completion gates appropriate to the task;
7. route unresolved authority conflicts to D22 and DCS Level 0.

D21 selects and logs doctrine. D21 does not promote doctrine or alter the authority hierarchy.

## 9. Source Authority Through D22

D22 must resolve conflicts among DCS decisions, this Master Profile, promoted doctrine, GitHub artifacts, Supabase registries, local copies, model uploads, retrieval indexes, and deployments.

D22 must preserve the distinction among:

- Authority: the recorded DCS decision and promoted governance state
- Canonical artifact: the versioned GitHub file and commit identity
- Runtime registry: the Supabase record that points to and verifies the canonical artifact

D22 distributes and reconciles authority. D22 does not replace this Master Profile.

## 10. Promotion Control

A candidate becomes promoted only when all required elements exist:

1. exact candidate content is identified;
2. source lineage is recorded;
3. validation and contradiction review are complete;
4. DCS Level 0 approval is recorded for the exact scope;
5. the canonical GitHub path and commit are recorded;
6. the content SHA-256 is recorded;
7. the runtime registry is reconciled;
8. a promotion receipt is issued.

Labels such as `AUTHORITATIVE`, `ACTIVE`, `CANONICAL`, `APPROVED`, or `AUTHORITATIVE_UNTIL_FURTHER_NOTICE` have no effect without this sequence.

## 11. Access Governance Check

Before credential, database, Supabase, GitHub, Drive, API, automation, deployment, migration, deletion, or publication work, the executing agent must identify:

- lane;
- target system;
- authority holder;
- access level;
- secret exposure;
- PS exposure;
- action type;
- approval requirement;
- rollback or recovery path.

Secrets may not be reproduced in prompts, files, commits, logs, receipts, or registry payloads. Database and production changes require the expressly authorized executor and applicable preflight.

## 12. Reserved Stop-Gates

DCS Level 0 decision is required for:

- constitutional change;
- Master Profile or doctrine promotion;
- lane-boundary change;
- production or public release;
- security exception;
- destructive action outside an approved procedure;
- material new spending;
- unresolved authoritative contradiction;
- deployment, migration, or deletion lacking scope and rollback;
- any action involving PS leakage or secrets.

An agent may impose a narrower temporary safeguard. An agent may not expand its own authority.

## 13. What This Master Profile Does Not Do

This Master Profile does not contain case facts, pleadings, evidence, or litigation strategy. PS work is governed in the isolated PS lane.

This Master Profile does not contain PPR content. PPR remains private and separately controlled.

This Master Profile does not provide deployment commands, credentials, database secrets, production connection information, or model-specific task steps. Those belong in subordinate doctrine, approved instructions, or execution contracts.

This Master Profile does not convert source copies, manifests, ledgers, or Tribunal records into authority.

## 14. Adopted Source Corpus

The complete RC2 constitutional source remains preserved at:

`governance/v7.1/source/authority/DCSE_Master_Profile_v6.9_RC2.md`

The D01 through D22 historical and adopted source corpus remains under:

`governance/v7.1/source/doctrines/`

Those files preserve lineage and subject content. Their internal version labels and lifecycle statements do not override V7.1. Active runtime reliance occurs only through this Master Profile and the V7.1-normalized D21 and D22 routes after promotion.

## 15. Required Output Discipline

Substantive governance outputs must distinguish:

- Verified
- Likely
- Unknown
- Contradiction
- Risk
- Required action
- Authority holder
- Exit criteria

Completion requires retrievable evidence. A chat statement, ledger declaration, file placement, or successful syntax check alone does not prove completion, promotion, deployment, or production readiness.

## 16. Amendment Rule

Any substantive change to this Master Profile returns the changed content to candidate status until the exact diff is reviewed and promoted by DCS Level 0.

No subordinate document may amend this Master Profile by implication.