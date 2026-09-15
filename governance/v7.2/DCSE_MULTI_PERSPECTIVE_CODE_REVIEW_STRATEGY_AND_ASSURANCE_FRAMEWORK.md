# DCSE MULTI-PERSPECTIVE CODE REVIEW STRATEGY AND ASSURANCE FRAMEWORK

**Deliverable:** 4 of 4
**Artifact Class:** Reusable methodology — testing, compliance, objectives, output, and success criteria
**Intended Life:** durable across controller versions; written to survive v7.3, v8.x, and successor execution surfaces
**Derived From:** the measured difference between Pass 1 (deductive/backward/negative) and Pass 2 (inductive/forward/abductive) of the v7.2 R4 review
**Binds To:** D01 Forward Thinking · D02 Forward and Backward Chaining · D17 DART (DEFINE/ASSESS/RESOLVE/TEST) · MP-05 Evidence · MP-07 Stop-Gates
**Status:** proposed standard. Advisory until DCS adopts.

---

## PART I — WHY THIS EXISTS

### I.1 The measured case for multi-perspective review

The v7.2 R4 review ran twice over the same artifacts with inverted methods:

```text
Pass 1  deductive · backward-chained · negative-prompted · doctrine→code
        → 40 findings, 4 CRITICAL
        → every finding was a divergence from a rule that already existed

Pass 2  inductive · forward-chained · abductive · artifacts→doctrine
        + steelman, STRIDE, temporal, and economic lenses
        → 14 findings, 8 CRITICAL
        → 8 of 14 were ABSENT CATEGORIES: defects with no doctrinal vocabulary
        → 1 root cause explaining ~6 of Pass 1's findings
        → 5 corrections to Pass 1's own severity and priority
```

**The two highest-severity findings in the entire engagement (PS exfiltration via the DDNA harvester; total receipt repudiability) were invisible to Pass 1 and unreachable by its method.** Not missed through carelessness — unreachable. A review that asks "does the code match the doctrine?" cannot find a hazard the doctrine has no words for.

**Governing conclusion:** *single-perspective review has a structural blind spot equal in size to the vocabulary of the standard it reviews against.* One thorough pass is not one review; it is one lens.

### I.2 The one rule to keep if all else is discarded

> **A review is complete when it has been run from at least one perspective that could have falsified the previous perspective's conclusions — not when a checklist is exhausted.**

---

## PART II — THE PERSPECTIVE REGISTRY

Ten lenses. Each states what it *can* find, what it *structurally cannot*, and its trigger.

### P-01 Deductive / Conformance — *"Does the code implement the rule?"*
Trace each normative provision to its implementation. Produces a traceability matrix.
**Finds:** divergence, missing implementation, weakened implementation.
**Blind to:** hazards absent from the standard; whether the standard is right.
**Trigger:** always. This is the floor, never the ceiling.

### P-02 Inductive / Evidential — *"What do the artifacts imply about rules that should exist?"*
Read code, data, UI, logs, commit history **without the standard in hand**. Generalize upward.
**Finds:** absent categories, fabricated evidence, prototype residue, cultural patterns.
**Blind to:** subtle conformance gaps; deliberate design intent.
**Trigger:** always, and **before** re-reading the standard, so priors don't contaminate observation.

### P-03 Backward-Chained / Goal Proof — *"What must be true for the goal state to hold?"*
From goal → acceptance evidence → state → transition → component → dependency → **first unverified edge**.
**Finds:** the true blocker among many symptoms; correct repair order.
**Blind to:** hazards not on the path to the stated goal.
**Trigger:** any readiness or cutover assessment. (R4 §40 already mandates this — use it.)

### P-04 Forward-Chained / Consequence — *"Where does today's state lead?"*
Project current state forward through plausible sequences.
**Finds:** divergence trajectories, latent time bombs, incentive drift.
**Blind to:** static defects with no dynamics.
**Trigger:** any system with feedback loops or operator trust.

