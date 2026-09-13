# DCSE MASTER PROFILE v7.2 R4 — ARCHITECTURAL EVALUATION, GAP ANALYSIS, AND KNOWLEDGE TRANSFER

**Deliverable:** 1 of 2
**Artifact Class:** Independent Enterprise-Architecture Evaluation (advisory)
**Reviewer Role:** Senior Principal Engineer / Architect, enterprise operating systems
**Review Method:** Section-by-section, line-by-line; forward-chaining, backward-chaining, deductive, inductive, and negative prompting
**Subjects Under Review:**

```text
A. DCSE_MASTER_PROFILE_v7.2_COMPILED_CONTROLLER_CANDIDATE_R4.md
   SHA-256 0590bb5349ac66f96ca757db628761fba18106da8e2a4e7a4c25c38bc2c08509  (VERIFIED by this review)
B. DCSE_MASTER_PROFILE_v7.2_R3_GEMINI_INSPECTION.md  (baseline for delta analysis)
C. governance/v7.2/DCSE_V7_2_R4_OPERATIVE_DESIGNATION_20260807.md
D. governance/v7.2/MP72_POLLER_SESSION_RUNTIME_DOCTRINE.md
E. apps/sc-agent-os/api/index.js  (Command Post runtime surface)
```

**Reviewer Disposition:** `PASS_WITH_REQUIRED_CORRECTIONS`
**Recommended Readiness State:** `READY_WITH_FINDINGS` (R4 currently self-asserts `READY`)
**Authority Note:** This document designates nothing. DCS retains authority under R4 §42.

---

## 0. HOW TO READ THIS DOCUMENT (KNOWLEDGE TRANSFER FRAME)

R4 is not a policy document. It is a **compiler specification for a governance controller**, and it should be evaluated with the same discipline as a compiler + linker + runtime loader:

| Compiler concept | R4 equivalent | Failure mode if wrong |
|---|---|---|
| Source set / SBOM | §2.2 frozen doctrine inventory + hashes | phantom or substituted doctrine |
| Symbol table, stable symbols | §9 rule addressing, immutable IDs | silent semantic drift under a stable name |
| Link-time conflict resolution | §8 conflict ledger | strongest-language-wins governance |
| Dead-code elimination | §29.1 dispositions | silent loss of a mandatory control |
| Loader / dynamic linking | §23 Context Compiler | under-restricted runtime packet |
| ABI version pinning | §5 atomic transition, §14 drift | split-brain authority |
| Build attestation | §24 hash semantics, §25 receipts | unverifiable provenance |
| Test suite | §31 MP72-xxx | tests that validate the artifact against itself |

**The single most important architectural property in R4 is this:** authority is *asserted by evidence*, never inferred from existence, recency, version number, or model memory (§2.3, §5, §14, §42). Nearly every finding below is an instance of that property being locally violated.

Two evaluation lenses are used throughout:

- **Positive lens (deductive/forward):** given the rules as written, does the intended goal state follow?
- **Negative lens (negative prompting / adversarial):** *what does this text permit that it did not intend to permit?* A rule is complete only when the prohibited state is unreachable, not merely undesired.

---

## 1. EXECUTIVE ASSESSMENT

### 1.1 What R4 gets right (retain, do not relitigate)

1. **Four-dimension state model (§4)** — separating Readiness / Authority / Deployment / Evolution is the correct fix for overloaded promotion semantics. This is the strongest single idea in the document and it is applied consistently in §31's split between build-readiness and cutover tests.
2. **Dual lane registry (§11)** — governance domains and runtime dispatch lanes are genuinely different ontologies. Conflating them was R2's real defect; R4 resolves it correctly and adds the mapping obligation.
3. **Hash class taxonomy (§24.1)** — explicitly refusing to equate `promoted_source_checksum` with a body SHA-256 is a mature, evidence-first move that most governance frameworks never make.
4. **Fail-closed context compilation (§23)** — "failure to resolve is not absence of restriction" is the correct default and is stated crisply.
5. **Runtime surface classes (§18.1)** — `AUTONOMOUS_CLAIMING` vs `INTERACTIVE_NON_CLAIMING` correctly legitimizes interactive sessions without letting them impersonate poller claims. This is the fix that makes the model honest about how work actually gets done.
6. **Reverse-chain diagnostic engine (§40)** — "repair the earliest broken dependency" is the right troubleshooting invariant and is directly reusable as an operational SOP.
7. **Capability independence + portability debt (§37)** — treating vendor capability as an accelerator and recording `TOOLSET_EXCEPTION` is unusually forward-looking.

### 1.2 The three findings that matter most

| ID | Severity | One-line statement |
|---|---|---|
| **F-01** | CRITICAL | The operative designation binds a controller artifact and a runtime manifest that **do not exist in the canonical repository** — authority is bound to unreachable evidence. |
| **F-02** | CRITICAL | R4's own body says `operative:false / v7.1 controlling`, while the repo designation says `OPERATIVE`. The corpus contains the exact controller-state mismatch its own linter (§28) is required to block on. |
| **F-03** | ERROR | Acceptance-test identifiers `MP72-041/043/044` (and `-002/-010/-011`) were **redefined between R3 and R4** while §9 declares identifiers immutable and non-reusable. Two coverage areas (PPR `default_load`, poller heartbeat/wall-time/health config) lost their only test in the process. |

### 1.3 Verdict

R4 is a substantial and largely sound advance over R3. It is **not** `READY` as written, because `READY` in R4's own definition means "the construction/source-validation gate has passed," and three construction-gate artifacts (canonical controller file in repo, runtime surface manifest, mechanical test evidence) are not present at the canonical source surface. The correct state is `READY_WITH_FINDINGS`, which R4 already defines in §4.1 and does not use.

