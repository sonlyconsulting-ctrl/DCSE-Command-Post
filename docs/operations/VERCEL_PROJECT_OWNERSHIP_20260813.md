# Vercel Project Ownership and Source-Root Reconciliation

**Record date:** 2026-08-13  
**Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Branch:** `fix/github-vercel-trigger-containment-20260813`  
**Status:** CANDIDATE OPERATIONS RECORD  
**Production authority:** NONE BY THIS DOCUMENT

## Finding

The repository was connected at repository-root scope to five Vercel projects. Ordinary documentation and Tribunal commits therefore created unrelated Vercel deployment activity.

Repository inspection establishes that only two of those five projects have a plausible source relationship to the current repository:

- `sc-agent-os` has a verified application root at `apps/sc-agent-os`.
- `sc-command-post` has a root deployment wrapper at `api/` plus root `vercel.json`, but its intended production/domain role still requires reconciliation.

No source root named or dedicated to `consumer-shell`, `dcse-asset-portal`, or `mental-ingenuity-qa` exists in the current repository tree.

## Temporary containment applied by DCS

DCS set Vercel `Ignored Build Step` to `Don't build anything` for:

- `consumer-shell`
- `dcse-asset-portal`
- `mental-ingenuity-qa`
- `sc-agent-os`
- `sc-command-post`

This prevents actual Git-triggered builds while the project/source mapping is repaired. Vercel can still create a canceled deployment record for a Git push, so this is containment, not the final architecture.

## Current project map

| Vercel project | Project ID | Current source relationship | Current disposition | Target action |
|---|---|---|---|---|
| `sc-agent-os` | `prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM` | VERIFIED: `apps/sc-agent-os` | KEEP / REWORK GIT MAPPING | Set Root Directory to `apps/sc-agent-os`, then use path-aware build skipping |
| `sc-command-post` | `prj_a9pbcrfvQczbmH2Cr1S2Q08p2975` | VERIFIED code at repository root, exact business role/domain ownership not yet reconciled | HOLD | Keep frozen until domain and product role are verified; then use a bounded root-path trigger or separate app root |
| `consumer-shell` | `prj_xVHcFD74DWyVD0QtizARSGIRSP2T` | VERIFIED: no dedicated source root in current repository | DISCONNECT-CANDIDATE | Disconnect this Git repository unless source is intentionally restored/migrated later |
| `dcse-asset-portal` | `prj_WJLnWl2RrdUcELBZHwPI6Qw8ZIZ9` | VERIFIED: no dedicated source root in current repository | DISCONNECT-CANDIDATE | Disconnect this Git repository unless source is intentionally restored/migrated later |
| `mental-ingenuity-qa` | `prj_3t9SKxOUuW0peitSq97OHWDWCQy9` | VERIFIED: no dedicated source root in current repository | DISCONNECT-CANDIDATE | Verify production Mental Ingenuity deployment, then disconnect this Git repository |
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

`APPLICATION -> VERCEL PROJECT -> SOURCE REPOSITORY -> ROOT DIRECTORY -> PRODUCTION BRANCH -> DOMAIN -> DATA OWNER -> BUILD TRIGGER -> ROLLBACK -> STATUS`

Required principles:

1. One Vercel project must map to one intentional application source root.
2. Documentation-only changes must not build unrelated applications.
3. A Git integration must not remain attached to a project with no matching source root.
4. Production domains must be explicitly owned and must not be inferred from historical Vercel configuration.
5. A project with a shared repository must use either:
   - a correct Root Directory plus path-aware Ignored Build Step; or
   - a purpose-built monorepo affected-project mechanism when the repository actually uses a compatible monorepo tool.
6. Do not introduce Turborepo merely to solve this incident. The current repository has no root package workspace/turbo configuration.
7. Supabase preview integration remains path-scoped to `supabase/` and should not be changed merely because Vercel was misconfigured.
8. GitHub Actions must contain only intentional workflows with valid triggers.

## Proposed `sc-agent-os` final Git behavior

After its Vercel Root Directory is set to `apps/sc-agent-os`, replace the temporary `Don't build anything` rule with a path-aware rule that skips builds when that application root is unchanged.

A simple Git-diff based Ignored Build Step is preferred over adding a monorepo framework solely for this purpose.

Exact command must be validated in the Vercel project context before production activation.

## Proposed `sc-command-post` hold

Do not unfreeze `sc-command-post` yet.

The repository-root wrapper currently imports `apps/sc-agent-os/api/index.js` and implements SC/DCSE secure access/authentication. The Vercel project also carries historical custom-domain assignments. That combination requires a deliberate product/domain ownership decision before automatic Git deployment is restored.

## Acceptance test for final repair

Use one documentation-only commit after all Vercel project mappings are corrected.

Expected behavior:

- `consumer-shell`: no Git deployment because repository is disconnected.
- `dcse-asset-portal`: no Git deployment because repository is disconnected.
- `mental-ingenuity-qa`: no Git deployment because repository is disconnected.
- `sc-agent-os`: no build when `apps/sc-agent-os` is unchanged.
- `sc-command-post`: no build for unrelated documentation until its bounded trigger is approved.
- Supabase: ignore when `supabase/` is unchanged.
- GitHub Actions: no obsolete one-shot Ollama workflow failure.

A second test should modify only `apps/sc-agent-os` and prove that only the intended SC Agent OS deployment executes.

## Rollback

Until final acceptance, retain the Vercel `Don't build anything` setting on the five affected projects. If a mapping change produces unexpected deployment activity, restore that setting immediately and do not continue to the next project.
