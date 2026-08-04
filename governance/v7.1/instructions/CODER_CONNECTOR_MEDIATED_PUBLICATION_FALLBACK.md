---
dcse_zone: execution
dcse_subzone: instructions
dcse_authority_level: INSTRUCTION
dcse_document_id: CODER_CONNECTOR_MEDIATED_PUBLICATION_FALLBACK
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: SC
dcse_policy_authority: false
---

# DCSE V7.1 Coder Connector-Mediated Publication Fallback

Status: ACTIVE CONTROLLED USE SUBJECT TO CONTROLLING GOVERNANCE
Authority route: Master Profile, D21, D22, and applicable task authorization
Applies to: Qwen Coder and any sandboxed implementation runtime lacking interactive GitHub authentication

## Purpose

A sandbox that cannot complete OAuth, store credentials, or access an approved SSH identity must not request secrets. In that condition, direct `git push` is optional. Canonical publication may proceed through an authenticated DCSE connector or approved reviewing runtime after provenance verification.

## Trigger

Use this fallback when all are true:

1. The runtime completed the assigned work locally.
2. GitHub write authentication is unavailable in that runtime.
3. No PAT, token, cookie, OAuth code, private key, or service-role credential will be exposed.
4. The local changes can be exported with complete provenance and integrity evidence.

## Required Coder Handoff Package

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

## Publication Path

1. Coder exports the handoff package without credentials.
2. DCS supplies the package to an authenticated GitHub connector, Claude Code with authenticated Git, or another approved publisher.
3. The publisher verifies hashes, base commit, branch, and changed files.
4. The publisher recreates or applies the commits without changing substantive content.
5. The publisher records new canonical GitHub commit SHA values.
6. Runtime records are updated with canonical GitHub SHAs and cross-references.
7. Coder's local-only SHAs remain provenance references, not canonical SHAs.

## Prohibited Actions

- Do not request or paste a PAT in chat.
- Do not embed credentials in a patch, bundle, archive, script, task packet, log, or database row.
- Do not claim a local commit is canonical before remote verification.
- Do not rewrite substantive content during publication without review.
- Do not declare an entire body of work blocked merely because direct push is unavailable.

## Readiness Disposition

A sandbox with no GitHub write path returns `READY_WITH_LIMITATIONS` when it can export a compliant handoff package. It returns `NOT_READY_FIXABLE` when it cannot produce or transfer the package. It returns `STOP_DCS_REQUIRED` for conflicting canonical history, suspected tampering, secret exposure, or an unauthorized destination.

## Instruction Boundary

This fallback defines a bounded publication method for an assigned task. It does not create GitHub authority, change the canonical branch, promote content, or override D22 source reconciliation.