# TRIBUNAL — Vow & Go Major Repair Build Receipt

Date: 2026-07-16

Authority: DCS/DCSE execution directive

Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`

Branch: `codex/vow-and-go-major-repair`

Supabase project: `DCSE-Family-Product-Line` (`ajwqmgwjtxonhkvngoca`)

Release posture: review build; no production-domain cutover
Hosted review: `https://vow-and-go-review.vercel.app`
Deployment: `dpl_4ADqDn1VzmkqRqfnJ2Y6rekAY2Nw` (READY)

## Completed

- Rebuilt the static application as a schema-driven, role-separated wedding experience and command-center workspace.
- Added three product modes, eight review identities, engagement selector, role-specific navigation, three themes, and exact title consistency.
- Added Wedding Party Hub, private measurement/fitting records and consent text, role schedules, destination guide, FAQ, secure invitation model, and reusable template safeguards.
- Added operational create/read/update/archive/delete/restore, search, sort, validation, activity, imports, and exports across comparable modules.
- Applied five additive Supabase migrations for governed RPC access, modular records, RLS, invitations, templates, feedback delivery, engagement selection, and platform context.
- Deployed `vow-go-feedback` Edge Function version 1 with JWT verification.
- Supabase security advisor after migrations: zero findings.
- Preserved private Storage and removed duplicate permissive policy warnings introduced by predecessor policies.
- Preserved local Windows one-click launch and isolated Vercel review configuration.
- Published the repaired build to the existing isolated Vercel review alias; HTTP 200 and security headers verified with SSO login absent.
- Added unit, security-contract, responsive browser, role, mode, CRUD, isolation, privacy, focus, reduced-motion, and axe tests.

## Evidence

- Unit/security-contract tests: 11 passed, 0 failed.
- Local server: HTTP 200.
- Supabase migrations: applied successfully.
- Edge Function: ACTIVE, JWT verification enabled.
- Security advisor: 0 findings.
- Browser test source: committed; current desktop session’s Playwright driver launched Chromium but did not return results. CI rerun is required before merge.

## Human actions required

1. Provision individual Supabase Auth users and active product-instance memberships for the role matrix and two test weddings.
2. Configure `RESEND_API_KEY` and `VOW_GO_FEEDBACK_FROM` Function secrets, then verify delivery.
3. Run the committed Playwright matrix on Node 20/22 and record results.
4. Test real invitation expiry/revocation, private signed media, and cross-engagement denial.
5. Review the isolated Vercel preview and approve or reject production promotion separately.
6. Do not merge until required checks pass and a reviewer clears remaining blocking defects.

GPS and live-location features remain explicitly deferred. No production data was deleted, no RLS was weakened, no secret was committed, and no production domain was changed.

Designed to target accessibility standards. Formal compliance is not claimed.
