# DCSE DDNA Rule Extraction Profile v1

**Document ID:** DCSE-DDNA-RULE-EXTRACT-001  
**Version:** 1.0  
**Status:** CANDIDATE  
**Parent:** DCSE v7.2 Rule Generation and Executable Baseline Standard  
**Purpose:** Convert DDNA learning into rule candidates without allowing DDNA to become an authority or self-modifying rules engine.

## 1. Processing Modes

### Mode A: Deterministic Capture

Use deterministic/local parsing where feasible to capture:

- explicit IF/THEN statements;
- MUST / SHALL / NEVER / REQUIRED / ONLY patterns;
- state transitions;
- thresholds;
- named triggers;
- required fields;
- prohibitions;
- exception language;
- repeated workflow sequences;
- explicit DCS corrections.

This mode preserves source text, location, timestamp, lane, and source identity.

### Mode B: AI-Assisted Rule Mining

AI may infer candidate rules from:

- multiple consistent observations;
- recurring failures;
- repeated user corrections;
- stable workflow behavior;
- product/campaign outcomes;
- design and technical patterns.

Every inferred rule must remain labeled `Likely` or `Unknown` until its source basis supports `Verified`.

## 2. Input Classes

- conversations;
- doctrine and directives;
- Tribunal decisions;
- product/campaign artifacts;
- workflow logs;
- QA findings;
- metrics and outcomes;
- model handoffs;
- DDNA signal arrays;
- RAG-retrieved source packets.

## 3. Rule Candidate Atom

For every candidate, extract:

1. proposed rule statement;
2. rule class;
3. lane/entity scope;
4. artifact/process scope;
5. trigger;
6. input fields;
7. condition;
8. action/result;
9. prohibition;
10. exceptions;
11. authority source;
12. provenance;
13. confidence;
14. contradiction set;
15. proposed tests;
16. observed recurrence;
17. proposed severity.

## 4. Candidate Creation Threshold

Create a candidate when:

- one explicit controlling source establishes the behavior; OR
- three materially consistent DDNA observations indicate a reusable pattern; OR
- one material failure/correction reveals a missing safety or integrity rule.

Recurrence affects candidate priority, not authority.

## 5. Five-Layer Mapping

The existing DDNA layers remain useful:

- **sentiment:** prioritization and tone evidence only;
- **logic:** primary source for workflow, decision, authority, and validation candidates;
- **design:** visual, typography, composition, interaction candidates;
- **product:** offer, assembly, packaging, release, and customer-facing candidates;
- **technical:** code, database, security, integration, performance, and runtime candidates.

Logic and controlling source status govern authority-sensitive candidate interpretation. Sentiment cannot promote, publish, deploy, migrate, delete, or override evidence.

## 6. RAG Use

RAG may retrieve:

- prior decisions;
- similar rules;
- product history;
- brand/design examples;
- prior failures;
- accepted/rejected artifacts;
- campaign outcomes.

RAG results are discovery evidence. Every retrieved item must be checked for lane, version, authority, freshness, promotion state, and contradictions before becoming candidate provenance.

## 7. Duplicate and Collision Handling

Before issuing a new candidate:

1. search active rule IDs and semantic neighbors;
2. detect equivalent rules with different wording;
3. detect contradictory outcomes for overlapping scopes;
4. detect renamed entities/terms;
5. detect public/internal or PS/non-PS collisions.

Do not silently merge contradictory candidates.

## 8. Extraction Output

Output must conform to `DCSE_RULE_SCHEMA_v1.json` or produce a structured rejection explaining missing required fields.

Suggested candidate ID:

`<FAMILY>-<SCOPE>-<SERIAL>`

Example:

`CONTENT-PUBLIC-001`

## 9. Non-Authority Rule

DDNA signals, embeddings, retrieval rank, model consensus, recurrence counts, and fluent explanations do not create promotion authority.

## 10. Review Loop

`EXTRACT -> DEDUPLICATE -> AUTHORITY CHECK -> NORMALIZE -> CHALLENGE -> TEST -> ELIGIBILITY`

Rejected candidates remain evidence for later learning but do not enter runtime enforcement.

## 11. Minimum Implementation for Current Product Sprint

For CTJ, Vow N Go, TSL, B4L, X50, and Beauty:

- capture explicit product truths and constraints;
- mine repeated content/design rules;
- extract channel and artifact requirements;
- preserve brand/entity distinctions;
- generate candidate rules only where reusable across more than one artifact or where a controlling source requires invariance.

Full enterprise RAG is not required. Targeted retrieval of relevant product, brand, audience, and prior-artifact context is sufficient for the current sprint.
