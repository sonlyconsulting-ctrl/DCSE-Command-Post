# GOTIME LEAKAGE SCANNER TEST REPORT

**Ref:** GoTime Phase 5 Leakage Scanner  
**Date:** 2026-07-02  
**Status:** VALIDATED (All Test Cases Passed)

---

## 1. Scanner Rules Configuration
The leakage scanner checks all text inputs (chat messages, pasted notes, Tribunal drops) using a set of compiled regular expressions targeting known PS litigation assets:

1.  **Case Number:** `(?i)\b8:?23-?cv-?0*489\b` (Matches variations of Case No. 8:23-cv-00489, including multi-zero sequences like 00489 or 0489).
2.  **Case Title:** `(?i)\bseals\s+v(s)?\.\s+dhhs\b` (Matches "seals v. dhhs" and variations).
3.  **Pro Se Indicator:** `(?i)\bpro\s+se\b` (Flags pro se litigation markers).
4.  **Defendant Code:** `(?i)\bdart\b` (Flags DART-related litigation indicators).
5.  **Coordinating Boundary:** `(?i)\btribunal\b` (Monitors coordinating activity markers).

---

## 2. Test Execution Log

We ran the scanner test suite against five test inputs:

| ID | Input Text | Leak Detected | Action Taken |
|----|------------|---------------|--------------|
| 1  | "This is a standard task to renew the Wix plan before July 17." | **FALSE** | None (Clean) |
| 2  | "DCS needs to review the draft filing for case 8:23-cv-00489 in Nebraska." | **TRUE** | Redacted Case Number |
| 3  | "We need to consolidate the seals v. dhhs case briefs." | **TRUE** | Redacted Case Title |
| 4  | "Send the employment resume details to the recruiter via email." | **FALSE** | None (Clean) |
| 5  | "The pro se litigant filed a new motion to seal the records." | **TRUE** | Redacted Pro Se Marker |

---

## 3. Redaction Verification Output
When a leak is detected, the body text is sanitized using a default placeholder `[REDACTED PS FIREWALL LOCK]`:

*   *Before:* "We need to consolidate the seals v. dhhs case briefs."
*   *After:* "We need to consolidate the `[REDACTED PS FIREWALL LOCK]` case briefs."

*   *Before:* "DCS needs to review the draft filing for case 8:23-cv-00489 in Nebraska."
*   *After:* "DCS needs to review the draft filing for case `[REDACTED PS FIREWALL LOCK]` in Nebraska."

---

## 4. Key Hardening Takeaway
During the initial test, the case number pattern `0?489` was found to miss the double-zero format `00489`. This was patched to use `0*` (any number of leading zeros), ensuring that standard court representations are fully intercepted.
