# ESCD-MVP-0.6 Build Receipt: ESCD talks with the AI Orchestrator

Date: 2026-09-17
Lane: DCSE (internal)
Directive: DCS, "#1 Priority is START FINISH TALKING WITH AI ORCHESTRATOR"
Baseline: ESCD-MVP-0.5 (production dpl_6PMWfBqiHM63UbhhZwfnYvpd2iJd)

## What was built

New Orchestrator section. ESCD joins the existing DCSE message bus (dcse_cp.agent_messages) as the DCS console under the registered identity dcs_authority.

- **Send:** pick one or more active or standby agents from agent_registry and write a subject and message. Several recipients share one conversation (correlation id). Every message is communication only; the database enforces execution_authorized = false.
- **Message agent from any record:** the record editor (Tasks, Ideas, Knowledge, Assets) has a Message agent button. It opens the Orchestrator with the record linked (kind, id, title in message metadata).
- **Receive:** ESCD pulls messages addressed to dcs_authority with read_agent_messages. The database writes a reader_pull_receipt for each one.
  - The section checks every 30 seconds while open.
  - It also checks in the background every 2 minutes and shows a count on the nav.
- **Conversations:** grouped by correlation id over the last 7 days. Messages other agents post in the same thread are included.
- **Delivery status per message:**
  - Queued (with attempt count)
  - Delivering
  - Delivered, with the receipt type (worker inbox receipt, or read by agent)
  - Expired, or failed after the maximum number of attempts
- **Reply:** answers the latest incoming message in the same thread.
  - The database blocks replies to acknowledgements and duplicate replies (H01 guard). In those cases ESCD sends a follow-up in the same thread, so DCS can keep the conversation going. The guard still stops agent ping-pong.
- **Delivery mode shown per agent:**
  - Host CLI agents (for example antigravity) get messages pushed to their Windows inbox by the 1-minute worker.
  - Chat agents read on session start.

## Not included (by design)

- Unattended model launches to auto-answer. Agents answer when their session reads the message.
- Dispatching executable work (agent_tasks). That needs a recorded DCS decision and is a separate, later control.

## Files

- runtime/mvp_data.py: orchestrator_agents, orchestrator_send, orchestrator_sync, orchestrator_threads, orchestrator_reply.
- api/mvp.py: routes GET /api/mvp/orchestrator/agents and /threads, and POST /send and /reply. All require an authenticated DCS operator. Version 0.6.
- web/mvp.html: Orchestrator section, Message agent button, polling, nav badge, 7-item mobile nav.
- tests/test_escd_orchestrator.py: 14 new tests.

No database schema change was needed. Existing RPCs, views and guards are reused.

## Verification

- Unit tests: 63 passed.
- Browser test (mock API):
  - The record-to-message flow works.
  - Validation works.
  - A sent message shows as queued.
  - An agent reply appears after Check now and is flagged new.
  - A DCS reply shows as delivered.
  - Mobile at 390 px has no horizontal scroll.
  - No console errors.
- The 0.5 CRUD browser suite still passes.
- Live end-to-end is not yet verified. It requires a preview deploy.

## Live preview test and fix (2026-09-17 06:30 UTC)

- VERIFIED (database):
  - Cowork sent test message ee2a6bd4 to dcs_authority. ESCD read it at 06:23:43 (reader_pull_receipt).
  - DCS replied from ESCD with 01081f35 at 06:25:02. Cowork read it at 06:26:20 (reader_pull_receipt).
  - Cowork answered with 33228f8e, which was QUEUED for ESCD to pick up.
- DEFECT (found by DCS): text typed in a thread's reply box disappeared when the 30-second refresh redrew the list.
  - Fixed: drafts are kept per thread, and focus and cursor are restored after each refresh.
  - A regression test reproduces the loss on the earlier build and passes on the fixed build.

## Follow-up (2026-09-17 06:33 UTC)

- DCS sent 4 more messages from preview dpl_Fk7JJxbx1s5NhgLBPe6PdPjPfV9R (the build before the fix).
  - All 4 were delivered, and Cowork read them at 06:31:25.
  - Cowork answered with 027bf9cd.
- DCS reported that the text still disappears. Expected: that preview predates the fix.
- DCS reported that Enter "sometimes works". Enter did not send from the reply box in that build.
  - Added: Enter sends from both the reply box and the new-message box. Shift+Enter adds a new line.
- Status wording changed from "Queued" to "Sent, waiting for <agent> to pick it up".
- Delivery check: the first save of the fixed mvp.html to the laptop wrote the earlier version (52,419 bytes, no fix).
  - This was caught by re-reading the laptop file.
  - The file was re-saved and now matches byte for byte (53,196 bytes, fix present).

## 0.6.1 (2026-09-17 06:55 UTC)

- DCS decision: Claude joins the Chat provider list, which retires the earlier no-Claude contract test.
  - Added the Anthropic Messages API adapter (anthropic-version 2023-06-01).
  - Consecutive turns of the same role are merged, and the system text goes in `system`.
  - Added sk-ant key redaction.
  - The registry row "anthropic" now uses model claude-sonnet-5 with a 60 s timeout (database update applied).
  - The key is stored in Vault through Provider settings and never reaches the browser.
- DCS direction: the Orchestrator should dispatch governed work through directives, not host conversations.
  - A dispatch build was started, then stopped by the session's safety controls before any code was deployed. It would have let the web console queue unattended agent runs on the host.
  - The related database functions were created and verified in a rolled-back test only, then dropped (migration revert_escd_directive_dispatch_20260917). The database is back to its prior state except the anthropic model update.
  - This capability is awaiting a DCS decision on how to proceed.
- Tests: 65 unit tests passed. The browser suites passed (CRUD, orchestrator, Claude listed in the provider dropdown).
