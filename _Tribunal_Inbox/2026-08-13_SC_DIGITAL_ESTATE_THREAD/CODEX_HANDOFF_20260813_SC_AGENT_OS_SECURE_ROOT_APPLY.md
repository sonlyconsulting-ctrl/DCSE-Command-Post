# Codex Apply Handoff: SC Agent OS Secure Root

Use the task packet `CODEX_TASK_20260813_SC_AGENT_OS_SECURE_DEPLOYMENT_RATIONALIZATION.md` as controlling implementation instructions.

A partial implementation has been staged on branch `test/sc-agent-os-doc-skip-20260813`:

- added `apps/sc-agent-os/api/secure.js`, adapted from the current repository-root secure gateway so the secure gateway can live inside the dedicated SC Agent OS root;
- production is still frozen;
- `apps/sc-agent-os/vercel.json` has NOT been changed because the connected GitHub mutation surface blocked that deployment-config write.

Codex shall inspect and validate the staged `secure.js`; do not assume it is correct because it was generated from the current root wrapper. Complete the refactor only after testing.

Minimum remaining implementation:

1. review `apps/sc-agent-os/api/secure.js` against root `api/index.js` and `apps/sc-agent-os/api/index.js`;
2. correct any drift or missing behavior;
3. change `apps/sc-agent-os/vercel.json` so all public/API routes enter the secure gateway, not `api/index.js` directly;
4. add executable tests for unauthenticated login gating, authenticated delegation, password recovery, security headers, server-managed provider credentials, and no direct Mission Control bypass;
5. run secret/client-storage scan;
6. determine `sc-command-post` disposition;
7. open a PR and stop before production promotion.

Do not unfreeze or promote production. Do not modify Supabase schema/data. Do not touch Mental Ingenuity or the disconnected Vercel projects.
