# DCSE Agent Adapter: Antigravity (AG)

**Document ID:** AGENT_ADAPTER_AG_v1
**Version:** 1.0 (v7.2 R5 Protocol Map)
**Target Entity:** Antigravity (Google)
**Execution Posture:** Command Post / Execution Owner

## 1. Adapter Purpose
This adapter dictates how the Antigravity (AG) agent interacts with the DCSE Shared Action Protocol (D18). It maps AG's native tool capabilities to the 7-step execution loop, ensuring protocol compliance without requiring protocol alteration.

## 2. Tool Mapping & Access
AG executes operations utilizing a local Windows command-line environment and file system tools.

*   **Repository Access:** Native file system navigation via default_api:run_command (PowerShell) and default_api:view_file.
*   **Git Interactions:** PowerShell git commands (git status, git add, git commit, git push origin).
*   **Content Modification:** Directed usage of default_api:replace_file_content for precise block edits and default_api:write_to_file for new artifact creation.

## 3. Protocol Execution Directives
When AG receives a workflow directive governed by D18, it must execute the following mapping:

1.  **Resolve & Isolate:** AG must generate the Shared Action Contract internally before issuing tool calls. AG will NOT halt to ask DCS for permission if the task falls within the provided Handoff ID authorization scope.
2.  **Baseline Check:** AG must run git status --short; git log -1 --stat prior to any file writes to isolate unrelated ESCD workflow changes.
3.  **Semantic Review:** AG must download/view the target files in full and evaluate them against the DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE rather than blindly relying on targeted search-and-replace for single strings.
4.  **Verification Readback:** AG must capture the stdout of the git push origin <branch> command and record the exact commit hash in the final shared receipt.
