# ESCD brand website links

Task: SC-ESCD-WEBSITE-LINKS-20261021-01
Handoff: SC-ESCD-WEBSITE-LINKS-HO-20261021-01
Lane: SC / ESCD product catalog, with separate SC and SS destinations.
Purpose/audience: direct brand website launches for ESCD operators.
Authority: DCS confirmed Sonly Consulting and Smoove Spots website links in the current conversation.
Preflight: verified canonical AGENTS.md and Master Profile source; no governance/controller changes. Main baseline 9e1b501ea03f58de9bed6dce5f57d619bc8e2fb1. Existing product entries reused to avoid duplicates. No database, schema, account, entitlement, domain or secret changes.

## Result
Existing SC and SS cards gain a separate Website link, preserving canvas, live-app and specification behavior. Both API catalog copies and built-in fallback carry the same URLs.
- Sonly Consulting: https://sonlyconsulting.com (Netlify sonlyconsulting-app configured primary URL; active ready deploy 6ad6b7cfb4adc6e92d314ca8).
- Smoove Spots: https://smoove-spots-c2a9eaaf-d58c-450d-a34.vercel.app (configured Vercel smoove-spots-v2 alias; production dpl_7c3WxwaNvVvcneVo7meWHbtiZ6QQ READY). No connected smoovespots.com domain verified.
Configured destinations are verified; full destination content and purchase flows were not retested by this task.
Alternatives: duplicate product records rejected because existing records already represent each brand; direct links selected instead of placing websites inside an iframe.

## Validation and preview
Run node tests/escd-brand-website-links.cjs from repository root (test defaults to root relative to its tests directory).
Both catalog copies identical; all inline scripts parse; renderer exercises server catalog and fallback. Each mode produces exactly two Website links with correct destinations, accessible names, target=_blank and rel=noopener noreferrer. Unrelated cards gain no website link. Catalog value comparison confirms only two website_url fields added.
Standalone review: previews/escd-brand-website-links.html (new links only; no authentication or ESCD API required).

## Production reconciliation and release boundary
Current ESCD production: dpl_4azYXmXv9mztsCWaZ9TrXQSccGk8, project prj_TfGqYXFwkLfaZth644kXLn48CMVR, team team_g4aI8rT2IsL2OCR3pYA65141. Canonical https://sc-escd.vercel.app/escd/app.
Production is a validated private source snapshot including a DCS Employment launcher not present on Command Post main. Never deploy this entire main-derived branch over production. Apply only this three-file website-link delta to the exact existing production snapshot, preserving the existing ten product records, UI privacy handling, audio and build configuration.
Locally staged production overlay has exactly three changed files. Both catalog copies: SHA256 0bdaf02f2c5d52e0fbb990348965d292e6e1778ff6f30013cda52db46b247a77. UI: SHA256 659caf548096506a82e0717236fa074f343290b08410b01935227c930ef06b1a. Renderer checks pass against the ten-product overlay too.
No DCS Employment module or its task register modified; only ESCD's brand website links are in scope.

Exit criteria for source work: scoped branch/PR, passing link and preservation checks, standalone review artifact. Complete.
Exit criteria for runtime release: separately authorized production deployment and authenticated ESCD card-link readback. Pending.
Status: SOURCE_READY / PRODUCTION_NOT_UPDATED.
