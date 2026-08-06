# DCSE Doctrine D22: Source Authority and Runtime Distribution

**Document ID:** DCSE-D22  
**Version:** v7.0  
**Created Date/Time:** 2026-07-29T18:07:30-04:00  
**Last Doc Modified Date/Time:** 2026-07-29T18:07:30-04:00  
**Status:** CANDIDATE PENDING DCS LEVEL 0 PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC  
**Canonical file:** D22_Source_Authority_Runtime_Distribution.md  
**Doctrine Description:** D22 governs source-of-truth identity and the controlled distribution of promoted doctrine among DCS decisions, GitHub canonical artifacts, Supabase runtime registries, local audit copies, model retrieval, and deployments. It is separate from Product Assembly D20.  
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

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

Runtime status values are `ACTIVE`, `CANDIDATE`, `SUPERSEDED`, `ARCHIVED`, `DRIFT`, and `BLOCKED`.

## 6. Model Access

Models access doctrine through approved GitHub, operator-upload, scoped Supabase retrieval, or approved local source methods. Access must be explicit, lane-scoped, logged when applicable, and revocable. No model receives unrestricted database access or implied permissions.

## 7. Retrieval and Embeddings

Search results, embeddings, chunks, summaries, and retrieved passages are access aids. They are not authority. Before use, verify doctrine ID, version, lane, classification, promotion state, source commit, and hash.

## 8. Conflict Resolution

When sources disagree: preserve both statements; identify each source and status; compare promotion records; compare GitHub commit and content hash; compare Supabase runtime reference; classify integrity or status mismatch as `DRIFT`; rely on the last verified promoted source; reconcile and issue a receipt.

## 9. July 9 Governance Hub Reconciliation

The July 9 DDNA Governance Hub milestone remains valid as follows: DCSE-DDNA Supabase is the constitutional runtime governance registry; GitHub is the versioned canonical artifact repository; DCS or DCSC promotion creates authority; other repositories maintain governed references and operational state.

## 10. Promotion and Synchronization Sequence

Candidate artifact -> validation -> DCS Level 0 promotion decision for exact content hashes -> GitHub canonical commit and hash -> Supabase runtime registry update -> local audit synchronization -> model distribution -> verification receipt.

No synchronization step independently promotes doctrine. The final receipt must bind the approved content hashes to the resulting GitHub commit and verified Supabase rows.

## 11. Drift Response

When `DRIFT` is detected, block reliance on the mismatched copy, retain the last verified promoted version, identify affected models and systems, correct the canonical artifact or runtime reference, update hashes and status, and record the reconciliation receipt.

## 12. Restrictions

PS content remains isolated. Sensitive access material is excluded from doctrine payloads and retrieval responses. Runtime access does not imply write authority. A database row does not promote doctrine. A GitHub merge does not promote doctrine without DCS Level 0 approval. A model summary does not replace the source.

## 13. Related Doctrine

- D03: model orchestration and access boundaries.
- D04: communications, GitHub operations, and receipts.
- D05: baselines, Level 0 promotion, drift, and rollback.
- D06: file, repository, storage, PS, and secret placement.
- D15: database administration.
- D20: Product Assembly Methodology, which retains its separate identity and lineage.

## 14. Promotion Boundary

D22 remains separate from Product Assembly D20. Promotion of D22 authorizes the source-identity and runtime-distribution rules in this file only; it does not silently amend product assembly, production deployment, database permissions, or the status of any other doctrine.

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in D03 Section 5.3: halt affected source-dependent execution, log `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`, and trigger STOPGATE when the missing source can materially affect authority, safety, secrets, PS isolation, synchronization, or promotion.
