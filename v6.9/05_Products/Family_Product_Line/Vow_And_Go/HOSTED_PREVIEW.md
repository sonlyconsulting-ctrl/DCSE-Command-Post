# Hosted Vow & Go Review

Isolated review project: `vow-and-go-review`

Stable review URL: <https://vow-and-go-review.vercel.app>

This app-local Vercel deployment does not target or overwrite `cp.sonlyconsulting.com`, another DCSE product, DNS, or a production alias. Vercel SSO protection is disabled only for this review project, as separately authorized; application roles and Supabase RLS remain in force.

## Role review links

- [Platform Owner](https://vow-and-go-review.vercel.app/?role=platform_owner)
- [Planner / Command Center Admin](https://vow-and-go-review.vercel.app/?role=planner&mode=full_command_center)
- [Couple Owner](https://vow-and-go-review.vercel.app/?role=couple_owner&mode=full_command_center)
- [Couple Collaborator](https://vow-and-go-review.vercel.app/?role=couple_collaborator&mode=coordination)
- [Guest Viewer](https://vow-and-go-review.vercel.app/?role=guest_viewer&mode=experience_only)
- [Guest Participant](https://vow-and-go-review.vercel.app/?role=guest_participant&mode=experience_only)
- [Trusted Contributor](https://vow-and-go-review.vercel.app/?role=trusted_contributor&mode=coordination)
- [Signed-Out User](https://vow-and-go-review.vercel.app/?role=signed_out&mode=experience_only)

## Product-mode links

- [Experience Only](https://vow-and-go-review.vercel.app/?role=planner&mode=experience_only)
- [Coordination](https://vow-and-go-review.vercel.app/?role=planner&mode=coordination)
- [Full Command Center](https://vow-and-go-review.vercel.app/?role=planner&mode=full_command_center)

Mode toggles hide disabled navigation, cards, and recommendations while retaining module code and engagement data.

## Deployment

From this application folder:

```powershell
vercel.cmd deploy --yes --project vow-and-go-review
```

Do not attach a production domain or overwrite another product project. Promotion requires a separate release authorization.
