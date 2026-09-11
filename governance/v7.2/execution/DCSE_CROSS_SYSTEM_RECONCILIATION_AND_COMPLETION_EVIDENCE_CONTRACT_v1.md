# DCSE Cross-System Reconciliation and Completion Evidence Contract v1

**Document ID:** DCSE-CSRC-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-11  
**Parent:** DCSE Governed Execution and Interaction Standard v1  
**Status:** APPROVED FOR CANONICAL v7.2 INTEGRATION

## 1. Purpose

Prevent models, agents, tools, and applications from reporting completion while GitHub, Vercel, Supabase, Tribunal, or conversation state disagree.

## 2. Reconciliation Principle

Each governed object has one canonical home under D22.

Other systems hold references, runtime state, deployment state, or evidence.

Reconciliation verifies that those representations agree on the facts they are responsible for.

## 3. Reconciliation Matrix

For each affected object capture as applicable:

| Dimension | GitHub | Vercel | Supabase | Tribunal | Conversation |
|---|---|---|---|---|---|
| identity/version | commit/path/hash | deployment/source commit | record/version | receipt refs | task refs |
| lifecycle state | branch/merged | preview/production | active/status | validation/promotion | working/closed |
| authority | canonical refs | none independently | registry ref only | evidence only | resolved authority |
| runtime | source/config | deployed runtime | structured state | runtime evidence | reported state |
| rollback | prior commit | prior deployment | migration/checkpoint | rollback receipt | rollback pointer |

## 4. Completion Invariant

A task touching multiple governed systems is COMPLETE only when:

1. all intended writes occurred;
2. each write was read back or independently verified;
3. canonical identity is known;
4. dependent references are current;
5. deployment/runtime state matches the claimed state;
6. authority and lifecycle state are not contradicted;
7. material hashes/versions are captured when required;
8. unresolved drift is either corrected or explicitly outside scope;
9. rollback/recovery is identified where applicable;
10. Completion Evidence is human-reviewable.

## 5. Drift Classes

- `IDENTITY_DRIFT`: version/hash/commit mismatch.
- `PATH_DRIFT`: stale canonical reference.
- `LIFECYCLE_DRIFT`: active/candidate/promoted/deployed states disagree.
- `AUTHORITY_DRIFT`: a surface claims authority it does not possess.
- `RUNTIME_DRIFT`: deployed or database state differs from source/expected state.
- `EVIDENCE_DRIFT`: receipt/log claims more than verified state.
- `SECRET_HANDLING_DRIFT`: sensitive data appears on an unauthorized surface.
- `TASK_STATE_DRIFT`: conversation/task close state differs from actual execution state.

Critical security or secret-handling drift triggers the applicable Stop-Gate.

## 6. Completion Evidence Packet

Minimum packet for material cross-system work:

```yaml
task_id:
baseline_or_start_state:
authority_source:
systems_involved:
changes:
canonical_artifacts:
commit_or_version_ids:
deployment_ids:
runtime_record_keys:
material_hashes:
validation_results:
security_validation:
reconciliation_results:
unresolved_findings:
rollback_or_recovery:
tribunal_receipt:
final_task_state:
dcs_decision_required:
```

## 7. Evidence Quality

Evidence SHALL be:

- attributable;
- specific;
- current enough for the claim;
- directly navigable where possible;
- free of secret values;
- sufficient to backward-chain the claimed final state.

Screenshots, logs, model statements, or database rows may support a claim but do not substitute for the proper canonical source where one exists.

## 8. Reconciliation Order

For governance/code/deployment workflows, preferred order is:

`AUTHORITY -> CANONICAL SOURCE -> VERSION/HASH -> RUNTIME/DEPLOYMENT -> REGISTRY -> TRIBUNAL -> CONVERSATION CLOSEOUT`

For a runtime-only state update, use the applicable canonical-home order under D22.

## 9. Failure Handling

If one system cannot be reconciled:

- do not erase conflicting evidence;
- classify the task PARTIAL or BLOCKED as appropriate;
- state whether the unresolved surface is canonical or distribution-only;
- identify impact on subsequent work;
- preserve the last verified state.

## 10. Baseline Relationship

Every material cross-system change SHOULD identify a pre-change baseline or rollback checkpoint.

For the first implementation of this contract, the parent checkpoint is:

`DCSE-V7.2-BASELINE-A-20260911 @ 68a3bc164e75dbbab710590c57c04bf9a142c850`

Future checkpoints may supersede it as rollback/reference anchors without rewriting it.

## 11. DDNA and Rule Foundry Feed

Reconciliation records are preferred evidence for future rule extraction because they expose expected state versus observed state.

DDNA may extract candidate rules from:
- repeated drift;
- repeated corrective actions;
- stable success criteria;
- recurring stop conditions;
- recurrent cross-system dependencies.

Only the Rule Foundry promotion process may convert those candidates into active executable baselines.

**Structure Precedes Scale.**
