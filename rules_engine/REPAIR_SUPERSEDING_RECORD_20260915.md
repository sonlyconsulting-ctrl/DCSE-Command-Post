# DCSE Rules Engineering v0.2.1 Candidate Superseding Record — 2026-09-15

**Lifecycle status:** CANDIDATE (PENDING PROMOTION)  
**Authority:** Candidate repair under Issue #119 (formal DCS Level 0 promotion pending)  
**Historical Lineage:** Preserves historical v0.2.0 OPERATIVE rules baseline and structure  
**Canonical repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Canonical path:** `rules_engine/`  
**Superseded version:** `0.2.0` (`rules_engine/DCSE_Rules_Engineering_Operative_v0_2.tar.gz`)  
**Superseded archive defect:** Git blob `148cc77c3016d6b4e63b325377e542b41f2685bd` (7,509 bytes) suffered an EOF truncation during original push, preventing clean independent bootstrap.  
**Repaired archive filename:** `DCSE_Rules_Engineering_Operative_v0_2_1.tar.gz`  
**Repaired archive SHA-256:** `7ee1e8e215be2bd4895535daab66efb8a064aa4f30006ee5ed4897a0f0a2747f`  

## Lineage and Equivalence Verification
- Extracted and verified from canonical blueprint `DCSE_Rules_Engineering_Blueprint_v0_2.zip` (52,555 bytes).
- 100% content-equivalent to the promoted source tree:
  * 5 Entity sets: `TASK` (10 rules), `IDE` (10 rules), `AST` (10 rules), `DDN` (10 rules), `KNW` (10 rules). Total 50 atomic rules, 5 composites.
  * 18 Capability sets: `ESCD`, `VOICE`, `SUPABASE`, `CONTENT`, `GITHUB`, `DEPLOYMENT`, `EMAIL`, `FILE-HANDLING`, `ASSET-GENERATION`, `EMPLOYMENT`, `SC`, `SS`, `TI`, `GOVERNANCE`, `TRIBUNAL`, `SECURITY`, `COMMUNICATIONS`, `MEDIA` (5 rules each = 90 rules).
  * 1 Meta set: `RULE_LIFECYCLE` (8 rules: `META-001`..`META-008`).
  * Total: 148 atomic rules, 5 composites.
- All individual file SHA-256 hashes match `FILE_HASHES.sha256`.
- Package status remains CANDIDATE pending formal DCS Level 0 promotion.

## Clean Checkout Test Evidence
- Command: `python rules_engine/bootstrap.py --test`
- Result: `Ran 12 tests in 0.041s — OK (12/12 PASS)`
- Bootstrap materialization succeeds independently without relying on external paths or Downloads folder.
