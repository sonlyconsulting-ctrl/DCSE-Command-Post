/**
 * Dispatcher/Recovery Service - Phase 1D
 *
 * Deterministic task orchestration and infrastructure recovery.
 * Minimal LLM involvement - primarily state machine logic and routing.
 *
 * Responsibilities:
 * 1. Dependency routing: resolve task prerequisites and ordering
 * 2. Stale lease recovery: detect and recover from abandoned task claims
 * 3. Heartbeat expiry handling: clean up inactive worker sessions
 * 4. Retry scheduling: re-queue failed tasks with backoff
 * 5. Dead-letter movement: escalate exhausted retries
 * 6. Cost-stop enforcement: prevent over-budget task execution
 * 7. Stop-Gate generation: escalate Level 0 decisions for manual review
 * 8. Orphan task recovery: identify tasks without claims or parents
 * 9. Duplicate prevention: detect and consolidate duplicate task enqueuing
 * 10. Queue metrics: track throughput, latency, error rates
 * 11. Escalation receipts: generate structured audit trails
 *
 * Deploy as: systemd service, Kubernetes deployment, or Cloud Run service
 * Polling interval: 10 seconds
 * Heartbeat timeout: 5 minutes (300s) - if no heartbeat, mark stale
 * Lease timeout: 30 minutes (1800s) - if claim not released, recover
 */

const crypto = require('crypto');

class DispatcherRecoveryService {
  constructor() {
    this.serviceId = 'DISPATCHER-RECOVERY-SERVICE-01@STAGING';
    this.pollingIntervalMs = 10000;  // 10 seconds
    this.heartbeatTimeoutMs = 5 * 60 * 1000;  // 5 minutes
    this.leaseTimeoutMs = 30 * 60 * 1000;  // 30 minutes
    this.maxRetries = 3;
    this.backoffMs = [1000, 5000, 30000];  // Exponential backoff

    this.metrics = {
      tasks_processed: 0,
      tasks_completed: 0,
      tasks_failed: 0,
      tasks_dead_lettered: 0,
      stale_leases_recovered: 0,
      stop_gates_created: 0,
      duplicates_detected: 0,
      start_time: Date.now()
    };

    this.escalations = [];
  }

  /**
   * Phase 1: Dependency Routing
   * Resolve task prerequisites and establish execution order
   */
  routeTaskDependencies(queuedTasks) {
    console.log('[DISPATCHER] Phase 1: Dependency Routing...');

    const taskGraph = new Map();

    for (const task of queuedTasks) {
      const dependencies = this.extractDependencies(task);
      taskGraph.set(task.task_id, {
        task,
        dependencies,
        ready: dependencies.length === 0,
        status: 'pending'
      });
    }

    // Topological sort
    const readyTasks = [];
    const visited = new Set();

    const visit = (taskId) => {
      if (visited.has(taskId)) return;
      visited.add(taskId);

      const node = taskGraph.get(taskId);
      if (!node) return;

      for (const dep of node.dependencies) {
        visit(dep);
      }

      if (node.ready) {
        readyTasks.push(node.task);
      }
    };

    for (const taskId of taskGraph.keys()) {
      visit(taskId);
    }

    console.log(`✓ Routed ${readyTasks.length}/${queuedTasks.length} tasks ready to execute`);
    return readyTasks;
  }

  /**
   * Extract task dependencies from parent_task_id or prerequisite fields
   */
  extractDependencies(task) {
    const deps = [];
    if (task.parent_task_id) {
      deps.push(task.parent_task_id);
    }
    if (task.depends_on && Array.isArray(task.depends_on)) {
      deps.push(...task.depends_on);
    }
    return deps;
  }

  /**
   * Phase 2: Stale Lease Recovery
   * Detect abandoned task claims and recover them
   */
  recoverStaleLeasess(activeClaims) {
    console.log('[DISPATCHER] Phase 2: Stale Lease Recovery...');

    const now = Date.now();
    const recovered = [];

    for (const claim of activeClaims) {
      const claimedAtMs = new Date(claim.claimed_at).getTime();
      const ageMs = now - claimedAtMs;

      if (ageMs > this.leaseTimeoutMs) {
        console.log(`  ⚠ Stale lease: ${claim.task_id} (age: ${(ageMs / 1000).toFixed(0)}s)`);

        recovered.push({
          claim_id: claim.claim_id,
          task_id: claim.task_id,
          reason: 'lease_timeout_exceeded',
          recovery_at: new Date().toISOString(),
          action: 'release_claim_and_re_enqueue'
        });

        this.metrics.stale_leases_recovered++;
      }
    }

    console.log(`✓ Recovered ${recovered.length} stale leases`);
    return recovered;
  }

