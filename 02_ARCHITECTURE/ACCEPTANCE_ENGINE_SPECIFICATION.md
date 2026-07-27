# Acceptance Engine Specification — DCSE V7 Phase E

**Status:** Phase E Design Complete  
**Version:** 1.0  
**Date:** 2026-07-27

---

## Overview

The Acceptance Engine validates that artifacts meet all governance requirements before promotion. It:

1. **Loads artifact** (code, schema, config, workflow)
2. **Executes acceptance checks** across 13 categories
3. **Collects evidence** from all checks
4. **Aggregates results** into pass/fail/repairable/blocked
5. **Generates acceptance receipt** with findings
6. **Decides promotion readiness** based on materiality

**Philosophy:** Acceptance is deterministic, multi-category, and evidence-driven. Every decision is justified.

---

## Acceptance Categories

| # | Category | Purpose | Checks | Evidence |
|----|----------|---------|--------|----------|
| 1 | **Doctrine** | Philosophical alignment | Values, principles, ethics | Design docs, commitments |
| 2 | **Rules** | Governance rules | Rule engine execution | Rule receipts, contradictions |
| 3 | **Skills** | Capability readiness | Skill availability, versioning | Skill registry, tests |
| 4 | **Workflow** | Process definition | Workflow structure, gates | Workflow registry, acceptance_tests |
| 5 | **Runtime** | Execution readiness | Packet compilation, hashing | Runtime receipts, metrics |
| 6 | **Dashboard** | UI/UX completeness | Panels, navigation, responsiveness | Screenshots, E2E tests |
| 7 | **Supabase** | Database readiness | Schema, RLS, migrations | Migration logs, audit |
| 8 | **GitHub** | Repository health | Commits, branches, PRs | Git history, CI logs |
| 9 | **Workers** | Worker availability | Model registration, health | Worker heartbeats, costs |
| 10 | **Security** | Threat model | Secrets, encryption, access | Scan reports, audit logs |
| 11 | **Accessibility** | WCAG compliance | A11y scans, keyboard nav | Audit reports, testing |
| 12 | **Deployment** | Production readiness | Health checks, metrics | Deployment logs, alerts |
| 13 | **Compliance** | Regulatory | GDPR, SOC 2, Data handling | Audit trail, consent logs |

---

## Acceptance Result States

```
PASS           → Artifact meets all acceptance criteria
                 All checks passed, no waived rules

REPAIRABLE     → Artifact has fixable issues
                 Apply repairs, retest, re-submit

STOP_GATE      → Critical findings block promotion
                 Requires architectural change, not quick fix

BLOCKED        → Artifact cannot proceed
                 Manual intervention required, escalation needed
```

---

## Acceptance Process

### 1. Load Artifact

Load and analyze the artifact to be accepted:
- Read source files (code, schema, config)
- Extract metadata (version, author, created_at)
- Calculate hashes (SHA256, ed25519)
- Check previous receipts (cache)

### 2. Execute Category Checks

For each of 13 categories:
- Load category acceptance rules
- Run automated checks
- Flag manual review items
- Collect evidence

### 3. Collect Evidence

Evidence forms include:
- **File evidence:** Lists of files, LOC, complexity
- **Metric evidence:** Coverage %, latency, cost
- **Audit evidence:** Logs, access patterns, changes
- **Scan evidence:** Security scans, WCAG, linting
- **Test evidence:** Test results, code quality
- **Receipt evidence:** Prior approvals, receipts

### 4. Aggregate Results

Combine findings across categories:
- Count passes, failures, inconclusive
- Detect contradictions
- Calculate confidence score
- Classify materiality

### 5. Generate Receipt

Create acceptance receipt with:
- Category results
- Blocking findings
- Evidence summary
- Remediation suggestions
- Promotion readiness

### 6. Decide Promotion

```
if all_categories_passed:
  promotion_ready = true
else if stop_gate_findings > 0:
  promotion_ready = false
  status = "STOP_GATE"
  escalation_level = 2
else if repairable_findings > 0:
  promotion_ready = false
  status = "REPAIRABLE"
  escalation_level = 1
else:
  promotion_ready = false
  status = "BLOCKED"
  escalation_level = 2
```

