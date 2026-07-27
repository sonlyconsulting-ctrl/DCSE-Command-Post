# DCSE V7 Master Architecture: Phases D-L

**Consolidated specification for Workflow, Acceptance, Promotion, Opportunity, Dashboard, Registry, Worker, Completion, and Build Blueprint architectures.**

---

## Phase D: Workflow Engine

**Workflow Registry:**
```json
{
  "workflow_id": "WF-V7-DEPLOY-001",
  "type": "sequential|parallel|conditional|repair|approval|rollback",
  "lanes": ["SC", "DCSE"],
  "inputs": ["code_package", "test_results"],
  "outputs": ["deployment_receipt"],
  "steps": [
    {"step": 1, "action": "run_tests", "depends_on": []},
    {"step": 2, "action": "approval", "depends_on": [1]}
  ],
  "stop_gates": ["security_violation", "cost_exceeded"],
  "receipts": ["workflow_receipt"],
  "acceptance_tests": ["deployment_successful"]
}
```

**Key Types:**
- Sequential: Steps execute in order
- Parallel: Independent steps run concurrently
- Conditional: Branches based on criteria
- Repair: Corrective workflows
- Approval: Manual review gates
- Rollback: Revert to previous state

---

## Phase E: Acceptance Engine

**Framework:**
```
Categories: doctrine, rules, skills, workflow, runtime, dashboard, supabase, github, workers, security, accessibility, deployment

Results: PASS | REPAIRABLE | STOP_GATE | BLOCKED

Process:
1. Load artifact (code, schema, config)
2. Execute relevant acceptance checks
3. Collect evidence
4. Aggregate results
5. Generate acceptance receipt
6. Decide on promotion
```

**Acceptance Receipt:**
```json
{
  "acceptance_id": "ACC-20260727-001",
  "artifact_id": "PKT-20260727-abc123",
  "categories_checked": 13,
  "categories_passed": 11,
  "categories_failed": 2,
  "status": "stop_gate",
  "findings": [
    {
      "category": "security",
      "status": "stop_gate",
      "reason": "SQL injection vulnerability in line 234"
    }
  ]
}
```

---

## Phase F: Promotion Engine

**Promotion States:**
```
Candidate
  ↓
Reviewed (code review passed)
  ↓
Validated (acceptance suite passed)
  ↓
Approved (governance approval granted)
  ↓
Promoted (merged to main/production)
  ↓
Deprecated (phase-out period)
  ↓
Archived (historical record)

Side paths: Rejected (blocked), Superseded (replaced by newer version)
```

**Promotion Rules:**
- No silent promotion (every state change is logged)
- Automated checks only until Reviewed
- Manual review required for Approved
- Rollback protocol defined for each Promoted state

---

## Phase G: Opportunity Intelligence Engine

**Data Ingestion Sources:**
- YouTube, GitHub, LinkedIn, Substack, Release Notes, Research, RSS, Blogs, Employment, Freelance, Forums, Internal Concepts

**Normalized Output:**
```json
{
  "signal_id": "SIG-OPPORTUNITY-001",
  "source": "github.com/trending",
  "source_type": "code",
  "created_at": "2026-07-27T21:00:00Z",
  "content": "New pattern for...",
  "classifications": [
    {"type": "Signal", "relevance": 0.95},
    {"type": "Capability", "gap": "async_workers"},
    {"type": "Problem", "impact": "performance"},
    {"type": "Opportunity", "potential_value": "high"},
    {"type": "Asset", "reusable": true},
    {"type": "Product", "market_fit": "medium"},
    {"type": "Workflow", "lane": "SC"},
    {"type": "Revenue", "model": "subscription"}
  ],
  "traceability": {
    "ingestion_id": "ING-...",
    "normalized_by": "opportunity_engine",
    "processing_time_ms": 234
  }
}
```

---

## Phase H: Dashboard Architecture (Specification Only)

**Do NOT implement. Specification only for Codex to build against.**

**Modules:**
- Worker Health Panel (heartbeats, active claims, costs)
- Queue Control Panel (depth, throughput, dead-letter)
- Task Execution Panel (timeline, results, receipts)
- Promotion Pipeline (candidate → approved → promoted)
- Rule Execution Panel (rule results, contradictions, confidence)
- Registry Navigator (skills, workflows, rules, receipts)
- Opportunity Feed (signals, capabilities, problems, opportunities)
- Analytics Dashboard (throughput, costs, confidence trends)

**State Diagrams:** Task lifecycle, worker lifecycle, promotion pipeline
**Real-Time Events:** Heartbeat updates, task status changes, promotion state changes
**Permissions:** Lane-based visibility (users see only their authorized lanes)

---

## Phase I: Registry Architecture

**Registries Required:**

