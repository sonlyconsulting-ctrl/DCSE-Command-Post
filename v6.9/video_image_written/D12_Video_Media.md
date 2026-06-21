# DCSE Doctrine D12: Video & Media

**Document ID:** DCSE-D12  
**Version:** v6.9 Update Candidate  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T17:05:00-04:00  
**Last Version/Release Date/Time:** 2026-06-21T17:05:00-04:00  
**Status:** CANDIDATE  
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
