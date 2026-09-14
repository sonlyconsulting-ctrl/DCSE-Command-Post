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
   - Current state: `ACTIVE_RATIFIED / ACTIVE_BY_DCS_DIRECTIVE_RUNTIME_RECONCILED`.

2. `DCSE-METH-MEDIA-THUMB-001`
   - Path: `governance/v7.2/methodologies/DCSE_METH_Thumbnail_Cover_Asset_Production_v1.md`
   - Current version: `v1.1`.
   - Trigger: thumbnail, video cover, poster frame, preview card, episode art, YouTube thumbnail, campaign video cover, website video card.
   - Relationship: specialized D18/D19 architectural workflow. Normal output is a human-review set of 3 to 5 materially distinct candidates, comparative selection matrix, human selection record, selected-candidate final asset, and manifest.
   - Current state: `ACTIVE_RATIFIED / ACTIVE_BY_DCS_DIRECTIVE_RUNTIME_RECONCILED`.

## Active by DCS Express Direction 2026-09-14

3. `DCSE-METH-PRICE-001`
   - Path: `governance/v7.2/methodologies/DCSE_METH_Product_Pricing_Packaging_v1.md`
   - Current version: `v1.0`.
   - Trigger: product pricing, packaging, commercial ladder, bundle pricing, launch pricing, promotional pricing, repricing review, product-card commercial architecture, or a request to apply the CTJ pricing strategy to another product.
   - Relationship: extracts the reusable analytical method proven in the locked CTJ commercial packaging package while explicitly excluding CTJ-specific dollar values and preserving Rule Set 17's product-specific cost/value input requirement.
   - Current state: `ACTIVE_BY_DCS_EXPRESS_DIRECTION_FOR_ANALYTICAL_REUSE / DETERMINISTIC_FORMULA_NOT_PROMOTED`.
   - First cross-product validation target: Vow & Go.

## Runtime Rule

D21 routing should load only the methodology required by the current task. A task may load both where, for example, an employment/consulting campaign includes a governed video asset.

The thumbnail/cover methodology is a workflow architecture. It does not require a standalone module or application in order to operate. Future automation may implement the workflow without changing its governing stages or human-selection gate.

All substantive-task closeout is also subject to `DCS-DIR-20260906-002`, the Completion Evidence Collector and Closure Integrity Directive.

## Promotion State

The two previously ratified artifacts remain ACTIVE BY DCS EXPRESS DIRECTIVE and RUNTIME RECONCILED for immediate task routing. Both exact v1.1 artifacts are ACTIVE_RATIFIED under D05 following validation-integrity receipt `DCSE-VAL-EMP-THUMB-20260911-001`. `DCSE-METH-PRICE-001` is separately active for analytical reuse by DCS express direction dated 2026-09-14; it is not yet a promoted deterministic pricing formula, and Rule Set 17's product-specific cost/value input gate remains controlling. Functional independence was applied under DCS-DIR-20260911-001; post-ratification integrity confirmed that only lifecycle metadata changed after the frozen-candidate validation.

## Closeout Integrity

Before a routed methodology task is reported COMPLETE, the executor must backward-check claimed final state against required evidence, reconcile affected dependent artifacts, and present a Completion Evidence Collector packet for human review under `DCS-DIR-20260906-002`.

Structure Precedes Scale.
