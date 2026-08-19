# DCSE Doctrine D18: Media Production Pipeline

**Document ID:** DCSE-D18
**Version:** v6.9
**Created Date/Time:** 2026-07-25T23:00:00-04:00
**Last Doc Modified Date/Time:** 2026-07-25T23:00:00-04:00
**Status:** ACTIVE_RATIFIED
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D18_Media_Production_Pipeline.md
**Doctrine Description:** The Media Production Pipeline (D18) extracts the operational methodology for video, audio, and multimedia production from D12 (Video & Media governance). D12 remains the governance authority defining rules, firewalls, and compliance requirements. D18 is the execution methodology defining how media gets produced: the four-phase pipeline, model-duty assignments, QA gates, and deliverable specifications. This separation mirrors the D17/D13 pattern where methodology was extracted from governance.
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

## 1. Media Production Pipeline as Universal Methodology

The Media Production Pipeline is a four-phase execution framework for creating video, audio, motion graphics, and multimedia deliverables across all DCSE entities. Each phase has defined inputs, outputs, quality gates, and model assignments.

The pipeline applies to any media production task: promotional videos, educational content, long-form engagement pieces, audio assets, motion graphics, social media clips, and podcast production.

D12 (Video & Media) remains the governance authority. D18 defines how the work gets done.

---

## 2. Phase Definitions

### 2.1 Phase 1: Strategic Foundation

Objective: Define what gets built, for whom, and to what standard before any production begins.

Inputs: Business objective, target entity, audience persona(s), distribution channel(s).

Steps:

1. Executive Brief Development: Define core message, audience personas (reference D10), emotional journey, and success metrics. Classify format:
   - Promo Videos: 30-60 seconds (High Impact)
   - Educational Videos: 2-5 minutes (Authority Building)
   - Long-form Videos: 10-20 minutes (Deep Engagement)
   - Social Clips: 15-30 seconds (Platform-Native)
   - Audio/Podcast: Variable length (Companion Content)

2. Script Architecture and Hook Design: Draft hook templates (0-3 seconds) targeting specific audience pain points. Apply the Three-Part Structure Rule:
   - Opening (Hook): Capture attention within 0-3 seconds.
   - Body: Core message in 30-45 second educational segments.
   - Close: Clear CTA and resolution (final 10-15% of runtime).

3. Brand Integration: Pull entity-specific brand tokens from D09. Activate GYTO suppression protocol for public-facing content. Verify entity isolation per D12 Section 1.

4. Asset Planning: Detail technical specifications, visual components, background tracks, and generation tool assignments before starting production.

Outputs: Video Build Declaration, Executive Brief, Script Architecture Document, Asset Requirements List.

Quality Gate: No production proceeds without a completed Video Build Declaration. This is a stop-gate.

### 2.2 Phase 2: AI-Powered Asset Creation

Objective: Generate all raw assets (script, storyboard, voice, visuals) using the model-duty assignment matrix.

Inputs: Approved outputs from Phase 1.

Steps:

1. Script and Storyboard Generation (Model-Duty Matrix):
   - Claude: Script writing, narrative structure, voiceover calibration, entity DNA review. Prompts optimized for brand-voice tone and emotional arcs.
   - ChatGPT: Storyboard creation, visual shot lists, metadata packaging. Prompts structured for pacing, layout, SEO metadata.
   - Gemini: Technical shot lists, timing markers, platform optimization scripts. Visual generation prompts.

2. Voice and Audio Generation:
   - Execute text-to-speech via authorized voice synthesis tools.
   - Voice models restricted to authorized vocal signatures.
   - Pacing target: 145 words per minute maximum for clarity and reflective maturity.
   - Tone archetype: slow-paced authority with modern relevance.

3. Visual Asset Curation:
   - Hero Images: Custom visual elements generated via image/video generation tools. Apply D19 Visual Creation Pipeline for prompt engineering.
   - Supporting Visuals: Explanatory diagrams, UI wireframes, data visualizations.
   - B-Roll Footage: High-quality motion sequences representing business, technology, or lifestyle themes per entity.
   - Visual Prompts must include three structural components: Scene Description, Style Details, Motion Instructions. Include negative controls (no distorted faces, extra limbs, garbled text, off-brand palettes).

