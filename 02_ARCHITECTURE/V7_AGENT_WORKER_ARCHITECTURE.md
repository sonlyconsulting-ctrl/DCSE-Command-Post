# V7 Agent Worker Architecture

## Overview

DCSE V7 moves from **human-initiated interactive sessions** to **persistent autonomous worker services** that continuously monitor Supabase, claim eligible tasks, execute them headlessly, and write results back.

**Current state (broken loop):**
```
Supabase task exists
  → No worker listening
  → Human opens Qwen/Claude session
  → Human manually says "check the database"
```

**Target state (autonomous):**
```
Supabase queue holds task
  → Persistent worker claims task (within 15s)
  → Worker executes via headless Qwen Code / Claude Agent SDK / Codex
  → Worker writes result back to Supabase
  → Next task automatically claimed
  → No human required until approval gate
```

## Architecture Layers

```
┌─────────────────────────────────────────┐
│      DCS Command Post (Human)           │  ← Approves tasks, reviews results
│      CP Dashboard & Slack               │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐    ┌───▼──────────────┐
│ Dispatcher  │    │ Monitoring Alerts│
│ (Cron/CLI)  │    │ (Stop-Gate, DLQ) │
└──────┬──────┘    └──────────────────┘
       │
┌──────▼─────────────────────────────────┐
│    Supabase Queues (v7_worker schema)  │  ← Durable task queue, claims, leases
│  - queue_message (pgmq)                │
│  - task_claim (visibility timeout)     │
│  - stop_gate (approval hold)           │
│  - dead_letter (retry exhaustion)      │
│  - cost_ledger (tracking)              │
│  - heartbeat (worker liveness)         │
└──────┬──────────────────────────────────┘
       │
   ┌───┴──────────────────────────────────────┐
   │                                          │
┌──▼─────────────────┐      ┌──────────────┬▼─────────────┐
│ Qwen Code Worker   │      │  Claude      │Deterministic │
│ (Build/Script/     │      │  Agent SDK   │Validator     │
│  Repair)           │      │  (Arch/     │(Schema/RLS/  │
│                    │      │   Review)   │ Test)        │
│ while(true):       │      │             │              │
│  claim_task()      │      │ while(true):│while(true):  │
│  qwen --prompt     │      │  claim()    │ validate()   │
│  submit_result()   │      │  claude()   │ test_sql()   │
│  send_heartbeat()  │      │  submit()   │ report()     │
└────────────────────┘      └─────────────┴──────────────┘
         │                           │              │
         └───────────────┬───────────┴──────────────┘
                         │
                ┌────────▼──────────┐
                │ Worker Heartbeat  │
                │ (15s poll cycle)  │
                │ - Liveness        │
                │ - Current task    │
                │ - Metrics         │
                │ - Errors          │
                └───────────────────┘
```

## v7_worker Schema: Tables and Contracts

### 1. agent_identity
Registry of persistent workers. Each worker has a unique ID, approved lanes/task-types, permission mode, and cost limits.

```sql
agent_id           text primary key  -- AGENT-QWEN-CODER-01@LAPTOP-PRIMARY
agent_name         text              -- Human-readable name
model_family       text              -- qwen | claude | codex | deterministic
device_id          text              -- LAPTOP-PRIMARY
device_hostname    text              -- dev-machine-01.local
deployment_env     text              -- staging | production | test
authorized_lanes   text[]            -- {DCSE, RAG, DDNA, SYSTEM}
authorized_task_types text[]        -- {schema_generation, script, migration, repair, ...}
approval_mode      text              -- read-only | plan-only | auto-edit | governed-approval | full-access
max_concurrent_tasks    integer      -- Usually 1 (serial execution)
max_wall_time_minutes   integer      -- 30 minutes typical
max_session_turns       integer      -- 30 turns typical
max_attempts_per_task   integer      -- 3 attempts (then dead-letter)
monthly_cost_limit_usd  numeric      -- 100-150 typical
tool_allowlist     jsonb             -- Explicit permitted tools
tool_denylist      jsonb             -- Explicitly forbidden tools
status             text              -- candidate | approved | suspended | retired
registered_at      timestamptz       -- Registration time
last_heartbeat_at  timestamptz       -- Last liveness signal
updated_at         timestamptz       -- Last modification
```

