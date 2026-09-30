# DCSE Protocol Adapter: Local Shell / Git CLI

**Document ID:** DCSE-ADAPTER-LOCAL-SHELL-GIT-v1
**Version:** 1.0
**Target Capability:** Environment with direct shell access and Git CLI (e.g. Antigravity, local developer terminals, container runtimes)
**Authority:** DCS (Handoff DCSE-WORKFLOW-HO-20260930-04)
**Status:** CANDIDATE

## 1. Capability Discovery
Before applying this adapter, execute discovery:
1. Verify shell execution: Run basic command (e.g., git --version).
2. Verify repository context: Run git rev-parse --is-inside-work-tree and git status.
3. If Git CLI is absent or unavailable, fail over to the API or Directed Instruction adapter.

## 2. Protocol Step Mappings
1. **Resolve Authority & Scope:** Record Shared Action Contract with Task ID, Handoff ID, and DCS authorization scope.
2. **Verify Baseline:**
   - Execute git status --short to inspect working tree state and isolate unrelated work.
   - Execute git ls-remote origin refs/heads/<target-branch> to confirm remote branch SHA before making changes.
3. **Isolate Task:** Restrict edits solely to authorized path targets.
4. **Implement:** Execute edits via native filesystem tools or file edit tools.
5. **Semantic Review:** Evaluate modified files against DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE. Prohibit mechanical string swaps that preserve absolute promises.
6. **Commit & Push:**
   - Stage only authorized target files (git add <files>).
   - Commit with explicit scope and verified deployment controls (e.g., [skip vercel] where build suppression is required).
   - Push to remote: git push origin <branch>.
7. **Remote Readback:** Query git ls-remote origin refs/heads/<branch> and verify the full commit SHA matches the local HEAD.
8. **Record Evidence:** Write shared receipt into repository under governance/v7.2/implementations/.
