# Ordered Remediation Plan
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Priority Remediation Sequence
**Doctrine:** Structure Precedes Scale

---

## Remediation Priority Framework

Ordered by: security risk first, then data integrity, then UX defects.

---

## Phase 1: Security (Immediate)

### R1. Remove Client-Side API Key Storage
**Priority:** P0
**Finding:** API_KEY_SECURITY_FINDINGS #1, #2
**Effort:** Medium

**Actions:**
1. Remove `KEY_STORES` object and all `localStorage.getItem/setItem` calls for API keys
2. Modify `handleChat` to inject API keys from `process.env` server-side
3. Remove `apiKey` field from client-side fetch body
4. Remove the API key input field from the chat UI header
5. Update `PROVIDER_META` check functions (no longer needed client-side)

**Verification:**
- No `localStorage` references to `sc_*_key` remain
- `/api/chat` works without client-supplied key
- Browser DevTools shows no keys in localStorage or request payloads

---

## Phase 2: Data Authority (Backend Migration)

### R2. Migrate Task Queue to Supabase
**Priority:** P0
**Finding:** PAGE_DATA_SOURCE_MATRIX, CRUD_COVERAGE_MATRIX
**Effort:** Medium

**Actions:**
1. Replace `localStorage` task CRUD with fetch calls to existing `/api/tribunal/dispatch` and `/api/tribunal/inbox`
2. Remove `sc_tasks` localStorage key and default task array
3. Task creation form POSTs to `/api/tribunal/dispatch`
4. Task list reads from `/api/tribunal/inbox`
5. Status updates via `/api/tribunal/status`

**Verification:**
- Tasks persist across browsers/devices
- Task panel shows live data from `dcse_cp.agent_tasks`
- No `sc_tasks` in localStorage

### R3. Migrate Portfolio to Supabase
**Priority:** P1
**Finding:** PAGE_DATA_SOURCE_MATRIX
**Effort:** Medium

**Actions:**
1. Create `/api/portfolio` handler with Supabase backing
2. Create portfolio table in `dcse_cp` schema (or use existing if present)
3. Replace `localStorage` CRUD with API calls
4. Remove `sc_portfolio` localStorage key and default array

**Verification:**
- Portfolio items persist in Supabase
- Build order reflects authoritative system of record

### R4. Migrate DDNA Scores/Notes to Supabase
**Priority:** P1
**Finding:** PAGE_DATA_SOURCE_MATRIX
**Effort:** Medium

**Actions:**
1. Create `/api/ddna` handler (or extend existing)
2. Store scores in `dcse_cp` DDNA table
3. Store notes with timestamps in Supabase
4. Remove `sc_ddna_scores` and `sc_ddna_notes` localStorage keys

**Verification:**
- Harvest scores persist in authoritative DB
- Audit trail for DDNA notes maintained server-side

### R5. Migrate RAG Sources to Supabase
**Priority:** P1
**Finding:** PAGE_DATA_SOURCE_MATRIX
**Effort:** Small

**Actions:**
1. Create `/api/ragsources` handler
2. Store source registry in `dcse_cp` table
3. Replace localStorage CRUD with API calls
4. Remove `sc_rag_sources` localStorage key

### R6. Replace Hardcoded Tribunal PR List
**Priority:** P2
**Finding:** PAGE_DATA_SOURCE_MATRIX
**Effort:** Small

**Actions:**
1. Create `/api/tribunal/prs` handler that queries GitHub API (or cache in Supabase)
2. Replace `TRIBUNAL_PRS` static array with dynamic fetch on panel load
3. Add refresh button to Tribunal panel

---

## Phase 3: Voice UX (Functional Defects)

### R7. Fix Voice Auto-Submit
**Priority:** P0
**Finding:** VOICE_STATE_MACHINE_FINDINGS #1
**Effort:** Small

**Actions:**
1. In `recognition.onresult`, populate input field only (do not call `sendMessage()`)
2. User reviews transcript and presses Enter or Send to submit
3. Add visual indicator that transcript is ready for review

**Verification:**
- Voice recognition populates input without sending
- User can edit transcript before submission

### R8. Implement Voice State Machine
**Priority:** P2
**Finding:** VOICE_STATE_MACHINE_FINDINGS #2
**Effort:** Medium

**Actions:**
1. Add `onspeechstart`, `onspeechend` handlers
2. Enable `interimResults: true` for real-time feedback
3. Update voice button/wave to reflect current state (IDLE/LISTENING/DETECTING/PROCESSING/RESULT)
4. Add silence timeout for auto-stop

---

## Phase 4: Structural Alignment

### R9. Dynamic Agent Dock
**Priority:** P2
**Finding:** PAGE_DATA_SOURCE_MATRIX
**Effort:** Small

**Actions:**
1. Fetch agent list from `/api/agentops` (already reads `dcse_cp.agent_registry`)
2. Replace static 12-agent HTML with dynamic render

### R10. Key Rotation Tracking
**Priority:** P3
**Finding:** API_KEY_SECURITY_FINDINGS #3
**Effort:** Small

**Actions:**
1. Track key creation/rotation dates in Supabase
2. Add rotation age to API Keys Admin readiness matrix
3. Surface rotation warnings in Assurance Loop

---

## Execution Schedule

| Phase | Items | Batch | DCS Gate |
|-------|-------|-------|----------|
| Phase 1 (Security) | R1 | Immediate | DCS authorization required |
| Phase 2 (Data) | R2, R3, R4, R5, R6 | B2 | DCS authorization required |
| Phase 3 (Voice) | R7, R8 | B2 | Agent-executable under supervision |
| Phase 4 (Structural) | R9, R10 | B3 | Agent-executable under supervision |

**Hard Constraint:** No remediation may proceed without DCS authorization per Standing Execution Authorization scope. Phase 1 (R1) and Phase 3 R7 are safety-critical and recommended for immediate authorization.

---

## Doctrine Alignment

| Principle | Current State | Post-Remediation |
|-----------|--------------|------------------|
| Structure Precedes Scale | PARTIAL: 6/17 entities in localStorage | COMPLIANT: all entities in Supabase |
| Authoritative Source Truth | PARTIAL: hardcoded PR list, static agents | COMPLIANT: all live data from DB |
| Backend Mediation | PARTIAL: 7 localStorage CRUD paths | COMPLIANT: all CRUD via API |
| Server-Side Credentials | FAILING: 4 keys in localStorage | COMPLIANT: all keys in process.env |
| No Agent Self-Approval | COMPLIANT | COMPLIANT |
| PS Firewall | COMPLIANT | COMPLIANT |