### 2. queue_message (wrapper around pgmq)
Durable task queue with visibility timeout and acknowledgment. Backed by pgmq for crash recovery.

```sql
msg_id                  bigint primary key  -- pgmq message ID
queue_name              text                -- dcse_agent_tasks (default)
task_id                 text                -- Reference to v7_bootstrap.tasks
lane                    text                -- DCSE | RAG | DDNA | SYSTEM
task_type               text                -- schema_generation | repair | architecture_review | ...
priority                integer             -- 5=default, higher = earlier
runtime_packet          jsonb               -- Task input, acceptance criteria, expected output
created_at              timestamptz         -- When task was created
enqueued_at             timestamptz         -- When queued
last_claimed_by         text                -- agent_id of claiming worker
last_claim_at           timestamptz         -- When worker claimed
dead_lettered_at        timestamptz         -- Moved to DLQ (null = active)
dead_letter_reason      text                -- Why moved to DLQ
```

### 3. task_claim
Lease record when worker claims a task. Tracks visibility timeout for crash recovery.

```sql
claim_id                bigint generated    -- Unique claim identifier
queue_msg_id            bigint              -- Reference to queue_message
task_id                 text                -- Reference to task
agent_id                text                -- Reference to agent_identity
lane                    text                -- Copy of queue_message.lane
task_type               text                -- Copy of queue_message.task_type
claimed_at              timestamptz         -- When worker claimed
visibility_timeout_at   timestamptz         -- Lease expires; message requeued if not acked
lease_expires_at        timestamptz         -- Hard deadline for completion
attempt_number          integer             -- Which attempt (1, 2, 3)
worker_session_id       text                -- Qwen/Claude session ID for resumption
worker_model_version    text                -- Model version that claimed task
released_at             timestamptz         -- When claim released (null = active)
release_reason          text                -- success | timeout | error | worker_crash | policy_violation
acked_at                timestamptz         -- When result was acknowledged
```

**Visibility Timeout Lifecycle:**
```
Worker claims task
  → visibility_timeout_at = now() + 30 minutes
  → Message hidden from other workers
  → If worker crashes before result_submission.acked_at
    → visibility_timeout_at expires
    → Message becomes visible to other workers
    → Retry attempt N+1 can claim it
  → If worker completes and acks result
    → release_task_claim(reason='success')
    → Message dead-lettered
    → No further retries
```

### 4. result_submission
Buffer for worker result before writing to dcse_cp.agent_task_events. Decouples worker session from result durability.

```sql
submission_id           bigint generated
task_id                 text
claim_id                bigint              -- Reference to task_claim
agent_id                text
submission_status       text                -- pending | acked | failed | retrying
result_event_type       text                -- completed | blocked | needs_review | error
result_output           jsonb               -- Output from worker (plan, code, test results, etc)
worker_session_id       text                -- Session ID for debuggging
submission_attempted_at timestamptz
submission_acked_at     timestamptz         -- When dcse_cp accepted result
retries                 integer             -- Retry count if dcse_cp write failed
last_error              text
dc_event_id             bigint              -- Foreign key to dcse_cp.agent_task_events
```

### 5. heartbeat
One-per-worker snapshot sent every poll cycle (~15s). Tracks liveness, current task, metrics, errors.

```sql
heartbeat_id            bigint generated
agent_id                text
current_task_id         text                -- Task worker is running (null if idle)
status                  text                -- idle | claiming | running | uploading_result | error
current_lane            text
workspace_path          text                -- /repo/DCSE-Command-Post
branch_name             text                -- claude/supabase-activity-report
model_version           text
last_successful_claim_at timestamptz
last_error              text
last_error_at           timestamptz
capabilities            jsonb               -- Tools, permission mode, limits snapshot
metrics                 jsonb               -- {tasks_claimed: 10, tasks_completed: 8, tasks_failed: 0, total_cost_usd: 45.20}
sent_at                 timestamptz
```

