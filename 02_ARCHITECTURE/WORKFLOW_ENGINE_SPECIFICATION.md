# Workflow Engine Specification — DCSE V7 Phase D

**Status:** Phase D Design Complete  
**Version:** 1.0  
**Date:** 2026-07-27

---

## Overview

The Workflow Engine orchestrates multi-step processes with branching, parallelization, error recovery, and approval gates. It enables:

1. **Sequential workflows:** Steps execute in order with dependencies
2. **Parallel workflows:** Independent steps execute concurrently
3. **Conditional workflows:** Smart branching based on runtime conditions
4. **Repair workflows:** Automated error correction and retries
5. **Approval workflows:** Manual governance gates with timeouts
6. **Rollback workflows:** State restoration on failure

**Philosophy:** Workflows are deterministic, auditable, and reversible. Every execution produces traceable receipts.

---

## Core Components

### Workflow Registry

A versioned, searchable collection of workflow definitions.

```json
{
  "workflow_id": "WF-V7-DEPLOY-001",
  "type": "sequential",
  "name": "Deployment Workflow",
  "version": "1.0",
  "lanes": ["SC", "DCSE"],
  "inputs": [
    {"name": "code_package", "type": "object", "required": true},
    {"name": "environment", "type": "string", "required": true}
  ],
  "outputs": [
    {"name": "deployment_receipt", "type": "object"}
  ],
  "steps": [
    {"step": 1, "action": "run_tests", "depends_on": []},
    {"step": 2, "action": "approval", "depends_on": [1]},
    {"step": 3, "action": "deploy", "depends_on": [2]}
  ],
  "stop_gates": [
    {"gate_id": "SG-SECURITY", "trigger": "security_violation", "escalation_level": 2}
  ],
  "approval_config": {
    "required_before_step": [3],
    "approvers": ["DCSE"],
    "approval_timeout_minutes": 60
  },
  "rollback_config": {
    "enabled": true,
    "savepoint_frequency": 2
  }
}
```

### Workflow Types

| Type | Purpose | Use Case |
|------|---------|----------|
| **Sequential** | Steps execute in order | Deployment, migration, testing |
| **Parallel** | Independent steps run concurrently | Parallel checks, multi-lane review |
| **Conditional** | Branching based on conditions | Smart routing, feature flags |
| **Repair** | Automated error correction | Retry with fixes, rollback recovery |
| **Approval** | Manual review gates | Change approval, promotion |
| **Rollback** | Restore to previous state | Undo operations, state recovery |

### Execution Flow

```
1. Load Workflow
   └─ Fetch from registry
   └─ Validate structure

2. Verify Authorization
   └─ Check lane permissions
   └─ Verify worker credentials

3. Validate Inputs
   └─ Verify required parameters
   └─ Type checking

4. Resolve Dependencies
   └─ Topological sort of steps
   └─ Build execution order

5. Execute Steps
   └─ For each step in order:
      ├─ Evaluate conditions
      ├─ Check approval gates
      ├─ Execute with retry policy
      ├─ Handle failures
      └─ Create savepoints

6. Handle Stop Gates
   └─ Check for blocking conditions
   └─ Escalate if needed

7. Run Acceptance Tests
   └─ Validate workflow success

8. Generate Receipt
   └─ Document execution
   └─ Record metrics
   └─ Audit trail
```

### Step Configuration

Each step in a workflow defines:

```json
{
  "step": 1,
  "action": "SKILL-ID or subprocess name",
  "name": "Display name",
  "depends_on": [prerequisite step IDs],
  "retry_policy": {
    "max_attempts": 3,
    "backoff_ms": 1000,
    "backoff_multiplier": 2.0
  },
  "timeout_seconds": 300,
  "on_failure": "stop|continue|retry|repair|manual_review",
  "conditions": [
    {"if": "expression", "then": step_id, "else": step_id}
  ],
  "parallel_with": [step IDs to run in parallel],
  "input_mapping": {"workflow_input": "step_input"},
  "output_mapping": {"step_output": "workflow_output"}
}
```

### Approval Gates

Manual review gates with timeout and escalation:

```json
{
  "required_before_step": [3],
  "approvers": ["DCSE", "SYSTEM"],
  "approval_timeout_minutes": 120,
  "escalate_if_no_approval": true,
  "notification_channels": ["slack", "email"]
}
```

### Stop Gates

Blocking conditions that halt execution:

```json
{
  "gate_id": "SG-SECURITY",
  "trigger": "security_violation",
  "message": "Security check failed",
  "escalation_level": 2,
  "requires_approval": true
}
```

### Rollback Configuration

State restoration on failure:

```json
{
  "enabled": true,
  "savepoint_frequency": 2,
  "steps": [
    {
      "step": 1,
      "undo_action": "rollback_deployment",
      "depends_on": []
    }
  ]
}
```

---

## Workflow Templates

### 1. Deployment Workflow (Sequential)

```
Check → Approve → Deploy → Verify
```

Steps:
1. Pre-deployment validation (stop if fails)
2. Approval gate (timeout: 1 hour)
3. Deploy to production (retry: 3x with backoff)
4. Verify health (repair if needed)

