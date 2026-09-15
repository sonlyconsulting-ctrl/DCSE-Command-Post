# DCSE Task Delegation Queue

This directory houses canonical task packets delegated to autonomous or pair-programming models under DCSE governance.

## Canonical Layout
- `tasks/README.md`: This execution directive and governance manual.
- `tasks/queue/`: Concrete task packets (`T-001.json`, `T-002.json`, etc.) ready or queued for evaluation.
- `tasks/operations/`: Operation schemas, reversibility definitions, and stage lifecycle rules.

## What to do

```bash
python -m dcse tasks
```

That prints every task, its reconciliation status, whether it is runnable, and whether it needs DCS approval.
The arrow (`->`) marks the next runnable task. A task with unmet dependencies or non-READY reconciliation status is blocked.

Open `tasks/queue/<id>.json`. Read all of it before touching anything, particularly `scope`, `forbidden`, and `acceptance`.

## Fields of Consequence

- **scope**: The only paths you may touch. Writes outside declared scope violate `GH-04`.
- **steps**: Ordered sequence of execution steps.
- **acceptance**: Machine-checkable commands and expected outputs. Paste actual output verbatim in your report.
- **forbidden**: Hard constraints based on past failure modes.
- **reconciliation**: State of human alignment (`READY`, `HOLD_DCS`, `STALE_RECONCILE`, `SUPERSEDED`, `BLOCKED`).
- **needs_approval**: Computed by rules, never asserted by the model.

## Task Status Summary

| Task ID | Reconciliation | Approval | Title | Disposition / Authority |
| :--- | :--- | :--- | :--- | :--- |
| `T-001` | `HOLD_DCS` | yours | Move ESCD validator out of build slot | Paused by DCS architectural directive on deployment |
| `T-002` | `READY` | auto | Write the five missing rule tests | Fully runnable; local test addition |
| `T-003` | `HOLD_DCS` | yours | Wire the deployment adapter | Paused by DCS architectural directive |
| `T-004` | `STALE_RECONCILE` | yours | Port v0.2 rules into register | Rules Engine promoted to OPERATIVE in ee9b0f2 |

## Verification Before Reporting

```bash
python -m dcse test
python -m dcse bench --against dcse/baseline.json
```
