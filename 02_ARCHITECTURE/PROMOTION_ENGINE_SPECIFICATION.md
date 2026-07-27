# Promotion Engine Specification — DCSE V7 Phase F

**Status:** Phase F Design Complete  
**Version:** 1.0  
**Date:** 2026-07-27

---

## Overview

The Promotion Engine manages the lifecycle of artifacts from candidate state through production promotion to eventual deprecation. It:

1. **Tracks promotion states** through a deterministic state machine
2. **Enforces approval gates** at critical transitions
3. **Records every state change** with no silent promotions
4. **Manages rollback and deprecation** for lifecycle completion
5. **Produces audit trail** for compliance

**Philosophy:** Promotion is gradual, audited, and reversible. Every transition requires evidence.

---

## Promotion State Machine

```
Candidate
  ↓ (code review passed)
Reviewed
  ↓ (acceptance suite passed)
Validated
  ↓ (governance approval granted)
Approved
  ↓ (merged to main/production)
Promoted
  ↓ (phase-out period begins)
Deprecated
  ↓ (historical record)
Archived
```

### Side Paths

```
Candidate → Rejected (blocked)
Promoted → Superseded (replaced by newer version)
Any State → Rolled Back (reverted to previous state)
```

---

## State Definitions

### 1. Candidate
**Entry:** Artifact created or submitted for promotion  
**Exit Conditions:**
- Code review passed (automated + manual)
- All tests green
- No critical findings

**Actions:**
- Run automated checks
- Request code review
- Collect evidence

**Metadata:**
- created_at
- created_by
- initial_evidence

---

### 2. Reviewed
**Entry:** Code review approved  
**Exit Conditions:**
- Acceptance suite executed
- All category checks passed
- Confidence score > 0.80

**Actions:**
- Run full acceptance suite
- Generate acceptance receipt
- Flag for approval if needed

**Metadata:**
- reviewed_at
- reviewed_by (comma-separated reviewers)
- review_findings
- acceptance_receipt_id

---

### 3. Validated
**Entry:** Acceptance suite passed  
**Exit Conditions:**
- Governance approval obtained
- Approval gate resolved
- Escalations handled

**Actions:**
- Request governance approval
- Escalate to approval board if needed
- Route to decision makers

**Metadata:**
- validated_at
- validated_by
- acceptance_confidence
- validation_evidence_count

---

### 4. Approved
**Entry:** Governance approval granted  
**Exit Conditions:**
- Merge to main completed
- Deployment successful
- Smoke tests pass

**Actions:**
- Merge to main branch
- Trigger deployment pipeline
- Monitor initial health

**Metadata:**
- approved_at
- approved_by (role)
- approval_ticket_id
- merge_commit_hash

---

### 5. Promoted
**Entry:** Successfully deployed to production  
**Exit Conditions:**
- Deprecation period begins (if planned)
- Superseded by new version
- Monitoring complete (30 days)

**Actions:**
- Monitor metrics (error rate, latency)
- Alert on regressions
- Collect performance data
- Plan deprecation timeline

**Metadata:**
- promoted_at
- promoted_to_env (production)
- deployment_receipt_id
- health_metrics
- monitoring_end_at

---

### 6. Deprecated
**Entry:** Deprecation period begins  
**Exit Conditions:**
- Deprecation period complete (90 days)
- No active users
- Replacement available

**Actions:**
- Send deprecation notices
- Monitor usage
- Document replacement
- Plan archival date

**Metadata:**
- deprecated_at
- deprecated_by
- deprecation_notice_sent_at
- replacement_artifact_id
- deprecation_end_at

---

### 7. Archived
**Entry:** Deprecation period complete  
**Actions:**
- Store in archive
- Remove from active registries
- Keep audit trail

**Metadata:**
- archived_at
- archived_by
- archive_location
- historical_record_complete

---

### Rejection
**Entry:** At any pre-approval state (Candidate, Reviewed, Validated)  
**Exit:** Final (no further promotion)

**Reasons:**
- Critical security finding (STOP_GATE)
- Architectural decision (requires redesign)
- Policy violation
- Business decision

**Metadata:**
- rejected_at
- rejected_by
- rejection_reason
- remediation_path (if available)

---

### Rollback
**Entry:** From Approved or Promoted (emergency)  
**Exit:** Revert to previous promotion state

**Triggers:**
- Critical production issue
- Data loss
- Unauthorized access

**Metadata:**
- rolled_back_at
- rolled_back_by
- rollback_reason
- previous_state
- restore_procedure

---

## Transition Rules

### Automatic Transitions (No Manual Approval)

```
Candidate → Reviewed
  when: code_review_approved == true
        AND all_tests_passed == true
        AND critical_findings == 0
```

### Manual Approval Required (Stop Gates)

```
Reviewed → Validated
  when: acceptance_suite_passed == true
        AND confidence_score > 0.80
  requires: manual review (not automatic)

Validated → Approved
  requires: governance approval
  approvers: DCSE lane
  timeout: 120 minutes

Approved → Promoted
  when: merge_to_main_successful == true
        AND deployment_healthy == true
  requires: monitoring (3 hours)
```

### Blocking Conditions

