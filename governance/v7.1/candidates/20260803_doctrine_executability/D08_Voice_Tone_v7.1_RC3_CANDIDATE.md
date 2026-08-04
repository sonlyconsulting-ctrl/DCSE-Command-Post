# DCSE Doctrine D08: Voice and Tone v7.1 RC3 Candidate

**Document ID:** DCSE-D08-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to entity and artifact profile  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D08_Voice_Tone.md`  
**Source SHA-256:** `3561c2faf5765c977f0d41fb713f56f34bac00c530192fc5349b3f82e6389712`  
**DART dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D17_DART_Universal_Assurance_v7.1_RC3_CANDIDATE.md`  
**DART dependency SHA-256:** `568a8f2b3b2f8a960ebcf30dc94679dbb66f94a51aa2a51a0a0f86dc1da633f1`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until exact DCS promotion and D22 reconciliation.  

## 1. Purpose

D08 governs written, spoken, conversational, interface, notification, narration, and presentation voice. It preserves entity identity while adapting tone to audience, purpose, channel, urgency, accessibility, and evidence.

D08 does not define brand visuals, persona identity, product requirements, or media-production mechanics. It supplies voice controls to those doctrines.

## 2. Governing principles

1. Accuracy controls tone. Style must not overstate evidence or status.
2. Voice belongs to an entity and artifact, not to a model provider.
3. Tone adapts to context without changing authority or facts.
4. Public, customer, internal, operational, and protected communications remain distinct.
5. Trait-based voice direction replaces celebrity imitation or soundalike direction.
6. Accessibility includes clarity, reading level, pace, captions, transcripts, pronunciation, and cognitive load.
7. Cultural authenticity must not become stereotype, caricature, or unsupported identity performance.
8. User preference may override a default where authority, safety, accessibility, and brand constraints permit.
9. Fixed prose examples are reference samples, not mandatory wording.
10. Missing D08 isolates voice-dependent release, not unrelated technical work.

## 3. Voice profile registry

```yaml
voice_profile:
  profile_id: ""
  entity: ""
  lane: ""
  audience: ""
  channel: ""
  purpose: ""
  traits: []
  prohibited_traits: []
  formality: ""
  warmth: ""
  energy: ""
  directness: ""
  technical_density: ""
  reading_level_target: ""
  sentence_length_target: ""
  terminology_rules: []
  accessibility_rules: []
  pronunciation_guide_ref: ""
  brand_profile_ref: ""
  approved_examples: []
  authority_ref: ""
  version: ""
  status: "CANDIDATE | ACTIVE | RETIRED"
```

Profiles are versioned registry assets. Doctrine must not freeze every entity's evolving voice into permanent prose.

## 4. Entity and artifact separation

The applicable voice is selected from:

- controlling entity and product;
- artifact class;
- intended audience;
- public, customer, partner, internal, operational, or confidential channel;
- communication purpose;
- urgency and consequence;
- accessibility needs;
- approved campaign or persona profile.

A technical incident report may be concise and clinical while a customer explanation may be calm and educational. Neither may change the underlying facts.

## 5. Universal writing controls

- Lead with the verified outcome or current condition.
- Distinguish verified facts, supported conclusions, assumptions, and unknowns.
- Use concrete actions, owners, and completion conditions.
- Avoid filler, generic enthusiasm, manipulative urgency, invented certainty, and repetitive reassurance.
- Avoid jargon when plain language preserves precision.
- Define necessary specialized terms at the audience's level.
- Use active, attributable language for actions and decisions.
- Do not claim delivery, acceptance, promotion, deployment, security, or completion without evidence.
- Preserve required confidentiality, legal, safety, and product notices without stylizing them away.
- Use third-person brand posture where the applicable entity profile requires it.

Punctuation, capitalization, date, number, and trademark rules belong in the applicable style profile and artifact contract rather than being presumed universal across every language and channel.

## 6. Tone selection

```yaml
tone_selection:
  selection_id: ""
  task_id: ""
  voice_profile_ref: ""
  artifact_class: ""
  audience_profile_ref: ""
  channel: ""
  purpose: ""
  urgency: ""
  traits_applied: []
  accessibility_adjustments: []
  deviations: []
  deviation_authority_ref: ""
```

Tone may change within an artifact when sections have different functions. A warning, instruction, explanation, and call to action should not be forced into one emotional register.

## 7. Audio and synthesized voice

Audio profiles declare:

```yaml
audio_voice_profile:
  profile_id: ""
  source_type: "HUMAN | SYNTHETIC | HYBRID"
  consent_or_license_ref: ""
  trait_direction: []
  pace_range_wpm: ""
  pronunciation_guide_ref: ""
  emphasis_rules: []
  pause_rules: []
  language_and_locale: ""
  caption_required: true
  transcript_required: true
  disclosure_requirement: ""
  prohibited_similarity_refs: []
  provider_adapter_ref: ""
```

