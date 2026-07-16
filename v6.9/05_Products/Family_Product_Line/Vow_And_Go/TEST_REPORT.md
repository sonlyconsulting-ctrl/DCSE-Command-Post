# Vow & Go Test Report

Date: 2026-07-16

Environment: Windows; Node.js 25.8.2; local HTTP server; Supabase project `ajwqmgwjtxonhkvngoca`.

## Automated result

`npm.cmd run test:unit`: **11 passed, 0 failed**.

Covered: role capability helpers, output escaping, HTTPS/provider validation, file-name normalization, countdown behavior, publishable-key-only client, RPC-only custom-schema access, server-derived membership boundary, private Storage contract, engagement-scoped repair schema, hashed invitations, template privacy guard, and Windows launcher behavior.

## Application test matrix

Implemented Playwright coverage in `tests/` for:

- Desktop 1440×1000, tablet 900×1180, and mobile 390×844.
- Signed-out approved-content filtering and no horizontal overflow.
- Planner full-command-center navigation.
- Create, update, archive, restore, search, sort, import, and export controls.
- Two-workspace engagement isolation.
- Experience-only, coordination, and full-command-center module visibility.
- Couple Owner, Couple Collaborator, Planner, Platform Owner, Guest Viewer, Guest Participant, Trusted Contributor, and signed-out navigation.
- Wedding Party Hub and fitting-media consent text.
- Guest self-service without a guest-list disclosure.
- Preview feedback exact non-persistence message.
- Unsafe URL rejection, keyboard focus, reduced motion, and automated axe scan.

Current machine limitation: the Playwright CLI launched Chromium but its driver process did not return results under this desktop session. The exact compatible Chromium build was installed, tests remain committed, and this is recorded as an environment block—not a passing browser assertion. Unit/security tests and local HTTP `200` completed. Browser matrix must run in GitHub Actions or another clean Node 20/22 runner before merge.

## Supabase validation

- Migrations applied successfully: browser RPC v1, major repair v2, advisor cleanup, engagement selector, platform context.
- Edge Function `vow-go-feedback` version 1 deployed ACTIVE with JWT verification enabled.
- Security advisor after migration: **0 findings**.
- Performance advisor: new foreign-key findings remediated; remaining Vow & Go notices are expected unused-index INFO notices on zero-row tables.
- No real role accounts or invitation tokens were available, so authenticated cross-role and cross-engagement runtime denial tests remain blocked.

## Not claimed as passed

- Real-user Supabase role matrix and password-reset email receipt.
- Invitation acceptance/expiry/revocation using issued tokens.
- Private media upload, moderation, signed read, restore, and deletion using real files.
- Feedback email delivery (provider secrets not configured).
- CI browser matrix, dependency audit, or formal accessibility/privacy/legal audit.

Designed to target accessibility standards. Formal compliance is not claimed.
