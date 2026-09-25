# CTJ Unified Design and Flow QA

**Task ID:** SC-CTJ-UNIFIED-R1-QA-20260925-01  
**Lane / Entity:** Sonly Consulting / CTJ / The Unified Path  
**Surface:** Local governed review prototype  
**Audit mode:** Combined UX and accessibility-risk audit  
**Status:** PARTIAL PASS WITH CORRECTIONS  
**Authority / Access:** Current local prototype, approved CTJ and Unified assets, governed build process v1.4  
**Deployment:** Not authorized and not performed  
**Handoff ID:** SC-CTJ-UNIFIED-R1-QA-20260925-H01

## Preflight validation

- Production build completes successfully.
- Sites packaging tests pass 4 of 4.
- Exact supplied CTJ family mark and Unified product artwork render in the public and application surfaces.
- Public attribution renders as `Powered by Sonly Consulting`.
- Browser audit used the local review build only. No live checkout, Wix mutation, Netlify publication, Vercel deployment, or production promotion occurred.
- The prior $1 Stripe and Cash App Pay payment evidence remains preserved separately. This audit does not repeat a financial transaction.

## User goal and accessibility target

A visitor should understand how the CTJ family fits together, distinguish the Parts from Unified, enter Unified with or without a current issue, complete a Decision Brief or Daily Thought Exercise, retain a reasoning trail, and continue without AI when AI is unavailable.

The target is keyboard-operable, responsive, readable interaction with visible labels, focus treatment, reduced-motion support, and no loss of work between steps. Full screen-reader, 200 percent zoom, and mobile-device certification remain release gates.

## Captured flow

| Step | Surface | Health | Evidence |
| --- | --- | --- | --- |
| 1 | Public CTJ home | PASS | `01-public-home.jpg` |
| 2 | CTJ product showroom | PASS WITH OPEN LINKS | `02-product-showroom.jpg` |
| 3 | Unified product page | PASS | `03-unified-product.jpg` |
| 4 | Unified cinematic arrival | PASS | `04-unified-arrival.jpg` |
| 5 | CTJ Exchange two-entrance selection | PASS | `05-ctj-exchange.jpg` |
| 6 | Decision Brief evidence mapping | PASS | `06-decision-evidence.jpg` |
| 7 | Reasoning record and bounded AI challenge | PASS | `07-decision-record.jpg`, `08-bounded-ai-challenge.jpg` |
| 8 | AI-unavailable fallback | PASS | `09-ai-unavailable.jpg` |
| 9 | Daily Thought Exercise | PASS | `10-daily-exercise.jpg` |
| 10 | Daily practice completion | PASS | `11-daily-complete.jpg` |
| 11 | Corrected perspective-step entry | PASS | `12-fixed-perspective-start.jpg` |

## Strengths

1. Public pages establish a distinct premium CTJ identity without turning the experience into a generic course catalog.
2. The product showroom communicates the family ladder: free SCA, three $39 Parts, $119 Unified, and $199 Keeper Collection.
3. The separation between Parts and Unified is understandable. Parts teach and practice; Unified integrates and continues.
4. Unified provides two valid entrances and explicitly states that no issue is required.
5. The working application shifts from cinematic arrival to a calmer reasoning workspace.
6. The Decision Brief preserves evidence, missing information, assumptions, options, action, and return conditions.
7. The AI panel asks a challenge question rather than issuing a verdict and labels its result as prototype synthesis.
8. The AI-unavailable state keeps the CTJ record usable and offers fixed prompts.
9. The Daily Thought Exercise supports evidence, counterview, plain-language restatement, time perspective, transfer, and deliberate pause.
10. Local save and resume behavior, return-to-Exchange behavior, focus styles, and reduced-motion CSS are present.

## Defects corrected during this audit

### R1-QA-01: Perspective answers crossed product modes

