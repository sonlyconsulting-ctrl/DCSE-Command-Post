# CTJ Virtual Packaging Specification

Task ID: SC-CTJ-VIRTUAL-PACKAGING-20260914-19
Lane: SC / CTJ
Date: 2026-09-14
Status: ACTIVE PACKAGE PHASE
Authority: DCS Level 0 current-session direction
Gate owner: DCS Level 0

## 1. Purpose

CTJ is now entering D20 Phase 4: PACKAGE after validated product-core testing and before final release-level visual/accessibility/deployment QA.

Virtual Packaging defines exactly what a customer receives, how it is delivered, how the files look, how bundle purchases are organized, and how package-level QA/compliance runs automatically before release.

This stage does not reopen product substance, pricing, or storefront design.

## 2. Customer Delivery Model

Each standalone CTJ purchase uses two customer package envelopes across the product lifecycle.

### A. Launch Pack ZIP

Delivered after payment is verified and entitlement/access is approved.

Filename pattern:
`CTJ-<PRODUCT>-Launch-Pack-v<PACKAGE_VERSION>.zip`

Exactly four files:

1. `00_START_HERE.pdf`
   - one-page premium branded opening
   - product title/subtitle
   - CTJ role: Discover, Learn, Practice, Prove, or Integrate
   - what the customer bought
   - expected effort
   - what they will produce/keep
   - start instruction

2. `01_OPEN_PRODUCT.html`
   - branded customer launcher
   - one primary START button
   - opens the authorized hosted product route
   - no embedded secret, password, API key, service-role key, reusable credential, or provider token
   - accessible fallback text if the launch link fails

3. `02_PRODUCT_GUIDE.pdf`
   - approximately 3 to 6 pages depending on product
   - product purpose
   - navigation
   - save/resume behavior
   - accessibility/display controls
   - privacy/local-storage boundary
   - how exports work
   - restart/reset behavior
   - support route
   - no durable price text, because transaction pricing belongs to the order record and product card

4. `03_PACKAGE_MANIFEST.json`
   - product ID
   - product name
   - edition/package version
   - package generated timestamp
   - source/version reference
   - expected file list
   - checksums where generated
   - no PII and no secrets

### B. Keeper Pack ZIP

Generated from inside the product when the user reaches the applicable completion/export state.

Filename pattern:
`CTJ-<PRODUCT>-Keeper-Pack-<YYYYMMDD>.zip`

Exactly four files:

1. primary branded PDF customer artifact
2. TXT portable/plain-text artifact
3. JSON structured backup artifact
4. `04_EXPORT_MANIFEST.json`

The PDF is the presentation artifact.
TXT is the universal human-readable fallback.
JSON is the structured backup/portability format.
The manifest is the integrity/version record.

Existing individual PDF/TXT/JSON download controls may remain available, but the default completion CTA should be:
`DOWNLOAD MY KEEPER PACK (.ZIP)`

## 3. Product-Specific Keeper Artifact Names

| Product | Primary PDF/TXT/JSON basename |
| --- | --- |
| Strategic Clarity Assessment | `CTJ_Strategic_Clarity_Profile` |
| Part 1 | `CTJ_Part_1_Workbook_Record` |
| Part 2 | `CTJ_Part_2_Workbook_Record` |
| Part 3 | `CTJ_Part_3_Workbook_Record` |
| Focus & Flow | `CTJ_Focus_Flow_Session_Record` |
| Mental Ingenuity | `CTJ_Mental_Ingenuity_Reasoning_Signature` |
| Unified Edition | `CTJ_Unified_Complete_Logic_Map` |

Mental Ingenuity currently uses TXT, JSON, and browser Print/Save PDF. Package compliance requires a deterministic generated PDF path before its Keeper ZIP can be final.

## 4. Bundle / Collection Delivery

Bundles do not send duplicate standalone Launch Packs.

A bundle purchase receives one four-file Launch Pack ZIP using the same structure:

- `00_START_HERE.pdf`
- `01_OPEN_COLLECTION.html`
- `02_COLLECTION_GUIDE.pdf`
- `03_PACKAGE_MANIFEST.json`

The collection launcher lists only the products actually purchased/entitled.

Applicable packages:

- Focus & Flow + Mental Ingenuity pair
- CTJ Intro Trio
- Parts 1-3 Collection
- Complete CTJ Keeper Collection

Each product later generates its own four-file Keeper Pack when completed.

## 5. Customer File Counts

### Standalone purchase
Initial delivery: 1 ZIP containing 4 files.
Completion delivery: 1 Keeper ZIP containing 4 files.
Lifecycle product-file total: 8 files, organized as two ZIPs.

### Pair / Trio / Parts collection
Initial delivery: 1 collection ZIP containing 4 files.
Each completed product: 1 four-file Keeper ZIP.

### Complete CTJ Keeper Collection
Initial delivery: 1 collection ZIP containing 4 files.
Completion: up to seven separate four-file Keeper ZIPs, one per product.
Do not dump 28 completion artifacts into one undifferentiated archive.

