# Tribunal Topic Record: SC Wix Hybrid Architecture and Visual Direction

**Record date:** 2026-08-13  
**Lane:** SC  
**Status:** DISCUSSION RECORD / PREIMPLEMENTATION  
**Implementation authority:** NONE

## Finding

The strongest current architecture hypothesis is not "Wix versus HTML." It is one SC experience rendered by multiple technologies under a shared design contract.

The working pattern is:

`Wix Header -> Wix Hero/Orientation -> Custom HTML/App Experience Where Valuable -> Wix Conversion/Continuation -> Wix Footer`

This is a starting hypothesis, not a mandatory pattern for every destination.

## Why the model emerged

DCS proposed that the first one or two landing-page sections for SC, SS, and related destinations remain Wix pages and then move into HTML/custom experiences. The discussion refined this into a renderer-independent experience model so visitors do not perceive a platform transition.

The strategic distinction is:

- use familiar UX conventions where familiarity improves trust;
- use distinctive design and software behavior where SC earns attention.

"More mainstream" should therefore not mean generic. It should mean recognizable navigation, hierarchy, mobile behavior, CTA patterns, accessibility, and page pacing combined with differentiated editorial composition, interaction, motion, and product experiences.

## Canonical shell requirement

A shared SC Design Contract should govern logo treatment, header, navigation, footer, typography, colors, spacing, content widths, buttons, breakpoints, motion, analytics, accessibility, and product-parent relationship.

Renderer rules:

- Wix native pages use the Wix shell directly.
- Embedded/custom modules do not render a second full header/footer.
- Full application surfaces may use a reduced application header while preserving obvious SC parent identity.
- External applications consume the same design tokens and visual rules.

## Wix platform posture

DCS reported:

- current production entitlement is Classic Editor Core;
- no Wix Studio subscription is currently intended.

Working rule:

**Target architecture must remain executable on the current Classic Editor Core environment unless a separately approved cost/benefit case justifies a different Wix tier.**

Historical Studio sites may be inspected for design patterns and reusable visual thinking. They should not create a target dependency on Wix Studio.

## Historical design archaeology

Old SC and SS Wix generations should be scored for human visual rhythm, whitespace, page pacing, hero credibility, photography, typography, navigation simplicity, section transitions, mainstream credibility, distinctiveness, mobile behavior, and reusable motifs.

The objective is to recover durable visual intelligence, not restore an old site.

## Renderer candidates

- `WIX_NATIVE`
- `WIX_VELO`
- `WIX_CUSTOM_ELEMENT`
- `WIX_IFRAME_BOUNDED`
- `STATIC_HTML`
- `EXTERNAL_APP_VERCEL`
- `EXTERNAL_APP_NETLIFY`
- `SUPABASE_BACKED_APP`
- `HEADLESS_OR_API_DRIVEN`
- `RETIRE`

The decision should be made per experience or section rather than forcing every property onto the same renderer.

## Current candidate by destination

### Sonly Consulting
Wix-dominant public/business shell with custom software surfaces where interaction creates material value.

### Smoove Spots
Wix/editorial-dominant storytelling shell with custom HTML/application surfaces for immersive stories, experiments, galleries, media, and interactive narrative.

### Mental Ingenuity
Wix entry/orientation plus a custom application experience, likely with persistent application data outside Wix where appropriate.

### Wedding Planner / Vow & Go
App-first. Wix is not presumed to be the primary application renderer.

### BrideGroom KeepSake
Likely hybrid: editorial/presentation composition plus application behavior for galleries, timelines, uploads, chapters, and media.

## Risks to prevent

- Wix page -> unrelated-looking HTML -> Wix again;
- duplicate headers/footers;
- CSS-token drift;
- full-site iframe shells;
- data trapped in Wix simply because the page is hosted there;
- rebuilding existing Velo before source inspection;
- buying Studio to solve a problem Classic Editor plus custom components can solve.

## Required decision artifacts before implementation

1. Design Contract.
2. Experience/Renderer Matrix.
3. Wix disposition matrix.
4. Visual archaeology comparison.
5. Velo/source audit.
6. Representative hybrid prototype on a non-production surface.
7. Mobile, accessibility, performance, security, and visual QA.
8. DCS implementation decision.