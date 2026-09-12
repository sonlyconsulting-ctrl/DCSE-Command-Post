# Wix Current State and Free-Plan Payment Gate

Task ID: SC-CTJ-COMMERCIAL-PACKAGING-PAYMENTS-20260912-16
Status: BLOCKED FOR LIVE WIX PAYMENT PROCESSING / FREE-COMPATIBLE DESIGN MAY PROCEED

## Verified current Wix state

Site:
Sonly Consulting

Plan:
Free

Status:
Published

Currency:
USD

Installed relevant apps:
- Wix Stores, Catalog V3
- Wix Pricing Plans
- Wix Members Area
- Wix Pay Links
- Wix Forms & Payments
- Wix Gift Cards

Read-only API access was used to inspect:
- existing store products
- current digital product prices
- existing pricing plans

No mutation was performed.

## Existing membership/plans

The site contains existing Pricing Plans unrelated to the CTJ redesign.

Current DCS direction:
DO NOT restructure existing membership plans merely to accommodate CTJ a la carte products.

This package follows that direction.

## Payment-processing gate

Reviewed Wix documentation confirms:
- Pricing Plans can represent one-time, recurring, and free plans.
- recurring payment plans require a payment provider that supports recurring payments.
- Wix eCommerce payment processing uses configured payment providers/gateways.

The reviewed Wix documentation does not establish that this current Free site can accept live customer payments.

Therefore:

LIVE WIX PAYMENT PROCESSING = UNVERIFIED / BLOCKED

Do not configure or promise live Wix checkout/payment processing under the Free plan until eligibility is positively verified.

## Free-compatible work authorized to continue

The following work does not depend on activating Wix payment processing:
- product packaging
- price architecture
- product-card design
- external Cash App / PayPal payment selection
- order-intent logic
- payment-submission form
- manual merchant verification
- email confirmation workflow
- entitlement state design
- catalog reconciliation plan
- static website content and external links, subject to release approval

## Stop gate

Do not:
- activate a paid Wix plan
- connect a payment provider
- publish changed CTJ prices
- change live products
- alter current membership plans
- create production checkout automation

without a separate DCS Level 0 production/payment authorization and verified account eligibility.
