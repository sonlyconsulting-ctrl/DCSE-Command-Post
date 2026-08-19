# OPERATIVE WORKFLOW: Evidence Recording + Tribunal Poller Dispatch (CORRECTED)

**Status:** OPERATIVE (pending DCS doctrine ratification)  
**Effective:** 2026-08-10  
**Authority:** DCS  
**Applies to:** All models, all lanes, all completion events

---

## CORRECTED PATTERN: Deploy → Record → Create TRIBUNAL Packet → Dispatch

The previous workflow used Supabase poller_wake_requests. **This is corrected.** The actual operative workflow uses TRIBUNAL packets in the _Tribunal_Inbox/ directory.

---

## STEP-BY-STEP WORKFLOW

### Step 1: Prepare Evidence Artifacts

When a deployment, build, audit, or decision completes:

Create three files in `tribunal/` with consistent naming:

```
tribunal/{LANE}-{PROJECT}-{EVENT}-MANIFEST-{DATE}.json
tribunal/{LANE}-{PROJECT}-{EVENT}-RECEIPT-{DATE}.json
tribunal/{LANE}-{PROJECT}-{EVENT}-SUMMARY-{DATE}.md
```

**Manifest (JSON):** Full metadata, build stats, URLs, verification proof.  
**Receipt (JSON):** Completion proof, approvals, next actions.  
**Summary (MD):** Human-readable quick reference.

### Step 2: Commit to GitHub (Atomic)

```bash
git add tribunal/{LANE}-{PROJECT}-{EVENT}-*
git commit -m "fix({LANE}): {descriptive message}

[Full details, URLs, verification status]

Co-Authored-By: Claude {Model} <noreply@anthropic.com>"

git push origin {current-branch}
```

### Step 3: Insert Supabase Record

Insert ONE task record in `dcse_cp.agent_tasks`:

```sql
INSERT INTO dcse_cp.agent_tasks (
  task_key, title, lane, task_type, status, priority, 
  created_by_label, description, confidentiality, output_refs, completed_at
) VALUES (
  '{LANE}-{PROJECT}-{EVENT}-{DATE}',
  '[Title]',
  '{LANE}',
  'build',  -- or appropriate type
  'needs_review',  -- IMPORTANT: use needs_review, not completed
  5,
  'Claude Code',
  '[Description, URLs, verification]',
  'public_safe',
  jsonb_build_object(
    'manifest_file', 'tribunal/{LANE}-{PROJECT}-{EVENT}-MANIFEST-{DATE}.json',
    'receipt_file', 'tribunal/{LANE}-{PROJECT}-{EVENT}-RECEIPT-{DATE}.json',
    '[other]', '[values]'
  ),
  now()
)
RETURNING id, task_key;
```

**KEY:** Status is `needs_review`, not `completed`. DCS must accept it before it moves to `completed`.

### Step 4: Create TRIBUNAL Packet

When the task is ready for poller dispatch (i.e., DCS has reviewed and approved), create a packet:

**File:** `_Tribunal_Inbox/TRIBUNAL_{DATE}_{LANE}_{PROJECT}_{EVENT}.json`

**Content:**

```json
{
  "POLLER_V7": {
    "task_id": "{LANE}-{PROJECT}-{EVENT}-{DATE}",
    "lane": "{LANE}",
    "approved_by": "DCS",
    "approved_at": "ISO-8601 timestamp",
    "worker": "codex",
    "working_directory": "C:\\DS All Things\\DCSE_Command_Center\\DCSE_CP_Project",
    "sandbox": false,
    "timeout_seconds": 300,
    "expected_outputs": [
      "tribunal/{LANE}-{PROJECT}-{EVENT}-MANIFEST-{DATE}.json",
      "tribunal/{LANE}-{PROJECT}-{EVENT}-RECEIPT-{DATE}.json"
    ]
  },
  "task": {
    "title": "[Title of completed work]",
    "lane": "{LANE}",
    "project": "[Project name]",
    "status": "completed",
    "description": "[Full description, URLs, verification status]",
    "deliverables": {
      "live_url": "[if applicable]",
      "website_page": "[if applicable]",
      "github_commit": "[commit hash]",
      "supabase_task_id": "[task UUID from agent_tasks]",
      "verification": {
        "status": "verified",
        "http_status": 200,
        "tests_passed": true
      }
    }
  }
}
```

### Step 5: Poller Dispatch

The poller automatically reads `_Tribunal_Inbox/TRIBUNAL_*.json` and processes packets with valid POLLER_V7 blocks.

