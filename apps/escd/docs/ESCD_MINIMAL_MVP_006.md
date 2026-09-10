# ESCD Minimal Operable MVP 006

Task ID: DCSE-ESCD-001-MVP-006
Parent: DCSE-ESCD-001
Status: IMPLEMENTATION

## Purpose
Deliver the smallest ESCD surface that DCS can use for real daily work before expanding executive-assistant features.

## Required user surfaces
1. Chat
2. Tasks
3. Ideas
4. Assets
5. DDNA

No static placeholder operational data is permitted.

## Chat
- Server-side provider credentials only.
- Initial providers: OpenAI and Gemini.
- No browser API-key entry or browser key persistence.
- Claude is excluded.
- Mistral/Ollama is deferred and does not block MVP.
- Provider availability must be derived from runtime configuration/health, not hard-coded status.
- Conversation records must be persisted before chat is considered release-complete.

## Tasks
- Real authenticated persistence.
- Create, read, update, complete/reopen, archive/delete as supported by the governed data model.
- Priority, status, due date, notes.

## Ideas
- Real authenticated persistence.
- Create, read, update, archive/delete.
- Promote an idea into a task without losing provenance.

## Assets
- Read live canonical asset records.
- Search/filter and record detail.
- Display only fields returned by the authoritative source.
- No fabricated counts or placeholder cards.

## DDNA
- Read live dedicated DCSE-DDNA records record-by-record.
- Initial browsing is source/processing data, not a claim of completed semantic DNA intelligence.
- Show available source metadata, status, public-safe state, content snapshot when present, and processing/job relationship when available.
- pgvector semantic retrieval is deferred until governed characteristics/embedding ingestion exists.

## Responsive acceptance
- Desktop: compact navigation plus content workspace.
- Tablet: collapsible navigation and full-width workspace.
- Mobile: single-column workspace with compact navigation.
- CRUD and record-detail flows must remain operable at all three form factors.

## Security and data rules
- Reuse the existing authenticated DCS operator boundary.
- Normal ESCD state uses caller JWT/RLS where supported.
- Provider and dedicated-DDNA service credentials remain server-side only.
- Never expose service-role or provider secrets to browser JavaScript.
- No production mutation or release is authorized by this packet.

## Explicitly deferred
- executive briefing presentation
- workflow designer/operator complexity in primary UI
- calendar/email mutation
- autonomous external actions
- Mistral/Ollama cloud bridge
- semantic DDNA/pgvector retrieval
- decorative analytics
- placeholder dashboards

## Exit criteria
MVP candidate is not complete until authenticated browser validation proves: Chat with at least one configured provider, real Task CRUD, real Idea CRUD, live Asset records, live DDNA records, persistence across refresh, honest loading/empty/error states, and responsive desktop/tablet/mobile operation.
