# Deployment Guide: Claude Reviewer Worker (Phase 1A)

**Status:** Ready for first deployment  
**Target:** DCSE V7 COMP 001 architecture review  
**Estimated deployment time:** 30 minutes  
**Monitoring duration:** 2-4 hours (autonomous execution)  

---

## Prerequisites

### 1. Verify PR #14 and Migrations
```bash
# Verify all CI checks pass
cd /home/user/DCSE-Command-Post
git fetch origin claude/supabase-activity-report-3z1k0v
git checkout claude/supabase-activity-report-3z1k0v

# Check Supabase Preview status
# ✅ All checks should be green:
#   - Database ✅
#   - Services ✅
#   - APIs ✅
#   - Migrations ✅
#   - Seeding ✅
```

### 2. Clone/Update Supabase Project
```bash
# Log in to Supabase CLI
supabase login

# Link to project
supabase link --project-ref liwdquzuigrlgfzgmpjp

# Pull latest schema (already migrated via preview branch)
supabase db pull

# Deploy Edge Function for worker auth
supabase functions deploy v7-worker-auth
```

### 3. Verify Worker Identity in Database
```bash
# Check seeded agents exist in preview database
psql -h db.liwdquzuigrlgfzgmpjp.supabase.co -U postgres -d postgres -c \
  "SELECT agent_id, model_family, authorized_lanes FROM v7_worker.agent_identity LIMIT 3;"

# Should show:
# AGENT-CLAUDE-REVIEWER-01@STAGING | claude | {SYSTEM,DCSE,RAG}
# AGENT-QWEN-BUILDER-01@DEVICE | qwen | {SC,DDNA}
# AGENT-DETERMINISTIC-VALIDATOR-01@CI | deterministic | {SYSTEM}
```

---

## Step 1: Obtain Worker Access Token

### Via cURL (manual test):
```bash
curl -X POST https://liwdquzuigrlgfzgmpjp.supabase.co/functions/v1/v7-worker-auth \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "AGENT-CLAUDE-REVIEWER-01@STAGING",
    "capabilities": ["read_v7_worker_queues", "write_v7_worker_results", "write_v7_worker_heartbeats"]
  }'

# Response:
# {
#   "access_token": "eyJhbGc...",
#   "expires_in": 3600,
#   "scope": ["read_v7_worker_queues", "write_v7_worker_results", "write_v7_worker_heartbeats"]
# }
```

### In Node.js (Claude worker will do this):
```javascript
const tokenResponse = await fetch(
  'https://liwdquzuigrlgfzgmpjp.supabase.co/functions/v1/v7-worker-auth',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agent_id: 'AGENT-CLAUDE-REVIEWER-01@STAGING',
      capabilities: ['read_v7_worker_queues', 'write_v7_worker_results']
    })
  }
);

const { access_token } = await tokenResponse.json();
process.env.WORKER_ACCESS_TOKEN = access_token;
```

---

## Step 2: Enqueue First Task (DCSE V7 COMP 001)

### Insert task into queue:
```sql
-- Insert into pgmq-backed queue_message table
INSERT INTO v7_worker.queue_message (
  task_id,
  lane,
  task_type,
  priority,
  runtime_packet,
  enqueued_by,
  enqueued_at
) VALUES (
  'DCSE-V7-COMP-001',
  'SYSTEM',
  'architecture_review',
  'P0',
  '{
    "task_id": "DCSE-V7-COMP-001",
    "task_type": "architecture_review",
    "lane": "SYSTEM",
    "instruction": "Review DCSE V7 Agent Worker Communication System: inspect architecture blueprint, migrations, worker runtime, RLS policies, functions, queue lifecycle, tests, v6.9 preservation, and PS firewall compliance. Produce architecture findings, code/schema defects, repairs, contradiction register, acceptance scorecard, and Level 0 decision packet.",
    "tools_allowed": ["read_file", "glob_search", "grep_search", "git_diff", "test_execution", "supabase_rpc"],
    "repo_scope": {
      "allowed_paths": [
        "02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md",
        "02_ARCHITECTURE/MODEL_REGISTRY.yaml",
        "supabase/migrations/20260728_*.sql",
        "supabase/migrations/20260716_*.sql",
        "workers/",
        "tests/"
      ],
      "forbidden_patterns": ["*.env", "credentials", "secrets"]
    },
    "deadline": "2026-07-27T23:00:00Z",
    "cost_estimate_usd": 2.50
  }'::jsonb,
  'claude-code-admin',
  now()
);

-- Verify enqueued
SELECT msg_id, task_id, lane, priority, enqueued_at FROM v7_worker.queue_message 
WHERE task_id = 'DCSE-V7-COMP-001';
```

Or via application bridge (when wired):
```javascript
const { data, error } = await supabase.rpc('enqueue_task', {
  p_task_id: 'DCSE-V7-COMP-001',
  p_lane: 'SYSTEM',
  p_task_type: 'architecture_review',
  p_priority: 'P0',
  p_runtime_packet: JSON.stringify({...})
});
```

