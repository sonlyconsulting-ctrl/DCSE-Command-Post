# ESCD-MVP-0.5 Build Receipt: Ollama provider and full record CRUD

Date: 2026-09-17
Lane: DCSE (internal)
Requested by: DCS, after reviewing production ESCD at sc-escd.vercel.app/escd/app
Scope: complete the current build phase using existing elements. Out of scope (next phase): adding models to the dropdown and expanding provider settings.

## Changes

1. Chat: Ollama added to the provider dropdown, status line and Provider settings (registry-driven, same Vault pattern as the other providers).
2. Tasks, Ideas, Knowledge, Assets now share one layout: search, Current/Archived/All filter, New, Refresh; each row opens a record editor (click title or Open).
3. Full CRUD on all four sections:
   - Create: New button (Tasks/Ideas quick-add forms kept).
   - Read: editor shows fields, ids and the full record.
   - Update: Save changes (only changed fields are sent). The browser prompt() title edit was removed.
   - Delete: Archive (Tasks, Ideas, Knowledge) and Retire (Assets). Governed and recorded; nothing is hard-deleted. The escd_items transition guard makes archive terminal for tasks and ideas.
4. Canonical registry records (read-only JSON) are adopted into live tables on first edit; the registry file is not changed.
5. Defect fixes found during the build:
   - Chat: runtime/mvp_data.py used datetime without importing it, so every successful provider reply failed with "name 'datetime' is not defined". Fixed and covered by test.
   - Tasks and Ideas were shown twice (live copy plus canonical copy). Dedupe now matches id and item_key. Expected counts: Tasks 65, Ideas 9 (were 119 and 18).
   - Mobile: the sidebar covered the page on phones (inline display:flex overrode the mobile rule). Fixed.
   - Lane firewall: the Assets list returned PS-Locked registry rows. They are now filtered server-side and asset writes reject PS lanes and tags.

## Database (applied to nevgdyfpxdaloacuutal)

Migration escd_provider_ollama_20260917: provider check constraint now allows 'ollama'; ollama row inserted.
Rollback: delete from dcse_cp.escd_provider_config where provider='ollama'; then re-create the check without 'ollama'.

## Verification

- Unit tests: 49 passed (31 existing plus 18 new in tests/test_escd_crud_and_ollama.py).
- Browser test (Chromium, mock API): desktop and 390px mobile flows for open, edit, save, create, complete, promote, archive and retire across all four sections; no console errors; no horizontal scroll.
- Not yet verified: a live Vercel deployment of this code. Production is still dpl_7zrsyvmm (CLI). Ollama chat is unverified until an Ollama key or endpoint is supplied.

## Status

MILESTONE RECORDED 2026-09-17 (see _Tribunal_Inbox/TRIBUNAL_MILESTONE_20260917_ESCD_MVP_0_5.md).
- Preview dpl_9QKdtyeecP84RYcLGRsMkN7Bt6yX: READY and used live. Login and reads returned 200. OpenAI and OpenRouter chat replied.
- Production promotion: pending.
- Live create, edit and archive: not yet exercised.
