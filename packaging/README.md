# CTJ Packaging: Launch Packs and Keeper Packs

**Current Status:** ACTIVE PACKAGE PHASE (D20 Phase 4)

This directory implements the **Virtual Packaging** layer for CTJ products. It defines exactly what customers receive, how products are delivered, and how package-level QA runs automatically before release.

## Directory Structure

```
packaging/
├── package.json                    # Build dependencies
├── products.config.json            # Product definitions (all 7 products)
├── README.md                       # This file
├── launch-packs/
│   ├── templates/                  # Reusable Launch Pack templates
│   │   ├── 00_START_HERE.html
│   │   ├── 01_OPEN_PRODUCT.html
│   │   ├── 02_PRODUCT_GUIDE.html
│   │   └── 03_PACKAGE_MANIFEST.json.template
│   └── [product-id]/               # Product-specific content
│       ├── unified/
│       │   └── content.json        # Unified Edition guide content
│       ├── sca/
│       ├── part1/
│       ├── part2/
│       ├── part3/
│       ├── focus-and-flow/
│       └── mental-ingenuity/
├── keeper-packs/
│   ├── templates/                  # Reusable Keeper Pack templates
│   └── [product-id]/               # Product-specific keeper formats
├── scripts/
│   ├── build-launch-pack.js        # Main build script
│   ├── validate-package.js         # Package compliance validator
│   ├── build-keeper-pack.js        # Keeper Pack generation (TBD)
│   └── generate-all-packs.js       # Batch build all products (TBD)
└── dist/                           # Output directory (created by build)
```

## What is a Launch Pack?

A **Launch Pack** is a ZIP file delivered to the customer immediately after payment verification. It contains:

1. **00_START_HERE.pdf/html** — One-page premium introduction with what they bought, time commitment, and what they'll produce
2. **01_OPEN_PRODUCT.html** — Branded launcher with a START button (opens hosted product, no embedded secrets)
3. **02_PRODUCT_GUIDE.pdf/html** — 3-6 page user guide covering navigation, save/resume, display controls, privacy, exports, reset behavior, support
4. **03_PACKAGE_MANIFEST.json** — Metadata, file checksums, verification info

**Filename pattern:** `CTJ-<PRODUCT>-Launch-Pack-v<VERSION>.zip`

## What is a Keeper Pack?

A **Keeper Pack** is a ZIP file generated inside the product when the user completes and exports their work. It contains:

1. **Branded PDF** — Premium-formatted artifact (e.g., `CTJ_Unified_Complete_Logic_Map.pdf`)
2. **Plain text** — Universal readable fallback
3. **JSON** — Structured backup/portability format
4. **04_EXPORT_MANIFEST.json** — Integrity and version record

**Filename pattern:** `CTJ-<PRODUCT>-Keeper-Pack-<YYYYMMDD>.zip`

## Building Launch Packs

### For a Single Product

```bash
cd packaging
npm install
node scripts/build-launch-pack.js unified ./dist
```

Output: `dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip`

### For All 7 Products

```bash
node scripts/generate-all-packs.js ./dist
```

## Validating Packages

After building, validate that the package meets the spec:

```bash
node scripts/validate-package.js ./dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip
```

Checks:
- ZIP structure (4 files, correct names)
- File integrity (no empty files)
- Manifest validity and consistency
- Secrets scan (no API keys, tokens, passwords)
- Launcher accessibility (keyboard, reduced motion)
- HTML/PDF rendering

## Product-Specific Content

Each product has a `content.json` that defines what goes into its guide:

```json
{
  "product": { "id", "name", "subtitle", "role", "effort", "price" },
  "guide": {
    "overview": "What is this product?",
    "what_you_do": "What will the user do?",
    "what_you_produce": "What will they keep?",
    "save_resume_behavior": "How does save/resume work?",
    "privacy_statement": "Privacy and data handling",
    "reset_behavior": "How to reset or start over",
    "product_boundaries": "What this is NOT",
    "accessibility_statement": "Accessibility features"
  }
}
```

**Status:**
- ✓ Unified Edition content complete (`launch-packs/unified/content.json`)
- ⚠ SCA, Part 1-3, Focus & Flow, Mental Ingenuity — content files needed

## Branding

The Launch Pack family uses consistent branding:
- **Foundation:** #2B2B2B (charcoal)
- **Platinum:** #E8E8E8 (silver emphasis)
- **Gold:** #D4A574 (accent)
- **Blue:** #4A7BA7 (connective accent)

Serif display font: Georgia  
Body font: system-ui / UI stack

## Current Build Status

| Product | Launch Pack | Content | Status |
|---------|-------------|---------|--------|
| Strategic Clarity Assessment | Template ready | TBD | Blocked on content |
| Part 1 | Template ready | TBD | Blocked on content |
| Part 2 | Template ready | TBD | Blocked on content |
| Part 3 | Template ready | TBD | Blocked on content |
| Focus & Flow | Template ready | TBD | Blocked on content |
| Mental Ingenuity | Template ready | TBD | Blocked on content |
| **Unified Edition** | Template ready | ✓ Complete | Ready to build |

## Next Steps

### Phase 1: Content (This Week)
- [ ] Create `content.json` for SCA, Part 1-3, Focus & Flow, Mental Ingenuity
- [ ] Review content for accuracy and brand voice
- [ ] Generate all Launch Packs
- [ ] Validate all packages

### Phase 2: PDF Generation (Next)
- [ ] Convert HTML templates to premium PDFs (using puppeteer or similar)
- [ ] Design Keeper Pack PDFs (branded formatting, typography, layout)
- [ ] Test PDF rendering across browsers
- [ ] Generate sample Keeper Packs from actual product exports

### Phase 3: Delivery Integration (Following)
- [ ] Wire up payment processor → Launch Pack generation
- [ ] Create secure download/access page
- [ ] Implement entitlement verification
- [ ] Test end-to-end delivery flow

### Phase 4: Release QA (Final)
- [ ] Manual screen-reader review
- [ ] 200% zoom responsive check
- [ ] Final visual/brand QA
- [ ] Accessibility formal audit
- [ ] Release approval by DCS Level 0

## Integration Points

The packaging system connects to:
1. **Payment Processor** — Triggers Launch Pack download after verification
2. **Product Runtime** — Products generate Keeper Packs on completion
3. **Entitlements System** — Controls which customer gets which package
4. **Analytics** — Logs package generation and downloads
5. **Support** — Uses `support_url` from manifest

## Notes

- **Templates use Mustache-style interpolation:** `{{VARIABLE_NAME}}`
- **Files are currently HTML; final PDFs TBD** (requires puppeteer/pdfkit)
- **No secrets should appear anywhere** in the package (validated automatically)
- **All three Keeper formats** (PDF, TXT, JSON) **must represent the same state**
- **Product Guide PDF will be 3-6 pages** depending on product complexity

## Governance

Authority: DCS Level 0  
Phase: D20 Phase 4 (PACKAGE)  
Status: ACTIVE DEVELOPMENT  
Next gate: Human package review + final visual/accessibility QA

---

For questions or issues, contact the governance team or see `_Tribunal_Inbox/ctj-virtual-packaging-20260914/`.
