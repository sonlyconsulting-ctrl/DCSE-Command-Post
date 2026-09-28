# DCSE D12 | Video and Media Governance v7.2 RC1 Candidate

**Document ID:** DCSE-D12-v7.2-RC1-CANDIDATE
**Date:** 2026-09-19
**Lane:** ALL, bounded by entity, rights, classification, channel
**Status:** CANDIDATE / NOT RATIFIED. DCS Level 0 is the final promotion and public-release authority.
**Lineage:** Current main v7.2 carried-forward D12 plus the proposed brand-ident Addendum C in PR #158; uploaded D12 v6.9 candidate (not authority); D09/D18/D19 and D21/D22/D05.
**Precedence:** This wrapper and Section 7 below identify candidate corrections to historical source language; no older embedded version/status/model-duty text independently overrides v7.2 R5/D21/D22/D05 or DCS instructions.

---
> **v7.2 consolidated-source projection (2026-09-11):** This file places the current carried-forward D12 subject matter inside the self-contained v7.2 governance package. Source lineage: `governance/v7.1/source/doctrines/D12_Video_Media.md`. Embedded legacy version labels, local file URLs, and pre-v7.2 routing references in the inherited body are provenance only and SHALL NOT control v7.2 runtime routing. Active authority, lane routing, source identity, and lifecycle state resolve through the operative v7.2 R5 controller, D21, D22, D05, the v7.2 Doctrine Index, and later DCS directives. This projection does not convert historical status text into a new promotion event.

# DCSE Doctrine D12: Video & Media

**Document ID:** DCSE-D12  
**Version:** v6.9 Update Candidate  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T19:27:00-04:00
**Last Version/Release Date/Time:** 2026-06-21T17:05:00-04:00  
**Status:** DCSE Authorized version Pending Approval  
**Classification:** INTERNAL  
**Lane:** ALL  
**Entityx:** DCS, DCSE  
**Canonical file:** D12_Video_Media.md  
**Doctrine Description:** The Video and Media Doctrine (D12) outlines the authoritative governance for the automated design, build, review, and promotion of all video content, motion graphics, audio assets, and multimedia deliverables across DCSE entities. It defines script structures, technical specifications, model-duty assignments, and strict release gates.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. Video Build Declaration (Idea & Persona Design)
No video production may proceed as an open-ended generation exercise. Every automated or supervised video build must initiate with a Video Build Declaration defining the target entity (SC, SS, PS, TI, or DCSE), content series, audience, public or internal status, assigned AI models, and agentic authorization level.
*   **Entity Isolation:** Video content must strictly adhere to the designated entity firewall.
    - **SC (Sonly Consulting):** Outputs must reflect executive warmth, business clarity, and structured messaging.
    - **SS (Sports Society):** Outputs must utilize soulful, cinematic storytelling, lifestyle framing, and narrative metaphors.
    - **TI (Tech Integration):** Outputs must remain instructional, focusing on training systems and procedural clarity.
    - **PS (Pro Se Litigation):** Outputs must remain precise, restrained, document-grade, and strictly offline. Absolutely no entertainment framing is allowed.
*   **GYTO Firewall:** The trademark "GET YOUR THINK ON!" (GYTO) must remain restricted to internal use and must be automatically suppressed from all public-facing video scripts, captions, thumbnails, and metadata unless explicitly authorized by DCS.

---

## 2. Script and Storyboard Architecture
*   **Structural Separation:** AI agents tasked with script generation must explicitly separate the narrative audio track from visual callouts, screen descriptions, and text overlays.
*   **Three-Part Structure Rule:** All generated scripts must flow through three mandatory phases:
    1. **Opening (Hook):** Capture immediate attention within 0-3 seconds.
    2. **Body:** Core message delivery partitioned into 30-45 second educational segments.
    3. **Close:** Clear call to action (CTA) and resolution (final 10-15% of run time).
*   **Voiceover Constraints:** Voiceover pacing must target a maximum of 145 words per minute to preserve clarity and reflective maturity. Tone must align with the "Morgan Freeman meets Michael B. Jordan" brand archetype, blending slow-paced authority with modern relevance.
*   **Storyboard Generation:** The generated script must be converted into a structured storyboard (JSON and Markdown) mapping the scene number, visual description, voiceover alignment, and specific production tools prior to visual rendering.

