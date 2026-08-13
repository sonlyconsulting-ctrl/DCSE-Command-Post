# Tribunal Topic Record: SC Wix CLI, Velo, Git Integration, and Engineering Model

**Record date:** 2026-08-13  
**Lane:** SC / DCSE  
**Status:** PREIMPLEMENTATION ENGINEERING DISCUSSION  
**Implementation authority:** NONE

## Finding

Wix CLI/Velo can perform a large share of engineering work for the current Sonly Consulting site, but it is not a complete substitute for the visual Wix Editor.

The target site uses the regular/classic Wix Editor with Velo enabled. DCS has a Classic Editor Core account and does not currently intend to purchase Wix Studio.

## Working completeness estimate

These percentages are planning estimates, not Wix-published metrics.

- Velo frontend/page code: 95-100%
- Backend Velo/Web Modules: 95-100%
- Wix Data/CMS logic: 90-100%
- Wix API integrations: 90-100%
- npm/package integration: 90-100%
- forms/business logic/custom workflows: 85-100%
- custom elements/interactive components: 90-100%
- automated testing/version control: 90-100%
- page visual composition/layout: approximately 50-80%
- overall full Wix site, including visual polish: approximately 75-90%

The main limitation is visual composition. Code can be engineered in local IDE/CLI workflows, while Wix Editor/Local Editor remains important for layout and visual QA.

## Git Integration implication

Wix Git Integration can connect the site to GitHub and support local IDE/CLI development for Velo code.

Important consequence: after Git Integration, normal Wix code-editing behavior changes and source-code authority moves toward the Git/local development workflow.

Therefore production SC.com should not be connected to Git merely as an experiment.

## Safe sequence

1. finish Wix estate inventory;
2. capture visual/current-state evidence;
3. reconcile historical design patterns;
4. decide target renderer/data architecture;
5. verify Git/Velo compatibility, including Velo Package constraints;
6. select a safe historical/clone/test site;
7. prove Git/CLI workflow there;
8. inspect/extract actual Velo source;
9. run code/security/data-flow audit;
10. prototype one bounded hybrid page;
11. independently validate;
12. DCS decides whether to apply the workflow to production SC.com.

## Engineering split

### Wix Editor / Local Editor
Best for visual layout, page composition, spacing, responsive adjustment, native Wix components, and manual design QA.

### IDE / Wix CLI / GitHub
Best for page code, backend Velo, web modules, packages, source control, tests, refactor, code review, and release evidence.

### Codex / Qwen / Antigravity
Best for bounded engineering tasks once source is exposed and the work package is explicit.

## Studio sites

Historical Wix Studio sites may be mined for visual ideas, layout patterns, typography, spacing, motion, and section pacing.

Do not make the target build dependent on Studio unless a separately approved cost/benefit analysis supports a subscription change.

## Validation rule

A successful CLI command is not a completed Wix change.

Completion requires correct source delta, visual behavior, mobile behavior, accessibility, Wix business/data behavior, test evidence, rollback, and DCS acceptance where required.