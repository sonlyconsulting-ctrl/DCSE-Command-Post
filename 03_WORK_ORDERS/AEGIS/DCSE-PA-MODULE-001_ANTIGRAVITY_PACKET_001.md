# AEGIS ANTIGRAVITY IMPLEMENTATION PACKET 001

**Task ID:** DCSE-PA-MODULE-001-AG01  
**Parent Task:** DCSE-PA-MODULE-001  
**Lane:** DCSE / Command Post  
**Role:** Independent implementation engineer  
**Branch:** `feature/aegis-antigravity-slice001`  
**Review authority:** Codex + GPT-6 Astra senior engineering review  
**Objective:** Implement Aegis Executive Kernel Slice 001 from the approved parent build packet without changing its architecture, governance, or acceptance criteria.

## 1. Controlling instructions

Read these before changing code:

1. repository root `AGENTS.md`
2. `03_WORK_ORDERS/AEGIS/DCSE-PA-MODULE-001_BUILD_PACKET_001.md`
3. `DCSE_MANIFEST.yaml`
4. current `governance/v7.2/` authority applicable to this task
5. existing `apps/sc-agent-os/` implementation and documentation
6. existing Supabase migrations, RLS/security controls, receipts/evidence patterns, DCS decision queue, phase gates, runtime health, Tribunal dispatch, task/portfolio functions

The parent Build Packet 001 defines product scope and acceptance. This Antigravity packet defines implementation role and handoff discipline. If they conflict, stop and report the conflict rather than silently choosing a new architecture.

## 2. Engineering role

Act as the implementation engineer, not product owner and not final release authority.

You may:

- inspect the repository and approved connected development resources
- create/refactor code on this branch
- create additive reversible migrations when justified
- implement automated tests
- run non-destructive tests and local development services
- document verified implementation evidence
- commit coherent checkpoints to this branch

You may not:

- merge to `main`
- production-deploy
- weaken RLS or existing security controls
- expose or commit secrets
- alter authoritative doctrine to make implementation easier
- delete authoritative evidence or source records
- change spending/subscriptions
- perform irreversible external actions
- declare final release approval

## 3. Baseline-first mandate

Do not begin by generating a new application from assumptions.

First inspect and record VERIFIED / LIKELY / UNKNOWN for:

- current Aegis/Command Post repository structure
- reusable `apps/sc-agent-os` services and UI/API patterns
- current database/schema assumptions and migrations
- auth integration points
- RLS and privileged-function boundaries
- job/task/dispatch/receipt patterns
- deployment/runtime wiring
- DCS branding assets/tokens
- test harnesses and package/runtime versions

Create `apps/aegis/docs/ANTIGRAVITY_BASELINE.md` before or alongside the first implementation commit. Do not expose credentials in evidence.

## 4. Required implementation

Implement the same Vertical Slice 001 specified by the parent packet. At minimum the branch must attempt to deliver:

- dedicated DCS-branded Aegis operating surface
- responsive desktop and Android-class layout
- DCS Enterprise and DCS Employment mission surfaces
- Google/Supabase auth scaffolding compatible with one DCS principal and linked identities where safely supported
- persisted executive session/state independent of chat history
- durable job lifecycle and event history
- approvals and evidence/receipts
- executive briefing derived from persisted state
- deterministic next-best-action scoring with transparent factors
- RLS for every exposed Aegis state table
- notification-intent/provider abstraction where full push provisioning is external
- Command Post deep link/control-plane relationship

Prefer reuse or compatible shared modules over duplication. If a parent requirement cannot be completed because of missing external configuration, implement the safe scaffolding, test what can be tested, and document the exact remaining action.

## 5. State and workflow contract

The minimum job state model remains:

`queued -> running -> waiting_approval -> completed | failed | cancelled -> archived`

Every job must have stable identity, mission, purpose, priority, executor/tool target, state, timestamps, provenance, approval requirement, evidence references, and failure detail where applicable.

The opening briefing must answer from real state:

1. What changed since the prior Aegis session?
2. What completed?
3. What requires DCS approval?
4. What is the highest-value next action?
5. What blockers exist?

Do not fabricate activity to make the UI appear populated. Seed/demo data, if necessary for automated UI testing, must be explicitly labeled test data and isolated from authoritative state.

## 6. Deterministic business logic

