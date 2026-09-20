# DCSE D19 | Visual Creation Pipeline v7.2 RC1 Candidate

**Document ID:** DCSE-D19-v7.2-RC1-CANDIDATE
**Date:** 2026-09-19
**Lane:** ALL subject to governed entity, brand profile, rights and PS firewall
**Status:** CANDIDATE / NOT RATIFIED
**Lineage:** Uploaded D19 v6.9; operative main v7.2 carried-forward D19; D09 RC3 profile candidate; D12/D18 proposed short-brand-ident profile in PR #158. Existing source/doctrine status labels are inherited provenance and cannot self-promote this version.
**Purpose of v7.2 overlay:** Source fidelity, identity-specific visual variants, controlled brand token inheritance, image-to-video derivatives and precise validation.

---
> **v7.2 consolidated-source projection (2026-09-11):** This file places the current carried-forward D19 subject matter inside the self-contained v7.2 governance package. Source lineage: `governance/v7.1/source/doctrines/D19_Visual_Creation_Pipeline.md`. Embedded legacy version labels, local file URLs, and pre-v7.2 routing references in the inherited body are provenance only and SHALL NOT control v7.2 runtime routing. Active authority, lane routing, source identity, and lifecycle state resolve through the operative v7.2 R5 controller, D21, D22, D05, the v7.2 Doctrine Index, and later DCS directives. This projection does not convert historical status text into a new promotion event.

# DCSE Doctrine D19: Visual Creation Pipeline

**Document ID:** DCSE-D19
**Version:** v6.9
**Created Date/Time:** 2026-07-25T23:00:00-04:00
**Last Doc Modified Date/Time:** 2026-07-25T23:00:00-04:00
**Status:** ACTIVE_RATIFIED
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D19_Visual_Creation_Pipeline.md
**Doctrine Description:** The Visual Creation Pipeline (D19) consolidates image, graphic, and visual asset creation methodology from D12 (visual prompt standards), D09 (brand color palette), and D11 (CSS token implementation). No single doctrine previously covered the end-to-end workflow from creative brief to delivered visual asset. D19 fills that gap with a five-phase pipeline: Brief, Prompt Engineering, Generation, Brand QA, and Format Delivery.
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

## 1. Visual Creation as Consolidated Methodology

Visual creation across DCSE was previously scattered:

- D12 Section 3 defined visual prompt structure (scene, style, motion, negatives).
- D12 Addendum A Phase 2 defined hero images, supporting visuals, and B-roll categories.
- D09 Section 3 defined the canonical brand color palette anchors.
- D11 Section 4.1 defined the CSS token implementation of brand colors and fonts.

D19 consolidates these into a single pipeline. The source doctrines retain their governance authority. D19 is the execution methodology for visual asset creation.

---

## 2. Phase Definitions

### 2.1 Phase 1: Creative Brief

Objective: Define exactly what visual asset is needed, for what purpose, in what context, before any generation begins.

Inputs: Business objective, target entity, intended placement, audience.

Steps:

1. Asset Classification: Determine the visual type:
   - Hero Image: Primary visual for landing page, video thumbnail, campaign header. Maximum impact, brand-forward.
   - Supporting Visual: Explanatory diagram, UI wireframe, data visualization, infographic. Clarity-first.
   - Social Graphic: Platform-native image for social media. Format-specific (1:1, 4:5, 16:9, 9:16).
   - Brand Element: Logo application, color palette swatch, typography specimen, pattern/texture.
   - B-Roll Still: Complementary image for editorial or video production context.
   - Icon/UI Element: Interface component, navigation element, status indicator.

