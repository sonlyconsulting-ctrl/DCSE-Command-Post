# SC / SS / Website / Content — Source File Inventory Report

**Artifact Type:** Tribunal Source File Report
**Report ID:** SC_SS_WEBSITE_CONTENT_SOURCE_INVENTORY_20260811
**Status:** UNDER REVIEW
**Generated:** 2026-08-11
**Authority:** DCSE Master Profile v7.2 R5
**Method:** Queried dcse_json_registry_v1.json (1,401 classified entries) + direct filesystem scan of DCSE_CP_Project

---

## Query Parameters

- **Registry match:** paths containing `website`, `screen.arch`, `landing`, `multi.product`, `smoove.spots`, `sonly.consulting`, `product_lane`, `content_pack`, `content_element`
- **Exclusions:** `.next` build artifacts, `build-manifest`, `prerender-manifest`, `app-path-manifest`, `server-reference-manifest`, `node_modules`
- **Direct scan:** `DCSE_CP_Project` tree for files matching `website|screen.arch|landing|multi.product|content.pack|content.element|product.map|site.build|smoove.spots|smoove_spots|SS_|SmooveSpots`

---

## SOURCE FILES — Categorized

### A. Active Product Lane Content (Authoritative Source)

| File | Path | Size | Purpose |
|---|---|---|---|
| SS Discovery Control Note | `product_lanes\SS_Smoove_Spots\00_CONTROL\SS_SMOOVE_SPOTS_DISCOVERY_CONTROL_NOTE.md` | 1.1 KB | Defines SS = Smoove Spots (not Sports Society); 283 path matches documented |
| SS Executive Findings | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_EXECUTIVE_FINDINGS.md` | 1.2 KB | SS membership intelligence summary |
| SS Product Intelligence Receipt | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_PRODUCT_INTELLIGENCE_INVENTORY_RECEIPT.md` | 737 B | Receipt for SS intelligence inventory pass |
| SS Master Inventory CSV | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_MASTER_INVENTORY.csv` | 378 KB | Full SS product file inventory (378K) |
| SS Authority Candidates CSV | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_AUTHORITY_CANDIDATES.csv` | 39 KB | SS authority candidate files |
| SS Duplicate Groups CSV | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_DUPLICATE_GROUPS.csv` | 58 KB | SS file deduplication groups |
| SS Future Product Candidates CSV | `product_lanes\SS_Smoove_Spots\01_INVENTORY\Product_Intelligence_Inventory\SS_FUTURE_PRODUCT_CANDIDATES.csv` | 63 KB | SS product roadmap candidates |
| SS Reconciled Copy Plan | `product_lanes\SS_Smoove_Spots\01_INVENTORY\SS_RECONCILED_COPY_PLAN.csv` | 636 KB | SS content copy reconciliation plan |
| SS Stage Copy Approval Queue | `product_lanes\SS_Smoove_Spots\01_INVENTORY\SS_STAGE_COPY_APPROVAL_QUEUE.csv` | 190 KB | SS copy awaiting approval |
| TSL Product Map | `SC_TSL\02_PRODUCT_ARCHITECTURE\TSL_Product_Map.md` | 118 B | TSL product mapping stub |
| CTJ Product Map | `SC_CTJ\02_PRODUCT_ARCHITECTURE\CTJ_Product_Map.md` | 106 B | CTJ product mapping stub |
| Gov-OS Landing Page Copy | `SC_Gov-OS\05_EXTERNAL_PACKAGING\14_LANDING_PAGE_COPY.md` | 407 B | Gov-OS landing page copy |

### B. Website Build & Architecture Files

| File | Path | Size | Purpose |
|---|---|---|---|
| Gemini SC Website Product Build PDF | `Inbox_From_Downloads\dcse Gemini SC website product build idea.pdf` | 139 KB | Gemini-generated SC website product build concept |
| CTJ Master Implementation Plan PDF | `SC_CTJ\20_RECONCILED_DOCTRINE_LIBRARY\05_DUPLICATE_LINEAGE_MANIFESTS\CTJ Master Implementation Plan_ Website to Product Launch.pdf` | 189 KB | CTJ website-to-product launch plan |
| V7.1 Owned Product Harness Build Plan | `governance\_archive\v7.1_legacy\v7.1\DCSE_V7.1_OWNED_PRODUCT_HARNESS_BUILD_PLAN.md` | 9.2 KB | Historical product harness build plan |
| Readiness Audit HTML | `DCSE_Staging_HTML\readiness_audit.html` | 26 KB | Staging readiness audit page |

### C. Tribunal Records — SC Website Activity (Deduplicated)

Multiple copies exist across worktrees and audit folders. Canonical source is in `DCSE_CP_Project\_Tribunal_Inbox\`:

| File | Path | Size | Purpose |
|---|---|---|---|
| SC Website Media ClaudeCP Review | `DCSE_CP_Project\_Tribunal_Inbox\TRIBUNAL_SC_WEBSITE_MEDIA_CLAUDECP_REVIEW_20260708_NATEBJONES.md` | 4.1 KB | Claude CP review of SC website media assets |
| SC Website YouTube Gemini Intake (ChatGPT) | `DCSE_CP_Project\_Tribunal_Inbox\TRIBUNAL_SC_WEBSITE_YOUTUBE_GEMINI_INTAKE_20260708_CHATGPT.md` + `.json` | 2.1 KB / 1.8 KB | Gemini/ChatGPT intake for SC website YouTube content |
| SC Website YouTube Gemini Intake (NateBJones) | `DCSE_CP_Project\_Tribunal_Inbox\TRIBUNAL_SC_WEBSITE_YOUTUBE_GEMINI_INTAKE_20260708_NATEBJONES_CHATGPT.md` + `.json` | 2.6 KB / 2.3 KB | NateBJones ChatGPT intake for SC website YouTube content |

**Duplicates of these tribunal records found in:**
- `\_worktrees\sc-agent-os-password-recovery\_Tribunal_Inbox\` (×2)
- `\_worktrees\v7-foundation-runtime-compiler\_Tribunal_Inbox\` (×2)
- `DCSE_V7_Runtime\_Tribunal_Inbox\` (×2)
- `DCSE_V71_Qwen_Review\_Tribunal_Inbox\` (×2)
- `DCSE_Governance_Audit\_Tribunal_Inbox\` (×2)
- `DCSE_Governance_Audit_PR39\_Tribunal_Inbox\` (×2)
- `\_Tribunal_Inbox\_Daily\2026-06-19\` (×1 snapshot)
- `\_Tribunal_Inbox\_Tribunal_Inbox\` (×1 closeout)

**Total duplicates:** 18 copies of 4 unique tribunal records.

### D. SC Website Rebuild Activity (June 2026)

| File | Path | Size | Purpose |
|---|---|---|---|
| CodeX SC Website Rebuild Activity Start | `\_Tribunal_Inbox\TRIBUNAL_SESSION_REPORT_20260619_CODEX_DCSE_WEBSITE_REBUILD_ACTIVITY_START.json` | — | Session report — website rebuild kickoff |
| ChatGPT SC Gov-OS RAG Website GitHub | `\_Tribunal_Inbox\_Tribunal_Inbox\TRIBUNAL_SESSION_CLOSEOUT_20260619_CHATGPT_SC_GOVOS_RAG_WEBSITE_GITHUB.json` | — | Session closeout — Gov-OS RAG website GitHub work |

### E. NotebookLM & Chat Exports (SC Command Post Build)

| File | Path | Size | Purpose |
|---|---|---|---|
| NotebookLM Bulk Export 1 | `DCSE_CP_Project OLD\knowledge_sources\02_SC_COMMAND_POST_BUILD\DCS notebooklm-bulk-export-1778008176877.json` | — | NotebookLM knowledge export for SC Command Post |
| NotebookLM Bulk Export 2 | `DCSE_CP_Project OLD\knowledge_sources\02_SC_COMMAND_POST_BUILD\DCS notebooklm-bulk-export-1778009126950.json` | — | NotebookLM knowledge export for SC Command Post |
| Chat Export | `DCSE_CP_Project OLD\knowledge_sources\02_SC_COMMAND_POST_BUILD\DCSE chat-export-1778166485891.json` | — | ChatGPT conversation export for SC Command Post build |

### F. External/Other Content

| File | Path | Size | Purpose |
|---|---|---|---|
| Landing Content Default | `DS Litigation\PS WIN WIN WIN\tools\opencontracts\frontend\src\config\landingContent\default.json` | — | OpenContracts tool landing page config (not SC-related) |
| Landing Content Public Record | `DS Litigation\PS WIN WIN WIN\tools\opencontracts\frontend\src\config\landingContent\publicRecord.json` | — | OpenContracts tool landing page config (not SC-related) |

---

## TODAY'S ATTACHED SOURCE FILES (from Downloads)

These 6 files were attached in the current session and are the **most current working sources** for SC website content:

| # | File | Path | Size | Purpose |
|---|---|---|---|---|
| 1 | DSeals Resume July 2026 | `C:\Users\dsead\Downloads\DSeals Resume July 2026.md` | 13 KB | Professional claims source |
| 2 | SC DCSE Website Screen Arch Gemini | `C:\Users\dsead\Downloads\SC DCSE Website Screen Arch Gemini.txt` | 4 KB | 5-product architecture table |
| 3 | SC DCSE Lmareana v72 R5 B.zip | `C:\Users\dsead\Downloads\SC DCSE Lmareana v72 R5 B.zip` | 118 KB | Arena variant B build |
| 4 | SC DCSE Lmarenai v72 R5 A.zip | `C:\Users\dsead\Downloads\SC DCSE Lmarenai v72 R5 A.zip` | 1.5 MB | Arena variant A build |
| 5 | SC DCSE Chat DCS_Multi_Product_Website_Preview.html | `C:\Users\dsead\Downloads\SC DCSE Chat DCS_Multi_Product_Website_Preview.html` | 26 KB | Interactive HTML preview |
| 6 | DCSE Captain Custom Instructions | `C:\Users\dsead\Downloads\DCSE_Captain_Custom_Instructions_Under_8000.txt` | 8 KB | Governed mission instructions |

---

## Summary

| Category | File Count | Notes |
|---|---|---|
| Active Product Lane Content | 12 | SS (9 files), TSL (1), CTJ (1), Gov-OS (1) |
| Website Build & Architecture | 4 | PDFs, HTML, build plans |
| Tribunal Records (unique) | 4 | 18 duplicates exist across worktrees/audits |
| June 2026 Rebuild Activity | 2 | Website rebuild session records |
| NotebookLM/Chat Exports | 3 | SC Command Post knowledge sources |
| **Today's Attached Sources** | **6** | **Most current — Downloads folder** |
| **TOTAL UNIQUE SOURCE FILES** | **31** | |

**Status: UNDER REVIEW** — All SC/SS/website/content source files identified and categorized. Today's 6 attached files from Downloads are the most current working sources.
