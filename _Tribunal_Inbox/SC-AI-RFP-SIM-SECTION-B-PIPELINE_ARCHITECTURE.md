# SECTION B: AUTOMATED PIPELINE & DDNA INTEGRATION
**Task ID:** SC-AI-RFP-SIM-001  
**Doctrine Refs:** D16 (DDNA extraction), D21 §11 (PS firewall), D02 (verification gates)  
**Status:** COMPLETE

---

## 1. DDNA FEEDBACK LOOP ARCHITECTURE (D16 Integration)

The website build pipeline captures reusable signals automatically at five layers. Each layer feeds into the next iteration's content, design, and technical decisions.

### 1.1 Layer 1 — Sentiment (Voice, Tone, Emotional Register)

**Definition:**  
L1 captures the emotional resonance and voice consistency across all content produced during the build.

**Extraction Points:**

| Phase | Extraction Trigger | Signal Captured | Measurement |
| :--- | :--- | :--- | :--- |
| Phase 1 | Product declaration and fingerprint definition | SC masthead voice establishment (precision, authority, forward-looking tone). SS reveal-moment emotional tone. | Qwen audit log: tone consistency check across three product-declaration drafts. |
| Phase 2 | Dossier entry drafting | Consistency of editorial register across five candidate entries. Does tone match "authored dossier" directive or slip toward generic agency voice? | Qwen editorial audit: tone deviation log and correction set. |
| Phase 5 | Prototype component copy | Do page titles, CTAs, and descriptive text maintain consistent voice across all six major pages? | Manual review: tone consistency matrix across (home, Dossier index, entry, product, philosophy, SS reveal). |
| Phase 6 | Media production (captions, alt-text, motion pacing) | Does video narration, image captions, and motion timing reinforce or contradict defined SC sentiment? | Qwen media audit: voice consistency on video/motion, alt-text tone alignment. |
| Phase 8 | Post-launch content review | Which Dossier entries or product pages generated strongest engagement? Which voice patterns appear in reader comments, inquiry forms, or feedback? | Analytics integration: sentiment-tagged engagement data feeds next iteration voice tuning. |

**Feedback Loop:**  
L1 signals captured in Phase 2-5 → Fed to Qwen (audit lead) → Voice corrections applied to Phase 5 prototype → Phase 6 media production uses refined voice → Phase 8 engagement data validates which tone patterns work → Next iteration inherits validated voice fingerprint.

**Evidence Output:**  
- Qwen editorial audit log with tone deviations flagged and corrected
- Voice consistency matrix showing alignment across all content
- Media production voice QA report
- Engagement sentiment report (Phase 8)

---

### 1.2 Layer 2 — Logic (Workflow, Routing, Decision Gates)

**Definition:**  
L2 captures workflow efficiency, routing patterns, decision-gate success rates, and where automation breaks down.

**Extraction Points:**

| Phase | Extraction Trigger | Signal Captured | Measurement |
| :--- | :--- | :--- | :--- |
| Phase 1 | Product declaration → DCS approval cycle | Time elapsed from phase exit to DCS approval decision. Where did work stall? Which assumptions required re-work? | Phase duration log and DCS gate completion time. |
| Phase 2 | Dossier entry creation → PS sanitation review → publication acceptance | Entry creation time, sanitation-checklist pass rate, rework cycles. Do entries fail on specific sanitation criteria? | Qwen audit: PS-firewall failure analysis and remediation time per entry. |
| Phase 3 | Sitemap creation → IA testing → discovery-journey validation | IA testing success rate (did visitors complete three-decision journey on first try?). Which navigation patterns failed? | IA test results: success rate, failed pathways, required revisions. |
| Phase 5 | Prototype component build → responsive testing → sign-off | Component build time, responsive-breakpoint failures, accessibility audit rework. Which components took longest? | Development log: time per component, test failures by breakpoint. |
| Phase 7 | Staging implementation → UAT → production readiness | UAT bug discovery rate, false starts on Wix implementation, code-review rework cycles. Which components had highest rework rate? | UAT bug log, code-review checklists, deployment readiness assessment. |

**Feedback Loop:**  
L2 signals captured in Phase 5-7 → Analysis identifies bottlenecks (e.g., "PS-sanitation checks took 40% of Phase 2 effort") → Process refinements applied → Phase 8 measurement tracks whether streamlined workflow reduced Phase 2 time in follow-up build → Efficiency gains documented for template reuse.

