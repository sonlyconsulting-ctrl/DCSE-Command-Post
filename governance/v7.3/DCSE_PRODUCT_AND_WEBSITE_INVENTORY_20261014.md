# Master Digital Product & Website Inventory (Live Links)

**Authority:** DCS Level 0 / DCSE v7.3 Directive  
**Date:** 2026-10-14  
**Classification:** CANONICAL PRODUCTION & DIGITAL ASSET INVENTORY  
**Status:** CONVERGED & VERIFIED (Replaces All Static Image Screenshots)

---

## 1. Digital Product Suite & Deliverables (Edition 1.1)

All prices, scopes, and deliverable packages are locked in accordance with DCS Level 0 directives and verified against `deliverables/v1.1/CTJ_PACKAGE_EVIDENCE_20261003.json`.

| Product Code | Official Title | Price | Delivery Asset | Interactive Scope & Architecture |
|---|---|---|---|---|
| **CTJ-PART-1** | Part 1: Building Clarity and Confidence | $39 | `CTJ_Part_1_v1.1.zip` | Days 1–10 (10 Builders, 21 Prompts, Day 5 & 10 Checkpoints, local persistence) |
| **CTJ-PART-2** | Part 2: Exploring Ideas and Making Moves | $39 | `CTJ_Part_2_v1.1.zip` | Days 11–20 (10 Builders, 21 Prompts, Day 15 & 20 Checkpoints, experiment testing) |
| **CTJ-PART-3** | Part 3: Finding Meaning and Balance | $49 | `CTJ_Part_3_v1.1.zip` | Days 21–30 (10 Builders, 21 Prompts, Day 25 & 30 Checkpoints, metacognition) |
| **CTJ-UNIFIED** | The Unified Path (Flagship Edition) | $119 | `CTJ_Unified_Path_v1.1.zip` | Decision Brief, Daily Thought Exercise, Integrated Capstone (4 scenarios & 7 CTJ lenses), deterministic Logic Map |
| **CTJ-COLLECTION** | The CTJ Collection (Complete 4-in-1) | $199 ($99 special) | `CTJ_Collection_v1.1.zip` | 4-in-1 complete runner (`START_HERE.html`), 4 printable workbooks (PDF), zero-network runner |
| **CTJ-SCA** | Strategic Clarity Assessment | Included / $20 Lead | Embedded / Web App | 31 deterministic diagnostic questions across 3 core pillars (Analytical, Creative, Systems) |
| **CTJ-VOTER** | CTJ: Voter Edition (`CANON-162`) | Included / Civic | Standalone Module | 7-step civic nonpartisan reflection framework + personal Clarity Card |

---

## 2. Live Web Applications, Showrooms & Review Sites (Direct HTTPS Links)

| Property Name | Platform / Host | Live Verified Link | Current Status & Access |
|---|---|---|---|
| **CTJ Unified Master Suite Preview** | Local Standalone Preview | [ctj_suite_unified_preview.html](file:///c:/DS%20All%20Things/DCSE_Command_Center/apps/ctj_suite_unified_preview.html) | Standalone Zero-Localhost Artifact (Zero Watermark) |
| **CTJ Part 1 Review** | Netlify Review App | [https://ctj-part1-review-20260912.netlify.app](https://ctj-part1-review-20260912.netlify.app) | Candidate Created / Staged |
| **CTJ Part 2 Review** | Netlify Review App | [https://ctj-part2-review-20260912.netlify.app](https://ctj-part2-review-20260912.netlify.app) | Active (Watermark Manually Removed) |
| **CTJ Unified Review** | Netlify Review App | [https://ctj-unified-review-20260912.netlify.app](https://ctj-unified-review-20260912.netlify.app) | Active (Includes `/success` return hook) |
| **SC CTJ Unified Review** | ChatGPT Sites | [https://sc-ctj-unified-review-20260926.sonlysc.chatgpt.site](https://sc-ctj-unified-review-20260926.sonlysc.chatgpt.site) | Active (Owner Allowlist) |
| **Sonly Consulting Product Showroom** | ChatGPT Sites | [https://sc-product-showroom-preview.sonlysc.chatgpt.site](https://sc-product-showroom-preview.sonlysc.chatgpt.site) | Active (Owner Allowlist) |
| **CTJ Silver Website Review** | ChatGPT Sites | [https://ctj-silver-review-20261013.sonlysc.chatgpt.site](https://ctj-silver-review-20261013.sonlysc.chatgpt.site) | Active Review (Published Oct 13, 2026) |
| **DCSE Command Post** | ChatGPT Sites | [https://dcse-command-post.sonlysc.chatgpt.site](https://dcse-command-post.sonlysc.chatgpt.site) | Active (Owner Allowlist) |
| **Sonly Consulting Rebuild** | ChatGPT Sites | [https://sonly-consulting-rebuild.sonlysc.chatgpt.site](https://sonly-consulting-rebuild.sonlysc.chatgpt.site) | Active (Version 3) |
| **Shoegirl Platinum Edition** | ChatGPT Sites | [https://shoegirl-platinum-edition.sonlysc.chatgpt.site](https://shoegirl-platinum-edition.sonlysc.chatgpt.site) | Active Public (Version 8) |
| **CTJ Focus & Flow Experience** | Google Cloud Run / Netlify | [https://ctj-focus-flow-review-20260912.netlify.app](https://ctj-focus-flow-review-20260912.netlify.app) | Active Review Link |
| **Mental Ingenuity QA** | Vercel QA App | [https://mental-ingenuity-qa.vercel.app](https://mental-ingenuity-qa.vercel.app) | Active QA Link |
| **SC-CTJ Web App** | Vercel Preview | [https://sc-ctj.vercel.app](https://sc-ctj.vercel.app) | Active Core Storefront |

---

## 3. Video & Media Production Status

| Media Asset | Associated Product / Experience | Status | Production Notes |
|---|---|---|---|
| **Get Your Think On!™ (GYTO) Video** | CTJ Product Suite / GYTO Entry | **REMAINING TO COMPLETE** | The single pending video in the CTJ production pipeline. 60-second interactive diagnostic hook / founder video bed. |
| **Focus & Flow Audio Beds** | Focus & Flow Satellite Experience | Complete / Staged | Soulful mid-tempo instrumentation. |
| **CTJ Unified Tour & Media Preview** | The Unified Path | Complete (`unified-commercial.webp`) | Embedded in buyer portal and web showroom. |

---

## 4. Production Release & Custom Domain Settings Gate

1. **Target Production Custom Domain:** `ctj.sonly-consulting.com` (or root parent `sonlyconsulting.com/ctj/`).
2. **Current Status:** Not yet activated in public DNS. All apps currently operate behind authenticated review domains (`*.netlify.app` and `*.chatgpt.site`).
3. **Required Promotion Gate Settings:**
   - **DNS:** Provision CNAME record for `ctj.sonly-consulting.com` pointing to the designated host.
   - **TLS/SSL:** Enforce Let's Encrypt / automated TLS certificate.
   - **Canonical Headers:** Enforce `rel="canonical"` and `robots.txt` (`noindex, nofollow` on temporary Netlify review domains; indexable only on production custom domain).
   - **Stripe Webhooks & Callbacks:** Rebind `success_url` and `cancel_url` from temporary Netlify domains to `https://ctj.sonly-consulting.com/success`.
   - **Cross-App Return URL:** Every cross-app transition preserves `?returnTo=` state to enable seamless back-navigation across the entire suite.
