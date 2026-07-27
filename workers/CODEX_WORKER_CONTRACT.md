# Phase 1E: Codex Worker Contract

**Status:** Contract specification (Phase 1E) - scaffolding only, full implementation deferred to Phase 2.

**Worker Identity:** `AGENT-CODEX-PREMIUM-01@STAGING`
**Model:** Claude 3.5 Sonnet or later (highest-context model)
**Execution Mode:** Implementation + Code Review
**Authorization:** Requires explicit cost approval for each task

---

## Premium Task Restrictions

Codex is NOT a default worker. It is exclusively reserved for high-value, complex tasks that justify premium model costs ($5-50+ per task).

### ✅ Approved Use Cases

1. **CP Dashboard Reconstruction** — Multi-page UI rebuild, state management, real-time sync with Supabase
2. **Complex Multi-File Implementation** — Projects affecting 10+ files across multiple domains
3. **Context Compiler** — Building cross-module knowledge bases and architecture synthesis documents
4. **Difficult CI/Pipeline Repair** — Fixing complex GitHub Actions, Vercel deployments, build toolchain issues
5. **Cross-Module Integration** — Coordinating changes across multiple codebases or services
6. **Complex Refactoring** — Rewriting large sections with architectural improvements
7. **Repository-Wide Acceptance Remediation** — Preparing repositories for compliance/standards migration

### ❌ Blocked Use Cases

- **Polling and task monitoring** — use Dispatcher Service instead
- **File inventories and listings** — use Glob or Grep tools
- **Deterministic validation** — use DeterministicValidator script
- **Routine repair work** — use Qwen Implementation Worker
- **Summaries and receipts** — use Claude Reviewer Worker
- **Basic checks and syntax fixes** — use automated linting
- **Repetitive transformations** — script or batch process instead
- **Ad-hoc investigations** — use Agent tools with narrower scope

---

## Task Contract Requirements

Every Codex task MUST include all of the following:

### 1. Usage Justification
```
Why Codex?
- Complexity: [brief explanation of why this requires highest-context model]
- Scope: [number of files, domains involved]
- Estimated cost: $[5-50+]
- Business impact: [what value does this deliver?]
```

### 2. Bounded Context
```
Files in scope:
  - apps/sc-agent-os/api/index.js (primary)
  - apps/sc-agent-os/migrations/* (secondary)
  - ...

Files OUT of scope:
  - supabase/migrations/20260728_* (blocked)
  - PS/* (product firewall)
  - ...
```

### 3. File Scope Manifest
```
Approved for modification:
  - [List every file Codex is authorized to change]

Read-only inspection:
  - [List files Codex may read but not modify]

Forbidden access:
  - PS/*
  - credentials
  - .env
  - [etc]
```

### 4. Acceptance Tests
```
Task succeeds when:
  [ ] Test 1: [specific condition]
  [ ] Test 2: [specific condition]
  [ ] Test 3: [specific condition]
  
Tests fail when:
  [✗] Security violation
  [✗] Files modified outside approved scope
  [✗] Cost exceeds ceiling
```

### 5. Attempt Ceiling
```
Max attempts: [typically 1-3]
Reason: [why is the ceiling this value?]
Cost-stop ceiling: $[max total cost across all attempts]
```

### 6. Approval Gate
```
Approval required from:
  [ ] Team lead (by name/role)
  [ ] Architecture reviewer
  [ ] Cost approval (if >$10)
  
Created: [date/time]
Expires: [date/time - typically 24 hours]
```

---

## Example: CP Dashboard Reconstruction

