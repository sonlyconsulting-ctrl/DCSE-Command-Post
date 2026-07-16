# Vow & Go Security and RLS Review

Date: 2026-07-16

Supabase project: `ajwqmgwjtxonhkvngoca`

## Result

Supabase security advisor after migration: **0 findings**. Custom schemas remain outside direct browser Data API exposure. The browser uses allowlisted `public` RPCs with `SECURITY INVOKER`; RLS remains the authorization boundary.

## Controls verified or implemented

- Every new table has RLS enabled and explicit least-privilege grants.
- Product IDs supplied for mutations are accepted only after active membership verification; planner engagement selection cannot cross memberships.
- Platform Owner context returns no private engagement content. Operational support needs separate authorization and audit.
- Engagement invitations store token hashes, expiration, acceptance, and revocation state; plaintext tokens are not stored.
- Reusable template types are allowlisted and reject known personal-data keys.
- Operational records, activity, invitations, feedback delivery, and templates are engagement or owner scoped.
- Private wedding Storage remains non-public. Object paths begin with a product-instance UUID and reads are controlled by membership, uploader, moderation state, and role.
- Private fitting and measurement media is never automatically published.
- Client code contains only a publishable Supabase key; no service-role key or shared admin password is present.
- External URLs require HTTPS; provider links open separately and no provider OAuth is required.
- Rendered record content is escaped; dynamic SQL/table names are not built from browser input.
- Vercel headers deny framing, MIME sniffing, camera, microphone, geolocation, and payment access. CSP limits scripts and connections.
- Feedback Edge Function requires JWT verification and forwards the caller token so RPC RLS applies. Email-provider secrets remain server-side.

## Storage/public-media posture

The bucket `family-wedding-private` is private. “Public” is a publication workflow state, not an anonymous bucket listing grant. Anonymous approved-gallery delivery would need a separately governed signed/public asset mechanism.

## Advisor follow-up

Foreign-key index notices introduced by this repair were remediated in `20260716231446_vow_go_major_repair_advisor_cleanup.sql`. Remaining Vow & Go performance notices are INFO-level unused-index notices expected on a new, empty dataset. Supabase remediation reference: <https://supabase.com/docs/guides/database/database-linter>

## Remaining live security tests

- Provision role-specific users and two isolated wedding workspaces.
- Execute authenticated owner/planner/collaborator/contributor/guest denial tests.
- Exercise invitation expiration/revocation and private signed-media URLs.
- Configure the email provider and verify delivery/bounce behavior.
- Conduct privacy, retention, legal, penetration, and formal accessibility audits before production release.

Designed to target accessibility standards. This review is not a formal compliance audit.
