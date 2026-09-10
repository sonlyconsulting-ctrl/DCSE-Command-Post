# SC.COM DOSSIER WEBSITE — BUILD PLAN & EXECUTION PROMPT
**Task ID:** SC-AI-RFP-SIM-001
**Lane:** SC (Product Campaign)
**Phases:** 1-8 (Complete Build Cycle)
**Date:** 2026-08-10
**Status:** Ready for Execution
**Source:** Sonly Consulting — AI RFP Simulation Exercise

---

## OBJECTIVE

Build SC.com as a **Dossier website**: a proof-first platform demonstrating organizational capabilities through real work, decisions, and outcomes. The site serves as both a public proof engine and an internal product demonstration.

**Core Directive:** Show the work. Do not describe capabilities generically — demonstrate them through structured proof: problems solved, decisions made, tradeoffs considered, results achieved, lessons learned.

---

## SITE FEATURES

- Curated Dossier entries (work samples, decision records, case studies)
- Product and service catalog
- Company philosophy and approach
- Related brand presence with distinct fingerprints
- Protected content architecture (isolated, never public-facing)

---

## PHASES 1-8: BUILD CYCLE

### PHASE 1: Ecosystem Declaration

**What to do:**
- Lock product families and service boundaries
- Define Dossier purpose: what counts as "approved public work"?
- Establish protected content rules: what never appears publicly and why
- Map visitor journeys: what should someone learn in three clicks?

**Exit gate (team consensus required):**
- Every proposed page maps to one lane, one audience purpose, one clear conversion outcome
- Product families stated and locked
- Dossier publishing rules written down
- Protected content explicitly excluded with reason
- Team confirms: "We know what we're building"

---

### PHASE 2: Dossier Content Model

**What to do:**
- Design Dossier entry template (schema: fields, rules, required elements)
- Write sanitation checklist (what must be verified before any entry goes public?)
- Create evidence standard (how do entries prove their claims?)
- Select and vet first five Dossier entries for publication
- Ensure zero protected content leakage through automated and manual checks

**Sanitation checklist must include:**
- Rights and ownership confirmed
- No protected identifiers, case references, or sensitive strategy exposed
- Claims verifiable or labeled as lesson/hypothesis
- Accessibility (alt-text for images, captions for video)
- Related products and next steps clear

**Exit gate:** Five entries vetted, sanitation 100% pass, protected content scan zero false positives.

---

### PHASE 3: Sitemap and Content Architecture

