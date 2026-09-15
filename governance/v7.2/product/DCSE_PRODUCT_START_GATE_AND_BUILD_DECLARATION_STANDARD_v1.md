# DCSE Product Start Gate and Build Declaration Standard v1

**Status:** OPERATIVE upon Level 0 promotion  
**Authority:** DCS Level 0  
**Parent methodology:** D20 Product Assembly Methodology  
**Related doctrine:** D07, D08, D09, D10, D11, D12, D18, D19, D21, D22  
**Escalation owner:** DCS-E / DCS Level 0 as applicable

## 1. Purpose

No product/task build should discover essential identity, brand, media, destination, commercial, packaging, dependency, or acceptance decisions after implementation has begun. This standard consolidates existing upstream requirements into one deterministic start gate.

## 2. Forward-chain start declaration

Before material build work, resolve and record:

### Governance and ownership
- Task ID and parent Task ID when applicable;
- entity/lane and confidentiality;
- product/project ID and canonical repository;
- Master Profile/governance version;
- applicable doctrine/methodology;
- authority holder and reserved decisions.

### Build mode, baseline, and preservation
- work mode: NEW_BUILD | MODIFY | PACKAGE | CAMPAIGN | HOTFIX | MIGRATION | REVIEW;
- exact starting branch/commit/version or approved source baseline;
- current production/release state when one exists;
- approved elements that SHALL be preserved unless specifically changed;
- prohibited changes and known invariants;
- supersession/replacement target when the task replaces an existing artifact;
- reusable prior architecture, content, brand, components, media, or workflows already searched.

### Product definition
- product name and purpose;
- audience/persona(s);
- problem/outcome;
- product/package/SKU and pricing state when commercial;
- intended delivery/fulfillment model;
- success metric.

### Customer/user journey and critical path
- intended user entry point;
- primary user/customer journey;
- critical path that must work at release;
- key pages/screens/states or experience stages;
- primary failure/recovery path;
- operator/admin journey when material;
- accessibility-sensitive interactions when material.

### Destination and URL
- primary destination;
- intended public/internal URL, route, domain, or canonical slug;
- Development/Preview/Production URL states when applicable;
- canonical host and redirect rules;
- platform/hosting architecture;
- CTA/conversion action;
- checkout/payment/access handoff when applicable;
- contact path;
- redirect/canonical-host requirements when applicable.

A URL may be `RESERVED/TBD_BY_DCS_E` only when the build does not require a routable destination yet. Public-release work may not reach release readiness with URL/destination unresolved.

### Brand and persona readiness
- approved entity/product logo/wordmark where applicable;
- palette;
- typography;
- voice/tone;
- visual theme/style;
- current product/persona images;
- backgrounds/textures/environment images;
- source/reference files;
- approved current image-use set;
- intended usage mapping for primary assets: hero, persona, background, thumbnail, social, product card, packaging, video, or other defined role;
- prohibited/cross-entity elements;
- accessibility/contrast requirements.

### Media and asset readiness
- `DCSE_MEDIA_ASSET_MANIFEST.json`;
- canonical binary storage;
- asset IDs and hashes;
- rights/license/release status;
- source/provenance;
- permitted agent/model access;
- output/derived-asset destination;
- required aspect ratios, dimensions, duration, resolution, file formats, or delivery variants when known;
- archive/retention requirement for source and final media.

### Deliverables, packaging, and fulfillment
- exact deliverable inventory expected from the task;
- file types/formats and naming requirements;
- package/folder/ZIP structure when applicable;
- customer-facing versus internal-only files;
- download/access mechanism;
- confirmation, receipt, onboarding, or fulfillment behavior;
- version/edition labeling;
- packaging QA and completeness criteria.

### Content and claims
- core message/value proposition;
- approved factual claims/evidence basis;
- required copy/content inputs;
- content/source-of-truth location;
- material approved wording that must be preserved;
- SEO/AEO/GEO metadata requirements when web/discoverable;
- legal/compliance disclaimers when applicable.

### Architecture, dependencies, and integrations
- runtime/deployment surface;
- database/storage dependencies;
- authentication/access;
- integrations/APIs/plugins;
- environment-variable names without values;
- secret-store location;
- browser/server boundary;
- upstream dependencies that can block the task;
- downstream products/workflows affected by the change;
- shared components or schemas affected;
- migration/backward-compatibility requirement when applicable.

### Constraints and operating envelope
- target completion/release date or deadline when material;
- time-to-market priority;
- spending/budget boundary;
- platform quotas/rate limits;
- performance/capacity assumptions;
- known technical or vendor constraints;
- required offline/local/cloud execution boundaries.

### Measurement and quality
- analytics/events/measurement plan when applicable;
- accessibility target;
- device/browser/platform targets;
- performance expectations;
- QA/compliance checks;
- acceptance criteria;
- evidence destination;
- promotion/release gate;
- rollback/recovery.

## 3. Reverse-chain completion test

Before build begins, ask:

> If the final product were presented for release now, what evidence, identity, brand, destination, asset, commercial, packaging, technical, dependency, or compliance information would be required to approve it?

Then reverse-map each required final-state condition to the earliest point at which it must be known. Any input that cannot be produced later without redesign, regeneration, re-editing, repackaging, data migration, customer-path change, or material rework belongs in the start declaration.

Also ask:

> What approved element could this task accidentally damage even if the requested change succeeds?

Those preservation constraints, dependencies, shared components, URLs, assets, integrations, and user journeys become explicit start-state invariants.

## 4. DCS-E escalation triggers

Trigger `DCS_E_PRODUCT_START_ESCALATION` when any required item is missing, contradictory, stale, or unverified and proceeding would force the builder/model to invent or materially assume it.

Mandatory escalation examples:

- no canonical product/project repository;
- no product identity or owning entity;
- no verified starting baseline for a modification/migration task;
- no definition of what approved material must be preserved;
- no brand palette/typography/voice where public branding is required;
- missing current persona/product images, backgrounds, or approved source/reference assets for a visual/media build;
- no asset manifest or unknown asset provenance/rights;
- no defined usage role for required persona/hero/background assets when the design depends on them;
- unresolved public URL/domain/route for a release-targeted web product;
- unclear Development/Preview/Production destination when the distinction affects execution;
- unclear CTA, package, price, checkout, fulfillment, or customer access for a commercial release;
- no deliverable/package inventory for a product intended for download, delivery, or fulfillment;
- conflicting product names/brands/repos;
- missing required platform/database/storage architecture;
- unresolved upstream dependency or material downstream impact;
- unclear public/private classification;
- required secret would have to enter a model-visible surface;
- PS/protected spill risk;
- no acceptance criteria, critical user journey, or release authority;
- deadline, budget, quota, or capacity condition materially changes the feasible architecture and has not been resolved.

## 5. Escalation behavior

On escalation:

1. do not fabricate the missing decision or asset;
2. preserve completed work that is not dependent on the missing input;
3. identify the exact missing prerequisite;
4. identify safe work that can continue;
5. route the missing decision/asset to DCS-E;
6. keep state `PARTIAL / START_GATE_BLOCKED` until resolved.

## 6. Reuse-before-redesign

The start gate must search approved prior product files, brand packs, persona assets, URLs, architecture, manifests, packages, customer flows, reusable components, and prior media before asking DCS-E to recreate them.

## 7. Required artifact

Every material product build SHALL create or update a machine-readable `DCSE_PRODUCT_START_DECLARATION.yaml` or equivalent project-manifest section.

The declaration SHALL identify unresolved fields explicitly. Absence of a field is not permission to infer it.

**Structure Precedes Scale. Product Identity Precedes Production.**
