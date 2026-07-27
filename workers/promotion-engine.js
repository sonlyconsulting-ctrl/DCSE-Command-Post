/**
 * Promotion Engine - Phase F Implementation
 *
 * Manages artifact lifecycle through promotion state machine.
 *
 * Responsibilities:
 * 1. Track promotion states (Candidate → Promoted → Deprecated → Archived)
 * 2. Enforce approval gates at critical transitions
 * 3. Record every state change with no silent promotions
 * 4. Manage rollback and deprecation
 * 5. Produce audit trail
 */

class PromotionEngine {
  constructor(transitionRules = null) {
    this.transitionRules = transitionRules || this.getDefaultRules();
    this.promotions = new Map();
    this.auditLog = [];
  }

  /**
   * Create new promotion record
   */
  async initiate(request) {
    console.log(`[PromotionEngine] Initiating promotion for: ${request.artifact_id}`);

    const promotion = {
      promotion_id: this.generatePromotionId(),
      artifact_id: request.artifact_id,
      version: request.version || '1.0.0',
      current_state: 'Candidate',
      previous_state: null,
      created_at: new Date().toISOString(),
      created_by: request.created_by || 'system',
      state_history: [
        {
          state: 'Candidate',
          entered_at: new Date().toISOString(),
          entered_by: request.created_by || 'system',
          evidence_count: 0
        }
      ],
      metadata: {
        lane: request.lane,
        promotion_velocity_hours: 0,
        blocking_issues: 0,
        rejections: 0,
        rollbacks: 0,
        total_evidence_collected: 0
      },
      approval_gates: [],
      deprecation: {
        status: 'not_planned'
      },
      rollback: {
        rolled_back: false
      },
      audit: {
        total_transitions: 1,
        total_duration_hours: 0,
        approval_gates_passed: 0,
        rejection_gates_triggered: 0,
        last_updated_at: new Date().toISOString(),
        last_updated_by: request.created_by || 'system'
      }
    };

    this.promotions.set(promotion.promotion_id, promotion);
    this.logAudit('promotion_initiated', promotion.promotion_id, request.created_by);

    return promotion;
  }

  /**
   * Transition artifact to next state
   */
  async transitionState(promotionId, toState, trigger, evidence, actor) {
    console.log(`[PromotionEngine] Transitioning ${promotionId} → ${toState}`);

    const promotion = this.promotions.get(promotionId);
    if (!promotion) {
      throw new Error(`Promotion not found: ${promotionId}`);
    }

    const fromState = promotion.current_state;

    // 1. Validate transition
    const transitionValid = this.isValidTransition(fromState, toState);
    if (!transitionValid) {
      throw new Error(`Invalid transition: ${fromState} → ${toState}`);
    }

    // 2. Check for approval gates
    const gateRequired = this.requiresApprovalGate(fromState, toState);
    if (gateRequired) {
      const gate = {
        gate_id: `GATE-${Date.now()}`,
        transition: { from: fromState, to: toState },
        approvers: this.getApproversForTransition(fromState, toState),
        timeout_minutes: this.getTimeoutForTransition(fromState, toState),
        status: 'pending',
        requested_at: new Date().toISOString()
      };

      promotion.approval_gates.push(gate);
      this.logAudit('approval_gate_triggered', promotionId, actor);
      console.log(`  ⚠ Approval gate required: ${gate.gate_id}`);

      return {
        status: 'pending_approval',
        gate_id: gate.gate_id,
        message: `Approval required from ${gate.approvers.join(', ')}`
      };
    }

    // 3. Check for blocking conditions
    if (evidence?.blocking_findings && evidence.blocking_findings.length > 0) {
      promotion.previous_state = fromState;
      promotion.current_state = 'Rejected';
      promotion.metadata.rejections++;
      this.recordStateChange(promotion, 'Rejected', actor, trigger, evidence);
      this.logAudit('promotion_rejected', promotionId, actor);
      console.log(`  ✗ Promotion rejected (blocking findings)`);

      return {
        status: 'rejected',
        reason: `${evidence.blocking_findings.length} blocking findings`,
        findings: evidence.blocking_findings
      };
    }

    // 4. Execute transition
    promotion.previous_state = fromState;
    promotion.current_state = toState;
    this.recordStateChange(promotion, toState, actor, trigger, evidence);

    promotion.audit.total_transitions++;
    promotion.audit.last_updated_at = new Date().toISOString();
    promotion.audit.last_updated_by = actor;

    this.logAudit('state_transition', promotionId, actor);
    console.log(`  ✓ Transitioned to ${toState}`);

    return {
      status: 'transitioned',
      from: fromState,
      to: toState,
      transition_id: `TRN-${Date.now()}`
    };
  }

