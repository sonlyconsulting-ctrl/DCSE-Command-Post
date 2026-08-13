# Tribunal Incident Record: GitHub to Vercel Deployment Storm

**Incident date:** 2026-08-13  
**Lane:** DCSE / SC infrastructure  
**Incident ID:** `TRIB-INC-20260813-GITHUB-VERCEL-001`  
**Status:** CONTAINED / REMEDIATION IN PROGRESS  
**DCS authority:** Cleanup and industry-standard deployment reorganization approved 2026-08-13  
**Production closeout:** NOT YET AUTHORIZED

## Executive finding

GitHub PR #53 did not contain application changes, but its commits triggered deployment activity across five Vercel projects connected to the same `DCSE-Command-Post` repository at repository-root scope.

The incident produced:

- repeated Vercel preview and production deployment email failures;
- unrelated application redeployments;
- failed `consumer-shell` and `dcse-asset-portal` builds;
- a Mental Ingenuity QA production regression during accidental root-repository deployment activity;
- repeated GitHub Actions failure messages from an obsolete malformed one-shot Ollama workflow.

Supabase was not a failing component. Its Git integration correctly ignored PR #53 because the `supabase/` directory did not change.

## Trigger

PR #53:

`Tribunal: record SC digital estate thread topics and AI skills`

Merged commit:

`145a3369987c98bdbf59381223e279797bcd4c79`

The PR contained Tribunal/documentation records and explicitly stated that no production deployment change was intended.

## Vercel projects involved

The PR Vercel integration reported activity for:

1. `consumer-shell`
2. `dcse-asset-portal`
3. `mental-ingenuity-qa`
4. `sc-agent-os`
5. `sc-command-post`

All five were connected to the shared repository with no project-specific source root identified in the PR integration record.

## Failure evidence

### consumer-shell

VERIFIED:

- configured as Next.js;
- Git deployment cloned `DCSE-Command-Post` repository root;
- failed because the expected root Next.js/package structure is absent;
- current repository contains no dedicated `consumer-shell` source root.

Disposition: `DISCONNECT-CANDIDATE` from this repository.

### dcse-asset-portal

VERIFIED:

- configured as Next.js;
- Git deployment cloned repository root;
- failed because the expected Next.js/package structure is absent;
- current repository contains no dedicated `dcse-asset-portal` source root.

Disposition: `DISCONNECT-CANDIDATE` from this repository.

### mental-ingenuity-qa

VERIFIED:

- current repository contains no dedicated Mental Ingenuity source root;
- the current production alias `mental-ingenuity-qa.vercel.app` was fetched on 2026-08-13 after containment and returned `DCSE Secure Access`, not Mental Ingenuity;
- therefore the production regression is still present and must be restored before Git disconnection;
- immutable deployment `dpl_94aDvMG9EhR8GhHeLubEuzY7Mn47` at `mental-ingenuity-ir1r1hfgp-sonlyconsulting-ctrls-projects.vercel.app` was fetched on 2026-08-13 and returned the correct `Mental Ingenuity` application HTML with its expected title and product metadata.

Disposition: `RESTORE PRODUCTION -> VERIFY -> DISCONNECT GIT`.

### sc-agent-os

VERIFIED:

- legitimate application root exists at `apps/sc-agent-os`;
- `apps/sc-agent-os/package.json` exists;
- `apps/sc-agent-os/vercel.json` exists;
- current Vercel Git mapping nevertheless operated at repository-root scope.

Disposition: `KEEP / REWORK GIT MAPPING`.

### sc-command-post

VERIFIED:

- repository root contains `api/index.js`, `api/chat.js`, and root `vercel.json`;
- root `api/index.js` imports `apps/sc-agent-os/api/index.js` and adds SC/DCSE secure-access/authentication behavior;
- Vercel project has historical custom-domain assignments requiring deliberate reconciliation before automatic Git deployment is restored.

Disposition: `HOLD / OWNERSHIP REVIEW`.

## Supabase result

VERIFIED:

Supabase bot comment on PR #53 stated that the pull request was ignored because no changes were detected in the `supabase` directory.

Conclusion:

**Supabase path filtering worked as intended. No Supabase integration repair is required for this incident.**

## GitHub Actions defect

The repository contained:

`.github/workflows/one-shot-fix-ollama-completion.yml`

It was intended as a temporary manual-only one-shot repair, but the repository showed repeated push-triggered workflow failures with zero useful jobs.

A first syntax/trigger repair attempt on the cleanup branch was insufficient and still produced a failed workflow record.

The obsolete one-shot workflow was then removed from the cleanup branch.

Deletion commit:

`481076213132c43515f0fc02cb822704a1f43a93`

Post-deletion verification for that commit returned:

`total_count: 0, workflow_runs: []`

