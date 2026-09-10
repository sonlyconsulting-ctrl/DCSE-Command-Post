# SC.COM DOSSIER WEBSITE BUILD PLAN
**Task ID:** SC-WEBSITE-BUILD-DOSSIER-001  
**Lane:** SC  
**Phases:** 1-8 (Complete Build Cycle)  
**Status:** Ready for Team Execution  
**Distribution:** Via Poller to All Team Members

---

## OBJECTIVE

Build SC.com as a **Dossier website**: a proof-first platform that demonstrates the organization's capabilities through real work, decisions, and outcomes. The website serves as both a public proof engine and an internal product demonstration.

The site will feature:
- Curated Dossier entries (work samples, decision records, case studies)
- Product and service catalog
- Company philosophy and approach  
- Related brand presence with distinct fingerprints
- Protected content architecture (isolated, not public-facing)

---

## CORE DIRECTIVE

**Show the work.** The website does not describe capabilities generically; it demonstrates them through structured proof: problems solved, decisions made, tradeoffs considered, results achieved, and lessons learned.

---

## PHASES 1-8: BUILD CYCLE

### **PHASE 1: Ecosystem Declaration**

**What to do:**
- Lock product families and service boundaries (what the org sells/offers)
- Define Dossier purpose: what counts as "approved public work"?
- Establish protected content rules: what never appears publicly and why
- Map visitor journeys: what should someone learn in three clicks?

**Who leads:** Primary (strategy authority), Fallback (narrative continuity)

**Exit gate (team consensus required):**
- Every proposed page maps to one lane, one audience purpose, one clear conversion outcome
- Product families stated and locked (no ambiguity)
- Dossier publishing rules written down
- Protected content explicitly excluded with reason
- Team confirms: "We know what we're building"

**Next:** Request Phase 2 approval only after exit gate passes

---

### **PHASE 2: Dossier Content Model**

**What to do:**
- Design the Dossier entry template (schema: fields, rules, required elements)
- Write sanitation checklist (what must be verified before any entry goes public?)
- Create evidence standard (how do entries prove their claims?)
- Select and vet first five Dossier entries for publication
- Ensure zero protected content leakage through automated and manual checks

**Who leads:** Editorial authority, Fallback (strategic review)

**Sanitation checklist must include:**
- Rights and ownership confirmed
- No protected identifiers, case references, or sensitive strategy exposed
- Claims verifiable or labeled as lesson/hypothesis
- Accessibility (alt-text for images, captions for video)
- Related products and next steps clear

**Exit gate (all five entries vetted, zero failures on sanitation):**
- Five entries submitted with completed checklist
- Protected content scan: 100% pass (no protected keywords, entities, or references detected)
- Each entry answers: What problem? What approach? What evidence? What changed? What's next?
- Team confirms: "We can publish these safely"

**Next:** Request Phase 3 approval only after exit gate passes

---

### **PHASE 3: Sitemap and Content Architecture**

