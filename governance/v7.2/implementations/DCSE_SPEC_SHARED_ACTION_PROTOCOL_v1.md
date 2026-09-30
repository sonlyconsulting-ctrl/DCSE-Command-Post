# DCSE Specification: Shared Action Protocol

**Document ID:** DCSE-SPEC-SHARED-ACTION-PROTOCOL-v1
**Version:** 1.0 (v7.2 R5 Implementation Specification)
**Authority:** DCS (Handoff DCSE-WORKFLOW-HO-20260930-04)
**Status:** CANDIDATE (Authorized for multi-agent development and evaluation)
**Scope:** Universal multi-agent workflow execution, verification, and automated enforcement

## 1. Core Principle
This specification eliminates recurring permission loops, mechanical string-replacement drift, and isolated execution silos by establishing one canonical workflow protocol across all participating agents and platforms. It strictly separates artifact lifecycle state (e.g., CANDIDATE) from action authority and enforces semantic whole-artifact review over isolated exact-phrase compliance.

## 2. The Shared Action Protocol Execution Loop
Every participating agent executing an authorized task within the DCSE Command Post ecosystem must adhere to this sequence:

1.  **Resolve Authority and Scope:** Determine the task scope, existing DCS authorization, and the exact boundaries of the delegated work. Do not request intermediate approvals for work that falls inside this authorized scope.
2.  **Verify Baseline:** Inspect the repository state, target branch, and query the remote commit SHA (e.g., via git ls-remote) before making edits. Unrelated work on the branch must be preserved.
3.  **Isolate the Task:** Formulate the Shared Action Contract for the execution session and identify the specific files requiring modification.
4.  **Implement:** Execute the structural or content modifications in accordance with the specified DART routing and Master Voice parameters.
5.  **Check Full Result:** Execute a whole-artifact semantic acceptance review against the DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE. Mechanical compliance (e.g., swapping a single word while leaving absolute outcome promises intact) is prohibited.
6.  **Commit and Push:** Commit within the specified scope, applying verified deployment controls (e.g., [skip vercel]), and push to the remote repository.
7.  **Remote Verification Readback:** Explicitly query the remote branch ref to verify that the remote commit SHA matches the local commit SHA.
8.  **Record Evidence:** Generate the Shared Action Receipt and store it in an authorized, accessible shared repository location. Do not claim production publication or platform-setting compliance without direct evidence.

## 3. Shared Action Contract Requirements
Every execution session must be governed by a Shared Action Contract containing the following explicit fields:
*   Task ID / entity / owner
*   Authority source / existing DCS authorization / scope
*   Artifact lifecycle state (e.g., CANDIDATE)
*   Authorized next actions
*   Reserved actions requiring additional approval (e.g., live deployment)
*   Applicable DART route (Command Post/SC or Protected PS)
*   Acceptance criteria / evidence locations
*   Handoff ID

## 4. Operational DART Routing
*   **Command Post / SC Route:** In ordinary commercial and operational contexts, DART routes to: Discovery, Assess, Refine, Transfer.
*   **Protected PS Route:** For sovereign legal, litigation, and forensic matters, DART routes to: Discovery, Attack, Rebuttal, Trial. Protected instructions, burden-shifting legal frameworks, and litigation assets must remain strictly segregated within the separately governed Protected adapter.
