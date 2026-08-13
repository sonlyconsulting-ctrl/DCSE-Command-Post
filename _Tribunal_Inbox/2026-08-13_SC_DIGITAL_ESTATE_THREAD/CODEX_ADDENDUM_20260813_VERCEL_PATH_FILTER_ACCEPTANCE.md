# Codex Addendum: Vercel Path Filter Acceptance

**Task:** `SC-AGENT-OS-SECURE-ROOT-20260813`
**Status:** BINDING ADDENDUM / NO PRODUCTION PROMOTION

The controlled acceptance test established that setting `Root Directory = apps/sc-agent-os` alone did not prevent a repository documentation-only commit from creating an SC Agent OS deployment when Ignored Build Step was `Automatic`.

Therefore the release candidate must not rely on an unverified assumption that Vercel root-aware skipping is sufficient for this repository.

Codex shall inspect whether `DCSE-Command-Post` satisfies Vercel monorepo/workspace requirements for automatic unaffected-project skipping. If it does not, propose the smallest explicit path-aware trigger boundary for SC Agent OS, preferably an Ignored Build Step/folder rule or repository-level workspace normalization that builds only for changes affecting the canonical SC Agent OS root/dependencies.

Acceptance requires both:

1. an SC Agent OS source change triggers the intended preview build; and
2. a Tribunal/docs-only change does not execute an SC Agent OS build.

Do not weaken authentication, do not promote production, and do not unfreeze `sc-command-post`.