---

## Acceptance Rules

Each category has rules:

```json
{
  "rule_id": "ACC-DOCTRINE-001",
  "category": "doctrine",
  "name": "Ethical Principles",
  "description": "Artifact aligns with ethical principles",
  "check_type": "manual|automated|hybrid",
  "acceptance_criteria": [
    "No exploitation of vulnerable users",
    "Transparent about limitations",
    "Respects user autonomy"
  ],
  "materiality": {
    "severity": "CRITICAL|HIGH|MEDIUM|LOW",
    "blocks_promotion": true,
    "requires_approval": true,
    "escalation_level": 0|1|2
  },
  "evidence_sources": [
    "design_doc",
    "code_review",
    "user_feedback"
  ],
  "remediation": {
    "automated_fix_available": false,
    "manual_steps": ["Consult ethics review board", "..."],
    "doc_link": "https://..."
  }
}
```

---

## Acceptance Receipt

```json
{
  "acceptance_id": "ACC-20260727-001",
  "artifact_id": "PKT-20260727-abc123",
  "created_at": "2026-07-27T21:00:00Z",
  "created_by": "deterministic-validator",
  "task_id": "TASK-123",
  "lane": "SC",
  "categories_checked": 13,
  "categories_passed": 11,
  "categories_failed": 2,
  "categories_repairable": 0,
  "status": "STOP_GATE",
  "confidence_score": 0.87,
  "promotion_ready": false,
  "findings": [
    {
      "finding_id": "ACC-SEC-001",
      "category": "security",
      "severity": "CRITICAL",
      "status": "fail",
      "title": "Hardcoded Secret Found",
      "description": "AWS_KEY found in source code at line 234",
      "evidence": "File: src/config.js, line 234",
      "remediation": "Remove secret, rotate key, use env vars",
      "blocks_promotion": true
    },
    {
      "finding_id": "ACC-DEPLOY-001",
      "category": "deployment",
      "severity": "HIGH",
      "status": "repairable",
      "title": "Missing Health Check",
      "description": "Deployment lacks /health endpoint",
      "remediation": "Add /health endpoint returning {status: ok}",
      "blocks_promotion": false
    }
  ],
  "category_results": {
    "doctrine": {"status": "pass", "findings": 0},
    "rules": {"status": "pass", "findings": 0},
    "skills": {"status": "pass", "findings": 0},
    "workflow": {"status": "pass", "findings": 0},
    "runtime": {"status": "pass", "findings": 0},
    "dashboard": {"status": "pass", "findings": 0},
    "supabase": {"status": "pass", "findings": 0},
    "github": {"status": "pass", "findings": 0},
    "workers": {"status": "pass", "findings": 0},
    "security": {"status": "fail", "findings": 1, "blocking": true},
    "accessibility": {"status": "pass", "findings": 0},
    "deployment": {"status": "repairable", "findings": 1},
    "compliance": {"status": "pass", "findings": 0}
  },
  "audit_trail": {
    "checked_by": "deterministic-validator",
    "checked_at": "2026-07-27T21:00:00Z",
    "evidence_count": 47,
    "check_duration_ms": 5234
  }
}
```

---

## Category-Specific Checks

### 1. Doctrine
- Ethical principles documented
- User autonomy respected
- No exploitative patterns
- Transparency commitments met

### 2. Rules
- All governance rules pass
- No rule contradictions
- Evidence collected for all rules
- Confidence score > 0.80

### 3. Skills
- All required skills available
- Skill versions compatible
- No circular dependencies
- Skills tested and stable

### 4. Workflow
- Workflow structure valid
- All steps defined
- Dependencies resolved
- Gates properly configured

### 5. Runtime
- Packets compile successfully
- Context compression ratio met
- Hashes verify correctly
- Tier allocation appropriate

### 6. Dashboard
- Panels load without error
- Responsive design verified
- Keyboard navigation works
- No accessibility violations

