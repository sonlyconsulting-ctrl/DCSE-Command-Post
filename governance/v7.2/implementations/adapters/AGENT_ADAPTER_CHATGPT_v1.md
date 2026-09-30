# DCSE Agent Adapter: ChatGPT

**Document ID:** AGENT_ADAPTER_CHATGPT_v1
**Version:** 1.0 (v7.2 R5 Protocol Map)
**Target Entity:** ChatGPT (OpenAI)
**Execution Posture:** Command Post

## 1. Adapter Purpose
This adapter dictates how ChatGPT interacts with the DCSE Shared Action Protocol (D18). Because ChatGPT often operates in environments without direct Git CLI access, this adapter standardizes how it receives baselines and outputs implementable code blocks for the user or a connecting script.

## 2. Tool Mapping & Access
ChatGPT executes operations utilizing provided context windows, code interpretation, or connected APIs (e.g., GitHub Actions).

*   **Repository Access:** Relies on user-provided repository snapshots or API-based repository retrieval.
*   **Git Interactions:** If connected to a GitHub API, uses API calls to create branches, commits, and PRs. If unconnected, outputs raw code blocks with explicit file paths for the user to commit.
*   **Content Modification:** Re-writes full files or provides exact diff blocks.

## 3. Protocol Execution Directives
When ChatGPT receives a workflow directive governed by D18, it must execute the following mapping:

1.  **Resolve & Isolate:** ChatGPT must output the Shared Action Contract at the top of its response. It must acknowledge its authorized scope before generating code.
2.  **Semantic Review:** ChatGPT must self-validate its output against the DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE *before* generating the final response. It must explicitly verify that no absolute guarantees or prohibited punctuation were introduced.
3.  **Handoff / Verification:** If unconnected to Git, ChatGPT must end its response with the required git commit -m syntax including [skip vercel] tags, instructing the user on how to correctly commit the artifact to the Command Post repository.
