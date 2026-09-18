# Critical Thinker's Journey (CTJ) — Complete Product Repository

**Status:** Unified Product Structure | Master Repository  
**Date:** 2026-09-18  
**Version:** v1.0 Reorganized

---

## Overview

The Critical Thinker's Journey is a portfolio of four interconnected products designed to guide users through structured thinking, clarity, and purposeful action. This repository consolidates all four products under a unified folder structure for easy navigation, maintenance, and deployment.

### Four Products

1. **Unified Path** — Complete integrated curriculum combining all frameworks
2. **Mental Ingenuity** — Deep chamber-based puzzle experience for creative reasoning
3. **Focus & Flow** — Productivity and presence optimization tool
4. **Strategic Clarity Assessment** — Decision-making framework and assessment

---

## Repository Structure

```
SC_CTJ/
├── README.md                              (this file — master entry point)
│
├── NEW_STRUCTURE/                         (canonical product source of truth)
│   │
│   ├── Unified_Path/
│   │   ├── 1_SOURCE/                      (curriculum modules & core content)
│   │   │   ├── 00_Unified_Edition/
│   │   │   ├── 01_Building_Clarity_and_Confidence/
│   │   │   ├── 02_Exploring_Ideas_and_Making_Moves/
│   │   │   └── 03_Finding_Meaning_and_Balance/
│   │   ├── 2_PRODUCT/                     (deliverables, builds, releases)
│   │   ├── 3_ARCHITECTURE/                (specs, technical design)
│   │   ├── 4_BRANDING_AND_MARKETING/      (visual assets, campaigns)
│   │   ├── 5_QA_AND_RELEASE/              (test evidence, receipts)
│   │   └── 6_PORTAL_AND_ECOMMERCE/        (Wix, payment, entitlements)
│   │
│   ├── Mental_Ingenuity/
│   │   ├── 1_SOURCE/                      (React/TypeScript source + docs)
│   │   ├── 2_PRODUCT/
│   │   ├── 3_ARCHITECTURE/
│   │   ├── 4_BRANDING_AND_MARKETING/
│   │   ├── 5_QA_AND_RELEASE/
│   │   └── 6_PORTAL_AND_ECOMMERCE/
│   │
│   ├── Focus_and_Flow/
│   │   ├── 1_SOURCE/                      (React/TypeScript source)
│   │   ├── 2_PRODUCT/
│   │   ├── 3_ARCHITECTURE/
│   │   ├── 4_BRANDING_AND_MARKETING/
│   │   ├── 5_QA_AND_RELEASE/
│   │   └── 6_PORTAL_AND_ECOMMERCE/
│   │
│   └── Strategic_Clarity_Assessment/
│       ├── 1_SOURCE/                      (assessment HTML + guide PDF)
│       ├── 2_PRODUCT/
│       ├── 3_ARCHITECTURE/
│       ├── 4_BRANDING_AND_MARKETING/
│       ├── 5_QA_AND_RELEASE/
│       └── 6_PORTAL_AND_ECOMMERCE/
│
├── _ARCHIVE/                              (deprecated structure — for reference only)
│   ├── 00_GOVERNANCE/
│   ├── 01_SOURCE_MATERIALS/
│   ├── [... legacy folders ...]
│   └── MIGRATION_LOG.md
│
└── [supporting assets & docs]
    ├── REORGANIZATION_PLAN.md
    ├── EXPORT_MANIFEST.md
    ├── MODULES_MANIFEST.md
    └── [design/branding assets]
```

---

## Quick Start by Product

### Unified Path
**Location:** `NEW_STRUCTURE/Unified_Path/`

The complete CTJ experience combining all three parts plus integrated applications.

- **Source:** `1_SOURCE/` — Parts 1, 2, 3, Unified Edition HTML modules
- **Latest Release:** CTJ_Unified_Path_v1.0
- **Entry Point:** START_HERE.html (customer experience flow)
- **Guide:** CTJ_Unified_Path_Quick_Start.html (companion guide template)

### Mental Ingenuity
**Location:** `NEW_STRUCTURE/Mental_Ingenuity/`

A six-chamber puzzle system for advanced reasoning and creative thinking.

- **Source:** `1_SOURCE/` — React/TypeScript application + audio/video assets
- **Tech Stack:** React, TypeScript, Vite, WebGL
- **Build:** `npm run build` (in 1_SOURCE/)
- **Entry Point:** index.html (interactive chamber system)

