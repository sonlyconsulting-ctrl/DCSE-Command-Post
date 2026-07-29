# DCSE Doctrine D05: Baseline and Promotion

**Document ID:** DCSE-D05  
**Version:** v7 reconciliation candidate  
**Last Modified:** 2026-07-29  
**Status:** CANDIDATE FOR PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC  
**Canonical file:** `D05_Baseline_Promotion.md`

## 1. Purpose

D05 governs baselines, verification, candidate handling, automatic promotion, manual promotion, rollback, and promotion receipts.

## 2. Baseline Standard

A baseline is a verified state of a governed package, repository, project, doctrine set, database schema, or deployment at a specific point in time.

Every baseline must identify:

- package or system name;
- version;
- lane;
- authority;
- source files or objects;
- repository and commit when applicable;
- SHA-256 or equivalent integrity hashes;
- exclusions;
- validation performed;
- unresolved risks;
- rollback or recovery path;
- exit criteria status.

## 3. Promotion States

```text
DRAFT
CANDIDATE
VALIDATING
BLOCKED
PROMOTED
SUPERSEDED
ARCHIVED
DRIFT
```

Candidate status is a lifecycle state, not an automatic approval requirement.

## 4. Automatic Promotion Rule

A candidate promotes automatically when all mandatory checks pass and no true Stop-Gate exists, provided the governing workflow expressly permits automatic promotion.

Mandatory checks include:

1. correct lane and authority;
2. complete source manifest;
3. required files present;
4. naming and version controls satisfied;
5. placeholders removed;
6. secret scan passed;
7. PS leakage scan passed;
8. syntax or schema validation passed when applicable;
9. dependencies resolved;
10. rollback or recovery path documented;
11. expected outputs produced;
12. exit criteria verified.

Routine candidate status, formatting review, or the mere existence of an approval field does not create a manual gate.

## 5. Manual Promotion Rule

DCS or DCSC manual approval is required when:

- doctrine or constitutional authority changes;
- PS material is involved;
- public publication creates legal or reputational risk;
- credentials, access, migration, deletion, or destructive actions are involved;
- a source conflict remains unresolved;
- the governing workflow expressly reserves promotion to Level 0;
- a failed mandatory check requires an exception;
- the action changes production ownership, security posture, or financial commitment.

## 6. Promotion Receipt

Every promotion receipt must include:

```text
item_id
version
lane
promotion_type = automatic | manual
promoted_by
promotion_timestamp
canonical_source
repository_commit
content_hash
mandatory_checks
stop_gate_scan
supersedes
rollback_path
final_status
```

## 7. Modification After Promotion

A material content change creates a new candidate version. The prior promoted version remains authoritative until the new version passes its promotion path. A minor non-substantive correction may preserve promotion only when the governing workflow defines that exception and records the new hash.

## 8. Drift Control

A mismatch among the promoted GitHub artifact, Supabase runtime record, local audit copy, or published deployment creates `DRIFT`.

During DRIFT:

- the last verified promoted version remains controlling;
- the mismatched copy is not relied upon;
- the source record and hashes are compared;
- reconciliation is logged;
- promotion resumes only after validation.

## 9. Rollback

Rollback must identify the prior promoted version, commit or baseline identifier, affected systems, restoration steps, data recovery requirements, and validation checks. A rollback is incomplete until the restored state is verified.

## 10. Related Doctrine

- D02: forward and backward validation
- D03: model authority and execution routing
- D04: communication and receipts
- D06: file and storage placement
- D20: source authority and runtime distribution
