# Architecture Summary

Stack: React 18, TypeScript strict mode, Vite 6. No backend, no paid services,
no runtime dependencies beyond react and react-dom.

## State

`src/state/store.tsx` holds a single reducer with the save file as the
persistent core. Every mutation flows through actions: NAVIGATE, START_LEVEL,
COMPLETE_LEVEL, USE_HINT, SET_SETTINGS, restart and modal actions. The save is
written to localStorage after every change with schema validation on load
(`src/lib/persistence.ts`), so corrupted or foreign data falls back to a fresh
save instead of crashing.

The save contains settings, unlocked chambers, per chamber results and best
scores, achievements, remaining hints, finished flag, and an in flight record
that powers resume after refresh.

## Scoring

`src/lib/scoring.ts` converts each level report into four dimensions:
Accuracy, Efficiency, Insight, Adaptability. Each level yields up to 300
points. The final signature (`src/lib/signature.ts`) aggregates chamber
affinity plus dimensions to pick one of six descriptive titles and explains it
with evidence lines drawn only from recorded behavior.

## Chambers

Each chamber owns its own interaction state and reports through a shared
`useSession` hook (`src/chambers/shared.tsx`) that tracks moves, errors,
attempts, hint spending, and events, then dispatches COMPLETE_LEVEL. The shell
renders objective, HUD, reset, pause, and the live region for feedback.

Determinism: every board derives from a seeded generator (`src/lib/rng.ts`),
so each challenge configuration is reproducible per chamber, level, and
attempt.

- SignalChamber: seeded random walk patterns in three families (cardinal,
  diagonal, leaping), noise flashes, presentation then recall.
- ConstraintForge: string defined grids parsed into cells, a beam tracer with
  mirror reflection tables, move budgets, undo stack, locked plating.
- PerspectiveEngine: three rings of twelve slots with per level gear coupling
  matrices, BFS computed par, rotation by buttons, keyboard, or pointer drag.
- CausalLabyrinth: integer node systems with delayed and memory nodes, tick
  simulation, stability counters, authored explanations.
- ParadoxVault: authored evidence cases with role mapping and verdict,
  explanation panel before sealing.
- Summit: integrates trace, route, and alignment stages, then a gate choice
  under a law that visibly revises mid climb. Adaptive tolerance reads prior
  best scores.

## Audio

`src/audio/engine.ts` runs three channels (music, ambience, SFX) on pooled
HTMLAudio elements. The engine initializes only on a user gesture, crossfades
scene changes, pauses on tab hide and pause overlay, honors per channel
volumes and mute, and never duplicates a track.

## Multimedia

All media is original. Images are generated artwork converted to WebP, the
cinematic is rendered frame by frame by scripts/make_video.py and encoded to
H.264 MP4 plus VP9 WebM, and every music, ambience, and effect file is
synthesized by scripts/make_audio.py from periodic components so loops join
seamlessly.

## Views

App.tsx maps the View union to components. The pause overlay suspends audio.
The restart flow requires confirmation and clears storage. The cinematic view
handles autoplay rules, captions, skip, replay, failure fallback, and the
reduced motion still alternative.
