# Vercel Project Ownership and Source-Root Reconciliation

**Record date:** 2026-08-13  
**Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Branch:** `fix/github-vercel-trigger-containment-20260813`  
**Status:** CANDIDATE OPERATIONS RECORD / REMEDIATION IN PROGRESS  
**Production authority:** NONE BY THIS DOCUMENT

## Finding

The repository was connected at repository-root scope to five Vercel projects. Ordinary documentation and Tribunal commits therefore created unrelated Vercel deployment activity.

Repository inspection establishes that only two of those five projects have a plausible source relationship to the current repository:

- `sc-agent-os` has a verified application root at `apps/sc-agent-os`.
- `sc-command-post` has a root deployment wrapper at `api/` plus root `vercel.json`, but its intended production/domain role still requires reconciliation.

No source root named or dedicated to `consumer-shell`, `dcse-asset-portal`, or `mental-ingenuity-qa` exists in the current repository tree.

## Incident containment and completed remediation

DCS first set Vercel `Ignored Build Step` to `Don't build anything` for the five affected projects to stop active Git-triggered builds while ownership was investigated.

The following remediation is now complete:

- `consumer-shell` Git connection to `DCSE-Command-Post`: **DISCONNECTED**.
- `dcse-asset-portal` Git connection to `DCSE-Command-Post`: **DISCONNECTED**.
- `mental-ingenuity-qa`: prior known-good Mental Ingenuity deployment promoted back to production and production alias independently verified to return the Mental Ingenuity application; Git connection to `DCSE-Command-Post`: **DISCONNECTED**.
- `sc-agent-os` Root Directory: **SET TO `apps/sc-agent-os`**.
- `sc-agent-os` Vercel root-aware option **Skip deployments when there are no changes to the root directory or its dependencies**: **ENABLED**.
- `sc-agent-os` temporary `Don't build anything` freeze: **REMAINS ENABLED PENDING ACCEPTANCE TEST**.
- `sc-command-post`: **REMAINS FROZEN / OWNERSHIP REVIEW REQUIRED**.
- obsolete repository script `scripts/vercel-git-ignore.sh`: **REMOVED** after source remapping made the shared-project freeze script unnecessary.

## Current project map

| Vercel project | Project ID | Source relationship | Current state | Next action |
|---|---|---|---|---|
| `sc-agent-os` | `prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM` | VERIFIED: `apps/sc-agent-os` | ROOT MAPPED / FROZEN | Run documentation-only acceptance test, then remove temporary freeze and validate targeted app change |
| `sc-command-post` | `prj_a9pbcrfvQczbmH2Cr1S2Q08p2975` | VERIFIED root wrapper at `api/`; exact product/domain ownership not yet reconciled | HOLD / FROZEN | Reconcile application role, custom domains, auth wrapper, source boundary, and rollback before re-enabling Git deployment |
| `consumer-shell` | `prj_xVHcFD74DWyVD0QtizARSGIRSP2T` | VERIFIED: no dedicated source root in current repository | DISCONNECTED | Inventory separately; reconnect only if source is intentionally restored/migrated later |
| `dcse-asset-portal` | `prj_WJLnWl2RrdUcELBZHwPI6Qw8ZIZ9` | VERIFIED: no dedicated source root in current repository | DISCONNECTED | Inventory separately; reconnect only if source is intentionally restored/migrated later |
| `mental-ingenuity-qa` | `prj_3t9SKxOUuW0peitSq97OHWDWCQy9` | VERIFIED: no dedicated source root in current repository | PRODUCTION RESTORED / DISCONNECTED | Preserve current known-good deployment; reconnect only to the actual Mental Ingenuity source repository/path when established |
| `dist` | `prj_QwjI6vtxDjkRoAXs0QHEBtblDMAf` | UNKNOWN | INVENTORY | Leave unchanged pending estate classification |
| `magical-learning-gift-review` | `prj_k1YwaMS7tHM06hVxB3vXOacs2tPT` | UNKNOWN / review asset | INVENTORY | Leave unchanged pending classification |
| `vow-and-go-review` | `prj_6mpgeMIZlmYSLZzNf2fRbv6ChhwZ` | LIKELY family-product review asset | INVENTORY | Leave unchanged pending classification |
| `dcse-wix-bridge` | `prj_KqoZpMU4NXG4z02ZvDybnsH0jKYL` | UNKNOWN | INVENTORY | Leave unchanged pending classification |
| `project-zmdcv` | `prj_8HIqLDzxubvVk5IDlOoFOvBwln1y` | UNKNOWN, no current deployment | ARCHIVE/REMOVE-CANDIDATE | Determine ownership before removal |
| `web` | `prj_3igUPxAHPwxFOiY5cvTOb7aqPZkf` | UNKNOWN, old ERROR deployment | ARCHIVE/REWORK-CANDIDATE | Determine ownership before removal |
| `retrograde-whirlpool` | `prj_iSBkssXcXMJyEY0Lhslo7YLitLVV` | UNKNOWN, old ERROR deployment | ARCHIVE/REMOVE-CANDIDATE | Determine ownership before removal |

