# DCS Employment RCHE Batch 3 Report

**Task ID:** DCSE-RCHE-20260909-EMP-HARVEST-001
**Status:** PARTIAL / UNSYNCHRONIZED
**Created:** 2026-09-09T09:08:20.147Z

## Scope

Batch 3 processed the verified Seed Corpus v0 plus clearly Employment-lane local support files. Raw sources were not modified. Canonical DCSE v7.2 R5 verification remains pending, so all authority-sensitive outputs remain UNSYNCHRONIZED.

## Results

- Source count: 12
- Processed source count: 9
- RAG chunks: 37
- Facts: 9
- Characteristics: 18
- Patterns: 7
- Rule candidates evaluated: 25
- Tested candidates: 21
- Conflicted candidates: 9
- Duplicate candidates: 0
- Rejected candidates: 3
- Seed-rule recovery: 15/15
- PS leakage result: EXCLUDED_REVIEW_REQUIRED
- Secret leakage result: PASS_NONE_DETECTED
- Regression result: NO_MATERIAL_REGRESSION

## Candidate Handling

No candidate was promoted to Approved or Active. Tested status here means RCHE technical admission passed for candidate-corpus use only.

Conflict-bearing candidates remain candidate records with preserved conflict references. They cannot be promoted without DCS or canonical governance review.

## Rules Tested

- EMP-RULE-001: TESTED - Inventory and classify employment sources before artifact creation; exclude PS-locked and secret
- EMP-RULE-002: TESTED - Map target requirements to verified DCS ingredients, identify gaps, remove unsupported claims, a
- EMP-RULE-003: TESTED - Classify substantive claims as Verified, Likely, Unknown, or Remove; restrain Likely claims and 
- EMP-RULE-004: TESTED - Use verified exact keywords and safe synonyms naturally; avoid keyword stuffing and audit false-
- EMP-RULE-005: TESTED - Employment writing should be direct, measured, senior, selective, substantive, human, technicall
- EMP-RULE-006: TESTED - Recruiter and employment communications must identify audience and objective, extract the ask, a
- EMP-RULE-007: TESTED - Adapt format, tone, structure, and density to the destination without changing verified substanc
- EMP-RULE-008: TESTED - PS-locked content may not enter Employment artifacts; material PS content triggers a governance 
- EMP-RULE-009: REJECT - Employment packages are named, versioned, destination-specific, indexed, and include exclusions,
- EMP-RULE-010: TESTED - Completion status must reflect actual sources processed, skipped items, blockers, validations, a
- EMP-RULE-011: TESTED - Classify an opportunity before producing application artifacts and evaluate compensation, work m
- EMP-RULE-012: TESTED - Do not create disjointed resume variants with conflicting professional identities; preserve the 
- EMP-RULE-013: TESTED - Do not use em or en dashes in governed DCS Employment prose; use plain hyphens for date ranges u
- EMP-RULE-014: TESTED - Named technologies, cloud services, AI capabilities, certifications, metrics, rates, responsibil
- EMP-RULE-015: TESTED - Preserve submission provenance across source, recruiter/vendor, end client when known, package, 
- EMP-RULE-016: TESTED - Every DCS correction should be evaluated as a possible reusable rule, preference, exception, or 
- EMP-RULE-017: TESTED - Recruiter-channel opportunities should track whether client submission was actually confirmed wh
- EMP-RULE-018: TESTED - Opportunity prioritization should account for tailoring effort and submission-channel risk, not 
- EMP-RULE-019: TESTED - Rate recommendations must distinguish remote-only from travel/onsite all-inclusive economics and
- EMP-RULE-020: TESTED - Resume length is destination-driven; direct applications may justify longer evidence-rich versio
- EMP-RULE-021: TESTED - AI should be positioned as a component of rule authoring, governance, gap analysis, evidence rev
- EMP-RULE-022: TESTED - Employment lifecycle should continue through offer evaluation, pre-start, personalized onboardin
- EMP-RULE-023: REJECT - Direct DCS employment pursuit remains DCS Employment; repeatable customer-facing employment plat
- EMP-RULE-024: REJECT - Closed, rejected, and unsuccessful opportunities remain harvestable for market, recruiter, fit, 
- EMP-RULE-025: CONFLICT - Builder and independent verifier should be separated for material Employment artifacts; model as
