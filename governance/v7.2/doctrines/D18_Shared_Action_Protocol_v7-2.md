# DCSE DOCTRINE D18: Shared Action Protocol

**Document ID:** D18_Shared_Action_Protocol_v7-2
**Version:** 1.0 (v7.2 R5)
**Status:** CANONICAL
**Scope:** Universal multi-agent workflow execution and validation

## 1. Core Principle
This doctrine eliminates recurring permission loops, mechanical string-replacement drift, and isolated execution silos by establishing one canonical workflow protocol for all participating agents. It separates artifact state from action authority and enforces semantic whole-artifact review over isolated exact-phrase compliance.

## 2. The Shared Action Protocol Execution Loop
Every agent executing a task within the DCSE Command Post ecosystem must rigidly adhere to this sequence:

1.  **Resolve Authority:** Determine the task scope, existing DCS authorization, and the exact boundaries of the delegated work. Do not request intermediate approvals for work that falls inside this authorized scope.
2.  **Verify Baseline:** Inspect the repository state, target branch, and remote remote parity before making edits. Unrelated work on the branch must be preserved.
3.  **Isolate the Task:** Formulate the Shared Action Contract for the execution session and identify the specific files requiring modification.
4.  **Implement:** Execute the structural or content modifications in accordance with the specified DART routing and Master Voice parameters.
5.  **Check Full Result:** Execute a whole-artifact semantic acceptance review against the DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE. Mechanical compliance (e.g., swapping a single word while leaving absolute outcome promises intact) is prohibited.
6.  **Commit and Push:** Commit within the specified scope, applying necessary Vercel suppression tags ([skip vercel]), and push to the remote repository. Verify the remote state (readback).
7.  **Record Evidence:** Generate the Shared Action Receipt and store it in an authorized, accessible shared repository location. Do not claim production publication without direct evidence.

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

## 4. Agent Adapters
Because agents operate utilizing different tooling (e.g., Git CLI vs API payload), each participating model (AG, ChatGPT, Claude) receives an adapter. The adapter specifies *how* the agent executes the 7-step sequence using its available tools, without altering the protocol itself.
