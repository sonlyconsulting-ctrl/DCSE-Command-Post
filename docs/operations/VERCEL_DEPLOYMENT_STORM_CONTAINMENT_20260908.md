# Vercel Deployment Storm Containment Record

**Task:** DCSE-VERCEL-CONTAIN-20260908-001  
**Parent:** Issue #59 / Issue #56 closure ledger  
**Classification:** INTERNAL OPERATIONS  
**Status:** PARTIAL, external project-setting mutation still required

## Verified current evidence

1. Vercel team: `sonlyconsulting-ctrl's projects`.
2. `sc-agent-os` project ID: `prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM`.
3. `mental-ingenuity-qa` project ID: `prj_3t9SKxOUuW0peitSq97OHWDWCQy9`.
4. Current Vercel project inventory reports `mental-ingenuity-qa` linked to GitHub repository `sonlyconsulting-ctrl/DCSE-Command-Post`.
5. This conflicts with prior repository operations record `docs/operations/VERCEL_PROJECT_OWNERSHIP_20260813.md`, which recorded `mental-ingenuity-qa` as disconnected from `DCSE-Command-Post` after production restoration.
6. DCS received Vercel error `api-deployments-free-per-day` indicating more than 100 deployments in one day. The latest observed `mental-ingenuity-qa` production-target deployment is CANCELED.
7. Recent `sc-agent-os` production-target deployments are also CANCELED.

## Root-cause classification

**VERIFIED DRIFT:** at least `mental-ingenuity-qa` is currently linked to `DCSE-Command-Post` despite the prior disconnected-state record.

**LIKELY CONTRIBUTION:** repository commits can therefore trigger unintended project deployments and consume free-plan deployment quota. Exact trigger settings still require project-setting inspection/mutation.

## Containment rule effective immediately

- Do not generate new Vercel deployments while the account daily deployment quota is exhausted.
- Do not buy capacity as a substitute for correcting unintended build triggers.
- Do not reconnect or retain Git links for projects with no verified matching source root.
- Preserve last-known-good production deployments and rollback references.
- `sc-agent-os` acceptance remains a single bounded deployment only after trigger containment and quota reset.

## Required project-setting correction

For `mental-ingenuity-qa`, disconnect the `DCSE-Command-Post` Git link unless a verified dedicated source root is established. For every other Vercel project currently linked to `DCSE-Command-Post`, reconcile:

`PROJECT -> SOURCE ROOT -> PRODUCTION BRANCH -> BUILD TRIGGER -> DOMAIN -> ROLLBACK`

Projects without a verified source root must not receive automatic deployments from repository commits.

## Tool boundary

The current Vercel connector exposes project/deployment read operations and deployment execution but does not expose a project-settings mutation or Git-disconnect operation. Therefore the drift is verified and the required correction is exact, but the disconnect itself cannot be executed from this chat connector without a supported Vercel settings-write surface.

This is an access/tool boundary, not an application ambiguity. No repeated deployment retry is authorized.
