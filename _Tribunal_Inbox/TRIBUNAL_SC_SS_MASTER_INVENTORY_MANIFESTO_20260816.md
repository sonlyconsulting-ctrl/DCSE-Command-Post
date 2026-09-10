# TRIBUNAL COORDINATION RECORD: MASTER SOURCE INVENTORY & REBUILD MANIFESTO

**Record ID:** TRIBUNAL_SC_SS_MASTER_INVENTORY_MANIFESTO_20260816  
**Status:** FILED & DEPOSITED IN _TRIBUNAL_INBOX  
**Date:** August 16, 2026  
**Related Lanes:** SC, SS, TSL, CTJ  
**Classification:** NON-PS / PUBLIC REBUILD BLUEPRINT  

---

## 1. Overview and Intent

This document serves as the **combined, authoritative source index and routing manifesto** to guide the executioner of the `sc.com` and `Smoove Spots (SS)` website rebuild. It lists all source files (HTML templates, Python script engines, assets, and CSV data tables) mapped into clear delivery channels.

> [!IMPORTANT]
> **Directive Compliance:** In strict adherence to DCS instructions, no source files were moved, copied, altered, or normalized. This manifesto serves as an informational blueprint.

---

## 2. Critical Statement: Embedded HTML Web Integrations

**Notice to the Rebuild Executioner:**  
There are active, embedded HTML web addresses within `sc.com` that function as iframe-hosted interactive widgets. 
*   **The Shoegirl Platinum Birthday Experience:** Currently hosted at [https://shoegirl-platinum-edition.sonlysc.chatgpt.site](https://shoegirl-platinum-edition.sonlysc.chatgpt.site) and embedded directly on the Wix-hosted page at [https://www.sonlyconsulting.com/shoe-girl](https://www.sonlyconsulting.com/shoe-girl).
*   **Wix Frame Viewport Constraints:** The Wix HTML iframe host is fixed at a height of 615 pixels. The embedded application must remain optimized for this host viewport to prevent nested scrollbars, clipping, or viewport scaling failures on mobile layouts.
*   **Integration Rule:** Future page templates must accommodate these embedded components, maintaining their host URLs and redirect targets.

---

## 3. Mandate for Claude-Related Agents

To ensure consistency and operational integrity across agent sessions, any future **Claude-related agents** tasked with developing, auditing, or deploying elements of the SC/SS platforms must adhere to the following directive:

### Claude Agent Instructions:
1.  **Strict Non-Destructive Boundary:** Under no circumstances are you to move, copy, alter, rename, stage, or delete any source files in the downloads directory or the repository lanes unless DCS has explicitly approved the exact scope.
2.  **Audit & Verification Flow:** Run systematic audits of the repository and Downloads folders. You must reference file size, absolute links, and relative positions, outputting detailed manifests in markdown.
3.  **Active Exclusions (Security and Legal):**
    *   **Security Logs:** Any CSV files containing credential exposures, API key sweeps, or secret scans must be excluded from public staging and repository commits.
    *   **PS Firewall:** Any file containing case logs, Bates indexes, pro se materials, or references to litigation (e.g. `Bates_Index_Provisional.csv`, `Deficiency_Log___For_Service.csv`, `PS_900-953_FINAL_litigation_review.csv`) must be completely isolated. Never index or quote legal content.
4.  **Split-Lane Classifications:** Route assets strictly according to the Lane Classifications listed in Section 6 below.

---

## 4. Key CSV Inventory Schemas

The following CSV files form the database registry of files and statuses in the platform. The schemas show how to read and parse these assets:

*   **SS Master Inventory:**
    *   *Path:* [SS_MASTER_INVENTORY.csv](file:///laptop-74uf76gb/DS All Things/DCSE_Command_Center/DCSE_CP_Project/product_lanes/SS_Smoove_Spots/01_INVENTORY/Product_Intelligence_Inventory/SS_MASTER_INVENTORY.csv) (Size: 369.19 KB)
    *   *Schema:* `"FileName","FullPath","FileType","Size","DateCreated","DateModified","RelatedProduct","CandidateProductFamily","VersionIndicator","LikelyAuthorityLevel","DuplicateIndicator","ArchiveCandidate","Notes","SHA256","Root"`
*   **SS Reconciled Copy Plan:**
    *   *Path:* [SS_RECONCILED_COPY_PLAN.csv](file:///laptop-74uf76gb/DS All Things/DCSE_Command_Center/DCSE_CP_Project/product_lanes/SS_Smoove_Spots/01_INVENTORY/SS_RECONCILED_COPY_PLAN.csv) (Size: 621.24 KB)
    *   *Schema:* `"plan_id","action","source_file_name","source_path","source_sha256","file_type","size_bytes","date_modified","candidate_product_family","related_product","likely_authority_level","duplicate_indicator","archive_candidate","destination_folder","destination_relative_folder","proposed_destination_name","authority_confidence","copy_status","rationale"`
*   **Four Lane Pre-Dive Status Index:**
    *   *Path:* [FOUR_LANE_PRE_DIVE_STATUS_INDEX.csv](file:///laptop-74uf76gb/DS All Things/DCSE_Command_Center/DCSE_CP_Project/FOUR_LANE_PRE_DIVE_STATUS_INDEX.csv) (Size: 1.99 KB)
    *   *Schema:* `"lane","identity","status","root","current_stage","copied","next_action","hold"`
*   **Four Lane Pre-Dive Artifact Check:**
    *   *Path:* [FOUR_LANE_PRE_DIVE_ARTIFACT_CHECK.csv](file:///laptop-74uf76gb/DS All Things/DCSE_Command_Center/DCSE_CP_Project/FOUR_LANE_PRE_DIVE_ARTIFACT_CHECK.csv) (Size: 1.04 KB)
    *   *Schema:* `"relative_path","exists","length","last_modified"`
*   **DCSE Asset Module Source Search:**
    *   *Path:* [dcse_asset_module_source_search.csv](file:///laptop-74uf76gb/DS All Things/DCSE_Command_Center/DCSE_CP_Project/dcse_asset_module_source_search.csv) (Size: 3055.29 KB)
    *   *Schema:* `"Path","LineNumber","Line"`

---

## 5. Downloads Folder HTML Inventory & Classification

A scan of the local Downloads folder identified **76 HTML files**. These have been classified into target domains:

### Category A: Sonly Consulting (SC) Platform & Support (16 Files)
These files represent the marketing pages, internal admin dashboard panels, intake portals, and professional resumes:

| File Name | Page Title | Size (KB) | File Link |
| --- | --- | --- | --- |
| DCS-Resume-v4.0 (1).html | Donald C. Seals, Jr. \| Enterprise Technical Architect | 38.41 | [DCS-Resume-v4.0 (1).html](file:///c:/Users/Donald Seals/Downloads/DCS-Resume-v4.0 (1).html) |
| DCS-Resume-v4.0.html | Donald C. Seals, Jr. \| Enterprise Technical Architect | 38.41 | [DCS-Resume-v4.0.html](file:///c:/Users/Donald Seals/Downloads/DCS-Resume-v4.0.html) |
| DCSE Admin Control Portal.html | DCSE Command Cortex — Admin Control Panel v1 (Live Preview) | 62.77 | [DCSE Admin Control Portal.html](file:///c:/Users/Donald Seals/Downloads/DCSE Admin Control Portal.html) |
| DCSE Blog Post App.html | DCSE Blog Command Post v1.0 | 11.59 | [DCSE Blog Post App.html](file:///c:/Users/Donald Seals/Downloads/DCSE Blog Post App.html) |
| DCSE Blog post V2.html | DCSE Blog Command Post v1.1 | 15.49 | [DCSE Blog post V2.html](file:///c:/Users/Donald Seals/Downloads/DCSE Blog post V2.html) |
| DCSE_SessionIntelligence_Interactive_20260624.html | DCSE Command Post \| Session Intelligence \| June 24, 2026 | 47.12 | [DCSE_SessionIntelligence_Interactive_20260624.html](file:///c:/Users/Donald Seals/Downloads/DCSE_SessionIntelligence_Interactive_20260624.html) |
| dcse_tax_worksheet_live_preview.html | DCSE Tax Operations Worksheet (2025–2026) — Live Preview | 49.65 | [dcse_tax_worksheet_live_preview.html](file:///c:/Users/Donald Seals/Downloads/dcse_tax_worksheet_live_preview.html) |
| deepseek_html_20260708_cf7f16.html | Sonly Consulting \| Enterprise Architecture, AI Readiness | 23.96 | [deepseek_html_20260708_cf7f16.html](file:///c:/Users/Donald Seals/Downloads/deepseek_html_20260708_cf7f16.html) |
| index.html | Sonly Consulting - Intake Portal | 0.76 | [index.html](file:///c:/Users/Donald Seals/Downloads/index.html) |
| sc_full_landing_page_v_1.html | Sonly Consulting \| Business Strategy, AI Implementation | 20.52 | [sc_full_landing_page_v_1.html](file:///c:/Users/Donald Seals/Downloads/sc_full_landing_page_v_1.html) |
| SC_Product_Preview_Digital_Campaign_MVP.html | Sonly Consulting \| Digital Campaign Upgraded MVP | 43.83 | [SC_Product_Preview_Digital_Campaign_MVP.html](file:///c:/Users/Donald Seals/Downloads/SC_Product_Preview_Digital_Campaign_MVP.html) |
| sonly-consulting-landing-v6.9.html | Sonly Consulting \| Structure Precedes Scale | 36.84 | [sonly-consulting-landing-v6.9.html](file:///c:/Users/Donald Seals/Downloads/sonly-consulting-landing-v6.9.html) |
| Sonly_Consulting_Systems_Governance_Landing_Page_20260706_v1.html | Sonly Consulting \| Systems Architecture & Governance | 18.62 | [Sonly_Consulting_Systems_Governance_Landing_Page_20260706_v1.html](file:///c:/Users/Donald Seals/Downloads/Sonly_Consulting_Systems_Governance_Landing_Page_20260706_v1.html) |
| sonly_future_experience_mvp (1).html | Sonly Consulting \| Future Experience & Retention MVP | 20176.88 | [sonly_future_experience_mvp (1).html](file:///c:/Users/Donald Seals/Downloads/sonly_future_experience_mvp (1).html) |
| sonly_future_experience_mvp (2).html | Sonly Consulting \| Future Experience & Retention MVP | 20177.54 | [sonly_future_experience_mvp (2).html](file:///c:/Users/Donald Seals/Downloads/sonly_future_experience_mvp (2).html) |
| sonly_future_experience_mvp.html | Sonly Consulting \| Future Experience & Retention MVP | 34.27 | [sonly_future_experience_mvp.html](file:///c:/Users/Donald Seals/Downloads/sonly_future_experience_mvp.html) |

### Category B: Smoove Spots (SS) & Tedo's Sports Lounge (TSL) (2 Files)
These represent user-facing layouts, simulators, or feeds for the spots/sports lounges:

| File Name | Page Title | Size (KB) | File Link |
| --- | --- | --- | --- |
| Gem BS.html | SC Sports Society \| Command Post Simulator | 6.26 | [Gem BS.html](file:///c:/Users/Donald Seals/Downloads/Gem BS.html) |
| index.html | Tedo’s Sports Lounge | 1.60 | [index.html](file:///c:/Users/Donald Seals/Downloads/DCSE Prompt Library/tedo's-sports-lounge (2)/index.html) |

### Category C: Critical Thinker's Journey (CTJ) Product (49 Files)
These are workbook files, assessments, and strategic focus flows for the CTJ reasoning brand:

| File Name | Page Title | Size (KB) | File Link |
| --- | --- | --- | --- |
| Chat 3 CTJs.html | The Critical Thinker’s Journey™ — Part 1: Foundations | 61.31 | [Chat 3 CTJs.html](file:///c:/Users/Donald Seals/Downloads/Chat 3 CTJs.html) |
| CHAT P1.html | The Critical Thinker’s Journey™ — Part 1: Foundations | 22.00 | [CHAT P1.html](file:///c:/Users/Donald Seals/Downloads/CHAT P1.html) |
| CHAT P2 CTJ.html | The Critical Thinker's Journey™ Part 2: Making Moves | 53.77 | [CHAT P2 CTJ.html](file:///c:/Users/Donald Seals/Downloads/CHAT P2 CTJ.html) |
| CTAE_CTJ_Architect_Edition_FINAL_v1.3.html | The Critical Thinker’s Architect Edition — Master System | 206.76 | [CTAE_CTJ_Architect_Edition_FINAL_v1.3.html](file:///c:/Users/Donald Seals/Downloads/CTAE_CTJ_Architect_Edition_FINAL_v1.3.html) |
| CTJ Unified Edition Combined Parts1-3 + Assessment v5.html | The Critical Thinker's Journey™ \| Unified Master Edition | 80.12 | [CTJ Unified Edition Combined Parts1-3 + Assessment v5.html](file:///c:/Users/Donald Seals/Downloads/CTJ Unified Edition Combined Parts1-3 + Assessment v5.html) |
| CTJ_Architect_Edition_v1.2_Final.html | The Critical Thinker’s Architect Edition — Master System | 206.32 | [CTJ_Architect_Edition_v1.2_Final.html](file:///c:/Users/Donald Seals/Downloads/CTJ_Architect_Edition_v1.2_Final.html) |
| ctj_focus_flow_guide.html | CTJ Focus & Flow User Guide | 35.42 | [ctj_focus_flow_guide.html](file:///c:/Users/Donald Seals/Downloads/ctj_focus_flow_guide.html) |
| SC_GYTO_Strategic_Clarity_Assessment_v7.4.html | GET YOUR THINK ON!™ \| Strategic Clarity Assessment | 61.78 | [SC_GYTO_Strategic_Clarity_Assessment_v7.4.html](file:///c:/Users/Donald Seals/Downloads/SC_GYTO_Strategic_Clarity_Assessment_v7.4.html) |
| SS CTJ Lifestyle Quiz.html | The Critical Thinker's Journey: Part 3 - Purpose | 43.39 | [SS CTJ Lifestyle Quiz.html](file:///c:/Users/Donald Seals/Downloads/SS CTJ Lifestyle Quiz.html) |

### Category D: Gifts & Supporting Utilities (Verse Vault / Scripture Selector) (4 Files)
Complimentary modular applications that serve as interactive platform gifts:

| File Name | Page Title | Size (KB) | File Link |
| --- | --- | --- | --- |
| DCSE SS Scripture Selector vs1.html | Verse Vault | 38.50 | [DCSE SS Scripture Selector vs1.html](file:///c:/Users/Donald Seals/Downloads/DCSE SS Scripture Selector vs1.html) |
| DCSE SS Scripture Selector vs2.html | Verse Vault | 45.43 | [DCSE SS Scripture Selector vs2.html](file:///c:/Users/Donald Seals/Downloads/DCSE SS Scripture Selector vs2.html) |
| verse_vault_multi_device_on_demand_bible_verse_module_single_file_html (1).html | Verse Vault | 43.17 | [verse_vault_multi_device_on_demand_bible_verse_module_single_file_html (1).html](file:///c:/Users/Donald Seals/Downloads/verse_vault_multi_device_on_demand_bible_verse_module_single_file_html (1).html) |

---

## 6. Deliverable Mapping: Rebuild Routing Rules

The executioner of the rebuild must route audited files into the following designated spaces:

### Lane 1: Public Website Scope (Include in Rebuild)
These files represent user-facing layouts, profiles, assets, and plans to be compiled into the public website build:
*   **Sonly Consulting Core Pages:** Main landing layouts, intake portals, and resume content (`DCS-Resume-v4.0.html`).
*   **Smoove Spots Pages & Feeds:** Staging previews, map coordinates, and media assets mapped in `SS_RECONCILED_COPY_PLAN.csv`.
*   **Tedo's Sports Lounge (TSL):** Athletics lounge feed templates.
*   **Critical Thinker's Journey (CTJ):** Unified learning modules and Strategic Clarity Assessment v7.4 interactive pages.
*   **Verse Vault (Gifts):** The multi-device scripture selector widget (`DCSE SS Scripture Selector vs2.html`).
*   **Domain Settings:** DNS records (`sonlyconsulting.com (DNS Records).csv`) for release deployment.

### Lane 2: Internal Platform Scope (Keep Out of Website Rebuild)
These files represent local utilities, configurations, and RAG vector databases used to run the Command Post. They must NOT be integrated into the public repository or deployment bundle:
*   **Daemon Jobs & Sorter Python Scripts:** HTML processor (`job_html_processor.py`), downloads sorter (`job_downloads_archive_router.py`), poller scripts, and daemons.
*   **Admin Dashboard Utilities:** Admin control panel interfaces (`DCSE Admin Control Portal.html`) and blog editors.
*   **RAG Knowledge Indexes:** NotebookLM exports and chat conversation logs.

### Lane 3: Security & Purge Audits (Strictly Excluded & Firewalled)
These files are logs of credential exposures, secret audit scans, and token purges:
*   Includes `credential_exposure_audit.csv`, `credential_artifacts_to_purge.csv`, and `secret_module_search_results.csv`.
*   *Action:* Retained in local git-ignored environments for administrator purges. Do not include in any staging build or public code repository.

### Lane 4: Legal & PS Firewall (Strictly Blocked)
These files represent Pro Se litigation logs, subpoena details, case deficiency lists, and case narratives:
*   Includes `AG_PHASE1_PS_FILE_INVENTORY.csv`, `Bates_Index_Provisional.csv`, `Deficiency_Log___For_Service.csv`, `PS_900-953_FINAL_litigation_review.csv`, and any file containing the labels *seals*, *dhhs*, *litigation*, or *pro se*.
*   *Action:* Absolutely blocked from all web portal codebases and repository paths. Stored only in isolated offline folders.
