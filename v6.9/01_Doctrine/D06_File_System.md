# DCSE Doctrine D06: File System, Repository, and Storage Governance

**Document ID:** DCSE-D06  
**Version:** v7 reconciliation candidate  
**Last Modified:** 2026-07-29  
**Status:** CANDIDATE FOR PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC / PS isolation controls  
**Canonical file:** `D06_File_System.md`

## 1. Purpose

D06 governs where files, doctrine, registries, receipts, databases, backups, deployments, and runtime references belong. Structure precedes movement, duplication, cleanup, synchronization, and scale.

## 2. Controlled Storage Layers

| Layer | Role | Authority Rule |
| --- | --- | --- |
| DCS decision record | Human authority | Controls promotion, exceptions, and delegated scope |
| GitHub | Versioned canonical artifact repository | Stores promoted and candidate source files, history, branches, diffs, and receipts |
| DCSE-DDNA Supabase | Constitutional runtime governance registry | Stores promoted directives, references, promotion state, runtime access, acknowledgements, queues, and model retrieval records |
| SC Command Post Supabase | Operational application repository | Stores SC application data, task state, operational activity, and governed references |
| Local Hub | Working and audit copy | Supports local execution, packaging, receipts, and reconciliation |
| Offline PS Spoke | PS-only protected storage | Stores PS evidence, strategy, litigation facts, and protected work product |
| Deployment platforms | Published execution state | Run approved applications and services; do not create doctrine authority |

## 3. Source Placement Rule

Promoted doctrine must have one canonical artifact path in GitHub and one matching constitutional runtime record in DCSE-DDNA Supabase. The Supabase record must include the GitHub repository, path, commit SHA, content hash, lane, classification, promotion state, and model read scope.

The local Hub may mirror the promoted artifact for audit and execution. A local copy does not supersede the promoted source without a recorded promotion.

## 4. Hub Structure

The v6.9 Hub retains these controlled directories:

```text
00_Authority
01_Doctrine
02_Registry
03_Communications
04_Command_Packets
05_Tribunal_Inbox
06_Baselines
07_Projects
08_Templates
09_Tools
10_Archive
11_Receipts
12_Diffs
13_Open_Items
```

Newer governed project structures may extend this layout when the controlling project or doctrine defines the child structure. Extension does not silently amend the constitutional Hub.

## 5. Intake and Classification

Every incoming item must be classified before placement:

1. identify lane;
2. identify source and provenance;
3. run secret scan;
4. run PS leakage scan;
5. determine authority and lifecycle state;
6. fingerprint or hash the item;
7. assign canonical destination;
8. record exclusions and duplicates;
9. move, copy, or register only after classification.

Ambiguous material routes to `13_Open_Items` or an equivalent governed quarantine state.

## 6. PS Isolation

PS material does not enter general GitHub repositories, SC Supabase projects, public deployments, TI assets, product repositories, or general model retrieval. PS material remains in the approved PS environment. Only sanitized metadata, integrity hashes, or expressly approved references may cross the firewall.

## 7. Secrets and Credentials

Secrets, passwords, tokens, service-role keys, recovery codes, MFA data, private connection strings, and unrestricted private URLs do not enter GitHub, ordinary Supabase content tables, model prompts, shared receipts, or public artifacts.

Credential references use names and secured-location identifiers only.

## 8. Device and Executor Controls

A device, model, agent, contractor, or automation receives no implied access from file visibility. Access must be explicit, scoped, logged, and revocable.

Before storage, migration, backup, deletion, or synchronization work, identify:

- lane;
- system;
- authority holder;
- access level;
- secret exposure;
- PS exposure;
- action type;
- approval need;
- rollback or recovery path.

## 9. Cleanup and Deletion Pipeline

```text
Inventory -> Classification -> Authority Check -> Duplicate Analysis ->
Cleanup Proposal -> Required Approval -> Execution -> Verification -> Receipt
```

No automated cleanup may bypass classification, retention, PS isolation, backup, and recovery controls.

## 10. Duplicate and Drift Rules

A duplicate is determined by content identity and authority, not filename alone. A hash match may support deduplication, but deletion still requires retention and authority review.

A mismatch among GitHub, Supabase, local audit copy, or deployment is `DRIFT`. D20 and D05 control reconciliation.

## 11. Backup and Recovery

Backups must identify source system, timestamp, encryption status, retention period, storage destination, restoration procedure, and verification result. A backup claim is incomplete until restoration or recoverability is validated to the required level.

## 12. Related Doctrine

- D03: model orchestration and access boundaries
- D04: communications and GitHub records
- D05: baseline, promotion, and drift
- D15: database administration
- D20: source authority and runtime distribution
