# DCS Medicare Decision Center: ESCD Product Registration

Task ID: `DCS-MEDICARE-APP-20261019-01`  
Handoff: `DCS-MEDICARE-APP-HO-20261020-01`  
Lane: DCS Private Personal Research (PPR) / ESCD integration  
Date: 2026-10-20  
Status: PRIVATE_PREVIEW_CANDIDATE / UNSYNCHRONIZED until DCS review and mainline approval

## Directive and preflight
DCS instructed the assistant to add DCS Medicare to the ESCD Products view. Source application: the local-first, single-file DCS Medicare Decision Center v1.1 HTML preview built in the conversation. No protected hosted URL, live plan feed, production credentials, or DCS production deployment approval was supplied for this change. Historical chat claims are not sufficient authority for medical coverage or plan eligibility.

## Implemented in the candidate branch
- Added one `dcs_medicare` product to `apps/escd/runtime/escd-products-catalog.json`, with a byte-identical fallback mirror at `content/escd-products-catalog.json`.
- Updated product count to 9 and recalculated all category counts, including the preexisting mismatch in the Flagships count.
- Added `personal_private` category, displayed in ESCD Products as "Private Personal Tools".
- Added a review-only launch experience for product records marked `PRIVATE_PREVIEW_CANDIDATE`. It opens the specifications dossier, without showing a false live-app link or embedding an unrelated enterprise canvas.
- Preserved existing product records, routes and functionality. No schema, RLS, authentication, provider or payment changes.

## Product classification and available capabilities
Product name: DCS Medicare Decision Center
Code: DCS-MEDICARE
Privacy: PRIVATE_PERSONAL_RESEARCH
Preview: v1.1, local self-contained HTML only
Scope: evidence-labeled Medicare plan comparison; premium/Part B/giveback cost scenarios; preventive service reference; appointment and document review checklist; private session-only export.

No existing plan recommendation is automatically verified by this catalog entry. The screenshot-supported 2026 No Rx plan and earlier assistant-proposed alternatives retain separate provenance.

## Privacy and access
- No Medicare number, SSA benefit letter, full personal name, birthdate, street address, or API credential is copied to GitHub product metadata.
- The source preview is a conversation artifact, not a production app. Do not insert `sandbox:` or `file:` URLs into ESCD's live catalog.
- Before a live app URL can be supplied: verify authenticated server-side access at the destination, per-user record isolation, security headers, correct caching semantics, no client-side secrets, and private storage boundaries.
- Product metadata is safe for the currently authenticated ESCD catalog API; do not add private beneficiary records to that API response.

## Candidate validation (2026-10-20)
- Both catalog JSON mirrors parse successfully and match.
- Nine unique products with exactly one `dcs_medicare` entry.
- Seven category counts agree with computed membership; 5 existing flagged flagships.
- UI JavaScript parses as a complete block.
- Review-only candidate has no live URL and cannot claim an embedded live app.
- No private identifier or credential marker found in added catalog metadata.

Not yet verified: full ESCD browser/E2E regression after application integration; current production product list; authenticated hosted app route; official 2027 plan comparisons.

## Exit gates and deployment
1. DCS reviews candidate branch/PR.
2. Select and implement an authenticated Medicare application route (recommended: ESCD launcher to separately protected application), without exposing personal documents or secrets.
3. Validate plan source currency and costs, accessibility targets, responsive operation, privacy and regression suite.
4. Obtain separate explicit production promotion authorization, then record release commit, preview deployment, production alias, acceptance, and rollback reference.

Rollback for this scoped change: revert the catalog entries, category filter, and review-only UI patch on a controlled branch. Existing ESCD product records and saved data remain unchanged.
