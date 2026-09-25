# CTJ SC and SS HTML Staging Inventory

**Date:** 2026-09-23  
**Source:** `SC DCSE HTML FILES.zip`  
**Source SHA-256:** `bc4a6f3004d63ffa2981ac5f3d8297265d7979f6365b64ecd7e60696bbefb437`  
**Scope:** Read-only review of 17 HTML files for possible use in the SC, CTJ, and SS website program.  
**Status:** Inventory decision record. No file is approved for publication by this review.

## Executive Decision

The ZIP contains valuable product content and reusable interaction mechanics, but no file should be published unchanged.

The strongest source assets are the three CTJ enhanced workbooks, the small CTJ Part 1 overview, the voice-recording mechanics, and QuantumDebt Analytics. The highest-risk files are the two investor prototypes, the 30-pillar command center, and both DCSE Voice Capture versions because they expose private or unsupported material.

The file named `30-bundle-interactive.html` is not a CTJ 30-day curriculum or a commercial bundle. It is a generic collection of 30 widgets. It should be treated as a component laboratory only.

## Disposition Summary

| Disposition | Count | Meaning |
| --- | ---: | --- |
| Rebuild for CTJ | 3 | Valuable CTJ content or merchandising patterns, but must be rebuilt inside the governed product architecture. |
| Protected CTJ source | 4 | Full or nearly full paid curriculum. Never expose as public page source or free download. |
| Reuse selected mechanics | 3 | Individual components may be extracted after code, privacy, and accessibility review. |
| Separate SS candidate | 1 | Potential SS tool, subject to financial calculation and compliance validation. |
| Internal editorial source | 1 | Useful as a topic backlog, not as a public page. |
| Internal QA source | 1 | Useful for internal review flow after false-functionality repair. |
| Quarantine or archive | 4 | Contains private litigation references, unsupported claims, fabricated metrics, or unsuitable internal material. |

## File by File Decisions