---

## 3. Automated Build and Production Standards
The build pipeline executes the storyboard through a coordinated stack of AI generation tools, maintaining cinema-grade targets.
*   **Visual Prompts:** Image and video generation prompts must require three specific structural components: Scene Description, Style Details, and Motion Instructions. Prompts must include negative controls to prevent distorted faces, extra limbs, garbled text, and off-brand palettes.
*   **Technical Specifications:** Master video assemblies must target 4K resolution (3840x2160) up to 8K, at 24 to 30 frames per second for cinematic or social delivery, up to 60 frames per second for smooth motion requirements.
*   **Post-Production Rendering:** Desktop assembly software (such as PowerDirector) must utilize the H.264 AVC or H.265 codec within an MP4 container. Bitrate must be optimized to 45 to 60 Mbps for 30fps, or 60 to 80 Mbps for 60fps, ensuring ultra-high quality. Audio mixes must keep the music bed at -18dB to -12dB below the primary voiceover.

---

## 4. Model-Duty Assignments for Media Generation
Model execution must follow specialized assignments:
*   **Claude:** Primary authority for script writing, narrative structure, voiceover calibration, and entity DNA review.
*   **ChatGPT:** Primary for storyboard creation, visual shot lists, and metadata packaging.
*   **Gemini/Veo/Sora:** Primary for visual generation, technical editing workflow optimization, and caption accuracy.
*   **Codex/AG:** Execution of internal test checklists, file generation, and directory routing.

---

## 5. Code Review, Self-Test, and Preflight (QA Gates)
Every governed video must pass an automated or supervised preflight checklist before transitioning to human review.
*   **Validation Checks:** The system must verify entity DNA compliance, accurate closed captions, balanced audio levels, and the absence of AI-generation artifacts.
*   **Secrets Management:** No API keys for generation tools (ElevenLabs, Sora, etc.) may be hardcoded into scripts, prompts, or exposed project files.
*   **Preflight Declaration:** The inspecting agent must produce a Preflight Declaration verifying GYTO suppression, music licensing, and PS Firewall compliance.

---

## 6. Promote and Fix (Release Rule)
No video is authorized for release merely because it renders successfully.
*   **Approval Chain:** The artifact must move through the Tribunal Inbox from Draft to Internal Review, requiring DCS Level 0 signoff before advancing to Approved or Published status.
*   **Agentic Levels:** All public-facing video content is restricted to Agentic Level 1 (Supervised). No public video release is authorized at Agentic Level 3 (Autonomous).

---

## Addendum A: Command Post (CP) Video Production Workflow
This workflow codifies the step-by-step process flow required for the creation of all media outputs within the Command Post (CP) system:

### Phase 1: Strategic Foundation
1. **Executive Brief Development:** Define the core message, audience personas, emotional journey, and success metrics. Classify the format:
   - **Promo Videos:** 30–60 seconds (High Impact)
   - **Educational Videos:** 2–5 minutes (Authority Building)
   - **Long-form Videos:** 10–20 minutes (Deep Engagement)
2. **Script Architecture & Hook Design:** Draft hook templates (0–3s) targeting specific audience pain points.
3. **Brand Integration:** Define specific brand overlays and ensure GYTO™ suppression protocols are active.
4. **Asset Planning:** Detail technical specifications, visual components, and background tracks before starting production.

### Phase 2: AI-Powered Asset Creation
1. **AI Script and Storyboard Generation:**
   - **ChatGPT:** Prompts structured for pacing, layout, SEO metadata, and draft composition.
   - **Claude:** Prompts optimized to enforce entity DNA, brand-voice tone, and emotional arcs.
   - **Gemini:** Prompts set to generate technical shot lists, timing markers, and platform optimization scripts.
2. **Voice & Audio Generation:** Execute text-to-speech audio via ElevenLabs, restricting voice models to authorized vocal signatures at exactly 145 WPM.
3. **Visual Curation & Curation:** Group visual assets into:
   - **Hero Images:** Custom visual elements generated via Sora/DALL-E.
   - **Supporting Visuals:** Explanatory diagrams or UI wireframes.
   - **B-Roll Footage:** High-quality motion sequences representing business or technology themes.

