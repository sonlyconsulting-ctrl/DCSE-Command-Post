# DCSE Doctrine D17: DART Universal Methodology

**Document ID:** DCSE-D17
**Version:** v6.9
**Created Date/Time:** 2026-07-25T21:30:00-04:00
**Last Doc Modified Date/Time:** 2026-07-25T21:30:00-04:00
**Status:** DCSE Authorized Pending DCS Approval
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D17_DART_Universal_Methodology.md
**Doctrine Description:** The DART Universal Methodology Doctrine (D17) defines the four-phase adversarial analysis framework (Discovery, Attack, Rebuttal, Trial) as a general-purpose analytical tool applicable to all entities and lanes. This is the methodology layer. The litigation-specific implementation remains in D13 and D14 (PS-locked).
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

## 1. DART as Universal Methodology

DART is a four-phase adversarial analysis framework. Each phase sharpens the output by forcing structured challenge, evidence validation, and stress-testing before delivery.

DART applies to any domain where a position must be defended, a claim must be substantiated, or a decision must survive scrutiny: employment strategy, product competitive analysis, brand positioning, recruiter negotiations, content validation, and architectural decisions.

The four phases are Discovery, Attack, Rebuttal, and Trial.

---

## 2. Phase Definitions (Non-PS Universal)

### 2.1 Discovery Phase

Objective: Gather, classify, and map all relevant evidence, data, and context before forming any position.

Universal rules:
- Identify all sources of truth for the domain (databases, documents, prior outputs, external data).
- Map stakeholders, decision-makers, and influencers.
- Catalog known facts separately from assumptions and inferences.
- Flag gaps where data is missing or unverified.
- Produce a Discovery Inventory listing every source, its reliability rating, and its relevance to the objective.

Domain applications:
- Employment: Map job requirements, company research, compensation benchmarks, cultural signals, contact chain.
- Product: Map competitive landscape, user needs, feature gaps, technical constraints, market timing.
- Brand/Content: Map audience segments, tone precedents, competitive messaging, channel requirements.
- Architecture: Map current state, dependencies, performance baselines, migration risks.

### 2.2 Attack Phase

Objective: Stress-test every claim, assumption, and deliverable by actively looking for weaknesses, contradictions, and failure modes.

Universal rules:
- For every claim in the deliverable, ask: "What evidence would disprove this?"
- Identify the strongest counterargument an adversary, competitor, or reviewer would raise.
- Flag unsupported assertions, circular reasoning, and assumptions presented as facts.
- Map vulnerabilities: single points of failure, unvalidated dependencies, untested edge cases.
- Produce an Attack Register listing each vulnerability, its severity, and the evidence that exposed it.

Domain applications:
- Employment: What would a hiring manager challenge on this resume? What gaps does a recruiter see? Where is the positioning weakest?
- Product: Where does the competitor win? What feature claim is unsupported? What user scenario breaks the design?
- Brand/Content: What claim would a skeptical audience reject? Where is the tone inconsistent? What message could backfire?
- Architecture: What fails under 10x load? What dependency is unmaintained? What migration step is irreversible?

### 2.3 Rebuttal Phase

Objective: Build pre-emptive defenses for every identified vulnerability. Strengthen the position before it faces external challenge.

Universal rules:
- For each item in the Attack Register, produce a specific, evidence-backed counterpoint.
- Do not dismiss vulnerabilities — address them with data, precedent, or structural mitigation.
- Where a vulnerability cannot be rebutted, acknowledge it and propose a mitigation strategy.
- Incorporate rebuttals directly into the deliverable so the final output is pre-hardened.
- Produce a Rebuttal Matrix mapping each attack to its defense and the evidence supporting it.

Domain applications:
- Employment: Preempt resume gaps with narrative positioning. Address job-hop concerns before the interviewer raises them. Counter comp objections with market data.
- Product: Address known UX weaknesses in release notes. Pre-position against competitive claims. Document known limitations with roadmap context.
- Brand/Content: Anticipate audience objections and address them in the copy. Include proof points for every major claim.
- Architecture: Document tradeoff rationale. Pre-answer "why not X?" for every major decision. Include rollback plans.

### 2.4 Trial Phase