| File | Actual contents | Decision | Intended destination | Required action |
| --- | --- | --- | --- | --- |
| `[WORKBOOK] CTJ_Part1_ENHANCED.html` | Full Part 1 workbook with 10 days and 63 response fields | Protected CTJ source | `/app/part-1` | Reconcile against the approved canonical curriculum. Add durable save, export, accessibility, and corrected metadata. Do not publish as a public page. |
| `[WORKBOOK] CTJ_Part2_ENHANCED.html` | Full Part 2 workbook with 10 days and 63 response fields | Protected CTJ source | `/app/part-2` | Correct copied Part 1 metadata and URLs. Reconcile duplicated exercises and approved Part 2 content. Add persistence and export. |
| `[WORKBOOK] CTJ_Part3_ENHANCED.html` | Full Part 3 workbook with 10 days and 63 response fields | Protected CTJ source | `/app/part-3` | Correct copied Part 1 metadata and URLs. Reconcile the approved Alignment Check and Part 3 content. Add persistence and export. |
| `[TEASER] CTJ_Part1_10EssentialClarityBuilders.html` | Nearly the full Part 1 workbook plus voice recording and old price copy | Protected source, not a teaser | Internal content reconciliation | Remove old `$117` trilogy offer and broad transformation claims. Extract the voice recorder mechanics separately. Do not expose the full workbook as a teaser. |
| `[TEASER] CTJp1.html` | Static summary of ten Part 1 builders | Rebuild for public preview | `/preview/part-1` or Part 1 product page | Strong seed for a product overview. Update naming, identity, footer, and approved product language. Decide how many builder names should be public. |
| `[TEASER] CTJ Chat v3a.html` | One static reflection micro-module, not a functioning chat | Rebuild for CTJ preview | `/preview/unified` or `/start` | Remove internal Claude and Gemini comments and QA checklists. Repair the missing worksheet link. Convert into a bounded CTJ Exchange demonstration. |
| `[TEASER] ctj_clarity_module_v_1.html` | Five-day feedback selector, local feedback storage, voice recording, daily card, holiday tab | Reuse selected mechanics | Free sample day and protected app | Retain local voice recording, daily prompt, and local save patterns. Separate holiday material. It does not transcribe audio. |
| `[COMPANION] CLARITY_FEEDBACK_VOICE_MEMO_HUB.html` | Internal feedback tool with voice recording, simulated transcription, daily cards, and holiday content | Internal QA source | Internal beta and content review | Do not describe its scripted placeholder as transcription. Feedback, sharing, saving, and PDF actions are alerts or console output rather than real services. |
| `[BUILDER] CTJ_Bundle_Builder_Interactive.html` | Five-pillar explorer and configurable offer selector | Rebuild interaction pattern | `/collection` or `/build-your-path` | All prices and access terms conflict with the approved Keeper model. Replace `$197`, `$297`, add-ons, and six-month access with canonical products and entitlements. Checkout is only an alert. |
| `[TEASER] 30-bundle-interactive.html` | Thirty generic widgets, games, utilities, and calculators | Component laboratory only | No direct public destination | It is not CTJ curriculum. Potentially reuse timer, progress, drawing, memory, team generator, and quiz mechanics. Remove `eval()` calculator logic and fake weather behavior before any reuse. |
| `[BUILDER] 00-pillar-index.html` | Thirty-topic enterprise content index across SC, SS, and private material | Internal editorial source | Editorial planning only | Extract SC and SS topic candidates into separate backlogs. Remove all private-lane references. Do not publish the combined command center. |
| `[ENTERPRISE] QuantumDebt Analytics.html` | Three working financial calculators with local save and PDF export | Separate SS candidate | SS free tool or low-cost utility | Validate every formula and edge case. Add accessible result summaries, privacy language, data deletion, correct disclaimers, and independent financial review. Treat as high-stakes content. |
| `[TEASER] DCSE Chat Fact Check Org 10252025.html` | Static fact-check form, poll, logic game, and fabricated leaderboard | Reuse selected mechanics | CTJ daily challenge or SS participation concept | Remove the fake leaderboard and unsupported community framing. The sequence game can inspire a daily logic exercise. This is not a real chat or fact-check system. |
| `[COMPANION] DCSE Voice Capture.html` | Internal voice utility containing a named case, private litigation category, and simulated transcription | Quarantine | Internal archive only | Contains protected case information and private workflow labels. Never use in SC, CTJ, or SS public builds. |
| `[COMPANION] DCSE Voice Capture2.html` | Minor formatting revision of the same protected voice utility | Quarantine, preferred archive copy only if needed | Internal archive only | Same public prohibition. It still contains case details and simulated transcription. Avoid maintaining both versions. |
| `[ENTERPRISE] DCSE Qwen Investor Mockup.html` | Investor page with revenue, users, projections, equity tiers, and private-lane references | Quarantine | No public destination | Contains unsupported financial metrics and investment representations. It requires verified books, legal review, securities review, and complete removal of private material before any future use. |
| `[TEASER] DCSE_INVESTOR_OPTION3_DataDriven.html` | Larger investor dashboard with revenue claims, market-size claims, equity terms, and private-lane references | Quarantine | No public destination | Same prohibition. It must not be repurposed as ordinary marketing copy. |

## Confirmed Public Website Roles

### SC.com

SC.com should showcase the CTJ family and link to the dedicated CTJ property. It should not host full workbooks or internal utilities.

Suitable source material from this ZIP:

- A repaired product-family overview derived from `CTJp1.html`.
- A CTJ collection card that launches the rebuilt path selector.
- A separate card for the CTJ methodology-based service.
- A carefully validated link to QuantumDebt Analytics only if SS owns and releases that tool.

### CTJ website

Suitable build candidates:

- Part 1 public preview derived from `CTJp1.html`.
- A bounded CTJ Exchange preview derived from `CTJ Chat v3a.html`.
- A sample-day experience using approved Part content plus selected mechanics from `ctj_clarity_module_v_1.html`.
- A governed collection selector derived from the bundle builder layout, but using the approved product family and Keeper terms.
- Protected Part 1, Part 2, and Part 3 applications built from the enhanced workbook content after reconciliation.

### SS website

Suitable candidates:

- QuantumDebt Analytics as a separate SS utility, subject to high-stakes validation.
- Soulful editorial treatments of selected topics from the 30-pillar index after lane separation.
- Seasonal or year-end reflection campaigns derived from the holiday prompts, without presenting them as CTJ core curriculum.
- SS storytelling pages that refer users to canonical CTJ previews and products.

