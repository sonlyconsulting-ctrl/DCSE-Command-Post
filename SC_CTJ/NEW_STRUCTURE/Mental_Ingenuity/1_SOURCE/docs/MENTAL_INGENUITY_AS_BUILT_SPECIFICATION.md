# Mental Ingenuity: As Built Specification

## Corrective baseline, 2026-08-09

This specification is read with the root corrective acceptance receipt. The corrective baseline repairs reduced-motion media, cumulative and final-action telemetry, production solution-oracle exposure, SC visual tokens, locked-node readability, per-channel visibility audio restoration, media evidence, test commands, screenshots, and checksum packaging. The corrected independent disposition is PARTIAL solely because a manual screen-reader and formal WCAG audit remain before any public-release decision.

Powered by Sonly Consulting

This document describes what was actually implemented, executed, and
verified in the delivered prototype. It is an as built record, not a plan.
Release state: internal prototype. Not authorized for public release until
reviewed and approved.

## 1. Stack and structure

- React 18.3 with TypeScript 5.6 in strict mode, bundled by Vite 6.4
- Runtime dependencies: react and react-dom only. No backend, no paid API,
  no secret keys
- Persistence: localStorage with validated schema and safe fallback
- Verification tooling: Playwright with headless Chromium, Python numpy plus
  imageio ffmpeg for original media generation

```
index.html, package.json, package-lock.json, tsconfig.json, vite.config.ts
src/          app shell, styles, store, audio engine, lib, views, chambers
scripts/      make_audio.py, make_video.py, brandScan.mjs
tests/        e2e.mjs, media.mjs
public/       favicon.svg and media/img, media/video, media/audio
docs/         architecture, chambers, verification, manifests, receipts,
              screenshots, logs, SHA256 manifest
```

## 2. Views implemented and verified

1. Cinematic opening with original MP4 and WebM cinematic, poster, loading
   indicator, skip, replay, captions, transcript, reduced motion still
   alternative, and graceful codec failure fallback
2. Start screen with exact brand lockup and opening line
3. How to Play
4. Chamber map with locked, active, and complete node states
5. Six playable chamber environments
6. Pause interface that suspends audio and offers resume, mute, volume, quit
7. Level completion analysis (Reasoning Record) with dimension bars and
   attempt diff narrative
8. Final Reasoning Signature with emblem, title, recorded evidence, and
   non diagnostic disclaimer
9. Progress and achievements (eight achievements)
10. Settings with master, music, ambience, and effect volumes, mute, reduced
    motion, high contrast, and captions
11. About with exact brand attribution
12. Restart confirmation modal
13. Resume session interface driven by the in flight record
14. Accessibility help view

## 3. Chamber mechanics as built

- The Signal Chamber: seeded walk patterns in three families on 5, 6, and 7
  cell grids with noise flashes, presentation then recall, replay, and hint
  reveal. Verified: three challenges completed through the UI
- The Constraint Forge: mirror rotation under move budgets, beam tracer with
  reflection tables, locked plating, undo and reset, efficiency against par.
  Verified: three challenges completed
- The Perspective Engine: three twelve slot rings with per level gear
  coupling, BFS par, button, keyboard, and drag rotation, alignment beam
  feedback. Verified: three challenges completed without overlay click
  interception
- The Causal Labyrinth: integer node systems with delayed and memory nodes,
  tick advance, stability counters, resettable experiments, authored causal
  explanations. Verified: three challenges completed
- The Paradox Vault: evidence board with role mapping, verdicts, and
  explanation panel across three authored cases. Verified: three challenges
  completed
- The Summit: trace plus route plus alignment plus gate synthesis with a
  visible mid climb law revision, adaptive tolerance from prior scores, and
  first decision adaptability evidence. Verified: three challenges completed

## 4. Scoring, records, signature

- Four dimensions per challenge: Accuracy, Efficiency, Insight, Adaptability,
  up to 300 points each. Hint spending reduces Insight
- Reasoning Record per challenge lists detection, governing constraint,
  attempts, moves, misreads, hints, strategy, decisive evidence, and change
  versus the previous attempt
- Final signature picks one of six titles from chamber affinity and
  dimensions, explained with recorded evidence lines only, plus an explicit
  statement that it is not a diagnosis or trait claim

## 5. Multimedia as built

- 10 WebP artworks, 1 JPEG poster, 1 SVG favicon, inline SVG emblems
- 16 second 1920x1080 24 fps opening cinematic in H.264 MP4 and VP9 WebM,
  rendered frame by frame by scripts/make_video.py. No text inside frames
- 7 music tracks, 6 ambiences, 14 SFX synthesized by scripts/make_audio.py as
  seamless OGG loops
- Audio engine: gesture only initialization, three independent channels,
  crossfades, pause suspension, tab visibility pause and resume, mute
  persistence, pooled SFX to prevent stacking
- Every audio clue has a visual equivalent. Captions and transcript provided.
  Reduced motion serves a still alternative with the transcript

## 6. Accessibility as built

- Semantic landmarks, skip link, visible gold focus outlines, high contrast
  mode, polite live region feedback, labeled grid cells, mirrors, rings,
  gates, cards, and slots
- Keyboard only completion verified for the Signal Chamber. Touch verified on
  mobile context. Reduced motion verified via OS and in app settings
- No horizontal overflow at 1440x900, 1920x1080, and 390x844

## 7. Verification results (direct execution)

- Production build: PASS
- E2E suite: 47 of 47 PASS, including full six chamber ascent through the
  real UI, persistence, resume, corrupted save recovery, locked chamber
  guard, pause, reset telemetry, visibility pause and resume, keyboard only
  completion, mobile touch, and console cleanliness
- Media suite: 46 of 46 PASS, including decode of all 27 OGG files, serving
  of all raster and video assets, muted autoplay, skip, replay, and reduced
  motion still
- Brand scan: CLEAN. Exact wording present. Zero unauthorized consulting
  name variants. Zero em or en dashes
- Screenshots: 18 files in docs/screenshots
- Machine readable outputs: docs/e2e-results.json, docs/media-results.json,
  docs/SHA256_MANIFEST.txt, docs/logs/

## 8. Deviations and known limitations

- Refresh during a challenge restarts that board from its initial state while
  restoring attempt counters and the event log. Full mid board serialization
  is intentionally out of scope for the prototype
- The WebM fallback adds roughly 3 MB for codec safety. Browsers that support
  H.264 never download it in practice because the MP4 source precedes it in
  selection order after the browser skips unsupported types
- Music is deliberately restrained and synthetic. A live production pass is
  the recommended next step
- Playwright execution requires Chromium plus system libraries on the machine
  running tests

## 9. Remediation record (this recovery pass)

- Preserved pre edit source in RECOVERY_pre-edit_source.tar.gz before edits
- Confirmed decorative beam and axis overlays use pointer-events none while
  mirrors, rings, and cells remain interactive
- Fixed tab visibility resume path so returning to a visible tab restores
  exactly the tracks that were paused
- Added regression checks for visibility pause and resume and cumulative
  reset telemetry, then re ran all suites to green

## 10. Release boundary

This build is an internal prototype. It must not be described as promoted,
deployed, production ready, or publicly released. Public release requires the
standing review and approval step.
