# Vercel Deployment Storm Containment Record

**Task:** DCSE-VERCEL-CONTAIN-20260908-001  
**Parent:** Issue #59 / Issue #56 closure ledger  
**Classification:** INTERNAL OPERATIONS  
**Status:** CONTAINMENT APPLIED / PROJECT DISCONNECT STILL RECOMMENDED

## Verified current evidence

1. Vercel team: `sonlyconsulting-ctrl's projects`.
2. `sc-agent-os` project ID: `prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM`.
3. `mental-ingenuity-qa` project ID: `prj_3t9SKxOUuW0peitSq97OHWDWCQy9`.
4. Current Vercel project inventory reports `mental-ingenuity-qa` linked to GitHub repository `sonlyconsulting-ctrl/DCSE-Command-Post`.
5. This conflicts with prior repository operations record `docs/operations/VERCEL_PROJECT_OWNERSHIP_20260813.md`, which recorded `mental-ingenuity-qa` as disconnected from `DCSE-Command-Post` after production restoration.
6. DCS received Vercel error `api-deployments-free-per-day` indicating more than 100 deployments in one day.
7. Direct Vercel deployment history proves multiple ordinary `DCSE-Command-Post` commits created production-target `mental-ingenuity-qa` deployments, which were canceled.
8. Recent `sc-agent-os` production-target deployments are also canceled while the account quota is exhausted.

## Root-cause classification

**VERIFIED DRIFT:** `mental-ingenuity-qa` is currently linked to `DCSE-Command-Post` despite the prior disconnected-state record.

**VERIFIED TRIGGER EFFECT:** repository commits are producing `mental-ingenuity-qa` deployment attempts.

## Code-level containment applied

Root `vercel.json` now contains a project-ID-specific `ignoreCommand`:

```json
"ignoreCommand": "[ \"$VERCEL_PROJECT_ID\" = \"prj_3t9SKxOUuW0peitSq97OHWDWCQy9\" ]"
```

Vercel's ignored-build convention treats exit code `0` as ignore and exit code `1` as continue. Therefore this check ignores builds only when the executing Vercel project is `mental-ingenuity-qa`; other root-backed Vercel projects continue to their existing behavior. Commit: `56458af72a26ed3ba39c37aad25c1b1fd59dadd8`.

This is a bounded containment control and does not claim the incorrect Git linkage itself has been removed.

## Containment rule effective immediately

- Do not generate manual/retry Vercel deployments while the daily deployment quota is exhausted.
- Do not buy capacity as a substitute for correcting unintended build triggers.
- Preserve last-known-good production deployments and rollback references.
- `sc-agent-os` acceptance remains a single bounded deployment only after quota reset and trigger behavior is rechecked.

## Required project-setting correction

For `mental-ingenuity-qa`, disconnect the `DCSE-Command-Post` Git link unless a verified dedicated source root is established. For every other Vercel project currently linked to `DCSE-Command-Post`, reconcile:

`PROJECT -> SOURCE ROOT -> PRODUCTION BRANCH -> BUILD TRIGGER -> DOMAIN -> ROLLBACK`

Projects without a verified source root must not receive automatic deployments from repository commits.

## Tool boundary

The current Vercel connector exposes project/deployment reads and deployment execution but does not expose project-settings mutation or Git-disconnect. The repository-level containment control is therefore applied now; the underlying Vercel Git-link correction remains a settings-write action on a surface not exposed in this chat.
