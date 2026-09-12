# Vow N Go v7.2 Adaptive Build Handoff

Task ID: SC-VNG-V72-ADAPTIVE-HANDOFF-20260912-18
Parent task family: DCSE-PRODUCT-SPRINT-20260911
Lane: SC / Vow N Go
Entity: Sonly Consulting
Date: 2026-09-12
Status: ACTIVE HANDOFF / BUILD CONTINUATION
Authority: DCS Level 0 current-session direction
Receiving model posture: ANY AUTHORIZED MODEL OR AGENT OPERATING UNDER DCSE v7.2
Gate owner: DCS Level 0 for reserved decisions, promotion, destructive actions, production release, and public release

## 1. Handoff Purpose

This is a model-portable continuation handoff for Vow N Go.

The receiving model SHALL NOT assume it must restart the product lifecycle from intake.

At any point in the module or product build, an authorized model may enter, inspect the current verified state, adapt itself to DCSE v7.2, load only the task-relevant rule/doctrine packet, identify the current production stage and unresolved gates, then continue from the first material unresolved requirement.

The handoff is therefore a continuity contract, not a vendor-specific prompt.

## 2. Core Adaptation Rule

On receipt:

1. Preserve this Task ID unless a child task is required. A child task must record this parent ID.
2. Start from the operative v7.2 front door, not historical governance folders.
3. Treat existing Vow N Go v6.9 product artifacts as product lineage/source evidence, not current governance authority.
4. Inspect current code, data, deployment, evidence, and user-directed changes before proposing redesign.
5. Identify the current build stage.
6. Run a bounded gap analysis from the current state to the required next state.
7. Apply D20 Reuse Before Redesign.
8. Reuse, adapt, or compose validated CTJ and other DCSE patterns only where they fit Vow N Go's own product genome.
9. Preserve product-specific brand, user journey, privacy, data, role, and experience requirements.
10. Continue execution from the next unresolved gate rather than replaying already-validated work.
11. Preserve evidence, validation, rollback, and DCL state through every handoff.
12. Do not self-promote or claim release readiness without direct evidence.

## 3. Mandatory v7.2 Startup Route

The receiving model shall resolve current governance through:

1. `governance/v7.2/00_START_HERE.md`
2. `governance/v7.2/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`
3. `governance/v7.2/registry/DCSE_Doctrine_Index_v7-2.md`
4. `governance/v7.2/V7_2_CANONICAL_GOVERNANCE_PACKAGE_MANIFEST.json`
5. D22 for source authority/distribution
6. D21 for task routing and Doctrine Consideration Log
7. D20 for Product Assembly and Reuse Before Redesign
8. task-relevant D07/D08/D09/D10/D11/D12/D15/D16/D18/D19 as routed
9. `governance/v7.2/rule-foundry/DCSE_CONTENT_AND_ARTIFACT_GENERATION_STANDARD_v1.md`
10. `governance/v7.2/implementations/DCSE_SIX_PRODUCT_SEQUENTIAL_PARALLEL_PRODUCTION_PROFILE_20260911.md`
11. `governance/v7.2/execution/DCSE_GOVERNED_EXECUTION_AND_INTERACTION_STANDARD_v1.md`
12. `governance/v7.2/execution/DCSE_CONVERSATION_INTAKE_AND_CLOSEOUT_CONTRACT_v1.md`
13. `governance/v7.2/execution/DCSE_PLATFORM_EXECUTION_PROFILES_GITHUB_VERCEL_SUPABASE_v1.md`

PS doctrine D13/D14 is excluded unless a separately authorized PS route exists.

## 4. Vow N Go Verified Product Baseline

Current product source establishes Vow N Go as:

- a wedding planning assistant;
- a private event portal;
- a family/friend contribution surface;
- a living keepsake;
- an app-first experience;
- a product with bride/groom/planner administration;
- a product with public, moderated, and private publication states;
- a product using Supabase Auth and product-scoped authorization;
- a product with planning surfaces for tasks, events, vendors, budget, guests, music references, chapters, media moderation, guestbook, feedback, and related wedding coordination;
- a product intended to keep privileged authorization in PostgreSQL RLS rather than hidden client UI;
- a product designed to target accessibility standards, with formal audit still pending.

The product narrative/experience moves from proposal through wedding, honeymoon, and later keepsake chapters.

## 5. Current Verified Technical / Release State

Verified current state:

- existing Vow N Go source:
  `v6.9/05_Products/Family_Product_Line/Vow_And_Go/`
- source status: MVP integration candidate
- Supabase application support migration exists:
  `supabase/migrations/20260716190000_vow_go_application_support_v1.sql`
