# SS production release, 2026-10-22

Task: DCSE-MEDIA-RECONCILIATION-20261021-01

DCS authorized completion, Vercel deployment, ESCD integration and follow-up testing in this thread.

## Released website

- Existing project: smoove-spots-v2 (prj_pctdasKxkRfN8cGYeebyAMrktCNw).
- Source commit: ee34942d3e9f802baf828c4a92f61c53d2f44ada.
- Deployment: dpl_3schbcQSqrRtYgkwULrcBKy4JZPV.
- Stable host: https://smoove-spots-v2-sonlyconsulting-ctrls-projects.vercel.app/
- SS PR: https://github.com/sonlyconsulting-ctrl/ss-website/pull/4
- Previous production deployment for rollback: dpl_7c3WxwaNvVvcneVo7meWHbtiZ6QQ.

## Changes and evidence

AG H07/H08 candidate retained. Repaired Windows-only test root; synchronized entries; added asset packaging checks and Vercel build/test gate; removed continuous decorative marquee animation; pause media on reduced-motion preference changes; enforce video mutex for both manual and automatic playback. Added SS favicon. Located and verified existing Focus & Flow preview rather than describing it as unreleased.

Vercel build and 11 tests passed on the first release (42e9e08). Final Focus & Flow change requires same gate, with its deployment result checked separately. Browser observed rendered desktop hero, navigation to Stories and Experiences, all nine images loaded after scrolling, video playback continuing beyond a 10-second clip, and switching reels pausing the prior reel. Mental Ingenuity, CTJ, TSL and Focus & Flow resolved to their actual applications. TSL has a member access flow; Focus & Flow labels itself an MVP preview. No payment, account, or protected data mutations were performed.

## ESCD integration boundary

This branch changes only SS catalog data and its fallback record, plus this receipt and a new canonical asset record. Main has 9 products while live ESCD source metadata has 10 including newer employment changes. Live API verification is blocked by Vercel authentication; the configured share link was rejected (401). Connected Chrome automation is blocked by an open extension UI. Do not redeploy the old main catalog over the live employment release. Integration is source-prepared, not runtime verified.

The live deployment api/chat.js and api/index.js SHA-1 file hashes match the existing private employment release bundle in ss-website at e16f6c4. The live catalog hash does not match that bundle, so it cannot be treated as an exact release source.

AG's reuse of CANON-160 conflicts with main's existing v7.3 governance authorization record. Preserve CANON-160 and use CANON-167 for this release.

## Remaining verification and routing

- Mobile viewport, zoom and full keyboard/accessibility checks remain partial. No WCAG certification claimed.
- Intended public SC path is https://sonlyconsulting.com/smoove-spots/. Parent site is sonlyconsulting-app on Netlify. No DNS or parent-site deployment change performed.
- Vercel reports smoovespots.com aliases, but their external DNS/HTTPS is not verified. Do not substitute these for the approved path.
- Claude share URL remains the original design workspace; edits in GitHub do not update it.

## Merge and deployment instruction

Apply the SS-only catalog/fallback changes onto the exact current ESCD release, retaining all other product records, icons, employment tools, chat repair and audio. Test Products -> Smoove Spots -> Live App and iframe behavior with authenticated ESCD access before marking runtime synchronization complete.
