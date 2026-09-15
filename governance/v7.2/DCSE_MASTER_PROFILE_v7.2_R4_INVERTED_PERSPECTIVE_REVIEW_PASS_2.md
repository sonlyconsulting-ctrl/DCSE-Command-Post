# DCSE v7.2 R4 — INVERTED-PERSPECTIVE REVIEW (PASS 2)

**Deliverable:** 3 of 4
**Relationship to Pass 1:** deliberate methodological inversion. Pass 1 reasoned **deductively and backward** from doctrine to code, using negative prompting. Pass 2 reasons **inductively, forward, and abductively** from runtime artifacts and repository behavior upward — plus positive/steelman, fault-tree, threat-model, temporal, and economic lenses that Pass 1 did not apply.
**Purpose:** find the defects a top-down doctrinal review is structurally incapable of seeing.
**Status:** advisory `INTERACTIVE_REVIEW` evidence. Designates nothing.

---

## 0. WHY AN INVERTED PASS FINDS DIFFERENT THINGS

A deductive review asks *"does the code implement the doctrine?"* It can only find defects **the doctrine already has words for**. Every Pass 1 finding was, by construction, a place where reality diverged from a rule that already existed.

An inductive review asks the opposite: *"what does the observed behavior of this system imply about rules that ought to exist and don't?"* It finds **absent categories** — defects with no doctrinal vocabulary, which is precisely why they survive doctrinal review.

Pass 1 found 40 divergences from R4. **Pass 2 found one root cause that explains most of them, and five defect classes R4 has no words for at all.**

---

## 1. INDUCTIVE PASS — WHAT THE ARTIFACTS SAY WHEN YOU STOP READING THE DOCTRINE

### 1.1 Measured repository behavior (last 60 commits)

```text
Markdown files changed ....... 156
JavaScript files changed .....   9
ratio ........................ 17.3 : 1

Commit distribution: 31 commits on 2026-08-04; 5 on 08-03;
                     1-2/day thereafter. Burst-then-silence.
Root package.json ............ absent
Configured test runner ....... none
Test files present ........... 5 (nothing executes them)
```

**I-01 — ROOT CAUSE (CRITICAL): the system generates governance faster than it can implement or verify it.**

At 17:1, doctrine is being produced at seventeen times the rate of enforcement code. This is not a values judgment — governance artifacts are the product here. It is a **rate mismatch**, and it is the abductive best explanation for nearly every Pass 1 finding:

| Pass 1 finding | Explained by I-01 as… |
|---|---|
| F-01 manifest absent | specified in prose, never materialized |
| F-12 conflict ledger absent | specified, never built |
| F-19 linter absent | specified, never built |
| F-27 no test evidence | 55 tests specified, 0 executable |
| F-15 fail-open lane | code predates the doctrine that forbids it and was never revisited |
| F-03 test IDs redefined | fast doctrinal iteration without a change-control instrument |

Pass 1 reported these as six independent findings. **They are one finding with six symptoms.** Fixing them individually treats symptoms; the structural fix is a *rate limiter*: no new normative section may be added while a previously specified instrument (manifest, ledger, linter, test runner) remains unbuilt. Call it a **governance work-in-progress limit** — borrowed from lean manufacturing, absent from R4 entirely.

**Prediction (falsifiable):** if this ratio holds, R5 will add sections and tests while the ledger, linter, and manifest remain unbuilt, and a Pass 3 will find a longer version of this same list. Measure the ratio at R5 to test it.

### 1.2 The DDNA subsystem — inductive findings

Reading the DDNA implementation *without* reference to D16 or §37 produces findings a doctrinal review would never reach.

**I-02 (CRITICAL) — PS exfiltration path through the DDNA harvester.**
`runDDNAHarvest()` takes a pasted **agent session transcript**, embeds it in a prompt, and sends it to whichever model `modelSelect` names — including OpenAI and Gemini, via `handleChat`, with a client-supplied key.

One of the eight scored dimensions is `ps_firewall: "Personal/sensitive content exclusion (100=perfect, 0=breach)"`.