Slice 001 next-best-action ranking must be reproducible before model enrichment. Include at least:

- mission priority
- job/task priority
- urgency/deadline
- blocked state
- approval dependency
- revenue relevance when known
- age/staleness
- explicit DCS override

Record the score components or reason structure so Codex/Astra can independently verify the ranking.

Do not embed controlling DCS doctrine solely inside LLM prompts. Keep deterministic policy/business logic inspectable and testable.

## 7. Supabase and security requirements

Security is a hard gate.

- RLS on all exposed Aegis user/state tables
- explicit principal/owner predicates
- no authorization based on user-editable metadata
- service-role and secret credentials server-side only
- least privilege
- parameterized operations
- inspect views, RPCs, `SECURITY DEFINER` functions and grants
- test authorized and unauthorized SELECT/INSERT/UPDATE/DELETE
- test anonymous rejection where required
- preserve existing security remediation
- run available Supabase security/advisor checks after schema changes
- record residual findings without waiving them

If a security control cannot be verified, classify the affected acceptance item as PARTIAL/BLOCKED rather than PASS.

## 8. Testing responsibility

Antigravity performs the implementation-side test pass before handoff.

Required tests include:

- reproducible app boot/build
- auth scaffolding/happy and rejected paths to the extent available
- persisted session restore
- mission retrieval
- job creation and valid/invalid transitions
- approval transitions and bypass rejection
- briefing derivation from actual persisted/test-isolated state
- next-best-action reproducibility
- evidence/receipt creation
- failure handling
- RLS access matrix
- desktop viewport
- Android-class viewport
- keyboard/accessibility basics
- duplicate/idempotency behavior where relevant
- stale job handling
- regression of reused Command Post functionality touched by changes

Repair implementation defects discovered during this pass. Do not manipulate tests or acceptance criteria to create a pass.

## 9. Evidence deliverables

Commit the implementation and, where applicable, create:

- `apps/aegis/docs/ANTIGRAVITY_BASELINE.md`
- `apps/aegis/docs/ANTIGRAVITY_IMPLEMENTATION_REPORT.md`
- `apps/aegis/docs/ANTIGRAVITY_TEST_EVIDENCE.md`
- `apps/aegis/docs/ANTIGRAVITY_SECURITY_REVIEW.md`
- `apps/aegis/docs/ANTIGRAVITY_HANDOFF.md`

The handoff must state:

- exact branch and final commit SHA
- files changed
- migrations added/changed
- commands/tests run and results
- what is VERIFIED / LIKELY / UNKNOWN
- unresolved defects by severity
- security residuals
- external configuration still required
- rollback procedure
- explicit statement that no production deployment or merge was performed

## 10. Handoff to Codex/Astra

When implementation-side work is complete, stop implementation and leave the branch ready for independent senior review.

Codex/Astra is expected to compare this branch against `feature/aegis-executive-kernel` and the parent Build Packet 001, then independently perform:

- architecture and requirements conformance review
- code/diff review
- security/RLS review
- migration review
- test-quality review
- independent functional/integration validation
- adversarial permission testing
- end-to-end/regression validation
- defect remediation where authorized
- objective release scoring

Do not self-promote the branch based solely on Antigravity's test results.

## 11. Stop gates

Stop and produce a precise BLOCKED/PARTIAL handoff only for a material condition such as:

- missing required authority or access
- credential/secret exposure
- destructive operation requiring approval
- unresolved critical security issue
- incompatible current governance
- required external OAuth/provider configuration that cannot be safely completed in code
- material architecture conflict with the parent packet

Minor implementation decisions should be resolved using existing repository patterns and documented rather than escalated.

## 12. Exit criteria

Antigravity's assignment is complete when:

- the Slice 001 implementation is committed to `feature/aegis-antigravity-slice001`
- implementation-side tests and security checks have been run
- evidence documents are committed
- rollback is explicit
- all limitations are disclosed
- the branch is clean and reviewable by Codex/Astra
- no production deployment or merge has occurred

**Final status vocabulary:** `READY_FOR_CODEX_REVIEW`, `PARTIAL`, or `BLOCKED`.

Do not use `COMPLETE`, `PRODUCTION_READY`, or `RELEASED`; final acceptance belongs to the independent Codex/Astra review and DCS governance gates.