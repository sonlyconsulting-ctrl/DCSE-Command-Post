# DCSE Doctrine D20: Product Assembly Methodology

**Document ID:** DCSE-D20
**Version:** v7.0
**Created Date/Time:** 2026-07-25T23:00:00-04:00
**Last Doc Modified Date/Time:** 2026-07-29T18:07:30-04:00
**Status:** CANDIDATE PENDING DCS LEVEL 0 PROMOTION
**Promoted Source Input SHA-256:** 902EC78EA0184E8C1576BE5503EC216B5013C431F9B38DFD198795D3BDCE9B56
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D20_Product_Assembly_Methodology.md
**Doctrine Description:** The Product Assembly Methodology (D20) consolidates the end-to-end product build lifecycle from intake through deployment. Previously scattered across D05 (promotion gates), D06 (file system routing), D11 (HTML/Wix/App standards), and D07 (campaign distribution), no single doctrine governed how products get built, tested, packaged, and shipped. D20 fills that gap with a six-phase pipeline: Intake, Build, Test, Package, Promote, Deploy. The Test phase integrates the Live Preview Mandate (D21 Section 6) and cybersecurity baseline as non-negotiable gates.
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

## 1. Product Assembly as Consolidated Methodology

A "product" in DCSE is any deliverable that reaches a user, client, or public audience: web applications, Wix-embedded widgets, standalone HTML tools, dashboards, calculators, landing pages, API endpoints, packaged media, and branded content systems.

The product lifecycle was previously governed piecemeal:

- D11 defined how to build web products (iframe sandboxing, responsive layout, brand tokens).
- D05 defined how to release them (baseline/promotion gates, SHA-256 verification).
- D06 defined where to put them (14-directory layout, file routing, device governance).
- D07 defined how to distribute them (campaign channels, SEO/GEO/AEO standards).

D20 consolidates these into a single execution pipeline. Source doctrines retain their governance authority. D20 is the methodology that sequences the work.

---

## 2. Phase Definitions

### 2.1 Phase 1: Intake

Objective: Define exactly what product is being built, for which entity, under what constraints, before any code is written.

Inputs: Business objective, target entity, target users, technical constraints, timeline.

Steps:

1. Product Declaration: Define:
   - Product name and asset ID (per D06 naming: ENTITY_Description_YYYYMMDD).
   - Entity scope (SC, SS, TI, DCS). Single entity per product unless cross-entity authorization from DCS.
   - Product type: web app, Wix widget, standalone HTML, API endpoint, dashboard, calculator, landing page, packaged media.
   - Target platforms: desktop, tablet, mobile, embedded (Wix iframe).
   - Agentic level: Level 1 (Supervised), Level 2 (Semi-autonomous), Level 3 (Autonomous). Public-facing products restricted to Level 1.

2. Requirements Gathering:
   - Functional requirements: what the product does.
   - Non-functional requirements: performance, accessibility (WCAG 2.1 AA minimum), security, responsive breakpoints.
   - Brand requirements: entity palette (D09), font stack (D11 Section 4.1), voice/tone (D08).
   - Integration requirements: Supabase tables, API endpoints, Wix embedding, external services.

3. Doctrine Routing (DDR):
   - Run the Dynamic Doctrine Router (D21 Section 2) to identify all applicable doctrines for this product type and entity.
   - Log the doctrine set in the DCL.

4. SC Lane Assignment (if applicable):
   - SC products are assigned to their lane folder under DCSE_CP_Project (SC_CTJ, SC_Gov-OS, SC_TSL, etc.) per D06 Section 7.4.
   - New SC product lanes require D06 Section 10.3 onboarding before the lane is operational.

Outputs: Product Declaration Document, Requirements Specification, Doctrine Set (from DDR), Lane Assignment.

Quality Gate: No build proceeds without a completed Product Declaration. This is a stop-gate.

### 2.2 Phase 2: Build

Objective: Construct the product according to the requirements and applicable doctrine standards.

Inputs: Approved outputs from Phase 1.

Steps:

1. Architecture:
   - Define component structure. Composable, reusable components. Each component handles one concern.
   - State management: minimal and colocated. No global state unless architecturally justified.
   - Data flow: define the data contract between frontend and backend. All database access through backend APIs.

