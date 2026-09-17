# ESCD Enterprise Retrieval + DDNA Conversation Flow

**Task ID:** DCSE-CTJ-SUITE-CF-001  
**Issue:** #139  
**Lane:** ESCD / Command Post with SC / CTJ certification family  
**Status:** CANDIDATE IMPLEMENTATION CONTROL  
**Authority:** DCS  
**Date:** 2026-09-17

## Rules

### ER-001 — Enterprise Retrieval Before User Escalation
When DCS requests an existing enterprise asset, identifier, URL, status, decision, document, deployment, repository, product, price, checkout target, or prior artifact, ESCD MUST exhaust authorized enterprise retrieval sources before asking DCS to provide information the enterprise may already possess.

Absence from immediate conversation context is not evidence of enterprise absence.

### ER-002 — Semantic Identity Resolution
Resolve aliases and conversational references to canonical enterprise objects before retrieval. Example: `Unified`, `CTJ Unified`, `Unified Edition`, and `the Unified product` resolve to the CTJ Unified canonical object when context/evidence supports that identity.

### ER-003 — Resolution State Machine
- `UNKNOWN`: unresolved; retrieval must continue where authorized sources remain.
- `SEARCHED_NOT_FOUND`: prescribed authoritative sources searched without resolution.
- `VERIFIED_ABSENT`: affirmative evidence establishes nonexistence.

ESCD MUST NOT translate UNKNOWN into absence or prematurely escalate UNKNOWN to DCS.

## Runtime Conversation Flow

```text
DCS turn
→ intent extraction
→ entity/product/alias resolution
→ conversation-variable extraction
→ candidate DDNA extraction
→ authoritative retrieval
→ evidence/authority reconciliation
→ permitted action/reasoning
→ validation
→ semantic-object state update
→ DDNA consolidation candidate
→ contextual response composition
```

## Conversation Variables

Maintain separately: turn, session, task, project/product, entity, preference, governance, and derived variables. Derived variables are confidence-scored and never outrank explicit DCS decisions or operative governance.

## DDNA Extraction

Conversation is evidence; DDNA is semantic distillation. Extract meaningful requests, decisions, corrections, rejected behavior, selected alternatives, terminology, product/brand traits, workflow expectations, and acceptance/release criteria.

```text
EXTRACT → CLASSIFY → NORMALIZE → DE-DUPLICATE → CORRELATE
→ DETECT PATTERNS → CHECK CONTRADICTIONS → SCORE AUTHORITY/CONFIDENCE
→ CANDIDATE DDNA → VALIDATE → PROMOTE DURABLE DDNA
```

Correction pairs are high-value evidence: prior agent behavior → DCS rejection → DCS correction → preferred behavior.

## Expression Classes

- STATIC: exact canonical wording/identifiers.
- PARAMETRIC: approved structure with controlled substitutions.
- COMPOSITIONAL: semantic facts assembled according to context.
- GENERATIVE: expression varies while authoritative semantics remain fixed.

**Invariant:** Variable expression may change wording. It may not silently change authoritative meaning.

## CTJ Certification

CTJ is the first certification family for ER-001 through ER-003. Each product must resolve to a canonical semantic object with identity/aliases, family/entity, repository/source lineage, review and production deployments, approved package, product/card media, commercial copy/SEO, price, commerce identifiers, checkout target, fulfillment, customer communications, lifecycle, verification date, and provenance where applicable.

## CTJ Inventory — 2026-09-17 Evidence Pass

Current governed evidence identifies these active product roles:

1. Strategic Clarity Assessment — 31-question directional assessment candidate; validated product-core candidate in `CTJ-MVP-11252025` PR #2.
2. CTJ Part 1 — 10-day curriculum; validated modernized candidate in `SS-CTJ-Part1` PR #1.
3. CTJ Part 2 — 10-day curriculum; validated modernized candidate in `SS-CTJ-Part2` PR #1.
4. CTJ Part 3 — reconstructed 10-day curriculum; validated candidate in `SS-CTJ-Part3` PR #1, with legacy source lineage in `SS-CTJ-Full` and duplicate `SS-CTJ-Part-3` requiring archival reconciliation.
5. Focus & Flow — PRACTICE / DAILY COMPANION; validated candidate in `ctj-focus-and-flow` PR #1.
6. Mental Ingenuity — PROVE / INTERACTIVE PROVING GROUND; validated candidate in `ctj-mental-ingenuity` PR #1.
7. CTJ Unified Edition — premium synthesis capstone candidate in `CTJ-MVP-11252025` PR #1; product-core CI passed, but commercial/release gates remain.
8. Commercial bundles evidenced in Command Post PR #95: Practice + Prove, Intro Trio, Parts 1-3, Unified, and Complete Collection. These require reconciliation against current product/pricing authority before publication.

Historical BOW-004 evidence identified six original CTJ repositories and two product generations. That audit was `APPROVE_WITH_FINDINGS` while production readiness was `NON_PASS`; newer 2026-09-12 product PRs supersede many technical deficiencies but do not by themselves authorize release.

## Unified Certification Object — Initial State

```yaml
canonical_id: CTJ-UNIFIED
canonical_name: CTJ Unified Edition
aliases:
  - CTJ Unified
  - Unified Edition
  - Unified
family: Critical Thinker's Journey
entity: SC
repository: sonlyconsulting-ctrl/CTJ-MVP-11252025
candidate_pr: 1
role: premium synthesis capstone
technical_validation: PASS
release_state: GATED
known_commerce_history:
  wix_listing: hidden
  wix_preserved_price_usd: 125
  prior_playbook_price_usd: 39
  prior_playbook_price_status: unapproved
  direct_payment_link_proposal: Lemon Squeezy
  stripe_verified_configuration: UNKNOWN
release_gates:
  - reconcile product authority/lineage
  - final customer package
  - approved offer identity
  - approved price
  - purchaser entitlement/delivery boundary
  - payment provider configuration
  - test purchase
  - post-checkout/customer experience validation
```

## Media DDNA Candidate

DCS supplied two current CTJ visual assets on 2026-09-17: a parent CTJ emblem and a Unified derivative carrying `THE UNIFIED PATH`. Candidate visual DNA: deep navy field; refined metallic gold/platinum geometry; circular journey/continuity framing; central luminous abstract path/axis; restrained premium serif typography; symbolic rather than literal cross treatment; product-family derivatives should preserve the parent visual grammar while product name/subtitle varies. Binary asset registration remains a separate media-registry action.

## Commerce State Clarification

No evidence found in the current GitHub CTJ PR corpus that Stripe product/price/payment-link configuration was completed. Existing evidence instead shows earlier Cash App/PayPal candidate logic and, on 2026-09-17, a proposed Lemon Squeezy direct-payment pivot for Unified. Therefore Stripe state remains `UNKNOWN` until the Stripe account itself is queried through authorized access. Do not infer `not configured` from this UNKNOWN state.

## Next Runtime Actions

1. Query authorized commerce provider state, beginning with Stripe when connected.
2. Reconcile each CTJ product/bundle to one canonical semantic object.
3. Resolve review/production deployment URLs from authoritative deployment evidence rather than asking DCS first.
4. Complete missing commercial fields product-by-product.
5. Generate DDNA candidates continuously; promote only after authority/contradiction review.
6. Validate static/parametric/compositional/generative responses against canonical semantic objects.
7. Record release evidence and retain VERIFIED / LIKELY / UNKNOWN distinctions.