**The tool that measures PS firewall integrity is itself an unrestricted PS egress channel.** To score whether a session leaked PS material, an operator pastes that session — PS material included — into a third-party model. No lane check, no classification prompt, no sanitization, no warning. R4 §12 forbids PS material in enterprise-shared runtime context; this path is neither shared nor governed, so §12's words do not reach it. **The firewall has a measurement instrument that bypasses the firewall.**

This is the highest-severity finding in either pass, and Pass 1 could not have found it: Pass 1 traced doctrine→code through the dispatch path, and DDNA is not mentioned in R4's normative sections at all.

**I-03 (CRITICAL) — DDNA evidence is not evidence.**

```javascript
let ddnaScores = JSON.parse(localStorage.getItem('sc_ddna_scores')||'null')
  || {voice_fidelity:94, ps_firewall:100, gate_discipline:97, packet_integrity:99,
      schema_accuracy:96, dcs_alignment:100, instruction_fidelity:95, divergence_signal:72};
let ddnaNotes = JSON.parse(localStorage.getItem('sc_ddna_notes')||'[]');
```

Three compounding defects:

1. **The scores are hardcoded defaults.** A fresh browser displays `ps_firewall: 100`, `dcs_alignment: 100` — numbers no measurement produced. The dashboard asserts perfect firewall compliance to any observer, by default, forever.
2. **Persistence is `localStorage`.** DDNA scores and notes live in one browser profile. They are not in Supabase, carry no `task_id`, no `agent_key`, no `controller_hash`, no timestamp, no provenance. Clearing site data destroys the record. Two operators see different "truth."
3. **The `73 QUEUED` badge is a string literal** in the HTML, not a query. A queue depth is being displayed that no queue reports.

Under R4 §35 "Evidence outranks narrative," DDNA currently produces **narrative shaped like evidence** — the most dangerous possible artifact, because it is indistinguishable from measurement at a glance and it reads as reassuring.

**I-04 (ERROR) — the local-model path is broken in production.** `runDDNAHarvest` fetches `http://localhost:11434` directly from the page. On the HTTPS production domain this is mixed-content and browsers block it. The Ollama route works only when the dashboard is served over `http://localhost`. **The "local/private" DDNA path — the one that would avoid I-02 — is precisely the one that does not function in deployment**, which means every real production harvest necessarily routes to a cloud provider. I-02 is not a possibility; it is the default.

**I-05 (WARNING) — measurement is truncated and unversioned.** `input.slice(0,3000)` silently discards everything past 3,000 characters of a transcript. The scoring prompt is inline, unversioned, and unhashed. Two harvests of the same session under different prompt revisions are not comparable, and nothing records which revision produced a score. Any longitudinal DDNA trend is uninterpretable.

### 1.3 What the UI asserts vs. what the system knows

Inducting from the interface alone: the dashboard displays a DDNA queue depth, eight perfect-ish scores, a capability matrix reading `UNTESTED` in five rows, and a Tribunal panel backed by `const TRIBUNAL_PRS = [...]` — a hardcoded array.

**I-06 (ERROR) — the dashboard mixes live data and fixtures with no visual distinction.** Some panels query Supabase; others render literals. An operator cannot tell which is which. This is a **governed-evidence integrity defect**: the control surface for a system whose first principle is "evidence outranks narrative" presents fixtures indistinguishably from measurements. Every fixture must be badged `FIXTURE` / `NOT MEASURED` at minimum; ideally removed.

Note the capability matrix gets this *right* — five explicit `UNTESTED` tags. That is the correct pattern; apply it everywhere.

---

## 2. FORWARD-CHAINING PASS — WHERE DOES TODAY'S STATE LEAD?

Pass 1 chained backward from the goal. Pass 2 chains forward from the present.

```text
STATE: doctrine 17x ahead of code; instruments unbuilt; DDNA emits fixtures as evidence
  ↓
Operators trust the dashboard because it is the control surface
  ↓
Hardcoded 100s are read as measured firewall compliance
  ↓
Confidence in PS isolation rises while actual isolation is unmeasured
  ↓ AND, independently
DDNA harvests route session transcripts to cloud providers (I-02/I-04)
  ↓
Actual PS exposure rises as measured confidence rises
  ↓
DIVERGENCE: the two curves move in opposite directions, and
            nothing in the system can detect the gap
```

