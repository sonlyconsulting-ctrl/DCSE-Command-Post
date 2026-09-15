# DCSE Platform Doctrine, Product Start Gate, and Shared Media Foundation Receipt

**Task ID:** DCSE-V72-PRODUCT-MEDIA-BOOTSTRAP-20260915-01  
**Parent Task ID:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02  
**Date:** 2026-09-15  
**Lane / Entity:** SC / DCSE Command Post  
**Authority:** DCS Level 0  
**Status:** CANDIDATE PENDING EXACT-HEAD GOVERNANCE VALIDATION

## 1. Platform doctrine reconciliation

The GitHub, Vercel, and Supabase platform controls are separate subordinate platform doctrines. They are not combined into one doctrine file and are not assigned new D-numbers.

- GitHub: `governance/v7.2/platforms/github/DCSE_GITHUB_AGENT_PLATFORM_DOCTRINE_v1.md`
- Vercel: `governance/v7.2/platforms/vercel/DCSE_VERCEL_AGENT_PLATFORM_DOCTRINE_v1.md`
- Supabase: `governance/v7.2/platforms/supabase/DCSE_SUPABASE_AGENT_PLATFORM_DOCTRINE_v1.md`

Controlling numbered doctrine remains:
- GitHub: D22, D05, D04, D21, D03
- Vercel: D20, D21, D22, D05
- Supabase: D15, D22, D21, D05

The shared `execution/DCSE_PLATFORM_EXECUTION_PROFILES_GITHUB_VERCEL_SUPABASE_v1.md` remains the common execution envelope. It does not replace the separate platform doctrines.

Masterclass/annotated-source material remains instructional and separate from doctrine.

## 2. Product Start Gate

D20 is amended to insert the Product Start Gate before material Build. New controlling subordinate standard:

`governance/v7.2/product/DCSE_PRODUCT_START_GATE_AND_BUILD_DECLARATION_STANDARD_v1.md`

Required start-state review includes product identity, entity/lane, audience/persona, URL/destination, CTA/conversion, brand/voice/visual identity, current persona/product imagery, backgrounds/source/reference assets, media manifest, commercial/package state where applicable, architecture/integrations, measurement, QA/accessibility, promotion authority, and rollback.

Missing mandatory inputs that would force invention or avoidable rework trigger:

`DCS_E_PRODUCT_START_ESCALATION`

## 3. Shared Media Governance

New standard:
`governance/v7.2/media/DCSE_SHARED_MEDIA_ASSET_STANDARD_v1.md`

New schema:
`governance/v7.2/media/DCSE_MEDIA_ASSET_MANIFEST_SCHEMA_v1.json`

Control model:
- GitHub = versioned control/index, manifests, hashes, provenance, rights, prompts/scripts/project metadata.
- SC-Command-Post Supabase Storage = governed binary media surface.
- DCSE-DDNA = authority/registry references, not large binary storage.
- Tribunal = material governance/evidence.

## 4. Shared Media Runtime Foundation

**Supabase project:** SC-Command-Post `nevgdyfpxdaloacuutal`  
**Migration:** `20260915174832_dcse_shared_media_asset_foundation`

Created:
- private bucket `dcse-media-assets`;
- schema `dcse_media`;
- service-only table `dcse_media.asset_registry`.

Verified:
- bucket is private;
- RLS enabled on registry;
- `anon` schema usage = false;
- `authenticated` schema usage = false;
- `anon` SELECT = false;
- `authenticated` SELECT = false;
- `service_role` SELECT = true.

No anonymous/authenticated Storage object policy was opened. Agent/human binary retrieval remains broker/server mediated until an explicit participant identity/access contract is implemented.

The first migration attempt failed because a COMMENT targeted the Supabase-owned `storage.buckets` table. The transaction rolled back completely. The corrected migration did not alter ownership/platform schema and succeeded.

Supabase advisor reports `RLS enabled, no policy` as INFO for `dcse_media.asset_registry`. This is intentional for its `INTERNAL_SERVER_ONLY` design with no client grants.

## 5. Initial Product Rollout

### Tedo's Sports Lounge
- repo: `sonlyconsulting-ctrl/SC-TedoSportsLounge`
- PR: #4
- current media indexed: 1
- verified existing production URL: `https://consumer-shell-seven.vercel.app`
- DCS-E findings: persona images, background/source set, complete brand pack not yet verified.

### SC Video Tool App
- repo: `sonlyconsulting-ctrl/SC-Video-Tool-App`
- PR: #2
- current media indexed: 0
- verified development surface: AI Studio link in repository README
- DCS-E findings: production/public URL, persona images, background/source set, brand pack.

### Mental Ingenuity
- repo: `sonlyconsulting-ctrl/ctj-mental-ingenuity`
- PR: #2
- current media indexed: 40
- existing corpus includes images, audio, and opening video.
- DCS-E findings: release URL unresolved, product/persona-image requirement requires review, media rights/provenance require manifest review.

Current Git assets are indexed by repository path, Git blob SHA, and byte size. Exact binary SHA-256 and rights/provenance remain pending and are not falsely asserted.

## 6. Scope boundaries

Not performed:
- no public release;
- no Vercel deployment;
- no secret handling;
- no PS content ingestion;
- no public/authenticated media-bucket access;
- no deletion or migration of existing product media binaries out of GitHub;
- no assertion that the CTJ family has one canonical repository.

## 7. Exit criteria

Before COMPLETE:
1. exact-head v7.2 governance validation passes;
2. Command Post PR merges to `main`;
3. main readback passes;
4. promoted standards are reconciled into DCSE-DDNA;
5. product manifest PRs are validated/merged or explicitly held with reason;
6. media foundation is read back and evidence retained.

**Structure Precedes Scale.**