```
Candidate → Rejected
  if: STOP_GATE finding exists
      OR critical vulnerability found
      OR architectural incompatibility detected

Reviewed → Rejected
  if: acceptance_suite has STOP_GATE
      OR confidence_score < 0.70

Validated → Rejected
  if: governance approval denied
      OR escalation unresolved > timeout
```

---

## Promotion Receipt

```json
{
  "promotion_id": "PRO-20260727-001",
  "artifact_id": "PKT-20260727-abc123",
  "created_at": "2026-07-27T21:00:00Z",
  "created_by": "system",
  "current_state": "Promoted",
  "previous_state": "Approved",
  "state_history": [
    {
      "state": "Candidate",
      "entered_at": "2026-07-27T20:00:00Z",
      "entered_by": "claude-reviewer",
      "evidence_count": 5
    },
    {
      "state": "Reviewed",
      "entered_at": "2026-07-27T20:15:00Z",
      "entered_by": "claude-reviewer",
      "reviewed_by": ["code-reviewer-1", "code-reviewer-2"],
      "evidence_count": 12
    }
  ],
  "transition_evidence": {
    "last_transition": {
      "from": "Approved",
      "to": "Promoted",
      "triggered_by": "deployment_successful",
      "at": "2026-07-27T21:00:00Z",
      "evidence": {
        "deployment_receipt_id": "DEP-123",
        "health_check_passed": true,
        "smoke_tests_passed": 15,
        "monitoring_started": true
      }
    }
  },
  "metadata": {
    "version": "1.0",
    "lane": "SC",
    "promotion_velocity_hours": 1.5,
    "blocking_issues": 0,
    "rejections": 0,
    "rollbacks": 0
  },
  "audit": {
    "total_transitions": 5,
    "total_duration_hours": 1.5,
    "approval_gates_passed": 2,
    "rejection_gates_triggered": 0
  }
}
```

---

## No Silent Promotion Rule

**Principle:** Every state change is logged with:
- timestamp (to the second)
- actor (user ID or system ID)
- trigger (what caused the transition)
- evidence (receipt IDs, metric values, etc.)
- justification (short reason)

**Implementation:**
```javascript
async transitionState(fromState, toState, trigger, evidence) {
  // 1. Validate transition is allowed
  if (!isValidTransition(fromState, toState)) {
    throw new Error(`Invalid transition: ${fromState} → ${toState}`);
  }

  // 2. Record old state
  const previousState = this.currentState;

  // 3. Change state
  this.currentState = toState;

  // 4. Record transition in audit log
  const transitionRecord = {
    timestamp: new Date().toISOString(),
    from: previousState,
    to: toState,
    trigger: trigger,
    evidence: evidence,
    actor: getCurrentActor(),
    recorded_at: new Date().toISOString()
  };

  this.stateHistory.push(transitionRecord);
  this.auditLog.push(transitionRecord);

  // 5. Emit event
  await this.emitPromotionEvent('state_changed', transitionRecord);

  return transitionRecord;
}
```

---

## Approval Gate Pattern

```
Validated → (GATE: governance approval) → Approved

Gate Configuration:
- gate_id: "APPROVAL-VALIDATED-TO-APPROVED"
- approvers: ["DCSE"]
- timeout_minutes: 120
- escalation_on_timeout: true
- escalate_to: "DCS"
```

When gate is triggered:
1. System sends approval request to approvers
2. Approvers have timeout_minutes to respond
3. If approved: transition proceeds
4. If rejected: artifact moves to Rejected state
5. If timeout: escalate to escalate_to lane

---

## Deprecation Timeline

```
Day 0 (Promoted → Deprecated)
  ├─ Send deprecation notice to all users
  ├─ Document replacement artifact
  └─ Set end_of_life date (typically 90 days)

Day 30
  ├─ First reminder notice
  ├─ Measure active usage
  └─ Monitor migration progress

Day 60
  ├─ Final reminder notice
  ├─ Identify holdouts
  └─ Offer migration support

Day 90 (Deprecated → Archived)
  ├─ Decommission active services
  ├─ Move to archive storage
  └─ Preserve audit trail
```

---

## Success Criteria (Phase F)

✅ State machine with 7 primary states + 3 side paths  
✅ Automatic transitions (Candidate → Reviewed)  
✅ Approval gates (manual review required)  
✅ Blocking conditions (STOP_GATE, rejection)  
✅ No silent promotion (audit trail on every transition)  
✅ Rollback capability with previous state tracking  
✅ Deprecation timeline management  
✅ Promotion receipt with full history  
✅ Transition evidence collection  
✅ Integration with Phases A-E  

---

## Integration Points

**Upstream (Phases A-E):**
- Phase A (Runtime): Provides packet evidence
- Phase B (Rules): Provides rule execution receipt
- Phase C (Skills): Provides skill availability
- Phase D (Workflow): Provides workflow validation
- Phase E (Acceptance): Provides acceptance receipt

**Downstream:**
- Phase G (Opportunities): Signals high-confidence artifacts
- Phase K (Completion): Part of promotion → deploy → monitor cycle

---

## Files Produced (Phase F)

- `PROMOTION_ENGINE_SPECIFICATION.md` (this file)
- `promotion_engine_schema.json` (JSON Schema)
- `promotion-engine.js` (implementation)
