# Vow & Go repository guidance

- Preserve Vow & Go as a wedding experience platform with optional professional planning administration.
- Keep `experience_only` as the default product mode. Disabled modules are hidden but their code and data are retained.
- Every live query and mutation must verify active product-instance membership and engagement scope. Never trust a client-supplied engagement ID without server verification.
- Keep custom schemas outside direct browser exposure. Prefer allowlisted `public` RPCs using `SECURITY INVOKER`; keep RLS authoritative.
- Use only the Supabase publishable key in browser code. Never commit service-role credentials, email-provider secrets, shared admin passwords, or invitation plaintext.
- Keep private media in private Storage. Measurement and fitting media defaults to private and requires participant knowledge and permission.
- Platform ownership does not imply private engagement access.
- Use the exact navigation titles defined in `app-data.js`, including `Settings & Access`.
- Do not implement GPS, browser geolocation, live/background tracking, route tracking, proximity alerts, check-in coordinates, or automatic venue-location detection.
- Do not attach a production domain, overwrite another DCSE product, weaken RLS, delete production data, or merge without passing tests and documented security review.
- Run `npm.cmd run test:unit` and `npm.cmd run test:browser` on a supported Node 20/22 runner before merge.
- Use the phrase “Designed to target accessibility standards.” Do not claim formal compliance without an audit.