2. Frontend Build (D11 compliance):
   - Semantic HTML: use header, main, section, article, nav, footer. No generic div-only structures.
   - Responsive layout: Flexbox/Grid. No hardcoded pixel widths on main containers. Breakpoints:
     - Mobile Portrait: less than 480px
     - Tablet/Mobile Landscape: 481px-768px
     - Laptop: 769px-1024px
     - Desktop: greater than 1025px
   - Fluid typography: rem, em, vh, vw, clamp(). No fixed pixel font sizes.
   - Brand token stack (D11 Section 4.1):
     - Display Font: Cormorant Garamond, Georgia, serif
     - UI Labels: Barlow Condensed, Arial Narrow, sans-serif
     - Monospace: DM Mono, monospace
     - Colors: per entity palette from D09 Section 3
   - Animations: interruptible, wrapped in @media (prefers-reduced-motion: reduce).
   - Overflow: box-sizing: border-box globally. overflow-x: auto on containers at risk.

3. Wix Integration (if applicable, D11 Part 2):
   - iframe sandboxing: sandbox="allow-scripts allow-downloads allow-forms allow-same-origin"
   - postMessage protocol: explicit origin validation on both sides. Reject unverified schemas.
   - Dynamic height: no fixed heights. iframe sends height via postMessage, Wix container resizes.
   - Style parity: match Wix parent styles via CSS variable inheritance.

4. Backend Build (if applicable):
   - Supabase integration: RLS policies required. Public-safe anonymous keys only in browser code.
   - API design: RESTful endpoints with proper HTTP methods. Input validation at every boundary.
   - Error handling: structured error responses. No stack traces in production responses.

5. Content Integration:
   - Copy: entity voice/tone per D08.
   - Visuals: invoke D19 Visual Creation Pipeline if custom images needed.
   - Media: invoke D18 Media Production Pipeline if video/audio needed.
   - Em/en dash compliance: no em dashes or en dashes in HTML text, meta tags, or document markup (D11 Section 4.2).

Outputs: Working Product Build, Component Documentation, Integration Configuration.

Quality Gate: Build must compile/render without errors before advancing to Test phase. This is not sufficient for completion; it is the minimum bar for Test entry.

### 2.3 Phase 3: Test

Objective: Verify the product works correctly, looks right, is secure, and survives first human contact. This phase is non-negotiable.

Inputs: Working build from Phase 2.

THE LIVE PREVIEW MANDATE: Any product that can render in a browser MUST be previewed in a browser before being reported as complete. Type checking and test suites verify code correctness, not feature correctness. The product must pass the first human contact standard.

Steps:

1. Functional Testing (Golden Path):
   - Start the dev server or open the product in browser preview.
   - Walk through the primary user flow end to end.
   - Verify every interactive element responds correctly.
   - Verify data flows correctly (forms submit, API calls succeed, state updates).
   - Verify error states render correctly (invalid input, network failure, empty state).

2. Visual Testing:
   - Verify brand compliance: correct entity colors (D09), correct fonts (D11), correct voice/tone (D08).
   - Verify responsive layout at all four breakpoints (mobile, tablet, laptop, desktop).
   - Verify dark/light theme if applicable.
   - Verify animation behavior and reduced-motion compliance.
   - Capture screenshots as proof of preview.

3. Console and Network Testing:
   - Check browser console for errors, warnings, and deprecation notices.
   - Check network requests for failures, unexpected calls, and CORS issues.
   - Check server logs for errors and unexpected behavior.

4. Accessibility Testing:
   - Semantic HTML structure verified.
   - ARIA labels present on interactive elements.
   - Keyboard navigation works end to end.
   - Color contrast meets WCAG 2.1 AA (4.5:1 text, 3:1 large text/graphics).
   - Alt text present on all images.

5. Cybersecurity Testing (D21 Section 5):
   - Secrets Scan: no API keys, tokens, passwords, or connection strings in client code, comments, or debug output.
   - Input Validation: all user inputs validated at the boundary (type, length, format).
   - XSS Prevention: all rendered content sanitized. HTML entities escaped. URLs validated.
   - SQL Injection Prevention: parameterized queries only. No string concatenation of user input in queries.
   - CORS: explicit, restrictive policies. No wildcard origins in production.
   - Content Security Policy: headers present on all HTML pages.
   - Credential Isolation: public-safe anonymous keys only in browser code. Service role keys server-side only.
   - Pre-commit: scan staged files for credential patterns before any git push.
   - HTTPS: required for all production endpoints.
   - File Upload: validate type, size, content before processing (if applicable).

6. Entity Firewall Testing:
   - Verify no cross-entity references in content or code.
   - Verify GYTO suppression for public-facing products.
   - Verify PS content exclusion for non-PS products.
   - Verify internal metadata stripped from public-facing outputs.

