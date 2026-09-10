# SC.COM DOSSIER WEBSITE BUILD PLAN — v1.1 (DISTRIBUTABLE)

**Task ID:** SC-WEBSITE-BUILD-DOSSIER-001
**Lane:** SC
**Phases:** 1-8 (Complete Build Cycle)
**Status:** Ready for Team Execution — pending DCS Level 0 Phase 1 entry approval
**Distribution:** Via Poller to all named executors below
**Supersedes:** SC-WEBSITE-DOSSIER-BUILD-PROMPT.md (v1.0, 2026-08-10)
**Internal reference (do not distribute):** SC-AI-RFP-SIM-001 Sections A/B/C

> **Sanitization notice.** This document is written for distribution to models outside the
> governance core. Internal lane codes, protected-surface names, related-brand names, and
> doctrine section references are deliberately withheld and replaced with neutral terms
> ("protected content", "related brand"). Do not reintroduce them. Executors requiring the
> controlled vocabulary request it per §0.2 — it is never inlined here.

---

## 0. PREREQUISITES (must be satisfied before Phase 1 begins)

### 0.1 Executor Roster

Every phase has one **Primary** (sole authority to declare the exit gate met), one **Fallback**,
and where noted a **mandatory co-signer** whose approval is independently required.

| Code | Role | Scope |
| :--- | :--- | :--- |
| DCS-L0 | Human release authority | Sole approver of go-live, product families, published content, and any gate-criteria modification. Cannot be delegated to any model. |
| CTO | Technical/architecture authority | Architecture, IA, schema, code, isolation design, evidence standard. |
| AUD | Audit + editorial authority | Editorial production, protected-content detection, voice consistency, visual/media production. |
| DBA | Deployment authority | Platform access, credentials, backups, staging, promotion, rollback. |
| NAR | Narrative continuity | Copy continuity, storytelling, brand through-line. Advisory; never a Primary. |
| MMQ | Multimodal QA | Independent second-opinion visual/accessibility review. Advisory; never a Primary. |

Phase assignments:

| Phase | Primary | Fallback | Mandatory co-signer |
| :--- | :--- | :--- | :--- |
| 1 Ecosystem Declaration | CTO | NAR | DCS-L0 (product families) |
| 2 Dossier Content Model | AUD | CTO | CTO (schema) + DCS-L0 (publish release) |
| 3 Sitemap & Architecture | CTO | NAR | AUD (discovery-surface isolation) |
| 4 Three Visual Directions | AUD | MMQ | CTO (platform feasibility) + DCS-L0 (selection) |
| 5 Responsive Prototype | CTO | AUD | AUD (isolation inspection) |
| 6 Visual Assets & Media | AUD | MMQ | MMQ (independent QA) |
| 7 Production Implementation | DBA | CTO | CTO (isolation re-test) |
| 8 Launch & Measurement | DBA | CTO | **DCS-L0 (go-live — MANDATORY, non-delegable)** |

**Rule:** a model may not approve its own output, may not act as its own co-signer, and may not
substitute for DCS-L0 under any circumstance, including schedule pressure.

### 0.2 Protected-Content Definition (resolves v1.0 critical gap)

The protected-content scans required at Phases 2, 5, 6, 7 and 8 are **not** executable against an
undefined target. Before Phase 2 opens:

- CTO publishes `SC-WEBSITE-PROTECTED-TERMS-v1.json` to the controlled store — a machine-readable
  list of prohibited keywords, entity names, identifiers, URL patterns, and file-path patterns.
- The list itself is protected content. It is referenced by hash, never pasted into any prompt,
  deliverable, commit message, or public artifact.
- Every scan reports: list version hash, corpus scanned, match count, and reviewer.
- A scan that cannot resolve the list version is a **failed scan**, not a passed one.

### 0.3 Toolchain Access Verification

DBA verifies and records working access to every tool required for Phases 5-8 before Phase 5
opens: platform (Wix), database, model APIs, source control, hosting, analytics, design, media
processing. Output: `SC-WEBSITE-TOOLCHAIN-VERIFICATION.md` with one PASS/FAIL row per tool.
**Phase 5 does not open with any FAIL row.**

### 0.4 Artifact Destinations

