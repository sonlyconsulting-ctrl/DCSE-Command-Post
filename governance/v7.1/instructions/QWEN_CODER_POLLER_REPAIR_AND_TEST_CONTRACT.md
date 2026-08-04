---
dcse_zone: execution
dcse_subzone: instructions
dcse_authority_level: INSTRUCTION
dcse_document_id: QWEN_CODER_POLLER_REPAIR_AND_TEST_CONTRACT
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: SC
dcse_policy_authority: false
---

# Qwen Coder Poller Repair and Test Contract

Status: ASSIGNED SUBJECT TO CONTROLLING GOVERNANCE
Authority route: Master Profile, D21, D22, and the recorded task authorization
Primary executor: Qwen Coder
Independent reviewer: Claude Code or another attributable independent reviewer
Task key: `V7_1_ACTION_1_POLLER_HARDENING`

## Objective

Restore and harden the existing poller system without creating another poller architecture.

## Mandatory Source Order

1. Read repository-root `DCSE_MANIFEST.yaml`.
2. Read `../POLLER_SOURCE_INTAKE_AND_BASELINE_DECISION.md`.
3. Read this contract.
4. Locate the uploaded-source equivalents and prior canonical files on the authorized host.
5. Query authenticated GitHub and both authorized Supabase projects before concluding that any dependency is absent.

## Baseline Rule

Use `job_tribunal_poller_v7.py` as the architectural repair baseline.

Treat `claude_code_poller.ps1` as the currently evidenced SC-Command-Post operational worker poller to test and harden.

Legacy `job_tribunal_poller.py` variants and `start_tribunal_poller_20260604.cmd` are evidence only. Do not activate them.

## Phase 1: Evidence and Location Audit

Record exact paths, hashes, Git status, branch, scheduled-task names, last-run timestamps, last heartbeat, and last successful task claim for:

- `job_tribunal_poller_v7.py`
- `tribunal_v7_state_machine.py`
- `tribunal_v7_codex_adapter.py`
- `tribunal_v7_fable_adapter.py`
- `claude_code_poller.ps1`
- registration scripts for Windows Task Scheduler
- credential-registration script
- poller state and log files

If two competing canonical implementations exist, stop the affected selection and report both. Do not select silently.

## Phase 2: Reproduce Before Patch

Run audit-only tests first. Do not use `--dispatch` until source and authorization controls are verified.

Required reproduction targets:

1. Confirm whether the scheduled task is firing.
2. Confirm whether the PowerShell poller can authenticate and write a heartbeat.
3. Confirm whether task claiming is atomic and limited to one concurrent task.
4. Confirm whether a temporary allowlist is blocking valid work.
5. Confirm whether missing CLI availability, credential decryption, branch mismatch, or stopped Task Scheduler is the actual outage cause.
6. Confirm whether the V7 Python candidate imports are resolvable.

## Phase 3: Classification

For every touched component, report one classification:

- RETAIN
- WRAP
- REFACTOR
- REPLACE

REPLACE requires direct evidence that repair is unsafe or impractical. Architectural preference is insufficient.

## Authorized Changes

- repair confirmed defects in existing scripts;
- narrow or replace temporary validation allowlists with capability and authority checks from `DCSE_MANIFEST.yaml`;
- add structured heartbeat and health evidence;
- add bounded retry and timeout behavior;
- add overlap prevention and idempotency tests;
- add a health monitor only if it monitors the existing scheduled poller rather than becoming another dispatcher;
- update tests and operational documentation;
- create a branch and draft PR for review.

## Prohibited Changes

- create a parallel poller or orchestration service;
- activate legacy Git bridge behavior;
- use `git add .` in an automated worker;
- make task packets mutable;
- move or rename quarantine files automatically;
- expose or request service-role keys in chat;
- alter production credentials;
- broaden lane access;
- merge or promote the changes;
- change production deployment state.

## Acceptance Tests

1. Startup reads `DCSE_MANIFEST.yaml` and records a startup acknowledgment.
2. GitHub repository and expected branch are verified.
3. SC-Command-Post heartbeat is written successfully.
4. One approved test task is claimed exactly once.
5. A second concurrent cycle cannot claim the same task.
6. Retry count is bounded.
7. Timeout produces a blocked or failed receipt, never success.
8. A failed worker cannot be marked completed.
9. A task requiring DCS authority remains blocked.
10. An operational V7.1 task not reserved to DCS can proceed without an obsolete temporary allowlist entry.
11. Restart recovery is demonstrated.
12. GitHub and Supabase remain independently usable while the poller is stopped.
13. No new canonical poller is introduced.
14. All changed files have exact reasons and before-and-after hashes.

## Required Output

Return:

- evidence coverage acknowledgment;
- component classification table;
- root cause statement;
- exact files changed;
- tests executed and results;
- Task Scheduler evidence;
- heartbeat and task-claim evidence;
- Git commit and draft PR;
- rollback procedure;
- unresolved blockers;
- recommendation to RETAIN, WRAP, REFACTOR, or REPLACE each component.

Stop after the draft PR and evidence submission. Independent review follows. DCS retains promotion authority.

## Instruction Boundary

This contract assigns bounded work. It does not create standing doctrine, choose constitutional authority, grant credentials, authorize production changes, or promote its own output.