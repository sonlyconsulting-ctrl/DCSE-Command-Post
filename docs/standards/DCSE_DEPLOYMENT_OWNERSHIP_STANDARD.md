# DCSE Deployment Ownership and Trigger Boundary Standard

**Standard ID:** `DCSE-DEPLOY-OWN-001`  
**Version:** 1.0 Candidate  
**Date:** 2026-08-13  
**Status:** CANDIDATE FOR DCS REVIEW  
**Scope:** GitHub-connected application deployment surfaces including Vercel and comparable hosts

## Purpose

Prevent unrelated repository activity from rebuilding, overwriting, or redeploying applications that do not own the changed source.

## Required deployment identity

Every deployed application must have a maintained record containing:

`APPLICATION -> HOST PROJECT -> SOURCE REPOSITORY -> ROOT DIRECTORY -> PRODUCTION BRANCH -> ENVIRONMENT -> DOMAIN -> DATA OWNER -> BUILD TRIGGER -> ROLLBACK -> OWNER -> STATUS`

No production deployment connection is complete until these fields are known or explicitly marked `UNKNOWN / HOLD`.

## Source ownership

Each host project must map to one intentional application source root.

A host project shall not remain Git-connected to a repository when:

- the repository contains no corresponding application source;
- the source root is unknown;
- the project is legacy/orphaned and has no current owner;
- the Git connection causes unrelated commits to trigger deployment activity.

Required behavior:

- disconnect stale or incorrect Git integrations;
- restore a Git integration only after source ownership is established.

## Monorepo and shared-repository rule

When multiple applications share one repository:

1. Each application receives a distinct root directory or explicit source boundary.
2. The host project must be configured to build only when that boundary or an approved shared dependency changes.
3. Documentation, Tribunal, governance, unrelated application, and unrelated database changes must not build the application unless a verified dependency requires it.
4. Do not introduce a monorepo framework merely to obtain change detection when a simpler bounded Git-diff rule is sufficient.
5. If a formal monorepo tool is later adopted, its affected-project graph becomes a governed dependency and requires tests.

## Git-trigger rule

Automatic Git deployment is permitted only when:

- source root is VERIFIED;
- production branch is VERIFIED;
- environment is VERIFIED;
- domain ownership is VERIFIED or not applicable;
- build command/framework is correct for that root;
- ignored-build/affected-project behavior has been tested;
- rollback is available.

Otherwise automatic deployment remains disabled or ignored.

## Documentation-only acceptance test

Before restoring automatic deployment for a shared repository, create one non-application documentation-only commit.

PASS requires:

- unrelated applications do not build;
- unrelated production aliases do not change;
- unrelated database previews do not execute;
- only intended repository validation workflows run.

A canceled/skipped record may be acceptable during migration, but the preferred steady state is no deployment record for projects that are not connected to the repository.

## Targeted application acceptance test

After the documentation-only test passes, create one bounded change under a single application source root.

PASS requires:

- the intended application builds;
- unrelated applications do not build;
- deployment maps to the expected branch/root;
- application smoke test passes;
- production promotion follows the applicable release gate;
- evidence is recorded.

## Database integration boundary

Database preview or migration integrations must be path-scoped to the database/migration source boundary where supported.

A website documentation change must not cause a database preview branch or migration unless database source changed or the task explicitly requires it.

## Domain ownership

Custom domains must be explicitly mapped to their intended product/application.

Do not infer domain ownership from an old host-project attachment.

Before moving, removing, or repointing a domain:

- verify current public destination;
- verify DNS/host ownership;
- identify rollback target;
- record DCS approval when the change is material.

## QA and rollback

Every production-capable host project must identify:

- last known good deployment;
- rollback mechanism;
- smoke-test URL or route;
- owner;
- status.

A deployment marked `READY` is not sufficient evidence of application correctness.

## Evidence requirements

Material deployment changes should produce:

- task/external ID;
- source branch/commit;
- host project ID;
- root directory;
- build/skip evidence;
- deployment ID when built;
- domain verification when applicable;
- smoke-test evidence;
- rollback reference;
- Tribunal receipt;
- Supabase/control-plane reconciliation when applicable.

## Failure response

If an unrelated commit triggers an unexpected deployment:

1. contain automatic builds;
2. preserve the last known good deployment;
3. identify affected projects;
4. inspect repository/source mapping;
5. repair project ownership and trigger boundaries;
6. test with documentation-only and targeted changes;
7. close only after evidence reconciliation.

## Validation

This standard is satisfied only when the deployment estate can answer, without inference:

- What is this project?
- Where is its source?
- What changes are allowed to build it?
- What domain does it own?
- What data system does it depend on?
- Who owns the decision?
- How is it rolled back?
- What evidence proves the deployed application is the intended one?