| Artifact class | Destination | Naming |
| :--- | :--- | :--- |
| Phase deliverables | `tribunal/SC-WEBSITE/phase-N/` | `SC-WEBSITE-P{N}-{SLUG}.md` |
| Gate receipts | `tribunal/SC-WEBSITE/receipts/` | `SC-WEBSITE-P{N}-GATE-RECEIPT.json` |
| Scan reports | `tribunal/SC-WEBSITE/scans/` | `SC-WEBSITE-P{N}-SCAN-{DATE}.json` |
| Prototype code | Feature branch, PR to main | `claude/sc-website-p5-prototype` |
| Decision log | `tribunal/SC-WEBSITE/DECISION_LOG.md` | append-only |

Every gate receipt records: phase, criteria list with per-criterion PASS/FAIL and evidence path,
approver, co-signer, timestamp, and scan list-version hash.

### 0.5 Completion Semantics (resolves v1.0 critical gap)

An executor's own report is **never** completion. Each phase task moves:

`planned → assigned → running → needs_review → (DCS accept) → completed`

A phase that self-declares "exit gate met" enters `needs_review`. Only DCS-L0 acceptance moves it
to `completed`, and only `completed` opens the next phase's entry gate. There is no path from
`running` to `completed`.

### 0.6 Evidence Rule

No placeholder, illustrative, sample, or projected figure may appear in any deliverable presented
as a result. Every stat is live-measured with its source and capture time recorded, or it is
labeled as an explicit hypothesis. This applies to Phase 5 performance baselines and all Phase 8
measurement without exception.

---

## OBJECTIVE

Build SC.com as a **Dossier website**: a proof-first platform that demonstrates the organization's
capabilities through real work, decisions, and outcomes. The site serves as both a public proof
engine and an internal product demonstration.

The site will feature:
- Curated Dossier entries (work samples, decision records, case studies)
- Product and service catalog
- Company philosophy and approach
- Related brand presence with distinct fingerprints
- Protected content architecture (isolated, not public-facing)

## CORE DIRECTIVE

**Show the work.** The website does not describe capabilities generically; it demonstrates them
through structured proof: problems solved, decisions made, tradeoffs considered, results achieved,
and lessons learned.

---

## PHASES 1-8: BUILD CYCLE

### PHASE 1: Ecosystem Declaration

**Primary:** CTO · **Fallback:** NAR · **Co-signer:** DCS-L0

**What to do:**
- Lock product families and service boundaries (what the org sells/offers)
- Define Dossier purpose: what counts as "approved public work"?
- Establish protected content rules: what never appears publicly and why
- Map visitor journeys: what should someone learn in three clicks?
- Produce the shared strategic brief that Phase 4's three directions will all derive from

**Exit gate:**
- Every proposed page maps to one lane, one audience purpose, one conversion outcome
- Product families stated and locked, with DCS-L0 written approval
- Dossier publishing rules written down
- Protected content categories explicitly excluded, each with a stated reason
- `SC-WEBSITE-PROTECTED-TERMS-v1.json` published and hash recorded (§0.2)
- Strategic brief accepted by CTO and AUD as sufficient input for Phase 4

**Deliverables:** `SC-WEBSITE-P1-ECOSYSTEM-DECLARATION.md`, `SC-WEBSITE-P1-STRATEGIC-BRIEF.md`,
`SC-WEBSITE-P1-GATE-RECEIPT.json`

---

### PHASE 2: Dossier Content Model

**Primary:** AUD · **Fallback:** CTO · **Co-signers:** CTO (schema), DCS-L0 (publication release)

**What to do:**
- Design the Dossier entry template (schema: fields, rules, required elements)
- Write the sanitation checklist
- Create the evidence standard (how entries prove their claims)
- Select and vet the first five Dossier entries
- Run automated + manual protected-content scans against §0.2 list

**Sanitation checklist must include:**
- Rights and ownership confirmed
- No protected identifiers, case references, or sensitive strategy exposed
- Claims verifiable, or explicitly labeled as lesson/hypothesis
- Accessibility (alt-text for images, captions for video)
- Related products and next steps clear

**Exit gate:**
- Five entries submitted, each with a completed checklist
- Automated scan: **zero matches** against the §0.2 list, list-version hash recorded
- Manual review by a second reader: **zero findings**, reviewer named
- *(v1.0 stated both "100% pass" and "0% false positives"; the metric is now singular — zero
  matches on automated scan AND zero findings on independent manual review. Any automated match is
  triaged and either remediated or documented as a justified exclusion signed by CTO.)*
- Each entry answers: What problem? What approach? What evidence? What changed? What's next?
- DCS-L0 approves the five entries for eventual publication