Outputs: Completed Script (separated audio/visual channels with timings), Storyboard (scene-by-scene with visual descriptions and asset seeds), Shot List (angles, lighting, camera motions), Voice Audio Files, Generated Visual Assets.

Quality Gate: All generated assets must pass entity DNA compliance check before advancing to Phase 3.

### 2.3 Phase 3: Production Excellence

Objective: Assemble raw assets into finished media with cinema-grade technical quality.

Inputs: All approved assets from Phase 2.

Steps:

1. Timeline Assembly: Align audio tracks with visual elements in the designated editing platform. Structural separation of narrative audio from visual callouts, screen descriptions, and text overlays must be maintained.

2. Audio Mastering:
   - Music bed: -18dB to -12dB below primary voiceover.
   - Normalize to -14 LUFS for streaming delivery.
   - Minimum 192kbps AAC for audio-only deliverables.

3. Graphics Overlay: Render text callouts and subtitle tracks. Zero phonetic spelling errors. Closed captions must be accurate.

4. Technical Quality:
   - Resolution: 4K (3840x2160) minimum for hero/featured content. 1080p minimum for web delivery. Up to 8K for archival.
   - Frame Rate: 24-30fps for cinematic/social delivery. Up to 60fps for smooth motion requirements.
   - Codec: H.264 AVC or H.265 within MP4 container.
   - Bitrate: 45-60 Mbps at 30fps. 60-80 Mbps at 60fps.

Outputs: Assembled Master Video, Audio Master, Graphics Package, Technical Specification Sheet.

Quality Gate: Automated preflight checklist must verify entity DNA compliance, caption accuracy, audio balance, AI artifact absence, and secrets management (no API keys in project files).

### 2.4 Phase 4: Strategic Distribution

Objective: Package and deliver finished media to target platforms with proper metadata and compliance.

Inputs: Approved master from Phase 3.

Steps:

1. Format Optimization:
   - 16:9 widescreen for YouTube, web embeds, presentations.
   - 9:16 vertical for Instagram Reels, TikTok, YouTube Shorts.
   - 1:1 square for LinkedIn, Facebook feed.
   - WebM fallback for web-only delivery.

2. Metadata Attachment: Embed title tags, meta descriptions, analytics hooks, and entity branding. Apply D07 SEO/GEO/AEO standards (no em dashes in metadata).

3. Thumbnail Generation: 16:9 aspect ratio, minimum 1280x720, brand overlay on lower third. Apply D09 brand palette.

4. Distribution Package: Bundle all deliverables with a plain-text manifest listing file name, format, resolution, duration, file size, and intended placement.

5. Tribunal Submission: Push the complete package to `05_Tribunal_Inbox` for DCS Level 0 approval before public release.

Outputs: Platform-Optimized Video Files, Metadata Package, Thumbnail Set, Distribution Manifest, Tribunal Submission Record.

Quality Gate: No public release without DCS Level 0 signoff. All public-facing video is restricted to Agentic Level 1 (Supervised).

---

## 3. Model-Duty Assignment Matrix

| Role | Primary Model | Backup Model | Phase(s) |
|---|---|---|---|
| Script writing, narrative structure | Claude | ChatGPT | 1, 2 |
| Storyboard, shot lists, metadata | ChatGPT | Gemini | 2 |
| Visual generation, editing optimization | Gemini/Veo/Sora | DALL-E | 2, 3 |
| Voice synthesis | ElevenLabs (tool) | — | 2 |
| Test checklists, file routing | Codex/AG | Claude Code | 2, 3, 4 |
| Entity DNA review, brand compliance | Claude | Qwen-Max | 1, 3, 4 |
| Timeline assembly, audio mastering | PowerDirector (tool) | — | 3 |

Model assignments are authoritative but not rigid. If a model is unavailable, the backup model may execute. The DCL (D21) must log any assignment deviation.

---

## 4. Trigger Mechanism