```markdown
# Codex Task: CP Dashboard Reconstruction

## Justification
- **Why Codex?** Full-stack UI rebuild across 3 files with state synchronization
  to live Supabase infrastructure. Requires architectural decisions, component
  design, and integration testing across new features.
- **Complexity:** 45+ component state changes, 8 new API routes, real-time
  connection handling
- **Scope:** Primary UI dashboard (sc-agent-os/api/index.js), 3 Supabase RPC
  functions, 2 migration helpers
- **Estimated cost:** $25-35
- **Business impact:** Enables live monitoring of V7 worker queue, heartbeats,
  task claims, results, and stop-gates

## Bounded Context
### Files in scope (approved for modification):
- apps/sc-agent-os/api/index.js (dashboard section only, lines 1500-2750)
- 02_ARCHITECTURE/CP_DASHBOARD_SCHEMA.md (documentation)
- tests/cp-dashboard-e2e.test.js (new file)

### Read-only inspection:
- supabase/migrations/20260728_v7_agent_worker_communication_system.sql
- 02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md
- supabase/functions/v7-worker-auth/index.ts

### Forbidden access:
- supabase/migrations/20260728_* (Phase 1A - read-only reference only)
- PS/* (product firewall - zero access)
- *.env (secrets)
- credentials, keys, tokens

## File Scope Manifest
**Can modify:**
- apps/sc-agent-os/api/index.js: handleDashboard, handleDashboardData functions

**Can read:**
- supabase/migrations/20260728_v7_agent_worker_communication_system.sql
- 02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md
- MODEL_REGISTRY.yaml

**Blocked:**
- .env files
- PS documentation
- Production migration files

## Acceptance Tests
✅ Task succeeds when:
- [ ] Dashboard loads with "Worker Health" panel active
- [ ] Live Supabase data flows to dashboard (heartbeats, queues, claims, results)
- [ ] Real-time updates work (new tasks appear within 5 seconds)
- [ ] All 8 proof points from Phase 1A are visible (worker ID, heartbeat count, task status)
- [ ] No browser console errors
- [ ] E2E tests pass (Playwright)
- [ ] Performance: dashboard loads < 2s cold start
- [ ] No secrets exposed in frontend code

❌ Task fails if:
- [✗] Files modified outside approved scope
- [✗] PS content accessed or referenced
- [✗] Cost exceeds $40 ceiling
- [✗] Takes more than 2 attempts
- [✗] Security validation fails

## Attempt Ceiling
**Max attempts:** 2
**Reason:** Complex UI work is high-cost; if 2 attempts fail to achieve acceptance
tests, escalate to team for architectural review instead of retry.
**Cost-stop ceiling:** $40 total across both attempts

## Approval Gate
**Requires approval from:**
- [ ] Team Lead (product owner)
- [ ] Architecture Reviewer (V7 system owner)
- [ ] Cost Approval (>$10 threshold)

**Created:** 2026-07-27T21:00:00Z
**Expires:** 2026-07-28T21:00:00Z (24 hours)

**Approved by:** [signature/approval record]
**Date approved:** [date/time]
```

---

## Deployment

Codex worker shares infrastructure with Claude Reviewer and Qwen workers:
- Same queue system (pgmq)
- Same heartbeat mechanism (v7_worker.heartbeat)
- Same cost ledger tracking
- Same authorization scopes (but with premium_codex lane added)

Deploy as:
```bash
node workers/codex-worker.js
# OR
docker run dcse/codex-worker:v1
# OR
gcloud run deploy dcse-codex --image dcse/codex-worker:v1
```

---

## Cost Accounting

All Codex tasks are charged to a separate cost center:
- Monthly budget: $500 (premium tasks only)
- Per-task ceiling: $50 (can be raised with approval)
- Tracking: v7_worker.cost_ledger with `worker_id = 'AGENT-CODEX-PREMIUM-01@STAGING'`
- Reporting: Dashboard shows Codex spend separately from standard workers

If monthly spend exceeds $500, task queue is paused and escalated for budget review.

---

## Security Posture

1. **No automatic approval:** Every Codex task requires explicit cost + scope approval
2. **Bounded context:** Task definition must list exact files and forbidden paths
3. **Deterministic validation mandatory:** Result must pass validation suite before acceptance
4. **Audit trail:** Every task execution logged with cost, files touched, approval record
5. **Reversion protocol:** If tests fail, automated rollback to previous commit

---

## Success Criteria for Phase 1E

✅ Contract specification complete and approved by architecture team
✅ Example task (CP Dashboard Reconstruction) approved and scheduled
✅ Cost approval workflow integrated with stop-gate system
✅ Codex worker implementation ready for Phase 2 (deferred)
✅ Documentation available to team

**Status:** Phase 1E contract complete. Full worker implementation in Phase 2.

---

## Next Phase: Phase 1E-2 Codex Worker Implementation

Once contract is approved, Phase 2 includes:
1. `workers/codex-worker.js` — full Claude Agent SDK worker with premium capabilities
2. `tests/codex-*.test.js` — comprehensive test suite for each approved use case
3. `CP_DASHBOARD_RECONSTRUCTION.md` — first real Codex task specification
4. `CODEX_COST_TRACKING.md` — billing and budget controls
5. PR #18-20 — Codex implementation and initial tasks

---

## Maintenance

This contract requires review and update:
- **Quarterly:** Adjust approved use cases based on operational experience
- **When new models released:** Update model recommendations
- **When costs change:** Adjust per-task and monthly ceilings
- **When security policies change:** Add new blocked patterns

Last updated: 2026-07-27
Maintained by: Architecture Team
