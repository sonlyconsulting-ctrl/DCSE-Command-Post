# DCSE Methodology: Product Pricing, Packaging, and Commercial Value Architecture

**Document ID:** DCSE-METH-PRICE-001  
**Version:** v1.0  
**Effective Date:** 2026-09-14  
**Status:** ACTIVE BY DCS EXPRESS DIRECTION FOR ANALYTICAL REUSE / NOT A PROMOTED DETERMINISTIC PRICE FORMULA  
**Classification:** INTERNAL  
**Lane:** DCSE / SC / reusable across approved product lanes  
**Parent Authority:** DCSE Master Profile v7.2 R5, OPERATIVE  
**Authority Holder:** DCS Level 0  
**Source Lineage:** CTJ commercial packaging/pricing package dated 2026-09-12; Rule Set 17 Economic, Cost and Time-to-Market; DCS express direction on 2026-09-14 to locate the actual CTJ pricing evidence and make the methodology reusable.  
**Purpose:** Reuse the CTJ-proven pricing strategy process across DCSE products without copying CTJ-specific prices, product roles, bundles, or market claims into another product.

## 1. Governing Distinction

This methodology governs **how to perform pricing and packaging analysis**.

It does not establish a universal price formula.

The following remain product-specific and must be sourced for each product:
- product scope and validated feature set;
- target buyer and use case;
- role in the product ladder;
- value delivered;
- ownership/access model;
- current and expected operating costs;
- support/fulfillment burden;
- payment/provider costs;
- market reference points;
- bundle relationships;
- promotional eligibility;
- legal/compliance constraints;
- DCS commercial intent.

Rule Set 17 remains controlling for deterministic promotion: a sell price or tier may not be treated as formulaically determined until sufficient product-specific cost/value inputs exist.

## 2. CTJ-Derived Core Principle

**Pricing and packaging are one architecture.**

The price ladder should tell the same story as the product ladder.

CTJ proved the reusable pattern by aligning distinct product roles to a coherent commercial progression rather than assigning isolated prices independently.

For a new product, first identify:
1. what role the product plays;
2. where it sits in the buyer journey;
3. whether it is entry, core, paired, premium, capstone, suite, membership, or promotional;
4. what adjacent offers it must not undermine.

Do not set price before the product's commercial role is understood.

## 3. Required Pricing Evidence Packet

Before recommending a price, assemble a product-specific evidence packet.

### 3.1 Product Facts
- canonical product identity;
- verified scope/features;
- current state and release posture;
- ownership/access model;
- delivery/fulfillment method;
- validated product role;
- related products and bundles;
- current approved price, if any;
- current contradictions or catalog drift.

### 3.2 Buyer and Value Facts
- target buyer;
- buyer problem/job-to-be-done;
- practical outcome;
- personal/business value;
- differentiation;
- substitute/alternative options;
- likely purchase context;
- expected commitment level.

### 3.3 Cost and Margin Inputs
Use actual or explicitly labeled estimated values for:
- hosting/platform;
- payment fees;
- support time;
- manual verification/fulfillment;
- maintenance/updates;
- authentication/storage;
- analytics;
- model/API usage where applicable;
- refunds/chargebacks;
- customer service;
- content refreshes;
- other variable or fixed product costs.

Low marginal compute cost does **not** mean total commercial cost is zero.

### 3.4 Market Evidence
Use current external reference points where they help establish buyer expectations.

Market evidence may include:
- direct competitors;
- adjacent products;
- category norms;
- familiar consumer price anchors;
- subscription reference points;
- substitute spend.

A market anchor is a **reference point**, not an equivalence claim.

Do not say two products are equivalent merely because they share a price point.

## 4. Build the Product/Value Ladder

Map the product into a ladder before evaluating exact price.

Typical commercial roles include:
- entry / discover;
- learn / core;
- practice;
- prove;
- pair / bundle;
- integrate / premium;
- suite / complete collection;
- membership / continuing value;
- promotional acquisition asset.

The names are not mandatory. The role logic is.

The ladder should make clear:
- why a lower-priced product exists;
- why a buyer would step up;
- why a bundle is economically coherent;
- why the premium product remains premium;
- why the complete collection/suite has a defensible anchor.

## 5. Generate Pricing Alternatives

Do not stop at the first plausible number.

Generate at least three viable structures when the decision is material.

Examples:
- conservative entry / faster conversion;
- balanced/value-aligned;
- premium/value-maximizing;
- one-time ownership;
- bundle-led;
- tiered;
- subscription/membership supplement;
- launch promotion plus evergreen baseline.

Each alternative must state:
- proposed price(s);
- rationale;
- product-role fit;
- buyer-friction implications;
- margin/cost implications where known;
- bundle effects;
- positioning implications;
- risks;
- required assumptions.

## 6. Bundle and Value Mathematics

For every proposed bundle, compute rather than imply.

Required calculations where applicable:

### 6.1 Standalone Sum
`standalone_sum = sum(individual component prices)`

### 6.2 Bundle Savings
`bundle_savings = standalone_sum - bundle_price`

### 6.3 Bundle Discount Percentage
`bundle_discount_pct = bundle_savings / standalone_sum`

### 6.4 Cheapest Evergreen Equivalent Path
Identify the least-expensive non-promotional combination of existing offers that reproduces the bundle's included value.

`evergreen_savings = cheapest_evergreen_equivalent - bundle_price`

### 6.5 Promotional Equivalent Path
If a launch/intro promotion exists, compare the permanent suite/bundle against that path too.

A bundle should not accidentally cost more than buying its components separately unless there is a verified additional value reason.

Discounts should be intentional and material enough to communicate the intended product-role relationship.

## 7. Market-Anchor Validation