---

## 2. R3 → R4 DELTA LEDGER (SECTION BY SECTION)

Legend — **Δ**: change; **V**: verification basis (`SOURCE-VERIFIED` / `RUNTIME-VERIFIED` / `INFERRED`); **Assessment**.

### §0 Controlling Purpose
**Δ** R3 ¶1: "compile the governing substance of D01 through D22." R4 ¶1: "compile the shared governing substance of D01-D12 and D15-D22, while compiling D13/D14 only as protected identities and routing controls."
**V** SOURCE-VERIFIED (both texts read).
**Assessment** Correct outcome, **improper mechanism**. This is a change to the *controlling purpose clause* — the most constitutional sentence in the artifact. §8 requires that any change to "constitutional meaning" receive explicit governance disposition and a conflict-ledger entry. No ledger entry exists. → **F-04 (ERROR)**.
**Negative test:** as written, a future compiler reading only R4 §0 cannot distinguish "D13/D14 deliberately excluded from shared body" from "D13/D14 dropped." §29.1 saves it, but the constitution should not depend on a downstream section to avoid ambiguity.

### §2.1–2.2 Source model and frozen inventory
**Δ** R4 adds a 22-row frozen inventory with SHA-256 values. R3 had no inventory.
**V** SOURCE-VERIFIED for presence; **UNKNOWN** for correctness — this review cannot verify the 22 hashes because the source doctrine files were not supplied to it.
**Assessment** Major improvement and the single largest R4 value-add. Three defects:
- **F-05 (ERROR):** inventory values are UPPERCASE hex; §17.1, §6, and the header use lowercase hex. No case-normalization rule exists anywhere. Any mechanical comparator that does not case-fold will produce false drift events, and §14 requires drift events to be non-silently reconciled — i.e. this defect manufactures Stop-Gates.
- **F-06 (ERROR):** §24.1 defines five hash classes; the inventory table has **no hash-class column**. Only D22 gets a prose note ("R4 direct hash of the canonical v7.1 source bytes"), which by implication leaves the other 21 rows' derivation unstated. MP72-028/029 cannot be executed against an untyped column.
- **F-07 (WARNING):** the table records no repository path, commit, retrieval timestamp, or byte length per row. R3 §24.1 explicitly *required* these ("The source-freeze manifest SHALL identify which byte sequence was hashed, the algorithm, repository commit, path, retrieval timestamp, and artifact size"). R4 §24 **deleted that sentence**. See §3.2 below — this is a silent deletion.

### §2.3 Source status and compiled authority
**Δ** R3's worked JSON example (`ACTIVE_IF_AUTHORIZED`) removed; R4 substitutes prose plus "promoted-with-known-gaps" language.
**Assessment** Acceptable prose-level equivalence, but the machine-readable exemplar is gone and the `compiled_status` enum (`ACTIVE_IF_AUTHORIZED`) now appears nowhere. Layer 4 (§7) requires a rule registry; it has no defined status vocabulary. → **F-08 (WARNING): compiled-rule status enum undefined.**

### §3 Status migration — **unchanged**. Sound. No finding.

### §4 Four-dimension state model — **unchanged**. Sound.
**Negative test passed:** §4.5 explicitly kills `OPERATIVE-PATCH`, closing the "release class masquerading as lifecycle state" hole. Good.
**Residual (F-09, INFO):** `READY_WITH_FINDINGS` is defined but has no entry criteria, no exit criteria, and no disposition owner. An unusable middle state pressures every build toward binary READY/NOT_READY — which is precisely what happened in R4.

### §5 Atomic authority transition
**Δ** unchanged text.
**Assessment** The text is correct. Its *implementation* in the repo is not — see F-02 and F-10. §5 requires `new -> OPERATIVE` and `prior -> SUPERSEDED` as **one logical transaction**; the designation document (C) writes "Prior-controller disposition: SUPERSEDED **upon operative runtime cutover reconciliation**," which defers half the transaction indefinitely.
**F-10 (CRITICAL): non-atomic transition creates a sanctioned split-brain window** in which v7.1 is not superseded and v7.2 is operative simultaneously — the exact condition §5 exists to prevent, and it is not covered by §5's "explicitly authorized migration condition" carve-out because no migration condition was declared.

### §6 Runtime surface manifest and session activation
**Δ** R3 §6 named six candidate categories and **required the manifest to record exact implementation identifiers** (scheduler task name, controller path/hash, worker path/hash, Supabase objects, deployed API surfaces). R4 §6 replaces this with six surface *classes* plus six named cutover surfaces, and points to an external manifest file by hash.
**V** The manifest file is **absent from the repository** (verified: no file matching `runtime_surface_manifest*` exists).
**Assessment** → **F-01 (CRITICAL)**. R4 §6's normative content has been externalized into an artifact that cannot be inspected, diffed, linted, or tested. MP72-039 ("manifest frozen and versioned") is unfalsifiable in the current corpus; a hash without a retrievable preimage is an assertion, not evidence. This directly contradicts §2.3's "SHALL never infer authority from file existence" — R4 infers manifest *content* from a hash string.
**F-11 (WARNING):** §6.1 lists `wake-probe interval candidate 5 minutes` inside a block presented as frozen. "Candidate" is ambiguous modality inside a frozen manifest section; §10's linter rule requires flagging exactly this.

### §6.2 Cutover gate — sound, and the strongest guardrail in the document. No finding.

### §7 Five layers — unchanged, sound.