**Observed:** Then, Now, and Next responses from a Decision Brief appeared automatically inside a later Daily Thought Exercise.  
**Cause:** Both modes shared the same `then`, `now`, and `next` state fields.  
**Correction:** Added separate decision and exercise perspective fields plus a schema-version boundary that clears contaminated legacy perspective fields.  
**Verification:** Daily Thought Exercise perspective fields reopened empty while the Decision Brief record remained separate.

### R1-QA-02: New steps retained the previous scroll position

**Observed:** A completed step could advance to a new screen with the heading partially above the viewport.  
**Cause:** Internal application steps changed React state without resetting document position.  
**Correction:** Added a scroll-to-top effect for stage and step changes.  
**Verification:** The corrected perspective step opened at `window.scrollY = 0` with the heading and first task visible.

## Open UX risks

1. **SCA CTA is not implemented.** The Strategic Clarity Assessment page describes the 31-question deterministic experience, but `Begin assessment` currently has no action. It must not be presented as complete.
2. **Part and Collection card destinations are incomplete.** Part 1, Part 2, Part 3, and Keeper Collection `View product` actions return to the shared showroom rather than distinct product detail or preview routes.
3. **Support and legal destinations are placeholders.** Public and application footer controls for Support, Privacy, and Accessibility do not yet open governed destinations.
4. **No explicit new-exchange reset exists.** The product can resume a local draft, but the user needs a deliberate way to begin a new record without browser storage management.
5. **AI is a bounded local prototype, not a connected governed model service.** The current challenge is deterministic interface behavior used to validate the interaction contract.
6. **Commerce is not integrated into this prototype.** The historical payment rail passed once, but current product selection does not yet create entitlement, delivery, first use, or return access.

## Accessibility risks and evidence limits

- Visible focus treatment is defined for buttons, text areas, and disclosure summaries.
- Fields use enclosing label elements and the desktop browser exposed meaningful accessible names.
- The four Evidence Table labels contain both a title and hint. Automated exact-label selection was inconsistent for these composite labels. Screen-reader output must be checked directly before release.
- Responsive CSS includes 1024, 768, and 480 pixel breakpoints, but this run did not capture a true mobile browser viewport.
- Screenshots cannot prove reading order, screen-reader announcements, keyboard trap absence, color contrast ratios, target sizes, or 200 percent zoom resilience.
- Full WCAG compliance is not claimed.

## Next implementation order

1. Connect the governed 31-question SCA engine and SCA-to-Unified handoff without changing deterministic scoring.
2. Add distinct product detail or preview routes for Parts 1 through 3 and the Keeper Collection.
3. Add explicit new-record and reset behavior with a confirmation boundary.
4. Bind governed Support, Privacy, Accessibility, Terms, and Refund destinations.
5. Complete mobile, keyboard-only, screen-reader, and 200 percent zoom verification.
6. Assemble the Claude Design handoff with assets, tokens, states, routes, screenshots, open issues, and acceptance rules.
7. Integrate current-product checkout reconciliation, entitlement, delivery, first use, and return access only after the review candidate passes.

## Exit criteria

- No cross-mode data contamination.
- Every new step starts at a readable viewport position.
- SCA and product-card actions have honest, working destinations.
- Local draft resume and new-record behavior are distinguishable.
- Responsive and assistive-technology evidence is recorded.
- Claude Design receives the exact approved assets and cannot redefine product logic, scoring, identity, or entitlement rules.
- Commerce remains nonpublic until a current-release purchase-to-access test passes.

## Evidence closeout

**Build:** PASS  
**Sites packaging tests:** 4 of 4 PASS  
**Decision Brief:** PASS after correction  
**Daily Thought Exercise:** PASS after correction  
**Bounded AI and unavailable state:** PASS as interface prototype  
**Mobile and assistive technology:** NOT YET VERIFIED  
**SCA integration:** OPEN  
**Current purchase-to-access integration:** OPEN  
**Overall:** PARTIAL PASS, suitable for continued review-candidate implementation and Claude Design preparation, not release.