**Evidence Output:**  
- Workflow duration log (time per phase, time to DCS gate)
- Bottleneck analysis (which phases had longest rework cycles?)
- Process efficiency metrics (PS-sanitation time, testing time, approval time)
- Recommended process optimizations for next cycle

---

### 1.3 Layer 3 — Design (Visual Language, Typography, Layout Patterns)

**Definition:**  
L3 captures visual patterns, layout choices, accessibility wins, and which design solutions perform in production.

**Extraction Points:**

| Phase | Extraction Trigger | Signal Captured | Measurement |
| :--- | :--- | :--- | :--- |
| Phase 4 | Three visual directions submitted | Core design decisions that distinguish Editorial / Business / Living. Which palette, typography, spacing, and motion choices define each direction? | Design system audit: component inventory, token library, motion-pattern definitions per direction. |
| Phase 5 | Prototype responsive testing | Which layout patterns work across all breakpoints (320px - 1440px+)? Which fail? Which required special mobile adjustments? | Responsive audit: component-by-breakpoint matrix showing pass/fail and required overrides. |
| Phase 6 | Media production (photography, motion, illustration) | Visual themes that repeat across feature imagery, motion studies, video production. Color usage, photography style, motion vocabulary. | Media audit: visual theme analysis, palette consistency check, motion-vocabulary definitions. |
| Phase 7 | Live Wix rendering and browser QA | How do design choices render in production across browsers? Visual regressions? Color shifts? Motion smoothness? | Browser-compatibility audit: rendering issues by browser and OS, visual-regression report. |
| Phase 8 | Engagement measurement | Which design elements (imagery, layout, typography size, color contrast) correlate with higher engagement, longer time-on-page, or conversion? | Analytics: element-level engagement correlation, heatmap analysis, scroll-depth patterns. |

**Feedback Loop:**  
L3 signals captured Phase 5-7 → Qwen visual audit identifies which component patterns are most reusable → Design system documented → Phase 8 engagement data shows which design choices drive behavior → Next iteration inherits visual patterns with evidence of what works → Template reuse accelerates subsequent phases.

**Evidence Output:**  
- Design system and component inventory (reusable patterns, token library)
- Responsive audit report (layout success by breakpoint)
- Visual-regression and browser-compatibility report
- Design-performance correlation report (Phase 8 analytics)

---

### 1.4 Layer 4 — Product (Reusable Components, Offerings, Packages)

**Definition:**  
L4 captures product patterns: which product descriptions, features lists, pricing tiers, and calls-to-action prove effective; which product-page layouts scale to new offerings.

**Extraction Points:**

| Phase | Extraction Trigger | Signal Captured | Measurement |
| :--- | :--- | :--- | :--- |
| Phase 1 | Product family declaration | Which product boundaries are clear? Which require clarification? Do product names align with audience understanding? | Product declaration audit: ambiguities flagged, audience-alignment assessment. |
| Phase 4 | Visual direction scorecard | Which design direction best supports product differentiation? Does layout make product tiers and benefits clear? | Design-direction assessment: clarity of product hierarchy and benefit communication per direction. |
| Phase 5 | Product-page prototype and IA | Product-listing architecture: can users find and compare products? Do related-product suggestions make sense? Is inquiry-funnel logic clear? | IA testing: product-discovery success rate, comparison logic effectiveness, inquiry-funnel completion. |
| Phase 8 | Product-engagement measurement | Which products generate most page views, longest engagement, most inquiries? Which product pages have lowest bounce rate? | Analytics: product-level engagement metrics, inquiry conversion by product, comparison-feature usage rates. |
| Phase 8 (future) | Post-launch feedback | Customer inquiries: which product descriptions create confusion? Which features do prospects ask about most? | Inquiry-form analysis: feature-understanding gaps, pricing-tier confusion patterns. |

**Feedback Loop:**  
L4 signals captured Phase 1-5 → Product patterns identified (e.g., "Custom Digital Campaigns page structure is most effective") → Pattern reused as template → Phase 8 engagement data validates product-tier differentiation → Pricing and package clarity feedback captured → Next product launch uses proven product-page template and information architecture.

**Evidence Output:**  
- Product family clarity audit (ambiguities, audience alignment)
- Product-page performance report (views, engagement, inquiry conversion by product)
- Reusable product-page template and component library
- Product differentiation effectiveness assessment