**Deliverables:** entry schema, sanitation checklist, evidence standard, 5 vetted entries, scan
report, gate receipt

---

### PHASE 3: Sitemap and Content Architecture

**Primary:** CTO · **Fallback:** NAR · **Co-signer:** AUD

**What to do:**
- Design navigation structure (primary menu, hierarchy, cross-links)
- Map discovery paths
- Define separation rules (protected content never in public nav, search, or discovery)
- Design the main-brand → related-brand transition
- Document how metadata and search indexes stay clean

**Three-click discovery test — method (resolves v1.0 unmeasurable gate):**
- Define 10 fixed tasks in advance (e.g. "find how the org approaches X", "find the price of Y")
- Test population: minimum 5 human testers unfamiliar with the sitemap. Model-simulated testers
  may supplement but do not count toward the minimum.
- Success = task completed in ≤3 navigation decisions without backtracking
- **Threshold: ≥80% of task-attempts succeed, AND no single task falls below 60%.**
  A high average that hides one unnavigable page is a fail.

**Exit gate:**
- Complete sitemap (all pages, desktop and mobile hierarchy)
- Three primary journeys documented and tested (awareness → decision → action)
- Discovery test meets both thresholds above, raw per-task results attached
- Search/index rules documented (what's indexed, what's excluded, why)

---

### PHASE 4: Three Visual Directions

**Primary:** AUD · **Fallback:** MMQ · **Co-signers:** CTO (feasibility), DCS-L0 (selection)

**What to do:**
- Produce three materially different directions from the Phase 1 strategic brief
- Direction 1 Editorial/publication · Direction 2 Business/service · Direction 3 Living/experiential
- For each: visual specification, representative mockups, clarity assessment

**Platform feasibility screen (new in v1.1 — prevents Phase 7 rework):**
Before selection, CTO scores each direction against the production platform's real constraints:
custom-component support, motion capability, CMS data-shape fit, form/logic support, performance
headroom. Each direction is rated BUILDABLE / BUILDABLE-WITH-COMPROMISE (compromises itemized) /
NOT BUILDABLE. **A NOT BUILDABLE direction cannot be selected.** This screen exists because a
direction chosen on aesthetics alone can be undeliverable on-platform, and that failure surfaces
at Phase 7 when the cost of change is highest.

**Exit gate:**
- Three directions, each with 5+ representative visual comps
- Visual specification each (hex codes, font scale, component patterns, motion rules)
- Scorecard across: brand alignment, proof clarity, conversion clarity, accessibility, motion
  quality, **and platform feasibility**
- Zero prohibited copying (original work; aesthetic references only, never trade dress)
- DCS-L0 selects one direction in writing

---

### PHASE 5: Responsive Prototype

**Primary:** CTO · **Fallback:** AUD · **Co-signer:** AUD (isolation inspection)
**Entry gate additionally requires §0.3 toolchain verification with zero FAIL rows.**

**What to do:**
- Build a working off-platform prototype of the selected direction
- Pages: home, Dossier index, one sample entry, product index, one product page, philosophy,
  related-brand reveal, call-to-action
- Responsive 320px → 1440px+
- Accessible to WCAG 2.1 AA
- Test protected-content isolation
- Establish performance baseline

**Exit gate:**
- Repository created and versioned; prototype on a feature branch
- Responsive: all pages pass visual review at 320, 768, 1024, 1440
- Accessibility (split into a claimable form — v1.0's "100% WCAG AA" was not an achievable
  automated assertion):
  - Automated (axe or equivalent): **zero violations** at all four breakpoints
  - Manual: keyboard-only traversal of all three primary journeys succeeds; visible focus on every
    interactive element; alt-text present and meaningful on every non-decorative image; contrast
    verified on all text/background pairs including hover and disabled states
  - Both recorded with tool version and date
- Protected-content isolation: automated verification proves protected content cannot reach
  prototype output, including page source, JSON payloads, sitemap, and build artifacts
- Performance baseline, scoped: **Lighthouse Performance ≥90, mobile emulation, simulated Slow 4G,
  median of 5 runs**; LCP <2.5s; CLS <0.1. Raw run data attached (§0.6 — no projected figures).

---

### PHASE 6: Visual Assets & Media Production

**Primary:** AUD · **Fallback:** MMQ · **Co-signer:** MMQ (independent QA)

**What to do:**
- Generate campaign imagery, feature art, and motion studies per the selected direction
- Produce one Dossier story video (30-90s)
- Create brand-aligned variants
- Document every asset: source/lineage, rights status, optimization, accessibility
- Quality assurance pass

