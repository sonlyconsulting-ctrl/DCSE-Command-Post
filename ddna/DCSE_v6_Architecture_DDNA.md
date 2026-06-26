# DCSE Command Center v6+ Architecture DDNA
**Classification:** GLOBAL KNOWLEDGE BASE
**Date:** June 1, 2026
**Architect:** AG (Antigravity) & DCSE Directorship

## 1. Executive Summary
The v6+ DCSE Command Center resolves the critical tension between cloud-connected AI (Qwen, Gemini) and offline, highly-sensitive Pro Se litigation materials (PS-DART). By implementing a "Hub and Spoke" local directory structure combined with automated Git/Cloud pipelines, the architecture achieves 100% offline security while retaining full cloud AI orchestrations.

## 2. The Hub and Spoke Architecture
The local hard drive (`C:\DS All Things`) is segregated into two primary operational zones:

### The Hub (`DCSE_Command_Center`)
*   **Purpose:** The central nervous system and integration layer.
*   **Contents:**
    *   `DCSE_CP_Project` (Enterprise code and assets)
    *   `_Tribunal_Inbox` (The core JSON communication bus for AI models)
    *   `job_tribunal_poller.py` (The Python Orchestration Engine)
    *   `_V6_MASTER_AI_INSTRUCTIONS.md` (Global AI behavior overrides)
*   **Cloud Status:** Approved for sync via Google Drive Desktop and GitHub Bridge.

### The Spoke (`DS Litigation`)
*   **Purpose:** The PS-DART Litigation vault.
*   **Contents:** 100% of Pro Se legal materials, DART reports, and evidence.
*   **Cloud Status:** STRICTLY OFFLINE. Never synced to cloud drives. Accessed by Hub scripts via strict path routing.

## 3. The Automation Engines
Three primary Python daemons handle cross-lane asset routing without breaching the firewall:
1.  **`job_downloads_archive_router.py`:** Sweeps the Windows Downloads folder. Uses keyword matching ("seals", "823cv489", "dart") to funnel PS evidence directly to the offline Spoke, and Enterprise assets directly to the Hub.
2.  **`job_html_processor.py`:** Sweeps the entire `C:\DS All Things` drive for stray HTML modules and routes them to their respective staging environments based on content signatures.
3.  **`job_ps_inventory.py`:** Generates `ps_ddna_registry.json` locally to catalog offline evidence via SHA-256 hashing.

## 4. The Intelligence Bridges (Cloud-to-Local Orchestration)
To allow web-bound models (Qwen, Gemini) to participate in local orchestration without compromising the offline Spoke, two bridges are established:

### A. The GitHub Bridge (For Qwen Coder)
*   **Mechanism:** The `_Tribunal_Inbox` is initialized as a local Git repository linked to a private remote (`DCSE-Tribunal-Relay`).
*   **Outbound:** The Python Poller detects local Tribunal JSON modifications and instantly executes a headless `git push`.
*   **Inbound:** Every 120 seconds, the Poller executes a headless `git pull`. If Qwen has modified the JSON via its web container, the changes are pulled locally, instantly triggering Tier 1 local agents (Claude/Codex).

### B. The GDrive Bridge (For Gemini & NotebookLM)
*   **Mechanism:** The Hub (`DCSE_Command_Center`) is synced via Google Drive Desktop.
*   **Operation:** Gemini reads the synced Tribunal files. It responds either by generating JSON for manual user copy/paste back into the local drive, or via a Google Apps Script Webhook.

## 5. Security & Governance Matrix
*   **Level 0 PS Bridge Authorization:** Granted exclusively to designated CCO models (Qwen) via explicit instruction files.
*   **Contamination Rule:** No file containing PS-DART evidence may be moved into the `DCSE_Command_Center` root or `_Tribunal_Inbox`. Only Tribunal status hashes and metadata are permitted in the Hub.

*Signed, End of Report*