### P-05 Abductive / Root Cause — *"What single explanation accounts for all of this?"*
Enumerate competing hypotheses; score against **all** observations, not the convenient ones.
**Finds:** the root cause behind a scatter of symptoms; correct remediation altitude.
**Blind to:** genuinely independent defects — do not force a unifying story.
**Trigger:** more than five findings in one component.

### P-06 Negative / Adversarial — *"What does this permit that it did not intend to permit?"*
For each rule, construct the compliant-but-harmful behavior.
**Finds:** loopholes, fail-open paths, unstated preconditions.
**Blind to:** things the rule never addressed at all.
**Trigger:** every normative rule, without exception.

### P-07 Positive / Steelman — *"Assume it's right. What must be true?"*
Derive the design's unstated preconditions; test each.
**Finds:** missing tooling, absent roles, unstaffed processes, unbuilt instruments.
**Blind to:** defects in things that do exist.
**Trigger:** any specification that assumes a capability, actor, or instrument.
**Note:** this lens found "a compiled controller with no compiler" (I-09) — the highest-leverage finding of Pass 2. It is the most underused lens in practice and the most productive on specification-heavy systems.

### P-08 Threat Model (STRIDE) — *"Who benefits from breaking it?"*
Spoofing · Tampering · Repudiation · Information disclosure · DoS · Elevation.
**Finds:** the security class doctrinal review reliably misses — **especially repudiation**, which is invisible to functional review and existential for evidence-based systems.
**Blind to:** correctness and performance.
**Trigger:** any externally reachable surface; any surface producing evidence.

### P-09 Temporal — *"What does time do to this?"*
Staleness, cadence, TTL, deadlines, ordering, clock skew, operating rhythm vs. designed rhythm.
**Finds:** unverifiable freezes, reactive-only detection, deadlines without countdowns, doctrine calibrated to a rhythm the org doesn't practice.
**Blind to:** instantaneous correctness.
**Trigger:** anything with a hash, a freeze, a deadline, a schedule, or a poll.

### P-10 Economic / Incentive — *"What does compliance cost, and what will people actually do?"*
Price each control in operator effort. Compare the cost gradient to the safety gradient.
**Finds:** controls that will be routed around; why a defect pattern persists despite everyone agreeing it's wrong.
**Blind to:** technical defects.
**Trigger:** every governance control, before it is ratified.
**Rule:** *if the compliant path is more expensive than the non-compliant path, the control is decorative.* Price it before you ratify it.

### Non-traditional lenses, applied as warranted

- **P-11 Archaeological** — read the git history as behavioral data. Commit ratios, burst patterns, and abandoned directories reveal what the organization actually does versus what it documents. Produced Pass 2's root cause.
- **P-12 Semiotic** — what does the interface *assert* to an operator, independent of what it computes? A hardcoded `100` asserts perfect compliance. Fixtures assert measurement. Produced I-03/I-06.
- **P-13 Absence audit** — inventory what is conspicuously *not* present: no test runner, no linter, no compiler, no Stop-Gate UI, no validator roster. **Absence is the hardest defect class to see, because nothing on screen is wrong.**
- **P-14 Self-inversion** — re-review your own prior review with the opposing method. Produced five corrections to Pass 1, including a reordering of the entire remediation plan.

---

## PART III — REVIEW STRATEGIES (COMPOSED LENS SEQUENCES)

Lenses are not run à la carte. These are the standard compositions.

### S-1 Governed Surface Review — *for any R4 §6 mandatory surface*
`P-02 → P-01 → P-06 → P-08 → P-10 → P-03`
Observe before reading the standard; conform; adversarialize; threat-model; price; then prove the goal.
**Exit:** traceability matrix complete, zero unpriced controls, zero open STRIDE categories, backward proof reaching a verified root.

