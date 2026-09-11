# DCSE v7.2 Task-Routed Methodology Index

Status: OPERATIVE ROUTING INDEX
Authority source: DCSE Master Profile v7.2 R5 plus registered DCS express directives
Manifest role: routing aid only; does not independently create authority

## Active by DCS Directive DCS-DIR-20260906-001, amended by DCS-DIR-20260906-003

1. `DCSE-METH-EMP-001`
   - Path: `governance/v7.2/methodologies/DCSE_METH_DCS_Employment_Opportunity_Package_v1.md`
   - Current version: `v1.1`.
   - Trigger: DCS Employment, engagement tracking, employment package, recruiter package, contract, freelance, consulting, advisory, direct DCS business opportunity, revenue-path classification, resume/package baseline preservation, pipeline review, engagement closeout.
   - Relationship: modernizes legacy DCS Employment Command Center package methodology and adds the durable engagement-tracking architecture defined by `DCS-DIR-20260906-003`.
   - Current state: `ACTIVE_BY_DCS_DIRECTIVE_RUNTIME_RECONCILED`.

2. `DCSE-METH-MEDIA-THUMB-001`
   - Path: `governance/v7.2/methodologies/DCSE_METH_Thumbnail_Cover_Asset_Production_v1.md`
   - Current version: `v1.1`.
   - Trigger: thumbnail, video cover, poster frame, preview card, episode art, YouTube thumbnail, campaign video cover, website video card.
   - Relationship: specialized D18/D19 architectural workflow. Normal output is a human-review set of 3 to 5 materially distinct candidates, comparative selection matrix, human selection record, selected-candidate final asset, and manifest.
   - Current state: `ACTIVE_BY_DCS_DIRECTIVE_RUNTIME_RECONCILED`.

## Runtime Rule

D21 routing should load only the methodology required by the current task. A task may load both where, for example, an employment/consulting campaign includes a governed video asset.

The thumbnail/cover methodology is a workflow architecture. It does not require a standalone module or application in order to operate. Future automation may implement the workflow without changing its governing stages or human-selection gate.

All substantive-task closeout is also subject to `DCS-DIR-20260906-002`, the Completion Evidence Collector and Closure Integrity Directive.

## Promotion State

The two exact artifacts above are ACTIVE BY DCS EXPRESS DIRECTIVE and RUNTIME RECONCILED for immediate task routing. Formal D05 `ACTIVE_RATIFIED` status remains separately observable and is pending an attributable validation-integrity receipt. Under the 2026-09-11 Level 0 direction, functional independence is sufficient unless a controlling source expressly requires actor separation.

## Closeout Integrity

Before a routed methodology task is reported COMPLETE, the executor must backward-check claimed final state against required evidence, reconcile affected dependent artifacts, and present a Completion Evidence Collector packet for human review under `DCS-DIR-20260906-002`.

Structure Precedes Scale.
