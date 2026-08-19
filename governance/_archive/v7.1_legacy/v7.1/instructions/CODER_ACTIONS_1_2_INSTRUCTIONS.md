---
dcse_zone: execution
dcse_subzone: instructions
dcse_authority_level: INSTRUCTION
dcse_document_id: CODER_ACTIONS_1_2_INSTRUCTIONS
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: SC
dcse_policy_authority: false
---

# Coder Instructions: V7.1 Actions 1 and 2

Status: AUTHORIZED FOR BOUNDED EXECUTION SUBJECT TO CONTROLLING GOVERNANCE
Authority route: `../DCSE_Master_Profile_v7.1.md`, D21, D22, and applicable DCS decision
Assignee class: Coder or equivalent bounded implementation agent

## Startup Gate

Before work, read `/DCSE_MANIFEST.yaml` and report:

- repository and branch verified
- GitHub access mode
- DCSE-DDNA access state
- SC-Command-Post access state
- lane and task loaded
- no privileged secret exposed

## Action 1: Restore and Harden Poller and Heartbeat

Objective: establish reliable task transport without making the poller a source of truth or single point of failure.

Required work:

1. Inventory the existing poller, Task Scheduler entry, configuration, logs, and credential dependencies.
2. Preserve the current implementation before modification.
3. Determine the actual failure mode using logs and scheduler history.
4. Repair bounded defects only.
5. Add `DCSE-PollerHealthMonitor.ps1` or a functionally equivalent monitor that:
   - runs independently every five minutes;
   - verifies the poller completed within the expected interval;
   - records heartbeat and failure evidence in SC-Command-Post;
   - attempts one bounded restart;
   - prevents restart loops;
   - raises a blocked event after repeated failure;
   - never stores service-role credentials in source or logs.
6. Add idempotency, duplicate-task protection, structured logs, and graceful network-failure handling.
7. Confirm manual authenticated sessions remain available when the poller is down.
8. Produce tests and evidence for normal operation, missed cycle, network outage, Supabase outage, GitHub outage, restart, and recovery.

Completion evidence:

- canonical paths and artifact IDs
- Git commit and PR reference
- scheduler configuration export
- test results
- heartbeat records
- rollback instructions
- known limitations

## Action 2: Resolve Staging Environment

Objective: restore a valid non-production environment for runtime promotion validation.

Required work:

1. Verify the reported staging project `liwdquzuigrlgfzgmpjp` and document its actual state.
2. Search GitHub, DCSE-DDNA, and SC-Command-Post for existing staging decisions, receipts, dependencies, and replacement candidates.
3. If recoverable, repair the existing staging target using the least disruptive method.
4. If unavailable, prepare or create a bounded replacement under the operational authority in `DCSE_MANIFEST.yaml`.
5. Do not alter production projects, domains, or production data.
6. Apply an unambiguous name and record project ID, owner, purpose, region, cost state, expiration or review date, and linked tasks.
7. Validate schema compatibility, migrations, secrets isolation, RLS, test data isolation, and rollback.
8. Update GitHub and both Supabase registries with evidence.

Completion evidence:

- verified staging project identity
- decision: RETAIN, REPAIR, or REPLACE
- GitHub and Supabase references
- validation test results
- cost and lifecycle notes
- remaining promotion blockers

## Stop Gates

Stop and escalate for:

- production impact
- destructive operation outside approved procedure
- security exception
- lane boundary conflict
- constitutional governance change
- unavailable required credentials that cannot be resolved through approved OAuth or Control Plane access

Ordinary documentation, artifact registration, draft PR creation, bounded repair, staging preparation, and evidence collection remain subject to the governing task authorization and applicable access controls.

## Instruction Boundary

This packet directs bounded work. It does not create standing policy, expand model authority, promote artifacts, or override the Master Profile, D21, D22, D05, or DCS reserved stop-gates.