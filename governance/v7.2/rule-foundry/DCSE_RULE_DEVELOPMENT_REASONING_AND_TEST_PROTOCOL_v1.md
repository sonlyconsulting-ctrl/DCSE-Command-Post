# DCSE Rule Development Reasoning and Test Protocol v1

**Document ID:** DCSE-RULE-REASON-TEST-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-11  
**Parent:** DCSE v7.2 Rule Foundry  
**Applies To:** all new or revised DCSE rule families  
**Status:** CANDIDATE FOR CANONICAL v7.2 INTEGRATION

## 1. Purpose

Require every material rule set to be developed through both constructive and adversarial reasoning.

The method combines:

- forward chaining;
- backward chaining;
- deductive reasoning;
- inductive reasoning;
- contradiction review;
- counterexample testing;
- boundary testing;
- exception testing.

No single reasoning mode is sufficient by itself.

## 2. Core Development Loop

`TARGET -> SOURCES -> FACTS -> CANDIDATES -> DEDUCTIVE CHECK -> INDUCTIVE CHECK -> NORMALIZE -> CHALLENGE -> TEST -> BACKWARD PROOF -> RECONCILE -> ELIGIBILITY`

## 3. Forward Chaining

Use forward chaining to derive candidate behavior from verified antecedents.

Sequence:

1. identify controlling sources;
2. extract atomic facts and explicit rules;
3. determine scope and trigger;
4. derive the action/result;
5. record the derivation path;
6. generate candidate tests from the derived behavior.

Forward chaining answers: **Given these verified facts and rules, what follows?**

## 4. Backward Chaining

Use backward chaining from the desired or prohibited target state.

Sequence:

1. define the target state;
2. identify conditions that must be true for that state to be valid;
3. identify evidence required for each condition;
4. identify missing or contradictory predicates;
5. identify rules required to prevent unsupported completion.

Backward chaining answers: **What must be proven for this result to be valid?**

Every promotion candidate SHALL survive both forward derivation and backward proof.

## 5. Deductive Reasoning

Deductive rules may be created when a controlling source explicitly establishes the behavior.

Pattern:

`CONTROLLING SOURCE + APPLICABLE FACTS -> REQUIRED RULE`

Deductive confidence may be `Verified` when source identity, scope, and authority are verified.

A deductive rule SHALL NOT silently broaden beyond the source scope.

## 6. Inductive Reasoning

Inductive reasoning may propose reusable rules from repeated observations, corrections, failures, outcomes, or successful patterns.

Pattern:

`OBSERVATIONS -> PATTERN -> CANDIDATE RULE`

Induction creates a candidate, not authority.

Recurrence increases priority and confidence in the pattern, but does not create promotion authority.

## 7. Rule Atomization

A rule SHOULD express one enforceable proposition.

If a rule contains multiple independent conditions with materially different outcomes, split it.

Decision-table rows may remain grouped when the table itself is the deterministic unit.

## 8. Required Challenge Questions

For every candidate ask:

1. What evidence would falsify this rule?
2. What valid case should pass that might accidentally fail?
3. What invalid case might accidentally pass?
4. What is the narrowest applicable scope?
5. What higher-authority rule could conflict?
6. What exception is legitimate?
7. What happens when an input is unknown?
8. Can the same normalized input produce different outputs?
9. Is the rule deterministic after the determinism boundary?
10. Is this really a rule, or only a preference?

## 9. Test Classes

Every material rule SHALL include:

### Positive
A valid input that must produce the intended pass/required result.

### Negative
An invalid input that must fail, hold, deny, or route.

### Boundary
An edge case at the threshold of applicability.

### Exception
A case where an authorized exception changes the normal result, if exceptions are allowed.

### Adversarial
A deliberately confusing or superficially compliant case designed to expose loopholes.

Adversarial tests may be stored in a separate matrix when the canonical rule schema does not yet include them directly.

## 10. Test Derivation

Tests SHALL be generated from both directions:

- **forward-derived tests:** prove known inputs produce the expected outcome;
- **backward-derived tests:** start from the desired final state and challenge each necessary predicate.

This prevents a rule from passing only the examples used to create it.

## 11. Contradiction Handling

When two candidate rules overlap and produce different outcomes:

1. preserve both;
2. identify authority and scope;
3. test whether the conflict is real or only apparent;
4. apply precedence;
5. narrow scope where appropriate;
6. do not silently average or merge contradictory outcomes.

## 12. Unknown Inputs

A deterministic rule SHALL define behavior for missing or unknown required inputs.

Allowed patterns include:

- `HOLD_FOR_REQUIRED_INPUT`;
- `NEEDS_REVIEW`;
- `ROUTE_TO_AUTHORITY_CHECK`;
- explicit safe default where authorized.

Guessing is not an allowed deterministic outcome.

## 13. Acceptance

A candidate is eligible for promotion only when:

- source/provenance is known;
- scope is explicit;
- authority is valid;
- contradiction review is complete;
- positive, negative, and boundary tests pass;
- exception tests pass where applicable;
- adversarial review exposes no unresolved material loophole;
- backward proof supports the claimed result;
- deterministic evaluation is reproducible;
- unresolved findings are disclosed.

## 14. DDNA Relationship

DDNA may supply inductive observations and candidate tests.

DDNA may also identify repeated failures that should become adversarial regression cases.

DDNA does not promote rules.

## 15. Rule Corpus Sequencing

Current rule-corpus sequence begins with Rule Set 5, Artifact and Content Generation.

Required later passes include Rule Sets 2, 3, 4 and cross-cutting sets 16 through 19 so the production corpus is eventually surrounded by lifecycle, lane, evidence, security, cost, reuse, and drift controls.

**Structure Precedes Scale.**