  /**
   * Phase 3: Heartbeat Expiry Handling
   * Clean up inactive worker sessions
   */
  handleHeartbeatExpiries(workerHeartbeats) {
    console.log('[DISPATCHER] Phase 3: Heartbeat Expiry Handling...');

    const now = Date.now();
    const expired = [];

    for (const hb of workerHeartbeats) {
      const lastHbMs = new Date(hb.sent_at).getTime();
      const silenceMs = now - lastHbMs;

      if (silenceMs > this.heartbeatTimeoutMs) {
        console.log(`  ⚠ Dead worker: ${hb.agent_id} (silence: ${(silenceMs / 1000).toFixed(0)}s)`);

        expired.push({
          agent_id: hb.agent_id,
          last_heartbeat_at: hb.sent_at,
          expired_at: new Date().toISOString(),
          action: 'mark_offline_recover_claims'
        });
      }
    }

    console.log(`✓ Identified ${expired.length} expired heartbeats`);
    return expired;
  }

  /**
   * Phase 4: Retry Scheduling
   * Re-queue failed tasks with exponential backoff
   */
  scheduleRetries(failedTasks) {
    console.log('[DISPATCHER] Phase 4: Retry Scheduling...');

    const retried = [];

    for (const task of failedTasks) {
      const retryCount = task.retry_count || 0;

      if (retryCount >= this.maxRetries) {
        console.log(`  ✗ Max retries exceeded: ${task.task_id} (${retryCount}/${this.maxRetries})`);
        continue;  // Will be moved to dead-letter in next phase
      }

      const backoffMs = this.backoffMs[retryCount] || this.backoffMs[this.backoffMs.length - 1];
      const retryAt = new Date(Date.now() + backoffMs).toISOString();

      retried.push({
        task_id: task.task_id,
        retry_count: retryCount + 1,
        retry_at: retryAt,
        reason: task.last_error,
        backoff_ms: backoffMs
      });

      console.log(`  → Retry ${retryCount + 1}/${this.maxRetries}: scheduled ${(backoffMs / 1000).toFixed(0)}s from now`);
    }

    console.log(`✓ Scheduled ${retried.length} retries`);
    return retried;
  }

  /**
   * Phase 5: Dead-Letter Movement
   * Escalate exhausted retries to dead-letter queue
   */
  moveToDeadLetter(exhaustedTasks) {
    console.log('[DISPATCHER] Phase 5: Dead-Letter Movement...');

    const deadLettered = [];

    for (const task of exhaustedTasks) {
      const retryCount = task.retry_count || 0;

      if (retryCount >= this.maxRetries) {
        console.log(`  ☠ Dead-lettering: ${task.task_id} (${retryCount}/${this.maxRetries} retries)`);

        deadLettered.push({
          task_id: task.task_id,
          dead_lettered_at: new Date().toISOString(),
          reason: 'max_retries_exceeded',
          error_summary: task.last_error,
          escalation_required: true
        });

        this.metrics.tasks_dead_lettered++;
      }
    }

    console.log(`✓ Moved ${deadLettered.length} tasks to dead-letter`);
    return deadLettered;
  }

  /**
   * Phase 6: Cost-Stop Enforcement
   * Prevent execution of tasks that would exceed cost limits
   */
  enforceCostStops(pendingTasks, costLedger) {
    console.log('[DISPATCHER] Phase 6: Cost-Stop Enforcement...');

    const stopped = [];

    for (const task of pendingTasks) {
      const agentLedger = costLedger.filter(e => e.agent_id === task.worker_id);
      const monthlySpent = agentLedger
        .filter(e => new Date(e.date).getMonth() === new Date().getMonth())
        .reduce((sum, e) => sum + (e.cost_usd || 0), 0);

      const estimatedTotal = monthlySpent + (task.cost_estimate_usd || 0);
      const agentLimit = task.cost_limit_usd || 100;

      if (estimatedTotal > agentLimit) {
        console.log(`  🛑 Cost stop: ${task.task_id} (spent: $${monthlySpent.toFixed(2)}, limit: $${agentLimit})`);

        stopped.push({
          task_id: task.task_id,
          worker_id: task.worker_id,
          current_month_spent: monthlySpent,
          cost_estimate: task.cost_estimate_usd,
          would_exceed_limit: estimatedTotal > agentLimit,
          limit_usd: agentLimit,
          action: 'stop_and_escalate_to_stop_gate'
        });

        this.metrics.tasks_failed++;
      }
    }

    console.log(`✓ Applied cost stops to ${stopped.length} tasks`);
    return stopped;
  }