**Per-asset requirements:** filename and dimensions · rights status (created/licensed/public
domain) · optimized · accessible (alt-text or captions) · lineage documented

**Exit gate:**
- All assets carry complete metadata
- Zero broken images, zero missing captions
- Quality review passed by AUD **and independently by MMQ** (a producer does not clear their own
  output)
- Video includes captions and meets audio standard
- **Protected-content scan extended to assets (new in v1.1):** scan covers filenames, alt-text,
  captions, lineage notes, embedded EXIF/XMP metadata, and any visible text rendered inside images
  or video frames. v1.0 ran no scan between Phase 5 and Phase 7, leaving asset metadata — the most
  likely leak surface in this phase — unchecked.

---

### PHASE 7: Production Implementation & Testing

**Primary:** DBA · **Fallback:** CTO · **Co-signer:** CTO (isolation re-test)

**Pre-work — mandatory before any modification (new in v1.1):**
- Full audit and inventory of the current live site
- **Verified backup of the existing site and its content**, with a documented and *executed*
  restore test proving the backup is usable
- Before-state performance and content capture
- v1.0 permitted production changes with no captured prior state and no proven revert path.
  **No modification to the live platform begins until the restore test passes.**

**What to do:**
- Move the prototype into the live platform
- Implement all components, forms, and dynamic logic
- Test on the live platform: rendering, form submission and backend actions, all links (no 404s),
  responsive parity with prototype, accessibility retest, protected-content isolation retest
- Set up analytics and measurement baseline
- Prepare and **test** the rollback plan

**Exit gate:**
- UAT: all primary journeys work, zero critical bugs
- Responsive re-run: desktop, tablet, mobile pass
- Accessibility re-audit meets the Phase 5 split standard (automated zero + manual pass)
- Protected-content isolation re-test: zero matches, list-version hash recorded
- Analytics firing correctly; baseline captured from live instrumentation (§0.6)
- Rollback plan documented **and rehearsed at least once**, with the rehearsal recorded

---

### PHASE 8: Launch and Measurement

**Primary:** DBA (execution) · **Fallback:** CTO · **Approval:** DCS-L0

**Release authority (restored in v1.1 — the single most important correction to v1.0):**
Go-live is a **DCS Level 0 decision only**. No model, under any delegated authority, schedule
pressure, or fallback provision, may authorize publication. DBA executes only after written DCS-L0
approval referencing the Phase 7 gate receipt. v1.0 listed Phase 8 leadership as "Technical
authority," which would have permitted an agent to self-approve launch.

**Entry gate:** Phase 7 `completed` (DCS-accepted, not self-declared) · release-readiness brief
submitted to DCS-L0 · DCS-L0 written approval recorded in the decision log.

**What to do:**
- Publish from staging to production
- Monitor launch metrics (performance, errors, visitor behavior)
- Measure engagement, capture early feedback, document lessons learned

**Measurement focus (4 weeks post-launch), all live-sourced per §0.6:**
- Dossier engagement: views, time-on-page, share rate by entry
- Product progression: service interest, inquiry completion rate
- Media performance: video watch-time, image click-through
- Visitor action: consultation inquiries, form submissions, signups
- Performance: Core Web Vitals stable, error rate, load times

**Exit gate (observational, no approval gate):**
- Baseline metrics recorded and compared against the Phase 7 captured baseline
- Early lessons captured
- Feedback compiled
- Next-iteration input prepared
- **Post-launch protected-content scan on the live production surface**, including the public
  search index and social/link previews, at 24 hours and at 4 weeks

---

## ENTRY & EXIT GATES SUMMARY

| Phase | Primary | Entry Gate | Exit Gate |
| :--- | :--- | :--- | :--- |
| 1 | CTO | DCS direction provided; roster confirmed | Product families locked (DCS-L0), protected rules written, term list published, brief accepted |
| 2 | AUD | Phase 1 `completed` | 5 entries vetted; automated scan zero matches; manual review zero findings; DCS-L0 publication approval |
| 3 | CTO | Phase 2 `completed` | Sitemap complete; 3 journeys tested; discovery ≥80% overall and ≥60% per task; index rules documented |
| 4 | AUD | Phase 3 `completed` | 3 directions + comps; scorecard incl. platform feasibility; no NOT BUILDABLE selection; DCS-L0 selects |
| 5 | CTO | Phase 4 selection; toolchain zero FAIL | Responsive at 4 breakpoints; axe zero + manual pass; isolation test zero matches; scoped perf baseline |
| 6 | AUD | Phase 5 `completed` | Asset metadata complete; dual QA (AUD + MMQ); asset-surface scan zero matches |
| 7 | DBA | Phase 6 `completed`; backup restore test passed | UAT clean; isolation re-test; live analytics baseline; rollback rehearsed |
| 8 | DBA | Phase 7 `completed`; **DCS-L0 written go-live approval** | Launch executed; 4-week measurement; lessons captured; post-launch scans at 24h and 4w |