### §8 Conflict resolution — unchanged, sound in text.
**Negative finding F-12 (ERROR):** §8 mandates a conflict ledger, §7 Layer 5 mandates it, §28 lints for "unresolved conflict-ledger entries," and §31 MP72-026 asserts "unresolved CRITICAL normative conflicts = 0". **No conflict ledger instance exists in the corpus.** A count of zero over an absent ledger is vacuously true. This is the archetypal self-referential test that §11.4 explicitly prohibits in another context.

### §9 Stable rule addressing
**Δ** unchanged text — and this is the problem.
**F-03 (ERROR):** §9 states identifiers "SHALL remain permanently reserved and SHALL NOT be reused for an unrelated rule." Between R3 and R4 the following MP72 IDs changed meaning:

| ID | R3 meaning | R4 meaning | Effect |
|---|---|---|---|
| MP72-002 | "PPR governance domain present **and protected**" | "PPR protection present" | narrowed |
| MP72-010 | PS protected module `default_load=false` | D13 `default_load=false` / `shared_body_compile=false` | subject substituted |
| MP72-011 | **PPR** protected module `default_load=false` | D14 `default_load=false` / `shared_body_compile=false` | **PPR coverage lost** |
| MP72-041 | poller manifest records scheduler, heartbeat, **wall-time, recovery, health-monitor** config | 60s cadence + 60-min inactivity | **heartbeat/wall-time/health coverage lost** while §18.2 still mandates it |
| MP72-043 | **all** ERROR findings resolved or dispositioned | **Gemini** ERROR findings corrected or dispositioned | scope narrowed to one reviewer |
| MP72-044 | controller header **fits** measured runtime packet budget | benchmark classes **defined** | normative → definitional (see §30) |

Three of these are simultaneous ID-reuse violations **and** silent coverage deletions. Under §9 the correct action was to retire the old IDs and mint MP72-060+.

### §10 Modal language — unchanged, sound. Note the linter obligation is unmet (F-11, F-19).

### §11 Dual lane registry
**Δ** §11.3's terminal rule changed from "Unknown or conflicting lane mappings SHALL produce a `LANE_MAPPING_STOP_GATE`" (R3) to "SHALL **first emit a `MIGRATION_REQUIRED` receipt** … **If no safe mapping is verified, execution then enters `LANE_MAPPING_STOP_GATE`**" (R4).
**Assessment** Correct in intent (prevents silent deletion of in-flight legacy tags) and R4 defends it with "It SHALL NOT authorize an unknown lane."
**Negative finding F-13 (ERROR):** the sequence is guarded by no test. MP72-005 accepts *either* branch ("map to authority **or** emit MIGRATION_REQUIRED then Stop-Gate"). Nothing in R4 forbids (a) auto-clearing a `MIGRATION_REQUIRED` receipt without DCS or governance disposition, (b) a runtime treating receipt emission as satisfaction of the gate, or (c) an unbounded backlog of MIGRATION_REQUIRED receipts accumulating as de-facto permanent unmapped lanes. **Required:** a TTL/disposition-owner on MIGRATION_REQUIRED and a negative test that receipt emission alone never admits execution.
**F-14 (ERROR, verified against runtime):** §11.2's frozen runtime lane registry contains nine lanes including `PS`. The Command Post implementation (`apps/sc-agent-os/api/index.js:2602`) enumerates **eight** — `PS` is absent — and the dispatch UI (`:781`) offers only seven (omits `PS` and `SS`). MP72-004 ("runtime-dispatch registry matches frozen v7.1 runtime inventory") **fails today**. Detail in Deliverable 2.
**F-15 (CRITICAL, verified against runtime):** the same code **silently coerces** an unrecognized lane to `'DCSE'` and an unrecognized task_type to `'other'`. This is fail-*open* substitution at the exact point §11.3 and §23 mandate fail-closed behavior, and it produces no MIGRATION_REQUIRED receipt. Detail in Deliverable 2.

### §11.4 Test rule — correctly forbids self-referential MP72-003. Note the same discipline is *not* applied to MP72-026, MP72-039, MP72-042 (F-12, F-01, F-19).

### §12 D13/D14/PS/PPR firewall
**Δ** R3's `PS-DART` and `PPR` entries each carried `cross_lane_export:false` **and** `unauthorized_access_action:"GOVERNANCE_STOP_GATE"`. R4's D13/D14 entries carry **neither**; R4's PPR entry keeps `cross_lane_export` but **loses `unauthorized_access_action`**.
**Assessment** → **F-16 (ERROR): silent weakening of the protected-module machine contract.** R4 adds prose ("Any attempt to inject protected D13/D14 material … SHALL fail closed and emit a sanitization/security receipt"), which is good, but the *machine-readable* enforcement fields that a context compiler actually reads were deleted with no ledger entry. Prose does not compile.
**Negative test:** a compiler consuming only R4's `protected_modules` JSON has no instruction for what to do on unauthorized access to D13/D14, and no prohibition on cross-lane export of D13/D14. Restore all three fields on all three entries.
**Positive note:** R4's addition of `shared_body_compile:false` and the explicit "D17 is **not** a PS-protected replacement for D13/D14" clarification are genuine improvements.

### §13 D21, §14 D22 — unchanged, sound.
**F-17 (ERROR, verified against runtime):** §14 requires "Every mandatory runtime surface SHALL be able to report the controller version and hash it is enforcing." Command Post — a §6 mandatory cutover surface — exposes **no** controller version/hash on any endpoint (`/api/runtime` included). MP72-045 cannot pass. Detail in Deliverable 2.

### §15 D04 communication states, §16 D05 promotion — unchanged, sound.

