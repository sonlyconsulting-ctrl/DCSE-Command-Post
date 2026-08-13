# Tribunal Topic Record: SC Chat/F&A, Blog, Offer, Product, and Membership Architecture

**Record date:** 2026-08-13  
**Lane:** SC  
**Status:** PRODUCT/SYSTEMS DISCUSSION RECORD  
**Implementation authority:** NONE

## Chat/F&A direction

DCS explicitly wants the current Chat/F&A capability upgraded.

The working principle is:

**Do not merely replace a chatbot. Define the business capabilities the conversational layer is authorized to perform.**

Candidate maturity levels:

1. static FAQ search;
2. retrieval from approved SC knowledge;
3. guided discovery/question answering;
4. product/service matching;
5. assessment/intake assistance;
6. authenticated member assistance;
7. approved read/write interaction with business systems;
8. human handoff and persistent history.

Open decisions include source corpus, anonymous conversation retention, member conversation persistence, account identity, supported business actions, handoff, and security/data-class boundaries.

Potential future actions include scheduling, product recommendation, assessment start, saved-result retrieval, member/purchase status, inquiry/support case creation, article surfacing, and escalation to DCS.

## Blog workflow

The working Blog architecture is not simply "write in Wix."

Candidate governed pipeline:

`Idea/Source -> Research/Evidence -> Draft -> Lane Check -> Voice/Persuasion Review -> Human Approval -> SEO/AEO/GEO -> Channel Adaptation -> Publish -> Receipt -> Metrics -> Refresh/Archive`

Possible channels include Wix Blog, Substack, LinkedIn/other professional channels, Google/Bing posts where supported, email/newsletter, and DDNA/RAG.

A canonical article artifact should exist so channel adaptations do not become competing versions of truth.

## Offer classification rule

Before a commercial offer enters Wix or another commerce system, classify it as one of:

- `PRODUCT`
- `MEMBERSHIP`
- `SERVICE`
- `BOOKING`
- `BUNDLE`
- `PROGRAM`
- `FREE_RESOURCE`

This prevents Store, Pricing Plans, Bookings, and ad-hoc offers from overlapping without business reason.

## Product formula

`Audience -> Need -> Artifact/Capability -> Use -> Practical Outcome -> Evidence -> Access -> Price -> CTA`

A product should have a clear completion/use event.

## Membership formula

`Audience -> Continuing Job/Need -> Recurring Value -> Entitlement -> Delivery Cadence -> Participation/Support -> Renewal Logic -> Price -> CTA`

Key test: **If SC cannot name a defensible recurring reason to remain subscribed, the offer probably should not be a membership/Pricing Plan.**

## Service formula

`Audience -> Problem -> Scope -> Inputs -> Method -> Deliverable -> Boundary -> Price/Quote Method -> CTA`

## Booking formula

`Service -> Session Purpose -> Eligibility -> Duration -> Preparation -> Delivery Method -> Availability -> Price -> Follow-up`

## Current Wix commercial implication

Existing Store, Pricing Plans, and Bookings contain overlapping historical offers.

Do not delete or consolidate them until current intentional offers are identified, each is reclassified, target customer/outcome is verified, price/billing is reviewed, member entitlement is defined, and the selected business system is identified.

## Member identity question

A major architecture decision remains: Wix Members as canonical SC identity, cross-product identity outside Wix, or a hybrid model with Wix entitlements bridged to application systems.

Do not solve this by default. The answer depends on product count, data reuse, external apps, authenticated Chat, and portability.