# DCSE V7 COMP 001: Architecture Review and Remediation

**Status:** Ready for Autonomous Execution  
**Assigned to:** Claude Reviewer Worker (Blueprint Mode)  
**Created:** 2026-07-27  
**Priority:** P0 - Blocks V7 deployment  
**Estimated effort:** 2-4 hours autonomous review + deterministic validation  

---

## Executive Assignment

Review the complete DCSE V7 Agent Worker Communication System implementation in PR #14 and live codebase.

**Output required:**
- Architecture findings (defects, risks, design gaps)
- Code and schema inspection results
- Automatic repairs (Blueprint Mode only)
- Repair task package for Qwen implementation worker
- Contradiction register
- Acceptance scorecard
- Level 0 decision packet for DCS promotion authority

**Success criterion:**
> Claude reviewer claims this task autonomously, compiles correct runtime packet from live PR #14 artifacts, evaluates actual code and schema, submits structured findings, and creates authorized repair tasks for Qwen while preserving Level 0 promotion authority.

---

## Scope: What to Inspect

### 1. Architecture Blueprint
**File:** `02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md`

Verify:
- [ ] Layer diagram accuracy (Data, Queue, Worker, Result, Governance)
- [ ] Worker lifecycle documented (heartbeat, claim, execute, submit, validate, archive)
- [ ] Visibility timeout behavior correct (30-min lease, 5-min renewal)
- [ ] Stop-Gate pattern properly explained
- [ ] Dead-Letter Queue routing logic sound
- [ ] Cost tracking and per-agent limits clear
- [ ] Security model: secret management, tool permissions, lane isolation
- [ ] Integration points with dcse_cp schema defined

**Defect examples to catch:**
- Incomplete visibility timeout example
- Missing heartbeat renewal interval
- Unclear deterministic validation handoff
- Ambiguous Level 0 promotion rules

### 2. Migration Files
**Files:**
- `supabase/migrations/20260728_v7_agent_worker_communication_system.sql`
- `supabase/migrations/20260716190000_vow_go_application_support_v1.sql`

Verify migration 20260728:
- [ ] `pgmq` extension created with schema
- [ ] `v7_worker` schema exists and documented
- [ ] 8 tables created: `agent_identity`, `queue_message`, `task_claim`, `heartbeat`, `result_submission`, `dead_letter`, `stop_gate`, `cost_ledger`
- [ ] Table schemas match architecture doc
- [ ] Indexes created for query performance
- [ ] RLS policies enabled on all data tables
- [ ] Service-role full access policy present
- [ ] Worker member SELECT policy correct (uses `authorized_lanes`)
- [ ] Worker INSERT/UPDATE/DELETE policies check roles
- [ ] 3 core functions present: `claim_next_task`, `send_heartbeat`, `release_task_claim`
- [ ] Function signatures match documentation
- [ ] Function security: SECURITY DEFINER with `set search_path`
- [ ] Grants correct (authenticated/anon/service_role)
- [ ] Seeded 3 example agents (Qwen, Claude, Deterministic Validator)

Verify migration 20260716 defensive patches:
- [ ] Schema creation guards (`if not exists`)
- [ ] Exception handlers around RLS policy creation
- [ ] No blocking errors on preview branch

**Defect examples to catch:**
- Missing SECURITY DEFINER on functions
- RLS policies exposing service-role data
- Incorrect function parameter names
- Seeded agents missing authorized_lanes
- Missing grants to authenticated role
- Duplicate function definitions

### 3. Worker Runtime Definition
**File:** `02_ARCHITECTURE/MODEL_REGISTRY.yaml`