  /**
   * Phase 7: Stop-Gate Generation
   * Escalate Level 0 decisions for manual review
   */
  generateStopGates(escalationItems) {
    console.log('[DISPATCHER] Phase 7: Stop-Gate Generation...');

    const gates = [];

    for (const item of escalationItems) {
      const gate = {
        stop_gate_id: `STOP-${crypto.randomBytes(8).toString('hex')}`,
        task_id: item.task_id || item.context,
        escalation_type: item.type,
        severity: item.severity || 'high',
        description: item.description,
        created_at: new Date().toISOString(),
        requires_approval: true,
        decision_deadline: new Date(Date.now() + 24 * 3600 * 1000).toISOString(),
        context: item
      };

      gates.push(gate);
      this.metrics.stop_gates_created++;

      console.log(`  🚫 Stop-gate created: ${gate.stop_gate_id} (${gate.escalation_type})`);
    }

    console.log(`✓ Generated ${gates.length} stop-gates`);
    return gates;
  }

  /**
   * Phase 8: Orphan Task Recovery
   * Identify and recover tasks without claims or parents
   */
  recoverOrphanTasks(allTasks, activeClaims, taskResults) {
    console.log('[DISPATCHER] Phase 8: Orphan Task Recovery...');

    const claimedTaskIds = new Set(activeClaims.map(c => c.task_id));
    const resultTaskIds = new Set(taskResults.map(r => r.task_id));

    const orphans = [];

    for (const task of allTasks) {
      const isClaimed = claimedTaskIds.has(task.task_id);
      const hasResult = resultTaskIds.has(task.task_id);
      const isParented = !!task.parent_task_id;

      // Orphan: no claim, no result, no parent (root task with no progress)
      if (!isClaimed && !hasResult && !isParented) {
        if (task.enqueued_at &&
            Date.now() - new Date(task.enqueued_at).getTime() > 10 * 60 * 1000) {
          console.log(`  🔍 Orphan detected: ${task.task_id}`);
          orphans.push({
            task_id: task.task_id,
            enqueued_at: task.enqueued_at,
            age_minutes: (Date.now() - new Date(task.enqueued_at).getTime()) / 60000,
            recovery_action: 're_enqueue_with_higher_priority'
          });
        }
      }
    }

    console.log(`✓ Recovered ${orphans.length} orphan tasks`);
    return orphans;
  }

  /**
   * Phase 9: Duplicate Prevention
   * Detect and consolidate duplicate task enqueuing
   */
  detectDuplicates(queuedTasks) {
    console.log('[DISPATCHER] Phase 9: Duplicate Prevention...');

    const taskSigs = new Map();
    const duplicates = [];

    for (const task of queuedTasks) {
      // Create signature: {task_type, lane, parent_task_id}
      const sig = `${task.task_type}:${task.lane}:${task.parent_task_id || 'ROOT'}`;

      if (taskSigs.has(sig)) {
        const existing = taskSigs.get(sig);
        console.log(`  ⚠ Duplicate: ${task.task_id} matches ${existing.task_id}`);

        duplicates.push({
          original_task_id: existing.task_id,
          duplicate_task_id: task.task_id,
          signature: sig,
          action: 'delete_duplicate_keep_original'
        });

        this.metrics.duplicates_detected++;
      } else {
        taskSigs.set(sig, task);
      }
    }

    console.log(`✓ Detected ${duplicates.length} duplicates`);
    return duplicates;
  }

  /**
   * Phase 10: Queue Metrics
   * Track throughput, latency, error rates
   */
  computeQueueMetrics(tasks, activeClaims, results) {
    console.log('[DISPATCHER] Phase 10: Queue Metrics...');

    const upTimeMs = Date.now() - this.metrics.start_time;
    const tasksPerMinute = (this.metrics.tasks_processed / upTimeMs) * 60000;

    const completedTasks = results.filter(r => r.status === 'completed');
    const avgLatencyMs = completedTasks.length > 0
      ? completedTasks.reduce((sum, r) => sum + (r.duration_ms || 0), 0) / completedTasks.length
      : 0;

    const queueMetrics = {
      timestamp: new Date().toISOString(),
      uptime_minutes: (upTimeMs / 60000).toFixed(1),
      total_tasks_processed: this.metrics.tasks_processed,
      total_tasks_completed: this.metrics.tasks_completed,
      total_tasks_failed: this.metrics.tasks_failed,
      total_dead_lettered: this.metrics.tasks_dead_lettered,
      queue_depth: tasks.filter(t => !t.claimed_at).length,
      active_claims: activeClaims.length,
      throughput_tasks_per_minute: tasksPerMinute.toFixed(2),
      avg_latency_ms: Math.round(avgLatencyMs),
      stale_leases_recovered: this.metrics.stale_leases_recovered,
      stop_gates_created: this.metrics.stop_gates_created,
      duplicates_detected: this.metrics.duplicates_detected,
      error_rate_percent: this.metrics.tasks_processed > 0
        ? ((this.metrics.tasks_failed / this.metrics.tasks_processed) * 100).toFixed(1)
        : 0
    };

    console.log(`✓ Queue metrics computed`);
    return queueMetrics;
  }

