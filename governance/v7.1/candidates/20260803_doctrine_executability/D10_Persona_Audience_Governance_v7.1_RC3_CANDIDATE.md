# DCSE Doctrine D10: Persona and Audience Governance v7.1 RC3 Candidate

**Document ID:** DCSE-D10-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to privacy, consent, entity, and product scope  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D10_Persona_Assets.md`  
**Source SHA-256:** `10b65c20f9f1346262dc44beca4d4644c5849cc1768f9ab8cf32894cdf31cfe6`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until exact DCS promotion and D22 reconciliation.  

## 1. Purpose

D10 governs research-backed audience segments, user archetypes, accessibility profiles, stakeholder profiles, and approved fictional or consented personas used for product, content, campaign, service, and experience decisions.

D10 replaces hardcoded descriptions of identifiable acquaintances with privacy-preserving, evidence-based profiles. A persona is a design instrument, not a claim about a real person's identity, behavior, health, finances, beliefs, competence, or future actions.

## 2. Governing principles

1. Use the minimum personal detail needed for the decision.
2. Prefer aggregated segments and behavioral needs over named individuals.
3. Do not infer sensitive traits without lawful, authorized, and documented basis.
4. A persona never grants consent, access, or authority.
5. Accessibility needs are requirements, not stereotypes.
6. Research evidence and assumptions remain separate.
7. Personas are versioned, testable, and retireable.
8. A single anecdote does not define a market segment.
9. Segment adaptation must not manipulate, exclude, discriminate, or exploit vulnerability.
10. Public assets must not expose internal individual references or private persona evidence.

## 3. Profile classes

| Class | Purpose |
| --- | --- |
| Audience segment | Aggregated needs, behaviors, constraints, and channels. |
| User archetype | Representative task, goal, environment, and capability pattern. |
| Accessibility profile | Interaction requirements used for inclusive testing. |
| Stakeholder profile | Decision, influence, information, and approval needs. |
| Fictional persona | Named fictional aid with no real-person claim. |
| Consented individual profile | Explicitly authorized limited use with retention and access controls. |

## 4. Persona record

```yaml
persona_profile:
  persona_id: ""
  profile_class: ""
  entity: ""
  product_or_workflow: ""
  display_label: ""
  fictional: true
  consent_ref: ""
  goals: []
  tasks: []
  barriers: []
  contexts: []
  channels: []
  device_and_connectivity_constraints: []
  accessibility_needs: []
  content_needs: []
  trust_and_privacy_needs: []
  evidence_refs: []
  assumptions: []
  prohibited_inferences: []
  retention_policy_ref: ""
  access_scope: []
  version: ""
  status: "CANDIDATE | ACTIVE | RETIRED"
```

## 5. Sensitive-data boundary

Sensitive persona data includes health, disability, finances, religion, political views, precise location, family relationships, minor status, employment hardship, legal matters, biometrics, identity masking, and other protected attributes.

Such data may be used only when:

- directly necessary for an authorized purpose;
- supported by consent or another approved basis;
- stored in an approved protected system;
- access is limited;
- retention and deletion are defined;
- the output does not expose the individual;
- D15 and D06 controls apply to storage and movement.

Public or general model prompts use de-identified requirements rather than personal histories.

## 6. Research and evidence

Persona evidence may include interviews, surveys, analytics, support themes, usability tests, market research, accessibility studies, and approved operational data.

Each evidence source records provenance, sample limitations, date, consent, permitted use, representativeness, and known bias. Model-generated persona details are assumptions until verified.

## 7. Anti-stereotype and fairness controls

Profiles must not assume capability, interest, purchasing power, technology literacy, motivation, trustworthiness, or content preference solely from age, race, gender, disability, income, religion, occupation, or family status.

Segmentation must be based on relevant goals, behaviors, context, constraints, and evidence. Findings are checked for exclusion, disparate experience, manipulative targeting, and inaccessible defaults.

## 8. Workflow integration

Personas may influence:

- requirement prioritization;
- task and journey maps;
- content depth and terminology;
- channel and device support;
- accessibility acceptance criteria;
- onboarding and recovery paths;
- notification preferences;
- trust, privacy, and consent explanations;
- usability test scenarios.

They may not silently override explicit user choices, product requirements, authority, security, or factual accuracy.

## 9. Audience test matrix

```yaml
audience_test:
  test_id: ""
  persona_ref: ""
  scenario: ""
  goal: ""
  starting_context: ""
  accessibility_requirements: []
  privacy_expectations: []
  success_criteria: []
  failure_conditions: []
  evidence_refs: []
  result: "PASS | FAIL | INSUFFICIENT_EVIDENCE"