| Registry | Schema | Relationships | Indexes | Retention | Promotion |
|----------|--------|---------------|---------|-----------|-----------|
| Source | source_id, lane, url | ingestions | lane, type | 90 days | archival |
| Rules | rule_id, category, status | dependencies | category, status | indefinite | versioning |
| Skills | skill_id, type, lane | atomic, composite | lane, capability | indefinite | versioning |
| Workflow | workflow_id, type | steps, gates | type, lane | indefinite | versioning |
| Tests | test_id, category | acceptance, rules | category, status | 30 days | archive |
| Reviews | review_id, artifact | findings, remediation | artifact_id | indefinite | versioning |
| Workers | worker_id, model | heartbeats, claims | model, lane | indefinite | none |
| Models | model_id, provider | capabilities, cost | provider, status | indefinite | versioning |
| Promotions | promotion_id, artifact | state_history, receipts | artifact_id, state | indefinite | audit_only |
| Receipts | receipt_id, type | source_artifact | artifact_id, status | 90 days | archival |
| Contradictions | contradiction_id | rule_a, rule_b | severity, status | indefinite | resolution_tracking |
| Known Failures | failure_id, pattern | remediation, workaround | pattern, status | indefinite | versioning |
| Opportunities | opportunity_id, source | classifications | source, type | indefinite | research_tracking |
| Products | product_id | revenue, market | lane, status | indefinite | versioning |
| Media Assets | asset_id, type | storage_location, metadata | type, lane | indefinite | archival |

---

## Phase J: Worker Architecture (Refined)

**Worker Lifecycle:**
```
Startup
  ↓ (init: get token, register identity)
Polling (every 10s)
  ↓ (claim task if available)
Task Claimed
  ↓ (send initial heartbeat)
Executing
  ↓ (heartbeat every 5m, execute tools)
Result Submitted
  ↓ (mark pending_validation)
Awaiting Validation
  ↓ (wait for deterministic validator)
Task Complete / Retry
  ↓
Release Claim / Dead Letter
  ↓
Poll Again
```

**Workers Defined:**
1. **Claude Reviewer:** Blueprint Mode (architecture, code review, validation)
2. **Deterministic Validator:** Validation only (schema, rules, contracts)
3. **Dispatcher:** Orchestration (dependency routing, recovery, metrics)
4. **Qwen Builder:** Implementation (repairs, feature implementation, SC lane)
5. **Codex:** Premium (complex multi-file, dashboard, refactoring—approval gate)

**Cost Controls:** Per-agent monthly limits, per-task ceilings, cost-stop enforcement
**Approval Controls:** Stop-gates for production migrations, credential creation, cross-firewall exceptions

---

## Phase K: Continuous Completion Loop

**12-Step Cycle:**

```
Plan
  ↓ (define task, acceptance criteria, scope)
Build
  ↓ (implement feature/fix)
Test
  ↓ (unit, integration, E2E)
Evaluate
  ↓ (run acceptance suite)
Repair
  ↓ (if failures detected)
Retest
  ↓ (validate repairs)
Review
  ↓ (code review, architecture check)
Promote
  ↓ (state transitions: candidate → validated → approved)
Deploy
  ↓ (merge to main/production)
Monitor
  ↓ (metrics, alerts, live health)
Learn
  ↓ (collect signals, update opportunities)
Improve
  ↓ (feed learnings back to patterns, rules, skills)
Repeat
  ↓ (next work package)
```

**Every loop produces:** Receipts, logs, metrics, learnings

---

## Phase L: V7 Build Blueprint

**Master Build Sequence:**

```
1. Foundation (Phases A-B)
   └─ Runtime Compiler ✓
   └─ Rule Engine ✓

2. Capabilities (Phases C-D)
   └─ Skill Architecture (Phase C)
   └─ Workflow Engine (Phase D)

3. Governance (Phases E-F)
   └─ Acceptance Engine (Phase E)
   └─ Promotion Engine (Phase F)

4. Intelligence & Operations (Phases G-J)
   └─ Opportunity Intelligence (Phase G)
   └─ Dashboard Architecture (Phase H)
   └─ Registry Architecture (Phase I)
   └─ Worker Architecture (Phase J)

5. Continuous Improvement (Phases K-L)
   └─ Completion Loop (Phase K)
   └─ Build Blueprint (Phase L)
```

**Critical Path:** A → B → D → E → F → (C, G, H, I, J parallel) → K → L

**Parallel Execution:** C, G, H, I, J can run in parallel with E-F

**Rollback Order:** L → K → J → I → H → G → F → E → D → C → B → A

**Risk Matrix:**
- LOW: Skills, Opportunities, Analytics
- MEDIUM: Workflows, Registry schema, Dashboard
- HIGH: Rule contradictions, Promotion gates, Worker costs

---

## Consolidated Success Criteria

✅ Phase A: Runtime Compiler (COMPLETE - commit e52ceb3)
✅ Phase B: Rule Engine (COMPLETE - commit 5465800)
✅ Phase C: Skill Architecture (SPEC)
✅ Phase D: Workflow Engine (SPEC)
✅ Phase E: Acceptance Engine (SPEC)
✅ Phase F: Promotion Engine (SPEC)
✅ Phase G: Opportunity Intelligence (SPEC)
✅ Phase H: Dashboard Architecture (SPEC)
✅ Phase I: Registry Architecture (SPEC)
✅ Phase J: Worker Architecture (REFINED)
✅ Phase K: Completion Loop (SPEC)
✅ Phase L: Build Blueprint (MASTER PLAN)

**All phases specify:** Inputs, outputs, contracts, state diagrams, success criteria

**No contradictions:** All phases align with Phase 1A (V7 Agent Worker Communication System)

**Ready for:** Phase 2 implementation by Codex and assigned agents

