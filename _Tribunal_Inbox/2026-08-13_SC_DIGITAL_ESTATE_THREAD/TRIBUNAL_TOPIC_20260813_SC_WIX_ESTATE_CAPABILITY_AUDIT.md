# Tribunal Topic Record: SC Wix Estate and Capability Audit

**Record date:** 2026-08-13  
**Lane:** SC  
**Status:** READ-ONLY AUDIT RECORD / PREIMPLEMENTATION  
**Implementation authority:** NONE

## Verified estate summary

The connected Wix account contains a large multi-generation estate, including the current Sonly Consulting site, historical SC variants, Smoove Spots variants, Tedo's Sports Lounge, experimental sites, and Studio-era builds.

The current canonical SC.com instance is published, uses the custom domain, is Premium, uses the regular Wix Editor, has Velo enabled, and has Wix business apps installed.

DCS reported that the paid target is Classic Editor Core and there is no current Wix Studio subscription.

## Current SC business capabilities discovered

### Store

Six visible digital products were found. Cleanup candidates include a title typo, a mismatched product slug/part number, one meaningfully populated CTJ category, and hidden categories that appear incomplete or historical.

### Pricing Plans

Seven Pricing Plan records were found, including public and private plans. The inventory suggests overlap among products, memberships, programs, bookings, services, and packages.

One PS-lane/private item discovered inside the SC estate remains `QUARANTINE / LANE REVIEW`. Its substantive contents must not be propagated into SC planning.

### Bookings

Four non-hidden services were identified. At least one course/session record appears stale relative to the current date and requires disposition review.

### Forms

Three active forms were identified.

A material privacy/copy issue exists in the upload/intake form: visible copy describes a local-only browser-storage model that does not match observed Wix server-backed submission/file-upload behavior. This is a high-priority `REWORK` candidate before broader use.

### Blog

Eight published posts plus unpublished material exist. Public/non-PS posts require relevance, voice, lane, and freshness review. PS-related material in the SC ecosystem is quarantined from the SC build and requires separate lane-governance disposition.

### Events

Three event records were found, including ended/test/duplicate material. These are strong archive candidates but have not been changed.

### SEO

Search-verification infrastructure exists. The site-level description was found blank in the Wix SEO inventory. Page/product SEO is inconsistent and needs a governed SEO/AEO/GEO pass.

### CMS/application infrastructure

Material finding: SC.com is not merely page content.

Custom Wix collections include application-oriented structures such as:

- `AdminRoles`
- `assessment`
- `CreditTransactions`
- `DashboardState`

The assessment data model contains answer payloads, scores, persona/recommendation state, consent, plan references, and attribution fields.

## Significance

Do not rebuild assessments, dashboards, or member/application logic externally until existing Velo and collection implementations are inspected.

A migration that ignores the current Wix data/application layer risks duplicate functionality, lost business rules, inconsistent identity, duplicated data, broken entitlements, and unnecessary cost.

## Working disposition taxonomy

- `KEEP`
- `REWORK`
- `MERGE`
- `REPLACE`
- `ARCHIVE`
- `QUARANTINE`
- `UNKNOWN`

Every disposition must state the reason and proposed future owner/renderer.

## Data-ownership principle

**Data ownership follows lifecycle, sensitivity, reuse, and system-of-record needs, not page location.**

Examples:

- public editorial content may suit Wix CMS;
- Wix Store catalog remains naturally owned by Wix if Wix commerce is retained;
- assessment history may belong in Supabase if persistent/cross-product;
- product source documentation may belong in GitHub/DDNA;
- task/evidence records belong in the DCSE control plane.

## Remaining audit gaps

1. full visual Editor canvas;
2. actual Velo/page/backend source;
3. dynamic-page relationships;
4. hidden/editor-only composition;
5. automations/custom-code details not exposed by current APIs;
6. final page inventory/disposition.

## Preimplementation gate

Do not connect the live site to Git/CLI or publish changes until current-state evidence is captured, compatibility is checked, target architecture is approved, a safe test workflow is selected, and rollback is defined.