from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class RuleDef:
    rule_id: str
    ruleset_id: str
    statement: str
    executor: str
    source: str

RULES: Tuple[RuleDef, ...] = (
    RuleDef('ESCD-GOV-001','RS-GOVERNANCE','ESCD serves DCS and does not replace DCSE authority.','governance boundary','ASSISTANT_OPERATING_RULES RUL-001'),
    RuleDef('ESCD-GOV-002','RS-GOVERNANCE','Preserve source provenance and separate derived state from source evidence.','dedupe_commitments/state persistence','RUL-002/003'),
    RuleDef('ESCD-GOV-003','RS-GOVERNANCE','Stable IDs survive handoff, retry, restart, and model change.','state model constraint','RUL-007'),
    RuleDef('ESCD-GOV-004','RS-GOVERNANCE','Material unknowns stop affected execution.','classify_autonomy','RUL-026'),
    RuleDef('ESCD-AUT-001','RS-AUTONOMY','Every consequential action resolves to A0-A4 before dispatch.','classify_autonomy','AUTONOMY_CONTRACT'),
    RuleDef('ESCD-AUT-002','RS-AUTONOMY','External/public/financial/production/destructive/auth/authority/legal-security/irreversible actions require approval.','classify_autonomy','AUTONOMY_CONTRACT A3'),
    RuleDef('ESCD-AUT-003','RS-AUTONOMY','Secrets, control bypass, fabricated evidence and protected-lane violations are prohibited.','classify_autonomy/contains_secret','AUTONOMY_CONTRACT A4'),
    RuleDef('ESCD-AUT-004','RS-AUTONOMY','Internal state changes may execute only with durable logging.','classify_autonomy','AUTONOMY_CONTRACT A1'),
    RuleDef('ESCD-TASK-001','RS-TASK-STATE','Blocked or dependent work cannot remain in NOW.','route_queue','RUL-009'),
    RuleDef('ESCD-TASK-002','RS-TASK-STATE','Missing approval routes to APPROVAL.','route_queue','NBA eligibility'),
    RuleDef('ESCD-TASK-003','RS-TASK-STATE','Future-trigger work routes to WATCH.','route_queue','workflow stream'),
    RuleDef('ESCD-TASK-004','RS-TASK-STATE','Duplicate source reports link to one commitment while preserving source refs.','dedupe_commitments','RUL-008'),
    RuleDef('ESCD-NBA-001','RS-NBA','Only actionable NOW items receive scores.','score_item','NEXT_BEST_ACTION_SPEC'),
    RuleDef('ESCD-NBA-002','RS-NBA','NBA score uses governed normalized weights totaling 100 percent.','score_item','NEXT_BEST_ACTION_SPEC'),
    RuleDef('ESCD-NBA-003','RS-NBA','Identical inputs produce identical rankings and deterministic tie breaks.','rank_items','NEXT_BEST_ACTION_SPEC'),
    RuleDef('ESCD-NBA-004','RS-NBA','DCS override outranks assistant inference.','rank_items','RUL-011/NBA override'),
    RuleDef('ESCD-CAL-001','RS-CALENDAR','Overlapping events surface C1 conflict.','detect_calendar_conflicts','CALENDAR_CONFLICT_POLICY'),
    RuleDef('ESCD-CAL-002','RS-CALENDAR','Insufficient configured transition buffer surfaces C2 conflict.','detect_calendar_conflicts','CALENDAR_CONFLICT_POLICY'),
    RuleDef('ESCD-CAL-003','RS-CALENDAR','Conflict detection never authorizes external calendar modification.','classify_autonomy','CALENDAR rule 1'),
    RuleDef('ESCD-COM-001','RS-COMMUNICATIONS','Messages route deterministically to decision, schedule, reply, waiting, action, watch, or reference.','communication_triage','EMAIL_MESSAGE_TRIAGE_RULES'),
    RuleDef('ESCD-COM-002','RS-COMMUNICATIONS','Drafting may be internal but external send is approval-gated by default.','classify_autonomy','RUL-014'),
    RuleDef('ESCD-PER-001','RS-PERSON-CONTEXT','Person context requires provenance.','contact_context_valid','RUL-015'),
    RuleDef('ESCD-PER-002','RS-PERSON-CONTEXT','ESCD does not infer sensitive traits into person context.','contact_context_valid','RUL-015'),
    RuleDef('ESCD-WF-001','RS-WORKFLOW','Templates must use approved template types and stable version identity.','validate_workflow_template','WORKFLOW_TEMPLATE_SCHEMA'),
    RuleDef('ESCD-WF-002','RS-WORKFLOW','Template steps require action, autonomy, verification and failure routes.','validate_workflow_template','WORKFLOW_TEMPLATE_SCHEMA'),
    RuleDef('ESCD-WF-003','RS-WORKFLOW','Child templates may add but not weaken parent approval, evidence, security or rollback controls.','child_controls_valid','WORKFLOW_TEMPLATE_SCHEMA inheritance'),
    RuleDef('ESCD-WF-004','RS-WORKFLOW','Templates must not contain secrets.','validate_workflow_template/contains_secret','WORKFLOW_TEMPLATE_SCHEMA rule 9'),
    RuleDef('ESCD-MFR-001','RS-MAKE-FIX-RELEASE','MAKE requires requirements, baseline, tests and exit criteria.','make_fix_release_gate','RUL-017/029'),
    RuleDef('ESCD-MFR-002','RS-MAKE-FIX-RELEASE','FIX requires target, defect, reproduction evidence, known-good baseline, regression surface and rollback.','make_fix_release_gate','RUL-017/029'),
    RuleDef('ESCD-MFR-003','RS-MAKE-FIX-RELEASE','RELEASE is independent and requires validated build, test evidence, rollback and approval.','make_fix_release_gate','RUL-018'),
    RuleDef('ESCD-REC-001','RS-RECOVERY','Retries are bounded and stay within original authorization envelope.','retry_allowed','RUL-010'),
    RuleDef('ESCD-REC-002','RS-RECOVERY','Permission, security, cost, payload or authority conflicts are not blindly retried.','retry_allowed','AUTONOMY failure policy'),
    RuleDef('ESCD-REC-003','RS-RECOVERY','Uncertain external side effects require reconciliation before retry.','retry_allowed','FAILURE_RECOVERY_MODEL'),
    RuleDef('ESCD-NOT-001','RS-NOTIFICATIONS','Notify on meaningful change, threshold crossing, worsening or deadline approach.','should_notify','RUL-019'),
    RuleDef('ESCD-NOT-002','RS-NOTIFICATIONS','Acknowledged unchanged state does not repeatedly notify.','should_notify','RUL-019/calendar rule 5'),
    RuleDef('ESCD-ROU-001','RS-ROUTINES','Paused or cancelled routines do not run.','routine_run_decision','RUL-020'),
    RuleDef('ESCD-ROU-002','RS-ROUTINES','Routine run keys enforce idempotency and missed-run policy.','routine_run_decision','RUL-020'),
    RuleDef('ESCD-DEC-001','RS-DECISIONS-EVIDENCE','Material decisions preserve facts, unknowns, alternatives, tradeoffs, recommendation, decision and evidence.','decision_record_valid','RUL-012'),
    RuleDef('ESCD-DEC-002','RS-DECISIONS-EVIDENCE','Executed decisions require execution evidence.','decision_record_valid','RUL-006/012'),
    RuleDef('ESCD-DDNA-001','RS-DDNA-CANDIDATE','ESCD DDNA outputs remain candidates and require source provenance.','ddna_candidate_valid','RUL-022'),
    RuleDef('ESCD-DDNA-002','RS-DDNA-CANDIDATE','DDNA candidates cannot contain secrets or self-promote to operative authority.','ddna_candidate_valid','RUL-022/023'),
    RuleDef('ESCD-CMD-001','RS-COMMAND','Commands normalize to an operation and pass authority evaluation before execution.','parse_command/classify_autonomy','COMMAND_GRAMMAR_SPEC'),
)

RULESETS = {}
for rule in RULES:
    RULESETS.setdefault(rule.ruleset_id, []).append(rule)

def validate_catalog():
    ids = [r.rule_id for r in RULES]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append('duplicate_rule_id')
    if any(not rs for rs in RULESETS.values()):
        errors.append('empty_ruleset')
    return errors
