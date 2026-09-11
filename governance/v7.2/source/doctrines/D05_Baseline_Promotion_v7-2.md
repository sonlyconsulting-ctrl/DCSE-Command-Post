# DCSE Doctrine D05: Baseline and Promotion

**Document ID:** DCSE-D05  
**Version:** v7.2  
**Status:** CANDIDATE UPDATE FOR v7.2 FINAL PROMOTION  
**Classification:** INTERNAL  
**Lane:** DCSE  
**Parent Controller:** `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`  
**Canonical Path:** `governance/v7.2/source/doctrines/D05_Baseline_Promotion_v7-2.md`  
**Source Lineage:** prior D05 plus DCS Level 0 direction dated 2026-09-11

## 1. Purpose

D05 governs frozen baselines, validation integrity, promotion eligibility, ratification, supersession, drift, rollback, and promotion evidence.

A baseline is a frozen reference state. Promotion is an authority-state change. A GitHub commit, database row, deployment, Tribunal receipt, model conclusion, or passing test does not create promotion authority by existence.

## 2. Baseline Contract

A governed baseline records, as applicable:

- object/package identity and version;
- lane and classification;
- canonical repository/path or approved storage location;
- content SHA-256 or equivalent governed identity;
- repository commit/tag when applicable;
- included and excluded scope;
- validation performed;
- unresolved findings;
- dependent runtime/registry references;
- rollback or recovery reference;
- lifecycle state;
- authority/promotion receipt.

A baseline may cover a single artifact, package, repository state, runtime configuration, product, or governance set.

## 3. Lifecycle

```text
DRAFT -> CANDIDATE -> VALIDATING -> ELIGIBLE -> ACTIVE_RATIFIED
                    -> BLOCKED
ACTIVE_RATIFIED -> SUPERSEDED -> ARCHIVED
Any governed copy -> DRIFT when identity or required distribution no longer reconciles
```

ACTIVE_RATIFIED applies only to the exact promoted identity.

## 4. Promotion Authority

DCS Level 0 remains the sovereign source of constitutional and doctrine promotion authority.

Promotion may occur through either:

1. an exact DCS Level 0 decision for the artifact/version; or
2. an explicit standing or task-scoped DCS delegation that authorizes promotion when predetermined objective gates are satisfied.

A delegated executor does not create new promotion authority. It consumes the authority already granted by the controlling DCS decision.

Passing validation makes a candidate eligible under the applicable authority envelope. It does not independently create authority.

## 5. Task-Scoped Advancement

When DCS authorizes an outcome that inherently includes validation, remediation, reconciliation, and promotion processing, the authorized DCSE participant SHALL perform or orchestrate all non-reserved work necessary to reach the governed decision boundary.

The participant shall not repeatedly seek approval for steps already included in the authorized task.

Escalation is required only when:

- the governing objective must change;
- a reserved DCS decision is reached;
- an exception/waiver is required;
- actor separation is expressly required and no eligible separate actor is available;
- verified access or evidence is unavailable;
- a protected lane, secret, destructive action, public release, or materially new risk falls outside the existing authority envelope.

## 6. Validation Integrity and Independence

Independence and authority are distinct but coordinated controls.

### 6.1 Functional Independence

Unless a controlling source expressly requires actor separation, validation independence is satisfied by a functionally independent validation act using:

- frozen or version-identified candidate inputs;
- predefined or separately derived acceptance criteria;
- evidence re-performance or direct inspection;
- counterexample and contradiction testing;
- explicit findings;
- no silent candidate mutation during validation;
- attributable validator identity/function;
- durable validation receipt.

The same authorized participant may perform construction and a later functionally independent validation role when these controls are preserved.

### 6.2 Actor Separation

A different model, agent, or human validator is required only when expressly mandated by:

- DCS Level 0;
- law or regulation;
- contract;
- security policy;
- the controlling artifact;
- another higher-precedence promoted rule.

When actor separation is required, D21 routes the separate validator. The gate is not a passive stop if an authorized validator can be assigned.

### 6.3 Validation Diversity

Even when not mandatory, another model/agent/human may be used to improve assurance, adversarial diversity, or specialist coverage. Diversity is a quality technique, not an artificial authority barrier.

## 7. Promotion Eligibility

A candidate is eligible for promotion when, as applicable:

1. exact candidate identity is frozen;
2. source lineage and authority are resolved;
3. required validation is complete;
4. material contradictions are resolved or dispositioned;
5. security and lane checks pass;
6. tests/acceptance criteria pass;
7. canonical source/path and content identity are recorded;
8. runtime/registry reconciliation is complete or explicitly sequenced as post-promotion distribution;
9. rollback/recovery is defined;
10. the applicable DCS authority for advancement is identified.

No unresolved critical stop-gate may be concealed to force eligibility.

## 8. Promotion Receipt

A promotion receipt records:

- document/object ID;
- version;
- lane/classification;
- canonical path;
- exact content identity;
- repository commit/tag when applicable;
- validation receipt(s);
- promotion authority source;
- promoted by / executed by;
- effective timestamp;
- superseded identity when applicable;
- runtime/distribution reconciliation state;
- rollback path;
- final lifecycle state.

Where promotion executes under standing delegated authority, the receipt must identify that delegation.

## 9. Modification After Promotion

A material content change creates a new candidate unless a controlling rule defines an allowed non-material correction process.

The prior ACTIVE_RATIFIED identity remains controlling until the changed identity is promoted or expressly superseded.

No implied clerical exception exists.

## 10. Drift and Reconciliation

A mismatch among canonical GitHub, runtime registry, object storage, local audit copy, distribution mirror, or deployed artifact is DRIFT when those surfaces are required to match.

During DRIFT:

1. identify the last verified promoted identity;
2. preserve conflicting evidence;
3. compare source/version/hash;
4. correct the mismatched surface through D22;
5. validate the repaired state;
6. record reconciliation.

DRIFT does not allow a lower-authority copy to replace the canonical source.

## 11. Rollback and Recovery

Rollback identifies:

- prior promoted identity;
- affected systems;
- restoration steps;
- data recovery requirements;
- access/secret considerations;
- post-restore validation;
- evidence/receipt path.

Rollback is complete only when the restored state is verified.

## 12. No Passive Promotion Gate

An unmet promotion prerequisite is a routing condition when an authorized resolution path exists.

The executor SHALL identify the unmet prerequisite, resolve or route it, re-test, and continue until reaching either the authorized goal state or an irreducible reserved boundary.

PARTIAL or BLOCKED is appropriate only when required authority, access, evidence, protected separation, or execution capability is genuinely unavailable.

## 13. Related Doctrine

- D02: forward/backward chaining and contradiction review.
- D03: delegated independent authority and model routing.
- D21: runtime routing, DCL, evidence, and no-passive-gate execution.
- D22: canonical source, runtime distribution, and drift reconciliation.
- 2026-09-11 Bounded Independent Authority and Rule Foundry Direction.

## 14. Missing-Source Handling

If the operative D05 source is missing, unreadable, or conflicts with registered authority:

1. preserve available evidence;
2. classify source state through D22;
3. use the last verified controlling D05/R5 rule where determinable;
4. block only the affected promotion action if source authority cannot be resolved;
5. record the conflict in DCL/Tribunal evidence.

Do not infer a promotion decision from model memory or artifact presence.

## 15. Promotion Condition

This exact D05 revision is a candidate in the v7.2 final-promotion package. Its substantive authority derives from the operative R5 controller and the DCS Level 0 direction dated 2026-09-11. Canonical ACTIVE_RATIFIED identity must be evidenced through the final v7.2 promotion record.