### §17 D17 / D15 — the R3 CRITICAL Stop-Gate is **closed** in R4
**Δ** R3 §17.1 held `SOURCE_IDENTITY_CONFLICT_D17` open at CRITICAL. R4 §17.1 closes it via resolution path 3 (the mislabeled artifact belongs under D15) plus a tombstone commit `98d3c6c…`.
**Assessment** **Accepted.** This is the correct resolution and it used a permitted R3 path rather than title similarity. R4 §36's instruction not to re-litigate it is legitimate and this review complies.
**Residual F-18 (WARNING):** two different values are recorded for D17 — artifact `12186A59…` and promoted checksum `568a8f2b…`. §24.1 correctly says these are different classes and §24 says a reviewer SHALL NOT reopen a conflict merely because classes differ. Sound. But **no procedure exists to ever reconcile them**, so a genuine unauthorized mutation of the promoted record would be indistinguishable from a benign class difference. Required: record the derivation algorithm for `promoted_source_checksum`, or classify it `UNKNOWN_HASH_SEMANTICS` — a classification R3 §24.1 defined and **R4 deleted** (see §3.2).

### §18 Capability and runtime classes — largely unchanged, sound.
**F-20 (ERROR, negative test):** `INTERACTIVE_NON_CLAIMING` (§18.1) is defined by six obligations, none of which bounds *what kind of work* it may perform. Nothing prohibits an interactive session from executing a governance mutation, a promotion, a D15 database change, or an operative designation. §20 fails closed only on *unknown source authority*, which does not cover a known-authority interactive promotion. **Required:** add "an INTERACTIVE_NON_CLAIMING surface SHALL NOT perform governance mutation, promotion, authority designation, or serve as independent validator of its own output," with a matching negative test.
**F-21 (WARNING):** §18.2 mandates recording heartbeat/wall-time/health-monitor config in the operative manifest, but after the MP72-041 redefinition (F-03) **no test asserts it**. Normative requirement with zero coverage.

### §19 artifact classes, §20 source modes, §21 reasoning states — unchanged, sound. `ASSUMPTION` is a good addition.

### §22 Goal-state orchestration — unchanged, sound. The `detect → diagnose → remediate → test → record → continue` loop is the operational heart of the document and should be lifted verbatim into worker onboarding.

### §23 Context compiler fail-closed — unchanged, sound in text; violated in implementation (F-15).

### §24 Provenance and hash semantics
**Δ** R4 expands the class taxonomy from three to five (adds `promoted_source_checksum`, `database_body_sha256`) — an improvement grounded in a real verified finding ("`governance_directives.checksum` values are not hashes of the database `body` field").
**Δ (deletions)** R4 **removed** from R3 §24: the many-to-one provenance JSON exemplar; the source-freeze manifest field requirements; the enumerated "build SHALL produce immutable hashes for [6 artifacts]" list; and the `UNKNOWN_HASH_SEMANTICS` classification.
**Assessment** → **F-22 (ERROR): four normative provisions deleted without conflict-ledger entries**, in an artifact whose §16 and §29.1 both promise that superseded controls "SHALL enter the conflict ledger rather than being silently discarded." R4 improved the taxonomy and simultaneously weakened the obligations that made the taxonomy enforceable.

### §25 Receipts — unchanged, sound.
**Negative finding F-23 (WARNING):** §25 requires structurally distinct executor and validator and forbids "independently validated with a null or anonymous validator." R4's own §33/§34 assert that Gemini's required corrections are incorporated and readiness is READY, with **no validator receipt** and no independent validation record for R4 itself. The controller does not meet its own §25 standard for the assertion that it is READY. This is the cleanest example of the artifact not applying its own rules to itself.

### §26 Rollback, §27 Backward compatibility — sound.
**F-24 (ERROR):** §27's default policy is "derived from source governance and risk classification during compilation" — i.e. undefined at read time. Under the document's own fail-closed doctrine (§23), an unresolved policy must resolve to the *safest* branch. **Required:** "Absent an explicit determination, the default SHALL be `PINNED_COMPLETION`." As written, an implementer may reasonably default to `MIGRATED_EXECUTION` and silently move in-flight work onto a new controller — the outcome §27's own last line prohibits.

### §28 Governance linter — unchanged list, sound and well-specified.
**F-19 (ERROR):** MP72-042 asserts "governance lint contains no unresolved CRITICAL finding." **No lint implementation, configuration, or output exists in the corpus.** As with F-12, this is a vacuous pass. Note further that a conforming linter run against R4 itself would raise at least: *controller-state mismatch* (F-02), *ambiguous modal language* (F-11), *missing source hashes* — path/commit fields (F-07), *inconsistent human/machine rule IDs* (F-03), *unresolved conflict-ledger entries* — ledger absent (F-12), and *missing mandatory-runtime activation evidence* (F-01). **Six of §28's own required checks would fire on R4.**

### §29 Build pipeline
**Δ** expanded to 26 steps; adds capability/toolset registries (14) and reverse-chain generation (16).
**Assessment** sound sequencing; step 3 correctly retains the CRITICAL source-identity stop.
**F-25 (WARNING):** R3 §29.1 published the **allowed disposition enum** (`RETAIN_LAYER3 / SUBSUMED_IN_MP / PROTECTED_MODULE / SOURCE_CONFLICT_STOP_GATE / EXPLICITLY_SUPERSEDED`). R4 §29.1 lists per-doctrine values but **dropped the enum**, so a linter has no closed vocabulary to validate against and `EXPLICITLY_SUPERSEDED` now exists nowhere in the corpus. Restore the enum.

