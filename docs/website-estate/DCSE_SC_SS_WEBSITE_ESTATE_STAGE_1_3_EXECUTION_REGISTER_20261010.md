# SC/SS Website Estate, Stages 1-3
Task: DCSE-SC-SS-SITES-20261010-01 | Date: 2026-10-10 | State: PARTIAL | Lane: SC/SS; CTJ/SE separately routed.
Authority: v7.3 OPERATIVE by DCS Level 0 continuity designation 2026-09-21; inherited v7.2 R5 controller. Runtime synchronization is not established by this record.

## Stage 1: Estate registry
| Lane | Public domain | Vercel project | GitHub candidate | Historical Wix sources | Status |
| SC | https://www.sonlyconsulting.com; apex redirects 308 to www | sc-command-post (prj_a9pbcrfvQczbmH2Cr1S2Q08p2975) | https://github.com/sonlyconsulting-ctrl/sc-website | Sonly Consulting, SC Main, SC.com Rebuild Staging 20260813, SC Published V1 07212025 | PARTIAL; deployed repo binding and ESCD link unknown |
| SS | https://www.smoovespots.com; apex verified, redirect not configured | smoove-spots-v2 (prj_pctdasKxkRfN8cGYeebyAMrktCNw) | https://github.com/sonlyconsulting-ctrl/ss-website | Smoove Spots, SmooveSpots_v1 | PARTIAL; deployed repo binding and ESCD link unknown |
| CTJ/SE | Exact website domain unknown | Not verified | https://github.com/sonlyconsulting-ctrl/SC-CTJ (verified repo, not proven SE hero source) | N/A | PARTIAL; SE hero ownership and deployment need source mapping |

## Stage 2: Wix premium feature parity
DCS requirement: SC and SS retain or exceed historical premium Wix features under branded domains. Free-tier Wix may be used for bounded auxiliary functions when permitted. Feature inventory must inspect historical site and determine: original feature, proof, target equivalent, account entitlement, business owner, migration data, QA, retain/rebuild/replace/retire. Candidate categories (not claims of historic existence): forms, store, booking, membership, blog, chat, media, SEO, analytics, mobile/accessibility, security.

## Stage 3: destinations, copy and DDNA
Inventory SC home, LinkedIn, DCS Employment (separate route), enterprise, freelance, social/campaign; SS home, stories and social/campaign; standalone CTJ SE hero. For each: URL, audience, CTA, offer, D08 voice, D09 brand, source lineage, approved copy, rights, image/video/audio, DDNA reference, reviewer, QA.

## DDNA extraction candidates from DCS thread, unpromoted
- Premium Wix parity for SC/SS with own-domain Vercel delivery; free Wix optionally auxiliary. VERIFIED DCS instruction, 2026-10-10; SC/SS.
- SE produces CTJ special edition hero for standalone CTJ website. VERIFIED DCS instruction; SC/CTJ. Exact source and URL unknown.
- LinkedIn/social/employment/enterprise/freelance destinations. VERIFIED DCS instruction; MIXED, enforce lane routing and PS exclusion.
- Media module includes video/images, potential audio/vocals/subtitles, DDNA-led voice and content. VERIFIED DCS requirement; implementation not verified.
- Stages 1-3 immediate; stage 4 media integration; stage 5 evidence/validation throughout. VERIFIED DCS instruction.

## Supabase insert preparation
No DB mutation performed. Inspect existing project, assets, tasks, DDNA schema/RLS and authorized rows; prepare idempotent mapping, validation, rollback and readback before writing. Proposed records are not authority.

## DCL
Applied: v7.3 continuity designation, D03/D05/D08/D09/D11/D12/D16/D18/D21 routing, lane separation, GitHub/Vercel/Wix evidence. Missing: historic Wix feature export, deployed Git binding, DDNA records, ESCD registry linkage, CTJ SE URL, independent validation. Contradiction: historic Wix hybrid design versus Vercel domain routing; reconcile by capability. Exit: stages 1-3 PARTIAL. No deployment, production mutation or promotion. DCS Level 0 gate retained.
