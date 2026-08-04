# DCSE Doctrine D02: Forward Derivation and Backward Proof v7.1 RC3 Candidate

**Document ID:** DCSE-D02-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to entity, confidentiality, privacy, and protected-lane isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D02_Forward_Backward_Chaining.md`  
**Source SHA-256:** `53347a643f9f7508845a77d873e33c682bbab4f286505a3a2275bcceaa661bd3`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**D01 dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D01_Forward_Thinking_v7.1_RC3_CANDIDATE.md`  
**D01 dependency SHA-256:** `b1eb4f764ec80722ee5040837561994bba42403284de0ae2de4269074e13033d`  
**DART dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D17_DART_Universal_Assurance_v7.1_RC3_CANDIDATE.md`  
**DART dependency SHA-256:** `568a8f2b3b2f8a960ebcf30dc94679dbb66f94a51aa2a51a0a0f86dc1da633f1`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D02 governs two complementary reasoning operations:

- forward derivation builds an output from admitted facts, rules, requirements, decisions, and dependencies;
- backward proof starts with the intended goal and proves that every required condition is satisfied by valid evidence.

D02 supports D17 Assess and Test while preserving traceability between source, decision, artifact, criterion, and result. It does not expose private chain-of-thought. It records material inputs, rules, decisions, evidence, and test outcomes.

## 2. Governing principles

1. Derivation begins only from admitted facts, rules, requirements, and authorized decisions.
2. Goal language is translated into observable conditions.
3. Every blocking condition has a proof requirement.
4. Material decisions are traceable without requiring paragraph-level private reasoning logs.
5. A failed proof returns the affected work to correction, not automatic rejection of unrelated work.
6. An error that happens before the intended control is exercised is an invalid test, not a pass.
7. Positive and negative tests are used where access, security, privacy, or failure behavior matters.
8. Circular support, self-citation, and repeated model assertions do not create corroboration.
9. Conflicting evidence is preserved and resolved explicitly.
10. Proof strength is proportional to consequence and intended use.

## 3. Input admission

Forward derivation may use:

- verified canonical sources;
- governed evidence;
- user-supplied facts with preserved provenance;
- external data admitted under D17 source controls;
- explicit DCS decisions;
- promoted doctrine and approved workflow rules;
- verified environment, capability, and configuration records;
- declared assumptions and inferences when their limits remain visible.

It must not silently treat model memory, generated summaries, stale caches, unverified registry rows, branch labels, or prior confidence statements as fact.

## 4. Forward derivation graph

```yaml
derivation_graph:
  graph_id: ""
  task_id: ""
  objective_ref: ""
  source_nodes: []
  rule_nodes: []
  requirement_nodes: []
  decision_nodes: []
  transformation_nodes: []
  artifact_nodes: []
  dependency_edges: []
  excluded_inputs: []
  unresolved_inputs: []
  generated_at: ""
```

### 4.1 Material derivation step

```yaml
derivation_step:
  step_id: ""
  input_refs: []
  rule_or_requirement_refs: []
  operation: ""
  output_ref: ""
  decision_basis: ""
  authority_ref: ""
  validation_ref: ""
  reversible: false
```

Traceability is required for material strategic, security, privacy, architectural, commercial, deployment, authority, and lifecycle decisions. It is not required for every sentence or ordinary formatting choice.

## 5. Forward execution procedure

1. normalize the objective and intended output;
2. load the D21 Doctrine Run Plan;
3. admit and classify sources;
4. identify requirements and acceptance criteria;
5. create the dependency graph;
6. order executable steps;
7. identify missing inputs, capabilities, and authority;
8. scaffold reversible structure where permitted;
9. execute steps within authority;
10. validate intermediate outputs at material boundaries;
11. preserve changes and evidence;
12. submit the result to backward proof.

Forward execution must not skip a dependency merely because a later output appears plausible.

## 6. Goal decomposition

Backward proof starts with a goal-state contract:

```yaml
goal_proof_contract:
  proof_id: ""
  goal_ref: ""
  intended_use: ""
  artifact_refs: []
  blocking_criteria: []
  nonblocking_criteria: []
  required_evidence: []
  required_positive_tests: []
  required_negative_tests: []
  required_regression_tests: []
  rollback_or_recovery_tests: []
  authority_requirements: []
  final_disposition_rule: ""