This is evidence that the obsolete workflow no longer generated a GitHub Actions run on that branch commit.

Main is not considered repaired until the cleanup branch is reviewed and merged.

## Temporary containment performed by DCS

DCS manually set Vercel:

`Project Settings -> Build and Deployment -> Ignored Build Step -> Don't build anything`

for all five affected projects.

The setting maps to a skip result and prevents actual Git-triggered builds.

Affected projects now temporarily frozen:

- `consumer-shell`
- `dcse-asset-portal`
- `mental-ingenuity-qa`
- `sc-agent-os`
- `sc-command-post`

## Containment verification

Post-containment branch documentation commits were observed in the affected Vercel projects as `CANCELED` deployment records rather than executed builds.

Verified examples include the incident-record commit and ownership-record commit on:

- `consumer-shell`;
- `dcse-asset-portal`;
- `mental-ingenuity-qa`;
- `sc-agent-os`;
- `sc-command-post`.

Conclusion:

**Temporary build containment is functioning across the five affected projects, but Git integration still creates deployment records. Final remediation requires project/source ownership correction.**

## Cleanup branch

Branch:

`fix/github-vercel-trigger-containment-20260813`

Material branch commits currently include:

- `7028decb06b170b54a768d67688a347acf8ba97b` - transitional Vercel containment script;
- `7cb111134b1c3e33d983fda6b70e738d2a1aecc2` - unsuccessful workflow repair attempt;
- `481076213132c43515f0fc02cb822704a1f43a93` - obsolete one-shot workflow removed;
- later documentation/ownership commits as remediation proceeds.

## Industry-standard remediation target

Every application deployment must have an explicit mapping:

`APPLICATION -> VERCEL PROJECT -> SOURCE REPOSITORY -> ROOT DIRECTORY -> PRODUCTION BRANCH -> DOMAIN -> DATA OWNER -> BUILD TRIGGER -> ROLLBACK -> STATUS`

Required end state:

1. `consumer-shell`, `dcse-asset-portal`, and `mental-ingenuity-qa` do not remain attached to a repository that contains no corresponding source root.
2. `sc-agent-os` maps to `apps/sc-agent-os` and builds only when that application changes.
3. `sc-command-post` remains frozen until its root application and domain ownership are explicitly approved.
4. documentation and Tribunal commits do not redeploy applications.
5. Supabase retains its working path-scoped behavior.
6. obsolete one-shot workflow is absent from main.
7. one documentation-only acceptance commit creates no unintended application builds.
8. one `apps/sc-agent-os` application commit triggers only the intended SC Agent OS deployment.

## Open actions

- [x] Identify five Vercel projects reacting to PR #53.
- [x] Verify Supabase correctly ignored non-Supabase changes.
- [x] Establish temporary Vercel build containment on all five projects.
- [x] Remove obsolete one-shot Ollama workflow on cleanup branch.
- [x] Verify no GitHub Actions run for the post-deletion branch commit.
- [x] Inventory current repository source roots.
- [x] Verify current Mental Ingenuity QA production alias is incorrect and identify a known-good immutable Mental Ingenuity deployment.
- [ ] Restore `mental-ingenuity-qa` production to `dpl_94aDvMG9EhR8GhHeLubEuzY7Mn47` or another independently verified Mental Ingenuity deployment.
- [ ] Verify restored Mental Ingenuity production alias by content, not READY state alone.
- [ ] Disconnect `consumer-shell` from `DCSE-Command-Post` Git integration.
- [ ] Disconnect `dcse-asset-portal` from `DCSE-Command-Post` Git integration.
- [ ] Disconnect `mental-ingenuity-qa` from `DCSE-Command-Post` Git integration after production restoration.
- [ ] Set `sc-agent-os` Root Directory to `apps/sc-agent-os`.
- [ ] Replace SC Agent OS temporary freeze with a validated path-aware ignored-build rule.
- [ ] Reconcile `sc-command-post` product and domain ownership.
- [ ] Run documentation-only acceptance test.
- [ ] Run SC Agent OS targeted-change acceptance test.
- [ ] Review cleanup branch.
- [ ] Merge approved remediation to main.
- [ ] Verify post-merge Vercel, GitHub Actions, Supabase, and public routes.
- [ ] Post/update Windows operational Tribunal receipt.
- [ ] Close Supabase control-plane task with evidence.

## Stop-Gate

Do not unfreeze automatic Git deployment for any affected Vercel project until that project has:

- a verified source root;
- explicit production role;
- explicit domain ownership;
- bounded build trigger;
- rollback path;
- successful acceptance evidence.

## Current disposition

**CONTAINED. REMEDIATION IN PROGRESS. MENTAL INGENUITY PRODUCTION RESTORATION REQUIRED. NOT CLOSED.**