### S-2 Governance Artifact Review — *for doctrine, profiles, controllers*
`P-01(vs prior revision) → P-13 → P-07 → P-06 → P-09 → P-05`
Diff against the prior revision **first** — silent deletions are the dominant defect class in doctrine and are invisible when reading a revision standalone.
**Exit:** every delta ledgered; every assumed instrument confirmed to exist; every rule adversarialized.

### S-3 Evidence-Producing Component Review — *receipts, DDNA, telemetry, dashboards*
`P-12 → P-08(Repudiation first) → P-02 → P-04`
**Mandatory question:** *could this component produce a number that no measurement generated?* If yes, that is a CRITICAL until proven otherwise.
**Exit:** every displayed value traceable to a measurement event with provenance and timestamp.

### S-4 Second-Pass Inversion — *for any review whose conclusions will drive significant work*
`P-14 → the inverse of every lens used in pass 1 → P-05 → re-prioritize`
**Exit:** pass 1's severity ranking and remediation order explicitly re-confirmed or corrected.
**Applicability rule:** required whenever a review's output will drive more than ~two weeks of work, gate a cutover, or be represented as independent validation.

### S-5 Pre-Ratification Review — *before any new normative rule enters the corpus*
`P-10 → P-06 → P-07 → P-09`
Price it, break it, find its preconditions, age it. **Cheapest possible intervention** — four questions, minutes each, applied before a rule exists rather than after it has propagated.

---

## PART IV — TESTING ARCHITECTURE

### IV.1 The five test tiers, and the two that DCSE lacks

| Tier | Question | DCSE status |
|---|---|---|
| T1 Unit | does the function behave? | 5 orphan files, no runner |
| T2 Conformance | does the code implement the rule? | MP72-001..059 specified, none executable |
| T3 **Negative** | does the prohibited state remain unreachable? | **absent** |
| T4 **Evidence-integrity** | can the system produce a claim no measurement supports? | **absent** |
| T5 Adversarial | can an attacker reach a governed state? | absent |

**T3 and T4 are the tiers that matter most for this system and neither exists.** A governance system is defined by what it refuses and by the trustworthiness of its evidence — so its tests must be predominantly negative and integrity-focused. Positive tests confirm the happy path a demo already showed you.

### IV.2 Negative test construction (T3) — the standard pattern

For every rule of the form *"X SHALL NOT Y"*, write a test that **attempts Y and asserts refusal plus receipt**:

```text
GIVEN   a lane value not in the frozen registry
WHEN    dispatch is called
THEN    no task row is created
AND     response is 400 with LANE_MAPPING_STOP_GATE
AND     a MIGRATION_REQUIRED receipt exists with the legacy value
AND     no default lane was substituted        ← the assertion that catches fail-open
```

That last assertion is the one conventional testing omits and the one that would have caught F-15 years earlier. **Every negative test must assert the absence of a silent substitution, not merely the presence of an error.**

### IV.3 Evidence-integrity test construction (T4) — the pattern DCSE most needs

```text
GIVEN   a fresh client with cleared storage and an empty database
WHEN    every dashboard panel is rendered
THEN    no panel displays a numeric metric
AND     every metric region reads NOT MEASURED
```

This single test would have caught I-03, I-06, and the `73 QUEUED` literal simultaneously. Generalized:

> **T4 invariant — with no data in the system, the system must display no data.** Any number surviving an empty database is a fabrication.

Adopt this as a standing acceptance test on every control surface, forever. It is cheap, it never becomes obsolete, and it defends the property the whole architecture rests on.

### IV.4 Test authorship rule

Negative and evidence-integrity tests **SHALL NOT** be authored solely by the party that wrote the implementation. An implementer's negative tests test the failures they anticipated — which are, by definition, the ones they already handled. This is the testing analogue of R4 §25's executor/validator separation, and it should be stated as a rule rather than assumed.

---

## PART V — COMPLIANCE MODEL

### V.1 Compliance is a measured property, not a declared one