```

Each criterion must be observable, attributable, and decidable. Subjective terms such as polished, complete, production-ready, secure, accessible, accurate, delivered, or approved require measurable definitions for the current artifact.

## 7. Backward proof graph

```yaml
backward_proof_graph:
  graph_id: ""
  goal_proof_ref: ""
  criterion_nodes: []
  evidence_nodes: []
  test_nodes: []
  authority_nodes: []
  dependency_edges: []
  satisfied_nodes: []
  failed_nodes: []
  invalid_test_nodes: []
  insufficient_evidence_nodes: []
  residual_findings: []
```

The proof proceeds from final intended use to every blocking precondition, then links each precondition to evidence or a valid test result.

## 8. Proof states

| State | Meaning |
| --- | --- |
| PROVEN | Valid evidence directly satisfies the criterion. |
| SUPPORTED | Evidence supports the criterion but does not meet final proof requirements. |
| FAILED | Valid evidence shows the criterion is not satisfied. |
| INVALID_TEST | The test did not exercise the intended condition. |
| INSUFFICIENT_EVIDENCE | Required proof is absent or inconclusive. |
| NOT_APPLICABLE | The criterion is outside declared scope with recorded basis. |

A criterion cannot be PROVEN by absence of an error when the intended code, policy, permission, workflow, or user path was never reached.

## 9. Evidence sufficiency

Evidence evaluation considers:

- identity and provenance;
- integrity and content hash where applicable;
- date, environment, and freshness;
- directness to the criterion;
- independence from the claim being tested;
- completeness of scope;
- positive and negative coverage;
- reproducibility;
- authority and permitted use;
- conflicting evidence;
- known limitations.

Multiple copies of the same source do not count as independent corroboration.

## 10. Positive, negative, and recovery proof

For authorization, security, privacy, access, and workflow controls:

- positive proof verifies that an authorized actor can perform the intended action;
- negative proof verifies that an unauthorized actor or invalid condition is denied for the intended reason;
- boundary proof verifies ownership, lane, role, time, state, and scope limits;
- recovery proof verifies retry, lease, rollback, restore, or forward-recovery behavior;
- regression proof verifies that correction did not break previously accepted behavior.

A denial caused by an unrelated constraint, missing fixture, syntax error, null violation, or unreachable endpoint is `INVALID_TEST` for the intended authorization rule.

## 11. Contradiction and conflict handling

When sources or tests conflict:

1. preserve each source and result;
2. compare authority, scope, environment, time, and integrity;
3. identify whether the conflict is factual, temporal, semantic, or representational;
4. obtain the minimum additional evidence needed;
5. apply the higher authority only within its scope;
6. retain `CONFLICTED` or `INSUFFICIENT_EVIDENCE` until resolved;
7. prevent the conflicted claim from supporting promotion or public release.

Newer is not automatically authoritative. More detailed is not automatically correct.

## 12. Correction loop

```text
DERIVE
  -> PROVE
  -> FIND GAP OR INVALID TEST
  -> D17 RESOLVE
  -> RE-DERIVE AFFECTED OUTPUT
  -> RE-PROVE AFFECTED AND REGRESSION CRITERIA
  -> DISPOSITION
```

The loop terminates when:

- all blocking criteria are proven;
- a valid failure requires correction outside current authority;
- evidence remains insufficient after authorized retrieval;
- the affected scope is isolated;
- DCS changes or ends the objective.

Repeated execution without new evidence, correction, or changed conditions is prohibited.

## 13. Resolution-first and non-stoppage

When backward proof identifies a gap, D02 routes it to D17 Resolve and D01 next-state planning. The executor corrects and retests within authority before escalating.

Missing noncritical proof does not block independent criteria. Missing blocking proof prevents the applicable PASS or promotion-ready state but does not erase completed evidence.

D21 controls the Stop-Gate. D02 records the failed or unproven condition and affected scope.

## 14. DART integration

| DART phase | D02 contribution |
| --- | --- |
| Define | Converts objective and intended use into requirements and proof criteria. |
| Assess | Builds source, derivation, dependency, risk, and evidence graphs. |
| Resolve | Identifies the exact failed node and affected derivation path. |
| Test | Performs backward proof and returns criterion states for final disposition. |

D02 does not independently promote, deploy, publish, or approve an artifact.

## 15. Workflow and product use

D02 can compile any governed workflow into:

- stage prerequisites;
- executable dependencies;
- tool and capability requirements;
- required doctrines;
- input and output contracts;
- acceptance criteria;
- evidence and receipt requirements;
- rollback and recovery conditions.

This supports employment workflows, product builds, websites, content, campaigns, media pipelines, database changes, deployments, and governance without embedding provider-specific behavior in doctrine.

## 16. Proof receipt

```yaml
backward_proof_receipt:
  receipt_id: ""
  task_id: ""
  derivation_graph_ref: ""
  goal_proof_ref: ""
  backward_graph_ref: ""
  criterion_results: []
  invalid_tests: []
  conflicts: []
  evidence_gaps: []
  corrections_applied: []
  regression_results: []
  rollback_or_recovery_results: []
  affected_scope: []
  result: "PROVEN | PARTIAL | FAILED | INSUFFICIENT_EVIDENCE"
  evidence_refs: []
  verified_at: ""