  /**
   * Phase 11: Escalation Receipts
   * Generate structured audit trails
   */
  generateEscalationReceipt(escalatedItems, queueMetrics) {
    console.log('[DISPATCHER] Phase 11: Escalation Receipts...');

    const receipt = {
      escalation_receipt_id: `ESC-${crypto.randomUUID()}`,
      service_id: this.serviceId,
      timestamp: new Date().toISOString(),
      polling_cycle: {
        poll_interval_ms: this.pollingIntervalMs,
        cycle_count: Math.floor((Date.now() - this.metrics.start_time) / this.pollingIntervalMs)
      },
      escalations: escalatedItems,
      metrics: queueMetrics,
      actions_taken: {
        stale_leases_recovered: this.metrics.stale_leases_recovered,
        stop_gates_created: this.metrics.stop_gates_created,
        tasks_dead_lettered: this.metrics.tasks_dead_lettered,
        duplicates_consolidated: this.metrics.duplicates_detected
      }
    };

    console.log(`✓ Escalation receipt generated (${receipt.escalation_receipt_id})`);
    return receipt;
  }

  /**
   * Run complete dispatcher cycle
   */
  async runPollingCycle() {
    console.log('\n' + '='.repeat(80));
    console.log('PHASE 1D: Dispatcher/Recovery Service - Polling Cycle');
    console.log('='.repeat(80));
    console.log(`Service: ${this.serviceId}`);
    console.log(`Cycle started at: ${new Date().toISOString()}`);

    // Simulate fetching queue state
    const queuedTasks = [
      { task_id: 'DCSE-V7-REPAIR-001', task_type: 'implement_feature', lane: 'SC', retry_count: 0 },
      { task_id: 'DCSE-V7-REPAIR-002', task_type: 'implement_feature', lane: 'SC', retry_count: 1 }
    ];

    const activeClaims = [
      { claim_id: 123, task_id: 'DCSE-V7-COMP-001', claimed_at: new Date(Date.now() - 60000).toISOString() }
    ];

    const failedTasks = [];
    const costLedger = [];
    const workerHeartbeats = [];
    const allTasks = [...queuedTasks];
    const taskResults = [];

    try {
      // Execute all phases
      const ready = this.routeTaskDependencies(queuedTasks);
      const recovered = this.recoverStaleLeasess(activeClaims);
      const expired = this.handleHeartbeatExpiries(workerHeartbeats);
      const retried = this.scheduleRetries(failedTasks);
      const deadLettered = this.moveToDeadLetter(failedTasks.filter(t => (t.retry_count || 0) >= this.maxRetries));
      const costStopped = this.enforceCostStops(queuedTasks, costLedger);
      const gates = this.generateStopGates([
        ...costStopped.map(c => ({ type: 'cost_limit', task_id: c.task_id, description: `Cost limit exceeded` }))
      ]);
      const orphans = this.recoverOrphanTasks(allTasks, activeClaims, taskResults);
      const dups = this.detectDuplicates(queuedTasks);
      const metrics = this.computeQueueMetrics(queuedTasks, activeClaims, taskResults);
      const receipt = this.generateEscalationReceipt([...gates], metrics);

      console.log('\n' + '='.repeat(80));
      console.log('✓ DISPATCHER CYCLE COMPLETE');
      console.log('='.repeat(80));

      return {
        success: true,
        cycle_summary: {
          ready_to_claim: ready.length,
          stale_leases_recovered: recovered.length,
          expired_workers: expired.length,
          retries_scheduled: retried.length,
          dead_lettered: deadLettered.length,
          cost_stops_enforced: costStopped.length,
          stop_gates_created: gates.length,
          orphans_recovered: orphans.length,
          duplicates_detected: dups.length
        },
        metrics,
        receipt
      };
    } catch (error) {
      console.error(`✗ Dispatcher cycle failed: ${error.message}`);
      throw error;
    }
  }
}

module.exports = DispatcherRecoveryService;

if (require.main === module) {
  const dispatcher = new DispatcherRecoveryService();
  dispatcher.runPollingCycle().catch(err => {
    console.error(err);
    process.exit(1);
  });
}
