---
dcse_zone: authority
dcse_authority_level: CANDIDATE
dcse_document_id: DCSE-D21
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: DCSE
dcse_required_approval: DCS_LEVEL_0_EXACT_DIFF
dcse_source_lineage: governance/v7.1/source/doctrines/D21_Doctrine_Runtime_Engine.md
---

# DCSE Doctrine D21: Doctrine Runtime Engine

## 1. Position Under the Master Profile

D21 is subordinate to `DCSE_Master_Profile_v7.1.md` and operates after D22 confirms the source and authority state.

The Master Profile is the constitutional entry point. D21 answers the downstream question: which doctrines and controls apply to the current task, in what order, and with what evidence?

D21 routes doctrine. D21 does not create constitutional authority, promote doctrine, expand access, waive stop-gates, or supersede the Master Profile.

## 2. Runtime Order

Every substantive task follows this order:

1. Load the promoted Master Profile.
2. Use D22 to verify source identity, authority state, canonical path, and drift status.
3. Use D21 to classify the task and select the minimum effective doctrine set.
4. Load the applicable onboarding, lane, subject, access, and destination controls.
5. Execute only within the authorized scope.
6. Validate evidence, security, lane isolation, and completion.
7. Produce a Doctrine Consideration Log and required receipts.

A missing Master Profile or unresolved D22 authority conflict blocks D21 routing.

## 3. Task Declaration

Before execution, D21 must establish:

- task ID;
- lane;
- entity;
- task type;
- destination;
- requested action;
- artifact type;
- confidentiality;
- authority holder;
- executing model or agent;
- access level;
- systems involved;
- secret exposure;
- PS exposure;
- approval requirement;
- rollback or recovery requirement;
- expected deliverables;
- exit criteria.

Reasonable operational details may be inferred when risk is low. Authority, lane, secrets, PS exposure, production impact, and destructive action may not be inferred silently.

## 4. Dynamic Doctrine Router

D21 selects the minimum effective doctrine set by evaluating:

1. Master Profile route.
2. Lane.
3. Task type.
4. Destination.
5. System and access type.
6. Risk and confidentiality.
7. Required methodology.
8. Promotion and release posture.
9. Model capability.
10. Source availability and freshness.

The router must include only the doctrines needed for the task, plus required constitutional, security, lane, and promotion controls.

## 5. Required Doctrine Routes

| Trigger | Required route |
| --- | --- |
| Any substantive task | Master Profile, D22, D21 |
| Agent startup or access | `UNIVERSAL_AGENT_ONBOARDING_AND_ACCESS_STANDARD.md` |
| Candidate promotion or baseline | D05 |
| GitHub, Tribunal, or communications | D04 |
| File placement, retention, device, or repository boundary | D06 |
| AI routing, prompt wrappers, or model delegation | D03 |
| Database, Supabase, schema, migration, RLS, cron, or storage | D15 and Access Governance Check |
| Campaign, website copy, social, or public communications | D07, D08, D09, and D10 as applicable |
| HTML, Wix, or application build | D11 and applicable product or media methodology |
| Product assembly | D20 |
| Media or audio/video production | D18 and applicable brand doctrine |
| Visual creation | D19 and applicable brand doctrine |
| General structured analysis | D17 and D02 as applicable |
| PS litigation | Isolated PS route only, including D13 and D14 |
| PPR | Isolated PPR route only |

Source files under `source/doctrines/` are adopted subject material. Their active use is bounded by the Master Profile and any V7.1-normalized doctrine.

## 6. Lane Firewall

D21 must exclude any doctrine, source, record, or artifact outside the declared lane unless a higher authority expressly permits cross-lane use.

PS and PPR content may not enter general routing. Where PS-locked material appears outside PS mode, D21 must stop the affected task and issue:

Governance Stop-Gate: PS-locked material detected. This content must remain isolated in PS mode and cannot be merged into TI, SC, public, or product lanes.

## 7. Capability and Access Routing