No output may request or claim a celebrity impersonation, soundalike, cloned voice, or identity simulation without verified rights and applicable consent. Conceptual influences must be translated into non-identifying traits.

Provider-specific settings such as stability, similarity, or style intensity belong in a versioned adapter. Doctrine controls the desired result and safety boundary.

## 8. Accessibility and comprehension

Applicable controls include:

- descriptive headings and logical information order;
- plain-language alternative for complex material;
- concise labels and actionable error text;
- avoidance of color-only, sound-only, or tone-only meaning;
- captions and transcripts for meaningful audio;
- pronunciation support for controlled names and terms;
- pace and pause appropriate to the audience;
- text alternatives for audio-only instructions;
- avoidance of flashing, startling, or manipulative notification language;
- localization review rather than literal word substitution.

Reading level is a target, not a reason to remove required precision.

## 9. Status, risk, and error language

Operational language must distinguish proposed, attempted, queued, dispatched, delivered, acknowledged, running, partial, failed, verified, promoted, deployed, and reconciled states.

Errors should state:

1. what occurred;
2. affected scope;
3. safe action available now;
4. whether data or work was preserved;
5. next automated or assigned action;
6. what evidence will confirm recovery.

Do not expose credentials, private identifiers, internal stack details, or protected content in user-facing errors.

## 10. DART assurance

D17 applies to material public, employment, customer, commercial, campaign, voiceover, and release artifacts.

- Define selects voice, audience, channel, and criteria.
- Assess checks accuracy, consistency, accessibility, cultural risk, and status claims.
- Resolve corrects drift and inappropriate language.
- Test verifies the artifact against the selected profile and intended use.

## 11. Voice validation receipt

```yaml
voice_validation_receipt:
  receipt_id: ""
  artifact_ref: ""
  voice_profile_ref: ""
  tone_selection_ref: ""
  factual_accuracy_result: ""
  entity_consistency_result: ""
  audience_fit_result: ""
  accessibility_result: ""
  status_accuracy_result: ""
  audio_rights_result: ""
  findings: []
  corrections: []
  disposition: "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE"
```

## 12. Runtime interfaces

```text
resolve_voice_profile(entity, artifact, audience, channel) -> VoiceProfile
select_tone(profile, purpose, context) -> ToneSelection
adapt_copy(content, selection) -> CandidateContent
validate_voice(content, profile, criteria) -> VoiceValidationReceipt
resolve_audio_profile(artifact, rights, locale) -> AudioVoiceProfile
```

## 13. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D08-001 | Model provider changes | Entity voice remains stable. |
| D08-002 | Evidence is uncertain | Tone does not claim certainty. |
| D08-003 | Public copy uses internal status language | Drift is detected and corrected. |
| D08-004 | Error message contains secret value | Validation fails and exposure response begins. |
| D08-005 | Voice direction names a celebrity soundalike | Direction is rejected and translated to traits. |
| D08-006 | Synthetic voice lacks rights or consent evidence | Release fails. |
| D08-007 | Meaningful audio lacks captions | Accessibility result fails. |
| D08-008 | Complex technical content targets a general audience | Plain-language support is required. |
| D08-009 | Tone profile conflicts with factual accuracy | Accuracy controls. |
| D08-010 | One artifact contains warning and invitation sections | Section-level tone may differ under one entity voice. |
| D08-011 | Cultural trait becomes stereotype | Finding blocks intended use until corrected. |
| D08-012 | Pronunciation is unverified | It remains unresolved rather than invented. |
| D08-013 | Queue insertion is described as delivery | Status-accuracy test fails. |
| D08-014 | User supplies an authorized tone preference | Preference is applied within constraints. |
| D08-015 | Localization uses literal translation only | Locale review remains incomplete. |
| D08-016 | Internal draft requires metadata | Public suppression rules do not remove draft evidence. |
| D08-017 | D08 is unavailable | Voice-dependent release is isolated. |
| D08-018 | All criteria pass | Receipt returns PASS without creating promotion. |

## 14. Source correction record

| Source condition | RC3 correction |
| --- | --- |
| Celebrity-based archetype | Trait-based voice profiles and anti-imitation controls. |
| Fixed lane prose | Versioned entity, artifact, audience, and channel profiles. |
| Fixed provider settings | Provider adapter with doctrine-level result criteria. |
| Narrow copy rules | Accuracy, accessibility, status, error, and localization controls. |
| Blanket halt | Voice-dependent affected-action isolation. |
| Fixed local links | Repository-relative identities. |

## 15. Candidate status

This candidate does not replace active D08 or authorize publication, synthesis, branding, or promotion until exact DCS promotion and D22 reconciliation.