### Focus & Flow
**Location:** `NEW_STRUCTURE/Focus_and_Flow/`

Presence and productivity optimization through guided practices.

- **Source:** `1_SOURCE/` — React/TypeScript application
- **Tech Stack:** React, TypeScript, Vite
- **Build:** `npm run build` (in 1_SOURCE/)
- **Features:** Warmup exercises, guided focus sessions, journal view, AI assist

### Strategic Clarity Assessment
**Location:** `NEW_STRUCTURE/Strategic_Clarity_Assessment/`

A decision-making framework and self-assessment tool.

- **Source:** `1_SOURCE/` — Standalone HTML assessment + welcome guide PDF
- **Format:** Single-page HTML application (no build required)
- **Deployment:** Static hosting ready

---

## Folder Categories (Consistent Across Products)

Each product has six category folders:

### 1_SOURCE
Raw source materials, code, curriculum content, and design specifications. The authoritative source for development.

### 2_PRODUCT
Current product deliverables, builds, releases, and customer-facing packages.

### 3_ARCHITECTURE
Technical specifications, module maps, design documents, and implementation guides.

### 4_BRANDING_AND_MARKETING
Visual identity, design systems, campaign materials, product positioning, and marketing copy.

### 5_QA_AND_RELEASE
Test evidence, release receipts, verification documents, and QA checklists.

### 6_PORTAL_AND_ECOMMERCE
Store configuration, payment integration, customer entitlements, portal setup, and Wix site management.

---

## Development Workflow

### Building a Product

Each product with a React/TypeScript source follows the same build pattern:

```bash
cd NEW_STRUCTURE/{PRODUCT_NAME}/1_SOURCE
npm install
npm run build
```

Built artifacts are placed in the product's `2_PRODUCT/` folder for release.

### Adding New Content

1. **Source materials** → `1_SOURCE/` (curriculum, code, docs)
2. **Architecture specs** → `3_ARCHITECTURE/` (design, specs, maps)
3. **Built releases** → `2_PRODUCT/` (compiled assets, zips, deliverables)
4. **Marketing assets** → `4_BRANDING_AND_MARKETING/` (images, copy, campaigns)
5. **QA evidence** → `5_QA_AND_RELEASE/` (test results, receipts, checksums)
6. **Portal config** → `6_PORTAL_AND_ECOMMERCE/` (integration setup)

### Deployment

Each product has independent deployment paths:

- **Unified Path:** Package as ZIP with START_HERE.html entry point
- **Mental Ingenuity:** Deploy built React app to static hosting or Vercel
- **Focus & Flow:** Deploy built React app to static hosting or Vercel
- **Strategic Clarity Assessment:** Deploy standalone HTML to static hosting

---

## Legacy Structure

The previous numbered folder structure (`00_GOVERNANCE/`, `01_SOURCE_MATERIALS/`, etc.) is archived in `_ARCHIVE/` for historical reference only.

**Migration Status:** All active content has been reorganized into `NEW_STRUCTURE/`.

---

## Collaboration & Contributions

### For Developers
1. Navigate to the product's `1_SOURCE/` folder
2. Review `3_ARCHITECTURE/` for specs
3. Build/test locally
4. Document changes in `5_QA_AND_RELEASE/`

### For Product/Marketing
1. Find product positioning in `4_BRANDING_AND_MARKETING/`
2. Access current releases from `2_PRODUCT/`
3. Coordinate releases through `6_PORTAL_AND_ECOMMERCE/`

### For QA/Validation
1. Review test matrix in `5_QA_AND_RELEASE/`
2. Execute tests against builds in `2_PRODUCT/`
3. Document evidence in release receipts

---

## Key Links & References

- **Unified Path Product:** https://buy.stripe.com/9B628r9G83uS16c3BE1ck00
- **Sonly Consulting:** https://sonlyconsulting.com
- **CTJ GitHub (Source):** sonlyconsulting-ctrl/CTJ-MVP-11252025

---

## Support & Questions

For questions about repository structure, product status, or deployment:
- Review REORGANIZATION_PLAN.md for migration details
- Check EXPORT_MANIFEST.md for packaging specifications
- See MODULES_MANIFEST.md for content structure

---

**Reorganized:** 2026-09-18  
**Authority:** Sonly Consulting  
**Maintained by:** Claude Design
