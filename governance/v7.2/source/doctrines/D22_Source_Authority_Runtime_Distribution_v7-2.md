# DCSE Doctrine D22: Source Authority and Runtime Distribution

**Document ID:** DCSE-D22  
**Version:** v7.2  
**Last Modified:** 2026-09-10T15:22:00-04:00  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Classification:** INTERNAL  
**Lane:** DCSE / ALL  
**Canonical File:** D22_Source_Authority_Runtime_Distribution_v7-2.md  
**Parent Controller:** DCSE Master Profile v7.2  

## 1. Purpose

D22 is the controlling DCSE doctrine for source authority, persistence routing, synchronization, registry linkage, runtime distribution, and drift resolution across GitHub, Supabase, DDNA, Tribunal, local working copies, storage, Vault, model retrieval, and deployment surfaces.

## 2. Authority Hierarchy

1. Explicit DCS / DCS Level 0 decision within its authorized scope.
2. Operative DCSE Master Profile.
3. Promoted doctrine and amendments.
4. Promoted authority/registry records linked to canonical artifacts.
5. Approved baselines.
6. Governed projects and artifacts.
7. Candidates, drafts, working copies, summaries, retrieval results, and model memory.

No platform, model, database row, repository object, file, branch, commit, embedding, Tribunal receipt, or deployment creates authority merely by existing.

## 3. Canonical Source and Persistence Model

### 3.1 GitHub
GitHub is the versioned canonical artifact repository for doctrine, code, schemas, reusable architecture, controlled configuration templates, prompts/workflows that are appropriate for version control, manifests, and other Git-eligible governed artifacts.

Canonical identity for a GitHub artifact is repository + path + commit SHA + content SHA-256 where available.

### 3.2 Supabase / DCSE-DDNA
DCSE-DDNA Supabase is the constitutional runtime governance and relationship registry. It stores authority records, canonical references, promotion state, integrity metadata, relationships, distribution state, runtime status, model scope, and cross-database references.

SC Command Post Supabase stores operational/application state and may reference constitutional authority. It does not become doctrine authority by copying a record.

### 3.3 Tribunal
Tribunal stores governance-significant decision, approval, execution, validation, exception, stop-gate, reconciliation, promotion, and closeout evidence. Tribunal is an evidence and communications surface, not a substitute canonical repository for doctrine or source code.

### 3.4 Object Storage
Approved object storage stores large or binary assets when GitHub is not the appropriate canonical artifact surface. Supabase registries retain metadata, hash/provenance, ownership, classification, and canonical storage reference.

### 3.5 Vault / Secret Stores
Secret values belong only in approved secret-management surfaces such as Vault or platform-secret stores. Secret values shall not be stored in doctrine, prompts, GitHub source, ordinary Supabase content, Tribunal receipts, model memory, or public artifacts.

### 3.6 Local Files
Local files are working, staging, execution, audit, or synchronized copies unless explicitly designated otherwise. Local existence does not create authority.

## 4. Deterministic Write Decision Rule

For every incoming or newly created object:

`INGEST -> CLASSIFY -> LANE/AUTHORITY CHECK -> DUPLICATE/REUSE CHECK -> SELECT ONE CANONICAL HOME -> WRITE CANONICAL ARTIFACT/STATE -> REGISTER REFERENCES/HASH -> TRIBUNAL RECEIPT WHEN GOVERNANCE-SIGNIFICANT -> VERIFY`

Agents and models shall not independently choose among GitHub, Supabase, Tribunal, Storage, or Vault when this routing doctrine applies.

### Persistence Matrix

| Object | Canonical Home | Supabase Role | Tribunal Role |
|---|---|---|---|
| Doctrine / promoted amendment | GitHub | authority + canonical reference + hash + status | approval/promotion/reconciliation evidence |
| Source code / schema / reusable workflow | GitHub | registry + relationships + deployment/reference state | material release/change evidence |
| Structured runtime/task/app state | Supabase | canonical structured state | material decisions/errors/transitions |
| DDNA structured signals/relationships | DCSE-DDNA Supabase | canonical structured signal/registry state | material promotion/reconciliation evidence |
| DDNA source artifact suitable for Git | GitHub | source/provenance/index reference | material approval/change evidence |
| Large/binary asset | Object Storage | metadata + hash + canonical URL/reference | material lifecycle evidence |
| Secret | Vault/approved secret store | secret reference only if needed | no secret value |
| Temporary/raw upload | controlled intake/staging | intake metadata as applicable | only if governance-significant |

## 5. Upload Rule

Not every uploaded file is automatically committed to GitHub. Every upload shall first be classified. Git-eligible governed artifacts shall be versioned in GitHub and registered in Supabase. Runtime data shall remain in Supabase. Large/binary assets shall use approved object storage where appropriate. Secrets shall use Vault. Governance-significant actions receive Tribunal evidence.

## 6. DDNA Relationship

DDNA shall preserve the distinction between source artifact, structured extracted knowledge, authority, and retrieval aid:

- source artifacts remain in their proper canonical artifact surface;
- structured DDNA signals, relationships, provenance, and runtime state reside in DCSE-DDNA Supabase;
- promotion and authority require explicit DCS authority and canonical source linkage;
- Tribunal records material decisions and reconciliation evidence;
- embeddings, chunks, summaries, and retrieval results are aids, never authority.

## 7. Synchronization Sequence

`AUTHORIZED CONTENT -> GITHUB/OTHER CANONICAL ARTIFACT -> CONTENT HASH -> SUPABASE AUTHORITY/REGISTRY UPDATE -> TRIBUNAL EVIDENCE -> DISTRIBUTION -> CROSS-VERIFY`

If explicit Level 0 approval precedes the mechanical synchronization, that approval is controlling for the exact authorized content. The remaining actions are administrative synchronization, not a new approval gate.

## 8. Drift

When GitHub, Supabase, DDNA, Tribunal, local files, master/controller references, or model-distributed references disagree:

1. preserve conflicting evidence;
2. classify the mismatch as DRIFT;
3. identify last verified promoted authority;
4. correct canonical/reference state within authorization;
5. update hashes and relationships;
6. record reconciliation evidence;
7. reverify before declaring synchronized.

## 9. Cross-Doctrine Control

D04 governs communications and Tribunal transport but defers persistence destination decisions to D22. D06 governs file classification/local placement but defers canonical platform selection to D22. D15 governs database administration but shall not treat all Tribunal transactions as Git ledger entries. D16 governs DDNA extraction and knowledge lifecycle but defers canonical artifact/persistence routing to D22. D20 governs assembly/reuse and invokes D22 for artifact capture and persistence.

## 10. Promotion Record

This v7.2 D22 synchronization and persistence-routing consolidation is **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 effective 2026-09-10**. It supersedes conflicting persistence-routing language in older D04, D06, D15, D16, and D22 copies while preserving non-conflicting specialized requirements.