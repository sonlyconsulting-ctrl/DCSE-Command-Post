# Review Vow & Go on Windows

1. Download or clone `sonlyconsulting-ctrl/DCSE-Command-Post`.
2. Open `v6.9\05_Products\Family_Product_Line\Vow_And_Go`.
3. Double-click `START_VOW_AND_GO.cmd`.
4. The default browser opens automatically, normally at `http://127.0.0.1:8080/`.

If 8080 is occupied, the launcher selects the first available port through 8099 and prints the exact address. It resolves its own folder, never serves from `C:\Windows\System32`, prefers Python 3, and falls back to the included Node static server. If neither runtime is available, it displays a clear installation message.

To stop the server, return to its command window and press `Ctrl+C`, or close that command window.

## Credential-free review

Open **Sign In & Access**, then select any role fixture. No signup or credential is needed for review fixtures. Role and product-mode links can also be opened directly; examples are in `HOSTED_PREVIEW.md`.

Fixture changes use browser local storage and remain separated by wedding workspace. Clear site data to reset fixtures. Preview feedback is intentionally not submitted or stored.

## Governed sign-in

Live access requires an individual Supabase Auth account and active product-instance membership. Shared admin passwords and client-side service-role credentials are not supported. Password reset and safe sign-out are available in **Sign In & Access**. Secure invitation-token review is represented, but real tokens must be issued by an authorized engagement administrator.

## Known review limitations

- Real administrator accounts, memberships, invitation tokens, and cross-role fixtures must be provisioned before live RLS testing.
- Feedback records are live-capable; email delivery additionally requires `RESEND_API_KEY` and `VOW_GO_FEEDBACK_FROM` as Supabase Function secrets.
- Private media needs authenticated Storage access and real test files.
- Browser GPS, live tracking, route tracking, proximity alerts, and location history are deliberately absent.
- Designed to target accessibility standards. Formal compliance requires a separate audit.
