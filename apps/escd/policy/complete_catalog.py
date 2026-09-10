from .catalog import RuleDef, RULES as BASE_RULES

EXTRA_RULES = (
    RuleDef('ESCD-STA-001','RS-STATE','Item, job and approval state transitions follow explicit lifecycle graphs.','transition_allowed','STATE_DATA_MODEL'),
    RuleDef('ESCD-STA-002','RS-STATE','Invalid transitions are rejected rather than silently normalized.','transition_allowed','STATE_DATA_MODEL acceptance'),
    RuleDef('ESCD-SRC-001','RS-SOURCE-ROUTING','Source conflicts use governed precedence and preserve contradictory evidence.','choose_source','CONNECTOR_SOURCE_ROUTING_MATRIX'),
    RuleDef('ESCD-SRC-002','RS-SOURCE-ROUTING','Model inference is lowest source precedence.','choose_source','CONNECTOR_SOURCE_ROUTING_MATRIX'),
    RuleDef('ESCD-SRC-003','RS-SOURCE-ROUTING','Connector writes resolve to an autonomy class before execution.','connector_execution_class','CONNECTOR_SOURCE_ROUTING_MATRIX'),
    RuleDef('ESCD-BRF-001','RS-BRIEFING','Briefing is generated only from persisted/reconciled state.','build_briefing_snapshot','EXECUTIVE_BRIEFING_SPEC'),
    RuleDef('ESCD-BRF-002','RS-BRIEFING','Missing briefing data remains empty/unknown rather than invented.','build_briefing_snapshot','EXECUTIVE_BRIEFING_SPEC'),
    RuleDef('ESCD-EVD-001','RS-DECISIONS-EVIDENCE','Completion requires exit criteria and evidence; attempt alone is not completion.','completion_valid','RUL-006/EXECUTIVE_BRIEFING_SPEC'),
    RuleDef('ESCD-NOT-003','RS-NOTIFICATIONS','N2 escalates only when unacknowledged and action window materially shrinks.','notification_escalation','NOTIFICATION_ESCALATION_POLICY'),
    RuleDef('ESCD-NOT-004','RS-NOTIFICATIONS','N4 remains a hard stop until acknowledged/resolved.','notification_escalation','NOTIFICATION_ESCALATION_POLICY'),
    RuleDef('ESCD-MOB-001','RS-MOBILE','Mobile action stays pending until server acknowledgement.','mobile_action_result','MOBILE_INTERACTION_MODEL'),
    RuleDef('ESCD-MOB-002','RS-MOBILE','Server acknowledgement without evidence is not verified completion.','mobile_action_result','MOBILE_INTERACTION_MODEL'),
)

_merged = {}
for rule in BASE_RULES + EXTRA_RULES:
    _merged.setdefault(rule.rule_id, rule)
RULES = tuple(_merged.values())
RULESETS = {}
for rule in RULES:
    RULESETS.setdefault(rule.ruleset_id, []).append(rule)

def validate_complete_catalog():
    ids = [r.rule_id for r in RULES]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append('duplicate_rule_id')
    if len(RULESETS) != 19:
        errors.append('unexpected_ruleset_count')
    if len(RULES) != 54:
        errors.append('unexpected_rule_count')
    return errors