  /**
   * Record state transition in history
   */
  recordStateChange(promotion, state, actor, trigger, evidence) {
    const prevStateEntry = promotion.state_history[promotion.state_history.length - 1];
    const now = new Date();
    const prevTime = new Date(prevStateEntry.entered_at);
    const duration = Math.round((now - prevTime) / 1000 / 60); // minutes

    prevStateEntry.duration_minutes = duration;

    const newEntry = {
      state: state,
      entered_at: now.toISOString(),
      entered_by: actor,
      evidence_count: evidence?.evidence_count || 0
    };

    if (evidence?.findings) {
      newEntry.findings = {
        total: evidence.findings.length,
        blocking: evidence.findings.filter(f => f.blocks_promotion).length,
        repairable: evidence.findings.filter(f => f.status === 'repairable').length
      };
    }

    if (evidence?.acceptance_confidence) {
      newEntry.acceptance_confidence = evidence.acceptance_confidence;
    }

    promotion.state_history.push(newEntry);
  }

  /**
   * Approve a pending approval gate
   */
  async approveGate(promotionId, gateId, approvedBy, comment = '') {
    const promotion = this.promotions.get(promotionId);
    if (!promotion) throw new Error(`Promotion not found: ${promotionId}`);

    const gate = promotion.approval_gates.find(g => g.gate_id === gateId);
    if (!gate) throw new Error(`Gate not found: ${gateId}`);

    gate.status = 'approved';
    gate.responded_at = new Date().toISOString();
    gate.approved_by = approvedBy;

    promotion.audit.approval_gates_passed++;
    this.logAudit('approval_gate_approved', promotionId, approvedBy);

    console.log(`  ✓ Gate ${gateId} approved by ${approvedBy}`);

    // Auto-transition if this was the only blocker
    const transition = gate.transition;
    return await this.transitionState(
      promotionId,
      transition.to,
      'approval_granted',
      { approval_gate_id: gateId },
      approvedBy
    );
  }

  /**
   * Reject a pending approval gate
   */
  async rejectGate(promotionId, gateId, rejectedBy, reason) {
    const promotion = this.promotions.get(promotionId);
    const gate = promotion.approval_gates.find(g => g.gate_id === gateId);

    gate.status = 'rejected';
    gate.responded_at = new Date().toISOString();
    gate.rejection_reason = reason;

    promotion.current_state = 'Rejected';
    promotion.metadata.rejections++;

    this.logAudit('approval_gate_rejected', promotionId, rejectedBy);
    console.log(`  ✗ Gate ${gateId} rejected by ${rejectedBy}`);

    return { status: 'rejected', reason: reason };
  }

  /**
   * Rollback to previous state
   */
  async rollback(promotionId, rolledBackBy, reason) {
    const promotion = this.promotions.get(promotionId);
    if (!promotion) throw new Error(`Promotion not found: ${promotionId}`);

    const currentState = promotion.current_state;
    const previousState = promotion.previous_state;

    if (!previousState || ['Candidate', 'Archived'].includes(currentState)) {
      throw new Error(`Cannot rollback from state: ${currentState}`);
    }

    promotion.current_state = previousState;
    promotion.rollback = {
      rolled_back: true,
      rolled_back_at: new Date().toISOString(),
      rolled_back_by: rolledBackBy,
      reason: reason,
      previous_state: currentState
    };

    promotion.metadata.rollbacks++;
    promotion.audit.total_transitions++;

    this.logAudit('rollback_executed', promotionId, rolledBackBy);
    console.log(`  ↶ Rolled back from ${currentState} to ${previousState}`);

    return {
      status: 'rolled_back',
      from: currentState,
      to: previousState
    };
  }

  /**
   * Begin deprecation
   */
  async beginDeprecation(promotionId, replacementArtifactId, begumBy) {
    const promotion = this.promotions.get(promotionId);

    promotion.deprecation = {
      status: 'active',
      announced_at: new Date().toISOString(),
      end_of_life_at: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(),
      replacement_artifact_id: replacementArtifactId,
      usage_level: 'medium',
      notices_sent: 1
    };

    this.logAudit('deprecation_begun', promotionId, begumBy);
    console.log(`  ⚠ Deprecation begun for ${promotionId}`);

    return promotion.deprecation;
  }

  /**
   * Validate transition
   */
  isValidTransition(fromState, toState) {
    const validTransitions = {
      'Candidate': ['Reviewed', 'Rejected'],
      'Reviewed': ['Validated', 'Rejected'],
      'Validated': ['Approved', 'Rejected'],
      'Approved': ['Promoted', 'Rejected'],
      'Promoted': ['Deprecated', 'Rolled Back', 'Superseded'],
      'Deprecated': ['Archived'],
      'Archived': [],
      'Rejected': [],
      'Rolled Back': [],
      'Superseded': []
    };

    return (validTransitions[fromState] || []).includes(toState);
  }

  /**
   * Check if approval gate is required
   */
  requiresApprovalGate(fromState, toState) {
    const gateRequiredTransitions = [
      ['Reviewed', 'Validated'],
      ['Validated', 'Approved'],
      ['Approved', 'Promoted']
    ];

    return gateRequiredTransitions.some(
      ([from, to]) => from === fromState && to === toState
    );
  }