D21 routes work by verified capability, access, risk, and accountability, not by model name alone.

Before tool-backed work, D21 must verify:

- the tool or connector exists;
- the agent has the required permission;
- access is scoped to the task;
- credentials are not exposed;
- the action is read, create, update, delete, deploy, migrate, publish, or promote;
- approval and rollback requirements are satisfied.

A model may propose work beyond its access. It may not claim execution without tool-backed evidence.

## 8. Doctrine Consideration Log

Every substantive task must produce a DCL containing:

```yaml
dcl:
  task_id: ""
  timestamp: ""
  model_or_agent: ""
  lane: ""
  task_type: ""
  destination: ""
  authority_source:
    master_profile: ""
    d22_status: ""
  loaded: []
  applied: []
  evaluated_not_applied: []
  excluded_by_lane: []
  excluded_by_access: []
  missing: []
  contradictions: []
  security:
    secret_scan: PASS
    ps_scan: PASS
    access_check: PASS
  validation: []
  evidence: []
  exit_status: "COMPLETE | PARTIAL | BLOCKED | CANDIDATE"
```

The DCL is an audit record. It does not create authority.

## 9. Evidence and Completion Gate

A task may be marked complete only when:

1. scope and completed work match;
2. required artifacts are retrievable;
3. validation was performed;
4. failures and skipped work are disclosed;
5. security and lane scans pass;
6. required review is attributable;
7. rollback or recovery exists where required;
8. GitHub and runtime records reconcile where applicable;
9. promotion state is stated accurately;
10. remaining blockers are named.

A statement of completion without evidence is non-pass.

## 10. Cybersecurity Baseline

Before delivery, commit, publication, deployment, or registry write, D21 must check for:

- passwords;
- tokens;
- API keys;
- private keys;
- connection strings;
- service-role credentials;
- private URLs;
- recovery codes;
- MFA data;
- unsafe client-side secrets;
- unvalidated input;
- XSS or injection risk;
- unrestricted CORS;
- unauthorized data access.

Any secret exposure blocks delivery until safely remediated.

## 11. Preview and Test Routing

Browser-renderable work requires a live preview or documented equivalent before completion.

Code requires syntax and relevant behavioral tests.

Database work requires schema inspection, transaction safety, rollback, and authorized execution evidence.

Governance work requires authority, contradiction, zone, and promotion review.

Evidence not re-performed by the reviewer must be disclosed.

## 12. Missing Doctrine and Conflict Handling

If a required doctrine is missing, unreadable, stale, or contradictory:

1. identify the missing or conflicting source;
2. identify the affected task scope;
3. preserve available evidence;
4. block only the affected action unless a reserved stop-gate requires broader halt;
5. route source and authority questions to D22;
6. route constitutional conflicts to DCS Level 0;
7. record the issue in the DCL and applicable Tribunal record.

D21 may not invent missing doctrine from model memory.

## 13. Confluence Rule

When multiple routed doctrines apply, the strictest applicable safety, evidence, lane, access, and promotion requirement controls.

A lower-level task description, instruction, ledger, or execution record cannot waive Master Profile authority, D05 promotion evidence, D21 runtime logging, D22 source reconciliation, lane isolation, or security controls.

This rule is standing doctrine only after this exact D21 version is promoted. It must not remain embedded as controlling policy in an execution register.

## 14. Source Lineage

This V7.1-normalized doctrine derives from:

`governance/v7.1/source/doctrines/D21_Doctrine_Runtime_Engine.md`

The source copy remains preserved as lineage. Its V6.9 status and parent references do not control V7.1 after this normalized doctrine is promoted.

## 15. Exit Criteria for Promotion

D21 is eligible for promotion only when:

1. the Master Profile exact diff is approved;
2. D22 exact diff is approved;
3. this exact D21 diff is approved;
4. the required route paths exist;
5. the DCL schema is validated;
6. CI verifies zone restrictions;
7. execution and evidence files no longer claim policy authority;
8. the runtime registry records the canonical path, commit, hash, and promotion state.