# DCSE Video Factory: Raw Asset Ingest & CyberLink PowerDirector MCP Bridge (v7.3-4)

**Status:** ACTIVE PROPOSAL // ARCHITECTURAL BRIDGE  
**Authority:** DCS Level 0 / Sonly Consulting  
**Classification:** DCSE Internal // SC-Media  
**Framework Baseline:** DCSE v7.3-4 Canonical Governance & Multi-Model Production Harness  
**Target Projects:** `SC-MyMy`, `SJL-B4Life`, `SC-CTJ`, DCSE Digital Campaigns  

---

## 1. Context & Architectural Problem

DCSE has extensive video doctrines (`D12_Video_Media`, `15_Video_Content_Framework_Doctrine_v6`, `16_Video_Technical_Production_Doctrine_v6`, `TRIB-20260607-SC-B4L-VIDEO-PIPELINE-DISPATCH`, and `video_production_workflow.html`). However, there has been an operational gap between **raw media capture** and **actionable video production**:
1. Single-purpose AI tools like HeyGen handle only talking-head avatars and fail at complex sports montage, multi-track audio, or action pacing.
2. Generative engines like Google AI Studio (Veo 2/Imagen 3) or OpenAI (Sora/DALL-E) yield isolated short clips rather than an edited narrative product.
3. Raw camera/mobile shoots (such as `SC-MyMy` from October 1, 2026) produce dozens of files (WAV audio, MPG/MP4 video clips, chronological burst JPG frames, AI concept art) that require structured assembly before creative editing can begin.

This architecture bridges that gap under **v7.3-4 Governance** by creating an automated ingest harness and a dedicated **CyberLink PowerDirector MCP Connector**.

---

## 2. The Raw Ingest Bridge: Zero-Discard Pre-Production Assembly (Draft 1)

### 2.1 The Ingest Principle
**Rule:** *Zero Discard on Draft 1.*  
Before editorial selection or creative cutting begins, 100% of the raw captured assets must be placed in chronological order onto the project timeline based on filesystem timestamps and sequence metadata.

### 2.2 Case Study: `SC-MyMy` Raw Ingest Sequence (2026-10-01)
- **Act 1: Setting & Team (03:17 – 03:46 EDT):**
  - Source Context: `bluetooth_content_share (2).html` (Sectional Semifinals news)
  - Establishing Kickoff Video: `CHS.mpg` (native duration)
  - Team Sideline Stills: `My CHS Team1.jpg`, `My CHS Team2.jpg`, `My CHS jpg.jpg` (3.0s display duration each)
- **Act 2: Play Progression & Burst Action (04:10 – 04:23 EDT):**
  - Pre-snap setup: `My 2 CHS jpg.jpg`, `My 3 CHS jpg.jpg`, `My 0 CHS jpg.jpg`, `My 1 CHS jpg.jpg`
  - Play Burst Sequence: `My 1-1 CHS jpg.jpg` through `My 1-12 CHS jpg.jpg` (12 frames sequenced at 0.6s per frame to produce an animated flip-book progression of the flag football play)
  - Reaction Still: `My 4 CHS jpg.jpg`
- **Act 3: Commentary & AI Vision Cards (04:47 – 05:26 EDT):**
  - Audio Narration Part 1: `Capture_20261001034047 (0).WAV` (3.4 MB voiceover track on Audio 1)
  - AI Concept Visuals: `ChatGPT Image Oct 1, 2026, 05_08_11 AM.png`, `05_19_55 AM.png`, `05_26_42 AM-1.png`, `05_26_46 AM-2.png`
- **Act 4: Climax Action & Collectible Finale (05:56 – 20:56 EDT):**
  - Audio Narration Part 2: `Capture_20261001034047 (1).WAV` (3.5 MB voiceover track continuing on Audio 1)
  - Commemorative Collectible Art: `MyMy NFT.jpg`, `MyMy NFT 0.jpg`
  - Climax Live Action Clip: `Somya Deefenvsive Posture.mp4` (9.9 MB highlight video)

### 2.3 The DCS Review Loop (Draft 1 to Draft 2)
1. **Draft 1 (Pre-Production Assembly):** Comprehensive assembly containing all 32 assets. Generated programmatically.
2. **DCS/SC Review Gate:** DCS reviews the complete assembled cut to evaluate narrative flow, identify weak frames, and determine trimming points.
3. **Draft 2 (Production Master):** Unneeded stills removed, audio ducked/leveled, transitions (crossfades/dip-to-black) applied, lower-third titles added, and multi-format exports produced (16:9 widescreen master + 9:16 vertical short).

---

## 3. Tooling Landscape & CyberLink PowerDirector MCP

### 3.1 Why PowerDirector 16 Is The Right Primary NLE Engine
- **Existing Asset & Licensing:** Lifetime licenses owned for PowerDirector 12 and 16. Installed on production host (`C:\Program Files\CyberLink\PowerDirector16\PDR.exe`).
- **File Format Discovery:** PowerDirector `.pds` project files are **native XML documents** (`<Project ActiveApplication="PowerDirector" AppVersion="16" ...>`).
- **Zero Lock-In:** Because the project format is XML, agents can inspect, generate, and modify `.pds` files directly without needing proprietary SDK licenses.

### 3.2 PowerDirector MCP Architecture (`powerdirector-mcp`)
```
+-----------------------------------------------------------+
|                   DCSE Agent OS (v7.3-4)                  |
+-----------------------------------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|              PowerDirector MCP Connector                  |
|  - pds_scaffold_project(folder, options) -> .pds XML     |
|  - pds_inspect_project(pds_path) -> track manifest        |
|  - pds_sync_audio(pds_path, audio_files) -> audio tracks  |
|  - pds_open_editor(pds_path) -> launches PDR.exe          |
+-----------------------------------------------------------+
         |                                          |
         v                                          v
 [Generates .pds XML]                  [Launches Desktop GUI]
  MyMy_Draft1.pds                       C:\Program Files\CyberLink\
                                        PowerDirector16\PDR.exe
```

### 3.3 Alternative Tooling Matrix
1. **Python + FFmpeg (`build_v2_videos.py`):**
   - Headless automated command-line rendering.
   - Already present in `sonly_campaign_mvp_voice_video_patched_package.zip`.
   - Role: Generates the instant MP4 video preview of Draft 1 in seconds.
2. **CyberLink PowerDirector 16 (`PDR.exe` + `.pds`):**
   - Desktop visual Non-Linear Editor with GPU acceleration.
   - Role: Where DCS performs hands-on fine-tuning, audio ducking, color timing, and final production master export.
3. **Google AI Studio (Veo 2 / Imagen 3) & OpenAI (Sora / DALL-E):**
   - Generative upstream asset creators.
   - Role: Feeds raw clips and concept art into the ingest folder, not used as editors.

---

## 4. Implementation Directives under v7.3-4

1. **Cataloging & Version Control:** All video pipeline dispatches and discovery manifests must be committed to `DCSE-Tribunal-Relay` (`_Tribunal_Inbox`) and `DCSE-Command-Post` with clear version receipts.
2. **DCS Signoff Prerequisite:** No external video publication or distribution shall occur without explicit DCS Level 0 signoff.
3. **Next Technical Action:** Finalize the Python `.pds` generator script to output `MyMy_Flag_Finale_Draft1_Full.pds` and test opening in `PDR.exe`.
