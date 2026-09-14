# CTJ Pricing Methodology Reuse Evidence Record

**Record ID:** DCSE-KNOW-CTJ-PRICE-REUSE-20260914  
**Date:** 2026-09-14  
**Status:** VERIFIED SOURCE EXTRACTION / REUSABLE METHODOLOGY DERIVATION  
**Authority:** DCS Level 0 direction to locate actual CTJ pricing evidence and make the methodology reusable  
**Derived Methodology:** `DCSE-METH-PRICE-001`

## Verified CTJ source package

The reusable methodology was derived from the actual CTJ commercial packaging package, not from conversational memory.

Primary sources:

1. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/00_PACKAGE_INDEX.md`
   - establishes packaging, pricing, payment selection, verification, fulfillment, and confirmation as one customer journey;
   - records the locked commercial packaging baseline and DCS Level 0 gate.

2. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/01_PRODUCT_PACKAGING_AND_PRICING.md`
   - states the central principle that pricing and packaging are one architecture;
   - ties price to the product ladder;
   - demonstrates value-ladder construction, bundle math, membership separation, market anchoring, cost discipline, contradiction reconciliation, and promotional-entry logic.

3. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/06_FRONTIER_MODEL_PRICING_BENCHMARK.md`
   - demonstrates use of an external consumer price cluster as a positioning anchor;
   - explicitly distinguishes a reference anchor from an equivalence claim;
   - preserves cost uncertainty despite low marginal model/compute expense.

4. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/07_FINAL_PRICING_DISPOSITION.md`
   - records the DCS-locked pricing ladder;
   - demonstrates bundle/suite comparisons;
   - defines material repricing triggers;
   - separates product value from open-source/local inference cost.

5. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/08_CTJ_INTRO_TRIO_CAMPAIGN_BRIEF.md`
   - demonstrates promotion as a distinct commercial architecture;
   - separates first-time promotional price from evergreen product value;
   - demonstrates campaign eligibility and free-lead-asset separation.

6. `_Tribunal_Inbox/ctj-commercial-packaging-20260912/09_DCS_LEVEL0_PACKAGING_LOCK.md`
   - establishes the working commercial baseline;
   - defines lock effect, material reopen triggers, exclusions, and superseded prior pricing assumptions.

## Related v7.2 rule dependency

`governance/v7.2/rule-foundry/DCSE-RULESET-17-ECONOMIC-COST-TTM-v1.json`

Relevant candidate rule:
- `ECON-PRICE-001`: a proposed sell price or tier requires sufficient cost/value inputs or must return `HOLD_FOR_COST_VALUE_INPUTS`.

The Wave 2 validation report explicitly states that Rule Set 17 commercial pricing/cost formulas remain validating until product-specific cost/value inputs are supplied.

Therefore this reuse package promotes a **methodology**, not a deterministic universal pricing formula.

## Reusable elements extracted

Verified reusable patterns:
- pricing and packaging treated together;
- price ladder mirrors product/value ladder;
- explicit product-role analysis before price;
- current-state/catalog contradiction review;
- standalone, bundle, promotional, premium, and suite comparisons;
- bundle savings math;
- cheapest evergreen equivalent-path comparison;
- promotional-path comparison;
- external market anchor used as reference, not equivalence;
- operating-cost discipline;
- ownership/membership separation;
- promotional eligibility treated separately from evergreen value;
- DCS approval/lock;
- material repricing triggers;
- exclusions separating pricing approval from release/deployment/payment activation.

## CTJ-specific elements explicitly not generalized

Do not reuse without new evidence:
- CTJ dollar amounts;
- CTJ product names;
- Discover / Practice / Prove / Integrate role labels as mandatory labels;
- the $20 premium-AI anchor as a current universal reference;
- CTJ bundle names;
- CTJ first-purchase promotion;
- CTJ Keeper terminology where another product uses a different ownership model;
- CTJ Wix/catalog facts;
- CTJ payment identities;
- CTJ-specific product contents.

## First reuse target

Vow & Go is designated as the first cross-product application.

Success requires the methodology to produce a pricing recommendation from Vow & Go-specific evidence without importing CTJ prices or unsupported market claims.

**Structure Precedes Scale.**
