# CTJ Agentic Product-Suite Restructure Plan

**Task ID:** SC-CTJ-AGENTIC-SUITE-ARCH-20260922-01  
**Lane / Entity:** Sonly Consulting / Critical Thinker's Journey  
**Governance baseline:** DCSE v7.3 operative package  
**Status:** Planning and evidence review complete; implementation and deployment not authorized  
**Handoff ID:** SC-CTJ-HO-20260922-01

## Executive decision

Do not automate additional CTJ products from the current Netlify Capstone build. It contains reusable visual and interaction ideas, but it is not a dependable parent template and it does not match the attached expected module.

Establish a governed CTJ Family Shell, product manifest schema, reusable feature modules, and acceptance-test contract first. Treat the product's content and scoring rules as versioned data rather than copying and editing large HTML files. Use Heroku as the proposed branded web-application host, subject to a separate deployment approval, while keeping product binaries in object storage and canonical source in GitHub.

## Verified evidence

### Live deployment

- The supplied post-checkout URL resolves to **The Critical Thinker's Journey — Unified Edition**.
- The live success page identifies the downloadable product as **The Critical Thinker's Journey: A Unified Path v1.0** and launches a four-stage Capstone experience.
- The live app exposes internal language to the buyer, including `public.sc_ctj_orders`, `Registered`, and `Version 3.0-CAPSTONE-CANDIDATE`.
- A Netlify badge is visibly injected at the lower-right corner.
- A Back control exists on the intake and scenario pages, but it is not a persistent navigation control. On the long scenario page it is at the bottom after seven large response sections; on intake it can appear clipped beneath the top shell. The user's experience of “no back button” is therefore a valid discoverability defect, not proof that the control is absent from the code.
- Dictation uses non-continuous, non-interim recognition and ends when the recognition session stops. This explains why natural pauses terminate dictation.
- The success page displays checkout/session and customer details more prominently than necessary. These should be masked or removed after server-side verification.

### Attached artifacts

- The attached expected HTML module contains the Strategic Clarity Assessment and Parts 1–3.
- The downloadable ZIP instead contains the Capstone app. Its README also references files or directories that are absent from the package.
- The package includes internal or redundant customer-facing artifacts that should not be in the final delivery ZIP.
- The standalone Quick Start has broken references and does not provide a dependable launch route.
- The terms, support, and refunds routes previously referenced by product material returned 404 and must not be published until valid governed destinations exist.

### Governance

- GitHub repository `sonlyconsulting-ctrl/DCSE-Command-Post` was read successfully at main head `a82b7770cc89643c2c0a0925da7f880715b91979`.
- The operative package designates DCSE v7.3 as active and carries forward the v7.2 R5 substantive controller.
- D20 requires a product start gate, search/reuse decision, build, test, package, promote, deploy, and reusable-pattern capture.
- D22 places canonical source in GitHub, structured runtime state in Supabase, evidence in the Tribunal, binaries in object storage, and secrets in a vault.

## Product-definition decision gate

The product name **Unified Edition** currently means two incompatible things:

1. The attached expected module: SCA plus Parts 1–3 in one product.
2. The deployed application: a four-stage Capstone synthesis product.

Automation must pause until this is resolved. Recommended portfolio definition:

- **SCA:** diagnostic entry product.
- **Part 1 / Part 2 / Part 3:** full curriculum products.
- **Unified Edition:** Capstone synthesis with an abbreviated standalone intake and optional import of prior CTJ history.
- **Complete Keeper Collection:** SCA + Parts 1–3 + Unified Edition.

This preserves a distinct role for every SKU and avoids making Unified Edition and the Complete Keeper Collection duplicates. If the owner instead decides that Unified must contain the full SCA and Parts 1–3, the Collection's scope, price, and value proposition must be revised before implementation.

## Target product architecture

### Fixed family system

Every product inherits the same:

- CTJ emblem and Sonly Consulting attribution
- header height, responsive behavior, and safe areas
- persistent Back, Home, Save status, progress, and accessibility controls
- typography scale, spacing grid, color tokens, focus states, and form behavior
- support, privacy, terms, refunds, version, and copyright footer structure
- autosave, export, voice, validation, error, and recovery patterns
- completion handoff and product-family navigation
- production telemetry and privacy rules

Production pages must not expose candidate labels, database table names, raw session identifiers, internal ledger language, or hosting-provider badges.

### Product-specific expression

Each product may uniquely define:

- approved hero artwork and accent token
- product name and subtitle
- opening mission brief
- curriculum, assessment, or scenario sequence
- prompt and question data
- scoring or synthesis rules
- prescribed recommendations and completion artifact
- optional product capabilities declared in its manifest

Uniqueness comes from governed content, purpose, imagery, and accent—not from rebuilding navigation or accessibility behavior for each product.

### Product manifest