**I-07 (CRITICAL) — confidence and safety are diverging, and no instrument observes the divergence.** This is the characteristic failure signature of governance systems that fail catastrophically rather than gradually: the warning indicators are themselves fabricated, so the first true signal is the incident. R4 has no concept for it. The required primitive is a **liveness/provenance requirement on every displayed metric** — a metric with no measurement event behind it must render as absent, never as a number.

---

## 3. ABDUCTIVE PASS — BEST EXPLANATION FOR THE OBSERVED DEFECT PATTERN

Given: fail-open lane coercion, self-approval receipts, client-supplied API keys, no auth, localStorage evidence, hardcoded queue depths.

Competing hypotheses:

| Hypothesis | Fit |
|---|---|
| H1 Careless engineering | **Poor.** Status validation is rigorous, column mapping correct, 400-before-503 ordering deliberate. This is careful work. |
| H2 Security not valued | **Poor.** The governance corpus is obsessive about isolation and evidence. |
| H3 **The code was written as a demonstration surface and was later reclassified as a governed enforcement surface without being re-engineered** | **Strong.** Explains every anomaly at once: fixtures and hardcoded scores are demo affordances; client-supplied keys let a demo run without server config; permissive defaults keep a demo from dead-ending; localStorage avoids demo backend setup. |

**I-08 (CRITICAL) — R4 §6 designated Command Post a mandatory cutover surface; nothing re-engineered it from prototype to enforcement.** Under H3 the correct remediation is not a patch list — it is an explicit **prototype→production reclassification gate**: an inventory pass over every affordance that exists to make a demo work (fixtures, permissive defaults, client credentials, local persistence), each either removed or re-justified under production requirements, before the surface can be counted for MP72-040.

R4 has no such gate. Every mandatory surface it names is at risk of the same silent promotion. **This is a missing constitutional control, not a bug.**

---

## 4. POSITIVE / STEELMAN PASS — WHAT MUST BE TRUE FOR THE DESIGN TO BE SOUND?

Pass 1 asked what R4 wrongly permits. The inversion: assume the design is correct and derive its unstated preconditions. Each unmet precondition is a gap.

| Precondition the design silently assumes | Met? |
|---|---|
| Someone can execute the compiler described in §29 | **NO** — no compiler exists; all compilation is manual |
| Manual compilation is deterministic and repeatable | **NO** — no procedure, no operator instructions, no reproducibility check |
| The frozen inventory's 22 hashes can be re-derived on demand | **UNKNOWN** — no script, no source snapshot committed |
| An operator can tell whether a given packet was correctly compiled | **NO** — no packet inspector, no rule-set hash computation |
| Someone is available to act as independent validator | **UNKNOWN** — no validator roster exists |
| Stop-Gates surface somewhere an operator will see them | **NO** — no Stop-Gate UI, no alert path, no queue |
| Governance state can be reconciled across surfaces | **NO** — no reconciliation tool; §14 drift detection has no implementation |

**I-09 (CRITICAL) — R4 specifies a compiled controller with no compiler.** Every "the compiler SHALL…" in R4 (§2.3, §3, §8, §11.3, §20, §29) currently resolves to *a human doing it by hand, undocumented, unrepeatably*. This is the most consequential absent category in the corpus: a governance **compiler** that exists only as prose is a governance **style guide**. R4 never states this, so no test detects it and no finding in Pass 1 names it.

**I-10 (ERROR) — no Stop-Gate has a delivery path.** Twelve-plus Stop-Gates are specified. None has a defined surface where a human sees it, an owner, an SLA, or an escalation route. A Stop-Gate nobody is notified of is a silent halt — functionally identical to the fail-open behavior the document prohibits, with worse ergonomics.

---

## 5. THREAT-MODEL PASS (STRIDE) — A LENS PASS 1 DID NOT USE

Applied to the Command Post surface as an unauthenticated internet-facing control plane.

