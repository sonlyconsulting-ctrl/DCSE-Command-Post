# DCSE GitHub Agent and Platform Doctrine v1

**Document ID:** DCSE-V72-GITHUB-PLATFORM-DOCTRINE-v1  
**Status:** OPERATIVE upon Level 0 promotion  
**Authority:** DCS Level 0  
**Parent:** DCSE Master Profile v7.2 R5  
**Controlling numbered doctrines:** D22, D05, D04, D21, D03  
**Scope:** GitHub repositories, branches, commits, pull requests, Actions, Releases, Issues, repository files, Git LFS references, and agent/reviewer operations.

## 1. Purpose

GitHub is DCSE's canonical versioned source and governed-artifact repository when D22 routes an artifact to Git. GitHub does not independently create constitutional authority, lifecycle promotion, production truth, or completion.

## 2. Required identity

Every governed GitHub action SHALL resolve:

- repository full name;
- owner/entity/lane;
- authority branch;
- starting commit;
- task ID;
- intended path(s);
- actor/access method;
- required checks/review;
- promotion authority;
- rollback/revert target;
- evidence destination.

## 3. Repository roles

GitHub MAY canonically store:

- doctrine and governance artifacts;
- source code and configuration;
- migrations and schemas;
- project/task manifests;
- machine-readable control matrices;
- scripts, templates, prompts, transcripts, captions, shot lists, and text-based media project artifacts;
- small binary assets when repository health permits;
- Git LFS pointer records where LFS is deliberately governed.

GitHub SHALL NOT be the default home for secrets, runtime database state, privileged credentials, or large/frequently changing media binaries when D22 routes those to another system.

## 4. Branch/PR lifecycle

Material changes follow:

`VERIFY REPO -> VERIFY MAIN/BASE -> TASK BRANCH -> CHANGE -> LOCAL/STATIC VALIDATION -> PR -> EXACT-HEAD CI -> REVIEW/RECONCILE -> MERGE -> MAIN READBACK -> REGISTRY/TRIBUNAL RECEIPT`

Direct-to-main writes require a separately approved procedure.

## 5. Authority and promotion

A commit, PR approval, merge, tag, release, or workflow success is evidence, not Level 0 authority by itself.

Promotion evidence SHALL bind:

- exact artifact/path;
- exact commit;
- required content hash where material;
- validation result;
- approving authority;
- registry reconciliation where required;
- Tribunal/receipt reference.

## 6. Agent boundaries

Authorized agents may inspect, branch, edit, test, prepare PRs, review diffs, and reconcile evidence within task scope. Repository access never implies permission to:

- rewrite protected history;
- delete repositories or protected branches;
- expose secrets;
- bypass required checks;
- self-promote governance;
- merge production/release-impacting changes outside delegated authority;
- cross lanes or repositories without task authorization.

## 7. Issues and work control

Issues are work/evidence coordination surfaces, not authority. Close completed items, consolidate overlap without losing acceptance criteria, preserve history, and distinguish blockers from backlog.

## 8. Actions and CI

CI SHOULD enforce machine-testable invariants. A green workflow proves only the checks it actually performed. Workflow definitions, permissions, action versions, secrets, branch triggers, and path filters are governed code.

Repeated CI/deployment fan-out caused by unrelated monorepo changes is a defect to be corrected, not a reason to normalize retry storms.

## 9. Binary/media rule

Ordinary Git is not the default warehouse for large production media. Product repositories SHALL use the DCSE Media Asset Manifest to reference canonical binary storage, hashes, rights, and access class. Small assets or deliberate Git LFS objects are permitted when the project manifest explicitly selects that route.

## 10. Project bootstrap

Every governed product repository SHOULD expose `DCSE_PROJECT_MANIFEST.yaml` at root. Product/media builds SHOULD expose `assets/DCSE_MEDIA_ASSET_MANIFEST.json`.

Missing required bootstrap artifacts trigger the Product Start Gate and may escalate to DCS-E.

## 11. Completion

GitHub work is COMPLETE only when requested outcomes, exact-head validation, merge/readback, dependent registry state, and evidence reconcile. An unmerged branch or unverified dependent state is PARTIAL.

## Related controls

- D22 Source Authority and Runtime Distribution
- D05 Baseline and Promotion
- D04 Command Post Communications
- D21 Doctrine Runtime Engine
- Universal Agent Onboarding and Access
- DCSE Platform Execution Profiles
- DCSE Cross-System Reconciliation Contract
