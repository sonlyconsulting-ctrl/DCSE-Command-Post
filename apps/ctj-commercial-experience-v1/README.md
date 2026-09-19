# CTJ Commercial Experience v1

Task ID: SC-CTJ-COMMERCIAL-EXPERIENCE-BUILD-20260912-17
Lane: SC / CTJ
Status: CANDIDATE BUILD
Branch: review/ctj-commercial-experience-20260912

## Purpose

Reusable customer-facing product-card and transaction-intent experience for the locked CTJ packaging baseline.

This candidate implements the free-compatible front end only:
- product cards
- locked pricing
- evergreen and first-time bundles
- order-intent creation
- Cash App / PayPal payment-method selection
- manual payment-submission capture
- verification-pending confirmation
- local save/resume
- portable order summary

It does not:
- process payments
- connect to Wix Payments
- connect to Cash App or PayPal APIs
- verify merchant-side transactions
- send production email
- grant production entitlements
- publish or deploy itself

## Locked prices

- SCA: $20
- Focus & Flow: $20
- Mental Ingenuity: $20
- Focus & Flow + Mental Ingenuity: $30
- CTJ Intro Trio: $45
- Part 1: $39
- Part 2: $39
- Part 3: $39
- Parts 1-3 Collection: $99
- Unified Edition: $119
- Complete CTJ Keeper Collection: $199

## Payment labels

- Cash App: $SonlyConsulting
- PayPal: @SonlyConsulting

No provider destination URL is included because it has not been verified.

## Reuse decision

COMPOSE / ADAPT.

This build composes the locked commercial package, D11 HTML/Wix standards, existing CTJ product metadata, and the established local-first persistence pattern used across the product family.

## Files

- index.html
- styles.css
- product-data.js
- app.js
- media-manifest.json

## Wix embed note

The candidate can be embedded later, but the exact parent origin must be configured before enabling dynamic-height postMessage behavior. No wildcard target origin is used.

## Release boundary

Candidate only. Public release, live catalog mutation, Wix payment activation, provider connection, merchant verification automation, email sending, and entitlement enforcement remain separate gates.