### 6. dead_letter
Tasks that exhausted retries, hit policy violations, or raised Stop-Gat. Requires manual review.

```sql
dead_letter_id          bigint generated
task_id                 text
queue_msg_id            bigint
lane                    text
task_type               text
reason                  text                -- Max attempts, cost overrun, policy violation, deadline exceeded
attempts                integer
last_claim_by           text                -- Last worker to attempt
last_error_message      text
policy_violated         text                -- security | privacy | cost | deadline | manual_hold
requires_manual_escalation  boolean
escalated_to_cp         boolean
escalated_at            timestamptz
moved_at                timestamptz
runtime_packet          jsonb               -- Preserved for manual intervention
```

### 7. stop_gate
Block execution pending manual approval. For security, privacy, policy, cost, or deadline gates.

```sql
gate_id                 bigint generated
task_id                 text
agent_id                text
gate_type               text                -- security | privacy | policy_violation | manual_hold | cost_overrun | deadline_exceeded
description             text
requires_dcs_approval   boolean
approval_deadline       timestamptz
approver_id             text                -- DCS who approved
approved_at             timestamptz
approval_decision       text                -- approved | rejected | modify_and_retry
approval_notes          text
raised_at               timestamptz
```

### 8. cost_ledger
Per-worker, per-task cost tracking to enforce monthly limits and billing.

```sql
ledger_id               bigint generated
agent_id                text
task_id                 text
billing_period          date                -- Month (YYYY-MM-01)
event_type              text                -- api_call | session_start | session_end | token_usage | manual_adjustment
cost_usd                numeric(10,4)
units                   integer
unit_type               text                -- tokens | requests | minutes | ...
metadata                jsonb
recorded_at             timestamptz
```

## RLS Policies

All v7_worker tables have RLS enabled. Access model:

1. **Service Role**: Full access (schema owner). Allowed to:
   - Insert messages into queue
   - Claim/release tasks
   - Write heartbeats and results
   - Escalate to dead-letter
   - Record costs

2. **Worker (Authenticated)**: Limited access via `app.worker_id` context.
   - Read own agent_identity
   - Read own heartbeat
   - Execute `claim_next_task(agent_id)` → returns eligible message
   - Execute `send_heartbeat(agent_id, ...)` → record liveness
   - Execute `release_task_claim(claim_id, agent_id, reason)` → release lease
   - Write own result_submission (insert only)

3. **Public/Anon**: No direct access. Must go through service-role proxy.

## Worker Execution Flow

### Heartbeat / Poll Cycle (every ~15 seconds)

```
Worker service startup
  ↓
while (true):
  ├─ send_heartbeat(AGENT-QWEN-CODER-01@LAPTOP, status='idle', metrics)
  ├─ sleep 15s
  └─ if < max_concurrent_tasks
      └─ try claim_next_task()
```

### Task Claim (when eligible message exists)

```
claim_next_task(agent_id='AGENT-QWEN-CODER-01@LAPTOP')
  ↓
  ├─ Verify agent is 'approved' and not max_concurrent
  ├─ SELECT highest-priority queue_message WHERE:
  │   ├─ dead_lettered_at IS NULL (active)
  │   ├─ lane = ANY(agent.authorized_lanes)
  │   ├─ task_type = ANY(agent.authorized_task_types)
  │   └─ no active lease (visibility_timeout_at > now())
  ├─ Verify attempt_count < max_attempts_per_task
  │   └─ If exceeded → move to dead_letter, return empty
  ├─ INSERT task_claim with:
  │   ├─ visibility_timeout_at = now() + 30 minutes
  │   ├─ lease_expires_at = now() + 30 minutes
  │   └─ attempt_number = previous_attempt_count + 1
  ├─ UPDATE queue_message: last_claimed_by, last_claim_at, read_count++
  └─ RETURN {queue_msg_id, task_id, lane, runtime_packet, attempt_number}
```

### Worker Execution (Headless Qwen Code / Claude Agent SDK)