Objective: Final validation and delivery. The output must survive presentation to its toughest audience.

Universal rules:
- Review the final deliverable as if presenting to an adversarial panel (hiring manager, competitor, skeptical stakeholder, code reviewer).
- Verify every fact traces to a documented source.
- Verify every claim has survived the Attack and Rebuttal cycle.
- Strip unsupported assertions that did not survive rebuttal.
- Produce the final deliverable with a Confidence Rating (High, Moderate, Conditional) and a list of any unresolved items.

Domain applications:
- Employment: Final resume, cover letter, or recruiter response is interview-ready. Mock questions answered. Comp positioning validated.
- Product: Feature is demo-ready. Edge cases tested. Release notes accurate.
- Brand/Content: Content is publish-ready. Claims verified. Tone consistent.
- Architecture: Design is review-ready. ADRs complete. Rollback tested.

---

## 3. DART Trigger Mechanism

DART mode activates when ANY of these conditions are met:

### 3.1 Explicit Triggers (User-Initiated)
- User says "apply DART," "run DART," "DART this," or "use the DART framework."
- User invokes a skill that requires DART (e.g., dcse-resume-align, dcse-recruiter-response, dcse-role-intake).
- User declares PS mode (triggers D13/D14 litigation DART, not this universal version).

### 3.2 Implicit Triggers (Auto-Detected)
- The task involves defending a position against scrutiny (resume targeting, competitive response, architectural decision record).
- The task involves evaluating credibility or legitimacy (job posting scam check, vendor evaluation, source verification).
- The task involves adversarial preparation (interview prep, negotiation strategy, competitive analysis).
- The task involves claim validation (marketing copy, product claims, compliance assertions).

### 3.3 Trigger Announcement
When DART activates, the model must announce:
"DART Universal activated. Running Discovery > Attack > Rebuttal > Trial."
This makes the methodology visible and auditable.

### 3.4 PS Escalation Gate
If during any DART phase the content touches Pro Se litigation, case law, court filings, or Case No. 8:23CV489, the model must:
1. HALT universal DART processing.
2. Announce "PS escalation detected. Switching to DART PS-Applied (D13/D14)."
3. Verify PS mode is authorized for this session.
4. If not authorized, flag as a firewall violation and stop.

---

## 4. DART Quality Gates (Universal)

Every DART-processed output must clear these 5 universal quality gates:

1. **Source Tracing**: Every factual claim traces to a named source.
2. **Attack Survival**: Every major assertion has been challenged and either rebutted or flagged as conditional.
3. **Consistency Check**: No internal contradictions between sections.
4. **Audience Calibration**: The output is tuned for its intended audience (hiring manager, customer, executive, developer).
5. **Confidence Declaration**: The output ends with a confidence rating and any unresolved items.

The 3 additional PS-specific quality gates (Bates validation, privilege log audit, legal authority validation) apply only when D13/D14 are loaded in PS mode.

---

## 5. DART Output Tag

All DART-processed outputs must include the tag:
"Processed under DART Universal Methodology — DCSE Proprietary"

PS-mode outputs use the separate tag:
"Powered by DART PS-Applied — DCSE Proprietary"

---

## 6. Tier Access

| Tier | DART Access |
|---|---|
| Tier 1 Sovereign | Full DART Universal + D13/D14 on PS demand |
| Tier 2 Internal Collaborator | DART Universal only. No D13/D14. No PS escalation. |
| Tier 3 External Product Build | DART Universal methodology description only (Section 2). No trigger mechanism, no quality gates, no PS references. |

---

## Related Doctrine

- D13_DART_Core.md — PS-specific litigation DART implementation (PS-Locked)
- D14_DART_PS_Protected.md — Case-specific parameters and blueprints (PS-Locked)
- D01_Forward_Thinking.md — Forward Thinking posture that feeds Discovery phase
- D02_Forward_Backward_Chaining.md — Chaining logic applied to DART quality gates

---

## Error-Catch Protocol

If this doctrine file is missing or unreadable, follow the canonical error-catch protocol:
1. HALT execution. Do not infer DART rules from pre-training.
2. LOG ERR_MISSING_DOCTRINE to Tribunal Inbox.
3. TRIGGER STOPGATE and alert the user.