### 4.1 Explicit Triggers

- User says "produce video," "create media," "run production pipeline," "build video," "media production."
- User invokes a media production skill.
- User requests a specific Phase (e.g., "write a video script" triggers Phase 1-2).

### 4.2 Implicit Triggers

- The task involves video scripting, storyboarding, or shot list creation.
- The task involves audio production, voiceover, or podcast content.
- The task involves motion graphics, animated content, or video editing.
- The task involves media distribution, thumbnail creation, or platform optimization.
- The task references D12 or media production standards.

### 4.3 Trigger Announcement

When D18 activates, the model must announce:
"Media Production Pipeline activated. Running Phase 1 (Strategic Foundation) > Phase 2 (Asset Creation) > Phase 3 (Production Excellence) > Phase 4 (Distribution)."

If only specific phases are triggered, announce those phases only.

### 4.4 Cross-Methodology Triggers

- If visual asset creation is needed during Phase 2, D19 (Visual Creation Pipeline) activates as a sub-pipeline.
- If adversarial analysis is needed (competitive positioning of media content), D17 (DART Universal) activates in parallel.
- If the media is part of a product build, D20 (Product Assembly) is the parent pipeline and D18 runs as a phase within it.

---

## 5. Core Deliverable Outputs

Every media production must produce these four structured deliverables:

1. Script: Separated audio/visual channels with exact timings.
2. Storyboard: Scene-by-scene map with visual descriptions and asset seeds.
3. Shot List: Technical breakdown of angles, lighting, and camera motions.
4. Production Brief: Metadata sheet with target resolution, codecs, bitrates, and model paths.

---

## 6. Quality Gates Summary

| Gate | Phase | Condition | Failure Action |
|---|---|---|---|
| Video Build Declaration | 1 | Must be complete before production | Stop-gate |
| Entity DNA Compliance | 2 | All assets match declared entity | Reject and regenerate |
| Preflight Checklist | 3 | Captions, audio, artifacts, secrets | Reject and remediate |
| DCS Level 0 Signoff | 4 | Required for public release | Hold in Tribunal Inbox |
| Live Preview | 3-4 | If output is browser-renderable | Fix before reporting complete (D21 Section 6) |

---

## 7. Cybersecurity Integration

Per D21 Section 5:

- No API keys for generation tools (ElevenLabs, Sora, DALL-E) may be hardcoded in scripts, prompts, or project files.
- No voice model credentials or synthesis API tokens in client-facing code.
- Media metadata must not contain internal system paths, Supabase project IDs, or governance references.
- Distribution manifests for public channels must be sanitized per D21 Section 5.3.

---

## 8. Tier Access

| Tier | D18 Access |
|---|---|
| Tier 1 Sovereign | Full pipeline, all phases, model-duty matrix, QA gates, Tribunal routing |
| Tier 2 Internal Collaborator | Pipeline phases without model-duty matrix. No Tribunal routing. QA gates apply. |
| Tier 3 External Product Build | Production specs only (Section 4 of Tier 3 Product Build Extract). No pipeline access, no model assignments. |

---

## Related Doctrine

- D12_Video_Media.md — Governance authority for video/media (D18 extracts methodology from D12)
- D19_Visual_Creation_Pipeline.md — Sub-pipeline for visual asset creation (Phase 2 integration)
- D17_DART_Universal_Methodology.md — Parallel methodology for adversarial analysis of media content
- D20_Product_Assembly_Methodology.md — Parent pipeline when media is part of a product build
- D09_Brand_Identity.md — Brand palette and controlled terms for media branding
- D07_Campaign_Governance.md — SEO/GEO/AEO standards for media metadata
- D21_Doctrine_Runtime_Engine.md — DCL logging, cybersecurity baseline, live preview mandate

---

## Error-Catch Protocol

If this doctrine file is missing or unreadable, follow the canonical error-catch protocol:
1. HALT execution. Do not infer media production rules from pre-training.
2. LOG `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. TRIGGER STOPGATE and alert the user.
4. FALLBACK: If D18 is unavailable, D12 remains the sole authority for media production governance and methodology.