| Threat | Present? | Evidence |
|---|---|---|
| **S**poofing | **YES** | no auth; `actor_label` is caller-supplied free text; any caller can claim any identity in the evidence record |
| **T**ampering | **YES** | any caller can PATCH task status through `/receipt`, including to `approved` |
| **R**epudiation | **YES** | no authenticated actor, no signature, no immutability; every receipt is deniable |
| **I**nformation disclosure | **YES** | raw PostgREST errors relayed (C-10); DDNA transcripts to third parties (I-02) |
| **D**enial of service | **YES** | unauthenticated writes, unbounded task creation, no rate limit |
| **E**levation of privilege | **YES** | anonymous caller reaches `approved` — the highest authority state the API exposes |

**Six of six STRIDE categories are present on a surface R4 designates as mandatory for enforcement.**

**I-11 (CRITICAL) — repudiation is the one that matters most here.** The others are conventional security problems. Repudiation is an *existential* problem for this specific system: DCSE's entire premise is that receipts constitute evidence. A receipt that any anonymous party could have written, containing a self-declared actor label, is not evidence of anything. **Every receipt produced by this surface to date is unattributable.** R4 §25 legislates receipt *structure* and never once requires receipt *authenticity* — an absent category, not a violation.

---

## 6. TEMPORAL PASS — TIME AS A FIRST-CLASS DEFECT SOURCE

| Observation | Finding |
|---|---|
| No doctrine hash carries a `verified_at` | **I-12 (ERROR)** — the frozen inventory is frozen at an unknown moment; "frozen" without a timestamp is unverifiable |
| Nothing re-verifies hashes on a cadence | **I-13 (ERROR)** — drift is detectable only if someone looks; §14 is entirely reactive with no trigger |
| `MIGRATION_REQUIRED` receipts have no TTL | confirms Pass 1 F-13 from a second direction |
| §37's 2026-10-03 deadline has no owner or countdown | confirms F-31; ~8 weeks out as of this review |
| Burst commit pattern (31 in a day, then near-silence) | **I-14 (WARNING)** — governance is produced in bursts; **an unattended system between bursts has no continuous assurance**, and the 60-minute poller doctrine assumes exactly the opposite operating rhythm |

**I-14 deserves emphasis:** §6.1/§39 design for a continuously-attended session runtime. The repository's actual rhythm is episodic. A poller doctrine calibrated to an operating model the organization does not practice will either be disabled or ignored. Calibrate the doctrine to observed rhythm, or change the rhythm deliberately — but do not ship a control that assumes facts contradicted by your own commit history.

---

## 7. ECONOMIC PASS — WHAT DOES COMPLIANCE COST?

An unasked question in Pass 1, and the strongest predictor of whether controls survive.

| Control | Cost per use today | Likely outcome |
|---|---|---|
| Dispatch a task | seconds (one API call) | used |
| Produce a compliant §25 receipt with distinct validator | manual, minutes, needs a second human | **routed around** |
| Compile a context packet per §23 | fully manual, no tooling | **skipped** |
| Run §31 acceptance tests | impossible (no runner) | **skipped** |
| Re-derive a doctrine hash | manual, no script | **skipped** |
| Write a governance section | minutes, high fluency, no gate | **over-produced** |

**I-15 (CRITICAL) — the cost gradient runs precisely opposite to the safety gradient.** The cheapest actions are the least governed; every control R4 depends on is the most expensive thing an operator could do. No amount of normative language survives that gradient — this is the mechanism by which the 17:1 ratio (I-01) is generated and sustained.

**The single highest-leverage intervention in this entire two-pass review is not a rule. It is tooling that inverts the gradient**: make the compliant path the cheapest path. One CLI that compiles a packet, one that emits a valid receipt, one that runs the tests, one that re-derives hashes. Four scripts would do more for v7.2 compliance than four more doctrine sections.

---

## 8. WHAT PASS 1 GOT WRONG OR OVERWEIGHTED

Intellectual honesty requires inverting on my own output too.

