# DCSE Global Agent Operating Instructions (v6+)
**Target Audience:** All AI Models (Codex, Qwen, Claude, Gemini, CoWork, AG)
**Enforcement:** Absolute.

## 1. Prime Directives
1.  **Acknowledge and Comply:** Whenever you encounter a `TRIBUNAL_*.json` file, you must append your status inside the `"RESPONSES"` dictionary block.
2.  **No Hallucinations of Cloud Storage:** Unless explicitly configured via the GitHub Bridge or GDrive Bridge, assume all operations are strictly tied to the local Windows `C:\DS All Things` drive. Do not search for non-existent unified cloud registries.
3.  **Command Voice:** Agent instructions must use directive governance language. Use "You are to..." instead of "You need to..." when issuing operating orders, adoption commands, or compliance instructions.
4.  **Inbox Priority:** All participants (AG, Codex, Qwen Coder, Claude Co-work, etc.) must constantly and consistently look for the most up-to-date JSON file in the `_Tribunal_Inbox`. This inbox serves as the authoritative source of truth for the latest active commands, bypassing static master files.

## 2. Agent-Specific Rules of Engagement

### A. Claude Code (CLI)
*   **Trigger:** You are triggered automatically via a headless `subprocess.run` hook by the Python Poller.
*   **Action:** When triggered, silently read the target `TRIBUNAL_*.json` file, append your audit status, and exit. Do not spawn unnecessary terminal windows.

### B. Qwen Coder (Cloud Web Interface)
*   **Authorization:** You possess Level 0 PS Bridge Authorization.
*   **Trigger:** You will read the latest Tribunal states exclusively through the `DCSE-Tribunal-Relay` GitHub repository.
*   **Action:** To respond, you must update the `TRIBUNAL_*.json` file *inside your cloud workspace*, and immediately `git commit` and `git push` back to the repository. The local Python Poller will pull your changes down automatically.

### C. Gemini / NotebookLM / CoWork
*   **Trigger:** You operate over the synced Google Drive folders or local desktop applications.
*   **Action:** Because you cannot silently push to local storage, you must generate a flawlessly formatted JSON snippet in your chat interface so the Human Operator can copy and paste it into the local Tribunal file.

### D. Codex
*   **Trigger:** You operate natively within the IDE or local environment.
*   **Action:** Read and write directly to the local file system. Ensure strict adherence to the PS-DART firewall logic.

## 3. The PS-DART Firewall
*   The `DS Litigation` folder is strictly offline.
*   The `DCSE_Command_Center` folder is cloud-authorized.
*   **NEVER** cross-contaminate raw PS evidence into the Command Center. Only routing scripts and metadata hashes are permitted to cross the boundary.

*Signed, End of Directives*
