from datetime import datetime, timedelta
import pytest
from apps.escd.policy.models import Action, Item, RetryContext, NotificationState, CalendarEvent, WorkflowTemplate
from apps.escd.policy.engine import *
from apps.escd.policy.catalog import RULES, RULESETS, validate_catalog


def item(**kw):
    base=dict(item_id="I1", title="x", mission_priority=50, explicit_priority=50, urgency=50,
              revenue_relevance=0, unblock_value=0, consequence=50, aging=50,
              effort_efficiency=50, strategic_leverage=50, dcs_override=0)
    base.update(kw)
    return Item(**base)

@pytest.mark.parametrize("action,expected", [
    (Action(kind="read"), "A0_AUTO"),
    (Action(kind="task_update", internal_state_change=True), "A1_AUTO_LOG"),
    (Action(kind="PROPOSE_CALENDAR", proposal_only=True), "A2_PROPOSE"),
    (Action(kind="send", external=True), "A3_APPROVAL_REQUIRED"),
    (Action(kind="deploy", production=True), "A3_APPROVAL_REQUIRED"),
    (Action(kind="delete", destructive=True), "A3_APPROVAL_REQUIRED"),
    (Action(kind="secret", exposes_secret=True), "A4_PROHIBITED"),
    (Action(kind="bypass", bypasses_control=True), "A4_PROHIBITED"),
    (Action(kind="fake", fabricates_evidence=True), "A4_PROHIBITED"),
])
def test_autonomy(action, expected):
    assert classify_autonomy(action) == expected

def test_more_restrictive_wins():
    assert classify_autonomy(Action(kind="x", external=True, exposes_secret=True)) == "A4_PROHIBITED"

def test_queue_now(): assert route_queue(item()) == "NOW"
def test_queue_approval(): assert route_queue(item(missing_approval=True)) == "APPROVAL"
def test_queue_waiting_blocked(): assert route_queue(item(blocked=True)) == "WAITING"
def test_queue_waiting_dependency(): assert route_queue(item(external_dependency=True)) == "WAITING"
def test_queue_watch(): assert route_queue(item(future_trigger=True)) == "WATCH"
def test_queue_backlog(): assert route_queue(item(actionable=False)) == "BACKLOG"
def test_blocked_not_scored(): assert score_item(item(blocked=True))["score"] is None

def test_score_deterministic():
    assert score_item(item()) == score_item(item())

def test_score_expected_weighted():
    assert score_item(item())["score"] == 37.5

def test_score_clamps():
    assert score_item(item(urgency=500))["contributions"]["urgency"] == 20.0

def test_rank_dcs_override_tiebreak():
    assert rank_items([item(item_id="A"), item(item_id="B", dcs_override=100)])[0]["item_id"] == "B"

def test_rank_stable_id_tiebreak():
    assert rank_items([item(item_id="B"), item(item_id="A")])[0]["item_id"] == "A"

def test_revenue_weighting():
    assert score_item(item(revenue_relevance=100))["score"] > score_item(item(revenue_relevance=0))["score"]

@pytest.mark.parametrize("ctx,allowed", [
    (RetryContext(0,3,idempotent=True), True),
    (RetryContext(3,3,idempotent=True), False),
    (RetryContext(0,3,security_failure=True,idempotent=True), False),
    (RetryContext(0,3,permission_failure=True,idempotent=True), False),
    (RetryContext(0,3,uncertain_external_side_effect=True,idempotent=True), False),
    (RetryContext(0,3,destructive=True,idempotent=False), False),
])
def test_retry(ctx, allowed):
    assert retry_allowed(ctx)[0] is allowed

@pytest.mark.parametrize("state,expected", [
    (NotificationState("x",2,1), True),
    (NotificationState("x",1,1), False),
    (NotificationState("x",1,1,threshold_crossed=True), True),
    (NotificationState("x",1,1,worsened=True), True),
    (NotificationState("x",1,1,deadline_approaching=True), True),
    (NotificationState("x",2,1,acknowledged=True), False),
])
def test_notify(state,expected):
    assert should_notify(state)[0] is expected

def test_calendar_overlap():
    t=datetime(2026,1,1,9)
    events=[CalendarEvent("A",t,t+timedelta(hours=1)),CalendarEvent("B",t+timedelta(minutes=30),t+timedelta(hours=2))]
    assert detect_calendar_conflicts(events)[0]["class"] == "C1"

def test_calendar_buffer():
    t=datetime(2026,1,1,9)
    events=[CalendarEvent("A",t,t+timedelta(hours=1)),CalendarEvent("B",t+timedelta(hours=1,minutes=5),t+timedelta(hours=2))]
    assert detect_calendar_conflicts(events,10)[0]["class"] == "C2"

def test_calendar_none():
    t=datetime(2026,1,1,9)
    events=[CalendarEvent("A",t,t+timedelta(hours=1)),CalendarEvent("B",t+timedelta(hours=2),t+timedelta(hours=3))]
    assert detect_calendar_conflicts(events,10) == []

def test_dedupe_preserves_sources():
    result=dedupe_commitments([{"commitment_id":"X","title":"t","source_ref":"a"},{"commitment_id":"x","title":"t","source_ref":"b"}])
    assert len(result) == 1 and result[0]["source_refs"] == ["a","b"]

@pytest.mark.parametrize("msg,expected", [
    ({"explicit_decision_required":True},"DECISION"),
    ({"meeting_request":True},"SCHEDULE"),
    ({"reply_required":True},"REPLY"),
    ({"waiting_on_other":True},"WAITING"),
    ({"action_required":True},"ACTION"),
    ({"monitor":True},"WATCH"),
    ({},"REFERENCE"),
])
def test_comm_triage(msg,expected):
    assert communication_triage(msg) == expected

