# DCSE Conversation Intake and Closeout Contract v1

**Document ID:** DCSE-CIC-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-11  
**Parent:** DCSE Governed Execution and Interaction Standard v1  
**Status:** APPROVED FOR CANONICAL v7.2 INTEGRATION

## 1. Purpose

Make the beginning and end of a governed conversation or task symmetrical, attributable, and machine-usable.

## 2. Intake Record

For every substantive task, capture before execution:

```yaml
task_id:
parent_task_id:
session_or_conversation_ref:
date_started:
lane:
entity:
task_type:
requested_outcome:
destination:
artifact_or_action:
authority_holder:
authority_source:
executing_model_or_agent:
systems:
access_state:
effort_level:
risk_level:
data_sensitivity:
change_scope:
reversibility:
secret_exposure:
ps_exposure:
approval_requirement:
rollback_requirement:
expected_deliverables:
exit_criteria:
initial_status:
```

The visible preflight may be concise, but the semantic fields must be preserved.

## 3. Runtime Event Record

Material events SHOULD preserve:

- timestamp/order;
- action;
- system;
- actor/tool;
- input authority/source;
- result;
- evidence pointer;
- status change;
- error/finding;
- corrective action.

Routine conversational reasoning need not become a verbose log. Capture state-changing or governance-significant events.

## 4. Closeout Trigger

Closeout begins when DCS clearly indicates completion or closure, including instructions equivalent to:

- close this conversation;
- close out the task;
- finalize and close;
- we are done with this asset/task;
- authorize closure.

If work is mechanically complete but explicit DCS closure is required and not yet given, status is `READY_TO_CLOSE`, not `CLOSED`.

## 5. Mandatory Closeout Record

```yaml
task_id:
date_closed:
close_authority:
original_requested_outcome:
actual_completed_outcome:
goal_status:
goal_shift_reasoning:
final_task_state:
deliverables:
systems_changed:
system_state_after:
validation_results:
evidence_references:
unresolved_findings:
deferred_items:
rollback_or_recovery:
next_recommended_work:
required_dcs_decision:
dcl_status:
completion_evidence_status:
conversation_close_state:
```

## 6. Final States

Allowed close states:

- `CLOSED_COMPLETE`
- `CLOSED_PARTIAL`
- `CLOSED_BLOCKED`
- `READY_TO_CLOSE`
- `SUPERSEDED`
- `TRANSFERRED_WITH_HANDOFF`

A closeout record SHALL NOT use COMPLETE when material dependent state remains unreconciled unless that dependency is explicitly outside scope and disclosed.

## 7. Goal Reconciliation

The closeout SHALL compare original goal to actual outcome.

Allowed goal status:

- UNCHANGED_COMPLETED
- UNCHANGED_PARTIAL
- SHIFTED_AUTHORIZED
- NARROWED_AUTHORIZED
- EXPANDED_AUTHORIZED
- BLOCKED
- SUPERSEDED

Silent goal substitution is prohibited.

## 8. Conversation-Level Evidence

The final response should expose enough navigation for DCS to inspect execution without reproducing secrets or low-value logs.

Where available include:

- GitHub PR/commit/path;
- Supabase project/schema/record key;
- Vercel project/deployment ID;
- Tribunal receipt;
- validation run;
- rollback reference;
- related task/issue.

## 9. Handoff Instead of Close

When a conversation ends because execution moves to another model, agent, tool, or session, create a handoff packet instead of falsely closing the task.

The handoff SHALL include:

- same task ID;
- current state;
- authority source;
- completed actions;
- outstanding actions;
- exact evidence;
- next gate;
- exclusions;
- rollback state.

## 10. DDNA Learning Boundary

Conversation intake and closeout records are strong DDNA learning sources because they expose input state, action path, and observed result.

DDNA may derive candidate patterns and candidate rules from these records. It may not convert frequency or recurrence into authority.

**Structure Precedes Scale.**