```powershell
# Pseudocode: Qwen Worker
while ($true) {
    $hb = Send-Heartbeat -AgentId "AGENT-QWEN-CODER-01@LAPTOP" -Status "idle"
    $task = Invoke-Claim-NextTask -AgentId "AGENT-QWEN-CODER-01@LAPTOP"
    
    if ($task) {
        $claimId = $task.claim_id
        Send-Heartbeat -AgentId $agentId -Status "running" -CurrentTask $task.task_id
        
        try {
            $result = qwen --prompt (ConvertTo-QwenPrompt $task.runtime_packet) `
                          --output-format json `
                          --approval-mode auto-edit `
                          --max-turns 30 `
                          --max-time 30m
            
            $submission = Submit-Result -ClaimId $claimId -Output $result -Status "completed"
            Write-Result-To-DCSE-CP -Submission $submission
            Release-TaskClaim -ClaimId $claimId -Reason "success"
            
        } catch {
            if ($_.Exception -match "CostExceeded") {
                Raise-StopGate -ClaimId $claimId -Type "cost_overrun" -Description $_.Exception.Message
            } else {
                Release-TaskClaim -ClaimId $claimId -Reason "error"
                # visibility_timeout will make message eligible for retry
            }
        }
        
        Send-Heartbeat -AgentId $agentId -Status "idle"
    }
    
    Start-Sleep -Seconds 15
}
```

### Result Submission (Worker → Supabase)

```
Worker receives completion result from Qwen
  ↓
INSERT v7_worker.result_submission {
  task_id, claim_id, agent_id,
  submission_status='pending',
  result_event_type='completed' | 'blocked' | 'error',
  result_output={...},
  worker_session_id,
  submission_attempted_at
}
  ↓
(Application layer, not worker)
SELECT from v7_worker.result_submission WHERE submission_status='pending'
  ↓
INSERT v7_worker.agent_task_events {
  task_id, event_type, ...
} → dcse_cp.agent_task_events
  ↓
UPDATE v7_worker.result_submission SET
  submission_status='acked',
  submission_acked_at=now(),
  dc_event_id=<dcse_cp event id>
  ↓
release_task_claim(claim_id, agent_id, 'success')
```

## Approval Gates (Stop-Gate Pattern)

**When to raise Stop-Gate:**
- Security violation detected (e.g., direct prod database access)
- Privacy concern (e.g., PII in output)
- Cost exceeded (e.g., task consumed $50+ in tokens)
- Deadline exceeded
- Policy violation (e.g., promoting without DCS signature)
- Manual hold (DCS decides to inspect)

**Stop-Gate flow:**
```
Worker detects condition
  ↓
INSERT v7_worker.stop_gate {
  task_id, agent_id, gate_type='security' | 'cost_overrun' | ...,
  requires_dcs_approval=true
}
  ↓
release_task_claim(claim_id, 'policy_violation')
  ↓
CP Dashboard highlights stop-gate
  ↓
DCS reviews evidence, makes decision:
  ├─ approved → Worker resumes/completes task
  ├─ rejected → Task moved to dead-letter
  └─ modify_and_retry → Worker re-claims with modified input
```

## Dead-Letter Queue (DLQ)

**Reasons for dead-letter:**

1. **Max attempts exceeded** (default 3)
   ```
   Attempt 1: timeout
   Attempt 2: error in worker
   Attempt 3: error in worker
   → moved to dead_letter, requires_manual_escalation=true
   ```

2. **Cost overrun** (monthly limit or per-task ceiling)
   ```
   Task consumed $100+ in token costs
   → moved to dead_letter, policy_violated='cost', escalated_to_cp
   ```

3. **Policy violation** (Stop-Gate rejected)
   ```
   Stop-Gate raised, DCS rejected approval
   → moved to dead_letter, policy_violated='policy_violation'
   ```

4. **Deadline exceeded**
   ```
   Task deadline passed
   → moved to dead_letter, policy_violated='deadline'
   ```

