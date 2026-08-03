# DCSE V7.1 Coder Connector-Mediated Publication Fallback

Status: ACTIVE CONTROLLED USE
Authority: DCS Level 0 conditional authorization
Applies to: Qwen Coder and any sandboxed implementation runtime lacking interactive GitHub authentication

## Purpose

A sandbox that cannot complete OAuth, store credentials, or access an approved SSH identity must not request secrets and must not hold enterprise publication hostage. In that condition, direct `git push` is optional. Canonical publication shall proceed through an authenticated DCSE connector or approved reviewing runtime.

## Trigger

Use this fallback when all are true:

1. The runtime has completed the assigned work locally.
2. GitHub write authentication is unavailable in that runtime.
3. No PAT, token, cookie, OAuth code, private key, or service-role credential will be exposed.
4. The local changes can be exported with complete provenance and integrity evidence.

## Required Coder handoff package

Coder shall produce one of the following, in priority order:

1. `git format-patch` files for the unpublished commit range;
2. a `git bundle` containing the unpublished commits;
3. a ZIP or TAR archive containing the complete changed files plus a manifest;
4. full UTF-8 file contents in separate artifacts when the earlier formats are unavailable.

The package must include:

- repository full name;
- source branch;
- local base commit SHA;
- full 40-character unpublished commit SHAs;
- ordered commit messages;
- changed-file list per commit;
- SHA-256 for every exported artifact;
- `git status --short` output;
- `git diff --stat <remote-head>..HEAD` output;
- declaration of whether uncommitted changes exist;
- expected destination branch;
- requested publication disposition.

## Publication path

1. Coder exports the handoff package without credentials.
2. DCS supplies the package to ChatGPT GitHub connector, Claude Code with authenticated Git, or another approved publisher.
3. Publisher verifies hashes, base commit, branch, and changed files.
4. Publisher recreates or applies the commits without changing substantive content.
5. Publisher records new canonical GitHub commit SHA values.
6. Supabase records are updated with canonical GitHub SHAs and cross-references.
7. Coder's local-only SHAs remain provenance references, not canonical SHAs.

## Prohibited actions

- Do not request or paste a PAT in chat.
- Do not embed credentials in a patch, bundle, archive, script, task packet, log, or Supabase row.
- Do not claim a local commit is canonical before remote verification.
- Do not rewrite substantive content during publication without returning it for review.
- Do not declare an entire body of work blocked because direct push is unavailable.

## First-assignment behavior

A sandbox with no GitHub write path must return `READY_WITH_LIMITATIONS` when it can export a compliant handoff package. It returns `NOT_READY_FIXABLE` only when it cannot produce or transfer the package. It returns `STOP_DCS_REQUIRED` only for conflicting canonical history, suspected tampering, secret exposure, or an unauthorized destination.

## Immediate application

For the V7.1 Foundational Trilogy local commit range ending at `4408e5bfc9e73c0cb69ea531950d318c3448a6dc`, Coder shall export the unpublished range from remote head `88fdc9e` through local HEAD as `git format-patch` or `git bundle`, compute SHA-256, and return the package for authenticated connector publication.
