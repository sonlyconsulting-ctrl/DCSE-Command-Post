# DCSE V7.1 Vercel Deployment Budget Policy

Status: Adopted for PR #47 remediation and subsequent DCSE Vercel-backed workflows.

## Principle

Git commit cadence and deployment cadence are separate concerns. A repository change MUST NOT consume a Vercel preview deployment unless the change can affect the deployed application surface or a deployment configuration that must be revalidated.

## Required behavior

1. Deployable-surface changes trigger a preview build. Examples include application/API code, public/static assets, Vercel configuration, and package/build metadata used by the deployed project.
2. Non-deployable-only changes are ignored by Vercel preview builds. Examples include governance/docs, Tribunal receipts, Windows controller/worker scripts, local runtime evidence, and unrelated repository documentation.
3. Mixed commits containing at least one deployable-surface change MUST build. Ignore logic must never suppress a build merely because the same commit also contains non-deployable files.
4. Related remediation changes SHOULD be batched to a coherent validation point instead of producing a deployment for every small commit.
5. A READY preview may be reused for multiple bounded validation checks when the deployed source has not changed.
6. A new preview is required after a change to a deployable surface that affects the behavior under validation.
7. Production promotion remains separate from preview generation and follows normal DCSE promotion/independent-validation gates.
8. Deployment quota exhaustion is an infrastructure constraint, not a code-failure signal. CI/status reporting must distinguish quota/rate-limit failures from build/test failures.

## SC Agent OS enforcement

`apps/sc-agent-os/vercel.json` defines an `ignoreCommand`. Vercel ignores a build when the command exits `0` and continues a build when it exits `1`.

The command is intentionally written as an explicit conditional: if any deployable SC Agent OS path changed, return `1` so Vercel builds; otherwise return `0` so the deployment is skipped.

Deployable paths currently include:

- `api/`
- `apps/sc-agent-os/api/`
- `public/` and `apps/sc-agent-os/public/`
- `vercel.json` / `apps/sc-agent-os/vercel.json`
- package/build manifests covered by `package.json` / `package-lock.json`

This avoids the unsafe inverse-match pattern `grep -qvE`, which can incorrectly skip a mixed commit containing both deployable and non-deployable files.

## Branch policy

Branch-wide preview suppression (for example, disabling all `chatgpt/*` previews) is not the default policy because it would also suppress legitimate UI/API validation on those branches. Path-aware ignored builds are the preferred control. Branch suppression may be added later as a project-specific cost-control measure when an explicit preview allowlist is desired.

## Preview lineage rule

A preview URL is valid evidence only for the exact source branch/commit that produced it. Older branch previews may remain useful for regression comparison, but they MUST NOT be cited as validation of fixes that exist only on another branch or a later commit.

For the 2026-08-07 incident, the older `claud-f0e056` preview predates both the PR #48 Dispatch fix branch (`claude/dispatch-fix-agent-file-assignment-20260807`) and the later login-removal work. It is therefore a clean regression reference only, not evidence for either fix.