**DLQ inspection and recovery:**
```sql
-- Find DLQ items needing escalation
SELECT * FROM v7_worker.dead_letter
WHERE requires_manual_escalation = true
  AND escalated_to_cp = false
ORDER BY moved_at DESC;

-- When fixed, can replay task:
INSERT INTO v7_worker.queue_message (task_id, lane, task_type, runtime_packet, priority)
SELECT task_id, lane, task_type, runtime_packet, 10  -- high priority for retry
FROM v7_worker.dead_letter
WHERE dead_letter_id = $1;

UPDATE v7_worker.dead_letter SET escalated_to_cp=true WHERE dead_letter_id=$1;
```

## Retry Policy

**Visibility Timeout (worker crash recovery):**
```
Worker claims task, visibility_timeout_at = now() + 30 min
  ↓
Worker runs Qwen Code for 25 minutes...
  ↓
Worker process crashes (no result submitted)
  ↓
Visibility timeout expires (30 min elapsed)
  ↓
queue_message.dead_lettered_at remains null
  ↓
Next worker (or retry after delay) claims message
  ↓
attempt_number incremented to 2
  ↓
Max 3 attempts before dead-letter
```

**Programmatic retry:**
```
release_task_claim(claim_id, 'timeout')
  → visibility_timeout_at > now() (still leased)
  → Next claim cycle sees message as not-visible
  → After timeout expires, message becomes visible
  
release_task_claim(claim_id, 'error')
  → release message to queue
  → mark as available for immediate retry
  → increment read_count
```

## Cost Tracking and Limits

**Per-agent monthly limit:**
```sql
SELECT SUM(cost_usd) FROM v7_worker.cost_ledger
WHERE agent_id = 'AGENT-QWEN-CODER-01@LAPTOP'
  AND billing_period = date_trunc('month', now())::date;

-- Compare against:
SELECT monthly_cost_limit_usd FROM v7_worker.agent_identity
WHERE agent_id = 'AGENT-QWEN-CODER-01@LAPTOP';
```

**Worker should check before executing:**
```powershell
$monthlySpent = Get-MonthlySpent -AgentId $agentId
$limit = Get-CostLimit -AgentId $agentId
$taskEstimated = Estimate-Cost -Task $task

if (($monthlySpent + $taskEstimated) -gt $limit) {
    Raise-StopGate -Type "cost_overrun" -Description "Would exceed $limit"
    return
}
```

## Integration: v7_worker ↔ dcse_cp

**Two-schema design:**

- **v7_worker**: Queue, claims, leases, heartbeats, results buffer, stop-gates, DLQ
- **dcse_cp**: Canonical task list (v7_bootstrap.tasks), canonical event log (agent_task_events)

**Bridge workflow:**

1. DCS creates task in v7_bootstrap.tasks (existing)
2. Dispatcher enqueues to v7_worker.queue_message
3. Worker claims and executes
4. Worker writes to v7_worker.result_submission
5. **Application layer (Vercel edge function / cron job) polls v7_worker.result_submission**
6. Application writes result to dcse_cp.agent_task_events
7. Application updates task status in v7_bootstrap.tasks
8. Application acknowledges in v7_worker.result_submission (submission_status='acked')

**Why two schemas?**
- v7_worker handles durability, leasing, and retry (pgmq responsibility)
- dcse_cp handles authority and audit trail (DCS source of truth)
- Separation of concerns: queue mechanics vs. business logic

## Worker Types

### 1. Qwen Build Worker
**Handles:** Schema, scripts, migrations, implementation, repair, test generation

**Configuration:**
```
agent_id: AGENT-QWEN-CODER-01@LAPTOP-PRIMARY
authorized_lanes: DCSE, RAG, DDNA, SYSTEM
authorized_task_types: schema_generation, script, extraction, migration, implementation, repair, test_generation
approval_mode: auto-edit
max_wall_time: 30 minutes
max_attempts: 3
monthly_cost_limit: $150.00
```

**Headless invocation:**
```powershell
qwen -p "$runtimePacket" `
     --output-format json `
     --approval-mode auto-edit `
     --max-turns 30 `
     --max-wall-time 30m `
     --unattended-retry true
