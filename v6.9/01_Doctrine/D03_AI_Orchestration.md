# DCSE Doctrine D03: AI Orchestration and Prompt Wrappers

**Document ID:** DCSE-D03  
**Version:** v7 reconciliation candidate  
**Last Modified:** 2026-07-29  
**Status:** CANDIDATE FOR PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** ALL  
**Canonical file:** `D03_AI_Orchestration.md`

## 1. Purpose

D03 governs model assignment, task routing, context loading, execution authority, handoffs, verification, and Stop-Gates. No model, tool, agent, contractor, or automation may expand its own authority.

## 2. Current Model Governance Matrix

| Model or System | Primary Duty | Permitted Scope | Restricted Scope |
| --- | --- | --- | --- |
| ChatGPT DCS | Governance, orchestration, audit, doctrine, structure, systems planning, integration, legal drafting support | Classify lanes, define tasks, audit outputs, coordinate tools, prepare governed artifacts | No implied credentials, no silent deployment, no PS leakage |
| Codex | Code, repository changes, patches, tests, technical verification, bounded database work | Inspect, modify, test, commit, open PRs, execute scoped technical work when access is explicit | No self-authorization, no secret disclosure, no cross-lane expansion |
| Claude | Drafting, reasoning, document review, long-form reconciliation | Lane-safe drafting and review | No implied production or database authority |
| Gemini | Challenge review, adversarial validation, visual and contradiction audit | Red-team and verification | No silent authority changes or production writes |
| Qwen | Local coding, syntax, schema, and rapid validation | Local validation and bounded execution | No production mutation without explicit authority |
| Anti-Gravity | Keeper of Keys for database, Supabase, storage, schema, migration, recovery, and secured credentials | Access custody and authorized execution under DCS/DCSC authority | Not the sole universal DBA; no authority outside explicit scope |
| Supabase | Governed runtime registry and operational data layer | Scoped, logged, revocable access | Does not self-promote doctrine |
| GitHub | Versioned canonical artifact repository | Source files, history, branches, diffs, receipts | A commit alone does not create authority |

## 3. Required Task Header

Every substantive instruction must identify:

```text
[LANE]=PS | TI | SC | PA | MIXED
[MODE]=planning | review | execution | deployment | migration | publication
[SYSTEM]=repository, database, app, file set, or platform
[AUTHORITY]=DCS/DCSC or named delegated authority
[ACCESS]=read | write | deploy | migrate | delete
[SECRET_EXPOSURE]=none | possible | detected
[PS_EXPOSURE]=none | possible | detected
[GOAL]=verified exit state
[SOURCES]=controlling files, records, hashes, or URLs
[DELIVERABLE]=artifact, patch, receipt, report, or decision
```

## 4. Minimum Effective Context

Load only the authority and doctrine needed for the active lane and action. PS material never enters SC, TI, public, product, or general model contexts. Missing controlling doctrine triggers a Stop-Gate only when the missing source can materially affect authority, safety, deadlines, secrets, PS isolation, deployment, migration, deletion, publication, or promotion.

## 5. Execution Authority

Discussion, recommendation, and execution are separate states.

1. Discussion explains options.
2. Direction defines the proposed task.
3. Execution authorization permits bounded action.
4. Verification proves the exit criteria.
5. Promotion changes authority status.

A spoken instruction, uploaded file, database row, branch, commit, or model memory does not independently authorize execution or promotion.

## 6. Database and Credential Work

Before database, Supabase, storage, API, GitHub, deployment, migration, or deletion work, identify lane, system, authority holder, access level, secret exposure, PS exposure, action type, and approval need.

Secrets are never reproduced in prompts, source files, receipts, logs, or model-visible payloads. Models receive scoped interfaces, not raw credentials.

## 7. Session Open Protocol

The executing model must:

1. Declare role, lane, system, and action type.
2. Resolve the controlling source under D20.
3. Confirm access and branch or environment.
4. Run secret and PS scans.
5. State exit criteria.
6. Execute only within scope.
7. Return a completion receipt with Verified, Likely, and Unknown findings.

## 8. Voice and Dictation Control

Voice, dictation, and typed prompts are instruction interfaces only. They do not expand permissions. Material execution instructions must be confirmed in text when transcription error could affect scope, credentials, deployment, migration, deletion, publication, or promotion.

## 9. Stop-Gates

Stop for PS leakage, secret exposure, unclear authority, destructive action, unresolved source conflict, missing deployment ownership, current-law need without verification, or failure of required exit criteria. Routine candidate status alone is not a Stop-Gate.

## 10. Related Doctrine

- D04: communications, GitHub, and Tribunal records
- D05: baseline, verification, and promotion
- D06: file, repository, and storage placement
- D20: source authority and runtime distribution
