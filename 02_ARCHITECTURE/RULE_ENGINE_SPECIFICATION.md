# Rule Engine Specification — DCSE V7 Phase B

**Status:** Phase B Design Complete  
**Version:** 1.0  
**Date:** 2026-07-27

---

## Overview

The Rule Engine is the deterministic decision-making system for DCSE V7. It:

1. **Compiles** doctrine rules into executable form
2. **Validates** rule syntax, dependencies, and completeness
3. **Detects** contradictions and circular dependencies
4. **Calculates** confidence scores and materiality
5. **Executes** rules against code/schema/workflow artifacts
6. **Generates** decision packets with justification

**Philosophy:** Rules are *applied*, not *interpreted*. Every decision is deterministic, traceable, and justified.

---

## Core Concepts

### Rule Registry

A searchable, versioned collection of all doctrine rules.

```json
{
  "rule_id": "RULE-V7-001-ARCHITECTURE-COMPLETENESS",
  "version": "1.0",
  "category": "architecture",
  "priority": 1,
  "status": "active",
  "created_at": "2026-01-01T00:00:00Z",
  "created_by": "architecture_team",
  "name": "Architecture Must Be Complete and Documented",
  "description": "All major system components must have documented architecture",
  "scope": ["02_ARCHITECTURE/**"],
  "triggers_on": ["commit", "pr_open", "manual_review"],
  "rule_definition": {
    "type": "file_presence",
    "files_required": ["V7_AGENT_WORKER_ARCHITECTURE.md"],
    "min_lines": 500
  },
  "acceptance": {
    "pass": "All architecture files present and well-documented",
    "fail": "Missing architecture documentation"
  },
  "contradictions": [],
  "dependencies": ["RULE-V7-002-MIGRATION-TESTING"],
  "materiality": {
    "scope": "ALL",
    "severity": "HIGH",
    "blocks_promotion": true
  }
}
```

### Doctrine Compiler

Transforms written doctrine statements into executable rules.

**Input:** Markdown/YAML with governance statements
```markdown
# Architecture Completeness

Every system must document its:
- Design decisions
- Data flow
- Security model
- Deployment model
```

**Output:** Executable rule registry entries with:
- Objective criteria (checkable)
- Automated or manual verification
- Contradiction detection
- Materiality classification

### Rule Validator

Checks rule syntax, completeness, and dependency graph.

```
Checks:
✓ Rule format valid
✓ Trigger conditions defined
✓ Acceptance criteria clear
✓ Dependencies resolvable
✓ No circular dependencies
✓ Contradictions detected
✓ Scope non-overlapping (or intentional)
✓ Materiality classification present
```

### Contradiction Detector

Finds rules that conflict with each other.

**Example Contradiction:**
```
RULE-A: "All production changes require approval"
RULE-B: "Manual changes to production forbidden"
→ CONTRADICTION: Can't require approval AND forbid it
```

**Detection Algorithm:**
1. Parse each rule's acceptance criteria
2. Build conflict matrix (rule A conflicts with rule B?)
3. For each pair, check if acceptance_conditions conflict
4. Report contradictions with severity (HIGH/MEDIUM/LOW)
5. Suggest resolution (merge, clarify, override)

### Confidence Model

Calculates how confident we should be that a rule is satisfied.

**Factors:**
- **Automation**: Automated checks = higher confidence (99%)
- **Coverage**: How much of the artifact is checked? (0-100%)
- **Recency**: When was rule last validated? (fresh = high)
- **Observer Effect**: Multiple independent checkers = higher

**Formula:**
```
confidence = (automation_score × 0.4) 
           + (coverage_score × 0.3) 
           + (recency_score × 0.2) 
           + (observer_score × 0.1)

automation_score = 0.99 (automated) or 0.70 (manual)
coverage_score = files_checked / files_in_scope
recency_score = 1 - min(days_since_check / 30, 1.0)
observer_score = 1 if independent_verification else 0
```

### Materiality Engine

Classifies rules by impact and blocks promotion if unmet.

**Materiality Levels:**

| Level | Scope | Blocks Promotion? | Example |
|-------|-------|-------------------|---------|
| CRITICAL | FULL_PRODUCT | YES | Security vulnerability |
| HIGH | LANE_DEPENDENT | YES (for that lane) | Missing required documentation |
| MEDIUM | COMPONENT | CONDITIONAL | Code style violation |
| LOW | OPTIONAL | NO | Enhancement opportunity |

**Blocking Rules:**
```
MATERIALITY_HIGH + status=fail → STOP PROMOTION
MATERIALITY_CRITICAL + status=fail → ESCALATE TO APPROVAL GATE
MATERIALITY_LOW + status=fail → CONTINUE (with warning)
```