**What to do:**
- Design navigation structure (primary menu, hierarchy, cross-links)
- Map discovery paths (how do visitors find what they need? Test: can they learn the org's perspective in three clicks?)
- Define separation rules (protected content never appears in public navigation, search, or discovery)
- Design the transition between main brand and related brand (if applicable)
- Document how metadata and search indexes stay clean (no protected content indexed)

**Who leads:** Information architecture authority, Fallback (narrative continuity)

**Exit gate (tested and confirmed):**
- Complete sitemap (all pages, desktop and mobile hierarchy)
- Three primary user journeys documented and tested (awareness → decision → action)
- Three-click discovery test: 80%+ success rate (visitors find what they're looking for)
- Search/index rules documented (what's indexed, what's excluded, why)
- Team confirms: "Visitors can navigate and find things"

**Next:** Request Phase 4 approval only after exit gate passes

---

### **PHASE 4: Three Visual Directions**

**What to do:**
- Produce three materially different design directions from the same strategic brief
- Each direction should feel distinct (different color palette, typography, imagery style, motion language)
- Direction 1: Editorial/publication (strong masthead, recurring departments, proof-focused)
- Direction 2: Business/service (clear value proposition, service pathways, consultation focus)
- Direction 3: Living/experiential (motion, recurring features, brand reveal pathway, community elements)
- For each direction: visual specification (colors, fonts, layout patterns), representative mockups, and clarity assessment

**Who leads:** Design authority, Fallback (visual continuity)

**Exit gate (three directions complete, scorecard done):**
- Three directions each with 5+ representative visual comps
- Visual specification for each (hex codes, font scale, component patterns, motion rules if applicable)
- Design scorecard comparing all three across: brand alignment, proof clarity, conversion clarity, accessibility, motion quality
- Zero prohibited copying (all work is original; aesthetic references only, not trade dress)
- Team selects one direction before Phase 5 begins

**Next:** Once direction is selected, request Phase 5 approval

---

### **PHASE 5: Responsive Prototype**

**What to do:**
- Build a working prototype of the selected direction (not Wix yet; off-platform if possible)
- Pages needed: home, Dossier index, one sample Dossier entry, product index, one product page, philosophy section, related-brand reveal, call-to-action page
- All pages responsive (works on 320px mobile through 1440px+ desktop)
- All pages accessible (WCAG 2.1 AA standard: color contrast, keyboard navigation, alt-text complete)
- Test protected content isolation: verify that protected content cannot be retrieved through public pages, search, or indexes
- Establish performance baseline (load time, Core Web Vitals)

**Who leads:** Technical authority, Fallback (visual QA)

**Exit gate (all criteria met, protected content test passes 100%):**
- Prototype code repository created and versioned
- Responsive testing: all pages pass visual review at 5 breakpoints (320, 768, 1024, 1440+)
- Accessibility audit: 100% WCAG AA compliance (no contrast failures, keyboard nav works, alt-text complete)
- Protected content isolation test: automated verification proves protected content cannot reach prototype output
- Performance baseline established (Lighthouse 90+, LCP <2.5s, CLS <0.1)
- Team confirms: "This looks right and works everywhere"

**Next:** Request Phase 6 approval only after exit gate passes

---

### **PHASE 6: Visual Assets & Media Production**

**What to do:**
- Generate high-end campaign imagery, feature art, and motion studies per the selected design direction
- Produce one short Dossier story video (30-90 seconds, can be sample entry or brand introduction)
- Create brand-aligned variants (multiple compositions, tonal variations)
- Document all assets: source/lineage, rights status, optimization technique, accessibility (captions, alt-text)
- Quality assurance pass (brand consistency, image optimization, motion smoothness)

**Who leads:** Visual/media production authority, Fallback (quality review)

**Asset requirements per item:**
- Filename and dimensions documented
- Rights status clear (created, licensed, public domain)
- Optimized (compressed, fast-loading)
- Accessible (alt-text or captions present)
- Lineage documented (what process created this?)

**Exit gate (all assets QA-passed, metadata complete):**
- All assets have complete metadata (lineage, rights, alt-text, optimization notes)
- Zero broken images or missing captions
- Quality review passed (brand consistency, no rendering errors, motion smooth)
- Video includes captions and meets audio standard
- Team confirms: "All assets ready for production"

**Next:** Request Phase 7 approval only after exit gate passes

---

### **PHASE 7: Production Implementation & Testing**

**What to do:**
- Move the prototype into the live platform (Wix if applicable)
- Implement all components, forms, and dynamic logic
- Run comprehensive testing on live platform:
  - All pages render correctly
  - All forms submit and trigger proper backend actions
  - All links work (no 404s)
  - Responsive behavior matches prototype
  - Accessibility preserved (retest WCAG AA)
  - Protected content isolation still passes (no protected content accessible from production)
- Set up analytics and measurement baseline (which metrics matter? what's the baseline from staging?)
- Prepare rollback plan (if something breaks at launch, how do we revert?)

**Who leads:** Technical authority, Fallback (visual QA)

**Exit gate (UAT complete, protected content re-verified, measurement ready):**
- User acceptance testing: all primary journeys work (no critical bugs)
- Responsive testing re-run: desktop, tablet, mobile all pass
- Accessibility re-audit: WCAG AA still met
- Protected content isolation re-test: 100% pass (no protected data accessible)
- Analytics tags firing correctly (all conversion events tracked, baseline established)
- Rollback plan documented and tested
- Team confirms: "Ready for go-live"

**Next:** Request Phase 8 (launch) approval only after exit gate passes

---

### **PHASE 8: Launch and Measurement**

**What to do:**
- Publish the site live (promotion from staging to production)
- Monitor launch metrics (performance, errors, visitor behavior)
- Measure engagement: Dossier article views, product-page progression, visitor actions
- Capture early feedback (visitor inquiries, support requests, behavior patterns)
- Document lessons learned: what worked, what needs improvement, which assumptions held

**Who leads:** Technical authority (go-live execution), Fallback (ops monitoring)

**Measurement focus (4 weeks post-launch):**
- Dossier engagement: which entries get most views, time-on-page, share rate
- Product progression: which services generate most interest, inquiry completion rate
- Media performance: video watch-time, image click-through, feature engagement
- Visitor action: consultation inquiries, contact form submissions, newsletter signups
- Performance: Core Web Vitals stable, error rates near zero, load times consistent

**Exit gate (4-week window, no gate required; observational):**
- Baseline metrics recorded and compared to staging projection
- Early lessons captured (what surprised us? what should we change?)
- Feedback compiled (visitor inquiries, patterns, requests)
- Next-iteration input prepared (what did we learn for v2?)

**Next:** Plan Phase 1 of next iteration based on Phase 8 lessons

---

## ENTRY & EXIT GATES SUMMARY

| Phase | Entry Gate | Exit Gate |
| :--- | :--- | :--- |
| 1 | DCS direction provided | Product families locked, protected rules written, team alignment confirmed |
| 2 | Phase 1 approved | Five entries vetted, sanitation 100% pass, protected content scan 0% false positives |
| 3 | Phase 2 approved | Sitemap complete, three journeys tested (80%+ success), navigation rules documented |
| 4 | Phase 3 approved | Three directions with comps, scorecard complete, direction selected by team |
| 5 | Phase 4 direction selected | Prototype responsive (all breakpoints), accessible (WCAG AA), protected content test 100% pass |
| 6 | Phase 5 approved | All assets QA-passed, metadata complete, zero missing captions/alt-text |
| 7 | Phase 6 approved | UAT complete, protected content re-verified, analytics baseline established, rollback tested |
| 8 | Phase 7 approved | Launch executed, 4-week measurement window, lessons captured |

---

## PROTECTED CONTENT HANDLING

**Principle:** Protected content exists in the org but never appears in public outputs, public search indexes, or public navigation.

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

✓ **Measurable:** Every phase has quantified exit gate (test pass rate, entry count, etc.), not subjective approval  
✓ **Autonomous:** Teams know their phase scope and exit criteria; no mid-phase ambiguity  
✓ **Safe:** Protected content never escapes; verification runs at critical phases  
✓ **Transparent:** All decisions logged, all blockers surfaced, all remediation documented  
✓ **Deliverable:** Phase 8 produces a live website that demonstrates the org's work through proof-first content

---

## HOW TO USE THIS PROMPT

**For each phase:**
1. Read the phase section (objective, what to do, who leads, exit gate)
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

**Ready to begin Phase 1?**

Confirm entry criteria:
- [ ] DCS direction/approval received
- [ ] Team members assigned and briefed
- [ ] This prompt read and understood by all team members
- [ ] Phase 1 resources (research, tools, access) available

Once confirmed, proceed with Phase 1: Ecosystem Declaration.

---

**Last Updated:** 2026-08-10  
**Status:** Ready for distribution and execution
