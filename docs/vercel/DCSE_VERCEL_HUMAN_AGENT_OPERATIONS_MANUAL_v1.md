# DCSE Vercel Human and Agent Operations Manual v1

**Status:** OPERATIVE - controlled execution manual  
**Package:** DCSE v7.2 Vercel Governance Package  
**Task ID:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02  
**Lane / Entity:** SC / DCSE Command Post  
**Authority:** Operates under the promoted Vercel Agent and Platform Doctrine, D21, D22, D05, and the v7.2 platform/reconciliation standards.  
**Non-action boundary:** This manual does not itself authorize production deployment, domain mutation, billing changes, secret changes, or Supabase mutation.

## 1. Preflight record

Before substantive Vercel work, record:

- Task ID and requested outcome;
- project/team and owning product/entity;
- environment: Development, Preview, or Production;
- repository, branch, exact source SHA, and root directory;
- authorized action class: read, build, preview, test, promote, rollback, domain, configuration, billing;
- systems touched;
- secret/PS exposure;
- approval gate;
- cost/rate-limit state;
- rollback target;
- evidence destination and exit criteria.

Unknown project identity, production authority, secret exposure, or destructive scope is a stop-gate.

## 2. Read-only inspection

Preferred inspection sequence:

1. verify team and project identity;
2. verify source link and root directory;
3. list relevant deployments;
4. inspect candidate deployment metadata and logs;
5. record domain/alias assignment;
6. inventory required variable names by environment without values;
7. inspect current plan/limit condition where material;
8. return Verified / Likely / Unknown.

Do not alter protection, settings, billing, domains, secrets, or deployments during a read-only task.

## 3. Linking and local project identity

Before `vercel link` or equivalent:

- confirm the intended team;
- confirm the exact project ID, not only a similar display name;
- run from the intended application/root directory;
- treat `.vercel/` as local linkage metadata;
- do not commit secrets;
- for monorepos, prefer explicit repository/project root mapping.

Record the resulting project/source identity in the task evidence.

## 4. Configuration changes

For `vercel.json`, `vercel.ts`, framework config, routes, headers, redirects, or Function configuration:

1. inspect current behavior;
2. define the exact defect or required capability;
3. compare no-change and smallest-change alternatives;
4. avoid migration merely because a newer format exists;
5. validate syntax/build locally where practical;
6. create one bounded preview;
7. test affected routes;
8. preserve rollback to the prior source commit/configuration.

## 5. Environment variable operations

Maintain a matrix of variable NAME, environment, public/server-only classification, owner, required/optional status, and last verified date. Never place secret values in the matrix.

When a variable is missing:

- identify which environment is affected;
- verify whether the product actually requires it;
- request or use authorized secret-store access;
- never copy a production secret into preview solely to make a check green;
- retest only the affected candidate.

## 6. Preview procedure

For a candidate preview:

1. record source SHA;
2. identify project/root;
3. create or identify one preview deployment;
4. preserve deployment protection;
5. wait for platform build state;
6. run route/API smoke tests;
7. test desktop/mobile as applicable;
8. test auth/data/provider path where applicable;
9. inspect browser console and runtime logs;
10. record result against the test matrix;
11. stop if quota limits make further retries non-informative.

A failed preview caused by plan capacity is an infrastructure gate, not proof of application failure.

## 7. Production promotion procedure

Production promotion is permitted only with explicit authority.

1. confirm exact validated deployment;
2. confirm exact PR/head SHA and applicable checks;
3. confirm no unresolved security or critical product finding;
4. confirm environment-variable presence without disclosure;
5. confirm domain target and customer critical path;
6. confirm data/provider compatibility and any database migration state;
7. confirm rollback target;
8. record DCS approval;
9. promote the exact validated deployment where the approved procedure supports build-once/promote;
10. observe runtime after traffic assignment;
11. reconcile GitHub, Vercel, data state, and Tribunal evidence.

Do not rebuild a different artifact and represent it as the validated candidate.

## 8. Rollback procedure

1. capture incident/task ID and reason;
2. identify current and target deployment IDs;
3. assess data and external side effects;
4. confirm rollback authority;
5. reassign traffic using the authorized rollback mechanism;
6. verify domains and critical routes;
7. inspect logs and customer path;
8. reconcile any database/external state that was not reversed;
9. record final status as COMPLETE, PARTIAL, or BLOCKED.

## 9. Monorepo deployment-storm containment

On unexpected deployment volume:

- stop manual and automated retries;
- identify all projects watching the repository;
- map root and trigger rules;
- identify documentation-only/unrelated changes that caused builds;
- preserve the first representative failures;
- do not buy capacity as the first correction;
- propose path/ignored-build/root controls;
- resume with one bounded validation after capacity returns.

## 10. Build failure runbook

Check in order:

1. project and deployment identity;
2. source SHA;
3. root directory;
4. first material build error;
5. package manager/lockfile;
6. runtime version;
7. required environment-variable presence;
8. framework/output settings;
9. smallest corrective change;
10. one rebuild and evidence update.

## 11. Runtime failure runbook

Check in order:

1. domain points to expected deployment;
2. reproduce one traceable request;
3. Function/runtime logs;
4. dependency/provider response;
5. authentication/authorization;
6. data source health;
7. cache behavior;
8. rollback versus forward-fix risk;
9. retest user journey;
10. reconcile evidence.

## 12. Agent execution boundaries

Agents may inspect and recommend within verified scope. Before any mutation, the agent SHALL re-evaluate action type, authority, rollback, secrets, cost, and destination. No agent may infer permission from Vercel access alone.

## 13. Evidence packet

Return:

- Task ID and outcome;
- project/team/environment;
- source repo/branch/SHA/root;
- deployment ID/URL/status;
- domains tested;
- variable-name review;
- build/runtime/browser test results;
- cost/limit state;
- data/provider dependencies;
- security findings;
- rollback;
- GitHub PR/check links;
- Tribunal evidence link;
- unresolved findings;
- required human decision if any.

## 14. Closeout states

- COMPLETE: outcome and cross-system proof reconcile.
- PARTIAL: useful work is done but one or more evidence/dependency states remain open.
- BLOCKED: required authority, access, separation, or execution surface is unavailable.
- HOLD: deliberate pause due to capacity, security, or dependent-system gate.

## Level Zero approval record

This manual was approved as part of the package-level Vercel governance promotion for Task `DCSE-V72-PLATFORM-GOVERNANCE-20260915-02`. It does not authorize production mutation by itself.
