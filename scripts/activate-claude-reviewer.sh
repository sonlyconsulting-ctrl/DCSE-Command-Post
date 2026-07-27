#!/bin/bash

##
# Activate Claude Reviewer Worker for V7
#
# Workflow:
# 1. Verify worker identity in database
# 2. Send initial heartbeat
# 3. Claim DCSE V7 COMP 001 task
# 4. Execute review (via node worker)
# 5. Submit results
# 6. Verify bridge processing
# 7. Generate completion receipt

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKER_ID="AGENT-CLAUDE-REVIEWER-01@STAGING"
TASK_ID="DCSE-V7-COMP-001"
SUPABASE_URL="${SUPABASE_URL:-https://nevgdyfpxdaloacuutal.supabase.co}"

echo "========================================================================"
echo "DCSE V7 COMP 001: Claude Reviewer Worker Activation"
echo "========================================================================"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Worker: $WORKER_ID"
echo "Task: $TASK_ID"
echo ""

# Verify environment
if [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
  echo "❌ ERROR: SUPABASE_SERVICE_ROLE_KEY not set"
  echo "   Set: export SUPABASE_SERVICE_ROLE_KEY=<key>"
  exit 1
fi

echo "✓ Environment verified"
echo ""

# Phase 1: Verify worker identity
echo "---------- PHASE 1: Worker Identity Verification ----------"
echo "Checking v7_worker.agent_identity for $WORKER_ID..."

WORKER_QUERY='
select agent_id, status, authorized_lanes, max_attempts_per_task, monthly_cost_limit_usd
from v7_worker.agent_identity
where agent_id = '"'"'AGENT-CLAUDE-REVIEWER-01@STAGING'"'"';
'

# Note: Would need curl + jq to query via SQL; for now, document the query
echo "Query to execute:"
echo "$WORKER_QUERY"
echo ""
echo "Expected: Agent exists with status = candidate"
echo ""

# Phase 2: Prepare task queue
echo "---------- PHASE 2: Task Queue Preparation ----------"
echo "Verifying DCSE V7 COMP 001 is queued..."

# Check if task exists in queue
QUEUE_QUERY='
select msg_id, task_id, lane, priority, runtime_packet
from v7_worker.queue_message
where task_id = '"'"'DCSE-V7-COMP-001'"'"'
  and dead_lettered_at is null
limit 1;
'

echo "Query to execute:"
echo "$QUEUE_QUERY"
echo ""
echo "Expected: Task queued in v7_worker.queue_message with SYSTEM lane"
echo ""

# Phase 3: Send heartbeat
echo "---------- PHASE 3: Initial Heartbeat ----------"
echo "Sending heartbeat for worker..."

HEARTBEAT_QUERY='
select v7_worker.send_heartbeat(
  '"'"'AGENT-CLAUDE-REVIEWER-01@STAGING'"'"',
  '"'"'idle'"'"',
  null,
  null,
  '"'"'DCSE-Command-Post'"'"',
  '"'"'claude/supabase-activity-report-3z1k0v'"'"',
  '"'"'claude-opus-5'"'"',
  '"'"'{"tools": ["read", "grep", "glob", "git_diff"]}'::jsonb,
  null
);
'

echo "Query to execute:"
echo "$HEARTBEAT_QUERY"
echo ""
echo "Expected: Heartbeat recorded in v7_worker.heartbeat"
echo ""

# Phase 4: Claim task
echo "---------- PHASE 4: Task Claim ----------"
echo "Attempting to claim DCSE V7 COMP 001..."

CLAIM_QUERY='
select queue_msg_id, task_id, lane, runtime_packet, attempt_number
from v7_worker.claim_next_task(
  '"'"'AGENT-CLAUDE-REVIEWER-01@STAGING'"'"',
  1800  -- 30 min visibility timeout
);
'

echo "Query to execute:"
echo "$CLAIM_QUERY"
echo ""
echo "Expected: Task claimed with attempt_number = 1"
echo "Output will include runtime_packet with task instructions"
echo ""

# Phase 5: Execute review (this would invoke node workers/claude-reviewer-worker.js)
echo "---------- PHASE 5: Review Execution ----------"
echo "Starting Claude Reviewer Worker in Blueprint Mode..."
echo ""
echo "Command to execute:"
echo "  cd $REPO_ROOT && node workers/claude-reviewer-worker.js"
echo ""
echo "Expected behavior:"
echo "  1. Worker reads claimed task and runtime_packet"
echo "  2. Executes architecture review (DCSE V7 COMP 001 scope)"
echo "  3. Produces findings document"
echo "  4. Generates repair tasks"
echo "  5. Inserts result_submission with status='pending'"
echo "  6. Returns completion receipt"
echo ""

# Phase 6: Submit results
echo "---------- PHASE 6: Result Submission ----------"
echo "Results will be written to v7_worker.result_submission"
echo ""
echo "Query executed by worker:"
echo "  INSERT INTO v7_worker.result_submission ("
echo "    task_id, claim_id, agent_id, submission_status, "
echo "    result_event_type, result_output"
echo "  ) VALUES ("
echo "    'DCSE-V7-COMP-001', <claim_id>, 'AGENT-CLAUDE-REVIEWER-01@STAGING',"
echo "    'pending', 'completed', <findings_json>"
echo "  );"
echo ""

# Phase 7: Bridge processing
echo "---------- PHASE 7: Result Bridge Processing ----------"
echo "Result bridge processes pending submission..."
echo ""
echo "Bridge operations:"
echo "  1. READ: v7_worker.result_submission WHERE status='pending'"
echo "  2. VALIDATE: result_output structure"
echo "  3. WRITE: INSERT into dcse_cp.agent_task_events"
echo "  4. UPDATE: v7_bootstrap.tasks status → 'completed'"
echo "  5. ACK: UPDATE result_submission status → 'acked'"
echo "  6. RECORD: audit receipt"
echo ""

# Phase 8: Verification
echo "---------- PHASE 8: Completion Verification ----------"
echo "Verifying end-to-end cycle completion..."
echo ""

VERIFY_QUERY='
select
  '"'"'Task Claimed'"'"' as step,
  count(*) filter (where released_at is null) as active_claims
from v7_worker.task_claim where task_id = '"'"'DCSE-V7-COMP-001'"'"'
union all
select
  '"'"'Result Submitted'"'"',
  count(*) filter (where submission_status = '"'"'acked'"'"')
from v7_worker.result_submission where task_id = '"'"'DCSE-V7-COMP-001'"'"'
union all
select
  '"'"'Event Written to dcse_cp'"'"',
  count(*)
from dcse_cp.agent_task_events where task_id = '"'"'DCSE-V7-COMP-001'"'"'
;
'

echo "Verification query:"
echo "$VERIFY_QUERY"
echo ""
echo "Expected results:"
echo "  Task Claimed: 1"
echo "  Result Submitted: 1"
echo "  Event Written to dcse_cp: 1"
echo ""

# Phase 9: Repair tasks
echo "---------- PHASE 9: Repair Task Generation ----------"
echo "Reviewing findings, generating repair tasks..."
echo ""

REPAIR_QUERY='
select repair_task_id, finding_id, title, assigned_lane, estimated_effort
from dcse_cp.agent_repair_tasks
where review_id = '"'"'DCSE-V7-COMP-001'"'"'
order by priority;
'

echo "Query to list repair tasks:"
echo "$REPAIR_QUERY"
echo ""
echo "Expected: 4 repair tasks created (DCSE-V7-REPAIR-001 through 004)"
echo ""

# Final summary
echo "========================================================================"
echo "ACTIVATION CHECKLIST"
echo "========================================================================"
cat << 'EOF'
[  ] Worker identity verified in v7_worker.agent_identity
[  ] Worker status = 'candidate' or 'approved'
[  ] DCSE V7 COMP 001 task queued in v7_worker.queue_message
[  ] Initial heartbeat recorded in v7_worker.heartbeat
[  ] Task claimed in v7_worker.task_claim (attempt_number = 1)
[  ] Runtime packet loaded and validated
[  ] Claude Reviewer Worker executed (review completed)
[  ] Result submitted to v7_worker.result_submission (status = 'pending')
[  ] Result bridge processed (status updated to 'acked')
[  ] Event written to dcse_cp.agent_task_events
[  ] Task status updated in v7_bootstrap.tasks
[  ] Audit receipt created
[  ] Repair tasks generated (4 tasks)
[  ] Next autonomous task already queued
EOF

echo ""
echo "========================================================================"
echo "ACTIVATION SCRIPT COMPLETE"
echo "========================================================================"
echo "Next steps:"
echo "  1. Set SUPABASE_SERVICE_ROLE_KEY environment variable"
echo "  2. Verify worker identity query returns correct worker"
echo "  3. Run: cd $REPO_ROOT && node workers/claude-reviewer-worker.js"
echo "  4. Monitor v7_worker.heartbeat for status updates"
echo "  5. Verify result in dcse_cp.agent_task_events"
echo ""