---

## Step 3: Deploy Claude Reviewer Worker

### Option A: Run Locally (for testing)
```bash
cd /home/user/DCSE-Command-Post/workers

# Set environment
export SUPABASE_URL="https://liwdquzuigrlgfzgmpjp.supabase.co"
export WORKER_ACCESS_TOKEN="<from step 1>"  # Will be obtained at runtime
export ANTHROPIC_API_KEY="<your-api-key>"
export NODE_ENV="staging"

# Run worker
node claude-reviewer-worker.js

# Expected output:
# [AGENT-CLAUDE-REVIEWER-01@STAGING] Worker started (model: claude-opus-5, mode: Blueprint)
# [AGENT-CLAUDE-REVIEWER-01@STAGING] No tasks. Sleeping 30s...
# [AGENT-CLAUDE-REVIEWER-01@STAGING] Claimed task: DCSE-V7-COMP-001
# [AGENT-CLAUDE-REVIEWER-01@STAGING] === TASK CLAIMED ===
# [AGENT-CLAUDE-REVIEWER-01@STAGING] === EXECUTING ===
# [AGENT-CLAUDE-REVIEWER-01@STAGING] Agent iteration 1/10
# [AGENT-CLAUDE-REVIEWER-01@STAGING] Tool: read_file
# ...
```

### Option B: Deploy as Systemd Service (production)
```bash
# Create service file
sudo tee /etc/systemd/system/dcse-claude-reviewer.service > /dev/null <<EOF
[Unit]
Description=DCSE Claude Reviewer Worker
After=network.target

[Service]
Type=simple
User=dcse
WorkingDirectory=/home/dcse/DCSE-Command-Post/workers
EnvironmentFile=/etc/dcse/worker.env
ExecStart=/usr/bin/node /home/dcse/DCSE-Command-Post/workers/claude-reviewer-worker.js
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create environment file
sudo tee /etc/dcse/worker.env > /dev/null <<EOF
SUPABASE_URL=https://liwdquzuigrlgfzgmpjp.supabase.co
ANTHROPIC_API_KEY=<your-key>
NODE_ENV=production
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable dcse-claude-reviewer
sudo systemctl start dcse-claude-reviewer
sudo systemctl status dcse-claude-reviewer
```

### Option C: Deploy to Container (recommended for managed environments)
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY workers/claude-reviewer-worker.js .
COPY package.json package-lock.json ./
COPY 02_ARCHITECTURE/MODEL_REGISTRY.yaml ./

RUN npm install --only=production

ENV NODE_ENV=production
ENV SUPABASE_URL=https://liwdquzuigrlgfzgmpjp.supabase.co

CMD ["node", "claude-reviewer-worker.js"]
```

Deploy to cloud:
```bash
# Build and push to Docker registry
docker build -t dcse/claude-reviewer:v1 .
docker push dcse/claude-reviewer:v1

# Deploy to orchestrator (Kubernetes, ECS, Cloud Run, etc.)
# Example: Google Cloud Run
gcloud run deploy dcse-claude-reviewer \
  --image dcse/claude-reviewer:v1 \
  --platform managed \
  --region us-central1 \
  --timeout 3600 \
  --memory 2Gi \
  --set-env-vars "SUPABASE_URL=https://liwdquzuigrlgfzgmpjp.supabase.co,ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
```

---

## Step 4: Monitor Execution

### Real-time logs (local):
```bash
# Watch worker logs
tail -f /tmp/dcse-claude-reviewer.log

# Or with systemd
sudo journalctl -f -u dcse-claude-reviewer
```

### Database polling:
```bash
# Watch heartbeats
watch -n 5 'psql -c "SELECT agent_id, status, last_heartbeat_at FROM v7_worker.agent_identity WHERE agent_id = '\''AGENT-CLAUDE-REVIEWER-01@STAGING'\''; SELECT COUNT(*) as active_claims FROM v7_worker.task_claim WHERE released_at IS NULL AND visibility_timeout_at > now();"'

# Watch result submissions
watch -n 10 'psql -c "SELECT task_id, submission_status, submitted_at FROM v7_worker.result_submission ORDER BY submitted_at DESC LIMIT 3;"'
```

### Expected timeline:
```
T+0:00   Task enqueued in queue
T+0:30   Worker polls and claims task
T+0:31   Heartbeat sent (initial)
T+0:35   Claude Agent iteration 1/10 (read architecture doc)
T+0:40   Claude Agent iteration 2/10 (grep for defects)
T+1:00   Claude Agent iteration 5/10 (analyze migrations)
T+2:00   Claude Agent iteration 10/10 (compile findings)
T+2:05   Result submitted (pending_validation)
T+2:10   Deterministic validator starts
T+2:15   Repair tasks created for Qwen
T+2:20   Task marked review_ready
T+2:25   Queue message archived
T+3:00   Level 0 decision packet compiled
```

---

## Step 5: Verify Results

### Query submitted findings:
```sql
SELECT 
  task_id,
  submission_status,
  result_data,
  submitted_at
