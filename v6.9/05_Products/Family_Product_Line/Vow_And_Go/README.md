# Vow & Go — Wedding Planning Assistant

Status: `MVP integration candidate`  
Supabase project: `DCSE-Family-Product-Line` (`ajwqmgwjtxonhkvngoca`)  
Release authority: pending real-user onboarding, end-to-end upload testing, and approval.

## Product definition

Vow & Go is a wedding planning assistant, private event portal, family/friend contribution surface, and living keepsake. The planning core supports bride, groom, and authorized planner administration. The content arc moves from the Cabo San Lucas proposal through the Hawaii wedding, honeymoon, and later family chapters.

## Included in this build

- Supabase Auth session detection and product-scoped role resolution.
- Bride/groom/planner administration posture.
- Admin-controlled `public`, `moderated`, or `private` publication behavior.
- Wedding tasks, events, vendors, budget, guests, special needs, music references, external planning links, chapters, media moderation, guestbook, and feedback.
- Guest media intended for private Supabase Storage.
- Google Drive/Dropbox links intended for administrator planning files, vendor contracts, spreadsheets, and working documents.
- Music provider mix: Spotify, Pandora, Apple Music, YouTube, uploaded licensed audio, or curated links.
- “Power of Love” is recorded only as an emotional reference. Playback requires a licensed or provider-authorized source.
- Feedback saves to Supabase when authenticated and prepares an email to `sonlyconsulting@gmail.com`.
- Progressive Cabo-to-Hawaii visual direction and administrator-controlled countdown background.
- Honeymoon chapter supports future, announced, open, and archived states.

## Security posture

- No service-role key is present in client code.
- The committed key is a Supabase publishable client key.
- Authorization is enforced by PostgreSQL RLS, not by hidden UI elements.
- Shared production passwords shown in the source mockup are deprecated. Production access uses individual Auth accounts and product memberships.
- The application is designed to target accessibility standards; no formal accessibility audit has been completed.

## Run locally

Serve the directory with an HTTP server. ES modules will not run reliably from a direct `file://` URL.

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Required Supabase configuration

The custom schemas must be exposed to the Data API, or equivalent public RPC/view mediation must be added:

- `family_core`
- `family_vow_go`

Real users must be created through Supabase Auth and assigned to `family_core.product_memberships`.

## Promotion gates

1. Create bride, groom, and planner test accounts.
2. Create the Akira and Connor product instance.
3. Validate RLS with real JWT sessions.
4. Test media upload, signed read access, moderation, and deletion.
5. Test public/moderated/private transitions.
6. Test Drive/Dropbox links without exposing private credentials.
7. Test email feedback delivery.
8. Test mobile, desktop, tablet, TV/display, reduced motion, and keyboard navigation.
9. Complete privacy, retention, and content-release review.
10. Promote only after approval receipt.

The HTML provided in the source conversation remains the visual baseline. This build adds integration scaffolding and governance controls; it is not yet approved for public release.
