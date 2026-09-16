# DCSE SC/SS Shared Site Chrome Standard v1

**Document ID:** DCSE-WEB-CHROME-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-16  
**Status:** ACTIVE BY DCS LEVEL 0 EXPRESS DIRECTIVE  
**Scope:** SC and SS public/product/task web surfaces  
**Parent controls:** Master Profile v7.2 R5, D08, D09, D11, D20, Product Start Gate

## 1. Purpose

Create consistent, reusable outer-site structure across Sonly Consulting and Smoove Spots product/task experiences without flattening their distinct identities.

## 2. Structural Rule

Public product/task experiences hosted under or associated with SC/SS web properties SHALL use an approved entity shell or a faithful standalone/review equivalent.

The shell consists of:
- entity header;
- approved navigation set;
- context/product identity region where needed;
- main experience;
- entity footer;
- support/legal/contact continuation where applicable.

The outer structure is standardized. The SC and SS visual identities, approved links, voice and product-specific interiors remain distinct.

## 3. Header Contract

A header SHALL:
- identify the correct public entity;
- use the approved entity logo/wordmark;
- expose only approved current navigation;
- provide a consistent home/continuation route;
- remain usable by keyboard and at mobile widths;
- preserve visible focus state;
- avoid internal DCS/DCSE governance language;
- not expose candidate, task, branch, hash or deployment metadata.

If the experience is embedded inside an existing host shell that already supplies the approved header, the embedded product SHALL NOT duplicate a competing global header.

## 4. Footer Contract

A footer SHALL:
- identify the correct public entity;
- expose approved contact/support/legal/privacy/terms routes as applicable to the product;
- preserve consistent placement and responsive behavior;
- avoid internal governance/status language;
- not embed stale commercial details that belong to transaction/product-card state.

If the host shell already supplies the approved footer, the embedded product SHALL use the host footer rather than create a conflicting duplicate.

## 5. SC vs SS Separation

Structural reuse does not authorize brand blending.

SC and SS SHALL preserve:
- their approved logos;
- entity-specific voice;
- palette/typography where governed;
- entity-specific site maps/navigation;
- product/initiative ownership;
- CTA/contact destinations.

A shared component implementation may accept entity configuration, but one entity's labels, links or visual tokens SHALL NOT silently leak into the other.

## 6. Product/Task Surface Integration

Reusable product/task shells should accept a configuration object containing at minimum:
- entity;
- product/task public title;
- active navigation context;
- approved CTA/continuation routes;
- support/contact route;
- legal/privacy/terms routes where applicable;
- brand token reference;
- header/footer variant.

The configuration is runtime/product context, not authority by itself.

## 7. Commerce and Payment Boundary

The header/footer standard does not invent or hard-code unverified provider destinations.

Payment and commerce links SHALL resolve from the product/commercial configuration or verified transaction surface. A product may display a payment CTA only when its destination has been verified for the current release.

## 8. Review/Standalone Builds

Review deployments that are not inside the final SC/SS host shell should include a faithful lightweight entity shell so DCS can review:
- visual continuity;
- navigation behavior;
- footer/legal/support placement;
- mobile behavior;
- product-to-site continuation.

Review-only shell links may target verified review routes. They SHALL NOT masquerade as production URLs.

## 9. Accessibility / UX

At minimum:
- semantic landmarks;
- keyboard operability;
- visible focus;
- mobile-safe navigation;
- readable contrast;
- reduced-motion compatibility where motion exists;
- no horizontal overflow caused by shell elements.

## 10. Reuse Before Redesign

Before creating a new header/footer:
1. inspect the current approved SC/SS shell/component;
2. reuse or configure it when compatible;
3. create a new variant only when product/runtime requirements materially differ;
4. record the reason for divergence.

## 11. Evidence

A release/review packet should identify:
- shell/component version;
- entity configuration used;
- verified link set;
- responsive/browser evidence;
- accessibility checks;
- unresolved production-only destinations.

**Structure Precedes Scale.**