### Phase 3: Production Excellence
1. **Timeline Assembly:** Align audio tracks with visual elements in PowerDirector.
2. **Audio Mastering:** Apply volume leveling, keeping background music beds under -12dB (targeting -18dB) below vocal tracks.
3. **Graphics Overlay:** Render text callouts and subtitle tracks with zero phonetic spelling errors.

### Phase 4: Strategic Distribution
1. **Format Optimization:** Export target aspects (16:9 widescreen or 9:16 vertical) matching platform specifications.
2. **Metadata Attachment:** Embed title tags, meta descriptions, and analytics hooks prior to pushing the package to the Tribunal Inbox.

---

## Addendum B: Core Deliverable Outputs
For every media campaign, the pipeline must produce the following four structured deliverables:
1. **Script:** Separated audio/visual channels with exact timings.
2. **Storyboard:** Scene-by-scene map containing visual descriptions and asset seeds.
3. **Shot List:** Technical breakdown of angles, lighting, and camera motions.
4. **Production Brief:** Metadata sheet detailing target resolution, codecs, bitrates, and model paths.

---

## Addendum C: Brand/Logo Motion Ident (6–8 Seconds)

**Decision source:** DCS Level 0 directive 2026-09-19; proposed new v7.2 D12 control for controlled promotion under D21/D05. Scope: each SC/DCSE-authorized brand and product-family identity with an approved logo has a paired **6–8 second illustrative brand-motion ident** as a required brand deliverable for future identity packages. Existing identities without an ident enter a separately tracked production backlog; do not silently represent the ident as already produced, revoke an existing approved asset, or block an unrelated release solely by retroactively assuming a video exists. Application to PS or any protected identity requires its own firewall and express DCS authorization; never import protected source material into public media.

1. **Source-of-truth preflight:** Identify exact entity > brand > product, approved static logo version, source binary/editable vector, typography/colors, classification, audience, rights, intended distribution, authorized video maker, DCS approval and evidence/rollback path. Retrieve existing approved brand videos before generating. Source image access/approval does not itself authorize public use, derivative rights, or a new brand name. No speculative trademark or public product claims.
2. **Motion meaning:** The 6–8 seconds must *illustrate the brand's own logical concept through purposeful motion*, not merely spin, zoom, sparkle or animate generic particles. Document the concept in one sentence, establish an observable start state, an understandable transformation, and a resolved state that matches the authorized static logo exactly. Retain the approved emblem geometry, names, letterforms, color relationships, trademark presentation and parent/child attribution. Never invent a new symbol, add labels/taglines, or alter text through video-generation hallucinations.
3. **Short-ident script exception:** For the bounded 6–8-second **non-narrated** identity ident, the long-form Section 2 three-part educational structure (0–3s hook, 30–45s body segments, closing CTA) does not apply. Use a timed **Origin > Logical Transformation > Identity Resolve/Hold** storyboard instead. No voiceover or CTA required; optional sound design must be authorized, rights-cleared and provided with a silent version. If a longer campaign film is requested, Section 2 applies.
4. **Technical / safety contract:** Default master exact 16:9, ideally 3840×2160, 24–30fps; platform derivatives only when requested, with logo safe-area and no clipping. A final minimum 1–1.5s stationary readable hold must use the approved artwork as a locked high-resolution plate or separately proofed compositor artwork, not regenerated AI lettering. No erratic rotations, jitter, strobing, rapid flashes, busy backgrounds or overexposed highlights masking text. Provide reduced-motion/static alternate and muted playback. Apply D09/D11/D19 brand/contrast checks and D18 operational pipeline; target accessibility standards but do not claim audited compliance without tests.
5. **Proof and promotion:** Record original and final asset ID/version, source-to-derivative hashes, maker/model/prompt, rights and music/SFX provenance, storyboard/timecodes, duration/aspect/frame-rate/audio checks, text/logo fidelity, start/end stills, playback preview, exceptions, named validator and DCS decision. An ident is APPROVED/PUBLISHED only after asset and media QA, independent review as applicable, and explicit DCS Level 0 release approval. A created doctrine row/PR or a generated video is not production proof.

