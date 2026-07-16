# Vow & Go — Wedding Experience & Command Center

Status: major repair review build

Supabase: `DCSE-Family-Product-Line` (`ajwqmgwjtxonhkvngoca`)

Production cutover: not authorized

Vow & Go is a modular wedding experience platform with optional professional planning administration. It supports couples who already use another planner or planning application. Its visual direction moves from Cabo to a Hawaii celebration and future honeymoon chapters.

## Architecture

The app remains a lightweight static ES-module application: semantic HTML, responsive CSS, schema-driven UI, pinned local Supabase client, governed public RPCs, private Storage, and a JWT-protected feedback Edge Function. No framework or bundler is required for local or hosted review.

Browser code uses only the Supabase publishable key. Custom schemas remain outside direct browser exposure; RLS-aware `public` RPCs mediate access.

## Product modes

- `experience_only` (default)
- `coordination`
- `full_command_center`

Disabled modules are hidden from navigation, dashboard cards, and recommendations while their records and implementation remain preserved.

## Roles

- Platform Owner — templates, planner approval, licensing placeholders, support, and authorized audit; no automatic private wedding access.
- Planner / Command Center Admin — multi-engagement operational administration.
- Couple Owner — engagement authority, approvals, access, and major decisions.
- Couple Collaborator — delegated editing without ownership/security transfer.
- Guest Viewer — approved public/protected wedding content, no account required.
- Guest Participant — invitation-scoped RSVP, needs, guestbook, media, and poll participation.
- Trusted Contributor — authenticated assigned content and task contribution.
- Signed-Out User — approved guest experience only.

## Major modules

Dashboard; Our Story; Media & Gallery Portal; Wedding Tasks & Checklist; Vendors & Contracts; Budget & Payments; Guests & Wedding Party; Wedding Party Hub; Schedule & Timeline; Travel & Hotel; Destination & Local Guide; Music & Playlists; Communications & Notifications; Help & Guidance; Settings & Access; Feedback & Support.

Generic operational records provide create/read/update/archive/delete/restore, search, sort, validation, activity history, JSON export, and JSON/CSV import. Financial, guest, media, security, communication, and feedback records favor archive before deletion.

## Local review

Double-click `START_VOW_AND_GO.cmd`. See `REVIEW_ON_WINDOWS.md`.

## Development

```powershell
npm.cmd install
npm.cmd run serve
npm.cmd run test:unit
npm.cmd run test:browser
```

The launcher does not require npm. Development dependencies are pinned. Browser tests should run on Node 20 or 22 in CI.

## Database and function artifacts

- `20260716224000_vow_go_public_rpc_preview_v1.sql`
- `20260716224258_vow_go_major_repair_v2.sql`
- `20260716231446_vow_go_major_repair_advisor_cleanup.sql`
- `20260716231535_vow_go_engagement_selector_rpc.sql`
- `20260716231732_vow_go_platform_owner_context.sql`
- `supabase/functions/vow-go-feedback/index.ts`

All migrations were applied to the approved project. Security advisor result after application: zero findings. Real role users and email-provider secrets remain human provisioning steps.

GPS, geolocation, live/background tracking, route tracking, proximity alerts, check-in coordinates, and automatic venue detection are explicitly deferred. Ordinary addresses and HTTPS map links are supported.

Designed to target accessibility standards. Formal compliance requires a separate audit.
