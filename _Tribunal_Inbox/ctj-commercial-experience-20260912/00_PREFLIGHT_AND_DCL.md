# CTJ Commercial Experience Build - Preflight + DCL

Task ID: SC-CTJ-COMMERCIAL-EXPERIENCE-BUILD-20260912-17
Date: 2026-09-12
Lane: SC / CTJ
Status: IN PROGRESS / CANDIDATE BUILD
Gate owner: DCS Level 0

## Preflight

Entity:
Sonly Consulting / CTJ

Destination:
GitHub candidate branch only.

Action:
Build reusable product-card -> order-intent -> external payment-selection -> payment-submission -> verification-pending customer experience.

Authority/source:
- DCS Level 0 "ok go" direction
- locked CTJ packaging baseline
- Family Audit Sync
- D11 HTML/Wix governance
- D20 Product Assembly Methodology

Model/agent:
ChatGPT / CTO-Senior DBA governance role, executing bounded frontend candidate work through authenticated GitHub connector.

Systems/access:
GitHub write to isolated review branch.

Secret exposure:
None. No API keys, passwords, provider credentials, bank/card data, MFA, or private connection strings.

Approval:
Candidate build authorized. Merge, deployment, public release, Wix mutation, payment-provider activation, production email, merchant automation, and entitlement enforcement remain excluded.

Rollback:
Delete or abandon review branch. Main is unchanged by the candidate code build.

Deliverables:
- standalone responsive product-card experience
- locked catalog data
- local order-intent state
- payment-method selection
- payment-submission form
- verification-pending confirmation
- downloadable order summary
- media manifest
- candidate documentation

Exit criteria:
- source created on isolated branch
- static validation
- security/secret scan
- responsive/live browser validation before any completion claim
- draft PR for review
- no production mutation

## Reuse decision

COMPOSE / ADAPT.

Reused:
- locked CTJ commercial package
- D11 standalone/Wix-compatible HTML implementation pattern
- local-first serializable state used across CTJ candidates
- customer-safe terminology from Family Audit

Not reused:
- Wix live checkout because current Free-plan processing is unverified/blocked
- external provider APIs because no governed integration is authorized
- existing product-runtime UI shells because this is a cross-family commercial surface rather than a product runtime

## DCL

Applied:
- D20 Product Assembly
- D11 HTML/Wix/App
- D21 task/runtime controls
- locked CTJ packaging record
- CTJ Family Audit outputs

Excluded:
- PS doctrine
- live payment-provider integration
- Supabase/auth/RLS implementation
- production email
- production entitlements
- public release

Known limitations:
- provider destination URLs are unverified and intentionally omitted
- customer-side submission cannot verify payment
- first-time Intro Trio eligibility is not automatically enforced in this candidate
- media manifest contains production slots and lineage references, not public-ready binary assets

Current exit state:
CANDIDATE BUILD IN PROGRESS.


## Scope expansion after visual/cart review

DCS Level 0 review found the initial storefront candidate materially too minimal for the CTJ visual/product intent.

Required correction now applied in the candidate branch:
- treat this as the website/product storefront layer, not a social-media platform page
- preserve social-media campaign cuts as downstream derivatives of the same Product Card Package
- apply CTJ luxe visual language: charcoal/black, platinum/silver, gold, deep blue, compass/path/labyrinth motif
- support multi-product selection
- provide a persistent shopping cart
- show bundle/overlap guidance without silently changing customer selections
- preserve Buy Now for single-product checkout
- preserve multi-product order totals through the payment-verification flow
- retain the free-compatible Cash App / PayPal manual verification boundary

User-supplied visual references reviewed in current session:
- CTJ silver compass/labyrinth parent image
- CTJ Strategic Clarity Assessment split gold/deep-blue image

These visual files are treated as production references/assets. The current GitHub connector can govern their manifest/reference but the binary image ingestion path remains separate from the text-code commit path.

Current storefront candidate head:
66ac50ac8c422bd03259aa84c6ae21ade6f93795

CI:
GitHub Actions run 34717949854 = SUCCESS.

Exit state:
CANDIDATE STOREFRONT + MULTI-PRODUCT CART STATICALLY VALIDATED.
Live hosted preview remains pending external deployment transport.