**D18 routing:** Short brand idents run the D18 four-phase pipeline using its ident-specific storyboard/QA profile, not long-form campaign assumptions. For CTJ Unified, use the separately scoped production brief; “executive audience” is a positioning observation, not a formal rename to Executive Suite.

---
## 7. v7.2 reconciliation and non-inference controls

### 7.1 Documented conflicts, not silently settled
The carried-forward Section 1 expands `SS` as "Sports Society" and `TI` as "Tech Integration", while current enterprise routing uses `SS` for Smoove Spots and `TI` for the Initiative/training lane. These historic names are **not** an authoritative entity reassignment. Resolve entity, lane, brand profile, classification, audience and approved voice from the current operative manifest and DCS instructions; block only a non-PS/public asset whose classification or source cannot be safely determined. Any PS-origin material remains PS-protected until explicitly authorized and sanitized by DCS.

The inherited Section 1 blanket `GET YOUR THINK ON!` public suppression conflicts with D09's historic listing of that phrase as a public mark and with product-specific public usage. The exact current brand-term/mark record and channel permission must be reconciled by DCS; do not assert universal public permission or blanket permanent prohibition from one historical paragraph. A public video containing an unverified protected/controlled term stays at the affected release gate pending an exact approved disposition.

### 7.2 Format profiles and authority of tool assignments
The educational script's 30–45 second body segments, mandatory hook/CTA, and voiceover limits apply **only when the declared format uses spoken long-form education or promotion**. They SHALL NOT force narration, artificial CTA or impossible segment lengths into a 6–8s brand ident. D12 Addendum C establishes `ORIGIN -> PURPOSEFUL LOGICAL TRANSFORMATION -> EXACT IDENTITY HOLD`, with source-faithful last 1–1.5s stationary end plate and no extra text. A CTA is optional for formats only when DCS specifically approves one.

The inherited model-duty table describes a historic preferred tool mix, not autonomous design or governance authority and not a claim that a model or production program is available in the current runtime. Route model/maker dynamically by the verified capabilities, rights and permissions, documenting source/input support, maximum clips, resolution, frame rate, editing/compositing access, delivered artifact and fallback. Gemini Video Gem is an instruction/coordination surface only until an authenticated tool returns the actual video.

`4K` is a master production target, **not** proof that every generator can render native 4K and not the bitrate delivered to mobile. A 1080p source upscaled later must be labeled as such. Effective final duration is measured with an actual container/video probe and verified playback, not inferred from requested duration.

### 7.3 Brand-ident proof contract and release control
Each primary-logo identity SHALL have a 6–8s ident production requirement or a scoped DCS-exception record in the versioned brand profile. Missing old idents create explicit backlog, not an invented completion claim. For a new ident package, DCS Level 0 determines whether the ident is an acceptance dependency for that specific release. The source artwork, render, editor output, original audio license, source and final checksums, elapsed duration, user-readable end plate, codec/aspect/resolution, silent and reduced-motion alternatives, cross-device QA, validator and precise human decision SHALL be separately recorded.

The approval chain is concept brief -> exact source access/rights -> storyboard -> candidate render -> QA and independent validation when applicable -> DCS approval -> authorized publication -> runtime verification. A direct approval of an existing *static* CTJ logo does not approve a *derived video*, and a recorded prompt does not mean a video exists.

### 7.4 Challenge cases
`D12-001` Seven-second ident is forced through 30-second educational body -> FAIL. `D12-002` Producer changes CTJ lettering or reintroduces deleted first-line tagline -> FAIL. `D12-003` Model returned prompt or image, but report says video rendered -> FAIL. `D12-004` Final logo holds 0.3s or loses safe area -> FAIL. `D12-005` Production master has no verified binary/hash/rights -> INSUFFICIENT_EVIDENCE. `D12-006` Intended SS/TI/PS entity cannot be resolved or protected material is routed to public SC -> affected action BLOCKED. `D12-007` Older brand video absent, release claims "already complete" -> FAIL.

**Exit:** v7.2 RC1 CANDIDATE. Addendum C is present as the PR #158 proposal and does not automatically become operative. The Gemini knowledge extract, if made, must exclude internal-only agent permissions and credentials, must carry source/version restrictions, and must not grant autonomous public release.