- RLS-backed application architecture exists
- earlier build approval and integration evidence exists:
  `_Tribunal_Inbox/TRIBUNAL_FAMILY_PRODUCT_LINE_VOW_GO_INTEGRATION_20260716_CHATGPT.md`
- digital-estate decision says Vow N Go is APP-FIRST and Wix is not presumed to be the primary application renderer:
  `_Tribunal_Inbox/2026-08-13_SC_DIGITAL_ESTATE_THREAD/TRIBUNAL_TOPIC_20260813_SC_WIX_HYBRID_ARCHITECTURE.md`
- Vercel inventory lists `vow-and-go-review` as a LIKELY family-product review asset, but exact source ownership remains unverified:
  `docs/operations/VERCEL_PROJECT_OWNERSHIP_20260813.md`

Existing release gates still include:
- real-user Auth validation;
- product-scoped role testing with real sessions;
- media upload / signed access / moderation / deletion;
- public/moderated/private transition tests;
- external planning-link privacy validation;
- feedback delivery;
- mobile / desktop / tablet / display testing;
- reduced-motion and keyboard testing;
- privacy / retention / content-release review;
- deployment validation;
- final DCS release approval.

## 6. Shared DCSE Production Spine

The receiving model shall locate Vow N Go on this spine:

`INTAKE -> PRODUCT GENOME -> TARGETED RETRIEVAL -> RULE PACKET -> COMMERCIAL DIRECTIONS -> CREATIVE DIRECTIONS -> CONVERGENCE -> ASSET PRODUCTION -> QA -> PACKAGE -> RELEASE DECISION -> LEARNING CAPTURE`

Equivalent v7.2 content/artifact sequence:

`GENOME -> RETRIEVE -> DIVERGE -> CHALLENGE -> CONVERGE -> PRODUCE -> INSPECT -> PACKAGE -> RELEASE -> LEARN`

Do not force the product backward to an earlier stage if that stage is already supported by evidence.

If current work enters at PRODUCT, UI, DATABASE, MEDIA, CAMPAIGN, PAYMENT, QA, or DEPLOYMENT, resolve the missing upstream prerequisites required for that specific work and continue.

## 7. Minimum Vow N Go Product Genome

Before downstream product/public artifact generation, verify or explicitly mark Unknown:

- product truth;
- intended customer/user groups;
- planning and keepsake jobs-to-be-done;
- promise;
- differentiators;
- offer and commercial model;
- evidence/proof;
- objections/trust concerns;
- visual personality;
- narrative/story;
- CTA;
- target channels;
- required application modules;
- required public/commercial artifacts;
- release gates;
- privacy and family/guest contribution boundaries;
- data ownership/retention model;
- role/permission model.

Do not invent missing Vow N Go facts merely to complete the genome.

## 8. CTJ Reuse Packet: Quality Floor, Not Clone Target

DCS has approved and locked the CTJ storefront / Product Card / cart candidate baseline.

Primary CTJ reuse reference:

`_Tribunal_Inbox/ctj-commercial-experience-20260912/01_DCS_LEVEL0_STOREFRONT_BASELINE_LOCK.md`

Candidate source:

`apps/ctj-commercial-experience-v1/`

Draft PR:
#95

Validated candidate head at lock:
`67a5feec4717286d73b00490bb3949c6f6d8077d`

Validated CI:
`34718056932` SUCCESS

Reusable CTJ patterns to evaluate for Vow N Go:

- product-genome -> product-card translation;
- showcase-quality website/product-page composition;
- richer product storytelling rather than thin feature tiles;
- a Product Card Package that carries copy, interaction, imagery, screenshots, B-roll, video/audio, artifacts, campaign derivatives, email, commerce, and fulfillment metadata;
- multi-product/cart pattern where Vow N Go has multiple sellable packages/add-ons;
- clear separation between customer payment submission and merchant verification;
- bundle/offer guidance without silent substitution;
- responsive and reduced-motion baseline;
- durable media manifest;
- static validation + human/browser review before release claims;
- visually distinctive product identity inside shared SC quality standards.

Do NOT copy CTJ:
- CTJ brand colors unless Vow N Go independently chooses them;
- CTJ compass/labyrinth identity;
- CTJ product names;
- CTJ pricing;
- CTJ curriculum structure;
- CTJ customer claims;
- CTJ interaction mechanics unrelated to Vow N Go.

Rule:
`REUSE THE SYSTEM QUALITY AND WORKFLOW. ADAPT THE EXPERIENCE TO THE VOW N GO GENOME.`

## 9. Vow N Go Uplift Target

Vow N Go shall be brought to or beyond the current CTJ production standard in all applicable dimensions:

### Product
- complete product genome;
- explicit roles/modules;
- coherent customer and administrator journeys;
- commercial packaging if applicable;
- clear offer/CTA architecture;
- portable artifacts or keepsake outputs where appropriate.

