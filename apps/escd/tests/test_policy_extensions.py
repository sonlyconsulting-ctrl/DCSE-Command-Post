from apps.escd.policy.extensions import *
from apps.escd.policy.complete_catalog import RULES, RULESETS, validate_complete_catalog


def test_item_transition_valid(): assert transition_allowed("item","captured","triaged")[0]
def test_item_transition_invalid(): assert not transition_allowed("item","captured","completed")[0]
def test_job_transition_retry_path(): assert transition_allowed("job","failed","queued")[0]
def test_approval_cannot_self_execute(): assert not transition_allowed("approval","approved","pending")[0]

def test_source_precedence_and_conflict():
    r=choose_source([
        {"source_class":"model_inference","source_ref":"m","value":2},
        {"source_class":"verified_live_operational","source_ref":"v","value":1},
    ])
    assert r["selected"]["source_ref"]=="v" and r["status"]=="conflict" and len(r["conflicts"])==1

def test_empty_source_unknown(): assert choose_source([])["status"]=="unknown"
def test_completion_requires_evidence(): assert completion_valid(True,[])[0] is False
def test_attempt_is_not_completion(): assert completion_valid(True,["e"],attempted_only=True)[0] is False
def test_verified_completion(): assert completion_valid(True,["e"])[0] is True

def test_briefing_empty_does_not_invent():
    b=build_briefing_snapshot({})
    assert b["changed"]==[] and b["completed"]==[] and b["next_best_action"] is None

def test_briefing_uses_persisted_state_marker(): assert build_briefing_snapshot({})["source"]=="persisted_reconciled_state"
def test_n2_escalates_only_on_shrinking_window():
    assert notification_escalation("N2",False,False)[0]=="N2"
    assert notification_escalation("N2",False,True)[0]=="N3"
def test_n4_persists(): assert notification_escalation("N4",False)[0]=="N4"
def test_ack_stops_escalation(): assert notification_escalation("N3",True,material_risk=True)[1]=="acknowledged"
def test_mobile_pending_until_server_ack(): assert mobile_action_result(False)["state"]=="pending"
def test_mobile_ack_without_evidence_not_complete(): assert mobile_action_result(True)["completed"] is False
def test_mobile_verified_requires_evidence(): assert mobile_action_result(True,"ev1")["completed"] is True
def test_connector_read_auto(): assert connector_execution_class("gmail","read")=="A0_AUTO"
def test_connector_external_write_approval(): assert connector_execution_class("gmail","send")=="A3_APPROVAL_REQUIRED"
def test_connector_internal_state_logs(): assert connector_execution_class("escd_state","update")=="A1_AUTO_LOG"
def test_complete_catalog_valid(): assert validate_complete_catalog()==[]
def test_complete_counts(): assert len(RULES)==54 and len(RULESETS)==19
