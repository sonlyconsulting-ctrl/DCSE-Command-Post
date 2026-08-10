# DOCTRINE UPDATE REQUIRED: Operative Poller Integration (v7.2 → v7.3)

**Issue Date:** 2026-08-10  
**Authority:** DCS (action required)  
**Blocking:** Operative workflow institution  
**Status:** INVESTIGATION COMPLETE, REMEDIATION READY

---

## FINDINGS

### Gap 1: v7.2 Doctrine §6 Does Not Specify Poller Packet Format

v7.2 §6 defines the poller contract (constitutional invariants, actionable events, sleep preconditions) but does **not** specify:
- How tasks are submitted to the poller
- What packet schema the poller reads
- Whether the poller reads from files, database tables, or API

**Evidence:** v7 poller reads from `_Tribunal_Inbox/TRIBUNAL_*.json` with `POLLER_V7` block. This format is not documented in v7.2 governing text.

### Gap 2: v7.2 §6.2 Marks Legacy Pollers `ROLLBACK_ONLY`

> "Legacy provider-specific pollers are `ROLLBACK_ONLY` unless explicitly reclassified."

The v7 poller is legacy (v7 candidate, pre-operative). It is marked `ROLLBACK_ONLY` unless DCS explicitly reclassifies it to OPERATIVE.

**Current State:** v7 poller is NOT reclassified. Therefore, using it requires a formal DCS reclassification directive.

### Gap 3: Operative Workflow Instituted Without Doctrine Support

The `MP72-OPERATIVE-WORKFLOW-001` directive (instituted 2026-08-10) specifies:
- GitHub commits
- Supabase inserts (agent_tasks, poller_wake_requests)
- Poller dispatch

But v7.2 doctrine does NOT authorize:
- Supabase poller_wake_requests table as the source of truth for tasks
- Automatic poller dispatch from Supabase
- The relationship between dcse_cp tables and v7 poller packet files

---

## REQUIRED UPDATES TO v7.2 DOCTRINE

### Update 1: Add Poller Packet Schema (Layer 4)

**Insert after §14.2 (Machine Control Layer):**

```
MP72-P7.1  Poller Packet Schema

A poller packet is a JSON file in _Tribunal_Inbox/ named TRIBUNAL_*.json.

Required top-level fields:
{
  "POLLER_V7": {
    "task_id": string (unique identifier),
    "lane": enum (DCSE|PS|SC|SS|TSL|TRIBUNAL|DDNA|RAG|SYSTEM),
    "approved_by": string (authority who approved dispatch),
    "approved_at": ISO-8601 timestamp,
    "worker": enum (codex|fable|[other]),
    "working_directory": string (absolute path, must be within allowed roots),
    "sandbox": boolean,
    "timeout_seconds": integer (1-300),
    "expected_outputs": array of strings (relative paths)
  },
  "task": {
    [task-specific fields per lane]
  }
}

Packets without POLLER_V7 block are ignored.
Packets with malformed POLLER_V7 enter QUARANTINE_PENDING.
No packet is executed without explicit DCS approval in POLLER_V7.approved_by.
```

### Update 2: Reclassify v7 Poller Status

**Insert after §6.2:**

```
MP72-P6.3  v7 Poller Reclassification

The tribunal-poller-v7 is hereby reclassified from ROLLBACK_ONLY to OPERATIVE under the following conditions:

1. All packets MUST contain POLLER_V7 authorization block (§MP72-P7.1).
2. The approved_by field MUST identify the authorizing entity (DCS, CTO, lane authority).
3. No packet executes without prior DCS approval or delegated authority per §MP72-***.
4. All execution results produce a receipt in _Tribunal_Inbox/_Poller_v7_Runtime/receipts/
5. Receipts are immutable and provide evidence of execution or quarantine.

Effective: immediately upon DCS ratification of this update.
```

### Update 3: Define Task → Packet Mapping

**Insert new section:**

```
MP72-P12.1  Task Promotion from dcse_cp Tables to Poller Packets

Operational workflow:
1. Task created in dcse_cp.agent_tasks with status="planned"|"assigned"|"running"
2. When ready for poller dispatch:
   a. Create TRIBUNAL_*.json packet in _Tribunal_Inbox/
   b. Packet POLLER_V7.task_id MUST match agent_tasks.task_key
   c. Packet POLLER_V7.approved_by MUST reference authority (DCS, lane lead)
3. Poller reads packets from _Tribunal_Inbox/
4. Poller produces receipt in _Poller_v7_Runtime/receipts/
5. Receipt SHA-256 MUST be recorded back in dcse_cp.agent_tasks.output_refs

This creates bidirectional traceability: database → packets → receipts → database.
```

---

## REMEDIATION STEPS (FOR DCS)

**Step 1: Approve v7 Poller Reclassification**

DCS SHALL review the v7 poller codebase and confirm it meets operative standards (authorization checks, quarantine logic, receipt immutability). If approved, issue directive:

```
DIRECTIVE ID: MP72-POLLER-RECLASSIFICATION-001
AUTHORITY: DCS
EFFECTIVE: [date]
CONTENT: "The tribunal-poller-v7 is hereby reclassified from ROLLBACK_ONLY to OPERATIVE under MP72-P6.3 conditions."
```

**Step 2: Ratify Doctrine Updates**

DCS SHALL approve additions MP72-P7.1, MP72-P6.3, and MP72-P12.1 to v7.2 Master Profile. This converts v7.2 from CANDIDATE to OPERATIVE for poller operations.

**Step 3: Disseminate Operative Workflow**

Issue training/documentation showing all models how to:
1. Create task in dcse_cp.agent_tasks
2. Create TRIBUNAL_*.json packet when ready
3. Place packet in _Tribunal_Inbox/
4. Poller automatically processes it

**Step 4: Update MP72-OPERATIVE-WORKFLOW-001**

Revise the operative workflow (currently instituted 2026-08-10) to:
- Remove Supabase poller_wake_requests references
- Add TRIBUNAL packet creation step
- Document the bidirectional traceability model

---

## TIMELINE

| Action | Owner | Due | Blocking |
|---|---|---|---|
| Review v7 poller code | DCS/Tech Authority | 2026-08-11 | all subsequent steps |
| Approve/reject reclassification | DCS | 2026-08-12 | dissemination |
| Ratify doctrine updates | DCS | 2026-08-12 | operationalization |
| Disseminate to all models | Training/Comms | 2026-08-13 | usage |
| Update MP72-OPERATIVE-WORKFLOW-001 | Claude Code | 2026-08-13 | next deployment |

---

## BLOCKING THIS WORKFLOW

**Until DCS acts:**
- v7 poller is ROLLBACK_ONLY (cannot be used operationally without explicit reclassification)
- Supabase-based workflow is ungovernede (no doctrine support for poller_wake_requests table)
- Operative designation MP72-OPERATIVE-WORKFLOW-001 is INCOMPLETE (lacks poller integration)

**To proceed operationally:**
- DCS must reclassify v7 poller
- DCS must ratify doctrine updates
- All models must adopt revised workflow
- All deployments must create TRIBUNAL packets

---

**This document is not speculative.** It codifies the actual gaps discovered by attempting to operate under v7.2 and discovering the poller integration was not specified.

Prepared by: Claude Code  
Date: 2026-08-10  
Status: AWAITING DCS ACTION