---

## PROTECTED CONTENT HANDLING

**Principle:** Protected content exists in the org but never appears in public outputs, public
search indexes, or public navigation.

**Verification runs at Phases 2, 5, 6, 7, and 8** (v1.0 ran 5/7/8 only):
- Protected content cannot be retrieved through public pages
- Protected content is not indexed in public search
- Protected content is not present in public metadata, previews, or asset metadata
- Automated scan against the §0.2 list **and** independent manual review both confirm zero leakage
- A scan without a resolvable list-version hash is a failed scan

**If protected content is detected:**
- Halt that phase immediately
- Remediate the leakage
- Re-test before proceeding
- Notify DCS-L0 within the same working session
- No exceptions, no workarounds, no schedule-based waivers

---

## COORDINATION RULES

**Phase handoffs:**
- Each phase has one Primary, one Fallback, and where specified a mandatory co-signer
- Only the Primary declares the exit gate met; the co-signer's approval is independent and
  required — it is not a formality and cannot be waived by the Primary
- If the Primary is unavailable, the Fallback may act and must document the substitution
- DCS-L0 has no fallback. Where DCS-L0 approval is required, work waits.
- All approvals logged to `DECISION_LOG.md`: who decided, when, on what evidence

**Escalation:**
- Surface an unmet gate immediately; do not carry it forward silently
- Do not skip gate criteria to hold schedule
- Options: (a) remediate and re-test, (b) modify gate criteria — **DCS-L0 only, logged with
  rationale**, (c) extend timeline

**Quality rule:**
- Every deliverable must be usable by the next phase without rework
- If a downstream phase rejects upstream output as incomplete, the upstream phase redoes the work
- No handoffs carrying debt or workarounds

---

## SUCCESS CRITERIA

✓ **Measurable** — every gate has a quantified criterion with a stated measurement method
✓ **Accountable** — every phase has a named Primary, Fallback, and co-signer
✓ **Safe** — protected content is defined, scanned at five phases, and halts work on detection
✓ **Reversible** — no production change without a proven backup and a rehearsed rollback
✓ **Authorized** — publication requires DCS-L0 and cannot be delegated
✓ **Evidence-based** — no placeholder or projected figure is ever presented as a result
✓ **Transparent** — decisions logged, blockers surfaced, remediation documented

---

## HOW TO USE THIS PROMPT

**For each phase:**
1. Read the phase section (objective, work, roster, exit gate)
2. Confirm the entry gate: is the prior phase `completed` (DCS-accepted, not self-declared)?
3. Execute the phase work
4. Meet every exit-gate criterion and attach evidence for each
5. Emit the gate receipt and move the task to `needs_review`
6. Wait for DCS acceptance. Acceptance — not your own report — opens the next phase.

**If blocked:**
- Name the specific unmet criterion
- State why it cannot pass
- Route to the Primary, then DCS-L0 if criteria modification is sought
- Log the decision, then proceed

**If distributed to multiple models:**
- Read the full prompt once for whole-cycle context
- Take only the role assigned to you in §0.1 — do not self-assign
- Coordinate at gates; never cross a gate unilaterally
- Document every decision and handoff

---

## PHASE 1 ENTRY CHECKLIST

- [ ] DCS Level 0 direction/approval received
- [ ] Executor roster (§0.1) confirmed; every code mapped to a real, available executor
- [ ] Protected-terms list (§0.2) owner assigned with a delivery date
- [ ] Artifact destinations (§0.4) created
- [ ] Completion semantics (§0.5) acknowledged by every executor
- [ ] This prompt read and acknowledged by all executors
- [ ] Phase 1 resources (research, tools, access) available

Once every box is checked, proceed with Phase 1: Ecosystem Declaration.

---

**Version:** 1.1
**Last Updated:** 2026-08-10
**Status:** Ready for distribution — Phase 1 blocked on DCS Level 0 entry approval
