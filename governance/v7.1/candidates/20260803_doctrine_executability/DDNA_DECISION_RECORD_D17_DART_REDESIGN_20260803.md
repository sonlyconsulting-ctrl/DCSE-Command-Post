# DDNA Decision Record: D17 DART Redesign

**Artifact ID:** DCSE-DDNA-D17-DART-REDESIGN-20260803  
**Status:** LEARNING CANDIDATE, NON-PROMOTING  
**Date:** 2026-08-03  
**Classification:** DCSE INTERNAL  
**Main theme:** Universal assurance methodology and doctrine orchestration  
**Source set:** DCS discussion, active D17 source, Master Profile RC3 candidate, D16 candidate, D21 candidate, and D22 candidate  
**Promotion effect:** NONE  
**Database mutation:** NONE  

## 1. Purpose

This record preserves the questions, decisions, rejected language, and downstream effects that produced the D17 RC3 candidate. It is a DDNA learning candidate, not promoted doctrine or an instruction to write to a database.

## 2. Verified source conditions

- The active D17 source is a v6.9 document imported into the v7.1 source tree on 2026-08-03.
- The supplied D17 and repository D17 have substantively identical content; their hashes differ because of line-ending representation.
- The source uses legal and adversarial phase names, narrow domain examples, fixed example skill names, a subjective audience test, general confidence ratings, mandatory conversational announcements, and global halt behavior.
- The Master Profile RC3 candidate currently classifies D17 as `PASS`, which is inconsistent with the source's descriptive and nonmechanical controls.
- D16 defines DDNA source admission, extraction, signals, candidates, deduplication, and feedback routing.
- D21 defines doctrine routing, run plans, consideration logs, affected-action isolation, and runtime contracts.
- D22 separates authority, canonical artifact, runtime reference, and distributed representations.

## 3. DCS decisions

1. D17 is a DCSE-wide methodology and must not use legal or protected-domain operating vocabulary.
2. DART remains the methodology name with phases Define, Assess, Resolve, and Test.
3. DART must support products, websites, applications, employment workflows, content, data, security, accessibility, media, architecture, operations, and governance.
4. The methodology must resolve correctable issues before escalating them.
5. The final result must use objective acceptance criteria and evidence, not a subjective toughest-audience standard.
6. General High, Moderate, or Conditional confidence ratings must not determine acceptance.
7. DART triggers must extend beyond counterpoints and claim review.
8. Trigger reliability must be governed through D21 metadata and a versioned catalog.
9. DART and DDNA must have distinct responsibilities, controlled sequencing, deduplication, and lane isolation.
10. Orchestration requires an early operating spine and a final reconciliation after all doctrine corrections.

## 4. Terminology decisions

| Legacy term | Approved term |
| --- | --- |
| Discovery | Define |
| Attack | Assess |
| Rebuttal | Resolve |
| Trial | Test |
| Adversarial methodology | Universal assurance and resolution methodology |
| Attack Register | Assessment Findings Register |
| Rebuttal Matrix | Resolution Matrix |
| Toughest audience | Authorized audience and declared acceptance criteria |
| Confidence Rating | Evidence coverage and objective disposition |

## 5. Objective dispositions

- PASS
- PASS_WITH_CORRECTIONS
- FAIL
- INSUFFICIENT_EVIDENCE

Confidence may be recorded only for a specific inference or probabilistic classification with supporting evidence, missing evidence, and effect if incorrect.

## 6. DART and DDNA operating relationship

```text
D21 route
  -> D16 source admission and extraction
  -> D17 Define, Assess, Resolve, Test
  -> D16 verified learning candidate
  -> D05 lifecycle decision
  -> D22 reconciliation and distribution
```

D16 owns signals and knowledge candidates. D17 owns assurance findings, resolutions, test evidence, and dispositions. Neither owns promotion.

## 7. Employment workflow implication

The local `DCS_Employment_Workflow` should be evaluated as a domain workflow package rather than presumed to be a doctrine. A future verified manifest should declare goals, stages, inputs, outputs, doctrines, capabilities, permissions, external-source rules, privacy, acceptance tests, evidence, and recovery behavior.

Provider-specific Gemini, Claude, ChatGPT, Qwen, script, and local-model implementations should use adapters to the same workflow contract.

The local folder was not accessible to the cloud review environment. No representation is made about its current contents.

## 8. Downstream reconciliation requirements

- Correct D01 so next-state reasoning supplies D17 Define and Resolve.
- Correct D02 so forward derivation and backward proof supply D17 Assess and Test.
- Correct D21 trigger and methodology interfaces.
- Change the Master Profile candidate's D17 status from `PASS` to `PARTIAL / REQUIRES_CORRECTION` until exact promotion.
- Preserve D03, D05, D16, D20, D21, and D22 authority boundaries.
- Compile the complete orchestration trigger and dependency graph after all doctrine candidates are finished.

## 9. Candidate disposition

`DDNA_LEARNING_CANDIDATE_CREATED_NOT_PROMOTED`

This record may inform doctrine correction and future DDNA processing. It must not be represented as stored, delivered, acknowledged, loaded, or promoted unless separate evidence proves each state.