```

### 2. Claude Architecture Worker
**Handles:** Blueprint, architecture review, doctrine reconciliation, contradiction analysis

**Configuration:**
```
agent_id: AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY
authorized_lanes: DCSE, SC
authorized_task_types: blueprint, architecture_review, doctrine_reconciliation, evaluation
approval_mode: plan-only
max_wall_time: 20 minutes
max_attempts: 2
monthly_cost_limit: $100.00
```

**Headless invocation via Claude Agent SDK:**
```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY,
});

const task = await claimNextTask(agentId);
const response = await client.messages.create({
  model: "claude-opus-5",
  max_tokens: 4000,
  tools: [readTool, grepTool, globTool], // read-only tools
  messages: [{
    role: "user",
    content: task.runtime_packet.prompt,
  }],
});

await submitResult(task.claim_id, response.content);
```

### 3. Deterministic Validator Worker
**Handles:** Schema validation, SQL tests, RLS tests, formatting, acceptance criteria

**Configuration:**
```
agent_id: AGENT-DETERMINISTIC-VALIDATOR-01@LAPTOP-PRIMARY
authorized_lanes: DCSE, SYSTEM
authorized_task_types: validation, test_execution, schema_check, rls_test, acceptance_criteria
approval_mode: read-only
max_wall_time: 10 minutes
max_concurrent_tasks: 4 (can parallelize tests)
max_attempts: 1
monthly_cost_limit: $10.00 (minimal LLM calls, mostly code)
```

**Execution (ordinary Python, not headless model):**
```python
import subprocess
import json

while True:
    heartbeat(agent_id, "idle")
    task = claim_next_task(agent_id)
    if not task:
        time.sleep(15)
        continue
    
    heartbeat(agent_id, "running", task["task_id"])
    
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "--json", task["acceptance_criteria"]],
            capture_output=True,
            timeout=600,
        )
        output = json.loads(result.stdout)
        submit_result(task["claim_id"], "completed", output)
    except Exception as e:
        submit_result(task["claim_id"], "error", {"error": str(e)})
    
    heartbeat(agent_id, "idle")
    time.sleep(15)
```

### 4. Dispatcher / Recovery Worker
**Handles:** Task routing, expired claims, retry management, dead-letter escalation, worker health

**Configuration (not a full worker; runs as cron job or scheduled service):**
```
Runs every 5 minutes:
  ├─ Find expired claims (visibility_timeout_at < now())
  │   └─ release_task_claim(reason='timeout'), message becomes visible
  ├─ Find dead_letter items needing escalation
  │   └─ Alert CP Dashboard
  ├─ Check worker heartbeats for stale ones (> 5 min old)
  │   └─ Mark agent status as 'error' if unresponsive
  ├─ Requeue messages from failed result_submission
  └─ Archive completed/acked messages
