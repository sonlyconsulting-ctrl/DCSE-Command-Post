# GOTIME LEAKAGE SCANNER V2 TEST REPORT

**Ref:** GoTime Phase 5 Leakage Scanner v2  
**Date:** 2026-07-02  
**Status:** VALIDATED (10/10 Test Cases Passed)

---

## 1. Expanded Term Matching Rules
The leakage scanner (v2) features expanded coverage to intercept legal terms, court milestones, case titles, defendant names, and comparators:

*   **Case Identifiers:** `8:23-cv-00489`, `8:23cv489`, `823cv489`, `Seals v. DHHS`, `DHHS`, `Nebraska`
*   **Court Terminology:** `docket`, `motion`, `summary judgment`, `bench trial`, `exhibit`, `witness`, `deposition`, `Rule 52`, `Title VII`, `§1981`, `1981`, `§1983`, `1983`
*   **Entities & People:** `Ballentine`, `Darden`, specific protected witness and comparator names.
*   **System/Folder Patterns:** Known PS directory structures (`PS_WIN_WIN_WIN`, `DCSE_PS_CP_Project`), litigation search terms, and seal patterns.

---

## 2. Ingestion & Redaction Test Log (10 Test Cases)
We ran the v2 scanner against 10 distinct test scenarios:

| ID | Test Case Category | Sample Input | Match? | Action / Redaction Outcome |
|----|--------------------|--------------|--------|----------------------------|
| 1  | Case Number Match  | "Filing updates for case 823cv489." | **YES** | Hold in Quarantine. Redact text for display. |
| 2  | Case Title Match   | "Consolidated records for Seals v. DHHS case." | **YES** | Hold in Quarantine. Redact text for display. |
| 3  | Comparator Match   | "Verify comparator list including Ballentine." | **YES** | Hold in Quarantine. Redact text for display. |
| 4  | Court Term Match   | "Prepare exhibit list for the bench trial." | **YES** | Hold in Quarantine. Redact text for display. |
| 5  | Legal Claim Match  | "Draft response regarding Section 1983 claims." | **YES** | Hold in Quarantine. Redact text for display. |
| 6  | PS Lane Match      | "Task routed with lane = 'PS'." | **YES** | Hold in Quarantine. Redact text for display. |
| 7  | Empty-Intake Test  | "" | **NO** | Reject (Invalid/Empty payload). |
| 8  | Bare Number Test   | "We need to fix issue 489 in the repository." | **NO** | Passed. (Bare number does not trigger regex). |
| 9  | Employment Safe    | "Update the LinkedIn dossier template." | **NO** | Passed (No litigation terms found). |
| 10 | Public Product Safe| "Deploy Vite frontend to Vercel portal." | **NO** | Passed (No litigation terms found). |

---

## 3. Strict Non-Auto-Clearance Rule
The v2 scanner **does not auto-redact and promote**. If any pattern matches:
1.  The record is flagged as `ps_leakage_status = 'FLAGGED'`.
2.  It is held in the `gotime_intake_quarantine` table.
3.  Auto-redaction is only applied to **dashboard preview cards** shown to standard users. The original raw text remains safely locked in the quarantine database schema and is only accessible to DCS administrators via service-role mediation.
4.  Promotion to an active work order requires manual DCS review and sign-off.
