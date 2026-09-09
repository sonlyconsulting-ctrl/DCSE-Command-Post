# ESCD PHASE ROADMAP

**Task ID:** DCSE-ESCD-001  
**Purpose:** Keep the assistant build moving as a controlled stream while separating non-material automatic progression from genuine DCS stop-gates.

## Phase 0: Contracts and control plane

Deliverables:
- ESCD identity/product boundary
- requirements registry
- task taxonomy
- autonomy/approval contract
- operating workflow/process stream
- phase roadmap

Exit: contracts committed and reviewable. No runtime release implied.

## Phase 1: Executive Kernel

Equivalent implementation lineage: prior Aegis Slice 001.

Deliver:
- ESCD UI identity/refactor
- persisted executive state
- DCSE + DCS Employment missions
- job lifecycle
- briefing
- deterministic NBA
- approvals
- evidence
- RLS/security
- responsive interface
- test passes and rollback

Gate: >=95/100 evidence score and no failed security/governance/authority/data-integrity/rollback gate.

## Phase 2: Intake, tasking and executive queues

Deliver:
- Inbox/Pins/Backlog normalization
- dedupe/provenance
- NOW/APPROVAL/WAITING/WATCH/BACKLOG queues
- project/dependency support
- reminders/notification intents
- stale/blocked routing and anti-loop behavior

May begin automatically after Phase 1 passes non-material gates. No production release is implied.

## Phase 3: DCS Employment mission operations

Deliver:
- opportunity pipeline
- recruiter/client/contact linkage
- deadlines and follow-up
- submission packet state
- resume/material version linkage
- rate/location/travel constraints
- revenue relevance
- interview/offer progression

External submissions remain governed by autonomy contract.

## Phase 4: Communications and calendar

Deliver:
- Gmail/calendar/contact integration where authorized
- message triage
- commitment extraction
- draft preparation
- follow-up/watch
- calendar agenda/conflict detection
- approval-gated send/change actions

Connector authorization and external writes remain stop-gated as required.

## Phase 5: DDNA/RAG knowledge integration

Deliver:
- governed retrieval contract
- source/provenance display
- candidate contribution path
- conflict/duplicate handling
- no silent authority promotion
- task-relevant knowledge injection without making chat the source of truth

Coordinate with dedicated DDNA consumer cutover; do not couple ESCD release to unfinished production cutover unless technically required.

## Phase 6: Delegated workflows and recurring operations

Deliver:
- reusable workflow templates
- scheduled/condition-triggered work
- bounded retries
- worker/model/tool routing
- receipts and recovery
- monitoring/watch workflows

## Phase 7: Voice and richer mobile assistant

Deliver when justified:
- voice-first interaction
- richer Android push actions
- mobile quick capture
- assistant presentation enhancements

## Phase 8: Broader personal mission domains

Add only after DCS defines desired boundaries and privacy posture.

## Automatic progression rule

Engineering may advance from one phase to the next without another DCS interruption only when:
- current phase acceptance evidence passes
- no critical security/governance/authority/data-integrity defect exists
- rollback/checkpoint exists
- no new secrets/access/spending/production release is required
- next phase remains inside this approved architecture and autonomy contract

Stop for DCS when a phase requires production release, new credential/access authority, spending, destructive operation, material architecture/economic change, unresolved governance conflict, or other A3/A4 condition.

## Parallel work rule

Independent non-conflicting workstreams may proceed concurrently, but they must preserve stable task IDs, branch ownership, evidence, and source boundaries. Do not allow two agents to edit the same implementation surface concurrently without explicit coordination.