2. Entity and Palette Declaration: Pull the entity-specific palette from D09:
   - SC (Sonly Consulting): Gold (#D4AF37), Deep Navy (#0A192F), Silver (#C0C0C0). Premium, executive aesthetic.
   - SS (Smoove Spots): Earth (#D2691E, #8B4513), Emerald (#50C878). Soulful, cinematic warmth.
   - TI (The Initiative): Deep Navy (#1B3A57), Silver (#C0C0C0), Emerald (#50C878). Authoritative, precise.
   - DCS Enterprise: DCSE Blue (#0A192F), Gold (#D4AF37). Metric-driven, structural.
   - Prohibited: Neon colors, default browser primaries, high-contrast combinations that degrade the premium aesthetic.

3. Context Specification: Define where the visual will appear (web page, email header, social post, video frame, print), at what dimensions, and alongside what content.

4. Constraint Declaration: List any negative constraints (no faces, no specific imagery, accessibility requirements, transparency needs).

Outputs: Visual Brief Document containing asset type, entity, palette, dimensions, placement context, and constraints.

Quality Gate: No generation proceeds without a completed Visual Brief. This is a stop-gate.

### 2.2 Phase 2: Prompt Engineering

Objective: Translate the Visual Brief into structured generation prompts optimized for AI image generation tools.

Inputs: Approved Visual Brief from Phase 1.

Steps:

1. Three-Component Prompt Structure (mandatory per D12 Section 3):
   - Scene Description: What is being depicted. Concrete, specific visual elements. Avoid abstract instructions.
   - Style Details: Art style, lighting, color palette (using exact hex values from D09), texture, mood, photographic or illustrative approach.
   - Motion Instructions: For video frames and animated assets, direction of movement, camera angle, transition intent. For static images, compositional flow and visual hierarchy.

2. Negative Control Prompts (mandatory):
   - No distorted faces or anatomical errors.
   - No extra limbs or merged body parts.
   - No garbled, misspelled, or AI-artifact text.
   - No off-brand palettes or unauthorized color schemes.
   - No watermarks, stock photo badges, or generation tool signatures.

3. Entity-Specific Style Tokens:
   - SC: "executive boardroom lighting, warm gold tones #D4AF37, navy depth #0A192F, clean modern composition, premium texture"
   - SS: "cinematic warmth, earth tones #D2691E #8B4513, natural light, soulful atmosphere, narrative composition, lifestyle editorial"
   - TI: "documentary precision, authoritative framing, deep navy #1B3A57, silver accents #C0C0C0, high contrast, factual"
   - DCS: "structural, data-informed, clinical navy #0A192F, gold highlights #D4AF37, minimal, metric-driven"

4. Resolution and Format Specification:
   - Web hero: Minimum 1920x1080, WebP preferred, JPEG fallback.
   - Social: Platform-native dimensions (1080x1080 for feed, 1080x1920 for stories, 1200x628 for link previews).
   - Thumbnail: 1280x720 minimum, 16:9 aspect ratio.
   - Print: 300 DPI minimum at target print dimensions.

Outputs: Structured Generation Prompt(s), Negative Control Set, Resolution Specification.

Quality Gate: Prompt must contain all three structural components (scene, style, motion/composition) plus negative controls before generation proceeds.

### 2.3 Phase 3: Generation

Objective: Execute the generation prompt(s) and produce raw visual assets.

Inputs: Approved prompts from Phase 2.

Steps:

1. Tool Selection:
   - AI Image Generation: DALL-E, Midjourney, Stable Diffusion, or other authorized tool per the task.
   - AI Video Frame Generation: Sora, Veo, or other authorized video generation tool.
   - Diagram/Infographic: Programmatic generation (SVG, Canvas, charting libraries) for data visualizations.
   - Screenshot/UI Capture: Browser automation for UI-based visuals.

2. Generation Execution:
   - Generate minimum 3 variants per hero image to allow selection.
   - Generate minimum 2 variants per supporting visual.
   - Single generation acceptable for diagrams, UI elements, and technical visuals.

3. Raw Asset Review:
   - Check for AI artifacts (distorted elements, hallucinated text, merged objects).
   - Check for palette compliance against D09 anchors.
   - Check for compositional quality (balance, hierarchy, focal point).
   - Reject and regenerate any asset that fails raw review.

Outputs: Raw Visual Assets (multiple variants for selection), Generation Metadata (tool used, prompt used, seed/parameters if applicable).

Quality Gate: At least one variant per asset must pass raw review before advancing to Brand QA.

### 2.4 Phase 4: Brand QA

Objective: Verify every visual asset against brand standards before delivery.

Inputs: Selected raw assets from Phase 3.

Steps:

1. Color Compliance:
   - Compare dominant colors against entity palette (D09 Section 3).
   - Verify no prohibited colors (neons, default browser primaries).
   - Verify sufficient contrast for accessibility (WCAG 2.1 AA minimum, 4.5:1 for text, 3:1 for large text/graphics).

2. Typography Compliance (if text is present):
   - Verify font family matches brand token stack (D11 Section 4.1):
     - Display: Cormorant Garamond, Georgia, serif
     - UI Labels: Barlow Condensed, Arial Narrow, sans-serif
     - Monospace: DM Mono, monospace
   - Verify no AI-generated text artifacts or spelling errors.

3. Entity Firewall:
   - Verify the visual contains no cross-entity references.
   - Verify GYTO suppression for public-facing visuals.
   - Verify PS content exclusion for non-PS visuals.

4. Composition Standards:
   - Brand overlay on lower third for thumbnails (D12 standard).
   - No unauthorized watermarks or third-party branding.
   - Proper aspect ratio for target platform.

5. Accessibility:
   - Alt text drafted for every visual (descriptive, not decorative).
   - Sufficient color contrast verified.
   - No seizure-risk animation patterns (if motion asset).

Outputs: QA-Approved Visual Assets, QA Report listing each check and its result, Alt Text for each asset.

Quality Gate: Every asset must pass all 5 Brand QA checks. Failures return to Phase 3 for regeneration or Phase 2 for prompt revision.

### 2.5 Phase 5: Format Delivery

Objective: Prepare final assets in the correct formats and sizes for their destination, with proper metadata.

Inputs: QA-approved assets from Phase 4.

Steps:

1. Format Conversion:
   - Web: WebP preferred. JPEG fallback. PNG for transparency only. Maximum 500KB per image for web delivery.
   - Social: Platform-native format and dimensions.
   - Video Production: Source-quality (PNG or TIFF) for compositing into video timeline.
   - Print: CMYK conversion at 300 DPI if print delivery is required.

2. Lazy Load Optimization: All below-the-fold web images must be configured for lazy loading.

3. Metadata Embedding:
   - File name per D06 naming convention: ENTITY_Description_YYYYMMDD.ext
   - Asset ID per registry format: BRAND-YEAR-TYPE-SERIAL
   - Alt text embedded in image metadata where format supports it.

4. Delivery Manifest: Plain-text manifest listing file name, format, resolution, file size, intended placement, and alt text.

5. Asset Registry: Register each visual asset in `dcse_asset_registry` with all 15 metadata elements.

Outputs: Final Visual Assets (format-optimized), Delivery Manifest, Asset Registry Entries.

Quality Gate: Live preview verification required if the visual is destined for a web page or app (D21 Section 6).

---

## 3. Trigger Mechanism

### 3.1 Explicit Triggers

- User says "create image," "generate visual," "hero image," "brand graphic," "make a thumbnail," "design social graphic."
- User invokes a visual creation skill or requests a specific Phase.
- D18 Phase 2 calls D19 as a sub-pipeline for visual asset creation.

### 3.2 Implicit Triggers

- The task involves image generation, graphic design, or visual asset creation.
- The task involves brand palette application to a visual deliverable.
- The task involves thumbnail creation for video or social media.
- The task involves UI screenshot capture or component visualization.
- The task references hero images, B-roll stills, or supporting visuals.

### 3.3 Trigger Announcement

When D19 activates, the model must announce:
"Visual Creation Pipeline activated. Running Phase 1 (Brief) > Phase 2 (Prompt Engineering) > Phase 3 (Generation) > Phase 4 (Brand QA) > Phase 5 (Delivery)."

### 3.4 Sub-Pipeline Behavior

When D19 activates as a sub-pipeline within D18 (Media Production), it runs Phases 1-5 for the visual assets needed, then returns completed assets to D18 Phase 2. The D19 trigger announcement includes "(sub-pipeline of D18 Media Production)" to maintain audit clarity.

---

## 4. Cybersecurity Integration

Per D21 Section 5:

- No image generation API keys or tokens in client-facing code or prompts shared externally.
- Generated images must not contain embedded metadata revealing internal system paths or API endpoints.
- Alt text must not contain internal governance references, doctrine IDs, or system architecture details.
- Images destined for public delivery must be stripped of EXIF data that reveals generation tool internals or file system paths.

---

## 5. Tier Access

| Tier | D19 Access |
|---|---|
| Tier 1 Sovereign | Full pipeline, all phases, prompt engineering templates, brand QA gates |
| Tier 2 Internal Collaborator | Pipeline phases without entity-specific style tokens. Brand QA gates apply. |
| Tier 3 External Product Build | Image requirements from Tier 3 Product Build Extract Section 4 only. No pipeline access, no prompt templates. |

---

## Related Doctrine

- D12_Video_Media.md — Visual prompt standards and B-roll categories (D19 extracts and extends)
- D09_Brand_Identity.md — Canonical brand color palette (D19 Phase 1 and Phase 4 reference)
- D11_HTML_Wix_App.md — CSS token implementation of brand colors and fonts (D19 Phase 4 typography)
- D18_Media_Production_Pipeline.md — Parent pipeline when visuals are for video production
- D07_Campaign_Governance.md — SEO/GEO/AEO standards for image metadata
- D21_Doctrine_Runtime_Engine.md — DCL logging, cybersecurity baseline, live preview mandate

---

## Error-Catch Protocol

If this doctrine file is missing or unreadable, follow the canonical error-catch protocol:
1. HALT execution. Do not infer visual creation rules from pre-training.
2. LOG `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. TRIGGER STOPGATE and alert the user.
4. FALLBACK: If D19 is unavailable, visual prompt standards from D12 Section 3 and brand palette from D09 Section 3 remain individually authoritative but unintegrated.

---
## 9. v7.2 brand-source and visual-asset fidelity profile

### 9.1 Existing-artwork-first and authority separation
Before generative visual production, resolve the exact source artwork, approved asset role (`LOGO`, `LOCKUP`, `ICON`, `PRODUCT_HERO`, `MOTION_END_PLATE`, `REFERENCE_ONLY`), parent-child brand profile, version, source location, byte-verified hash, creator/provider, rights and explicitly approved uses. A missing in-session attachment or media-registry row is not verified enterprise absence. A referenced image available only in older chat is `ACCESS_PENDING` until actual binary retrieval, not permission to invent a visually similar substitute. A selected rendering and its transparent-background experiment are distinct versions and SHALL remain separately traceable.

Use original source artwork unchanged when asked to compare color palettes or apply an existing logo to backgrounds. For a request to edit that same image, preserve the source and capture the new derivative's relation, version, hash and review status. For a genuine design-revision task, distinguish image generation/interpretive design from pixel-preserving deterministic edits; do not claim exact source-pixel preservation after generative modification without independent image comparison. A user's approval of an illustration does not imply all derived icon, transparent cutout, video or text treatments are approved.

### 9.2 SC > CTJ design-token inheritance
Resolve entity/product-appropriate D09 profile. Until DCS adopts an updated D09 profile, preserve SC established anchors `#D4AF37` gold, `#0A192F`/ `#1B3A57` navy, `#C0C0C0` silver. CTJ's selected common UI `#061A33` is a scoped child variant, not a D09 enterprise anchor replacement. The distinct light-background canvas palette candidates shall not be collectively treated as approved. Metallic source artwork may contain gradients/illumination not exactly equal to CSS token stops. Record CSS tokens and representative sampled image colors as **different data types**.

Inherited SC display family `Cormorant Garamond, Georgia, serif` and labels `Barlow Condensed, Arial Narrow, sans-serif` remain currently documented in carried-forward D11; parent-child profile overrides shall identify authority/version. Exact font in a flattened/generated wordmark is UNKNOWN until editable source proves it. Video models and image generators shall not be trusted to retype critical trademark, fine typography or logo geometry; protect the source plate or compositor text layer, and inspect letter-by-letter for change.

### 9.3 Asset-type-specific generation contracts
- Exact-source, user-directed image edits and deterministic crop/export may produce **one approved-source derivative** when the request is precise; the inherited three-variant hero/two-variant supporting-image default applies to exploratory concepts, not to altering a locked logo three different ways without authority.
- For social/web thumbnails, placement-specific layout is permitted only inside approved logo safe area, with exact wordmark and brand asset role.
- An ident's opening/transform motion may be newly generated per D12/D18, but the final static logo frame is the exact authorized master/plate. A motion prompt, a generated still and an actual playable video have distinct lifecycle states.
- Image alt text, resized formats and mobile crops must preserve source identity; transparent-background exports require actual alpha/edge verification, not a preview that shows black as transparency.
- Production masters, web-optimized delivery copies and thumbnail derivatives have separate size/performance targets. The inherited blanket `500KB per web image` is an optimization target subject to product/device requirements, not authority to degrade a meaningful detailed logo or enforce impossible fidelity.

### 9.4 Accessibility, validation and registration
Require explicit tests for non-text contrast, readable tiny icons at 16/24/32/48px, dark/light compositing, exact wording and trademark, zoom/reflow, reduced-motion/static alternatives where used, color/state independence, safe areas and no light flashes; record actual results, not aspirational “accessibility compliant”. WCAG levels/thresholds used are target design criteria until an applicable release audit verifies them. The digital original and every approved derivative SHALL be retrievable through a governed asset index + authorized binary storage; a reference-only public URL, issue title or one-session sandbox path is not durable storage proof.

### 9.5 Challenge tests
`D19-001` Original logo unavailable in session but model invents compass -> FAIL. `D19-002` Transparent cutout on checkerboard retains opaque black background -> transparency test fails. `D19-003` AI alters supplied tagline but claims “all text unchanged” -> FAIL. `D19-004` Source CSS hex is reported as exact image pixel color without pixel extraction -> FAIL. `D19-005` Three random redesigns made instead of exact requested edit -> scope drift. `D19-006` Previous candidate image is mistaken for newest user-selected source -> supersession/lineage fail. `D19-007` Asset indexed but fresh authorized agent cannot read binary -> ACCESS_PENDING, no source-fidelity completion.

**Exit:** V7.2 RC1 CANDIDATE; artifact source/rights/brand authority remain separately resolved per D09, D21, D22 and DCS approval.
