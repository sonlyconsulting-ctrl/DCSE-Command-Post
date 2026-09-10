# TRIBUNAL INSTRUCTION: Gemini Activity File Creation Protocols (v1.0)

**Date:** 2026-07-01  
**Target:** Gemini (Advanced Agentic Coding Assistant)  
**Lane:** SC // Command Post // Governance // Operational Control  
**Authority:** DCS Level 0 / AG Agents  
**Status:** ACTIVE DIRECTIVE  

## 1. Context and Objective
Gemini sessions are governed by the Tribunal Mandatory Reporting Rule (Adopted 2026-06-18) and the inbox-primacy rule. Every session must end with a structured report filed directly into the `_Tribunal_Inbox` to coordinate and sync state between sessions.

Since Gemini operates via terminal tools or copy-paste interfaces, Gemini must execute direct file writes when workspace tools are equipped, or output raw snippets to the human operator if tools are restricted.

## 2. Naming Conventions for Activity Files
Every session must produce two files in `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`:

1.  **Full Session Report (JSON):**
    *   **Name Pattern:** `TRIBUNAL_YYYYMMDD_[LANE_OR_SUMMARY].json`
    *   **Template:** Follow `TRIBUNAL_SESSION_REPORT_TEMPLATE.json` structure.
2.  **Daily Activity Sync (JSON):**
    *   **Name Pattern:** `TRIBUNAL_ACTIVITY_SYNC_YYYYMMDD.json`
    *   **Template:** Follow the brief sync structure with `date`, `activity`, `system_commits`, and `governance_status`.

*(Note: Replace `YYYYMMDD` with the local session date, e.g., `20260701`)*

## 3. Step-by-Step Execution Guide for Gemini

### Step 1: Scan and Read Before Writing
1.  Always read `AGENTS.md` in the command center root to verify active stop-gates.
2.  Search the `_Tribunal_Inbox` for the most recent `TRIBUNAL_*.json` files to pull forward any open interjections or instructions from DCS.

### Step 2: Compile the Session Accomplishments
Group accomplishments into clear categories matching active tracks:
*   `governance` (adoptions, rule updates)
*   `infrastructure` (path configs, workspace setups)
*   `TSL` (lounge UI/UX, admin console progress)
*   `SJL` (GPS, cloud architecture, legal matrices)
*   `CTJ` / `RAG` / `Ollama` (RAG vector modeling, local model runtimes)
*   `litigation_prep` / `PS` (segregated litigation facts, deficiency logs)

### Step 3: Implement Mandatory Reporting Checklists
The report's `mandatory_reporting` object must contain:
*   `files_read`: Array of absolute paths of files examined.
*   `files_created`: Array of absolute paths of files generated.
*   `files_edited`: Array of absolute paths of files updated.
*   `files_skipped`: Array of objects detailing skipped files and reasons.
*   `restrictions_followed`: Affirmation of DART firewall, no secrets, local-only limits.
*   `pending_dcs_response_items`: Decisions required from DCS Level 0.
*   `next_recommended_action`: Next command string to be run.
*   `json_updated_and_validated`: `true`.

### Step 4: Define Response Slots
Always initialize the `RESPONSE_SLOTS` with:
*   `"DCS": "PENDING_REVIEW"`
*   `"Gemini": "COMPLETED_SESSION"`

### Step 5: Write the Files Natively
Use `write_to_file` to write the files directly to `_Tribunal_Inbox` without creating an Antigravity artifact metadata block unless writing internally to the brain database.

## 4. Active Stop-Gates for Gemini
*   **NEVER** write raw PS/litigation facts, credentials, API keys, or private URLs in the activity files.
*   **NEVER** perform `git add .` or stage unapproved directories.
*   **NEVER** execute production database migrations or Vercel updates without explicit DCS Level 0 clearance.

*End of Instructions*