---

### 1.5 Layer 5 — Technical (APIs, Database Schema, Performance, Error Patterns)

**Definition:**  
L5 captures technical signals: component load times, API response patterns, error logs, token usage efficiency, and architecture decisions that did or did not scale.

**Extraction Points:**

| Phase | Extraction Trigger | Signal Captured | Measurement |
| :--- | :--- | :--- | :--- |
| Phase 5 | Prototype build and performance testing | Component load times, CSS performance, JS bundle size, image optimization, Lighthouse scores at all breakpoints. | Performance audit: component load-time baseline, performance budget adherence. |
| Phase 6 | Qwen media production | Image asset file sizes and optimization techniques used. Qwen processing time per asset type. Token efficiency of media generation. | Media production audit: asset optimization report, token-efficiency log. |
| Phase 7 | Staging implementation on Wix | Wix API performance, custom Velo code execution time, database query patterns, form-submission latency. | Wix performance audit: API response times, custom-code efficiency, database-query optimization opportunities. |
| Phase 7 | Responsive testing and browser QA | Performance across devices and network speeds (throttled testing). Lighthouse performance on mobile vs. desktop. | Mobile performance audit: performance degradation by device class, throttled-network testing results. |
| Phase 8 | Production monitoring | Real-world performance metrics: page load time, Core Web Vitals (LCP, FID, CLS), error-rate logs, 404 patterns. | Production performance report: Core Web Vitals dashboard, error-log analysis, uptime/availability. |
| Phase 8 | Model usage and efficiency tracking | Claude token usage across phases 1-8. Qwen media-generation token usage. ChatGPT API calls and costs. | AI model-efficiency report: tokens per deliverable, cost per phase, efficiency gains from fallback routing. |

**Feedback Loop:**  
L5 signals captured Phase 5-8 → Performance bottlenecks identified (e.g., "Dossier index load time exceeds SLA due to unoptimized queries") → Technical improvements specified → Next-phase build uses optimized schema or component patterns → Production monitoring validates fixes → Performance data feeds into next-build technical spec.

**Evidence Output:**  
- Performance baseline report (Lighthouse, Core Web Vitals, asset optimization)
- Wix API and custom-code efficiency audit
- Mobile-performance and throttled-network testing report
- Error-log analysis and 404-pattern report
- AI model-efficiency report (tokens per deliverable, cost by phase)

---

### 1.6 DDNA Feedback Loop Integration

**Extraction Cadence:**
- **Immediate:** Phase 2-5 L1 (tone) and L2 (workflow) signals captured real-time by model audit logs
- **Milestone:** Phase 5 complete → L3 (design patterns) and L4 (product patterns) extracted and analyzed
- **Pre-Production:** Phase 7 complete → L5 (technical performance) baseline established
- **Post-Launch:** Phase 8 ongoing → Live engagement data feeds all five layers for next-iteration tuning

**Output Registry:**  
All signals flow to DCSE asset lifecycle:
1. Captured (raw signal log from model audits and performance monitoring)
2. Staged (analysis + pattern identification by lead model, e.g., Qwen for L1-L3, Claude for L5)
3. Confirmed (evidence review, pattern validity check)
4. Promoted (patterns documented as reusable templates for next build cycle)

**Governance:**  
DDNA extraction logs maintained in DCSE_DDNA_SUPABASE_STAGING per task declaration section 2.1. Annual DDNA review feeds architecture decisions for SC product and website roadmap.

---

## 2. PS/PPR FIREWALL ARCHITECTURE (D21 §11 Technical Implementation)

The PS firewall is not prompt-only guidance. It is a technical architecture enforced at runtime, with automated sanitation, access denial, and verification tests.

