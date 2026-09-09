# ESCD ANTIGRAVITY POLLER CONTROL PACKET 002

**Task ID:** DCSE-ESCD-001-AG02  
**Parent:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Worker:** Antigravity  
**Execution role:** Bounded implementation worker  
**Controller:** DCS / DCSE control  
**Review authority:** Codex / senior engineering review after reset  
**Authorized branch:** `feature/escd-poller-ag02`  
**Status:** READY FOR ANTIGRAVITY EXECUTION  
**Primary objective:** Recover, harden, and validate the DCSE universal poller/dispatcher path for Antigravity and prepare it for controlled multi-model task dispatch without giving Antigravity product, governance, release, or branch-management authority.

## 1. Conduct rule

Antigravity is an executor, not a product owner, architect, governance authority, release authority, scheduler policy owner, or autonomous branch manager.

Antigravity SHALL:

- follow this packet literally;
- make only the minimum changes required to satisfy the stated acceptance criteria;
- prefer inspection and existing patterns over invention;
- stop on material ambiguity instead of selecting a new architecture;
- use VERIFIED / LIKELY / UNKNOWN in evidence;
- preserve all existing work and evidence;
- return only the allowed terminal states defined below.

Antigravity SHALL NOT:

- invent tasks, branches, architectures, registries, schemas, agents, model assignments, or release paths;
- broaden its own authority;
- create or switch to any branch other than the exact branch named in this packet;
- merge to `main`;
- rebase, force-push, reset, clean, delete, drop a stash, pop a stash, or overwrite uncommitted work;
- modify Codex-owned inherited Aegis reconciliation surfaces unless explicitly listed in ALLOWED PATHS;
- deploy production;
- change production authentication, credentials, permissions, RLS, secrets, spending, billing, or public state;
- self-approve a consequential action;
- treat successful command execution as acceptance without evidence;
- mark itself admitted based only on registry insertion.

If a requested action falls outside this packet, STOP and return the exact blocker.

## 2. Model instruction

For this task, use **Claude Opus 4.6 (Thinking)** as the execution model if that is the model selected by DCS in Antigravity.

Do not autonomously switch models during the task.

If the selected model becomes unavailable or rate-limited, STOP with `BLOCKED_MODEL_UNAVAILABLE` unless the controller has explicitly authorized a fallback model.

A future controller may authorize Claude Sonnet 4.6 (Thinking) for a bounded continuation, but Antigravity may not make that decision itself.

## 3. Git safety gate