Use market anchors after the internal product/value structure is understood.

Required interpretation:
- What customer expectation does the anchor establish?
- Is it direct or adjacent?
- Is it current?
- Is the comparison legitimate?
- Does it support or challenge the proposed price?
- Would using it publicly create an equivalence claim that should be avoided?

Do not reprice merely because a competitor changes a price or introduces a new tier.

External changes become relevant only when they materially change customer expectations or positioning.

## 8. Ownership, Membership, and Access Separation

When a product can be purchased outright and also participates in membership/access programs, keep the economic roles distinct.

Evaluate:
- owned/Keeper-style purchase;
- ongoing access;
- member-only continuing value;
- optional expansions;
- variable-cost AI capability;
- what survives membership cancellation;
- whether owners are unfairly penalized by later membership.

Do not redesign an existing membership program merely to force a product launch unless DCS explicitly directs it.

## 9. Promotional Architecture

Treat launch/intro pricing as a separate commercial object from the evergreen price.

For a promotion define:
- objective;
- eligible audience;
- normal standalone value;
- promotional price;
- absolute savings;
- percentage savings;
- eligibility rule;
- duration or first-purchase rule;
- operational enforcement method;
- customer-facing framing.

Do not use clearance framing for current strategic products unless the actual business intent is clearance.

A free acquisition asset must be treated as a distinct campaign artifact if it is materially different from the paid product.

Do not quietly redefine the paid product as free.

## 10. Contradiction and Catalog Reconciliation

Before finalizing price, compare the proposed architecture against the current live/commercial state.

Check for:
- inconsistent prices;
- bundle math errors;
- stale titles/slugs;
- missing products;
- obsolete product-role assumptions;
- conflicts with prior approved decisions;
- membership contradictions;
- fulfillment/payment contradictions.

Record contradictions explicitly.

Do not mutate storefront/catalog state merely because the analysis identified a mismatch. Catalog mutation is a separate governed action.

## 11. Recommendation Structure

A pricing recommendation should contain:

1. **Verified product state**
2. **Product-role / value ladder**
3. **Cost/value inputs**
4. **Market anchors**
5. **Pricing alternatives**
6. **Bundle mathematics**
7. **Promotional architecture**
8. **Risks and unknowns**
9. **Recommended launch/evergreen structure**
10. **What requires DCS approval**
11. **Implementation dependencies**
12. **Reopen triggers**

Separate:
- VERIFIED facts;
- LIKELY interpretations;
- UNKNOWN inputs;
- ASSUMPTIONS;
- RECOMMENDATIONS;
- DCS DECISIONS.

## 12. DCS Decision and Lock

A recommendation is not operative pricing until DCS approves it.

Once DCS locks the commercial baseline:
- preserve the approved ladder;
- preserve bundle math;
- preserve promotion logic;
- preserve exclusions;
- record the authority/decision;
- do not reopen because of minor market noise.

The lock does **not** automatically authorize:
- public release;
- payment-provider activation;
- storefront/catalog mutation;
- production deployment;
- membership redesign;
- destructive cleanup.

Those remain separate gates.

## 13. Material Reopen Triggers

Reopen pricing only when a material trigger occurs, including:
1. DCS changes commercial strategy;
2. actual unit economics materially weaken margin;
3. payment/support/hosting/model cost materially changes;
4. product scope materially expands or contracts;
5. membership/ownership economics materially change;
6. payment architecture materially changes;
7. legal/compliance requirements materially alter the offer;
8. validated customer/market evidence indicates material mispricing;
9. market reference pricing shifts enough to change buyer expectations materially.

Do not repeatedly reprice based on small competitor movements.

## 14. Reuse Rule

When this methodology is invoked for a new product:
- reuse the **method**;
- refresh the **evidence**;
- recompute the **math**;
- regenerate the **alternatives**;
- preserve the **DCS approval gate**.

Never carry CTJ-specific dollar amounts, role labels, bundle names, consumer-AI benchmarks, or promotional assumptions into another product unless independently supported for that product.

## 15. Vow & Go First Cross-Product Application

Vow & Go is the first designated cross-product validation case for this methodology.

The Vow & Go pricing run should:
1. resolve the current Vow & Go product state;
2. gather verified scope/assets/tasks/deployment evidence;
3. identify its commercial role and campaign goal;
4. assemble product-specific cost/value inputs;
5. refresh relevant market anchors;
6. produce at least three pricing structures;
7. calculate bundle/promotion math where applicable;
8. separate facts, assumptions, unknowns, recommendations, and DCS decisions;
9. route the recommended price to DCS Level 0 for approval;
10. persist the approved decision as product state without treating the recommendation itself as operative.

This validation does not authorize Vow & Go public pricing or release by itself.

## 16. Outputs

Authorized analytical outputs include:
- Pricing Evidence Packet;
- Product/Value Ladder;
- Market Anchor Brief;
- Cost Input Matrix;
- Pricing Alternatives Matrix;
- Bundle Math Worksheet;
- Promotion Architecture;
- Pricing Recommendation;
- DCS Pricing Decision Record;
- Pricing Lock Record;
- Repricing Trigger Review;
- Product Card commercial data packet.

## 17. Exit Criteria

A pricing analysis is complete only when:
- canonical product scope is resolved;
- product role is explicit;
- material cost/value inputs are known or labeled UNKNOWN;
- market evidence is current enough for the decision;
- at least three viable alternatives were considered for material decisions;
- bundle math is correct;
- promotional logic is explicit;
- contradictions are recorded;
- recommendation is evidence-grounded;
- required DCS approval is clear;
- operative vs candidate state is not confused;
- material reopen triggers are documented.

**Structure Precedes Scale.**