| Level | Meaning | Evidence required |
|---|---|---|
| L0 Asserted | someone says it complies | none — **carries no weight** |
| L1 Traced | a traceability matrix maps rule→implementation | matrix, reviewer identity |
| L2 Tested | conformance tests pass | test output, runner version, commit |
| L3 Negatively tested | prohibited states proven unreachable | negative test output |
| L4 Independently validated | a distinct party reproduced L2+L3 | validator receipt, distinct identity |
| L5 Continuously verified | re-runs on a cadence; drift alerts | scheduled runs, alert history |

**Current DCSE v7.2 state: L0 on nearly everything.** Named readiness states must carry a compliance level; `READY` at L0 means only that someone wrote the word.

**Rule:** *no artifact may be represented at a compliance level higher than its weakest constituent control.*

### V.2 Compliance drift — the four detectors

1. **Structural drift** — implementation diverges from doctrine → detector: T2 in CI on every PR.
2. **Evidentiary drift** — displayed claims outrun measurements → detector: T4 on every release.
3. **Temporal drift** — verified facts go stale → detector: `verified_at` + expiry on every hash and registry row.
4. **Behavioral drift** — operators route around expensive controls → detector: P-10 pricing review each cycle **plus** a usage metric per control. *A control with zero recorded uses in a period where it should have fired is either unnecessary or bypassed. Both require investigation.*

Detector 4 is the one almost no organization implements and the one that predicts the others.

---

## PART VI — OBJECTIVES, OUTPUT, AND SUCCESS CRITERIA

### VI.1 System objectives this framework serves

```text
O-1  No governed action occurs without traceable authority
O-2  No claim exists without a measurement behind it
O-3  No prohibited state is reachable through a permitted path
O-4  Every control is cheaper to comply with than to bypass
O-5  Every rule that exists is enforced by something executable
O-6  Every review can be falsified by a subsequent review
```

O-4 and O-6 are new; they are the two objectives the R4 corpus does not currently express, and they are the two that determine whether the other four survive contact with operators.

### VI.2 Required review output schema

Every review produced under this framework SHALL emit:

```json
{
  "review_id": "REV-YYYYMMDD-NN",
  "subject": {"artifact": "", "sha256": "", "commit": "", "surface": ""},
  "strategy": "S-1|S-2|S-3|S-4|S-5",
  "lenses_applied": ["P-01","P-02","..."],
  "lenses_deliberately_omitted": [{"lens":"","reason":""}],
  "reviewer": {"identity": "", "runtime_surface": "", "runtime_class": ""},
  "controller_version": "", "controller_hash": "",
  "findings": [{
    "id": "", "severity": "INFO|WARNING|ERROR|CRITICAL",
    "class": "conformance|absent_category|evidence_integrity|threat|temporal|economic|root_cause",
    "verification": "SOURCE-VERIFIED|RUNTIME-VERIFIED|INFERRED|UNKNOWN",
    "lens": "", "site": "", "failure_scenario": "",
    "required_correction": "", "changes_constitutional_meaning": false,
    "detecting_test": "", "disposition": "OPEN|ACCEPTED|REJECTED|DEFERRED"
  }],
  "root_causes": [], "corrections_to_prior_reviews": [],
  "facts_not_verifiable": [], "compliance_level_assessed": "L0..L5",
  "validator": null
}
```

Three fields carry unusual weight:

- **`lenses_deliberately_omitted`** — makes the blind spot explicit and reviewable. A review that omits P-08 on an internet-facing surface should be visibly incomplete, not silently so.
- **`detecting_test`** — **every finding must name the test that would have caught it, or state that no such test exists.** This converts a review into permanent regression coverage instead of a one-time document. It is the mechanism by which review effort compounds.
- **`corrections_to_prior_reviews`** — makes self-inversion auditable and normalizes correcting one's own prior work.

### VI.3 Success criteria for a review