### §30 Token economy
**Δ** R3 carried a **normative acceptance rule**: "The Controller Header and required task governance packet SHALL fit inside the smallest supported runtime context budget after reserving the approved task/evidence budget, without dropping mandatory rule dependencies." R4 replaces it with three benchmark classes (32k/128k/1M+) and "acceptance testing SHALL demonstrate that mandatory governance can coexist with a useful task/evidence reserve."
**Assessment** → **F-26 (ERROR): normative downgrade.** "A useful reserve" is unmeasurable; "fits within budget X after reserving Y" was measurable. Combined with the MP72-044 redefinition (F-03), R4 has no pass/fail token gate at all. This is an **overcorrection in the loosening direction** in response to Gemini G-04, which asked for *targets* — R4 supplied classes instead of targets and removed the pre-existing rule.
**Required:** restore the R3 acceptance rule, retain the benchmark classes as the measurement harness, and re-mint the "header fits budget" test under a new ID.
**Retained strength:** "No mandatory rule may be deleted solely to meet a token target" is correct and should never be relaxed.

### §31 Acceptance tests
**Δ** split into build-readiness vs operative cutover — **excellent**, and the correct consequence of §4's state model. New tests MP72-049..059 are well-aimed (PS injection sanitization, toolset governance, portability debt, maintenance as first-class work, reverse-chain diagnosis, wake-probe without model launch).
**Findings** F-03 (ID reuse), F-12/F-19 (vacuous passes), plus:
- **F-27 (ERROR): no test evidence exists.** §31 is a specification of tests, not a result set. Nowhere in the corpus is there a test runner, a results file, or a receipt binding MP72-001..055 to PASS with a validator identity. `Readiness: READY` therefore rests on unproduced evidence — the definitional failure mode R4 §35 calls out as "Evidence outranks narrative."
- **F-28 (WARNING): missing tests.** No test covers: PPR `default_load=false` (lost via F-03); protected-module `unauthorized_access_action` (lost via F-16); §14 drift-event generation on version/hash mismatch; §26 rollback *execution* (MP72-035 only asserts the model "exists"); §37's 2026-10-03 portability deadline; the CLAUDE.md security constraint "no family or minor content in public repositories" (§11.3 mentions FAMILY but no test guards it); and negative authorization tests for §17.3's D15 controls.

### §32–§34 Convergence and disposition
**F-29 (ERROR): internal numeric inconsistency.** §32 states "R4 incorporates **four** evidence streams" and lists four (Review A, Review B, Claude Code R2, Gemini). §34 records `"formal_review_inputs": 3`. Both may be defensible (Gemini is advisory, not formal), but the artifact never says so at either site. Under §21 this is an unlabeled `ASSUMPTION` presented as fact in a machine-readable disposition block. Add `"advisory_inputs": 1` and a one-line reconciliation.
**F-30 (WARNING):** §32 asserts "Claude's former F-01 lane concern is resolved by the dual registry." The *specification* is resolved; the *implementation* is not (F-14, F-15). Closing a finding against a spec change while the runtime still exhibits the defect is exactly the drift §14 exists to catch. Re-open as an implementation finding with a cutover owner.

### §35 Controlling principle — strong. Retain verbatim. It is the best available one-page onboarding artifact for new participants.

### §36 Review baseline after Gemini — legitimate and correctly bounded ("A future conflict may be opened only by new evidence…"). No finding.

### §37 Capability independence
**Δ** new in R4. Strong.
**F-31 (WARNING):** the 2026-10-03 parity deadline has no owner, no defined test procedure, no evidence artifact, and no consequence on miss. MP72-051 covers portability *debt recording*, not deadline satisfaction. A dated commitment without a gate is a wish.

### §38 Infrastructure control layers — new in R4, sound and practical. §38.2's governed git lifecycle and "blind pull/overwrite is prohibited" are directly actionable. "A dashboard warning without remediation ownership is not a maintenance strategy" is the right principle and should be generalized into a rule with an owner field.

### §39 Session poller — new; overlaps §6.1.
**F-32 (WARNING): duplicated normative content.** The 60-minute rule, wake sources, and probe behavior appear in both §6.1 and §39 in non-identical wording. §28 lints for "duplicate mandatory rules." Designate one section normative and make the other a cross-reference.

### §40 Reverse-chain diagnostic — new; excellent. Retain. Pair it with §22 as the standard operational procedure.

### §41–§42 Build confirmation and DCS gate — text is correct and appropriately conservative. Its execution is where F-01, F-02, and F-10 live.

---

## 3. CROSS-CUTTING GAP ANALYSIS

### 3.1 Backward-chaining proof from the declared goal state

Goal state (R4 §42): *v7.2 R4 is the controlling enterprise Master Profile.*

```text
GOAL: R4 is controlling
 ↓ requires (§42) DCS designation binding exact artifact hash + repository commit/path
   → PARTIAL: hash bound and VERIFIED (0590bb53… matches). Repository path/commit NOT bound;
     the artifact is absent from the repo.                                    ← F-01
 ↓ requires (§5) atomic transition, prior → SUPERSEDED
   → BROKEN: supersession deferred to future reconciliation.                  ← F-10
 ↓ requires (§6.2) every mandatory cutover surface acknowledges controller identity
   → BROKEN: Command Post reports no controller version/hash.                 ← F-17
 ↓ requires (§31) MP72-040/045/056-059 cutover evidence
   → BROKEN: no evidence artifacts exist.                                     ← F-27
 ↓ requires Readiness = READY
   → requires MP72-001..055 pass
     → BROKEN: no test results exist.                                         ← F-27
   → requires §28 lint with no unresolved CRITICAL
     → BROKEN: no linter exists; six checks would fire if it did.        ← F-19, F-02
   → requires §6 frozen runtime surface manifest
     → BROKEN: manifest file absent.                                          ← F-01
```