@pytest.mark.parametrize("text,op", [
    ("make website","MAKE"),("fix app","FIX"),("review draft","REVIEW"),("release build","RELEASE"),
    ("monitor status","MONITOR"),("research topic","RESEARCH"),("send note","COMMUNICATE"),
    ("decide option","DECIDE"),("remind me","ROUTINE"),("organize files","DO"),
])
def test_parse_command(text,op):
    assert parse_command(text)["operation"] == op

def valid_template(**kw):
    base=dict(template_id="T1",name="T",version="1.0",status="candidate",template_type="MAKE",purpose="p",scope="s",
              supported_context_types=["product"],input_contract={},required_sources=[],preconditions=[],
              steps=[{"step_id":"S1","action_type":"DO","instruction":"x","autonomy_class":"A0_AUTO","verification_method":"test","failure_route":"stop"}],
              decision_points=[],approval_points=[],executor_classes=["python"],connector_requirements=[],evidence_requirements=["receipt"],
              test_requirements=["unit"],rollback_or_recovery="revert",exit_criteria=["pass"],follow_up_rules=[],notification_policy="none",
              lane_restrictions=[],retry_policy={"max":2},owner="DCS",provenance=["spec"])
    base.update(kw)
    return WorkflowTemplate(**base)

def test_template_valid(): assert validate_workflow_template(valid_template()) == []
def test_template_invalid_type(): assert "invalid_template_type" in validate_workflow_template(valid_template(template_type="BOGUS"))
def test_template_steps_required(): assert "steps_required" in validate_workflow_template(valid_template(steps=[]))
def test_template_step_contract(): assert any(x.startswith("step_contract_incomplete") for x in validate_workflow_template(valid_template(steps=[{"step_id":"S1"}])))
def test_template_secret(): assert "secret_prohibited" in validate_workflow_template(valid_template(input_contract={"password":"x"}))
def test_child_cannot_weaken(): assert child_controls_valid({"approval_required":True},{"approval_required":False})[0] is False
def test_child_can_strengthen(): assert child_controls_valid({"approval_required":False},{"approval_required":True})[0] is True

def test_ddna_candidate_valid():
    c={"candidate_id":"C","source_refs":["s"],"provenance":["p"],"candidate_type":"rule","content":"x","status":"candidate"}
    assert ddna_candidate_valid(c)[0] is True

def test_ddna_requires_source():
    c={"candidate_id":"C","source_refs":[],"provenance":["p"],"candidate_type":"rule","content":"x","status":"candidate"}
    assert ddna_candidate_valid(c)[0] is False

def test_ddna_no_secret():
    c={"candidate_id":"C","source_refs":["s"],"provenance":["p"],"candidate_type":"rule","content":"password=x","status":"candidate"}
    assert ddna_candidate_valid(c)[0] is False

def test_decision_record():
    r={"decision_id":"D","facts":[],"unknowns":[],"alternatives":[],"tradeoffs":[],"recommendation":"x","decision":"pending","evidence_refs":[]}
    assert decision_record_valid(r)[0]

def test_executed_decision_requires_evidence():
    r={"decision_id":"D","facts":[],"unknowns":[],"alternatives":[],"tradeoffs":[],"recommendation":"x","decision":"executed","evidence_refs":[]}
    assert decision_record_valid(r)[0] is False

def test_contact_requires_source(): assert contact_context_valid({})[0] is False
def test_contact_no_sensitive_inference(): assert contact_context_valid({"source_refs":["x"],"inferred_sensitive_trait":True})[0] is False

@pytest.mark.parametrize("routine,prior,expected", [
    ({"paused":True},None,"SKIP"),({"cancelled":True},None,"SKIP"),({"run_key":"1"},"1","SKIP"),
    ({"run_key":"2","missed":True,"missed_run_policy":"skip"},"1","SKIP"),({"run_key":"2"},"1","RUN"),
])
def test_routine(routine,prior,expected):
    assert routine_run_decision(routine,prior)[0] == expected

def test_make_gate():
    ok,_=make_fix_release_gate("MAKE",{"requirements":1,"baseline":1,"test_requirements":1,"exit_criteria":1})
    assert ok

def test_fix_gate():
    ok,_=make_fix_release_gate("FIX",{"target":1,"problem_statement":1,"reproduction_evidence":1,"known_good_baseline":1,"regression_surface":1,"rollback_point":1})
    assert ok

def test_release_gate_requires_approval():
    ok,errors=make_fix_release_gate("RELEASE",{"validated_build":1,"test_evidence":1,"rollback":1,"approval_state":"pending"})
    assert not ok and "approval_required" in errors

def test_release_gate_passes():
    ok,_=make_fix_release_gate("RELEASE",{"validated_build":1,"test_evidence":1,"rollback":1,"approval_state":"approved"})
    assert ok

def test_rule_catalog_valid(): assert validate_catalog() == []
def test_rule_catalog_has_all_major_sets():
    expected={"RS-GOVERNANCE","RS-AUTONOMY","RS-TASK-STATE","RS-NBA","RS-CALENDAR","RS-COMMUNICATIONS","RS-PERSON-CONTEXT","RS-WORKFLOW","RS-MAKE-FIX-RELEASE","RS-RECOVERY","RS-NOTIFICATIONS","RS-ROUTINES","RS-DECISIONS-EVIDENCE","RS-DDNA-CANDIDATE","RS-COMMAND"}
    assert expected.issubset(RULESETS.keys())
def test_rule_ids_unique(): assert len({r.rule_id for r in RULES}) == len(RULES)
def test_every_rule_has_executor_and_source(): assert all(r.executor and r.source for r in RULES)
