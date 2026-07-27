# Phase 1A: Claude Reviewer Worker — Live Proof Execution

**Status:** Implementation complete. Live execution proof pending.

**Objective:** Deploy Claude Reviewer Worker (Blueprint Mode) in staging and execute DCSE V7 COMP 001 autonomously to demonstrate the full live cycle.

**Evidence Required:**
1. Worker startup and initialization
2. Heartbeat record creation
3. Autonomous task claim
4. Runtime packet loading
5. Architecture review execution
6. Structured findings submission
7. Repair task creation
8. Task status transition to awaiting-validation

**Deployment Target:** Staging environment (Supabase preview branch)

**Task:** DCSE V7 COMP 001 (live real task, not synthetic)

**Timeline:** Immediate execution upon PR #14 merge

---

## Deployment Checklist

- [ ] Verify PR #14 merged to main
- [ ] Clone/pull latest code
- [ ] Verify supabase/config.toml in place
- [ ] Deploy Edge Function: v7-worker-auth
- [ ] Verify agent_identity seeded with Claude agent
- [ ] Enqueue DCSE V7 COMP 001 task
- [ ] Start Claude Reviewer Worker
- [ ] Monitor logs (secrets removed)
- [ ] Capture heartbeat records
- [ ] Verify task claimed
- [ ] Verify result submitted
- [ ] Verify repair tasks created
- [ ] Collect all evidence
- [ ] Generate execution report

---

## Evidence Collection Format

```json
{
  "phase": "1A",
  "timestamp": "2026-07-27T...",
  "execution_id": "PROOF-1A-20260727-...",
  "worker_identity": "AGENT-CLAUDE-REVIEWER-01@STAGING",
  "deployment_host": "...",
  "startup_command": "node /path/to/claude-reviewer-worker.js",
  "startup_time": "...",
  "startup_logs": [...],
  "heartbeat_record": {
    "heartbeat_id": 123,
    "agent_id": "...",
    "recorded_at": "...",
    "status": "running"
  },
  "task_claim": {
    "task_id": "DCSE-V7-COMP-001",
    "claimed_at": "...",
    "claim_id": 456,
    "visibility_timeout_at": "..."
  },
  "runtime_packet": {
    "task_id": "...",
    "hash": "...",
    "loaded_at": "...",
    "tool_allowlist": [...]
  },
  "execution_timeline": [
    { "time": "...", "event": "heartbeat_sent", "metrics": {...} },
    { "time": "...", "event": "tool_read_file", "file": "..." },
    { "time": "...", "event": "tool_grep_search", "pattern": "..." },
    { "time": "...", "event": "agent_iteration", "iteration": 1 }
  ],
  "result_submission": {
    "submission_id": 789,
    "task_id": "...",
    "submitted_at": "...",
    "findings_hash": "...",
    "repair_task_count": 5
  },
  "repair_tasks_created": [
    {
      "task_id": "DCSE-V7-REPAIR-001",
      "finding_id": "F-123",
      "lane": "SC",
      "created_at": "..."
    }
  ],
  "final_task_status": "awaiting_validation",
  "audit_receipt": {
    "receipt_id": "...",
    "created_at": "...",
    "verified_by": "deterministic_validator"
  },
  "logs_sanitized": true,
  "secrets_present": false
}
```

---

## Success Criteria

✅ All 8 proof points captured  
✅ No secrets in logs  
✅ Heartbeat records show 5-min renewal  
✅ Task claimed within 2 minutes of enqueue  
✅ Architecture review findings submitted  
✅ Repair tasks created with proper lane/type  
✅ Deterministic validator confirms receipt  
✅ Execution time and token usage documented

---

## Next: Phase 1B Deterministic Validator

Upon completion of Phase 1A proof, Phase 1B validation suite is ready for integration.

Validator will confirm Phase 1A findings against PR #14 artifacts.