```

The receipt feeds D17 Test and D05 promotion readiness. It does not create a promotion state.

## 17. Runtime interfaces

```text
build_derivation_graph(task, sources, rules, requirements) -> DerivationGraph
execute_derivation_step(step, capability, authority) -> StepResult
compile_goal_proof(goal, criteria, evidence_rules) -> GoalProofContract
build_backward_proof(goal_proof, artifacts, tests) -> BackwardProofGraph
classify_test_validity(test_result, intended_control) -> ProofState
resolve_evidence_conflict(conflict, sources) -> ConflictDisposition
emit_backward_proof_receipt(graph, results) -> BackwardProofReceipt
```

## 18. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D02-001 | Output uses an unadmitted fact | Derivation gate fails. |
| D02-002 | Material decision lacks source or rule | Traceability finding is created. |
| D02-003 | Ordinary formatting choice lacks paragraph log | No failure is created. |
| D02-004 | Goal says production-ready | Observable blocking criteria are required. |
| D02-005 | Required dependency was skipped | Forward derivation remains incomplete. |
| D02-006 | Authorized action succeeds | Positive proof may pass within tested scope. |
| D02-007 | Unauthorized action is denied by intended policy | Negative proof may pass. |
| D02-008 | Unauthorized action fails from null violation first | Authorization test is INVALID_TEST. |
| D02-009 | Same source is copied three times | It counts as one provenance source. |
| D02-010 | Live state conflicts with an old receipt | Conflict is preserved and scoped by time and environment. |
| D02-011 | Newer source lacks authority | It does not silently supersede the controlling source. |
| D02-012 | Blocking criterion lacks evidence | Final proof is INSUFFICIENT_EVIDENCE. |
| D02-013 | Nonblocking criterion fails | Proven independent criteria remain preserved. |
| D02-014 | Correction changes shared behavior | Regression proof is required. |
| D02-015 | Rollback claim lacks restore test | Recovery criterion is not PROVEN. |
| D02-016 | Repeated loop has no new evidence | Loop terminates and records unresolved state. |
| D02-017 | Protected input enters general graph | Input is excluded and isolated before derivation. |
| D02-018 | Provider changes | Workflow graph remains provider-neutral and D03 remaps capability. |
| D02-019 | D02 source is unavailable | Only proof-dependent final claims are isolated. |
| D02-020 | All blocking criteria pass | Receipt returns PROVEN for D17 disposition analysis. |

## 19. Cross-doctrine boundaries

- D01 governs next-state reasoning and resolution paths.
- D03 assigns capability and fallback.
- D05 governs promotion and rollback authority.
- D15 supplies database proof requirements.
- D17 governs Define, Assess, Resolve, and Test dispositions.
- D20 supplies product acceptance requirements.
- D21 selects doctrine, controls isolation, and records execution.
- D22 supplies canonical source and reconciliation identity.

## 20. Source correction record

| Source condition | RC3 correction | Reason |
| --- | --- | --- |
| Content-generation examples treated as universal | Provider-neutral derivation graph | Supports all artifact and workflow classes. |
| Paragraph-level rule logging | Material-decision traceability | Preserves auditability without private reasoning disclosure. |
| Fixed resume formatting checks | Goal-specific acceptance contract | Removes stale domain assumptions. |
| Any unproven condition rejects entire document | Criterion-level proof and affected scope | Preserves valid work and non-stoppage. |
| No invalid-test state | Explicit INVALID_TEST classification | Prevents false authorization and security passes. |
| No correction loop | D17 Resolve and targeted reproof | Makes quality assurance operational. |
| Blanket halt on missing doctrine | Proof-dependent isolation | Preserves unrelated safe execution. |
| Fixed local file links | Repository-relative identities | Supports portable v7.1 execution. |

## 21. Candidate status

This candidate is correction evidence only. It does not replace the active D02 or prove, approve, promote, deploy, or publish any governed artifact until DCS promotes the exact candidate or exact diff and D22 records the authoritative representation.