A review is successful when **all** hold:

```text
SC-1  ≥2 lenses applied, at least one able to falsify another's conclusions
SC-2  every finding carries a failure scenario, not merely a rule citation
SC-3  every finding names a detecting test or declares its absence
SC-4  root-cause analysis attempted; symptoms not reported as independent defects
SC-5  omitted lenses declared with reasons
SC-6  prior-review corrections stated explicitly
SC-7  findings prioritized by LIVE RISK, not by ease of verification
SC-8  the compliance level of the subject is assessed, not assumed
```

**SC-7 exists because Pass 1 failed it.** It led with provability work while an active exfiltration path and total receipt repudiability went unfound. Verifiable is not the same as important, and reviewers systematically over-rank what they can easily prove.

### VI.4 Anti-criteria — how to recognize a failing review

```text
A-1  finding count presented as a quality measure
A-2  all findings at the same altitude (no root causes)
A-3  no finding contradicts a prior review or the reviewer's own priors
A-4  every finding is mechanically detectable (availability bias)
A-5  no absent categories found (the standard was the only lens)
A-6  severity correlates with ease of verification rather than consequence
A-7  reviewer validated their own findings
```

Pass 1 exhibited A-4, A-6, and partially A-2. Publishing these anti-criteria alongside the framework is deliberate: a methodology that cannot name its own failure modes is subject to them.

---

## PART VII — FORWARD-THINKING PROVISIONS

Written for a system that will keep evolving.

**FT-1 — Lens registry is extensible; strategies are versioned.** New lenses get `P-nn` identifiers under R4 §9 immutability. **A retired lens ID is never reused.**

**FT-2 — Every review names its execution surface and runtime class.** Reviews by different surfaces have different independence properties. An `INTERACTIVE_NON_CLAIMING` surface may produce review evidence but never validate its own findings. As surfaces multiply, this becomes the property that determines whether "independent validation" means anything.

**FT-3 — Model-agnostic by construction.** Nothing here depends on a vendor, model, or plan. When a surface changes, the lens registry does not. Vendor capability lives in a dated surface registry, never in methodology.

**FT-4 — Cross-model review as an independence mechanism.** Different model families exhibit different blind spots; routing Pass 1 and Pass 2 to different families is a cheap and real independence gain — but it is **not a substitute for method inversion**. Two models applying the same lens share that lens's blind spot. **Method diversity dominates model diversity.** Prefer one model running two inverted methods over two models running the same method.

**FT-5 — Review debt is tracked like technical debt.** Any lens skipped is recorded as debt against the artifact, with an owner and an expiry, and surfaces at the next readiness gate.

**FT-6 — Findings become tests; tests become the corpus.** Via `detecting_test`, review output ratchets into permanent coverage. **The long-term objective is that each review generation becomes structurally incapable of missing what the previous generation found.** That is the only mechanism by which assurance improves rather than merely repeating.

**FT-7 — Periodic full re-inversion.** At each controller major version, re-run S-4 against the accumulated corpus. Standards accrete blind spots as they accrete vocabulary; the inversion is what keeps the vocabulary from becoming the boundary of perception.

---

## PART VIII — MINIMUM VIABLE ADOPTION

If only three things are adopted from this document, adopt these:

1. **The T4 empty-database invariant** — with no data, display no data. One test; defends the system's foundational property; would have caught three CRITICALs.
2. **P-10 pricing before ratification** — four questions before any new rule enters the corpus. Prevents the cost-gradient inversion (I-15) that generates the 17:1 doctrine-to-code ratio.
3. **S-4 second-pass inversion on anything that gates a cutover** — the measured yield was 8 absent categories and 5 corrections to the first pass, including a full reordering of remediation priority.

Everything else in this framework is refinement. These three are load-bearing.

---

**Proposed standard, advisory until DCS adopts. Prepared as `INTERACTIVE_REVIEW` evidence; designates nothing.**
