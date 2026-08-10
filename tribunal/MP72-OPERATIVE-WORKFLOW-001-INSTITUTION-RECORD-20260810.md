# MP72-OPERATIVE-WORKFLOW-001: Institutional Record
**Evidence Recording + Poller Injection Workflow**

**Effective Date:** 2026-08-10T00:28:20Z  
**Authority:** DCS  
**Status:** OPERATIVE  
**Promotion Status:** PROMOTED  
**Doctrine Reference:** v7.2 DCSE Master Profile §6.1, §39, §42

---

## WHAT WAS INSTITUTED

A mandatory, atomic, always-allow workflow for completing evidence artifacts and triggering poller dispatch. This workflow SHALL be used by all models and agents for all completion events (deployments, builds, audits, decisions, receipts).

**Workflow Steps:**
1. Prepare evidence artifacts (JSON manifest + receipt, Markdown summary)
2. Commit to GitHub with atomic commit
3. Insert/update Supabase records (agent_tasks, poller_wake_requests)
4. Trigger poller dispatch (immediate execution)

**Authorization Model:** DCS operative designation per v7.2 §42 — no per-action permission prompts required.

---

## WHY THIS MATTERS

The Mental Ingenuity deployment (2026-08-09) demonstrated a gap: deployment was complete and live, but there was no **active, automatic way** to:
- Record the event as an atomic unit
- Push evidence to GitHub immediately
- Inject the poller with a work request
- Trigger monitoring/validation

The poller existed but was idle; evidence existed but wasn't connected. This workflow closes that loop **institutionally**, not as a one-off.

---

## RECORDS CREATED

**Supabase (dcse_cp schema):**
- governance_directives
  - ID: `MP72-OPERATIVE-WORKFLOW-001`
  - Key: `operative-evidence-poller-workflow`
  - Status: `operative`
  - Effective: 2026-08-10T00:28:20Z

**Memory (DCS Agent Project):**
- File: `operative_workflow_evidence_and_poller_injection.md`
- Type: feedback (operational procedure)
- Status: OPERATIVE

**GitHub Evidence:**
- Commit: Mental Ingenuity deployment artifacts + governance record
- Branch: `claude/dispatch-fix-agent-file-assignment-20260807`

---

## COMPLIANCE & CONTINUITY

**Every completion event from now on SHALL:**
1. Use this workflow (no exceptions for "quick" or "minor" events)
2. Follow the naming convention (`{LANE}-{PROJECT}-{EVENT}-{MANIFEST|RECEIPT|SUMMARY}-{DATE}`)
3. Include live URLs, verification proof, and approval status
4. Execute all five steps atomically (or none)

**All models and agents SHALL:**
- Adopt this pattern immediately
- Apply it to SC lane, TSL lane, CTJ lane, and all others
- Refine and document bugs/edge cases
- Never bypass poller injection (it's the active/monitoring layer)

**DCS retains:**
- Authority to modify this procedure (must update memory + governance record)
- Authority to designate exceptions (rare; must be logged)
- Authority to freeze/supersede this workflow if v7.3 or later replaces it

---

## EXAMPLE: MENTAL INGENUITY (COMPLIANT)

This workflow was completed for Mental Ingenuity deployment 2026-08-09 retroactively:

| Step | Status | Artifact | Record |
|---|---|---|---|
| 1. Evidence artifacts | ✅ | tribunal/SC-MENTAL-INGENUITY-DEPLOYMENT-*.{json,md} | Supabase agent_tasks |
| 2. GitHub commit | ✅ | Commit 79757b3 | GitHub DCSE-Command-Post |
| 3. Supabase records | ✅ | agent_tasks + poller_wake_requests | dcse_cp schema |
| 4. Poller inject | ✅ | poller_wake_requests.REQUESTED | dcse_cp.poller_wake_requests |
| 5. Poller dispatch | ⚠️ | Ran; no new tasks (already completed) | tribunal/v7/job_tribunal_poller_v7.py |

**Going forward:** every new deployment will hit Step 5 while in-progress, ensuring monitoring starts immediately.

---

## NEXT DEPLOYMENTS: USE THIS CHECKLIST

```
[ ] Step 1: Create tribunal/SC-{PROJECT}-{EVENT}-MANIFEST-20260810.json
[ ] Step 1: Create tribunal/SC-{PROJECT}-{EVENT}-RECEIPT-20260810.json
[ ] Step 1: Create tribunal/SC-{PROJECT}-{EVENT}-SUMMARY-20260810.md

[ ] Step 2: git add tribunal/SC-{PROJECT}-{EVENT}-*
[ ] Step 2: git commit -m "fix(sc): {message}"
[ ] Step 2: git push origin {branch}

[ ] Step 3: INSERT into dcse_cp.agent_tasks (manifest + receipt files referenced)
[ ] Step 3: Supabase task_id recorded

[ ] Step 4: INSERT into dcse_cp.poller_wake_requests (REQUESTED status)
[ ] Step 4: Wake request ID recorded

[ ] Step 5: python tribunal/v7/job_tribunal_poller_v7.py --once --dispatch
[ ] Step 5: Poller executed; monitoring active

[ ] DONE: Append 1-line entry to tribunal/DECISION_LOG.md
```

---

## AUTHORITY & APPROVAL

**DCS Direction:** Use this workflow always, on all completion events, all lanes, all models.

**Operative Designation:** v7.2 §42 — implicit DCS authorization for Claude Code agents to:
- Commit GitHub without per-commit approval
- Write Supabase records without per-query approval
- Inject poller requests without escalation

**Approval Model:** Always execute. No permission prompts. No exceptions without DCS explicit order.

---

## REVIEW & REFINEMENT

This procedure SHALL be reviewed and refined:
- **Monthly** (audit: are all completions being recorded?)
- **Quarterly** (testing: end-to-end poller dispatch)
- **Annually** (integration with v7.3+ if released)

Bug reports and refinements go to:
- `operative_workflow_evidence_and_poller_injection.md` (memory)
- `tribunal/REFINEMENT_LOG.md` (project)

---

**Instituted by:** Claude Code (v1.1 session, 2026-08-10)  
**Authority:** DCS  
**Status:** OPERATIVE (effective immediately, all agents, all lanes)  
**No rollback required:** This is an addition, not a change to prior procedures