Create one validated `product.manifest.json` per SKU with fields for identity, lifecycle status, version, product code, routes, modules, content-pack version, artwork references, capabilities, output modes, legal/support route references, package inventory, and acceptance criteria.

The builder must reject missing routes, duplicate product codes, unapproved content versions, broken asset references, candidate status in a production build, and incompatible capabilities.

### Shared packages

- CTJ design tokens and artwork contracts
- application shell and navigation
- persistence and history import
- voice capture with continuous/interim behavior and explicit pause/resume/fallback controls
- assessment and synthesis engine
- export and completion artifacts
- accessibility utilities
- packaging, checksum, and QA evidence generation

The assessment engine must not reproduce the current weighted-percentage calculation until the scoring model is formally approved. Multiplying already-normalized percentages by 1.2 and 1.5 and then capping at 100 inflates Parts 2 and 3 and can distort diagnostic thresholds.

## Heroku deployment adjustment

Heroku is the proposed host for the branded application and server-side orchestration—not the canonical repository and not the durable binary store.

Proposed topology:

- **GitHub:** approved source, schemas, manifests, tests, release metadata
- **Heroku:** branded CTJ web application, Stripe session verification, entitlement API, orchestration, and approved production release
- **Custom domain:** a governed Sonly Consulting subdomain, with TLS enabled before public cutover
- **Supabase/Postgres:** entitlement, progress, consent, and structured runtime state with row-level controls
- **Object storage:** signed delivery of ZIP, PDF, image, and export binaries
- **Vault/config vars:** Stripe, Gemini, Qwen, and other runtime credentials; never client-side or committed to Git
- **Tribunal/evidence store:** decision records, test evidence, release receipts, and rollback references

Heroku supports custom domains, automated certificate management, and API-driven app setup. Its dyno filesystem is ephemeral, so durable packages and user-generated exports must not rely on local dyno disk.

Migration sequence:

1. Freeze the current Netlify build as evidence; do not use it as the generator parent.
2. Resolve the Unified-versus-Collection product decision.
3. Approve the manifest and family-shell contracts.
4. Build a local/reference implementation and a Heroku review app.
5. Correct the success page, package inventory, navigation, voice experience, and legal/support routes.
6. Validate Stripe verification, entitlements, signed downloads, and recovery behavior without exposing sensitive identifiers.
7. Run functional, visual, accessibility, security, responsive, offline/package, and cross-browser acceptance tests.
8. Obtain owner acceptance, then separately authorize production cutover and Netlify retirement/redirect.

## Bounded agentic build pipeline

1. **Intake agent:** validates the product brief and creates a draft manifest.
2. **Content agent:** assembles only approved, versioned content packs.
3. **Composition agent:** applies the shared shell and product-specific artwork/tokens.
4. **Validation agent:** runs schema, link, navigation, scoring, voice, accessibility, responsive, and visual-regression tests.
5. **Packaging agent:** creates only approved customer deliverables, manifests, hashes, and release metadata.
6. **Evidence agent:** records results and prepares the promotion packet.

No agent may approve scoring, invent legal language, expose secrets, change SKU scope, promote a candidate, or deploy to production. Those are explicit human/governance gates.

## Minimum acceptance contract

- Correct product launches from the post-purchase page.
- Persistent and keyboard-accessible navigation is visible at every step.
- Progress survives refresh and supports deliberate reset/recovery.
- Dictation tolerates natural pauses, clearly indicates state, and has typed fallback.
- All legal/support links resolve to approved branded pages.
- No provider badge, candidate label, internal table name, raw session token, or unnecessary buyer data appears.
- Text and controls meet WCAG 2.2 AA expectations, including focus, contrast, zoom, reduced motion, and screen-reader labeling.
- Every package matches its manifest and contains no internal design, test, or storefront files.
- The downloaded/local product remains usable according to its declared offline contract.
- Scoring and prescriptions have unit tests with approved fixtures and boundary cases.
- The product is tested at mobile and desktop sizes and in current supported browsers.

## Exit criteria for the next implementation phase

- CTJ product-definition decision recorded.
- Canonical source repository and branch confirmed.
- Family shell, manifest schema, and design-token contract approved.
- SCA question set and scoring model designated as canonical.
- Legal/support destination owners and URLs approved.
- Heroku, Supabase, object-storage, Stripe, DNS, and secret-management authority confirmed.
- Reference product passes the acceptance contract in a review environment.
- Owner grants a separate promotion/deployment authorization.

## Evidence closeout

**Verified:** live mismatch, Netlify badge, Capstone structure, buried Back control, dictation behavior, package mismatch, broken package references, v7.3 governance authority.  
**Likely:** Netlify was selected to make the module directly accessible as an app; no decision record proving that motive was found.  
**Unknown:** correctness of live entitlement/receipt claims, production data controls, approved legal copy, final SKU definition, and Heroku account/DNS authority.

No deployment, repository mutation, credential handling, DNS change, or production write was performed during this review.
