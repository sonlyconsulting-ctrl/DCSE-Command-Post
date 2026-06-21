# DCSE Doctrine D05: Baseline & Promotion

**Document ID:** DCSE-D05  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T15:22:37-04:00  
**Last Version/Release Date/Time:** 2026-06-21T15:22:37-04:00  
**Status:** CANDIDATE  
**Classification:** INTERNAL  
**Lane:** DCSE  
**Canonical file:** D05_Baseline_Promotion.md  
**Doctrine Description:** The Baseline and Promotion Doctrine (D05) establishes the lifecycle management and quality gates for committing system assets. It replaces traditional releases with signed "Baselines" containing cryptographic checksum mappings of the entire workspace. D05 defines the promotion gateway, which requires human Level 0 authorization to shift any candidate file into an active ratified status, preventing accidental or unverified promotion of volatile content.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. Baseline System (Replaces "Releases")

The concept of a "Release" is replaced by a "Baseline".
- A Baseline represents a verified state of the entire repository at a specific timestamp.
- Baselines are committed to `06_Baselines/`.
- Every baseline contains a `baseline_receipt.json` mapping all file paths to their current SHA-256 hash values.

---

## 2. Promotion Protocol

Promotion shifts a document's status from `CANDIDATE` to `ACTIVE_RATIFIED`.
- Only DCS Level 0 may ratify a promotion.
- Verification receipts are generated upon promotion, logging:
  - Document ID and hash.
  - Date and time of ratification.
  - Sign-off block of the final approver.
- If a document is modified after promotion, its status reverts to `CANDIDATE` until a new ratification event occurs.

---

## Related Doctrine

- [D02_Forward_Backward_Chaining.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D02_Forward_Backward_Chaining.md) - Backward chaining validates documents before promotion
- [D06_File_System.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D06_File_System.md) - Baselines committed to 06_Baselines directory

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
