# Mental Ingenuity

Powered by Sonly Consulting

Internal prototype of a layered mental adventure. Not authorized for public
release until reviewed and approved.

## What it is

Mental Ingenuity is a browser game in which the player climbs The Ingenuity
Ascent, a sequence of six chambers. Each chamber exercises a different mode of
reasoning through a genuine interactive mechanic:

1. The Signal Chamber: perception, pattern recognition, evidence filtering
2. The Constraint Forge: planning under constraints, sequencing, efficiency
3. The Perspective Engine: spatial reasoning, mental rotation, abstraction
4. The Causal Labyrinth: systems thinking, cause and effect, feedback loops
5. The Paradox Vault: deductive review, assumption detection, evidence reconciliation
6. The Summit: synthesis, adaptability, cross domain reasoning, and a discoverable rule change

The product makes no medical, psychological, diagnostic, therapeutic, or
cognitive improvement claims. Scores describe gameplay behavior only.

## Startup instructions

Requirements: Node.js 20 or newer, npm.

```
npm install
npm run dev        # development server on http://localhost:5173
```

Production style run:

```
npm install
npm run build      # type check and bundle into dist/
npm run preview    # serves the build on http://localhost:4173
```

No paid API, no secret keys, no backend. Progress persists in localStorage.

## Commands

- `npm run dev` start the development server
- `npm run build` type check with tsc, then bundle with Vite
- `npm run preview` serve the production build
- `npm run test:e2e` run the full Playwright verification suite (requires `npm run preview` running and Chromium installed via `npx playwright install chromium`)
- `npm run brand-scan` verify exact brand wording and typography rules across the project

Browser test prerequisites used during this build (already installed in the
reference environment): system Chromium libraries for Playwright.

## Project layout

```
index.html                 entry document
src/
  main.tsx                 React bootstrap
  App.tsx                  view router, scene audio, pause and restart overlays
  styles.css               full visual system
  audio/engine.ts          music, ambience, and SFX channels with crossfades
  lib/                     seeded rng, types, scoring, signature, achievements, persistence, content
  state/store.tsx          reducer plus localStorage persistence
  components/ui.tsx        buttons, sliders, toggles, modals, emblems
  views/                   cinematic, start, howto, map, record, signature, progress, settings, about, help, resume, pause
  chambers/                the six playable mechanics plus shared session shell
scripts/
  make_audio.py            original music, ambience, and SFX synthesis
  make_video.py            original opening cinematic renderer
  brandScan.mjs            brand and typography verifier
tests/
  e2e.mjs                  full player route and negative test suite
  media.mjs                multimedia playback and accessibility verification
public/
  favicon.svg              application icon
  media/img/               original WebP artwork and poster
  media/video/             opening cinematic MP4, WebM fallback, poster JPG
  media/audio/             original OGG music, ambience, and effects
docs/                      verification, manifest, receipts, screenshots
```

## Accessibility summary

Semantic landmarks, visible focus outlines, keyboard operable controls
everywhere including grid cells, mirrors, rings, and evidence cards, polite
live regions for gameplay feedback, reduced motion mode with a still cinematic
alternative, high contrast mode, separate music, ambience, and effect volumes
with a master mute, and captions for the opening cinematic. No puzzle requires
sound as its only information channel.

## Legal and brand

Product name shown exactly as: Mental Ingenuity
Attribution shown exactly as: Powered by Sonly Consulting
All art, music, ambience, sound effects, and the opening cinematic are
original assets created for this product. No third party logos, licensed
characters, or stock media are used.
