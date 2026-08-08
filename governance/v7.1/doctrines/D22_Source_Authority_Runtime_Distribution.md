---
dcse_zone: authority
dcse_authority_level: PROMOTED
dcse_document_id: DCSE-D22
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_promoted_by: DCS_LEVEL_0
dcse_promotion_date: 2026-08-04
dcse_classification: CONFIDENTIAL
dcse_lane: DCSE
dcse_required_approval: DCS_LEVEL_0_EXACT_DIFF
dcse_source_lineage: governance/v7.1/source/doctrines/D22_Source_Authority_Runtime_Distribution.md
---

# DCSE Doctrine D22: Source Authority and Runtime Distribution

## 1. Position Under the Master Profile

D22 is subordinate to `DCSE_Master_Profile_v7.1.md`.

The Master Profile is the constitutional entry point. D22 answers the downstream question: which source controls, how is that authority represented, and how are canonical artifacts and runtime registries reconciled?

D22 may distribute, validate, and reconcile authority. D22 may not replace the Master Profile, amend the authority hierarchy, or promote itself.

## 2. Three-Part Source Model

### 2.1 Authority

Authority is a recorded DCS Level 0 decision operating through the promoted Master Profile and promoted subordinate doctrine within the scope of that decision.

### 2.2 Canonical Artifact

GitHub stores the versioned canonical artifact. Canonical identity requires:

- repository;
- branch or tag;
- path;
- commit SHA;
- content SHA-256;
- promotion receipt reference.

A GitHub file or commit is evidence and distribution infrastructure. It does not create authority by existence.

### 2.3 Constitutional Runtime Registry

DCSE-DDNA Supabase stores runtime governance records that point to and verify the canonical artifact. A runtime record must not substitute for the source file or promotion record.

The SC Command Post Supabase project stores operational state. It may reference DCSE-DDNA authority but does not become the constitutional governance source.

## 3. Source Precedence

When sources disagree, apply this order:

1. DCS Level 0 decision within its exact recorded scope.
2. Promoted `DCSE_Master_Profile_v7.1.md`.
3. Promoted V7.1 doctrine expressly routed by the Master Profile.
4. Promoted registry and authority record that matches the canonical artifact and promotion receipt.
5. Approved baseline.
6. Governed project artifact.
7. Instruction, execution contract, ledger, report, or evidence record.
8. Candidate, source copy, draft, historical record, model memory, or retrieval result.

A lower source cannot waive or amend a higher source.

## 4. Required Runtime Doctrine Record

Every promoted doctrine record must include:

- doctrine ID;
- document title;
- version;
- parent Master Profile;
- lane;
- classification;
- zone;
- authority level;
- promotion status;
- promoted by;
- promotion timestamp;
- GitHub repository;
- GitHub path;
- GitHub commit SHA;
- content SHA-256;
- source lineage;
- supersedes;
- superseded by;
- model read scope;
- PS restriction;
- secret scan status;
- runtime status;
- last reconciliation timestamp.

Allowed runtime statuses are `ACTIVE`, `CANDIDATE`, `SUPERSEDED`, `ARCHIVED`, `DRIFT`, and `BLOCKED`.

## 5. Access and Retrieval

Models may access doctrine only through approved GitHub, scoped Supabase retrieval, operator upload, or approved local source methods.

Before relying on retrieved content, verify:

1. document ID;
2. parent Master Profile;
3. version;
4. lane;
5. classification;
6. zone;
7. authority level;
8. promotion state;
9. GitHub commit;
10. content hash.

Search results, embeddings, chunks, summaries, and memories are retrieval aids. They are not authority.

## 6. Conflict and Drift Protocol

When sources conflict:

1. preserve each statement;
2. identify each source and zone;
3. identify each authority level and promotion state;
4. compare GitHub commit and content hash;
5. compare runtime registry values;
6. classify the mismatch as authority conflict, content drift, status drift, path drift, or registry drift;
7. rely on the last verified promoted source;
8. block the mismatched copy from active routing;
9. issue a reconciliation record;
10. route unresolved constitutional conflicts to DCS Level 0.

Required conflict format:

- Verified Source A
- Verified Source B
- Contradiction
- Controlling authority
- Risk
- Required correction
- DCS decision required

## 7. Promotion and Synchronization Sequence

The valid sequence is:

1. candidate artifact;
2. source and contradiction review;
3. validation;
4. DCS Level 0 approval for the exact content or exact diff;
5. canonical GitHub commit;
6. content SHA-256 verification;
7. DCSE-DDNA registry update;
8. local audit synchronization;
9. model distribution;
10. reconciliation receipt.

No synchronization step independently promotes doctrine.

## 8. Zone Integrity

D22 must reject authority claims from execution and evidence zones.

An execution contract may direct bounded work. A ledger may record activity. A Tribunal record may preserve evidence. None may declare itself promoted, constitutional, or authoritative.

If an execution or evidence file contains a policy rule needed for future tasks, that rule must be extracted into a candidate authority document and promoted through the required sequence.

## 9. Restrictions

- PS content remains isolated.
- Secrets remain excluded from doctrine payloads and retrieval responses.
- Runtime read access does not imply write authority.
- Database access does not imply promotion authority.
- A GitHub merge does not imply DCS approval.
- A manifest does not supersede the Master Profile.
- A model summary does not replace the source.
- D22 does not amend the Master Profile.

## 10. Source Lineage

This V7.1-normalized doctrine derives from:

`governance/v7.1/source/doctrines/D22_Source_Authority_Runtime_Distribution.md`

The source copy remains preserved as lineage and has no independent active authority after this normalized doctrine is promoted.

## 11. Exit Criteria for Promotion

D22 is eligible for promotion only when:

1. the Master Profile exact diff is approved;
2. this exact D22 diff is approved;
3. the canonical path and commit are recorded;
4. content SHA-256 is recorded;
5. the runtime registry row is updated;
6. D21 points to this normalized path;
7. validation confirms that no source, execution, evidence, or manifest file competes with the Master Profile.