### 2.1 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DCSE ASSET RETRIEVAL LAYER                          │
│  (Supabase, GitHub, Wix CMS, local vector indexes)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼────────┐ ┌───▼────────┐ ┌───▼────────┐
            │  SC Lane Data  │ │ SS Content │ │ PS Sealed  │
            │  (Public)      │ │ (Branded)  │ │ (Isolated) │
            └────────┬───────┘ └───┬────────┘ └────┬───────┘
                     │             │               │
                     └──────┬──────┴───────┬───────┘
                            │             │
                    ┌───────▼──────┐      │
                    │   RETRIEVAL  │      │
                    │   ROUTING    │      │
                    │   LAYER      │      │
                    └───────┬──────┘      │
                            │             │
            ┌───────────────┴────────┐    │
            │                        │    │
      ┌─────▼────────┐         ┌────▼────────────┐
      │ SC/SS Query  │         │ PS Query Attempt│
      │ Approved     │         │ DENIED          │
      │              │         │                 │
      │ Pass to      │         │ Trigger Kill    │
      │ Model        │         │ Switch →        │
      │              │         │ Audit + Alert   │
      └─────┬────────┘         └────────────────┘
            │
      ┌─────▼──────────────────────────────────────┐
      │     SANITATION CHECKPOINT (Layer 1)        │
      │                                            │
      │  Input Verification:                       │
      │  - Lane tag validation (must be SC or SS) │
      │  - PS keyword scan (case references)      │
      │  - Protected-entity detection             │
      │  - Classification check vs. allow-list    │
      │                                            │
      │  REJECT if:                                │
      │  - Lane = PS or unknown                    │
      │  - PS keyword match                        │
      │  - Protected entity detected               │
      │  - Classification not in whitelist         │
      └─────┬──────────────────────────────────────┘
            │
            │ PASS (SC or SS, clean)
            │
      ┌─────▼──────────────────────────────────────┐
      │     MODEL EXECUTION (Claude, Qwen, etc)   │
      │     - Generate, transform, or output      │
      └─────┬──────────────────────────────────────┘
            │
      ┌─────▼──────────────────────────────────────┐
      │     SANITATION CHECKPOINT (Layer 2)        │
      │     OUTPUT VERIFICATION                    │
      │                                            │
      │  Output Inspection:                        │
      │  - PS keyword scan on generated content   │
      │  - Case reference detection                │
      │  - Protected-entity name matching          │
      │  - Metadata tag validation                 │
      │                                            │
      │  REDACT if:                                │
      │  - PS keyword found in output              │
      │  - Case reference in narrative             │
      │  - Protected entity revealed               │
      │  - Metadata lane not SC or SS              │
      │                                            │
      │  REJECT OUTPUT (do not publish) if:        │
      │  - Redaction would break meaning           │
      │  - Multiple PS keywords in single passage  │
      │  - Case core strategy exposed              │
      └─────┬──────────────────────────────────────┘
            │
            │ OUTPUT PASS (clean SC/SS content)
            │
      ┌─────▼──────────────────────────────────────┐
      │    PUBLIC ARTIFACT GENERATION               │
      │    (Web page, Dossier entry, asset)        │
      │                                            │
      │  - Lane tag set to SC or SS                │
      │  - Metadata published without PS refs      │
      │  - Public search index updated (SC/SS only)│
      │  - Social preview cards generated          │
      │  - Analytics event fired (no PS identity)  │
      └─────┬──────────────────────────────────────┘
            │
      ┌─────▼──────────────────────────────────────┐
      │    PUBLIC DELIVERY                          │
      │    (sonlyconsulting.com)                   │
      └──────────────────────────────────────────────┘

             (PS sealed system never contacted)
