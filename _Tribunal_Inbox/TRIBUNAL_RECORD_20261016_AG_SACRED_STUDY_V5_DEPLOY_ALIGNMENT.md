# Tribunal Record: Sacred Study v5 Deployment, Ambiance, Voice Selection & Routing Resolution

**Record ID:** `TRIB-REC-20261016-AG-SACRED-STUDY-V5-DEPLOY-ALIGNMENT`  
**Date:** 2026-10-16  
**Actor:** Antigravity (AG) — Sovereign Auditor & Gatekeeper  
**Principal:** DCS (Donald C. Seals Jr.)  
**Repository:** `DCSE_Command_Center`  
**Branch:** `feat/sc-components-20261012-01-contracts` (Merged into `main` via PR #192, Commit: `374d68c`)  
**Deployment Target:** `https://sc-escd.vercel.app/scripture` & `https://sc-escd.vercel.app/escd/app`

---

## 1. Executive Summary & Root Cause Analysis

Following DCS directive and analysis of Claude handoff findings:
1. **Login Screen Redirection Root Cause**:
   - The root `vercel.json` redirected `/` unconditionally to `/escd` (`login.html`), while missing an explicit rewrite for `/scripture`. Consequently, direct clicks on `🌐 Live App ↗` from the Products card or direct navigation to `/scripture` hit the unauthenticated operator sign-in barrier (`login.html`).
   - The products catalog (`apps/escd/runtime/escd-products-catalog.json` and `content/escd-products-catalog.json`) held `live_url: "https://sc-escd.vercel.app"`, sending users to the root redirect rather than the dedicated `/scripture` route.
2. **Truncated Chapter Display & Read Aloud**:
   - The Scripture app had hardcoded 3-verse fragments in `BIBLE['2 Samuel'][7]` (verses 1, 16, 22) and 2 verses for Psalm 139 (14, 23). The chapter loader checked `if (cached) renderVerses(cached);`, truncating 2 Samuel 7 from its full 29 verses down to 3 sample verses and preventing the voice reader from reading the whole chapter.
3. **Missing Ambiance & Voice Customization**:
   - Chapter Reader previously lacked the contemplative 432 Hz Scriptorium ambient soundscape and did not offer user selection between Female and Male speech synthesis voices.

---

## 2. Implemented Resolutions

1. **Chapter Reader Full Chapter Display**:
   - Pre-seeded all 29 verses of 2 Samuel 7, 24 verses of Psalm 139, 39 verses of Romans 8, 36 verses of John 3, and all 23 daily study chapters with complete verse text.
   - Enhanced `renderChapter()` to load all verses seamlessly without truncation.
   - When transitioning from Daily Verse via "📖 Read Full Chapter", loads the whole chapter and smoothly scrolls to highlight the featured verse in context.
2. **Whole Chapter Read Aloud with Female / Male Voice Selection**:
   - Added Reader Voice Selection dropdown (`♀ Female Voice`, `♂ Male Voice`, `Default Voice`) with automatic system voice matching and localStorage persistence.
   - Read Aloud reads the entire chapter sequentially (announces chapter heading, then iterates `Verse X: [text]` through chapter end).
   - Dynamically highlights the active verse on screen with smooth scrolling as speech progresses.
3. **432 Hz Scriptorium Ambiance Music**:
   - Built a pure Web Audio API ambient harmonic generator (432 Hz sine root + 216 Hz warm sub-harmonic with smooth gain envelope).
   - Added toggle button (`🎵 Ambiance`) with active pulsing gold/emerald visual feedback that runs alongside voice reading or independently during contemplative study.
4. **Unified Vercel Routing**:
   - Configured root `vercel.json` and `apps/escd/vercel.json`:
     - `/scripture` -> `/apps/escd/web/scripture.html`
     - `/` -> `/apps/escd/web/scripture.html`
     - `/escd/app` -> `/apps/escd/web/mvp.html`
     - `/escd` and `/login` -> `/apps/escd/web/login.html`
   - Updated product catalogs and preview files to direct `live_url` to `https://sc-escd.vercel.app/scripture`.
5. **Zero-Localhost Preview Delivery**:
   - Generated and synchronized `sc_sacred_study_v5_preview.html` and `apps/escd/web/sc_sacred_study_v5_preview.html` with the verified DCSE Sovereign Executive Review Bar.

---

## 3. GitHub & Deployment Finality
- Pull Request #192 opened, all regression contract tests verified (11/11 passing), and cleanly merged into `main` (`374d68c`).
- Vercel CI completed successfully for all linked services (`sc-escd`, `sc-command-post`, `sc-agent-os`, `b4l`).