## Freebie and Intro Decisions

The strongest free entry sequence remains:

1. Strategic Clarity Assessment.
2. Daily Thought Exercise.
3. One governed sample day from Part 1.
4. A one-page Then Now Next field sheet.
5. A bounded CTJ Exchange demonstration.

The ZIP does not contain a validated 30-day free curriculum. A future 30-day experience should be designed from the verified 30-day CTJ curriculum, not from `30-bundle-interactive.html`.

## Critical Findings

### Commerce conflicts

`CTJ_Bundle_Builder_Interactive.html` uses old offers:

- Core Journey: `$197`
- Audio add-on: `$47`
- Video add-on: `$47`
- Seven-day accelerator: `$97`
- Complete bundle: `$297`
- Six-month platform access

These conflict with the approved Keeper family. The page is an interaction reference only. None of its prices or entitlements should enter the new build.

### Product-content exposure

`CTJ_Part1_10EssentialClarityBuilders.html` is mislabeled as a teaser. It contains nearly the full paid Part 1 content. Public previews should reveal the experience and one representative exercise without releasing the paid workbook.

### False functionality

Several files visually claim functions they do not perform:

- The clarity feedback hub inserts a fixed sample transcript instead of transcribing speech.
- Its feedback submission, note saving, card sharing, and holiday PDF actions are alerts or console operations.
- The voice-capture utilities also generate fixed mock transcripts and do not save to a real Library or inventory.
- CTJ Chat v3a is a static micro-module, not a chat system.
- Both investor prototypes contain buttons without governed workflows.

These behaviors must never be represented as working customer capabilities.

### Privacy and firewall failures

The 30-pillar page and both investor files mix public entities with private material. The two voice-capture files contain a named legal matter and private case workflow. These files are prohibited from public reuse.

### Metadata defects

The enhanced workbooks contain stale or copied metadata:

- The domain is misspelled as `solnyconsulting.com`.
- Part 2 and Part 3 reuse Part 1 canonical URLs, descriptions, social metadata, and course schema.
- Public claims such as predictable success and complete transformation require removal or substantiation.
- Product footer and attribution should use the exact approved phrase `Powered by Sonly Consulting.`

## Reusable Mechanics Library

These mechanics may be extracted into governed components after code review:

| Mechanic | Best use |
| --- | --- |
| Local browser voice recording | CTJ responses, Unified Exchange, optional daily reflection |
| Timer and progress meter | Daily exercise pacing and completion feedback |
| Drawing canvas | Mapping assumptions, systems, or scenario relationships |
| Memory and sequencing interactions | Optional thinking warmups, not scored doctrine |
| Daily prompt card | CTJ continuing practice and SS social promotion |
| Local-only draft storage | Anonymous SCA or free exercise continuity |
| PDF export pattern | User-controlled result and reflection export |
| Product path selector | CTJ collection comparison after canonical pricing integration |

No reusable mechanic should carry over old visual identity, unsupported claims, mock data, or internal labels.

## Recommended Build Order

1. Import the three workbook files as protected source material, not runnable public pages.
2. Reconcile their content against the approved CTJ canonical curriculum.
3. Build the public Part 1 preview from one representative exercise and selected copy from `CTJp1.html`.
4. Build the Daily Thought Exercise and CTJ Exchange preview from governed prompts, using only selected local recording and card mechanics.
5. Rebuild the collection selector around the approved Keeper products, pricing, and entitlements.
6. Keep QuantumDebt Analytics in a separate SS validation track.
7. Quarantine both investor pages and both DCSE voice-capture pages from all public repositories and Claude Design inputs.

## Claude Design Handoff Rule

Claude Design may receive only the approved, cleaned source package. Do not include the entire ZIP. The handoff should contain:

- Approved brand assets and exact logo variants.
- Public CTJ preview content only.
- The governed product and route manifest.
- The rebuilt collection selector with approved pricing data.
- The app-shell prototype with fixed, adaptive, and generative boundaries.
- A component list identifying which mechanics came from legacy prototypes.
- A do-not-use list covering investor claims, private material, mock transcripts, old prices, old access terms, internal comments, and stale metadata.

## Release Status

This review authorizes source classification only. It does not authorize deployment, publication, checkout activation, pricing changes, or content deletion.