```

### 2.2 Firewall Access Control Rules

**Layer 1: Input Routing (before model execution)**

| Lane Tag | Allowed? | Action | Fallback |
| :--- | :--- | :--- | :--- |
| `lane: SC` | YES | Pass to retrieval layer and model | N/A |
| `lane: SS` | YES | Pass to retrieval layer and model | N/A |
| `lane: PS` | NO | REJECT immediately. Log attempt. Do not proceed to model. | Halt. Escalate to DCS. |
| `lane: unknown` or missing | NO | REJECT. Classify requirement before proceeding. | Return to orchestration for lane mapping. |

**Layer 2: Input Sanitization (keyword and entity scan)**

| Trigger | Keyword Class | Detection Method | Action |
| :--- | :--- | :--- | :--- |
| Case reference | "8:23CV489", "civil case", "docket", "plaintiff" | Exact match + regex pattern | REJECT input. Do not pass to model. Escalate. |
| Protected entity name | "Case Owner Name", "Adversary Names" (from PS lane registry) | Exact name + fuzzy match (80%+) | REJECT input. Quarantine. Escalate. |
| Protected strategy | "claim theory", "settlement ceiling", "deposition strategy" | Contextual keyword + proximity scan | REJECT input. Log as attempted PS access. Escalate. |
| Litigation date/timeline | Case-specific event dates known from PS materials | Temporal pattern matching | REJECT input if matches PS timeline. Escalate. |

**Layer 3: Output Verification (after model generation)**

| Check | Method | Failure Behavior |
| :--- | :--- | :--- |
| PS keyword re-scan | Full content text search on generated output. Scan all metadata fields. | If keyword found: attempt targeted redaction. If redaction violates context integrity: REJECT entire output. Do not publish. |
| Protected entity detection | Name-matcher on all proper nouns in output against PS entity registry. | If entity detected: quarantine output. Manual review gate. Do not auto-redact names. |
| Metadata lane validation | Confirm output metadata.lane = SC or SS (never PS). | If metadata.lane not set or = PS: REJECT. Assign correct lane or halt. |
| Cross-reference proof | If output mentions "evidence" or "sources," verify no sources link to PS case or PS repository. | If PS source detected in bibliography: REJECT output. Require SC or SS sources only. |

**Layer 4: Public Index Control**

| Index/Search | PS Content Allowed | Implementation |
| :--- | :--- | :--- |
| Site search index (sonlyconsulting.com) | NO | Only SC and SS articles indexed. PS lane indexed separately (not accessible from public search). |
| Social preview / OG tags | NO | Metadata never includes case references, protected entities, or PS keywords. |
| Google/Bing sitemap | NO | PS URLs excluded from sitemap.xml. robots.txt blocks PS directory crawl. |
| Analytics event tracking | NO | Analytics tag never fires with PS user identity. Anonymous tracking only. |
| AI retrieval index (if used for Q&A) | NO | Retrieval index contains only SC and SS artifacts. PS materials in separate, access-controlled index. |

---

### 2.3 Kill-Switch Mechanism

**Trigger Conditions:**

Kill-switch engages automatically if:

1. **Multiple PS keyword matches in single artifact** (3+) → Output rejected, audit alert fired, DCS notified.
2. **Protected entity name detected in public metadata** → Output quarantined, manual review gate enabled, DCS notified within 1 hour.
3. **Unauthorized lane-bridge attempt detected** (PS data routed to SC retrieval) → Retrieval halted, attempted access logged, DCS escalation priority.
4. **Search index contains PS URL or content** → Index rollback to last known-clean snapshot, audit of index creation, DCS notification.

**Kill-Switch Actions:**

1. Halt all downstream processing (model execution paused, output not published).
2. Log full context: source request, detected violation, timestamp, user/model identity, content snippet.
3. Quarantine the artifact to a protected audit folder (no public access).
4. Fire notification to DCS Level 0 authority with action options: (a) escalate to legal, (b) manual remediation path, (c) rejection and archive.
5. Prevent rollback to prior version containing PS material (no silent history reversion).

**Evidence:**  
Kill-switch engagement logged in DCSE_Voice_Isolation_Log.md with:
- Timestamp and initiating request
- Detected PS keyword or entity
- Model/agent that generated output
- Containment action taken
- DCS decision recorded

---

### 2.4 Verification Test: Proof that PS Cannot Enter SC Retrieval Index

**Test Name:** PS_FIREWALL_ISOLATION_VERIFICATION_v1  
**Authority:** CRITICAL. Must pass before any public artifact is published.

**Test Procedure:**

1. **Setup:**
   - Create a test artifact tagged `lane: PS` with known PS keywords (e.g., "8:23CV489", "case strategy").
   - Attempt to retrieve this artifact through SC search/retrieval API.
   - Attempt to index this artifact in public search index.

2. **Expected Outcome:**
   - Retrieval API REJECTS the PS-tagged artifact. HTTP 403 Forbidden or equivalent access-denied signal.
   - Search index NEVER contains PS-tagged content. Public queries return zero results for PS keywords.
   - Audit log RECORDS the rejection attempt with timestamp and model/user identity.

3. **Failure Condition:**
   - If PS-tagged content is retrieved, indexed, or appears in search results: **TEST FAILS. Do not proceed to publication.**
   - If rejection is not logged: **TEST FAILS. Audit trail is incomplete.**

4. **Verification:**
   - Run test in Phase 5 (prototype stage).
   - Re-run test in Phase 7 (staging).
   - Re-run test in Phase 8 (before go-live).
   - Every test must PASS 100% to unlock next phase.

**Evidence:**  
Pass/fail report signed by Claude (CTO) and AG (DBA) with timestamped test logs. No publication without passing test.

---

## 3. VERIFICATION GATES (D02 Process Compliance)

Every pipeline stage has four verification gates: input admission, transformation validation, output proof, regression check.

### 3.1 Phase 1: Ecosystem Declaration

**Input Admission:**  
- DCS direction recorded (from plan section 1)?
- Product families identified (from plan section 9)?
- PS exclusion policy stated (from plan section 5)?
- **GATE:** If any missing, route back to DCS for clarification before proceeding.

**Transformation Validation:**  
- Does product declaration include boundaries and audience?
- Does Dossier schema prevent PS-tagged content from appearing in SC outputs?
- Does fingerprint sheet distinguish SC voice from SS narrative?
- **GATE:** If validation fails on any criterion, model reworks declaration before sign-off.

**Output Proof:**  
- Product families are specific (not "AI" or "web" alone; e.g., "Custom Digital Campaigns").
- Dossier schema has at minimum 8 fields including lane tag and PS-firewall checkbox.
- Fingerprint sheets show tone, color, imagery guidance for SC and SS distinctly.
- **GATE:** Output signed off by Claude (CTO) + DCS approval before Phase 2 begins.

**Regression Check:**  
- N/A for Phase 1 (no prior version to regress).

---

### 3.2 Phase 2: Dossier Content Model

**Input Admission:**  
- Phase 1 ecosystem declaration approved and finalized?
- Sanitation checklist template available (from plan section 3.3.2)?
- Five candidate Dossier entries identified (SC or SS only, no PS)?
- **GATE:** If any missing, halt Phase 2 and request missing input.

**Transformation Validation:**  
- Does sanitation checklist cover all required elements (rights, accessibility, metadata, PS-firewall check)?
- Do five candidate entries match Dossier schema exactly (8+ required fields)?
- Does every entry pass PS-keyword scan and entity detection?
- **GATE:** Qwen audit sign-off required on PS-firewall checks for all five entries.

**Output Proof:**  
- Five entries submitted with completed sanitation checklists (no skipped items).
- Zero PS keywords in any entry.
- Every entry has lane tag (SC or SS), rights documentation, alt-text, and accessibility review.
- **GATE:** Qwen + Claude sign-off before Phase 3 begins.

**Regression Check:**  
- Do five entries maintain voice consistency with fingerprint sheets from Phase 1?
- Does any entry accidentally contradict SC philosophy established in Phase 1?
- **GATE:** If regression detected, entry reworked before sign-off.

---

### 3.3 Phase 3: Sitemap and Content Architecture

**Input Admission:**  
- Phase 2 Dossier model finalized?
- Navigation system requirements defined (from plan section 3.1-3.8)?
- SC-to-SS reveal pathway concept approved?
- **GATE:** Missing requirements trigger Phase 1-2 rework.

**Transformation Validation:**  
- Does sitemap route all eight primary navigation pages?
- Do four discovery views (by topic, product, format, outcome) resolve to same canonical content without duplication?
- Does IA pass three-decision discovery test with 80%+ success rate?
- **GATE:** IA testing required before sign-off.

**Output Proof:**  
- Complete sitemap (desktop + mobile hierarchy).
- Navigation rules documented (when to show/hide SC vs. SS content).
- Three primary user journeys documented and tested.
- SC-to-SS reveal moment defined with visual and interactive spec.
- **GATE:** Claude (CTO) + DCS approval before Phase 4.

**Regression Check:**  
- Does new sitemap incorporate all product families from Phase 1?
- Does IA still accommodate all Dossier entry types from Phase 2?
- Is PS systems architecture preserved (no PS content accessible from public nav)?
- **GATE:** If regression detected, sitemap revised.

---

### 3.4 Phase 4: Three Visual Directions

**Input Admission:**  
- Phase 3 sitemap finalized?
- Visual reference board approved (from plan section 1)?
- Design brief outline ready (section 9)?
- **GATE:** If missing, request before design begins.

**Transformation Validation:**  
- Does each direction materially differ from the other two (palette, typography, layout, motion)?
- Does each direction avoid prohibited reference copying (Playboy, Work & Co, Clay, BURN, Monocle, Soho House)?
- Does each direction fit within approved reference board (Playboy publication architecture, Work & Co clean layouts, etc. — aesthetic only, no copying)?
- **GATE:** Design audit for reference compliance required.

**Output Proof:**  
- Three directions each with 5+ representative comps.
- Scorecard comparing directions across 8+ criteria (brand alignment, proof clarity, conversion clarity, accessibility, motion performance, etc.).
- Visual specification for each direction (palette hex codes, typography scale, component patterns).
- **GATE:** Qwen visual QA + Claude strategy review before DCS selection decision (section 8.5).

**Regression Check:**  
- Do all three directions support SC philosophy fingerprint from Phase 1?
- Can Dossier entries from Phase 2 render in all three directions without visual contradiction?
- Does SS reveal moment work visually in all three directions?
- **GATE:** If any direction violates Phase 1-2 requirements, rework or retire that direction.

---

### 3.5 Phase 5: Off-Site Responsive Prototype

**Input Admission:**  
- DCS selected one direction from Phase 4?
- Visual specification for selected direction finalized?
- Component architecture and IA from Phase 3 available?
- Approved asset sources identified (for hero imagery, icons, etc.)?
- **GATE:** Missing any input halts prototype work.

**Transformation Validation:**  
- Does prototype match selected visual direction across all six major pages (home, Dossier index, entry, products, philosophy, SS reveal)?
- Do all components render responsively at breakpoints: 320px, 768px, 1024px, 1440px+?
- Does every page pass WCAG 2.1 AA accessibility (color contrast, keyboard nav, alt-text complete)?
- Does PS firewall verification test (section 2.4) pass 100%?
- **GATE:** All four criteria must pass before Phase 6. If any fails, prototype revised.

**Output Proof:**  
- Prototype code repository with commit history.
- Responsive test results at all breakpoints (pass/fail per component per breakpoint).
- Accessibility audit report (WAVE, axe, or equivalent tool).
- Performance baseline (Lighthouse score 90+, Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1).
- PS firewall test report (100% pass, logged).
- **GATE:** Claude (CTO) + Qwen (visual QA) + AG (PS isolation) sign-off required.

**Regression Check:**  
- Does prototype render Dossier entries from Phase 2 correctly?
- Do all product families from Phase 1 have working detail pages?
- Is IA from Phase 3 properly implemented (all discovery views functional)?
- Does SC-to-SS reveal pathway from Phase 3 work as designed?
- **GATE:** Regressions must be fixed before proceeding.

---

### 3.6 Phase 6: Qwen Premium Media Sprint

**Input Admission:**  
- Prototype from Phase 5 finalized and approved?
- Media brief with campaign imagery direction defined?
- Rights and brand-pack documentation available?
- Required asset list (count and type: hero images, feature images, video, motion studies)?
- **GATE:** Missing brief or asset list halts media production.

**Transformation Validation:**  
- Do generated assets match campaign brief and brand direction?
- Do all assets have documented lineage, rights status, and accessibility (alt-text, captions)?
- Do visual assets align with SC fingerprint from Phase 1 (if SC-branded media) or SS fingerprint (if SS media)?
- Does video narration or caption tone match established voice from Phase 2 Dossier entries?
- **GATE:** Qwen + Gemini multimodal QA required before assets enter production.

**Output Proof:**  
- All assets with metadata: filename, dimensions, optimization technique, rights holder, release status, alt-text, accessibility notes.
- Asset lineage log (which Qwen capability generated each asset, token count if applicable).
- Quality audit report (color accuracy, contrast, motion smoothness, audio levels).
- **GATE:** Qwen (lead) + Gemini (QA) sign-off required before Phase 7 asset deployment.

**Regression Check:**  
- Do new assets replace placeholder imagery in prototype without breaking layout?
- Do new assets' color palette align with Phase 4 visual direction?
- Do captions and alt-text use voice consistent with Phase 2 Dossier entries?
- **GATE:** If regression, asset revised or placeholder retained until fix available.

---

### 3.7 Phase 7: Wix Staging

**Input Admission:**  
- Phase 5 prototype fully approved?
- Phase 6 media assets finalized?
- Current Wix site backed up and before-state captured?
- Velo code specification available?
- **GATE:** Missing any prerequisite halts Wix implementation.

**Transformation Validation:**  
- Does staged implementation render prototype design accurately in Wix (within Wix rendering constraints)?
- Do all responsive breakpoints pass visual review on live Wix site (not just test server)?
- Do all forms submit correctly (product inquiry, consultation request)?
- Do analytics events fire on primary conversions (Dossier engagement, product inquiry)?
- Does PS firewall test (section 2.4) still pass 100% in staged environment?
- **GATE:** UAT must cover all functional areas before production promotion.

**Output Proof:**  
- Staging site URL with all pages accessible (home, Dossier index, 2 entries, products index, 1 product page, philosophy, AI section, SS reveal, Start Here).
- UAT test results: all primary user journeys tested, 100% functional pass rate.
- Responsive testing report (screenshot evidence at all breakpoints).
- PS firewall re-verification test report (100% pass logged).
- Analytics event audit (all tracked events firing correctly).
- Performance baseline on live Wix site (Lighthouse, Core Web Vitals).
- **GATE:** Claude (CTO) + AG (DBA) + Qwen (visual QA) sign-off before production promotion decision (section 8.7).

**Regression Check:**  
- Do all Dossier entries from Phase 2 display correctly in Wix rendering?
- Do all product families from Phase 1 have working detail pages in staging?
- Does IA from Phase 3 work correctly in live Wix environment (all discovery views functional)?
- Does SC-to-SS reveal work as designed in production Wix code?
- **GATE:** All regressions must be resolved before go-live approval.

---

### 3.8 Phase 8: Release and Measurement

**Input Admission:**  
- Phase 7 staging fully approved and ready for promotion?
- DCS release decision obtained (yes/no for go-live)?
- Measurement plan established (which metrics to track, baseline established in Phase 7)?
- Rollback plan documented (what to revert if critical errors occur)?
- **GATE:** Missing DCS approval halts release. Missing measurement plan halts Phase 8.

**Transformation Validation:**  
- Does production site render identically to staging site (post-promotion verification)?
- Do all forms and conversion events fire correctly in production?
- Are all metrics tracking correctly (Dossier engagement, product pages, inquiry actions)?
- Is analytics baseline from Phase 7 established as production comparison benchmark?
- **GATE:** Post-launch verification required within 24 hours of go-live.

**Output Proof:**  
- Production go-live signoff (DCS decision + timestamp).
- Post-launch verification report (production vs. staging comparison).
- 4-week engagement metrics (Dossier views, product-page progression, inquiry-action volume).
- Lesson-capture report (what worked, what broke, what assumptions held).
- **GATE:** No gate; Phase 8 is observational and continuous. Lessons feed into next-build planning.

**Regression Check:**  
- Do live metrics track correctly against Phase 7 baseline?
- Are there unexpected error patterns, 404s, or conversion blockers in production?
- Does engagement match Phase 5-7 projections or diverge significantly?
- **GATE:** If critical production issue detected, trigger rollback plan or emergency fix protocol.

---

## VERIFICATION SUMMARY TABLE

| Phase | Input Gate | Transform Gate | Output Gate | Regression Gate |
| :--- | :--- | :--- | :--- | :--- |
| 1 | DCS direction + product families | Product declaration, Dossier schema, fingerprints | Product families declared, schema validated, fingerprints signed | N/A (first phase) |
| 2 | Phase 1 approved + sanitation template | Sanitation checklist, PS-firewall checks, five entries | Five entries + checklists + PS audit | Voice consistency with Phase 1 fingerprint |
| 3 | Phase 2 approved + nav requirements | Sitemap, IA tests, reveal pathway | Sitemap + IA test results + reveal spec | Product and Dossier content accommodation |
| 4 | Phase 3 approved + design brief | Three materially different directions + scorecards | Three directions + scorecard + visual spec | SC/SS fingerprint alignment |
| 5 | Direction selected + visual spec + asset sources | Prototype build, responsive testing, PS firewall test | Prototype + responsive report + accessibility audit + PS test | Content accommodation + voice consistency |
| 6 | Phase 5 approved + media brief + asset list | Asset generation, lineage logging, QA | Assets + metadata + lineage log + QA report | Layout integrity + color/voice alignment |
| 7 | Phase 6 approved + Wix backup + Velo spec | Staging build, UAT, PS firewall re-test | Staging URL + UAT results + PS test + performance baseline | Dossier/product/IA rendering + reveal functionality |
| 8 | Phase 7 approved + DCS decision + measurement plan | Production promotion verification | Go-live signoff + post-launch report + lesson capture | Metric accuracy vs. baseline |

---

**Status:** READY FOR EXECUTION  
**Next Action:** Proceed to Section C (Toolchain Integration)