Outputs: Test Report (all checks with PASS/FAIL), Screenshot Proof, Console/Network Logs, Cybersecurity Clearance.

Quality Gate: ALL tests must pass before advancing to Package. Any failure returns to Phase 2 for remediation. No exceptions. No "ship it and fix later."

### 2.4 Phase 4: Package

Objective: Prepare the tested product for promotion and deployment with proper metadata and registry entries.

Inputs: Test-passing build from Phase 3.

Steps:

1. File Organization:
   - Place product files in the correct D06 directory (07_Projects for active workspaces, or SC lane folder for SC products).
   - Apply D06 naming conventions to all files.

2. Asset Registry (15-Point):
   - Register every file in `dcse_asset_registry` with all 15 metadata elements.
   - Generate SHA-256 hash for each file.
   - Set lifecycle_status to "Review" (not Active until promoted).

3. Dependency Documentation:
   - List all external dependencies (npm packages, APIs, CDNs, tools).
   - List all doctrine dependencies (which doctrines governed this build).
   - List all integration points (Supabase tables, Wix embeds, external services).

4. Distribution Manifest:
   - Plain-text manifest listing all product files, their formats, sizes, purposes, and deployment targets.

Outputs: Packaged Product Directory, Asset Registry Entries, Dependency Map, Distribution Manifest.

Quality Gate: Asset registry entries must be confirmed in Supabase before promotion. Registry write failure triggers a stop-gate.

### 2.5 Phase 5: Promote

Objective: Move the product from candidate to active status through the D05 promotion protocol.

Inputs: Packaged product from Phase 4.

Steps:

1. Tribunal Submission:
   - Submit the product package to `05_Tribunal_Inbox` with the distribution manifest, test report, and cybersecurity clearance.

2. DCS Level 0 Review:
   - DCS reviews the submission, test results, and security clearance.
   - DCS may request changes (returns to Phase 2), approve (advances to Phase 6), or hold.

3. Promotion Execution (D05):
   - Status shifts from CANDIDATE to ACTIVE_RATIFIED.
   - Verification receipt generated with document ID, SHA-256 hash, ratification timestamp, and approver signoff.
   - Asset registry entries updated: lifecycle_status changes to "Active", promotion_status changes to "PROMOTED".

4. Baseline Capture (D05):
   - If this is a versioned product release, capture a baseline receipt in `06_Baselines` with SHA-256 hashes of all product files.

Outputs: Promotion Receipt, Updated Asset Registry, Baseline Receipt (if applicable).

Quality Gate: Only DCS Level 0 may ratify promotion. No automated promotion. No self-promotion by AI models.

### 2.6 Phase 6: Deploy

Objective: Ship the promoted product to its target platform and verify it works in production.

Inputs: Promoted product from Phase 5.

Steps:

1. Platform Deployment:
   - Web App: deploy to hosting platform. Verify HTTPS, CSP headers, CORS configuration.
   - Wix Widget: embed in target Wix page. Verify iframe sandboxing, postMessage protocol, dynamic sizing.
   - API Endpoint: deploy to server. Verify rate limiting, authentication, error handling.
   - Standalone HTML: publish to hosting or distribute via the defined channel.

2. Production Verification:
   - Run a subset of Phase 3 tests against the production deployment.
   - Verify the golden path works in production (not just staging/dev).
   - Check production console and network for errors.
   - Verify analytics hooks and metadata are active.

3. Post-Deploy Monitoring:
   - Set up error monitoring if available (console errors, API failures, performance degradation).
   - Define rollback procedure if production issues are discovered.

4. Campaign Integration (if applicable):
   - Hand off to D07 Campaign Governance for distribution across channels.
   - Invoke D18 Media Production Pipeline if launch media is needed.

Outputs: Production Deployment Record, Production Verification Report, Monitoring Configuration, Rollback Plan.

Quality Gate: Production verification must pass before the product is announced or distributed. Deployment without verification is a governance violation.

---

## 3. Trigger Mechanism

### 3.1 Explicit Triggers

- User says "build product," "create app," "build page," "assemble product," "ship this," "product assembly."
- User invokes a product build skill.
- User requests a specific Phase (e.g., "test this app" triggers Phase 3 directly).

### 3.2 Implicit Triggers

- The task involves creating a web application, HTML tool, dashboard, or interactive module.
- The task involves building a Wix-embedded widget or component.
- The task involves creating a landing page or campaign asset that requires build/test/deploy.
- The task involves packaging files for distribution or promotion.
- The task involves deploying a completed product to a hosting platform.

### 3.3 Trigger Announcement

