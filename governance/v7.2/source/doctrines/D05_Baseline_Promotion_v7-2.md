> **v7.2 alignment note (2026-09-11):** This file is the v7.2 authority-path projection of the baseline and promotion rules already compiled into the operative R5 controller. It does not fabricate a separate historical ratification event. Exact new promotions still require the evidence gates stated below.

# DCSE Doctrine D05: Baseline & Promotion

**Document ID:** DCSE-D05  
**Version:** v7.2  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-07-29T18:07:30-04:00
**Last Version/Release Date/Time:** 2026-07-29T18:07:30-04:00  
**Status:** ACTIVE / OPERATIVE VIA DCSE MASTER PROFILE v7.2 R5  
**Classification:** INTERNAL  
**Lane:** DCSE  
**Canonical file:** D05_Baseline_Promotion.md  
**Doctrine Description:** The Baseline and Promotion Doctrine (D05) establishes the lifecycle management and quality gates for committing system assets. It replaces traditional releases with signed "Baselines" containing cryptographic checksum mappings of the entire workspace. D05 defines the promotion gateway, which requires human Level 0 authorization to shift any candidate file into an active ratified status, preventing accidental or unverified promotion of volatile content.  
**Parent Controller:** `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`  

---

## 1. Baseline System (Replaces "Releases")

The concept of a "Release" is replaced by a "Baseline".
- A Baseline represents a verified state of the entire repository at a specific timestamp.
- Baselines are committed to `06_Baselines/`.
- Every baseline contains a `baseline_receipt.json` mapping all file paths to their current SHA-256 hash values.
- Every baseline also identifies package or system name, version, lane, authority, repository and commit when applicable, exclusions, validation performed, unresolved risks, rollback or recovery path, and exit-criteria status.

---

## 2. Promotion Protocol

Promotion shifts a validated document from `CANDIDATE` to `ACTIVE_RATIFIED` through a recorded manual Level 0 decision.
- Only DCS Level 0 may ratify a promotion.
- No doctrine candidate promotes automatically. Passing checks makes a candidate eligible for Level 0 review; it does not create authority.
- Verification receipts are generated upon promotion, logging:
  - Document ID and hash.
  - Date and time of ratification.
  - Sign-off block of the final approver.
- If a document is modified after promotion, its status reverts to `CANDIDATE` until a new ratification event occurs.

### 2.1 Controlled Lifecycle States

```text
DRAFT -> CANDIDATE -> VALIDATING -> ACTIVE_RATIFIED
                    -> BLOCKED
ACTIVE_RATIFIED -> SUPERSEDED -> ARCHIVED
Any governed copy -> DRIFT when source identity or integrity no longer matches
```

`ACTIVE_RATIFIED` means the exact content hash was promoted. A status label without a matching Level 0 receipt is not sufficient proof.

### 2.2 Promotion Receipt Requirements

Every receipt must record document ID, version, lane, manual promotion type, promoted by, timestamp, canonical repository and path, repository commit when known, content SHA-256, mandatory-check results, STOPGATE scan, superseded version, rollback path, and final status.

### 2.3 Modification After Promotion

A material content change creates a new candidate. The prior promoted version remains controlling until the changed version receives a new Level 0 decision. A non-substantive correction may preserve promotion only when an expressly governed exception records the corrected hash; there is no implied clerical exception.

### 2.4 Drift Control

A mismatch among the promoted GitHub artifact, Supabase runtime record, local audit copy, or published deployment is `DRIFT`. During DRIFT, the last verified promoted version remains controlling, the mismatched copy is not relied upon, source records and hashes are compared, and reconciliation is logged before distribution resumes.

### 2.5 Rollback and Recovery

Rollback must identify the prior promoted version, commit or baseline identifier, affected systems, restoration steps, data recovery requirements, and validation checks. A rollback is incomplete until the restored state is verified.

---

## Related Doctrine

- D02 Forward and Backward Chaining - Backward chaining validates documents before promotion
- D06 File System - Baselines committed to 06_Baselines directory
- D22 Source Authority and Runtime Distribution - Promotion linkage to canonical GitHub artifacts and runtime records

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