### 7. Supabase
- All migrations applied
- Schema matches specification
- RLS policies enforced
- Foreign keys valid

### 8. GitHub
- All commits signed
- Branch protection enforced
- CI/CD pipeline passes
- No merge conflicts

### 9. Workers
- All workers registered
- Model health good
- Cost estimates accurate
- Availability > 99%

### 10. Security
- No hardcoded secrets
- Dependencies scanned
- Encryption enabled
- Audit logging active

### 11. Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigation works
- Screen reader compatible
- Color contrast sufficient

### 12. Deployment
- /health endpoint responds
- Metrics available
- Rollback procedure tested
- Alert thresholds set

### 13. Compliance
- GDPR data handling verified
- Consent mechanisms present
- Data deletion capability works
- Audit logs comprehensive

---

## Evidence Sources

| Source | Type | Example |
|--------|------|---------|
| **Code Analysis** | automated | Linting, type checking, complexity |
| **Test Results** | automated | Unit, integration, E2E test reports |
| **Scan Reports** | automated | Security, WCAG, dependency scans |
| **Audit Logs** | automated | Access patterns, changes, events |
| **Metrics** | automated | Coverage, latency, throughput, cost |
| **Documentation** | manual | Design docs, runbooks, commit messages |
| **Code Review** | manual | Reviewer comments, approval status |
| **Manual Testing** | manual | Screenshots, E2E walkthroughs |
| **Receipts** | hybrid | Prior approvals, test receipts |
| **Monitoring** | automated | Production metrics, error rates |

---

## Confidence Calculation

```
confidence = (automation_score × 0.40)
           + (coverage_score × 0.30)
           + (recency_score × 0.20)
           + (evidence_diversity × 0.10)

automation_score = categories_with_automated_checks / 13
coverage_score = evidence_items / required_evidence
recency_score = 1 - min(days_since_check / 30, 1.0)
evidence_diversity = unique_evidence_types / total_types
```

---

## Materiality Engine

### Severity Levels

| Level | Scope | Impact | Blocks |
|-------|-------|--------|--------|
| **CRITICAL** | Full product | Catastrophic | Always |
| **HIGH** | Component/lane | Significant | Usually |
| **MEDIUM** | Component | Moderate | Sometimes |
| **LOW** | Local | Minor | Rarely |

### Blocking Rules

```
if finding.severity == CRITICAL and finding.status == fail:
  promotion_ready = false
  escalation_level = 2
  status = STOP_GATE

else if finding.severity == HIGH and finding.status == fail:
  if finding.requires_approval:
    requires_manual_approval = true
    status = BLOCKED
  else:
    promotion_ready = false
    status = REPAIRABLE

else if finding.status == repairable:
  status = REPAIRABLE
  promotion_ready = false

else:
  finding.status == pass
  // no promotion block
```

---

## Success Criteria (Phase E)

✅ Acceptance Engine with 13 categories  
✅ 4-state results (PASS, REPAIRABLE, STOP_GATE, BLOCKED)  
✅ 6-step process (Load → Execute → Collect → Aggregate → Generate → Decide)  
✅ Evidence collection from 10+ sources  
✅ Confidence model (4 factors)  
✅ Materiality engine with blocking rules  
✅ Acceptance receipt schema  
✅ Category-specific checks (all 13 implemented)  
✅ Audit trail with timestamps  
✅ No contradictions with Phases A-D  

---

## Integration Points

**Upstream (Phases A-D):**
- Phase A (Runtime): Validates runtime packets
- Phase B (Rules): Executes rule acceptance
- Phase C (Skills): Checks skill availability
- Phase D (Workflow): Validates workflow definitions

**Downstream (Phases F+):**
- Phase F (Promotion): Feeds promotion state machine
- Phase G (Opportunities): Uses acceptance as signal
- Phase K (Completion): Part of continuous loop

---

## Files Produced (Phase E)

- `ACCEPTANCE_ENGINE_SPECIFICATION.md` (this file)
- `acceptance_engine_schema.json` (JSON Schema)
- `acceptance-engine.js` (implementation)