When D20 activates, the model must announce:
"Product Assembly Pipeline activated. Running Phase 1 (Intake) > Phase 2 (Build) > Phase 3 (Test) > Phase 4 (Package) > Phase 5 (Promote) > Phase 6 (Deploy)."

If only specific phases are triggered (e.g., testing an existing product), announce those phases only.

### 3.4 Sub-Pipeline Integration

- D18 (Media Production Pipeline) activates as a sub-pipeline when the product includes video/audio content.
- D19 (Visual Creation Pipeline) activates as a sub-pipeline when the product requires custom visual assets.
- D17 (DART Universal) activates in parallel when the product requires adversarial quality analysis (competitive positioning, claim validation).
- All sub-pipeline activations are logged in the DCL (D21).

---

## 4. Testing Depth by Product Type

| Product Type | Functional | Visual | Console/Network | Accessibility | Cybersecurity | Entity Firewall | Live Preview |
|---|---|---|---|---|---|---|---|
| Web App | Full | Full | Full | Full | Full | Full | Required |
| Wix Widget | Full | Full (in Wix context) | Full | Full | Full | Full | Required |
| Standalone HTML | Full | Full | Console only | Full | Secrets + XSS | Full | Required |
| Dashboard | Full | Full | Full | Full | Full + RLS | Full | Required |
| Landing Page | Golden path | Full | Network only | Full | Secrets | Full | Required |
| API Endpoint | Full (via requests) | N/A | Server logs | N/A | Full | Full | N/A |
| Backend Script | Unit/integration | N/A | Logs | N/A | Secrets + injection | Full | N/A |
| Packaged Media | Manifest check | Brand QA | N/A | Alt text | Metadata scan | Full | If web-renderable |

---

## 5. Cybersecurity Quick Reference

The full cybersecurity baseline is defined in D21 Section 5. This section provides a quick-reference checklist for product builds:

1. No secrets in client code (API keys, tokens, passwords, connection strings).
2. All user input validated at the boundary.
3. All rendered content sanitized against XSS.
4. All queries parameterized (no SQL injection vectors).
5. CORS explicit and restrictive (no wildcard origins).
6. CSP headers on all HTML pages.
7. HTTPS required for production.
8. Pre-commit scans for credential patterns.
9. Public-safe keys only in browser code. Service role keys server-side only.
10. File uploads validated (type, size, content) before processing.

Any failure on items 1-4 is a hard stop. No product ships with secrets exposure, unvalidated input, XSS vectors, or injection vulnerabilities.

---

## 6. Tier Access

| Tier | D20 Access |
|---|---|
| Tier 1 Sovereign | Full pipeline, all phases, testing depth matrix, cybersecurity checklist, and authority to issue a promotion recommendation. Final promotion ratification remains exclusively with DCS Level 0. |
| Tier 2 Internal Collaborator | Build and Test phases. No promotion recommendation or ratification authority; hand off to Tier 1 for review and then DCS Level 0 for any final promotion decision. Cybersecurity checks required. |
| Tier 3 External Product Build | UI/UX standards from Tier 3 Product Build Extract Section 3 only. No pipeline access. Cybersecurity is the responsibility of the Tier 1 reviewer. |

---

## Related Doctrine

- D11_HTML_Wix_App.md — Build standards for web products (D20 Phase 2 references)
- D05_Baseline_Promotion.md — Promotion protocol (D20 Phase 5 implements)
- D06_File_System.md — File routing and directory layout (D20 Phase 1 and 4 reference)
- D07_Campaign_Governance.md — Distribution channels (D20 Phase 6 hands off to)
- D09_Brand_Identity.md — Brand palette for visual compliance (D20 Phase 3 Brand QA)
- D18_Media_Production_Pipeline.md — Sub-pipeline for media content within products
- D19_Visual_Creation_Pipeline.md — Sub-pipeline for visual assets within products
- D17_DART_Universal_Methodology.md — Parallel methodology for adversarial quality analysis
- D21_Doctrine_Runtime_Engine.md — DCL logging, cybersecurity baseline, live preview mandate

---

## Error-Catch Protocol

If this doctrine file is missing or unreadable, follow the canonical error-catch protocol:
1. HALT execution. Do not infer product assembly rules from pre-training.
2. LOG `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. TRIGGER STOPGATE and alert the user.
4. FALLBACK: If D20 is unavailable, D11 (build standards), D05 (promotion), D06 (file routing), and D07 (distribution) remain individually authoritative but unsequenced. Testing and cybersecurity requirements from D21 still apply independently.
