# Vow & Go feedback function

Authenticated feedback is stored through RLS-aware RPCs before email delivery is attempted.

Required hosted secrets:

- `RESEND_API_KEY`
- `VOW_GO_FEEDBACK_FROM` (a verified sender, for example `Vow & Go <support@example.com>`)

Supabase provides `SUPABASE_URL` and `SUPABASE_ANON_KEY`. The function deliberately uses the caller's Authorization header and never uses a service-role key.