To manually trigger dispatch:

```bash
python tribunal/v7/job_tribunal_poller_v7.py --once --dispatch
```

To keep poller running (continuous, per v7.2 §6 session-based model):

```bash
python tribunal/v7/job_tribunal_poller_v7.py --watch --dispatch
```

---

## RULES

1. **Always atomic** — all five steps complete or none.

2. **Status progression:**
   - After Step 3: `needs_review` (awaiting DCS)
   - After DCS approval: create TRIBUNAL packet
   - After Step 5: poller produces receipt

3. **No placeholder data** — all URLs, stats, verification must be live/measured.

4. **Bidirectional traceability:**
   - agent_tasks.output_refs → GitHub + tribunal files
   - TRIBUNAL packet.task_id → agent_tasks.task_key
   - Poller receipt SHA-256 → agent_tasks output_refs

5. **Always-allow operations:**
   - GitHub commits (tribunal/*)
   - Supabase inserts (agent_tasks)
   - TRIBUNAL packet creation (_Tribunal_Inbox/)
   - Poller dispatch (v7)

---

## EXAMPLE: Mental Ingenuity Deployment (CORRECTED)

**Step 1: Evidence created**
```
tribunal/SC-MENTAL-INGENUITY-DEPLOYMENT-MANIFEST-20260809.json
tribunal/SC-MENTAL-INGENUITY-DEPLOYMENT-RECEIPT-20260809.json
tribunal/SC-MENTAL-INGENUITY-DEPLOYMENT-SUMMARY-20260809.md
```

**Step 2: GitHub commit**
```
79757b3 fix(sc): record Mental Ingenuity deployment artifacts
```

**Step 3: Supabase task inserted**
```
agent_tasks.task_key = MENTAL-INGENUITY-DEPLOYMENT-20260809
agent_tasks.status = needs_review
```

**Step 4: TRIBUNAL packet created**
```
_Tribunal_Inbox/TRIBUNAL_20260810_SC_MENTAL_INGENUITY_DEPLOYMENT.json
```

**Step 5: Poller dispatched**
```
python tribunal/v7/job_tribunal_poller_v7.py --once --dispatch
Receipt: _Poller_v7_Runtime/receipts/MENTAL-INGENUITY-DEPLOYMENT-20260809__[HASH].receipt.json
```

---

## TIMELINE FOR NEXT DEPLOYMENT

Use this checklist:

```
TASK CHECKLIST: {LANE}-{PROJECT}-{EVENT}

[ ] Step 1: Create manifest/receipt/summary in tribunal/
[ ] Step 1: Verify all URLs are live (HTTP 200)
[ ] Step 1: Verify all stats are measured (no "projected" or "placeholder")

[ ] Step 2: git add tribunal/{LANE}-{PROJECT}-{EVENT}-*
[ ] Step 2: git commit with full context
[ ] Step 2: git push to feature branch

[ ] Step 3: INSERT agent_tasks (status=needs_review)
[ ] Step 3: Record task UUID in local notes

[ ] [PAUSE for DCS review + approval]

[ ] Step 4: Create TRIBUNAL_{DATE}_{LANE}_{PROJECT}_{EVENT}.json
[ ] Step 4: Place in _Tribunal_Inbox/
[ ] Step 4: Verify POLLER_V7 block is complete and valid

[ ] Step 5: python tribunal/v7/job_tribunal_poller_v7.py --once --dispatch
[ ] Step 5: Check receipt in _Poller_v7_Runtime/receipts/
[ ] Step 5: Verify poller outcome (AUTHORIZED_DRY_RUN_HOLD or executed)

[ ] DONE: Append line to tribunal/COMPLETION_LOG.md
```

---

## FOR ALL MODELS AND AGENTS

**This workflow is MANDATORY for all completion events.**

- ✅ Use after every deployment
- ✅ Use after every build
- ✅ Use after every audit or decision
- ✅ Use after every receipt or closure

**No exceptions** without explicit DCS order.

---

## WHEN v7.2 DOCTRINE IS RATIFIED

Once DCS ratifies the doctrine updates (MP72-P6.3, MP72-P7.1, MP72-P12.1), this workflow becomes **fully operative** with no further gates or reviews needed. Until then, DCS review is required between Steps 3 and 4.

---

**Last Updated:** 2026-08-10  
**Authority:** DCS (operative designation pending doctrine ratification)  
**Status:** READY FOR IMMEDIATE USE (with DCS gate between Steps 3-4)