Transaction confirmation/receipt is a commerce record and is not counted as a product-package file.

## 6. Delivery Channel

Target production flow:

`PAYMENT_VERIFIED -> VERIFICATION EMAIL -> SECURE ACCESS PAGE -> START PRODUCT + DOWNLOAD LAUNCH PACK`

The verification email is the delivery envelope.

Do not attach large ZIP files directly to email by default.
Provide a governed download/action link from the verified access page.

The Launch Pack may be regenerated for an entitled customer without changing ownership.

Product access is hosted. Source code is never delivered to the customer.

## 7. Visual Design Contract

### Launch Pack PDF / Collection Guide
- premium CTJ family presentation
- charcoal/dark neutral foundation
- platinum/silver hierarchy
- restrained gold/deep-blue connective accents
- product-specific sub-brand variation preserved
- strong serif display typography paired with readable UI/body type
- clear whitespace and section hierarchy
- no generic office-document appearance
- no code/version/internal candidate language on customer-facing pages

### Launcher HTML
- visually consistent with the locked CTJ storefront
- product hero or emblem
- concise product role and expected outcome
- large START CTA
- responsive/mobile-safe
- keyboard/focus-safe
- reduced-motion-safe
- no secret-bearing query parameters stored in the file

### Keeper PDF
Current exports are functional product records, but several use basic jsPDF Helvetica/Times output and are not yet the final premium package presentation.

The packaging phase therefore includes redesigning Keeper PDFs so the exported artifact feels like part of the product, not a raw system printout.

The final PDF should include:
- CTJ/product cover treatment
- product title/subtitle
- export date
- section hierarchy
- branded rule/divider treatment
- readable long-form typography
- page numbers/footer where appropriate
- product-specific result/workbook content
- required non-diagnostic or interpretation boundary where applicable

TXT and JSON remain intentionally utilitarian.

## 8. Automatic Package QA and Compliance

Package QA is mandatory and runs before human final release QA.

For every Launch Pack and Keeper Pack, automation shall verify as applicable:

### Structure
- ZIP opens successfully
- exact expected file count
- no unexpected executables/source files
- filenames match contract
- no nested duplicate package
- manifest matches physical ZIP contents

### Integrity
- all files non-empty
- hashes/checksums generated where configured
- package/product/version IDs reconcile
- no stale candidate/MVP/internal-only wording
- no secret/token/password/key patterns
- no PII in generic package templates

### Content
- product title/subtitle correct
- role correct
- guide content matches actual runtime behavior
- support/privacy/export wording matches implemented product
- required disclaimers present where applicable
- no unsupported AI/clinical/psychometric claims
- no stale pricing embedded in durable product docs

### Visual / document
- PDF renders
- no clipped/blank pages
- no overflow at expected page size
- headings and body text visible
- branded cover present
- product-specific visual identity preserved

### Web launcher
- HTML parses
- keyboard-accessible START control
- responsive layout
- reduced-motion support
- safe link contract
- no wildcard postMessage
- no embedded secrets
- no broken asset references

### Keeper export consistency
- PDF/TXT/JSON represent the same completed product state
- JSON parses
- TXT is readable
- manifest identifies all three artifacts
- export filenames stable

Automated PASS does not replace manual screen-reader review, 200 percent zoom review, or final human cosmetic QA.

## 9. Package-Stage Sequence

`LOCKED PRODUCT CARD/PRICE -> BUILD LAUNCH PACK -> BUILD KEEPER PACK -> ZIP -> AUTOMATED PACKAGE QA -> FIX/REPACKAGE -> HUMAN PACKAGE REVIEW -> FINAL MODULE VISUAL/ACCESSIBILITY QA -> PROMOTION/DEPLOYMENT DECISION`

This preserves D20:
product-core Build/Test is already validated; Package now occurs before final release-level inspection and promotion.

## 10. Current Build Gap

Verified current state:
- all seven products already have product-core exports or equivalent output surfaces
- SCA, Parts 1-3, Focus & Flow, and Unified currently generate PDF/JSON/TXT
- Mental Ingenuity currently generates TXT/JSON and Print/Save PDF
- no standardized four-file Launch Pack ZIP currently exists
- no standardized four-file Keeper ZIP currently exists
- current PDF exports require package-level aesthetic normalization before release
- storefront payment verification and entitlement delivery remain integration work

## 11. Exit Criteria

Virtual Packaging is complete only when:

1. all seven standalone Launch Pack ZIPs are generated and pass automated package QA;
2. bundle/collection Launch Pack ZIPs are generated and pass automated package QA;
3. all seven Keeper Pack contracts are implemented;
4. Mental Ingenuity has a deterministic generated PDF;
5. all Keeper PDFs receive premium visual treatment;
6. package manifests reconcile to actual contents;
7. browser/runtime can produce or retrieve the correct package;
8. no secret/PII leakage is found;
9. human package review evidence is recorded;
10. final visual/accessibility/release QA may then proceed.

Exit state:
ACTIVE PACKAGE PHASE.
