# DCSE Methodology: Website Creation Workflow (D20/D16)

**Document ID:** DCSE-METH-WEBSITE-CREATION-v1  
**Version:** 1.0  
**Authority:** DCS Level 0  
**Status:** ACTIVE / OPERATIVE  
**Applicable Lanes:** SC / DCSE / ALL  
**Parent Doctrines:** D20 Product Assembly, D16 DDNA Governance, D11 Application Development

---

## 1. Controlling Purpose

This methodology establishes a deterministic, fail-closed standard for producing, updating, and releasing commercial websites and digital storefronts across DCSE entities (specifically Sonly Consulting SC.com artifacts). 

Agents and developers SHALL NOT start website creation from a blank canvas. Every web surface must be strictly derived from past build DDNA, verified brand assets, locked price authorities, and accessibility baselines.

---

## 2. The 5-Stage Fail-Closed Pipeline

`	ext
STAGE 1: DDNA INTAKE & PAST BUILD AUDIT
  |  Verify Level 0 authority for colors, typography, brand marks, and locked prices.
  |  Evaluate past build receipts and test coverage before writing code.
  v
STAGE 2: COMMERCIAL ARCHITECTURE & SECTIONS
  |  Hero & Positioning: Family entity relationship (e.g. Sonly Consulting -> CTJ).
  |  Role-Based Product Grid: Categorized by functional roles (DISCOVER, LEARN, PRACTICE, PROVE, INTEGRATE).
  |  Interactive Product Cards: Standardized fields (Role badge, Title, Tagline, Effort, Produce/Keeper, Price, Action).
  |  Strategic Bundle Tiers: High-margin cross-product pathways.
  v
STAGE 3: COMMERCE & PAYMENT GATEWAYS
  |  Dual-Target Architecture: Direct payment redirects (Stripe, Lemon Squeezy) + manual merchant paths (Cash App, PayPal).
  |  Zero-Secret Rule: Client code SHALL NOT contain secret keys, API tokens, or server-side credentials.
  |  State Boundary: Customer submission creates PAYMENT_SUBMITTED; only merchant verification grants ENTITLEMENT.
  v
STAGE 4: D20 QUALITY & ACCESSIBILITY MECHANICAL GATE
  |  Deterministic static linting: 0 em/en dashes, zero secrets, valid DOM IDs.
  |  WCAG AA Baseline: Keyboard accessibility (:focus-visible), High Contrast ratios, text scaling, and prefers-reduced-motion.
  |  Governed browser preview before claiming completion.
  v
STAGE 5: PACKAGING & FULFILLMENT HANDOFF
  |  Post-checkout webhooks trigger 4-file Launch Pack ZIP delivery.
  |  Client-side completion triggers 4-file Keeper Pack ZIP export.
`

---

## 3. Brand Relationship Doctrine (SC.com Complementary Standards)

When a product family (such as CTJ) operates as an artifact of Sonly Consulting (SC.com):
1. **Complementary, Not Identical:** The product site must honor the parent entity's visual DNA while establishing its own product identity.
2. **Gold-to-Navy Reversal Rule (DCS Direction 2026-09-19):**
   - **Primary Canvas / Header:** Warm Metallic Gold & Champagne Cream (#f4efe6, --gold-banner).
   - **Secondary Structural Anchor:** Deep Navy (#1a3d5c, #061a33) for typography, navigation elements, card borders, and primary CTA buttons.
   - **Capstone Distinction:** The flagship synthesis product (Unified Edition) inverts the card field to Deep Navy with Gold Foil typography to immediately signal premium tier.
3. **Typography Standard:**
   - Display & Headings: Restrained Georgia / Times serif.
   - Body & Controls: System UI / Inter / Arial sans-serif.

---

## 4. Preflight & Acceptance Gates

A website release is NON_PASS if any of the following occur:
* **Invented Pricing:** Prices differ from the locked packaging manifest.
* **Secret Leakage:** Any pattern matching sk-, AIza, private keys, or passwords exists in client code.
* **Accessibility Blindness:** Elements cannot be fully operated via Tab/Enter keys or break under prefers-reduced-motion.
* **Ungrounded Visuals:** Unapproved color palettes or fonts deployed without explicit Level 0 approval.
