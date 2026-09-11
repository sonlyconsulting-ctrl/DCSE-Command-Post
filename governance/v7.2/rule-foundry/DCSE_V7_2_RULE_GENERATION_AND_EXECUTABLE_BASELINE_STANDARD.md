# DCSE v7.2 Rule Generation and Executable Baseline Standard

**Document ID:** DCSE-V72-RULE-FOUNDRY-STD-001  
**Version:** 1.0  
**Status:** CANDIDATE FOR v7.2 FINAL PROMOTION  
**Lane:** DCSE  
**Classification:** INTERNAL  
**Authority:** Operative R5 controller plus DCS direction dated 2026-09-11  
**Purpose:** Govern how DCSE discovers, creates, tests, promotes, executes, and revises reusable rules.

## 1. Governing Principle

AI may discover, infer, propose, challenge, and improve rules. DDNA may extract, aggregate, and rank candidate rules. Neither activity silently changes the active deterministic baseline.

Only a rule that passes this standard and reaches its governed lifecycle state may become an executable baseline.

## 2. Architecture

`SOURCE -> DISCOVER -> EXTRACT -> NORMALIZE -> TRACE -> CHALLENGE -> TEST -> PROMOTE -> EXECUTE -> OBSERVE -> REVISE`

The active baseline is immutable in place. New learning creates a new candidate version.

## 3. Rule Foundry Boundary

The Rule Foundry is the controlled meta-layer for generating all DCSE rule families. It is not recursively self-modifying.

The Foundry defines how rules are created. Rules created by the Foundry may not rewrite the Foundry or their own promotion controls without a separately authorized governance change.

## 4. Rule Sources

Candidate rules may originate from:

- DCS directives and decisions;
- promoted Master Profile and doctrine;
- validated workflows and SOPs;
- repeated DDNA patterns;
- product or campaign outcomes;
- defect and failure analysis;
- user corrections;
- model or human reviews;
- external standards when explicitly adopted;
- deterministic tests and runtime evidence.

Frequency is evidence of recurrence, not authority.

A single controlling directive may outweigh many repeated lower-authority observations.

## 5. Rule Classes

1. **Invariant:** must always hold.
2. **Decision Rule:** deterministic IF/THEN behavior.
3. **Constraint:** bounds available choices.
4. **Preference:** default behavior that may be overridden under its stated rule.
5. **Routing Rule:** selects an execution or destination path.
6. **Validation Rule:** determines pass/fail or required remediation.
7. **Calculation Rule:** deterministic numeric or formula output.
8. **Transformation Rule:** maps validated input to output.
9. **Generation Rule:** constrains AI-created content/artifacts.
10. **Scoring Rule:** produces finite-state or bounded scores from declared inputs.

## 6. Candidate Rule Contract

Every candidate must identify at minimum:

- rule ID and version;
- rule family and class;
- scope: lane, entity, product/process, artifact type, release posture;
- trigger;
- required inputs;
- condition;
- action;
- prohibition where applicable;
- exception/override conditions;
- expected output or state transition;
- authority source;
- provenance;
- confidence: Verified, Likely, Unknown;
- contradictions;
- severity;
- positive, negative, and boundary tests;
- deterministic evaluation method;
- lifecycle status.

## 7. Candidate Creation

A candidate may be created when any of the following is true:

- a controlling source states a reusable rule;
- a failure exposes a missing invariant or validation rule;
- three or more materially consistent DDNA observations indicate a repeatable pattern;
- a single high-authority DCS direction establishes the behavior;
- a reusable workflow contains a stable decision boundary.

The three-signal threshold is a discovery heuristic only. It does not create authority.

## 8. Normalization

Natural-language reasoning must be reduced to atomic rule behavior.

A normalized rule shall avoid combining unrelated decisions. If one sentence contains multiple triggers or outcomes, split it into multiple rule candidates unless they must execute transactionally.

Where possible, conditions and outputs should resolve to finite states such as:

- PASS / FAIL;
- ALLOW / DENY;
- REQUIRED / NOT_REQUIRED;
- MATCH / NO_MATCH;
- ROUTE_A / ROUTE_B;
- SCORE within a defined range.

## 9. Challenge

Before promotion, the validator must attempt to break the candidate through:

- counterexamples;
- contradictory authority;
- ambiguous input;
- missing input;
- boundary values;
- lane collision;
- PS/PPR leakage;
- secret exposure;
- public/internal collision;
- unintended override;
- circular rule dependency;
- model interpretation variance.

## 10. Testing

Every promoted deterministic rule requires executable or reproducible tests appropriate to its type:

- positive case expected to pass;
- negative case expected to fail;
- boundary case;
- exception case if exceptions exist;
- contradiction case when authority conflict is plausible.

AI-generated test cases may be used, but the expected result must be anchored to the rule contract.

## 11. Promotion

Candidate lifecycle:

`DRAFT -> CANDIDATE -> VALIDATING -> ELIGIBLE -> ACTIVE_BASELINE -> SUPERSEDED -> ARCHIVED`

`BLOCKED` and `DRIFT` may apply at any appropriate stage.

Promotion does not occur because a model produced the rule, a file was committed, a database row exists, or a test passed. Promotion state resolves through D05, D22, the operative controller, and applicable DCS directives.

## 12. Runtime Execution

Once promoted, the active rule baseline is read-only to ordinary runtime participants.

Runtime AI may:

- interpret context into declared input fields;
- propose an exception;
- identify ambiguity;
- request or retrieve missing source data;
- recommend a rule revision.

Runtime AI may not silently modify the baseline or reinterpret an invariant into its opposite.

## 13. Revision

Observed performance, DDNA, RAG retrieval, model disagreement, product metrics, or user correction may create a new candidate version.

The active version continues to control until the replacement version completes the governed lifecycle.

## 14. RAG Relationship

RAG is a learning and retrieval capability, not a mandatory control layer for every rule.

Use enough retrieval to become operationally useful:

- find relevant prior decisions;
- surface similar rules;
- recover product/design history;
- locate prior failures and validations;
- detect likely duplicates and contradictions.

Retrieved material remains subject to authority, lineage, lane, freshness, and confidence checks.

## 15. DDNA Relationship

DDNA is the macro learning layer. It captures reusable intelligence and pattern evidence.

DDNA SHALL NOT promote rules by recurrence. It produces candidate observations and provenance packets consumed by the Rule Foundry.

## 16. Deterministic Baseline Principle

DCSE intentionally separates:

- **dynamic intelligence:** interpretation, creativity, pattern discovery, challenge;
- **static control:** invariants, routing, required fields, lifecycle, validation, thresholds.

The design target is maximum useful AI intelligence inside stable executable guardrails.

## 17. Evidence

A promoted rule should be traceable to:

- canonical rule artifact;
- version and content identity;
- authority source;
- test evidence;
- contradiction review;
- promotion record;
- supersession relationship when applicable.

## 18. Exit Criteria

The Rule Foundry is operational when:

1. the rule schema validates;
2. the DDNA extraction profile can emit schema-ready candidates;
3. at least one real rule family is compiled into the schema;
4. tests distinguish pass/fail behavior;
5. active baselines cannot be silently mutated by extraction or generation;
6. GitHub contains canonical source and version history;
7. runtime registries reference rather than replace the canonical source.