FROM v7_worker.result_submission
WHERE task_id = 'DCSE-V7-COMP-001'
LIMIT 1 \gx
```

### Expected output structure:
```json
{
  "review_type": "architecture_v7_comp_001",
  "timestamp": "2026-07-27T22:30:00Z",
  "findings": {
    "architecture": [...],
    "schema": [...],
    "security": [...],
    "compliance": [...]
  },
  "automatic_repairs_applied": [...],
  "repair_tasks_created": ["DCSE-V7-REPAIR-001", ...],
  "acceptance_scorecard": {
    "architecture_complete": true,
    "migrations_pass_preview": true,
    "...": "..."
  },
  "level_0_decision": {
    "recommendation": "approve|conditional|reject",
    "reason": "..."
  }
}
```

### Check created repair tasks:
```sql
SELECT task_id, title, lane, created_by FROM v7_worker.queue_message 
WHERE parent_task_id = 'DCSE-V7-COMP-001' AND created_by = 'AGENT-CLAUDE-REVIEWER-01@STAGING'
ORDER BY created_at;
```

---

## Troubleshooting

### Worker not claiming tasks
```bash
# Check agent identity exists
psql -c "SELECT * FROM v7_worker.agent_identity WHERE agent_id = 'AGENT-CLAUDE-REVIEWER-01@STAGING';"

# Check queue has messages
psql -c "SELECT COUNT(*) FROM v7_worker.queue_message WHERE dead_lettered_at IS NULL;"

# Verify RLS policy allows reads
psql -c "SELECT * FROM v7_worker.queue_message LIMIT 1;" 
# If denied: check `workers_read_eligible_messages` policy and agent's authorized_lanes
```

### Token expiration
```bash
# Worker will auto-request new token if expired
# Check Edge Function logs
supabase functions logs v7-worker-auth

# Verify JWT_SECRET matches
# Check environment variable is set
echo $JWT_SECRET | base64 -d
```

### Model not found
```bash
# Verify Anthropic API key is valid
curl -s https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" | jq '.data[] | select(.id | contains("opus"))'

# Check MODEL_REGISTRY.yaml has current model ID
grep approved_model_id 02_ARCHITECTURE/MODEL_REGISTRY.yaml
```

### RLS policy error: "path traversal rejected"
This is intentional. Worker uses Blueprint Mode tool constraints:
- Read: restricted to repo root only
- Glob: searches under repo root
- Grep: searches under repo root
- No file write (implementation mode only)

### Task stuck in "claiming" state
```bash
# Check visibility timeout
SELECT task_id, visibility_timeout_at, now() FROM v7_worker.task_claim 
WHERE released_at IS NULL ORDER BY visibility_timeout_at;

# If timeout expired, heartbeat renewal will have failed
# Check worker logs for error classification
# Manual recovery: run `release_task_claim()` with reason='visibility_expired'
```

---

## Success Criteria

✅ **Deployment successful when:**

1. Worker starts and logs: `Worker started (model: claude-opus-5, mode: Blueprint)`
2. Worker claims DCSE-V7-COMP-001 task within 2 minutes
3. Heartbeat records appear in `v7_worker.heartbeat` table every 5 minutes
4. Claude Agent executes 5-10 iterations calling approved tools
5. Result submitted to `result_submission` table with `submission_status = 'pending_validation'`
6. Repair tasks created in queue with `created_by = 'AGENT-CLAUDE-REVIEWER-01@STAGING'`
7. Findings JSON contains `architecture`, `schema`, `security`, `compliance` sections
8. No critical errors in worker logs (warnings are OK)
9. Deterministic validator processes result automatically
10. Level 0 decision packet appears in findings

✅ **First execution complete when:**
All above + task marked `review_ready` + queue message archived

---

## Next Phase (Phase 1B)

Once Claude reviewer worker succeeds:

1. Deploy deterministic validator worker
2. Implement Qwen build worker for repairs
3. Wire CP Dashboard task dispatch UI
4. Run end-to-end cycle on real repair work

---

## Rollback

If deployment fails catastrophically:

```bash
# Stop worker
sudo systemctl stop dcse-claude-reviewer

# Drain queue (mark messages dead-lettered)
UPDATE v7_worker.queue_message 
SET dead_lettered_at = now(), dead_letter_reason = 'manual_drain'
WHERE dead_lettered_at IS NULL;

# Revert migration (back to v6.9)
supabase db reset  # or: supabase migration down

# Verify v6.9 schema intact
psql -c "\dt dcse_cp.*"
```

---

## Reference

- **PR #14:** https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post/pull/14
- **Migration:** `supabase/migrations/20260728_v7_agent_worker_communication_system.sql`
- **Task definition:** `03_WORK_ORDERS/DCSE_V7_COMP_001_ARCHITECTURE_REVIEW.md`
- **Worker code:** `workers/claude-reviewer-worker.js`
- **Model registry:** `02_ARCHITECTURE/MODEL_REGISTRY.yaml`
- **Architecture guide:** `02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md`