```

## Implementation Checklist

- [ ] Migration 20260728_v7_agent_worker_communication_system.sql applied
- [ ] Agent identities seeded (Qwen, Claude, Deterministic examples)
- [ ] v7_worker schema RLS policies tested
- [ ] claim_next_task() function tested
- [ ] send_heartbeat() function tested
- [ ] release_task_claim() function tested
- [ ] Qwen headless worker script deployed (PowerShell on Windows)
- [ ] Claude Agent SDK worker deployed (Python or TypeScript)
- [ ] Deterministic validator deployed (Python subprocess)
- [ ] Dispatcher/recovery cron job deployed
- [ ] Application layer bridge (result_submission → dcse_cp) implemented
- [ ] CP Dashboard updated to show worker status
- [ ] Alerts configured for dead-letter, stop-gate, worker crash
- [ ] Cost tracking confirmed operational
- [ ] End-to-end test: DCS creates task → worker claims → executes → result in dcse_cp

## Security Considerations

1. **Secret Management**: Workers hold `SUPABASE_SERVICE_ROLE_KEY` outside model context.
   - Store in environment variable or local keystore (Windows Credential Manager, AWS Secrets Manager)
   - Pass only task_id to model; model calls Supabase indirectly via application API

2. **Tool Permissions**: Each worker has explicit tool_allowlist + tool_denylist.
   - Qwen build worker: allowed to edit/create files, run tests, commit
   - Claude architect: allowed to read/search, no file writes
   - Deterministic validator: allowed to run tests, no model calls

3. **Lane Isolation**: Workers scoped to authorized_lanes.
   - AGENT-QWEN-CODER-01 cannot claim PS/litigation tasks
   - Enforced by RLS on queue_message select

4. **Cost Limits**: Enforced per-agent, per-task, per-month.
   - Worker checks before execution
   - Stop-Gate raised if overrun
   - Monthly ledger prevents infinite spend

5. **Approval Gates**: Security/privacy/policy decisions require DCS approval.
   - Worker cannot bypass Stop-Gate
   - dead_letter escalates unresolved gates to CP Dashboard

## Monitoring and Alerts

**Metrics to track:**
- Worker liveness (last_heartbeat_at within 5 min)
- Tasks claimed per worker per day
- Tasks completed successfully (result_submission.acked_at recorded)
- Tasks in DLQ by reason
- Stop-Gates raised by type
- Cost spent per worker per month
- Visibility timeout expires (worker crash detection)

**Alert conditions:**
- Worker heartbeat stale (> 5 min)
- Task in DLQ > 1 hour
- Stop-Gate pending > 2 hours (requires human decision)
- Monthly cost approaching limit
- Multiple visibility timeouts for same worker (repeated crashes)

**Dashboard queries:**
```sql
-- Worker health
SELECT agent_id, last_heartbeat_at, status, current_task_id
FROM v7_worker.agent_identity
LEFT JOIN v7_worker.heartbeat h ON agent_identity.agent_id = h.agent_id
  AND h.sent_at = (SELECT MAX(sent_at) FROM v7_worker.heartbeat hh WHERE hh.agent_id = agent_identity.agent_id)
WHERE status = 'approved'
ORDER BY last_heartbeat_at DESC;

-- DLQ pending escalation
SELECT task_id, lane, reason, moved_at, attempts, last_error_message
FROM v7_worker.dead_letter
WHERE requires_manual_escalation AND escalated_to_cp = false
ORDER BY moved_at ASC;

-- Cost tracking
SELECT agent_id, billing_period, SUM(cost_usd) as spent
FROM v7_worker.cost_ledger
WHERE billing_period = date_trunc('month', now())::date
GROUP BY agent_id, billing_period
ORDER BY spent DESC;

-- Tasks in flight
SELECT tc.task_id, tc.agent_id, tc.claimed_at, tc.visibility_timeout_at,
       EXTRACT(EPOCH FROM (tc.visibility_timeout_at - now())) as seconds_remaining
FROM v7_worker.task_claim tc
WHERE released_at IS NULL
ORDER BY visibility_timeout_at ASC;
```

## Testing

**Unit tests:**
- RLS policies prevent cross-agent access
- claim_next_task() respects lane/task-type authorization
- Visibility timeout lifecycle works correctly
- Dead-letter correctly moves exhausted tasks
- Cost tracking increments accurately

**Integration tests:**
- End-to-end: task creation → queue → claim → execution → result → acked
- Retry: worker crash (force visibility timeout expiry) → another worker claims and completes
- Stop-Gate: worker detects policy violation → raises gate → DCS approves → worker resumes

**Load test:**
- 4 concurrent workers claiming tasks
- 100 messages in queue
- Verify no duplicate claims
- Verify all messages claimed/processed within SLA

## Future Enhancements

1. **Codex Worker**: Code review, formatting, linting
2. **Browser-Based Worker**: Visual inspection, screenshot-based testing
3. **Distributed Workers**: Deploy workers on multiple machines, synchronize via Supabase
4. **Adaptive Retry**: Increase timeout for timeout-prone tasks
5. **Predictive Routing**: Route task to worker likeliest to succeed (based on historical metrics)
6. **Partial Result Recovery**: Resume task mid-stream if interrupted
7. **Live Progress**: Stream execution updates to CP Dashboard via websocket/Realtime