**What to do:**
- Design navigation structure (primary menu, hierarchy, cross-links)
- Map discovery paths (can visitors learn the org's perspective in three clicks?)
- Define separation rules (protected content never appears in public navigation, search, or discovery)
- Design transition between main brand and related brand (if applicable)
- Document how metadata and search indexes stay clean

**Exit gate:** Complete sitemap, three primary user journeys documented and tested (80%+ success), search/index rules documented.

---

### PHASE 4: Three Visual Directions

**What to do:**
- Produce three materially different design directions from the same strategic brief
- Direction 1: Editorial/publication (strong masthead, recurring departments, proof-focused)
- Direction 2: Business/service (clear value proposition, service pathways, consultation focus)
- Direction 3: Living/experiential (motion, recurring features, brand reveal pathway)
- For each: visual specification (colors, fonts, layout patterns), representative mockups, clarity assessment

**Exit gate:** Three directions each with 5+ visual comps, scorecard complete, direction selected by team before Phase 5.

---

### PHASE 5: Responsive Prototype

**What to do:**
- Build working prototype of selected direction (off-platform)
- Pages: home, Dossier index, one sample Dossier entry, product index, one product page, philosophy section, related-brand reveal, call-to-action
- All pages responsive (320px mobile through 1440px+ desktop)
- All pages accessible (WCAG 2.1 AA)
- Test protected content isolation: verify protected content cannot be retrieved through public pages, search, or indexes
- Establish performance baseline (Lighthouse 90+, LCP <2.5s, CLS <0.1)

**Exit gate:** Prototype responsive at all breakpoints, accessible (WCAG AA), protected content test 100% pass.

---

### PHASE 6: Visual Assets & Media Production

**What to do:**
- Generate campaign imagery, feature art, and motion studies per selected design direction
- Produce one short Dossier story video (30-90 seconds)
- Create brand-aligned variants (multiple compositions, tonal variations)
- Document all assets: source/lineage, rights status, optimization technique, accessibility
- Quality assurance pass (brand consistency, image optimization, motion smoothness)

**Exit gate:** All assets QA-passed, metadata complete, zero missing captions/alt-text.

---

### PHASE 7: Production Implementation & Testing

**What to do:**
- Move prototype into live platform
- Implement all components, forms, and dynamic logic
- Run comprehensive testing:
  - All pages render correctly
  - All forms submit and trigger proper backend actions
  - All links work (no 404s)
  - Responsive behavior matches prototype
  - Accessibility preserved (retest WCAG AA)
  - Protected content isolation still passes
- Set up analytics and measurement baseline
- Prepare rollback plan

**Exit gate:** UAT complete, protected content re-verified, analytics baseline established, rollback tested.

---

### PHASE 8: Launch and Measurement

**What to do:**
- Publish site live (promotion from staging to production)
- Monitor launch metrics (performance, errors, visitor behavior)
- Measure engagement: Dossier article views, product-page progression, visitor actions
- Capture early feedback (visitor inquiries, support requests, behavior patterns)
- Document lessons learned

**Measurement focus (4 weeks post-launch):**
- Dossier engagement: views, time-on-page, share rate
- Product progression: service interest, inquiry completion rate
- Media performance: video watch-time, image click-through
- Visitor action: consultation inquiries, contact form submissions, newsletter signups
- Performance: Core Web Vitals stable, error rates near zero

**Exit gate:** 4-week window, baseline metrics recorded, lessons captured, next-iteration input prepared.

---

## ENTRY & EXIT GATES SUMMARY

| Phase | Entry Gate | Exit Gate |
| :--- | :--- | :--- |
| 1 | DCS direction provided | Product families locked, protected rules written, team alignment confirmed |
| 2 | Phase 1 approved | Five entries vetted, sanitation 100% pass, protected content scan 0% false positives |
| 3 | Phase 2 approved | Sitemap complete, three journeys tested (80%+ success), navigation rules documented |
| 4 | Phase 3 approved | Three directions with comps, scorecard complete, direction selected by team |
| 5 | Phase 4 direction selected | Prototype responsive, accessible (WCAG AA), protected content test 100% pass |
| 6 | Phase 5 approved | All assets QA-passed, metadata complete, zero missing captions/alt-text |
| 7 | Phase 6 approved | UAT complete, protected content re-verified, analytics baseline established, rollback tested |
| 8 | Phase 7 approved | Launch executed, 4-week measurement window, lessons captured |

---

## PROTECTED CONTENT HANDLING

**Principle:** Protected content exists in the organization but never appears in public outputs, public search indexes, or public navigation.

**Verification (runs at Phase 5, Phase 7, and Phase 8):**
- Protected content cannot be retrieved through public pages
- Protected content is not indexed in public search
- Protected content is not mentioned in public metadata or previews
- Automated scan + manual review both confirm zero leakage

**If protected content is detected:**
- Halt that phase immediately
- Remediate the leakage
- Re-test before proceeding
- No exceptions, no workarounds

---

## COORDINATION RULES

**Phase handoffs:**
- Each phase has a primary authority and a fallback
- Only the primary authority can approve exit from that phase
- If primary is unavailable, fallback can approve and document the substitution
- All approvals logged (who decided, when, what evidence)

**Escalation:**
- If a phase cannot meet its exit gate, surface the blocker immediately
- Do not skip gate criteria to maintain schedule
- Options: (a) remediate and re-test, (b) modify gate criteria (rare, requires team discussion), (c) extend timeline

**Quality rule:**
- Every deliverable at every phase must be usable by the next phase without rework
- If downstream phase rejects Phase N output as incomplete, Phase N redoes work
- No hand-offs with debt or workarounds

---

## SUCCESS CRITERIA

- **Measurable:** Every phase has quantified exit gate (test pass rate, entry count, etc.)
- **Autonomous:** Teams know their phase scope and exit criteria; no mid-phase ambiguity
- **Safe:** Protected content never escapes; verification runs at critical phases
- **Transparent:** All decisions logged, all blockers surfaced, all remediation documented
- **Deliverable:** Phase 8 produces a live website that demonstrates the org's work through proof-first content

---

## HOW TO USE THIS PROMPT

**For each phase:**
1. Read the phase section (objective, what to do, exit gate)
2. Align on entry gate (previous phase passed? resources ready?)
3. Execute the phase work
4. Meet exit gate criteria (all checkpoints pass)
5. Signal completion: "Phase N exit gate met, ready for Phase N+1"
6. Proceed to next phase

**If blocked:**
- Identify which gate criterion is not met
- Surface the blocker (why can't it pass?)
- Decide: remediate, modify criteria, or extend timeline
- Log the decision and proceed

**If distributed to multiple models/team members:**
- Read full prompt once (get context for all 8 phases)
- Specialize: take the role suited to your strength (editorial, technical, strategy, design)
- Coordinate at phase gates (team alignment before proceeding)
- Document decisions and handoffs

---

## TOOLCHAIN VERIFICATION (Pre-Phase 5)

Before Phase 5 begins, verify access to all critical tools:
1. Website platform (Wix or equivalent) — functional, credentials current
2. Database (Supabase) — connection tested, schemas accessible
3. Version control (GitHub) — push/pull working, branch protection configured
4. Deployment (Vercel) — staging and production access confirmed
5. Design tools (Figma or equivalent) — team access verified
6. Analytics (Google Analytics or equivalent) — tags firing, dashboard accessible
7. Media tools (FFmpeg or equivalent) — video processing pipeline tested
8. AI model APIs — all assigned models accessible, tokens available

Do not begin Phase 5 until all critical tools are verified functional.

---

## DDNA FEEDBACK LOOP

Throughout all phases, capture signals at five levels:

- **L1 (Sentiment/Voice):** Output tone matches organizational register — precise, load-bearing, zero ornamentation
- **L2 (Logic/Workflow):** Measurable workflow efficiency — hours per phase, test pass rates, artifact counts
- **L3 (Design/Structure):** Reusable patterns in layout, verification gates, component libraries
- **L4 (Product/Components):** Reusable templates for task allocation, evidence recording, phase handoffs
- **L5 (Technical/Performance):** API access, schema stability, performance baselines, error patterns

Capture signals continuously. Compile into "next iteration input" at Phase 8 close.

---

## OPEN ITEMS (Awaiting Resolution)

| # | Item | Owner | Due | Status |
|---|------|-------|-----|--------|
| 1 | Editorial/PS firewall audit review | Lead Systems Auditor | 2026-08-12 | Pending |
| 2 | Architecture review & sign-off | CTO Authority | 2026-08-12 | Pending |
| 3 | Toolchain verification & pre-Phase 5 checklist | DBA/Infrastructure | 2026-08-15 | Pending |
| 4 | DCS Level 0 Phase 1 approval gate | DCS Authority | 2026-08-15 | Pending |
| 5 | Phase 1 execution package assembly | CTO + Project Lead | 2026-08-20 | Conditional on #4 |
| 6 | DDNA asset lifecycle management | DDNA Lead + Registry | Ongoing | TBD |
| 7 | PS firewall test pass (Phase 5 gate) | CTO + DBA | ~2026-09-14 | TBD Phase 5 |
| 8 | Analytics measurement plan setup | CTO + DBA | ~2026-10-15 | TBD Phase 7 |
| 9 | Documentation & lesson capture (Phase 8) | CTO + Project Lead | ~2026-11-15 | TBD Phase 8 |

**Critical path:** Items 1-4 must complete in sequence to unblock Phase 1.
Estimated total time to Phase 1 start: 10-12 business days from 2026-08-10.

---

**Ready to begin Phase 1?**

Confirm entry criteria:
- [ ] DCS direction/approval received
- [ ] Team members assigned and briefed
- [ ] This prompt read and understood by all team members
- [ ] Phase 1 resources (research, tools, access) available

Once confirmed, proceed with Phase 1: Ecosystem Declaration.

---

**Prepared by:** Sonly Consulting — AI RFP Simulation Exercise
**Last Updated:** 2026-08-10
**Status:** Ready for distribution and execution
