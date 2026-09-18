# Verification Report

Environment: Node 20.20.2, Debian 13, headless Chromium via Playwright,
app served by `npm run preview` on port 4173.

## Suites

- `npm run build` : TypeScript strict compile plus Vite bundle. PASS
- `npm run test:e2e` : 47 of 47 checks PASS
- `npm run test media` (tests/media.mjs) : 46 of 46 checks PASS
- `npm run brand-scan` : CLEAN (exact brand wording present, no unauthorized
  consulting names, no em or en dashes in interface, docs, or filenames)

## E2E coverage (47 checks)

- Cinematic opens with exact brand text and attribution. Skip works. Start screen and opening line render
- Audio engine does not initialize before a user gesture
- Full ascent: all six chambers, all eighteen challenges completed by driving the real UI, each producing a Reasoning Record
- Final Reasoning Signature reached with a valid title and disclaimer
- Save contains finished flag, summit results, and all eight achievements
- Reload shows continue. Six completed chambers persisted
- Corrupted localStorage save falls back safely with a recovery notice
- Locked chamber cannot be entered
- Refresh during a chamber offers resume. Resume returns into the chamber
- Pause overlay opens and closes. Quit returns to map
- Reduced motion setting applies the motion suppression class
- Keyboard only completion of Signal Chamber challenge 1 (Tab, Enter, focus rings)
- 1920 by 1080 desktop and 390 by 844 mobile portrait: zero horizontal overflow
- Touch tap enters a chamber on mobile
- No material console errors. No uncaught page errors
- Browser visibility pause and resume: hidden tab pauses music, visible tab resumes it
- Reset telemetry: reset increments the attempt counter and zeroes moves while events stay cumulative

## Media coverage (46 checks)

- All ten WebP images, MP4, WebM, and poster served with HTTP 200
- All 27 OGG audio files decode in WebAudio with expected durations
- Cinematic video autoplays muted (readyState 4, currentTime advancing) and starts muted
- Reduced motion serves the still alternative: poster, transcript, no video element
- Missing asset request resolves without page failure
- No console errors during media playback

## Accessibility spot checks performed in E2E

- Keyboard-only route through cinematic, start, map, and a full chamber completion
- Focus outlines visible in screenshots. Live regions announce feedback
- Accessible names present on grid cells, mirrors, rings, gates, cards, and slots

## Negative matrix (all exercised)

- Refresh during a chamber: PASS via in flight record
- Refresh after completion: PASS via persisted results
- Corrupted local state: PASS with fresh fallback and notice
- Rapid repeated clicks: PASS (begin, pause, continue paths)
- Keyboard-only completion: PASS
- Touch interaction: PASS
- Narrow mobile viewport: PASS, no overflow
- Large desktop viewport: PASS, no overflow
- Reduced motion preference: PASS, still cinematic and calm UI
- Sound disabled and muted startup: PASS, no audio before gesture
- Repeated reset: PASS (reset counted as attempts without crash)
- Hint before an attempt and hint exhaustion: PASS (guarded, message shown)
- Move budget exhaustion: PASS (error path plus reset suggestion)
- Locked chamber skip attempt: PASS (button disabled)
- Summit rule change: PASS (law panel revision verified in UI and save)
- Missing optional asset: PASS (onError hides, 404 tolerated)
- Invalid player action: PASS (wrong cells, wrong placements counted as errors)

## Known limitations

- Refresh during a challenge restarts that challenge board from its initial
  state. Attempts and progress counters are restored, mid board state is not serialized
- The opening cinematic video relies on browser codec support. On unsupported
  browsers the poster fallback engages automatically
- Playwright system libraries must be installed on the machine running tests
- Music loops are intentionally minimal and meditative rather than orchestral

## Remediation performed during the build

- Replaced invalid HTML button inside SVG with focusable SVG groups
- Added pointer-events none to beam overlays that intercepted mirror clicks
- Corrected accessible names so they match visible labels on start and resume
- Deduplicated the summit law evidence line in the Reasoning Signature
- Fixed test harness browser cleanup so failures exit cleanly