  /**
   * Get approvers for transition
   */
  getApproversForTransition(fromState, toState) {
    const approverMap = {
      'Reviewed-Validated': ['code_reviewer'],
      'Validated-Approved': ['DCSE'],
      'Approved-Promoted': ['DCSE', 'deployment_lead']
    };

    const key = `${fromState}-${toState}`;
    return approverMap[key] || ['DCSE'];
  }

  /**
   * Get timeout for transition
   */
  getTimeoutForTransition(fromState, toState) {
    const timeoutMap = {
      'Reviewed-Validated': 60,
      'Validated-Approved': 120,
      'Approved-Promoted': 180
    };

    const key = `${fromState}-${toState}`;
    return timeoutMap[key] || 60;
  }

  /**
   * Get default transition rules
   */
  getDefaultRules() {
    return {
      automatic: [
        {
          from: 'Candidate',
          to: 'Reviewed',
          condition: 'code_review_approved && all_tests_passed && !critical_findings'
        }
      ],
      manual_approval: [
        {
          from: 'Reviewed',
          to: 'Validated',
          approvers: ['code_reviewer'],
          timeout_minutes: 60
        },
        {
          from: 'Validated',
          to: 'Approved',
          approvers: ['DCSE'],
          timeout_minutes: 120
        },
        {
          from: 'Approved',
          to: 'Promoted',
          approvers: ['DCSE', 'deployment_lead'],
          timeout_minutes: 180
        }
      ],
      blocking: [
        { from: 'Candidate', to: 'Rejected', trigger: 'stop_gate_finding' },
        { from: 'Reviewed', to: 'Rejected', trigger: 'acceptance_suite_failed' },
        { from: 'Validated', to: 'Rejected', trigger: 'governance_denied' }
      ]
    };
  }

  /**
   * Log audit event
   */
  logAudit(eventType, promotionId, actor) {
    this.auditLog.push({
      event_type: eventType,
      promotion_id: promotionId,
      actor: actor,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Get promotion record
   */
  getPromotion(promotionId) {
    return this.promotions.get(promotionId);
  }

  /**
   * Generate promotion ID
   */
  generatePromotionId() {
    const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 8);
    const random = Math.random().toString(36).substring(2, 8);
    return `PRO-${timestamp}-${random}`;
  }
}

module.exports = PromotionEngine;

// Test if run directly
if (require.main === module) {
  (async () => {
    const engine = new PromotionEngine();

    console.log('\n' + '='.repeat(80));
    console.log('PROMOTION ENGINE TEST');
    console.log('='.repeat(80));

    // Test 1: Initiate promotion
    console.log('\n--- Test 1: Initiate Promotion ---\n');
    const promotion = await engine.initiate({
      artifact_id: 'PKT-20260727-abc123',
      version: '1.0.0',
      lane: 'SC',
      created_by: 'claude-reviewer'
    });

    console.log(`Promotion ID: ${promotion.promotion_id}`);
    console.log(`State: ${promotion.current_state}`);
    console.log(`Created: ${promotion.created_at}`);

    // Test 2: Transition to Reviewed
    console.log('\n--- Test 2: Transition to Reviewed ---\n');
    const result2 = await engine.transitionState(
      promotion.promotion_id,
      'Reviewed',
      'code_review_approved',
      { evidence_count: 5 },
      'code-reviewer-1'
    );
    console.log(`Result: ${result2.status}`);

    // Test 3: Transition to Validated (requires approval gate)
    console.log('\n--- Test 3: Transition to Validated (Approval Gate) ---\n');
    const result3 = await engine.transitionState(
      promotion.promotion_id,
      'Validated',
      'acceptance_passed',
      { evidence_count: 12, acceptance_confidence: 0.92 },
      'claude-reviewer'
    );
    console.log(`Result: ${result3.status}`);
    if (result3.status === 'pending_approval') {
      console.log(`Gate ID: ${result3.gate_id}`);
      console.log(`Message: ${result3.message}`);

      // Approve the gate
      console.log('\n--- Approving Gate ---\n');
      const approved = await engine.approveGate(
        promotion.promotion_id,
        result3.gate_id,
        'code-reviewer-1'
      );
      console.log(`Approval result: ${approved.status}`);
    }

    // Test 4: Transition to Approved
    console.log('\n--- Test 4: Transition to Approved (Approval Gate) ---\n');
    const updated = engine.getPromotion(promotion.promotion_id);
    const result4 = await engine.transitionState(
      promotion.promotion_id,
      'Approved',
      'governance_approved',
      { evidence_count: 20 },
      'dcse-approver'
    );
    console.log(`Result: ${result4.status}`);

    // Test 5: View promotion state
    console.log('\n--- Test 5: Current Promotion State ---\n');
    const current = engine.getPromotion(promotion.promotion_id);
    console.log(`Current State: ${current.current_state}`);
    console.log(`Total Transitions: ${current.audit.total_transitions}`);
    console.log(`Approval Gates Passed: ${current.audit.approval_gates_passed}`);
    console.log(`State History:`);
    current.state_history.forEach((entry, i) => {
      console.log(`  ${i}: ${entry.state} @ ${entry.entered_at.substring(11, 16)}`);
    });

    console.log('\n' + '='.repeat(80));
  })();
}