Before any modification, run and report:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git stash list
git log -1 --oneline
```

Required branch is exactly:

`feature/escd-poller-ag02`

Rules:

1. If the current branch already equals the required branch and the worktree is clean, continue.
2. If the current branch differs but the worktree is clean, Antigravity MAY run only:
   `git switch feature/escd-poller-ag02`
3. If the worktree is dirty, STOP. Do not stash, reset, clean, checkout, force-switch, or move files.
4. If the required branch is missing locally, `git fetch origin feature/escd-poller-ag02` is permitted. After fetch, switch only if the worktree is clean.
5. Do not create another branch.
6. Do not rename the branch.
7. Do not touch or alter the historical stash `pre-aegis-slice001-stash` if present.

Allowed branch terminal condition: clean or intentionally modified only by this task.

## 4. Controlling sources

Read before editing:

1. root `AGENTS.md`
2. `DCSE_MANIFEST.yaml`
3. current operative `governance/v7.2/` designation and controlling R5 artifact
4. `03_WORK_ORDERS/ESCD/DCSE-ESCD-001_IMPLEMENTATION_PACKET_002.md`
5. `03_WORK_ORDERS/ESCD/DCSE-ESCD-001_RULESET_REGISTRY.md`
6. `03_WORK_ORDERS/ESCD/DCSE-ESCD-001_ANTIGRAVITY_POLLER_CONTROL_PACKET_002.md`
7. current universal dispatcher / poller code
8. `v7_worker` migrations, queue/claim/heartbeat/receipt contracts
9. existing runtime surface registry and agent registry contracts
10. prior Antigravity runtime admission artifacts and logs if present in repo

Do not substitute memory or model assumptions for repository/runtime evidence.

## 5. Historical defects that MUST be explicitly checked

Prior Antigravity runtime evidence showed all of the following defect classes. Treat them as required regression targets, not anecdotes.

### D1. Runtime surface identity mismatch

Historical values included both:

- `antigravity_windows_cli`
- `agy_windows_cli`

The runtime surface was not present in `runtime_surface_registry`, causing heartbeat foreign-key failure.

Required behavior:

- discover the current canonical runtime-surface naming contract;
- select the existing governed canonical value if present;
- if no canonical Antigravity surface exists, prepare the minimum additive registry/config change required by the existing schema;
- do not invent multiple aliases;
- one logical agent may have one or more execution surfaces only when the current schema explicitly supports that relationship.

### D2. Launcher command assumption

Historical preflight attempted `agy` even though the command was not recognized.

Required behavior:

- do not assume a launcher alias exists;
- inspect actual invocation configuration, PowerShell command resolution, scripts, wrappers, or executable path;
- use `Get-Command`, `where.exe`, repository config, or existing dispatcher configuration to discover the real executable path;
- do not install a package, change PATH, or invent an alias unless the packet is amended.

### D3. Heartbeat before admission

Historical heartbeat failed while later task claims still occurred.

Required behavior:

A worker is NOT claimable until all are true:

1. logical agent identity is registered and enabled;
2. runtime surface is registered and enabled;
3. host/runtime emits a valid heartbeat for the exact surface;
4. heartbeat is current within the existing lease/TTL contract;
5. the dispatcher identifies the surface as claimable;
6. lane/task authorization passes.

No heartbeat, no claim.

### D4. Assignment normalization / lane parsing defect

Historical inbox payloads contained `lane="DCSE"`, while the poller reported `lane '' not authorized`.

Required behavior:

- inspect the deserialization and candidate-normalization path;
- verify array/object enumeration for PowerShell `PSCustomObject`, JSON `.value`, single-object and multiple-object responses;
- preserve `task_key`, `task_id`, `assignment_id`, `lane`, `task_type`, `assignment_role`, and `assignment_status` through normalization;
- if authorization blocks a task, log the actual normalized task key and actual lane value;
- never authorize a blank lane by fallback.

### D5. Candidate enumeration inconsistency

Historical evidence showed candidate counts/types changing between `Object[]` and `PSCustomObject` before claims succeeded.

Required behavior:

- normalize inbox responses into one deterministic collection representation before filtering;
- unit-test zero, one, and multiple assignment shapes;
- unit-test `.value` wrapper and direct object shapes if both are supported by current code;
- no claim logic may depend on accidental PowerShell collection coercion.

## 6. Task boundary

### Primary task

Recover and validate the universal poller/dispatcher so Antigravity can be admitted and dispatched as a bounded runtime with minimal manual DCS intervention.

### Secondary task, only after primary acceptance

Prepare the dispatcher contracts needed to support multiple approved worker classes, including Codex, Antigravity, and Qwen, without assigning those models new authority.

This secondary work is interface/config scaffolding only unless the current repository already contains those worker registrations and launchers.

Do not build a new orchestration platform if the existing universal dispatcher can be repaired.

## 7. Allowed paths

Antigravity may modify only files proven to be part of the current universal dispatcher, worker-runtime configuration, poller tests, or task-specific evidence documentation.

Allowed examples, only if they already exist or are clearly the approved successor location:

- `09_WORKERS/**`
- `supabase/migrations/**` for additive dispatcher/runtime registry migration artifacts only
- dispatcher/poller scripts under the current canonical worker path
- test files for dispatcher/claim/heartbeat logic
- `03_WORK_ORDERS/ESCD/**` task evidence for AG02
- a dedicated `apps/escd/docs/**` or approved runtime evidence path

Read-only unless separately authorized:

- `apps/escd/policy/**`
- `apps/escd/tests/**` policy rules already passed
- `apps/aegis/**`
- `apps/sc-agent-os/**`
- governance files
- DDNA production migration/cutover files

If path ownership is unclear, STOP before editing it.

## 8. Preflight output

Before mutation, return and persist a short preflight:

```text
TASK_ID: DCSE-ESCD-001-AG02
BRANCH:
WORKTREE: CLEAN | DIRTY
AUTHORITY SOURCE:
OPERATIVE GOVERNANCE:
CURRENT POLLER PATH:
CURRENT DISPATCHER PATH:
CURRENT AGENT REGISTRY STATE:
CURRENT RUNTIME SURFACE STATE:
CURRENT HEARTBEAT STATE:
CURRENT CLAIM FUNCTION/PATH:
CURRENT RECEIPT/RESULT PATH:
CANONICAL ANTIGRAVITY RUNTIME ID:
ACTUAL ANTIGRAVITY LAUNCH COMMAND OR PATH:
VERIFIED:
LIKELY:
UNKNOWN:
PLANNED MINIMUM DELTA:
ROLLBACK:
STOP_GATES:
```

Do not continue if current poller/dispatcher location, branch state, or authority cannot be established.

## 9. Implementation sequence

Execute in this order. Do not skip ahead.

### Phase A. Inspect existing neutral dispatcher

Identify:

- scheduler/poller entry point;
- polling cadence source;
- assignment inbox source;
- candidate normalization;
- authorization filter;
- atomic claim function;
- lease/heartbeat mechanism;
- runtime surface registry lookup;
- agent registry lookup;
- task status/result submission;
- receipt/evidence path;
- worker invocation mapping;
- retry/recovery logic;
- current tests.

Produce a one-page CURRENT STATE note before edits.

### Phase B. Establish one canonical Antigravity execution surface

Do not invent architecture.

If the current governed registry already defines the surface, use it.

If it is missing, create the minimum additive migration/config artifact required to register exactly one canonical Antigravity Windows execution surface.

Required fields are whatever the current schema requires, including family, enabled/disabled state, polling mode, claimability, host/runtime identity, or equivalent.

Do not weaken foreign keys or bypass the registry to make heartbeat succeed.

### Phase C. Repair launcher discovery

Resolve the actual non-interactive Antigravity invocation path.

Do not assume `agy`.

If no reliable headless/non-interactive invocation exists in the current environment, STOP with exact evidence:

`BLOCKED_HEADLESS_INVOCATION`

Do not simulate execution.

### Phase D. Repair heartbeat admission gate

Enforce:

`registered agent + registered surface + valid heartbeat + current lease = eligible for claim evaluation`

If heartbeat fails, worker remains NOT_ADMITTED and claim logic is not called.

Record explicit heartbeat failure reason without credentials.

### Phase E. Repair candidate normalization and authorization

Normalize assignment responses deterministically.

Test at minimum:

- zero assignments;
- one assignment;
- two assignments;
- `.value` wrapped response;
- direct object response if supported;
- DCSE authorized lane;
- unauthorized lane;
- missing lane;
- assigned to another worker;
- inactive/closed assignment;
- duplicate assignment response.

A missing or blank lane must fail closed.

### Phase F. Atomic claim verification

Use the existing governed atomic claim mechanism.

Do not replace it with ad hoc status updates.

Prove that two simulated workers cannot successfully claim the same assignment.

If the current atomic claim contract cannot be proven, STOP with:

`BLOCKED_ATOMIC_CLAIM`

### Phase G. Receipt and completion path

A successful governed smoke task must produce:

- task/assignment identity;
- worker identity;
- runtime surface;
- claim timestamp;
- heartbeat/lease evidence;
- execution result;
- completion/submit timestamp;
- receipt/evidence reference;
- no secret material.

### Phase H. Multi-worker routing scaffold

Only after Antigravity passes admission and claim acceptance:

Inspect whether the existing dispatcher already has a worker capability map.

If yes, extend configuration minimally so the dispatcher can represent worker classes such as:

- Codex
- Antigravity
- Qwen

Do not invent launch commands for unavailable workers.

Each worker record should support existing schema equivalents for:

- logical agent/model identity;
- runtime surface;
- enabled/available state;
- allowed lane/task types;
- branch/path ownership if already supported;
- heartbeat/lease;
- current assignment;
- review requirement.

Antigravity does not choose which model receives an arbitrary task. It only implements the controller-provided routing contract.

## 10. Poller control behavior

The poller must operate by exception and preserve DCS attention.

Required behavior:

1. poll at the existing governed cadence;
2. read eligible assignments;
3. normalize response shape;
4. reject tasks outside worker authorization;
5. reject claim when runtime heartbeat/lease is invalid;
6. reject tasks whose branch/path lock conflicts with an active assignment if current architecture supports locks;
7. atomically claim one eligible task;
8. invoke only the configured worker/runtime;
9. update heartbeat while work is active according to current contract;
10. submit result/receipt;
11. release/expire lease according to current contract;
12. continue to next eligible assignment only after prior claim reaches a valid terminal/handoff state.

No silent infinite retry.

No self-generated tasks.

No self-generated branches.

No task reassignment based on model preference.

## 11. Decision authority

Antigravity MAY make only bounded implementation choices when all are true:

- choice is inside the exact task scope;
- no architecture change;
- no authority change;
- no security weakening;
- no new dependency or service;
- no production release;
- reversible;
- supported by existing repository pattern;
- covered by tests.

Antigravity MUST STOP for:

- branch/worktree conflict;
- missing authority;
- unclear canonical source;
- architecture conflict;
- security/RLS uncertainty affecting production;
- destructive operation;
- credential/auth/permission change;
- production DB mutation not explicitly authorized;
- model/launcher unavailability;
- inability to prove atomic claim;
- inability to obtain a real heartbeat;
- protected-lane conflict;
- external spend;
- public deploy/release;
- request to alter governance;
- request to override Codex-owned files.

The stop output must identify the smallest action required to unblock.

## 12. Supabase rule

Supabase may be inspected using approved access.

Antigravity may prepare additive migration/config artifacts needed for runtime admission.

Do not apply destructive DDL.

Do not weaken RLS.

Do not expose service-role keys.

Do not change production authentication.

If a live non-destructive registry write is required to prove admission, do not perform it unless the current task packet, operative governance, and runtime access policy explicitly permit that exact class of write. Otherwise stop at `READY_FOR_CONTROLLED_REGISTRY_APPLY` with the exact SQL/RPC/config delta and rollback.

## 13. Required tests

### Static

- script syntax/parse test;
- configuration parse test;
- no secret scan;
- no unauthorized path change;
- branch/path ownership validation.

### Unit

- runtime identity resolution;
- launcher discovery failure behavior;
- heartbeat success/failure;
- admission gate;
- assignment collection normalization;
- lane authorization;
- assigned-worker authorization;
- empty/missing lane fail closed;
- candidate dedupe;
- atomic claim simulation;
- lease expiry/recovery;
- receipt construction;
- retry bound.

### Integration, safe environment

- real dispatcher reads assignment inbox;
- real Antigravity heartbeat accepted;
- one governed smoke assignment claimed only after heartbeat;
- one result submitted;
- evidence/receipt produced;
- second worker cannot claim the same assignment;
- restart/recovery does not double-execute;
- unchanged queue does not create duplicate work.

### Regression

Specifically reproduce and prove repaired:

- FK heartbeat failure for missing runtime surface;
- unrecognized `agy` launcher assumption;
- blank-lane authorization bug;
- Object[] vs PSCustomObject candidate-shape bug;
- claim attempted without valid admission.

## 14. Repair loop

Use one continuous loop:

`inspect -> reproduce -> minimal repair -> test -> repair -> retest`

Do not lower test expectations to create a pass.

Do not delete failing tests.

Do not broaden scope because another defect is nearby.

P0/P1 security, authority, atomicity, evidence, branch integrity, and double-execution defects must be repaired or returned BLOCKED.

## 15. Evidence deliverables

Create or update only on the authorized branch:

- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_PREFLIGHT.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_POLLER_CURRENT_STATE.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_IMPLEMENTATION_REPORT.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_TEST_EVIDENCE.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_SECURITY_REVIEW.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_ROLLBACK.md`
- `03_WORK_ORDERS/ESCD/DCSE-ESCD-001-AG02_HANDOFF.md`

Handoff must state:

- exact branch;
- exact final commit SHA;
- files changed;
- runtime/config/migration artifacts changed;
- tests and exact results;
- real heartbeat evidence;
- claim evidence;
- receipt evidence;
- failures repaired;
- remaining UNKNOWN items;
- rollback;
- whether any live Supabase write occurred;
- explicit statement that no production deployment, merge, credential exposure, or governance promotion occurred.

## 16. Commit discipline

Commit only coherent task-owned changes.

Before each commit:

```text
git status --short
git diff --check
git diff --stat
git diff
```

Stage only explicit task files. Do not use broad staging commands such as `git add .` or `git add -A`.

Use explicit file paths.

After commit:

```text
git status --short
git log -1 --oneline
```

Do not push to another branch.

Do not merge.

## 17. Final acceptance for Antigravity

Antigravity may return `READY_FOR_CODEX_REVIEW` only when all are true:

- branch integrity preserved;
- canonical runtime surface resolved;
- actual launcher path resolved;
- real heartbeat succeeds;
- heartbeat gates claim eligibility;
- candidate normalization is deterministic;
- lane authorization bug is repaired/tested;
- atomic claim behavior is proven;
- governed smoke claim executes only after admission;
- result and receipt are produced;
- no duplicate claim/execution occurs;
- regression suite passes;
- rollback is documented;
- evidence package is complete;
- no prohibited action occurred.

If code/tests are complete but a controlled live registry application is the only remaining step, return:

`READY_FOR_CONTROLLED_REGISTRY_APPLY`

If a material dependency is missing, return:

`BLOCKED`

If bounded work is valid but incomplete, return:

`PARTIAL`

Do not use `COMPLETE`, `PRODUCTION_READY`, or `RELEASED`.

## 18. Required final response format

Return only this structure:

```text
TASK_ID: DCSE-ESCD-001-AG02
STATUS: READY_FOR_CODEX_REVIEW | READY_FOR_CONTROLLED_REGISTRY_APPLY | PARTIAL | BLOCKED
BRANCH:
FINAL_COMMIT:
MODEL_USED:
RUNTIME_SURFACE:
LAUNCHER_PATH:
HEARTBEAT: PASS | FAIL | NOT_RUN
ATOMIC_CLAIM: PASS | FAIL | NOT_RUN
SMOKE_ASSIGNMENT: PASS | FAIL | NOT_RUN
TESTS:
FILES_CHANGED:
LIVE_SUPABASE_WRITE: YES | NO
PRODUCTION_DEPLOY: NO
MERGE: NO
SECRETS_EXPOSED: NO
VERIFIED:
LIKELY:
UNKNOWN:
BLOCKERS:
ROLLBACK:
NEXT_HANDOFF: Codex / DCSE controller
```

No narrative beyond this structure unless reporting a material blocker that requires exact technical evidence.