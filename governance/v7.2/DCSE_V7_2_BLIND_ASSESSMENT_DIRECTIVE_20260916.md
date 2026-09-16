# DCSE v7.2 Blind Assessment Directive

**Directive:** DCS-DIR-20260916-001  
**Authority:** DCS Level 0, express approval 2026-09-16  
**Status:** ACTIVE BY DCS DIRECTIVE  
**Scope:** DCSE v7.2 governance, model/agent independent assessment workflows  
**Effective:** Immediately

## Decision
DCS Level 0 approves the Blind Assessment Rule for immediate development and integration with v7.2.

## Rule
When DCSE requests a genuinely independent model or agent assessment, the assessment packet must minimize framing that can bias the receiving evaluator.

The packet should provide only the information necessary to perform the assessment safely and competently, including the problem or decision question, source evidence and provenance, verified constraints, material unknowns, access/safety boundaries, required output, and applicable authorization/Stop-Gates.

Unless materially required for authority, safety, provenance, or task execution, the packet must not:
1. Name or characterize the receiving model/agent.
2. Assign the receiving evaluator a persona, organizational role, seniority, expected posture, or identity.
3. State a preferred conclusion, recommendation, ranking, or expected answer.
4. Direct the evaluator to agree with, corroborate, contradict, validate, or disprove another model's conclusion.
5. Present prior interpretations as established conclusions when the underlying evidence can be supplied instead.
6. Disclose another evaluator's recommendation when that disclosure is unnecessary to the independent assessment.
7. Use positive or negative framing intended to steer the evaluator toward a result.

## Evidence Versus Interpretation
Raw/verified observations and necessary provenance may be included. Prior interpretations must be clearly separated from verified evidence and omitted when they are not necessary to the assigned assessment. The evaluator must be free to determine materiality, causation, alternatives, uncertainty, contradictions, and recommendations from the supplied evidence.

## Required Exceptions
Blindness does not override governance. The packet must still include information required to preserve DCS Level 0 reserved authority and approval gates, lane and PS firewall controls, credential/secret protections, destructive/production/public-release/migration/access/legal/deadline Stop-Gates, evidence provenance where material, and task scope/permitted actions.

Any exception that introduces potentially biasing context must be limited to the minimum necessary information and identified as an authority, safety, provenance, or execution requirement.

## Multi-Model Use
Where multiple independent assessments are requested, each evaluator should receive the same neutral evidence baseline unless a documented test design requires otherwise. Responses should be preserved separately before reconciliation so later evaluators are not contaminated by earlier conclusions.

Reconciliation occurs only after independent outputs have been captured. The reconciliation layer may compare agreements, contradictions, evidence strength, assumptions, omissions, and alternatives without retroactively altering the independent records.

## Integration Requirement
This rule is to be incorporated into v7.2 task routing, handoff/assessment packet generation, model-orchestration controls, D21/DCL validation where applicable, and future multi-model assessment workflows.

Existing active assessment packets should be reviewed for unnecessary evaluator identity, role, expectation, or conclusion framing when doing so does not destroy historical evidence. Historical records remain lineage; corrections should preserve the fact and reason for the correction.

## Validation Criteria
A blind assessment workflow passes when:
1. Sufficient evidence and constraints are supplied.
2. Unnecessary evaluator identity/role framing is absent.
3. No desired answer or agreement/disagreement instruction is embedded.
4. Evidence is distinguishable from prior interpretation.
5. Required governance and safety boundaries remain intact.
6. Independent outputs are captured before cross-model reconciliation.
7. Any necessary exception to blindness is documented and narrowly scoped.

## Promotion State
This directive is **ACTIVE BY DCS DIRECTIVE** effective immediately. Its existence in GitHub does not by itself constitute D05 `ACTIVE_RATIFIED` promotion. Any formal baseline promotion/reconciliation required by D05 remains a separate governed step.