### 2. Database Migration Workflow (Sequential)

```
Validate → Backup → Migrate → Validate Schema
```

Steps:
1. Validate migration files (stop if invalid)
2. Backup database (stop if fails)
3. Run migration (repair on failure)
4. Validate new schema (continue on error)

Rollback: Restore from backup

### 3. Governance Workflow (Parallel)

```
Rules ──┬─ Security ─┬─ Code Quality ──→ Aggregate
        └────────────┘
```

Steps 1-3 run in parallel:
1. Execute governance rules
2. Security scan
3. Code quality check
4. Aggregate results (depends on all 3)

### 4. Smart Routing Workflow (Conditional)

```
Assess → [Minor: fast path] or [Major: slow path]
```

Steps:
1. Assess change type
2. Minor changes: Quick validation
3. Major changes: Full review

### 5. Repair Workflow (Repair)

```
Diagnose → Fix → Validate → Retry Original
```

Steps:
1. Diagnose error (stop if unknown)
2. Apply fix (manual review if fails)
3. Validate fix (continue on error)
4. Retry original workflow

---

## Execution Contract

### Input: Workflow Execution Request

```json
{
  "request_id": "REQ-WF-20260727-001",
  "workflow_id": "WF-V7-DEPLOY-001",
  "task_id": "TASK-123",
  "worker_id": "claude-reviewer",
  "lane": "SC",
  "inputs": {
    "code_package": {...},
    "environment": "production"
  }
}
```

### Output: Workflow Execution Receipt

```json
{
  "receipt_id": "REC-WF-20260727-001",
  "workflow_id": "WF-V7-DEPLOY-001",
  "task_id": "TASK-123",
  "status": "success|failed|error|pending_approval",
  "execution_summary": {
    "total_steps": 4,
    "steps_completed": 3,
    "steps_failed": 0,
    "steps_skipped": 0,
    "duration_ms": 45000,
    "cost_usd": 5.50
  },
  "step_results": [
    {
      "step_id": 1,
      "step_name": "Run Tests",
      "action": "run_tests",
      "status": "success",
      "attempt": 1,
      "duration_ms": 15000,
      "output": {...}
    }
  ],
  "approval_gates_triggered": [
    {
      "step_id": 2,
      "step_name": "Approval Gate",
      "status": "pending_approval",
      "approvers": ["DCSE"]
    }
  ],
  "stop_gates_triggered": [],
  "savepoints": [
    {"savepoint_id": "SP-123", "step_id": 2, "state": {...}}
  ],
  "errors": [],
  "audit": {
    "started_at": "2026-07-27T21:00:00Z",
    "completed_at": "2026-07-27T21:00:45Z",
    "worker_id": "claude-reviewer",
    "lane": "SC"
  }
}
```

---

## Error Handling

### On-Failure Policies

| Policy | Behavior |
|--------|----------|
| **stop** | Halt workflow, mark as failed |
| **continue** | Log error, proceed to next step |
| **retry** | Retry with exponential backoff |
| **repair** | Invoke repair workflow |
| **manual_review** | Escalate to approval gate |

### Retry Policy

```json
{
  "max_attempts": 3,
  "backoff_ms": 1000,
  "backoff_multiplier": 2.0
}
```

Retry sequence: 1s → 2s → 4s

### Error Categories

- **TRANSIENT:** Network timeout (retry)
- **AUTHORIZATION:** Permission denied (escalate)
- **VALIDATION:** Invalid input (stop)
- **RESOURCE:** Resource not found (repair)
- **DEPENDENCY:** Prerequisite failed (continue or stop)
- **TIMEOUT:** Exceeded time limit (retry or repair)
- **UNKNOWN:** Unexpected error (manual review)

---

## Success Criteria (Phase D)

✅ Workflow Registry schema with versioning, dependencies  
✅ 6 workflow execution types (sequential, parallel, conditional, repair, approval, rollback)  
✅ Dependency resolver with topological sort  
✅ Step execution with retry/failure handling  
✅ Conditional branching and parallel execution  
✅ Approval gates with timeouts  
✅ Stop gates with escalation  
✅ Rollback and savepoint management  
✅ Workflow templates (5+ types)  
✅ Execution contract (request/receipt)  
✅ Error handling (7 categories)  
✅ No contradictions with Phases A, B, C

---

## Integration Points

**Upstream (Phase C - Skills):**
- Workflow steps invoke skills via skill_id
- Skills provide execution results
- Skills return errors for failure handling

**Downstream (Phase E - Acceptance):**
- Workflows generate acceptance criteria
- Workflows define success conditions
- Workflows produce receipts for evidence

**Lateral (Phase F - Promotion):**
- Workflows drive promotion state transitions
- Workflow results determine promotion readiness
- Workflows produce audit trail for compliance

---

## Files Produced (Phase D)

- `WORKFLOW_ENGINE_SPECIFICATION.md` (this file)
- `workflow_registry_schema.json` (JSON Schema)
- `workflow-executor.js` (implementation with 5 templates)