```

A persona-based test supplements, but does not replace, testing with actual users when the acceptance plan requires it.

## 10. Change and retirement

Profiles are reviewed when research, product scope, audience, regulation, accessibility requirements, or observed behavior changes. Conflicting evidence updates assumptions rather than being discarded.

Retired profiles preserve lineage and affected artifact references. Real-person consent withdrawal triggers the applicable deletion, de-identification, and downstream reconciliation process.

## 11. Validation receipt

```yaml
persona_validation_receipt:
  receipt_id: ""
  profile_ref: ""
  purpose_result: ""
  evidence_result: ""
  consent_result: ""
  minimization_result: ""
  fairness_result: ""
  accessibility_result: ""
  public_exposure_result: ""
  findings: []
  disposition: "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE"
```

## 12. Runtime interfaces

```text
resolve_audience_profile(entity, product, objective) -> PersonaProfiles
admit_persona_evidence(source, purpose) -> EvidenceAdmission
generate_persona_candidate(evidence, constraints) -> PersonaCandidate
validate_persona(profile, evidence, privacy) -> PersonaValidationReceipt
compile_audience_tests(profile, requirements) -> AudienceTests
```

## 13. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D10-001 | Named acquaintance appears without consent | General persona use fails. |
| D10-002 | Fictional label resembles a real person | Identity risk is reviewed. |
| D10-003 | Segment assumes low literacy from age | Fairness test fails. |
| D10-004 | Accessibility need is evidence-backed | Requirement is preserved without stereotype. |
| D10-005 | Model invents income or belief | Detail remains prohibited or assumed, not fact. |
| D10-006 | Survey sample is small | Limitation remains attached to the profile. |
| D10-007 | Public asset exposes internal individual label | Validation fails. |
| D10-008 | Persona overrides explicit user preference | Test fails. |
| D10-009 | Sensitive data lacks retention rule | Profile fails admission. |
| D10-010 | Consent is withdrawn | Deletion or de-identification and reconciliation begin. |
| D10-011 | Product scope changes | Persona applicability is reviewed. |
| D10-012 | Persona test passes without real-user test required by plan | Final acceptance remains incomplete. |
| D10-013 | Segment receives worse recovery path | Disparate-experience finding is created. |
| D10-014 | One anecdote defines market size | Evidence result fails. |
| D10-015 | Research conflicts with assumption | Assumption is corrected or marked conflicted. |
| D10-016 | Protected data enters general prompt | Affected data is isolated. |
| D10-017 | D10 is unavailable | Persona-dependent decisions are isolated. |
| D10-018 | All controls pass | Receipt returns PASS without promotion. |

## 14. Source correction record

| Source condition | RC3 correction |
| --- | --- |
| Seventeen named or identifiable personal profiles | Aggregated, fictional, or consented registry profiles. |
| Sensitive personal descriptions | Data minimization, consent, access, and retention controls. |
| Traits treated as facts | Evidence and assumption separation. |
| No fairness or accessibility testing | Anti-stereotype and audience-test contracts. |
| Static list | Versioned lifecycle and retirement. |
| Blanket halt | Persona-dependent affected-action isolation. |

## 15. Candidate status

This candidate does not replace active D10 or authorize personal-data use, targeting, publication, or promotion until exact DCS promotion and D22 reconciliation.
