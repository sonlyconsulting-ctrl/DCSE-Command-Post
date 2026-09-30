# DCSE Protocol Adapter: Directed Instruction / Interactive Chat

**Document ID:** DCSE-ADAPTER-DIRECTED-INSTRUCTION-v1
**Version:** 1.0
**Target Capability:** Environment without direct Git CLI or shell execution (e.g. ChatGPT web interface, Claude web UI, interactive assistant windows)
**Authority:** DCS (Handoff DCSE-WORKFLOW-HO-20260930-04)
**Status:** CANDIDATE

## 1. Capability Discovery
Before applying this adapter, execute discovery:
1. Verify if environment lacks tool-based command execution or direct shell invocation.
2. If shell commands cannot be run directly, apply this adapter.

## 2. Protocol Step Mappings
1. **Resolve Authority & Scope:** Output the full Shared Action Contract block at the beginning of the response. State authorizing authority (DCS) and current lifecycle status (CANDIDATE).
2. **Verify Baseline:** Rely on user-provided branch and commit baseline context. Do not invent commit SHAs or assume repository state without input.
3. **Isolate Task:** Explicitly identify target files and boundaries.
4. **Implement:** Provide complete, unabridged replacement blocks or targeted diff specifications.
5. **Semantic Review:** Complete self-review against DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE prior to output. Ensure zero em dashes, zero unsupported guarantees, and accurate DART routing.
6. **Commit & Push Instruction:** Provide the exact, copy-pasteable Git CLI command sequence for the operator, including staging targets, explicit commit messages with appropriate deployment controls (e.g. [skip vercel]), and push target.
7. **Remote Readback Instruction:** Provide the exact readback command (git ls-remote ...) for the operator to verify.
8. **Record Evidence:** Supply the text of the shared receipt for repository storage.