## Repository evidence

The current cleanup branch tree contains:

- `apps/sc-agent-os/package.json`
- `apps/sc-agent-os/vercel.json`
- `apps/sc-agent-os/api/index.js`
- root `api/index.js`
- root `api/chat.js`
- root `vercel.json`

The branch tree contains no dedicated path for:

- `consumer-shell`
- `dcse-asset-portal`
- `mental-ingenuity-qa`

The repository contains only one `package.json`, at `apps/sc-agent-os/package.json`.

## Industry-standard target pattern

Every deployed application should have an explicit ownership record:

`APPLICATION -> HOST PROJECT -> SOURCE REPOSITORY -> ROOT DIRECTORY -> PRODUCTION BRANCH -> ENVIRONMENT -> DOMAIN -> DATA OWNER -> BUILD TRIGGER -> ROLLBACK -> OWNER -> STATUS`

Required principles:

1. One host project maps to one intentional application source root.
2. Documentation-only changes do not build unrelated applications.
3. A Git integration does not remain attached to a project with no matching source root.
4. Production domains are explicitly owned and are not inferred from historical host configuration.
5. Shared-repository applications use a verified Root Directory plus affected-project/root-aware deployment behavior where supported.
6. Do not introduce a monorepo framework merely to solve change detection when native host root-awareness is sufficient.
7. Supabase preview integration remains path-scoped to `supabase/` and should not be changed merely because Vercel was misconfigured.
8. GitHub Actions contains only intentional workflows with valid triggers.

## `sc-agent-os` final Git behavior

Current Vercel configuration now establishes:

- Root Directory: `apps/sc-agent-os`
- include files outside root directory in Build Step: enabled
- skip deployments when no changes to root directory or dependencies: enabled
- temporary `Don't build anything`: still enabled

The preferred steady state is to rely on Vercel's root-aware change detection rather than a custom repository-wide ignore script, provided acceptance testing proves the behavior.

## `sc-command-post` hold

Do not unfreeze `sc-command-post` yet.

The repository-root wrapper currently imports `apps/sc-agent-os/api/index.js` and implements SC/DCSE secure access/authentication. The Vercel project also carries historical custom-domain assignments. That combination requires a deliberate product/domain ownership decision before automatic Git deployment is restored.

## Acceptance test for final repair

### Test 1: documentation-only commit

Expected behavior:

- `consumer-shell`: no Git deployment because repository is disconnected.
- `dcse-asset-portal`: no Git deployment because repository is disconnected.
- `mental-ingenuity-qa`: no Git deployment because repository is disconnected.
- `sc-agent-os`: no application build when `apps/sc-agent-os` and its dependencies are unchanged.
- `sc-command-post`: no active build because the project remains frozen.
- Supabase: ignore when `supabase/` is unchanged.
- GitHub Actions: no obsolete one-shot Ollama workflow failure.

### Test 2: targeted `sc-agent-os` change

After Test 1 passes and DCS removes the temporary `Don't build anything` setting only for `sc-agent-os`, make one bounded change under `apps/sc-agent-os`.

PASS requires:

- only the intended SC Agent OS deployment executes;
- unrelated disconnected Vercel projects remain silent;
- `sc-command-post` remains frozen;
- build and smoke test pass;
- expected domain/preview behavior is preserved;
- evidence is recorded.

## Rollback

Until final acceptance, retain the temporary `Don't build anything` setting on `sc-agent-os` and `sc-command-post`.

If `sc-agent-os` produces unexpected deployment activity after unfreezing, immediately restore `Don't build anything`, preserve the last known good deployment, and stop the acceptance sequence.
