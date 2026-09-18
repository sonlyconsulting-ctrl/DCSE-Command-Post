# File Manifest

## Root

- package.json: scripts and dependencies
- package-lock.json: lockfile
- tsconfig.json: strict TypeScript config
- vite.config.ts: dev and preview server config
- index.html: entry document with meta and favicon
- README.md: startup instructions and overview

## public

- public/favicon.svg: application icon
- public/media/img/: hero.webp, map.webp, chamber_signal.webp, chamber_forge.webp, chamber_perspective.webp, chamber_causal.webp, chamber_vault.webp, chamber_summit.webp, about.webp, social.webp
- public/media/video/: opening.mp4, opening.webm, poster.jpg
- public/media/audio/: music_opening.ogg, music_map.ogg, music_focus.ogg, music_structure.ogg, music_tension.ogg, music_summit.ogg, music_complete.ogg, amb_signal.ogg, amb_forge.ogg, amb_perspective.ogg, amb_causal.ogg, amb_vault.ogg, amb_summit.ogg, sfx_select.ogg, sfx_place.ogg, sfx_invalid.ogg, sfx_rotate.ogg, sfx_connect.ogg, sfx_activate.ogg, sfx_reset.ogg, sfx_hint.ogg, sfx_discover.ogg, sfx_complete.ogg, sfx_unlock.ogg, sfx_rule_change.ogg, sfx_achievement.ogg, sfx_final.ogg

## src

- src/main.tsx, src/App.tsx, src/styles.css
- src/lib/rng.ts, types.ts, scoring.ts, signature.ts, achievements.ts, content.ts, persistence.ts
- src/state/store.tsx
- src/audio/engine.ts
- src/components/ui.tsx
- src/chambers/shared.tsx, SignalChamber.tsx, ConstraintForge.tsx, PerspectiveEngine.tsx, CausalLabyrinth.tsx, ParadoxVault.tsx, Summit.tsx
- src/views/Cinematic.tsx, Start.tsx, HowTo.tsx, MapView.tsx, RecordView.tsx, SignatureView.tsx, ProgressView.tsx, SettingsView.tsx, AboutView.tsx, HelpView.tsx, ResumeView.tsx, PauseOverlay.tsx

## scripts

- scripts/make_audio.py: original audio synthesis source
- scripts/make_video.py: original cinematic render source
- scripts/brandScan.mjs: brand and typography verifier

## tests

- tests/e2e.mjs: full route and negative suite
- tests/media.mjs: multimedia verification suite

## docs

- docs/ARCHITECTURE.md, CHAMBERS.md, VERIFICATION.md, MULTIMEDIA_MANIFEST.md, EVIDENCE_RECEIPT.md, FILE_MANIFEST.md
- docs/e2e-results.json, docs/media-results.json: machine readable run output
- docs/screenshots/: 01-cinematic.png, 01b-cinematic-playing.png, 01c-cinematic-reduced.png, 02-start.png, 03-map.png, 04-thesignalchamber.png, 04a-signal-showing.png, 04b-signal-recall.png, 05-theconstraintforge.png, 06-theperspectiveengine.png, 07-causallabyrinth.png, 08-paradoxvault.png, 09-summit.png, 10-signature.png, 11-settings.png, 12-pause.png, 13-mobile-map.png, 14-mobile-chamber.png