### Experience
- distinctive, emotionally credible wedding/keepsake visual language;
- not generic wedding-template UI;
- clear planning-to-memory narrative;
- mobile-first guest contribution experience;
- strong admin/planner usability;
- media-rich sections that remain performant and accessible;
- consistent design contract across public, private, admin, and keepsake surfaces.

### Technical
- verified Auth/RLS;
- role boundaries;
- private media handling;
- signed/authorized access;
- upload/delete/moderation paths;
- state persistence;
- error handling;
- responsive behavior;
- secret-safe client architecture;
- rollback/checkpoints;
- deployment/source ownership reconciliation.

### Production assets
- hero/cover assets;
- screenshots;
- product mockups;
- B-roll;
- ceremony/travel/keepsake visual categories;
- video story beats;
- approved music/audio references and rights posture;
- email assets;
- social/campaign derivatives;
- metadata and lineage.

### Commercial / operations
- package and pricing only from verified DCS direction;
- payment and entitlement architecture if included;
- support path;
- confirmation emails;
- privacy/terms/refund/retention requirements where applicable;
- analytics/measurement plan;
- fulfillment or customer onboarding.

## 10. Mid-Build Entry Protocol

A receiving model may enter at any module or stage.

It SHALL perform this compact adaptation sequence:

`READ HANDOFF -> VERIFY TASK ID -> READ v7.2 FRONT DOOR -> INSPECT CURRENT ARTIFACT -> IDENTIFY STAGE -> LOAD TARGETED DOCTRINE/RULES -> REUSE CHECK -> GAP CHECK -> EXECUTE -> VALIDATE -> RECORD -> HANDOFF/CLOSE`

Required current-state declaration:

- current module/artifact;
- current branch/repo/runtime;
- last verified evidence;
- current production stage;
- applied v7.2 rules;
- excluded rules;
- unresolved blockers;
- next executable action;
- DCS reserved gate, if any.

A model SHALL NOT discard working implementation merely because its local context started late.

A model SHALL NOT require prior chat memory when canonical source/evidence is available.

## 11. Technical Access and Secret Boundary

For Vow N Go privileged work:

- use verified Supabase project/access;
- no service-role key in client code;
- no passwords/tokens/MFA/private keys/connection strings in prompts, GitHub, Tribunal, logs, or handoff;
- inspect current schema/RLS before changing;
- preserve positive and negative access tests;
- use backup/checkpoint and rollback where applicable;
- read back all material writes.

Credential custody never creates decision authority.

## 12. Model Independence

This handoff applies to ChatGPT, Codex, Work, Claude, Gemini, Qwen, local models, or another authorized model/agent.

No model vendor is presumed to have special authority.

Every receiving model gets authority from:
- DCS direction;
- operative v7.2 controller;
- routed doctrine/rules;
- task scope;
- verified system access.

The model may adapt its implementation style to its capabilities, but may not weaken lane, security, evidence, promotion, or release controls.

## 13. Required DCL

The receiving model maintains:

Applied:
- task-relevant v7.2 doctrines;
- active capability modules;
- Vow N Go product sources;
- verified reusable patterns;
- current user/DCS directives.

Excluded:
- unrelated doctrines;
- PS doctrine unless separately authorized;
- unrelated product-specific rules;
- secrets.

Missing:
- required inputs not yet verified.

Contradictions:
- source conflicts;
- stale product truth;
- code/runtime mismatch;
- deployment ownership mismatch;
- data/schema mismatch.

Validation:
- tests run;
- browser/runtime checks;
- RLS/access checks;
- asset/content inspections;
- evidence references.

Exit:
- current achieved state;
- unresolved findings;
- rollback;
- next action;
- DCS gate owner.

## 14. Completion Standard

Do not report Vow N Go COMPLETE because code exists or a deployment returns 200.

Completion must backward-chain to:
- requested outcome;
- validated product/module behavior;
- access/security tests where relevant;
- browser/runtime evidence;
- reconciled source/deployment/database state;
- material asset/content QA;
- unresolved findings disclosed;
- promotion/release status accurately stated;
- DCS closeout when required.

## 15. Immediate Receiving-Model Instruction

Continue Vow N Go from its actual current state.

First produce a CURRENT-STATE + GAP MATRIX against:
1. the verified Vow N Go baseline;
2. the operative v7.2 production spine;
3. the applicable CTJ quality/reuse patterns;
4. the user's current Vow N Go changes.

Then execute the highest-value unblocked gap.

Do not restart the product.
Do not clone CTJ.
Do not wait for another model merely because prior work was performed elsewhere.
Do not claim production readiness without evidence.

Structure Precedes Scale.
