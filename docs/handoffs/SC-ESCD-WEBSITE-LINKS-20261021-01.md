# ESCD brand website links release receipt

Task: SC-ESCD-WEBSITE-LINKS-20261021-01
Handoff: SC-ESCD-WEBSITE-LINKS-HO-20261021-01
Lane: SC / ESCD catalog, SC and SS websites.
Status: PRODUCTION READY / HTTP AND SOURCE VERIFICATION PASSED / FINAL BROWSER VISUAL CHECK BLOCKED.

DCS approved the preview packet, instructed promotion, and requested icons for both websites. This release adds Website links and original brand logos to the existing SC and SS cards. Existing canvas/specification behavior and all ten production product records are preserved. DCS Employment module and task register are unchanged.

## Destinations and original assets
- SC: https://sonlyconsulting.com. Logo from https://sonlyconsulting.com/uploads/assets-1786937403355-edhq.png.
- SS: https://smoove-spots-c2a9eaaf-d58c-450d-a34.vercel.app. Logo from its public bundled manifest asset 640ad1b0-e886-4f14-9c60-174c9cdeabe1. A connected smoovespots.com domain is not verified.
Both originals are preserved intact, displayed with object-fit contain and accessible names. Duplicate product records and iframe website launches were rejected in favor of direct links on existing cards.

## Authority, source and access
Canonical AGENTS.md, Master Profile source and deployment/release standards were read. No controller or governance baseline changed. Source main baseline 9e1b501ea03f58de9bed6dce5f57d619bc8e2fb1; link/logo source commit 2c02daa7c8aa459cd03d1d5ff417821f8053a361. Production was reconstructed from the existing private source snapshot e16f6c4bfe19180f9f4d65346504d81aeb3a8bd2, not wholesale replacement with the older public main runtime. All unchanged source files were verified against their stored Git blobs before use. Forty-eight source files supplied. Database/schema, account, auth configuration, domain and secret changes: none.

## Deployment and verification
Team: sonlyconsulting-ctrls-projects / team_g4aI8rT2IsL2OCR3pYA65141.
Project: sc-escd / prj_TfGqYXFwkLfaZth644kXLn48CMVR.
Preview: dpl_E7NZRiJeWacdxKf8Nsw7QLmywS7i, READY.
Production: dpl_FSLSCJ1FgPbXmA8dmADxJbSXaUPw, READY.
URL: https://sc-escd.vercel.app/escd/app
Rollback: dpl_4azYXmXv9mztsCWaZ9TrXQSccGk8.
The promote endpoint returned 422. A production redeploy of the validated preview source completed; it is not represented as an unchanged build promotion. Production HTML matches the preview and local staged HTML exactly. Both logos return HTTP 200 with correct MIME and byte size. Build logs verify the original three audio files. Deployment-scoped error/fatal log grouping returned no groups in the 10-minute window; this does not establish unexercised API health.
Source/renderer checks pass for API catalog and fallback, destinations, target/rel, accessible link/logo names, image bounds, ten-product preservation and unchanged configuration except the icon route. Detailed artifact hashes: evidence/SC-ESCD-WEBSITE-LINKS-20261021-01.json.

## Browser limitation and handoff
Normal Google sign-in to the immutable preview completed. Chrome subsequently blocked automation because another extension UI was open. Final rendered-card screenshots and live website click-through remain unverified. No account or browser permission settings were changed to circumvent the block.
Standalone review file with both logos: previews/escd-brand-website-links.html.
Source PR: #202. No main merge claimed. No further deployment approval is being requested.