| Pass 1 position | Pass 2 correction |
|---|---|
| 40 findings presented as independent | **Most are symptoms of I-01/I-09.** The finding count overstates the problem's dimensionality; the corrective backlog is shorter and more structural than Pass 1 implied. |
| F-05 (hash case) rated ERROR | **Overweighted.** A one-line case-fold. INFO/WARNING at most. Pass 1 over-ranked mechanically-detectable defects because they were easy to verify — an availability bias in the review method itself. |
| F-03 (ID reuse) rated ERROR | Sound, but **the deeper issue is the absence of any change-control instrument**, which Pass 1 never named. |
| Correction sequence led with Wave 0 "commit the artifacts" | **Wrong priority.** I-02 (PS exfiltration) and I-11 (receipt repudiation) are live, exploitable, and ongoing. Committing a manifest is documentation hygiene. **Live risk precedes provability.** |
| Treated R4's prose as the system | **The system is the code, the data, and the operators' habits.** R4 is a description of an intended system. Pass 1 reviewed the description far more thoroughly than the thing. |

---

## 9. CONSOLIDATED PASS 2 FINDINGS

| ID | Sev | Class | Finding |
|---|---|---|---|
| I-02 | CRITICAL | absent category | DDNA harvester is an unrestricted PS exfiltration channel |
| I-11 | CRITICAL | absent category | Receipts are unauthenticated and fully repudiable |
| I-01 | CRITICAL | root cause | Governance produced 17x faster than enforcement; no WIP limit |
| I-09 | CRITICAL | absent category | A compiled controller with no compiler |
| I-03 | CRITICAL | evidence integrity | DDNA scores are hardcoded fixtures in localStorage |
| I-07 | CRITICAL | absent category | Confidence and safety diverge with no observing instrument |
| I-08 | CRITICAL | absent category | No prototype→production reclassification gate |
| I-15 | CRITICAL | structural | Cost gradient runs opposite to safety gradient |
| I-04 | ERROR | implementation | Local Ollama path blocked by mixed content in production |
| I-06 | ERROR | evidence integrity | Fixtures and live data visually indistinguishable |
| I-10 | ERROR | absent category | Stop-Gates have no delivery path, owner, or SLA |
| I-12/13 | ERROR | temporal | No `verified_at`; no re-verification cadence |
| I-05 | WARNING | measurement | Truncated input; unversioned scoring prompt |
| I-14 | WARNING | temporal | Poller doctrine assumes an operating rhythm not practiced |

**Eight of fourteen are absent categories** — defects with no R4 vocabulary. That is the return on inverting the method, and it is the argument for making multi-perspective review standard rather than incidental (see Deliverable 4).

---

## 10. MERGED PRIORITY — BOTH PASSES

Superseding Pass 1's Wave order. **Live exploitable risk first; provability second.**

```text
WAVE A — STOP THE BLEEDING (live, exploitable, today)
  A1  I-02  Gate DDNA harvest: lane check + local-only until sanitization exists
  A2  I-11  Authenticate receipt/status/dispatch writes; bind actor to credential
  A3  C-05  Remove the self-approval path
  A4  F-15  Fail closed on unknown lane
  A5  C-04  Server-side provider credentials only

WAVE B — STOP MANUFACTURING FALSE EVIDENCE
  B1  I-03  Remove hardcoded DDNA defaults; persist to Supabase with provenance
  B2  I-06  Badge or delete every fixture in the UI
  B3  I-07  No metric renders without a backing measurement event

WAVE C — INVERT THE COST GRADIENT (highest leverage)
  C1  packet-compile CLI      C2  receipt-emit CLI
  C3  test runner + MP72 harness    C4  hash re-derivation script
  C5  governance linter

WAVE D — CLOSE THE ABSENT CATEGORIES
  D1  I-08 prototype→production gate    D2  I-09 name the compiler and its operator
  D3  I-10 Stop-Gate delivery path      D4  I-01 governance WIP limit
  D5  I-12/13 verified_at + re-verification cadence

WAVE E — PASS 1 PROVABILITY WORK (manifest, ledger, artifact commits, ID retirement)
```

Pass 1's Wave 0 becomes Wave E. That reordering is the most important single output of this second pass.

---

**Advisory `INTERACTIVE_REVIEW` evidence. Designates nothing. DCS retains authority under R4 §42.**