Verify:
- [ ] `claude_architecture_reviewer` config present
- [ ] Model ID from Anthropic official list
- [ ] Tool allowlist explicit: Read, Glob, Grep, Git diff, test execution, Supabase RPC
- [ ] `claude_implementation_worker` has Edit, Write, Bash, Git ops
- [ ] `qwen_build_worker` defined for shell execution
- [ ] `deterministic_validator` defined with SQL/schema checks
- [ ] Supabase auth method is `edge_function_rpc`, NOT service-role
- [ ] Heartbeat renewal interval ~300s (5 minutes)
- [ ] Visibility timeout 1800s (30 minutes)
- [ ] Max renewals documented

**Defect examples:**
- Hardcoded model name instead of registry
- Tool allowlist missing required tools
- Service-role key exposed in config
- No heartbeat renewal interval
- Visibility timeout shorter than renewal

### 4. Duplicate Migration Candidates
**Check:**
- [ ] List all `0007` migrations (multiple authors/dates?)
- [ ] Identify which is canonical
- [ ] Check for conflicting table/function definitions
- [ ] Verify one is superseded (archive or rename)
- [ ] Confirm migration numbering unique

### 5. SECURITY DEFINER Functions
**Check all functions for:**
- [ ] `security definer` keyword present
- [ ] `set search_path = public, v7_worker` (no wildcards)
- [ ] Function owner is `postgres` (not authenticated user)
- [ ] No raw SQL interpolation (parameterized only)
- [ ] Exception handlers on privilege checks
- [ ] Logging does not leak secrets

### 6. RLS Policy Audit
**For each table with RLS:**
- [ ] `enable row level security` executed
- [ ] At least one policy per table
- [ ] Service-role bypass policy present (for batch operations)
- [ ] Worker select policy uses `authorized_lanes`/`authorized_task_types`
- [ ] Worker insert/update check `has_product_role`
- [ ] No public policies on sensitive columns
- [ ] Policy grants correct roles (authenticated, service_role)

### 7. Context Compiler
**File:** Check if runtime packet compilation exists

Verify:
- [ ] Task details → runtime packet conversion documented
- [ ] Instruction templates for each worker type
- [ ] Tool permissions encoded in packet
- [ ] Cost estimate included
- [ ] Deadline included
- [ ] Repo scope (allowed paths, forbidden patterns)
- [ ] Secret masking in logs

**If missing:** Document as remediation task.

### 8. Queue Lifecycle
**Check pgmq wrapper functions:**
- [ ] `enqueue_task()` creates message + task_claim
- [ ] `claim_next_task()` sets visibility timeout + heartbeat
- [ ] `send_heartbeat()` renews both
- [ ] `release_task_claim()` releases on completion
- [ ] Dead-letter routing on max retries
- [ ] Message archival after validation
- [ ] Queue cleanup policy (retention)

### 9. Tests and Acceptance
**Check test directory:**
- [ ] Unit tests for RLS policies
- [ ] Integration test: claim → execute → submit flow
- [ ] Error classification tests
- [ ] Heartbeat renewal under load
- [ ] Visibility timeout recovery
- [ ] Dead-letter routing
- [ ] Cost limit enforcement

**If missing:** Create test task for implementation worker.

### 10. Rollback and V6.9 Preservation
**Verify:**
- [ ] V6.9 schema (`dcse_cp`) untouched
- [ ] No foreign keys FROM v7_worker TO dcse_cp
- [ ] Migration can be rolled back without data loss
- [ ] Downtime window acceptable (none if read-only first)

### 11. SC/SS Capability Representation
**Check:**
- [ ] SC (Systems Coordination) lane agents defined
- [ ] SS (Specialized Services) lane agents defined
- [ ] Both can claim appropriate tasks
- [ ] Cost tracking per lane

### 12. PS Firewall Compliance
**Verify:**
- [ ] No PS (Privacy-Sensitive) content in migrations
- [ ] No personally identifiable data in seed agents
- [ ] No sensitive URLs or credentials
- [ ] Queue messages don't expose family context

---

## Deliverables