**FIRST dependency not VERIFIED (per §40's own method): the runtime surface manifest and the canonical R4 artifact are not present at the canonical source surface (F-01).** Everything above it in the chain is unprovable until that edge is repaired. Per §40, repair the smallest bounded broken edge first: **commit the artifact and the manifest, then re-run the reverse proof.**

### 3.2 Silent-deletion register (R3 provisions absent from R4 with no ledger entry)

| # | Deleted provision | R3 site | Impact |
|---|---|---|---|
| 1 | Source-freeze manifest must record byte sequence, algorithm, commit, path, retrieval timestamp, artifact size | §24.1 | provenance unverifiable per-row (F-07) |
| 2 | `UNKNOWN_HASH_SEMANTICS` classification | §24.1 | no safe state for the D17 checksum (F-18) |
| 3 | "Build SHALL produce immutable hashes for [source artifacts, compiled controller, machine manifest, rule registry, context compiler release, acceptance-test output]" | §24.1 | manifest/test-output hashing no longer required (F-27) |
| 4 | `unauthorized_access_action: GOVERNANCE_STOP_GATE` on protected modules | §12 | no machine-readable enforcement action (F-16) |
| 5 | `cross_lane_export: false` on the PS-protected module | §12 | export prohibition now prose-only (F-16) |
| 6 | Token acceptance rule (header+packet must fit smallest budget) | §30 | no pass/fail token gate (F-26) |
| 7 | Disposition value enum incl. `EXPLICITLY_SUPERSEDED` | §29.1 | linter has no closed vocabulary (F-25) |
| 8 | Doctrine compilation-status exemplar (`ACTIVE_IF_AUTHORIZED`) | §2.3 | rule-registry status enum undefined (F-08) |

**Every one of these is a §16-class event** ("shall enter the conflict ledger rather than being silently discarded") and none was ledgered. This register is itself the most valuable output of the R3→R4 diff and should be attached to the conflict ledger when it is created.

### 3.3 Negative prompting — what R4 permits that it should not

For each: the adversarial reading, then the required closing rule.

| # | An implementer complying with R4's literal text could… | Closed by | Required correction |
|---|---|---|---|
| N-01 | …declare `Readiness: READY` with no test results, because no rule requires evidence *artifacts* for §31 | nothing | MP72-060: readiness requires a signed test-result artifact with validator identity |
| N-02 | …accumulate MIGRATION_REQUIRED receipts indefinitely and never reach the Stop-Gate | nothing | TTL + disposition owner + negative test (F-13) |
| N-03 | …execute a governance promotion from an interactive browser session | nothing | prohibit governance mutation on INTERACTIVE_NON_CLAIMING (F-20) |
| N-04 | …coerce an unknown lane to a default lane and proceed (and the CP code does exactly this) | §23 in spirit only | explicit "SHALL NOT substitute a default for an unresolved lane" (F-15) |
| N-05 | …satisfy MP72-026/042 with an absent ledger and absent linter | nothing | require artifact existence, not counter value (F-12, F-19) |
| N-06 | …default in-flight work to MIGRATED_EXECUTION | nothing | default `PINNED_COMPLETION` (F-24) |
| N-07 | …validate its own output because §25's "structurally distinct" is undefined for a single-agent session | partially | define distinctness: different agent_key **and** different runtime_instance |
| N-08 | …reuse a retired MP72 test ID with new meaning (R4 did this six times) | §9 (violated) | extend §9 explicitly to test IDs, not only rule IDs (F-03) |
| N-09 | …treat the absence of D13/D14 from the shared table as "doctrine missing" and re-add it | §2.1 ¶3 | **CLOSED — R4 handles this well.** Retain verbatim. |
| N-10 | …infer authority from the highest version number | §5 last line | **CLOSED.** Retain. |
| N-11 | …reopen D17 on a hash-class difference | §24, §36 | **CLOSED.** Retain. |
| N-12 | …emit protected D13/D14 body into a shared packet | §12 prose | partially closed; restore machine fields (F-16) |

R4 closes four of twelve adversarial paths cleanly. The remaining eight are the corrective backlog.

### 3.4 Forward-chaining sanity check (inductive)

From the current verified state — *artifact hash verified, designation signed, code deployed, no manifest, no tests, lanes mismatched* — the most probable failure sequence if cutover proceeds unchanged:

1. A dispatch arrives with `lane: "PS"` (a §11.2-authorized lane). CP coerces it to `DCSE` (F-15, F-14).
2. A PS-classified task now executes in a non-PS lane with a non-PS context packet.
3. §12's firewall is not violated by the *compiler* — it is bypassed *upstream* of the compiler, so no sanitization receipt fires and MP72-049 still passes.
4. The receipt records lane `DCSE`, so the evidence trail attests to the wrong lane and the violation is invisible to audit.

**This is the highest-consequence risk in the system today, it is verified in code, and it is not detected by any existing MP72 test.** It is a firewall bypass reachable through a fail-open default, not through the firewall itself. Treat as CRITICAL and fix before cutover.

---

## 4. CONSOLIDATED FINDINGS REGISTER

Format per R3 §36's required output shape.

| ID | Class | Sev | Site | Issue | Required correction | Changes constitutional meaning? | Disposition |
|---|---|---|---|---|---|---|---|
| F-01 | SOURCE-VERIFIED | CRITICAL | §6, §42, designation | Canonical R4 artifact and `runtime_surface_manifest.v7.2.r4.json` absent from repository; authority bound to unreachable evidence | Commit both at canonical paths; bind path+commit in the designation | No | OPEN |
| F-02 | SOURCE-VERIFIED | CRITICAL | §34 vs designation | R4 body says `operative:false`/v7.1 controlling; repo designation says OPERATIVE | Issue R4.1 body-state correction or an addendum reconciling both | No (corrective) | OPEN |
| F-10 | SOURCE-VERIFIED | CRITICAL | §5 vs designation | Supersession deferred → sanctioned split-brain window | Either complete the transaction or declare an explicit §5 migration condition with an end date | No | OPEN |
| F-15 | RUNTIME-VERIFIED | CRITICAL | §11.3/§23 vs `index.js:2602` | Unknown lane silently coerced to `DCSE`; enables firewall bypass (§3.4) | Reject unknown lane 400 + MIGRATION_REQUIRED receipt | No | OPEN |
| F-03 | SOURCE-VERIFIED | ERROR | §9, §31 | Six MP72 IDs redefined; PPR and poller-config coverage lost | Retire reused IDs, re-mint 060+, restore lost tests | No | OPEN |
| F-12 | SOURCE-VERIFIED | ERROR | §8, §31 MP72-026 | Conflict ledger does not exist; zero-count is vacuous | Create ledger; seed with §3.2 register | No | OPEN |
| F-14 | RUNTIME-VERIFIED | ERROR | §11.2 vs `index.js:2602`, `:781` | Runtime lane set omits `PS` (and UI omits `PS`,`SS`) | Reconcile to the frozen nine or amend the registry with evidence | No | OPEN |
| F-16 | SOURCE-VERIFIED | ERROR | §12 | `unauthorized_access_action` / `cross_lane_export` deleted from protected-module JSON | Restore all three fields on D13, D14, PPR | **Yes — restores a protection** | OPEN |
| F-17 | RUNTIME-VERIFIED | ERROR | §14 vs CP API | Mandatory surface cannot report controller version/hash | Add controller identity to `/api/runtime` | No | OPEN |
| F-19 | SOURCE-VERIFIED | ERROR | §28, MP72-042 | No linter exists; six of its own checks would fire on R4 | Implement linter; run against R4 | No | OPEN |
| F-20 | INFERRED | ERROR | §18.1 | Interactive surfaces unbounded as to work class | Prohibit governance mutation/promotion/self-validation | **Yes — adds a restriction** | OPEN |
| F-22 | SOURCE-VERIFIED | ERROR | §24 | Four provenance provisions deleted without ledger | Restore or ledger each | No | OPEN |
| F-24 | SOURCE-VERIFIED | ERROR | §27 | In-flight default policy undefined | Default `PINNED_COMPLETION` | No | OPEN |
| F-26 | SOURCE-VERIFIED | ERROR | §30 | Normative token acceptance rule downgraded to advisory classes | Restore R3 acceptance rule; keep classes as harness | **Yes — restores a gate** | OPEN |
| F-27 | SOURCE-VERIFIED | ERROR | §31 | No acceptance-test evidence exists | Produce signed result artifact before READY | No | OPEN |
| F-29 | SOURCE-VERIFIED | ERROR | §32 vs §34 | 4 evidence streams vs `formal_review_inputs:3` | Add `advisory_inputs` and reconcile | No | OPEN |
| F-04 | SOURCE-VERIFIED | ERROR | §0 | Controlling-purpose clause changed without ledger entry | Ledger the change | No | OPEN |
| F-05 | SOURCE-VERIFIED | ERROR | §2.2 | Hash case not normalized | Mandate lowercase hex; case-fold on compare | No | OPEN |
| F-06 | SOURCE-VERIFIED | ERROR | §2.2 vs §24.1 | Inventory rows untyped by hash class | Add `hash_class` column | No | OPEN |
| F-13 | INFERRED | ERROR | §11.3 | MIGRATION_REQUIRED unbounded, untested | TTL, owner, negative test | No | OPEN |
| F-25 | SOURCE-VERIFIED | WARNING | §29.1 | Disposition enum dropped | Restore enum | No | OPEN |
| F-07,08,09,11,18,21,23,28,30,31,32 | mixed | WARNING/INFO | various | See §2 | See §2 | No | OPEN |

**Counts:** CRITICAL 4 · ERROR 14 · WARNING 10 · INFO 1.

Under R4 §28's own gate behavior (`CRITICAL → authority/readiness gate blocked`), **four CRITICAL findings block `READY` and block cutover** until corrected or expressly dispositioned by DCS.

---

## 5. TOP FIVE RESIDUAL RISKS

1. **Authority bound to absent evidence (F-01/F-02/F-10).** The governance system's central claim — "one operative controller, provably identified" — is currently unprovable from the repository alone. This is a systemic credibility risk, not a paperwork risk.
2. **Fail-open lane coercion enabling silent PS firewall bypass (F-15/F-14).** Highest consequence, verified in code, undetected by existing tests, and it corrupts the audit trail as a side effect.
3. **Vacuous mechanical assurance (F-12/F-19/F-27).** Three of R4's strongest guarantees (zero conflicts, clean lint, tests pass) are currently assertions over non-existent instruments. This is the failure mode most likely to be discovered by an outside party rather than internally.
4. **Silent normative erosion across revisions (F-03/F-16/F-22/F-26 + §3.2).** R4 deleted eight provisions with no ledger. If this rate persists across R5/R6, the controller will drift materially from its own doctrine while every individual revision looks like an improvement. **The conflict ledger is the only structural defense and it does not exist.**
5. **Deadlines and states with no owner (F-09/F-31/§38.3).** `READY_WITH_FINDINGS` unusable, 2026-10-03 parity unowned, remediation ownership unassigned — the document itself observes that "a dashboard warning without remediation ownership is not a maintenance strategy."

---

## 6. FACTS THIS REVIEW COULD NOT VERIFY

```text
UNKNOWN  the 22 doctrine SHA-256 values in §2.2 (source files not supplied)
UNKNOWN  contents of runtime_surface_manifest.v7.2.r4.json (file absent)
UNKNOWN  the derivation of promoted_source_checksum 568a8f2b… for D17
UNKNOWN  live Supabase dcse_cp control-plane state (not queried in this review)
UNKNOWN  Windows DCSE_Universal_Dispatch_Controller / wake-probe host state
UNKNOWN  the original text of Review Input A and Review Input B
VERIFIED R4 artifact SHA-256 0590bb53… matches the designation
VERIFIED absence of the R4 artifact and manifest from the repository tree
VERIFIED CP runtime lane enumeration and fail-open coercion (index.js:781, :2602)
```

---

## 7. OVERCORRECTIONS AND THINGS TO LEAVE ALONE

- **Overcorrection (loosening):** §30 token economy (F-26) and MP72-044. Gemini G-04 asked for targets; R4 removed the one gate that existed.
- **Overcorrection (loosening):** §12 protected-module JSON (F-16). Prose was added while enforcement fields were removed — net weakening disguised as clarification.
- **Correctly bounded, do not reopen:** §17 D17 resolution, §36 review baseline, §2.1 D13/D14 shared-table exclusion, §11.2 retention of TSL/TRIBUNAL/DDNA/RAG/SYSTEM, §24's rule against reopening on hash-class difference.
- **Do not touch:** §35 Controlling Principle, §40 reverse-chain engine, §22 goal-state loop, §6.2 cutover gate, §4 four-dimension model. These are the load-bearing walls.

---

## 8. RECOMMENDED CORRECTION SEQUENCE (R4.1)

Ordered by §40 — earliest broken dependency first, smallest bounded edge, then forward-chain.

```text
Wave 0 — restore provability (unblocks everything above it in §3.1)
  0.1 Commit the canonical R4 artifact at governance/v7.2/ and bind path+commit in the designation
  0.2 Commit runtime_surface_manifest.v7.2.r4.json; verify 45a504d8… against the committed bytes
  0.3 Publish the conflict ledger; seed it with the §3.2 silent-deletion register

Wave 1 — CRITICAL corrections
  1.1 Fix lane fail-open in Command Post (F-15) and reconcile the lane set (F-14)
  1.2 Reconcile controller state: R4 body vs designation (F-02)
  1.3 Complete or explicitly bound the atomic transition (F-10)

Wave 2 — restore deleted protections
  2.1 §12 protected-module fields (F-16)
  2.2 §30 token acceptance rule (F-26)
  2.3 §24 provenance provisions + UNKNOWN_HASH_SEMANTICS (F-22, F-18)
  2.4 §29.1 disposition enum (F-25); §2.2 hash_class + lowercase hex (F-05, F-06)

Wave 3 — restore and extend test coverage
  3.1 Retire reused MP72 IDs; re-mint MP72-060+ (F-03)
  3.2 Re-add PPR default_load and poller-config tests
  3.3 Add tests from F-28 and negative tests N-01..N-08
  3.4 Implement the §28 linter; run it against R4 and publish output

Wave 4 — close the semantic holes
  4.1 §18.1 interactive-surface work-class prohibition (F-20)
  4.2 §27 default PINNED_COMPLETION (F-24)
  4.3 §11.3 MIGRATION_REQUIRED TTL/owner (F-13)
  4.4 §32/§34 review-count reconciliation (F-29); §0 ledger entry (F-04)

Wave 5 — re-run the §3.1 backward proof, produce signed test evidence, re-disposition readiness
```

Waves 0–1 are prerequisites to any honest `READY`. Waves 2–4 are prerequisites to `OPERATIVE` under R4's own §28 gate behavior.

---

## 9. KNOWLEDGE TRANSFER — THE SEVEN RULES A NEW PARTICIPANT MUST INTERNALIZE

1. **Existence is not authority.** A file, a row, a version number, a deployment, or a model's memory proves nothing. Only a DCS designation binding an exact hash creates authority (§2.3, §5, §42).
2. **Unresolved means stop, never default.** Fail-closed is not a preference; substituting a default for an unresolved lane, authority, or dependency is the primary way this system gets breached (§23, and F-15 is the live proof).
3. **Readiness ≠ Authority ≠ Deployment ≠ Evolution.** Four independent dimensions. Never collapse them into one word (§4).
4. **Identifiers are immutable.** Retire, never reuse — for rules *and* tests. A stable ID with changed meaning is undetectable drift (§9, F-03).
5. **Deletions get ledgered.** If a control disappears between revisions, it goes in the conflict ledger with a disposition. Silent deletion is the failure mode that ends governance systems (§8, §16, §3.2).
6. **Executor ≠ validator.** No artifact is "independently validated" by the agent that produced it, and that includes this controller validating its own readiness (§25, F-23).
7. **Diagnose backwards, repair forwards.** Reverse-chain to the *first* unverified dependency, repair the smallest bounded edge, forward-chain the fix, re-run the proof (§40, §22). This document's §3.1 is a worked example.

---

**Prepared as advisory evidence for DCS. This document designates nothing and transitions no authority. It does not reopen the D17 identity question (R4 §36) and records no finding based on hash-class difference alone (R4 §24).**
