# Tribunal Receipt — Family Product Line / Vow & Go Integration

Date: 2026-07-16  
Agent: ChatGPT  
Branch: `family-product-line-v1`  
Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`

## Authority and release posture

Status: `MVP INTEGRATION CANDIDATE — PENDING APPROVAL`

This receipt does not promote the application to production authority. It records the Supabase schema expansion and Git application-integration work completed during the session.

## Supabase runtime

Project: `DCSE-Family-Product-Line`  
Project reference: `ajwqmgwjtxonhkvngoca`  
Region: `us-east-2`

Applied migration:

- `vow_go_application_support_v1`

Added Vow & Go application-support tables:

- `family_vow_go.wedding_settings`
- `family_vow_go.wedding_events`
- `family_vow_go.vendors`
- `family_vow_go.budget_items`
- `family_vow_go.guests`
- `family_vow_go.music_items`
- `family_vow_go.external_integrations`
- `family_vow_go.content_chapters`
- `family_vow_go.admin_feedback`

RLS posture:

- Product members may read authorized records.
- Owner, couple administrator, and planner may create and update planning records.
- Owner and couple administrator control destructive deletion.
- Feedback submitters may submit their own feedback; product administrators may review it.
- No service-role key is present in client code.

## Git application build

Application path:

`v6.9/05_Products/Family_Product_Line/Vow_And_Go/`

Files:

- `index.html`
- `config.js`
- `vow-go-supabase.js`
- `README.md`

Features represented:

- Wedding planning assistant positioning
- Bride, groom, and planner administration
- Public, moderated, or private publication decisions
- Vendor and budget planning categories
- DJ, flower, accessibility, dietary, medical, childcare, travel, and lodging considerations
- Supabase guest upload and moderation posture
- Google Drive and Dropbox administrator planning links
- Spotify, Pandora, Apple Music, YouTube, and licensed-upload music options
- “Power of Love” as an emotional reference only, not bundled media
- Cabo-to-Hawaii visual transition direction
- Administrator-controlled wedding-date background
- Future/announced/open honeymoon state
- Feedback records plus email preparation to `sonlyconsulting@gmail.com`

## Known limits and stop gates

- The committed `index.html` is an integration shell derived from the supplied concept, not a line-for-line production conversion of the full 72 KB source mockup.
- Custom schemas must be exposed to the Supabase Data API or mediated through public RPCs/views before browser integration will function.
- Bride, groom, planner, contributor, and viewer Auth accounts have not been created.
- The Akira and Connor product instance has not been seeded because real-user ownership must be established first.
- Real JWT role testing, file upload testing, moderation testing, signed URL testing, and email delivery testing remain pending.
- No deployment or public release was authorized.

## Promotion requirements

1. Resolve custom-schema API mediation.
2. Create real administrator accounts.
3. Seed the product instance and memberships.
4. Execute real-session RLS positive and denial tests.
5. Validate Supabase Storage upload, review, publication, and deletion.
6. Complete responsive, keyboard, reduced-motion, privacy, and retention review.
7. Obtain explicit approval before merge and deployment.