### Part 1: Structured Findings
```json
{
  "review_type": "architecture_v7_comp_001",
  "timestamp": "2026-07-27T20:30:00Z",
  "reviewer": "AGENT-CLAUDE-REVIEWER-01@STAGING",
  "status": "complete",
  "findings": {
    "architecture": [
      { "category": "defect|gap|risk", "severity": "critical|high|medium|low", "finding": "...", "location": "file:line", "remediation": "..." }
    ],
    "schema": [ ... ],
    "security": [ ... ],
    "compliance": [ ... ]
  },
  "automatic_repairs_applied": [ ... ],
  "contradiction_register": [ ... ],
  "acceptance_scorecard": {
    "architecture_complete": true/false,
    "migrations_pass_preview": true/false,
    "functions_documented": true/false,
    "rls_correct": true/false,
    "tests_present": true/false,
    "security_approved": true/false,
    "v6_9_preserved": true/false,
    "ps_firewall_clean": true/false,
    "score": "X/100"
  },
  "repair_tasks_created": [ "TASK-ID", "TASK-ID", ... ],
  "level_0_decision": {
    "recommendation": "approve|conditional|reject",
    "reason": "...",
    "conditions": [ ... ],
    "requires_dcs_review": true/false
  }
}
```

### Part 2: Repair Task Package
For each defect that requires code changes:
```json
{
  "repair_task_id": "DCSE-V7-REPAIR-NNN",
  "finding_id": "F-123",
  "title": "Fix RLS policy array comparison",
  "description": "...",
  "affected_files": [ "supabase/migrations/..." ],
  "assigned_to_lane": "SC",
  "estimated_effort": "15 min",
  "acceptance_criteria": [ ... ]
}
```

### Part 3: Contradiction Register
Any conflicts between documentation, schema, and code.

### Part 4: Level 0 Decision Packet
For DCS promotion authority to accept/reject V7 deployment.

---

## Runtime Packet Compilation

When claimed, this task compiles to runtime packet:

```json
{
  "task_id": "DCSE-V7-COMP-001",
  "task_type": "architecture_review",
  "lane": "SYSTEM",
  "instruction": "[See above inspection scope]",
  "tools_allowed": ["read_file", "glob_search", "grep_search", "git_diff", "test_execution", "supabase_rpc"],
  "repo_scope": {
    "allowed_paths": [
      "02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md",
      "02_ARCHITECTURE/MODEL_REGISTRY.yaml",
      "supabase/migrations/20260728_*.sql",
      "supabase/migrations/20260716_*.sql",
      "workers/",
      "tests/"
    ],
    "forbidden_patterns": ["*.env", "credentials", "secrets"]
  },
  "deadline": "2026-07-27T23:00:00Z",
  "cost_estimate_usd": 2.50,
  "agent_id": "AGENT-CLAUDE-REVIEWER-01@STAGING"
}
```

---

## Evaluation

**Pass criteria:**
- ✅ All 12 scope items inspected
- ✅ Defects documented with location and severity
- ✅ Repair tasks created for implementation
- ✅ Acceptance scorecard complete
- ✅ Level 0 decision packet submitted
- ✅ No blocking security issues
- ✅ V6.9 preserved

**Conditional pass:**
- ⚠️ Medium-severity issues with clear remediation plan
- ⚠️ Tests to be added post-deployment

**Fail:**
- ❌ Critical security defect
- ❌ RLS bypass possible
- ❌ PS firewall violation
- ❌ V6.9 data at risk

---

## History

| Date | Event |
|------|-------|
| 2026-07-27 20:09 | Migration 20260728 passes Supabase Preview CI ✅ |
| 2026-07-27 20:10 | Claude Reviewer Worker deployed in Blueprint Mode |
| 2026-07-27 20:11 | DCSE V7 COMP 001 created and queued |
| TBD | Claude reviewer claims task |
| TBD | Findings submitted |
| TBD | Deterministic validator confirms |
| TBD | Qwen implements repairs |
| TBD | Level 0 decision to DCS |

