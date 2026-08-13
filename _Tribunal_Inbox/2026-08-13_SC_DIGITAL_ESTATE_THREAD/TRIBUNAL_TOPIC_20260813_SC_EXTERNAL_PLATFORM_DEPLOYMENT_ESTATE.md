# Tribunal Topic Record: SC External Platform and Deployment Estate

**Record date:** 2026-08-13  
**Lane:** SC / DCSE  
**Status:** INVENTORY / DIAGNOSTIC CANDIDATE  
**Implementation authority:** NONE

## Scope

This topic records external web, publishing, search, and deployment surfaces that must be included in the SC Digital Estate architecture rather than treated as incidental tools.

Included: Vercel, Netlify, Substack, Google and Bing public profiles, domains and external identity, analytics/search tooling, and deployment portability.

## Vercel

### Verified connected estate

The connected Vercel team contains 12 visible projects:

- `mental-ingenuity-qa`
- `dist`
- `sc-agent-os`
- `sc-command-post`
- `consumer-shell`
- `dcse-asset-portal`
- `magical-learning-gift-review`
- `vow-and-go-review`
- `dcse-wix-bridge`
- `project-zmdcv`
- `web`
- `retrograde-whirlpool`

Recent deployment history shows that multiple Vercel projects connected to the shared `DCSE-Command-Post` repository have rebuilt from commits that appear unrelated to deployed application code, including governance changes.

### Likely risk

Repository/project deployment triggers may be broader than necessary.

Possible consequences include unnecessary builds, canceled deployments, notification noise, build-minute consumption, confusing deployment history, and difficulty tying a deployment to a product change.

This may relate to recent "deployment failed" email activity, but the exact failed email/deployment has not yet been correlated. Do not claim root cause until the specific failed deployment is identified and its logs are reviewed.

### Required bounded diagnostic

1. identify failed emails/deployment IDs;
2. map every Vercel project to intended repository path;
3. classify production, QA, preview, abandoned, and experimental states;
4. identify Git trigger scope;
5. review failed build logs;
6. recommend path filters, ignored-build rules, project consolidation, or repository separation only where evidence supports it;
7. make no configuration change before DCS review.

## Netlify

DCS recalled Netlify as part of the estate/toolset. Current status remains `UNKNOWN`.

Required inventory: account/team, site names, URLs/domains, Git connections, build settings, plan/billing tier, active traffic/dependency, and current purpose. Secret values must not be exposed.

Disposition candidates: active host, static-site specialist, portability/fallback host, legacy, or retire.

Do not choose Vercel or Netlify based on vendor preference. Choose based on application needs, portability, cost, operational simplicity, and evidence.

## Substack

DCS recalled Substack as part of the publishing estate. Current publication state and intended role remain `UNKNOWN`.

Possible roles include primary newsletter, secondary distribution, long-form publication, SS storytelling channel, DCS personal publication, or legacy.

Preferred architecture if retained:

`Canonical approved content -> channel-specific adaptation -> Substack publish -> receipt/metrics`

Substack should not silently become the source of truth if the same content must also power Wix, search profiles, DDNA/RAG, and other channels.

## Google and Bing public profiles

Do not classify these as fully static or fully dynamic.

### Static governed identity layer

Business name, canonical domain, approved description, contact identity, logo/images, categories, official links, core service names, and legal/policy links should originate from a canonical `SC_PUBLIC_PROFILE` record and change infrequently.

### Dynamic operational layer

Potentially posts, updates, offers, temporary hours, selected products/services, events, campaign links, current media, and profile/search performance metrics.

Dynamic updates should be selective and governed. Automation capability must be verified per platform before implementation.

## Required future matrix

`APPLICATION -> HOST -> ENVIRONMENT -> REPOSITORY/PATH -> DOMAIN -> DATA OWNER -> BUILD TRIGGER -> ROLLBACK -> COST CLASS -> STATUS`