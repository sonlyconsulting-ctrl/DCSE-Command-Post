# DCSE Doctrine D20: Source Authority and Runtime Distribution

**Document ID:** DCSE-D20  
**Version:** v1.0 reconciliation candidate  
**Created:** 2026-07-29  
**Status:** CANDIDATE FOR PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC  
**Canonical file:** `D20_Source_Authority_Runtime_Distribution.md`

## 1. Purpose

D20 resolves source-of-truth conflicts among DCS decisions, promoted Markdown, GitHub, DCSE-DDNA Supabase, SC Command Post Supabase, local files, model uploads, retrieval indexes, and deployments.

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

GitHub stores the versioned canonical artifact for doctrine and governed source files. The canonical identity is:

```text
repository + path + commit SHA + content SHA-256
```

A GitHub commit is evidence and distribution infrastructure. It becomes controlling only when linked to the applicable promotion state.

### 3.3 Constitutional Runtime Registry

DCSE-DDNA Supabase is the constitutional runtime governance registry. It stores governance directives, canonical references, promotion state, integrity hashes, model read scopes, acknowledgements, queues, execution records, and cross-database references.

Supabase does not replace the canonical artifact. It points to and verifies it.

## 4. Operational Supabase Separation

The SC Command Post Supabase project stores application and operational state. It may retain governed references to DCSE-DDNA authority, but it does not become the constitutional doctrine source by copying a record.

## 5. Required Runtime Doctrine Record

Every doctrine record distributed through Supabase must include:

```text
doctrine_id
canonical_filename
version
lane
classification
promotion_status
promotion_type
promoted_by
promotion_timestamp
github_repository
github_path
github_commit_sha
content_sha256
supersedes
superseded_by
model_read_scope
ps_restriction
secret_scan_status
runtime_status
```

`runtime_status` values:

```text
ACTIVE
CANDIDATE
SUPERSEDED
ARCHIVED
DRIFT
BLOCKED
```

## 6. Model Access

Models access doctrine through one or more approved methods:

- GitHub repository checkout;
- GitHub connector or raw promoted source;
- operator-uploaded promoted source package;
- scoped Supabase retrieval endpoint;
- approved local source package.

Model access must be explicit, lane-scoped, logged when applicable, and revocable. No model receives unrestricted database access or implied permissions.

## 7. Retrieval and Embeddings

Search results, embeddings, chunks, summaries, and retrieved passages are access aids. They are not authority. Before use, the executing model must verify doctrine ID, version, lane, classification, promotion state, source commit, and hash.

## 8. Conflict Resolution

When sources disagree:

1. preserve both statements;
2. identify each source and status;
3. compare promotion records;
4. compare GitHub commit and content hash;
5. compare Supabase runtime reference;
6. classify the mismatch as `DRIFT` when integrity or status differs;
7. rely on the last verified promoted source;
8. reconcile and issue a receipt.

## 9. July 9 Governance Hub Reconciliation

The July 9 DDNA Governance Hub milestone remains valid as follows:

- DCSE-DDNA Supabase is the constitutional runtime governance repository.
- GitHub is the versioned canonical artifact repository.
- DCS or DCSC promotion creates authority.
- Other repositories maintain governed references and operational state.

Any reading that makes Supabase alone, GitHub alone, or a model alone self-authoritative is superseded by this three-part model.

## 10. Promotion and Synchronization Sequence

```text
Draft artifact
-> validation
-> promotion decision or authorized automatic promotion
-> GitHub canonical commit and hash
-> Supabase runtime registry update
-> local audit synchronization
-> model distribution
-> verification receipt
```

The sequence may be transacted atomically by approved automation, but all required identities and receipts must exist at closeout.

## 11. Drift Response

When DRIFT is detected:

- block reliance on the mismatched copy;
- retain the last verified promoted version;
- identify affected models and systems;
- correct the canonical artifact or runtime reference as required;
- update hashes and status;
- record the reconciliation receipt.

## 12. Restrictions

- PS content remains isolated.
- Sensitive access material is excluded from doctrine payloads and retrieval responses.
- Runtime access does not imply write authority.
- A database row does not promote doctrine.
- A GitHub merge does not promote doctrine without the governing promotion rule.
- A model summary does not replace the source.

## 13. Related Doctrine

- D03: model orchestration and access
- D04: communications, GitHub, and receipts
- D05: baselines, promotion, and drift
- D06: file, repository, and storage placement
- D15: database administration
