# ESCD Next Build Phase: Draft Task Packet

Task ID: DCSE-ESCD-PHASE-0.6-20260917
Status: CANDIDATE (scope for DCS approval; not started)
Lane: DCSE (internal)
Baseline: ESCD-MVP-0.5 (milestone DCSE-ESCD-MILESTONE-20260917-MVP-0.5)

## Scope, in recommended order

### A. Models and provider settings (already agreed as next phase)
- Model dropdown per provider, loaded from the provider's model list where an API offers one, plus a curated fallback list stored in the registry.
- The provider settings panel shows the key status (never the key), the endpoint (Ollama base URL), limits, and a "Test connection" button that runs a minimal call.
- Acceptance: switching the model changes the model shown in the next chat reply meta. A failed connection test shows the provider's safe error text.

### B. Claude (Anthropic) as a chat provider
- Decision required from DCS: the current ESCD contract test deliberately excludes Claude and Anthropic from the chat surface (test_mvp_chat_excludes_claude). Adding Claude means retiring that rule on the record.
- The database already has an anthropic registry row (model value is outdated and must be updated) and Vault secret name escd/anthropic/api_key.
- Build: Messages API adapter using the same registry, Vault and redaction pattern. Add an sk-ant redaction pattern.
- Acceptance: a Claude reply appears with its model in the meta, and the key never reaches the browser.

### C. Attachments on any record (Tasks, Ideas, Knowledge, Assets)
- Storage: a private Supabase Storage bucket escd-attachments. The browser uploads directly with a signed upload URL issued by the ESCD API. Files therefore never pass through Vercel functions, whose request body is capped at a few MB.
- Large files: use resumable (TUS) uploads. The largest allowed file size is set by the Supabase plan and bucket limit (UNKNOWN; verify before promising "any size").
- New table dcse_cp.escd_attachments:
  - Columns: id, record_kind, record_id, storage_path, file_name, mime_type, size_bytes, sha256, uploaded_by, created_at, archived_at.
  - RLS: owner only.
  - Deleting an attachment archives it, the same as for records.
- UI: an Attachments section inside the record editor (upload, list, download via short-lived signed URL, archive).
- Guard: PS-lane files are refused, and no public URLs are issued.
- Acceptance: a 1 GB test file uploads and downloads with a matching SHA-256 (or the plan limit is documented), and a 10 MB file works on mobile.

### D. ESCD to AI Orchestrator (message bus / Poller)
- ESCD becomes a participant on dcse_cp.agent_messages as dcs_authority (the DCS console):
  - Send: "Message agent" from Chat or from any record, using send_agent_message or broadcast_agent_message. The record link travels in metadata.
  - Receive: an Orchestrator inbox view using read_agent_messages('dcs_authority'). This produces a reader receipt, threads by correlation_id, and allows replies with reply eligibility enforced by the database.
  - Delivery health: shown from agent_message_delivery_status.
- Guardrails: messages stay communication only (execution_authorized = false).
  - Dispatching work, meaning governed agent_tasks, is a separate button that records a DCS decision reference before anything runs.
  - The poller is on demand and is not started from ESCD.
- Acceptance: DCS sends a message from ESCD to antigravity; the worker delivers it with a receipt; the reply shows in the ESCD inbox within about 2 minutes.

## Out of scope for this phase
- Unattended model launches to auto-answer messages.
- Public release.

## Prerequisites
- ESCD-MVP-0.5 promoted and verified in production.
- apps/escd committed to Git on a clean branch, and the git author email fixed.
