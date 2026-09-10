# Tribunal Activity Manager UX Implementation Plan

**Authority:** DCSE v6.7.1 + Active v6.8 Direction  
**Lane:** DCSE-CP (Integration) / SS-SJL (Staging)  
**Status:** Candidate for DCS Review  
**Author:** AG (Antigravity) & Codex Co-Architects  

---

## 1. Goal Description

This plan outlines the architecture and execution sequence to replace the manual "Notepad" workflow for editing and reviewing Tribunal activity JSON files. It proposes a dual UX solution:
1.  **Integrated Dashboard (`/tribunal`):** A custom, rich route built into both CP web apps (Next.js/Node stack) with a backend API that reads/writes directly to the local `_Tribunal_Inbox` folder.
2.  **Standalone Manager (`tribunal_manager.html`):** A portable, serverless HTML+JS interface saved directly inside the `_Tribunal_Inbox` folder that can be double-clicked and run directly in any web browser using the HTML5 File API.

It also verifies the structural safeguards preventing **information or execution drift** during Tribunal runs.

---

## 2. Integrated Solution Architecture (Next.js CP Web App)

```
[Browser Dashboard /tribunal] <---> [API /api/tribunal] <---> [Local File System _Tribunal_Inbox/*.json]
```

### A. Backend API Routes
We will add local-only API endpoints in the CP web application:
*   **`GET /api/tribunal`**:
    *   Reads all `TRIBUNAL_*.json` files in `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`.
    *   Parses their contents into a unified JSON structure (ID, Date, Status, Roster, Responses, Reproofs).
    *   Returns the list sorted by modification time.
*   **`POST /api/tribunal`**:
    *   Receives updates for a specific JSON package.
    *   Handles modifications to `RESPONSES`, `STATUS`, and adding human notes inside the `RESPONSES.DCS` or `DCS_INTERJECTIONS` slots.
    *   Calculates and returns the new SHA-256 hash of the file.
*   **`POST /api/tribunal/refresh`**:
    *   Executes `python tribunal_inbox_ux_refresh.py` headlessly and returns the new daily index summary.

### B. Frontend UI Route (`/app/tribunal/page.tsx`)
A custom, premium dark glassmorphism dashboard containing:
*   **Active Package List Sidebar:** Displays all Tribunal JSON files, color-coded by status (e.g. green for `ACTIVE_RATIFIED`, amber for `ORCHESTRATOR_PINGED_AGENTS`, grey for completed test files).
*   **Central Workspace:**
    *   **Core Metrics:** Package ID, authority level, creation date, and current status.
    *   **Roster Response Matrix:** Interactive grid displaying the role, lane, and current signed response statement for each node. Provides an "Override / Sign" button for manual intervention.
    *   **WIN-WIN-WIN Reproof Console:** Compares the "WIN-WIN-WIN" statements of all participating models side-by-side to audit alignment.
    *   **DCS Interjection Panel:** A rich text editor allowing the user to type comments, instructions, or corrections. Saving instantly appends the entry into the live JSON file in the inbox root.
*   **System Action Panel:**
    *   Displays file details: size, last write time, and SHA-256 hash.
    *   "Run Refresh Script" button.
    *   "Export Snapshot" button.

---

## 3. Standalone Solution Architecture (`tribunal_manager.html`)

For quick, offline access without launching the Next.js development server:
*   **File Location:** [tribunal_manager.html](file:///c:/DS%20All%20Things/DCSE_Command_Center/_Tribunal_Inbox/tribunal_manager.html)
*   **Technology:** Single file, plain vanilla HTML5 + CSS Grid (modern, dark-themed glassmorphism layout) + pure vanilla JavaScript. Zero external CDNs or dependencies.
*   **Workflow:**
    1.  User opens `tribunal_manager.html` in any web browser.
    2.  User drags and drops a `TRIBUNAL_*.json` file from `_Tribunal_Inbox` into the drop zone.
    3.  JavaScript parses the JSON via the File Reader API and renders the interactive dashboard (showing status, roster, responses, and interjections).
    4.  User edits fields, types a DCS Interjection, or overrides a model's response.
    5.  User clicks **"Generate & Save JSON"** which downloads the updated JSON file.
    6.  User saves the file back to `_Tribunal_Inbox` (overwriting the original).

---

## 4. Drift Verification Analysis (Confirming Zero Drift)

The user asked to confirm that reading the JSON "reads and packages everything for execution per topic with no drift." We confirm this is correct, enforced by five structural safeguards:

```
                  DRIFT-FREE EXECUTION CYCLE
   [Strict JSON Schema] --> Enforces topic separation
            |
            v
   [SHA-256 Hashing]   --> Detects any character change
            |
            v
   [Consensus Lock]    --> Blocks transition until signed
            |
            v
   [Git Relays]        --> Prevents silent overwrites
```

1.  **Strict Schema Isolation:** Directives are packaged under explicit arrays (e.g. `construction_directives.scope`). The poller and participating models parse these arrays item-by-item rather than reading large text paragraphs. This prevents models from "summarizing" or ignoring individual topics.
2.  **Explicit Response Slots:** Roster positions are explicitly mapped. A model cannot reply out-of-context; it must write its status to its specific key under `RESPONSES` and `REPROOF_WIN_WIN_WIN.RESPONSES`. Any missing slot keeps the status locked at `PENDING`.
3.  **Cryptographic Integrity Checks:** The `tribunal_inbox_ux_refresh.py` and `job_ps_inventory.py` scripts calculate SHA-256 hashes of the files. If any node attempts to modify adjacent topics or erase history, the hash mismatches, flagging the transaction for human audit.
4.  **Consensus State Gates:** The poller will only advance the package state to `ACTIVE_RATIFIED` or `MANUAL_DRIVER_AGGREGATION_COMPLETE` once all required nodes have returned non-pending, non-empty response blocks.
5.  **Git Conflict Guardrails:** The `_Tribunal_Inbox` is a Git repository. If Qwen Coder and Codex attempt to modify the same JSON concurrently, Git blocks the push and raises a merge conflict. This forces the poller to hold execution until the contradiction is resolved, preventing silent information loss.

---

## 5. Proposed Changes

### [NEW] [tribunal_manager.html](file:///c:/DS%20All%20Things/DCSE_Command_Center/_Tribunal_Inbox/tribunal_manager.html)
A standalone, drag-and-drop HTML dashboard for local browser execution.

### [NEW] [api/tribunal/route.ts](file:///c:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/api/tribunal/route.ts)
Endpoint to read and edit Tribunal JSON files from the inbox.

### [NEW] [app/cp/tribunal/page.tsx](file:///c:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/cp/tribunal/page.tsx)
Next.js UI dashboard route.

### [MODIFY] [cp/page.tsx](file:///c:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/cp/page.tsx)
Add link "Tribunal Manager" to the navigation header.

---

## 6. Verification Plan

### Automated Checks
*   Verify `tribunal_manager.html` passes local W3C validation.
*   Test that Next.js compiling completes without routing errors.
*   Assert that `TRIBUNAL_*.json` updates write exactly back to the inbox with updated SHA-256 hashes.

### Manual Verification
1.  Open `tribunal_manager.html` in a local browser, drag-and-drop a launch JSON, add an interjection, and download the output. Confirm the structure matches the original schema.
2.  Navigate to `/cp/tribunal` in the local web app, verify the roster shows Codex as "VERIFIED" and other models as "PENDING".
3.  Type a test interjection from the dashboard, save it, and verify it updates the root JSON file on disk.
