# ESCD Save Chat and Saved Chats repair

Task: `SC-ESCD-CHAT-PERSISTENCE-20261019-01`  
Lane/entity: SC / ESCD  
Handoff: `HO-SC-ESCD-CHAT-20261019-01`  
State: CANDIDATE / PARTIAL — source verified; authenticated deployment verification pending.  
Authority: DCS repair instruction in the current session. Production promotion requires separate DCS Level 0 authorization.

## Preflight and authoritative baseline

- Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`.
- Production source branch: `main`; inspected source/base commit: `fe308859cb694a1ea44eccfcdc81c9b3cbdd3fd0`.
- Production alias: `https://sc-escd.vercel.app`; deployment: `dpl_4octnuCf1RnfVoTzw3hBnbELeGLS`, READY. These are observed preflight values, not a new release.
- Vercel project: `sc-escd` / `prj_TfGqYXFwkLfaZth644kXLn48CMVR`; team: `team_g4aI8rT2IsL2OCR3pYA65141`.
- Root `vercel.json` routes `/escd/app` to `apps/escd/web/mvp.html`; `/api/mvp/*` uses the root `api/mvp.py` adapter and `apps/escd/api/mvp.py` handler.
- Read `AGENTS.md` and the relevant v7.3 Master Profile authority, evidence, and database provisions. The repository identifies v7.3 as operative. No controller was adopted, promoted, or edited by this repair. Cross-system governance synchronization remains unverified.
- Work isolated on `feat/SC-ESCD-CHAT-PERSISTENCE-20261019-01-save-restore` from inspected `main`.
- Supabase MCP read-only inspection of `SC-Command-Post` (`nevgdyfpxdaloacuutal`) verified `dcse_cp.escd_items`, unique `item_key`, JSONB `source_refs`, owner default `auth.uid()`, authenticated SELECT/INSERT/UPDATE grants, and enabled/forced RLS. No migration, policy, grant, user, or production record was changed. The inspected project had zero `escd_saved_chat` records. The deployment's environment-to-database mapping was not read from secret environment values; confirm it during authenticated preview verification.

## Findings and choice

The old browser save request contained only an ID and title. The handler tried to save completed turns from a process-local cache, which can be empty on another serverless worker. Provider failures never become completed turns. The existing save key included a timestamp, causing a fresh insert each time. Saved Chats displayed raw records without opening/restoring them. The old save/list path used a service configuration rather than the caller's RLS client and swallowed listing failures.

Compared approaches: retaining the cache as save authority would remain unreliable across workers; adding a new conversation schema would require database work outside this repair. The selected approach saves explicit browser transcript snapshots in the existing table using the authenticated repository connection. Provider routing and configuration remain unchanged.

## Changed files

| File | Purpose |
| --- | --- |
| `apps/escd/web/mvp.html` | Send the transcript on save; restore saved history and ID; open saved chats; serialize busy operations; preserve content on persistence failures; generate unique new-thread IDs. |
| `apps/escd/api/mvp.py` | Route save/list/open through authenticated persistence; attach verified caller ID; restore saved snapshots on refresh; seed restored continuation history in a user-scoped cache. |
| `apps/escd/runtime/saved_chats.py` | Validate snapshots; read legacy turns; scope record queries by caller and source; use stable per-user/thread keys; update existing rows; propagate failures without false success. |
| `apps/escd/tests/test_saved_chat_persistence.py` | Persistence, cold-cache, ownership, failures, legacy, JWT, and HTTP boundary tests. |
| `apps/escd/tests/test_chat_browser.cjs` | Reproducible browser workflow checks with a simulated persistence adapter. |
| `apps/escd/tests/build_chat_preview.py` | Refresh the standalone UI review artifact from the actual application source. |
| `apps/escd/docs/previews/chat_persistence_preview.html` | Zero-localhost interactive review preview; visibly marked as simulated; never contacts production. |
| `apps/escd/docs/CHAT_PERSISTENCE_REPAIR_20261019.md` | Evidence, limitations, deployment recommendation, and rollback handoff. |

