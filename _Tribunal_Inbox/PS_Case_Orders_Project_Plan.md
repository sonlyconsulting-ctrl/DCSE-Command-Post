# PS Case Orders & Schedule Project Plan

**Case:** Seals v. State of Nebraska-Department of Health and Human Services (8:23-cv-00489-RFR-JMD)
**Judge / Magistrate:** Hon. Robert F. Rossiter, Jr. / Hon. Jacqueline M. DeLuca
**Phase:** Trial Ready - Summary Judgment Pending
**Counsel Status:** Pro Se (pending retention on summary judgment denial)
**Current Date/Timestamp:** 2026-07-01

> [!WARNING]
> This plan was extracted under temporary lightening of PS guardrails strictly for project planning purposes. Strict PS (Case 8:23CV489) firewall doctrine resumes immediately after the generation of this document.

---

## 1. Track Schedule & Priorities

| Track | Name | Deadline | Status | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Track A** | Motion in Limine | 2026-08-17 | `AUTHORIZED_PENDING_OI-1_OI-2` | **HIGH** |
| **Track B1** | Justin J. Hall Litigation Profile | *N/A* | `AUTHORIZED` | MEDIUM |
| **Track B2** | DART Rule Group 11 Build | *N/A* | `AUTHORIZED` | MEDIUM |
| **Track C** | Damages Reconciliation Worksheet | 2026-08-19 | `AUTHORIZED_PENDING_OI-3` | **HIGH** |

---

## 2. Blockers & Open Items (OI)

> [!CAUTION]
> The following Open Items are currently blocking High Priority tracks.

*   **OI-1 (Blocking Track A):** Need decision on Track A format — Court-ready or annotated draft?
*   **OI-2 (Blocking Track A):** Need Track A Bates references for post-hoc performance documents.
*   **OI-3 (Blocking Track C):** Pending resolution for the Damages Reconciliation Worksheet parameters.

---

## 3. Attorney & Team Action Items

*   **[ ] QA Verification:** Verify page counts are populated (indexing complete) via `list_documents`.
*   **[ ] LKG Extraction:** Begin `search_corpus` and `get_document_text` for Legal Knowledge Graph extraction.
*   **[ ] Privilege Boundary Update:** Update `CLAUDE.md` context when trial counsel is officially retained, as this activates Attorney-Client privilege boundaries (currently only Work Product).

---

## 4. Systems & Infrastructure Status

*   **Document Ingestion:** 12 exhibits successfully ingested, chunked, and indexed via FAISS (210 vectors).
*   **Legal Knowledge Graph:** Extracted 63 Facts, 34 Legal Norms, 28 Legal Applications, and 27 Statutory Provisions.
*   **Docket Monitoring:** CourtListener MCP active. CM/ECF email routing to `sonlyconsulting@gmail.com` confirmed.
*   **Infrastructure:** Docker OpenContracts server running successfully.

---

## 5. Outstanding Executive / DCS Decisions Required

> [!IMPORTANT]
> The following items require executive review based on recent Tribunal activity logs.

1.  **PS Firewall Verification:** DCS must confirm that the remediation of the PS Firewall breach in `SC_CTJ` is sufficient, or authorize a full PS-contamination sweep across all SC product folders before CTJ/SS public launch.
2.  **Domain Model Conflict:** DCS must resolve the domain-model conflict regarding PS content pasted into the Employment thread (Four-pillar DCSE model vs. Eight-CISSP-domain model).
3.  **Employment Classification:** DCS must confirm `PS_WIN_WIN_WIN` classification before any future session treats it as employment-related material.
