# DCSE Doctrine D22: Source Authority and Runtime Distribution

**Document ID:** DCSE-D22  
**Version:** v1.0 reconciliation candidate  
**Created:** 2026-07-29  
**Status:** CANDIDATE PENDING REVIEW  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC  
**Canonical file:** `D22_Source_Authority_Runtime_Distribution.md`

## 1. Purpose
D22 resolves source-of-truth conflicts among DCS decisions, promoted Markdown, GitHub, DCSE-DDNA Supabase, SC Command Post Supabase, local files, model uploads, retrieval indexes, and deployments.

## 2. Authority Hierarchy
1. DCS or DCSC recorded decision.
2. Promoted Master Profile.
3. Promoted doctrine.
4. Promoted registries and authority records.
5. Approved baselines.
6. Governed projects and artifacts.
7. Candidates and drafts.

No platform, model, database, repository, deployment, file, branch, commit, embedding, retrieval result, or memory creates authority by existence.

## 3. Three-Part Source Model
### 3.1 Authority
Authority is the DCS or DCSC promotion decision and its recorded scope.

### 3.2 Canonical Artifact
GitHub stores the versioned canonical artifact for doctrine and governed source files. Canonical identity is repository + path + commit SHA + content SHA-256. A GitHub commit is evidence and distribution infrastructure. It becomes controlling only when linked to the applicable promotion state.

### 3.3 Constitutional Runtime Registry
DCSE-DDNA Supabase is the constitutional runtime governance registry. It stores governance directives, canonical references, promotion state, integrity hashes, model read scopes, acknowledgements, queues, execution records, and cross-database references. Supabase does not replace the canonical artifact. It points to and verifies it.

## 4. Operational Supabase Separation
The SC Command Post Supabase project stores application and operational state. It may retain governed references to DCSE-DDNA authority, but it does not become the constitutional doctrine source by copying a record.

## 5. Required Runtime Doctrine Record
Every doctrine record distributed through Supabase must include doctrine ID, canonical filename, version, lane, classification, promotion status, promotion type, promoted by, promotion timestamp, GitHub repository, GitHub path, GitHub commit SHA, content SHA-256, supersedes, superseded by, model read scope, PS restriction, secret scan status, and runtime status.

Runtime status values are ACTIVE, CANDIDATE, SUPERSEDED, ARCHIVED, DRIFT, and BLOCKED.

## 6. Model Access
Models access doctrine through approved GitHub, operator-upload, scoped Supabase retrieval, or approved local source methods. Access must be explicit, lane-scoped, logged when applicable, and revocable. No model receives unrestricted database access or implied permissions.

## 7. Retrieval and Embeddings
Search results, embeddings, chunks, summaries, and retrieved passages are access aids. They are not authority. Before use, verify doctrine ID, version, lane, classification, promotion state, source commit, and hash.

## 8. Conflict Resolution
When sources disagree: preserve both statements; identify each source and status; compare promotion records; compare GitHub commit and content hash; compare Supabase runtime reference; classify integrity or status mismatch as DRIFT; rely on the last verified promoted source; reconcile and issue a receipt.

## 9. July 9 Governance Hub Reconciliation
The July 9 DDNA Governance Hub milestone remains valid as follows: DCSE-DDNA Supabase is the constitutional runtime governance repository; GitHub is the versioned canonical artifact repository; DCS or DCSC promotion creates authority; other repositories maintain governed references and operational state.

## 10. Promotion and Synchronization Sequence
Draft artifact -> validation -> DCS Level 0 promotion decision -> GitHub canonical commit and hash -> Supabase runtime registry update -> local audit synchronization -> model distribution -> verification receipt.

No synchronization step independently promotes doctrine.

## 11. Drift Response
When DRIFT is detected, block reliance on the mismatched copy, retain the last verified promoted version, identify affected models and systems, correct the canonical artifact or runtime reference, update hashes and status, and record the reconciliation receipt.

## 12. Restrictions
PS content remains isolated. Sensitive access material is excluded from doctrine payloads and retrieval responses. Runtime access does not imply write authority. A database row does not promote doctrine. A GitHub merge does not promote doctrine without DCS Level 0 approval. A model summary does not replace the source.

## 13. Related Doctrine
D03 model orchestration and access; D04 communications and receipts; D05 baselines and promotion; D06 file and storage placement; D15 database administration; D20 Product Assembly.

## 14. Promotion Boundary
This file is a candidate only. It does not alter Product Assembly D20, D17-D21, the doctrine index, Supabase, or any production system. DCS Level 0 review is required before promotion.