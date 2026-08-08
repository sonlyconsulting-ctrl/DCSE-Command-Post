# MP72 Poller Session Runtime Doctrine

Authority: DCS
Controller: DCSE Master Profile v7.2 R4
Authority state: OPERATIVE
Classification: DCSE_OPERATIONAL
Effective date: 2026-08-07

## Purpose

This directive operationalizes the v7.2 session-poller, wake, admission, execution, recovery, and receipting requirements for all governed DCSE participants and runtime surfaces.

## Binding Rules

1. DCSE SHALL use one neutral `DCSE_Universal_Dispatch_Controller` architecture. Provider-specific legacy pollers are `ROLLBACK_ONLY` unless expressly reclassified by DCS.
2. The active controller SHALL use a 60-second polling cadence unless an authorized runtime manifest changes that operational value without weakening a constitutional guarantee.
3. The lightweight Windows wake probe SHALL use the current five-minute target interval and SHALL check for actionable work or durable wake requests without launching a model when no work exists.
4. The controller SHALL remain eligible for not less than 60 continuous minutes of verified inactivity before transitioning to IDLE or SLEEP.
5. The inactivity window SHALL reset on actionable Control Plane activity, including task assignment, DCS instruction, actionable comment, review completion, result submission, handoff-ready event, recovery event, or explicit dashboard/manual wake.
6. Sleep is prohibited while claimable assignments, running workers, pending recovery, unconsumed wake requests, or actionable event/dispatch activity exist.
7. Autonomous execution SHALL preserve runtime admission evaluation, per-runtime authorization, atomic database claim, bounded execution, intermediate heartbeat for long-running work, stale/orphan recovery, Stop-Gate evaluation, immutable result evidence, and receipt submission.
8. Interactive non-claiming sessions SHALL NOT fabricate autonomous claims and SHALL identify their execution basis in receipts.
9. Wake requests SHALL be acknowledged before controller start and marked consumed only after verified controller start.
10. The poller and wake path SHALL preserve PS/PPR firewall controls, source authority, rollback, independent validation, and evidence requirements.
11. A discovered in-scope runtime defect SHALL follow `detect -> diagnose -> remediate -> test -> record -> continue` unless a legitimate Stop-Gate applies.
12. Reverse-chain diagnosis SHALL identify the first dependency not VERIFIED, repair the smallest bounded broken edge, forward-test the correction, and repeat until goal-state evidence closes.

## Required Cutover Evidence

The operative runtime cutover SHALL produce evidence for controller identity reconciliation, wake without unnecessary model launch, minimum 60-minute inactivity behavior, dispatch -> claim -> heartbeat -> receipt -> convergence -> Results Inbox, restart/orphan recovery, rollback, and final state reconciliation.

## Source Basis

Derived from DCSE Master Profile v7.2 R4 Sections 6, 18, 22, 31, 39, 40, and 42. Approved R4 SHA-256: `0590bb5349ac66f96ca757db628761fba18106da8e2a4e7a4c25c38bc2c08509`.