---

## Rule Execution Flow

```
1. Load Rules
   └─ Query rule registry
   └─ Filter by scope/trigger
   └─ Validate rule format

2. Prepare Evidence
   └─ Read artifact (code, schema, config)
   └─ Extract metadata
   └─ Calculate checksums

3. Check Dependencies
   └─ Verify prerequisites are met
   └─ Build execution order
   └─ Detect circular dependencies

4. Execute Rules (in order)
   └─ Apply rule logic to evidence
   └─ Collect findings
   └─ Calculate confidence score

5. Detect Contradictions
   └─ Check for conflicting findings
   └─ Flag for manual review if needed
   └─ Suggest resolutions

6. Generate Decision
   └─ Aggregate results
   └─ Calculate confidence
   └─ Classify materiality
   └─ Create decision packet

7. Output Receipt
   └─ Rule execution receipt
   └─ Decision summary
   └─ Promotion readiness
```

---

## Rule Categories

### Architecture Rules
- System design documented
- Layer boundaries defined
- Security model specified
- Deployment model clear
- Version compatibility

### Migration Rules
- Schema changes documented
- Backward compatibility maintained
- Rollback procedure defined
- No irreversible operations on production data
- Testing requirements met

### Security Rules
- No secrets in code
- Encryption in transit/at rest
- Access control defined
- Audit logging enabled
- Vulnerability scanning passed

### Compliance Rules
- GDPR: Data deletion, consent, privacy
- SOC 2: Logging, monitoring, access
- PS Firewall: Product content isolated
- Performance: Latency/throughput targets

### Testing Rules
- Unit tests for all functions
- Integration tests for critical paths
- E2E tests for user workflows
- Coverage threshold (80%+)
- No flaky tests

### Documentation Rules
- API documented (OpenAPI)
- Architecture documented
- Deployment documented
- Runbooks for operations
- Change logs maintained

---

## Execution Contract

### Input: Rule Execution Request
```json
{
  "request_id": "REQ-RULE-20260727-001",
  "artifact_type": "schema|code|workflow|config",
  "artifact_path": "supabase/migrations/20260728_*.sql",
  "rules_to_apply": ["RULE-V7-001", "RULE-V7-002"],
  "scope": "lane|component|full_product",
  "trigger": "commit|pr_open|manual_review",
  "user_context": {"user_id": "...", "role": "..."}
}
```

### Output: Rule Execution Receipt
```json
{
  "receipt_id": "REC-RULE-20260727-001",
  "request_id": "REQ-RULE-20260727-001",
  "status": "pass|fail|stop_gate|needs_review",
  "execution_summary": {
    "rules_executed": 10,
    "rules_passed": 9,
    "rules_failed": 1,
    "rules_inconclusive": 0,
    "confidence_score": 0.92
  },
  "results": [
    {
      "rule_id": "RULE-V7-001",
      "status": "pass",
      "confidence": 0.99,
      "evidence": "Architecture doc found: V7_AGENT_WORKER_ARCHITECTURE.md (1474 lines)",
      "materiality": "HIGH"
    },
    {
      "rule_id": "RULE-V7-003",
      "status": "fail",
      "confidence": 0.95,
      "finding": "SQL injection vulnerability detected in line 234",
      "remediation": "Use parameterized queries",
      "materiality": "CRITICAL"
    }
  ],
  "contradictions": [],
  "promotion_ready": false,
  "blocking_reasons": [
    "RULE-V7-003: CRITICAL security finding"
  ]
}
```

---

## Success Criteria (Phase B)

✅ Rule Registry schema defined (with versioning, dependencies)  
✅ Doctrine Compiler specification (Markdown → Rule)  
✅ Rule Validator with 8-point checklist  
✅ Contradiction Detector with conflict matrix  
✅ Confidence Model with 4-factor formula  
✅ Materiality Engine with blocking logic  
✅ Rule Execution Flow documented (7 steps)  
✅ 6 rule categories specified with examples  
✅ Execution contract (input/output) defined  
✅ No contradictions with Phase A or Phase 1A

---

## Implementation Order (Phase B)

1. Rule Registry + Schema
2. Rule Validator
3. Contradiction Detector
4. Confidence Model
5. Materiality Engine
6. Rule Executor
7. Doctrine Compiler

---

## Files Produced (Phase B)

- `RULE_ENGINE_SPECIFICATION.md` (this file)
- `rule_registry_schema.json` (next)
- `rule-executor.js` (implementation)
- `doctrine-compiler.js` (doctrine → rules)
- `contradiction-detector.js` (conflict analysis)