Existing snapshots are not deleted or bulk-converted. Legacy snapshots can be read and updated in place. Provider error notices retain an explicit error flag and are preserved in saved history; they are excluded from model context on continuation. The caller's user messages remain saveable even if a provider never returned a valid answer.

## Validation closeout

- `python -m pytest apps/escd/tests -q`: **108 passed**, including the existing regression suite and 14 new persistence cases.
- Python compilation, inline JavaScript parsing, and `git diff --check`: pass.
- Chromium browser workflow: **PASS** for empty messaging, multiple turns, save, refresh restore, listing/opening, repeat save without duplicate rows, preservation of provider-error history, outage failure, missing record, expired-session content preservation, new browser-session listing/restoration, and mobile horizontal fit/control visibility.
- Browser checks exercise the actual UI and a simulated adapter. Python tests exercise the persistence service and real HTTP handler with a controlled repository double. They do **not** constitute a live authenticated Supabase write/read or real two-account certification.
- Standalone preview checked at 1280×900 and 390×844. The runtime Chromium package's browser download failed; the checks passed using Chromium Headless Shell 134 from Playwright 1.51.1 via `PLAYWRIGHT_CHROMIUM_EXECUTABLE`. No application dependencies were changed.

Reproduce:

```bash
python -m pytest apps/escd/tests -q
python apps/escd/tests/build_chat_preview.py
node apps/escd/tests/test_chat_browser.cjs
```

The browser command requires Playwright and its Chromium installation. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` optionally selects an existing Chromium executable. The preview is a review artifact with demo-only storage, not a deployment/runtime acceptance test.

## Security finding and release exit criteria

The existing RLS SELECT predicate is `dcse_cp.is_dcs_owner()`, permitting reads by authorized DCS operators generally. Its write check also requires `created_by_user_id = auth.uid()`. The repaired API adds owner predicates to save/list/open queries and uses the caller JWT, with no service-role fallback. Tests verify API ownership filtering and refusal to open/update another user's ID.

Strict per-user isolation through direct PostgREST access is **not certified** by that existing SELECT predicate. If multiple authorized operators require isolation at that layer, a separately reviewed and approved RLS change is necessary. No policy was changed here.

Before release:

1. Verify the exact candidate commit and `sc-escd` preview deployment mapping.
2. With a real authenticated session, save multiple turns, refresh, reopen, update, and start a new authenticated session to reopen again. Confirm the deployment uses the inspected database.
3. Exercise a real provider failure after valid turns; save/reopen the retained transcript.
4. Verify expired session and failed persistence retain visible content.
5. Verify unauthorized access and two-account behavior with authorized test identities; review the direct-access RLS finding with DCS.
6. Obtain the repository-required independent audit/signoff and DCS Level 0 production authorization. Do not infer either from local tests or a READY preview.

## Deployment recommendation and rollback

Recommend **preview review only / production HOLD**. Do not merge to `main` or promote a deployment until exit criteria and DCS Level 0 authorization are recorded. A branch push may produce Git-integrated preview deployments; it is not production promotion.

Before a later authorized release, record the current production deployment ID again; it may have changed since preflight. Stage/test the intended production build under the approved workflow and promote only after authorization.

If rollback is authorized after release, restore the recorded prior production deployment for `sc-escd` (preflight candidate: `dpl_4octnuCf1RnfVoTzw3hBnbELeGLS`) and verify alias readback. Source rollback is a new controlled branch reverting the repair commit, followed by normal review. No schema rollback is needed. Do not delete or downgrade saved records. Older code cannot fully use version-2 snapshots, so preserving records does not imply old runtime compatibility; reapplying the repair restores their reader.

Candidate commit and branch evidence are supplied with the final handoff and in GitHub history; this document does not self-assert its own commit SHA.
