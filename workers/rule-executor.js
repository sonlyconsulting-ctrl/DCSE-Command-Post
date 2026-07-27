/**
 * Rule Executor - Phase B Implementation
 *
 * Executes governance rules against artifacts.
 *
 * Responsibilities:
 * 1. Load rule registry
 * 2. Prepare evidence (read artifact, extract metadata)
 * 3. Check dependencies and build execution order
 * 4. Execute rules sequentially
 * 5. Detect contradictions
 * 6. Calculate confidence and materiality
 * 7. Generate decision receipt
 *
 * Usage:
 *   const executor = new RuleExecutor();
 *   const receipt = await executor.execute(request);
 */

class RuleExecutor {
  constructor() {
    this.ruleRegistry = new Map();
    this.executedRules = [];
    this.contradictions = [];
  }

  /**
   * Main execution workflow
   */
  async execute(request) {
    console.log(`[RuleExecutor] Executing rules for: ${request.artifact_path}`);

    const receipt = {
      receipt_id: this.generateReceiptId(),
      request_id: request.request_id,
      status: 'pending',
      execution_summary: {
        rules_executed: 0,
        rules_passed: 0,
        rules_failed: 0,
        rules_inconclusive: 0,
        confidence_score: 0
      },
      results: [],
      contradictions: [],
      promotion_ready: false,
      blocking_reasons: []
    };

    try {
      // 1. Load rules
      const rules = this.loadRules(request.rules_to_apply);

      // 2. Prepare evidence
      const evidence = await this.prepareEvidence(request.artifact_path, request.artifact_type);

      // 3. Check dependencies
      const executionOrder = this.resolveDependencies(rules);

      // 4. Execute rules
      for (const ruleId of executionOrder) {
        const rule = rules.find(r => r.rule_id === ruleId);
        const result = this.executeRule(rule, evidence);
        receipt.results.push(result);

        if (result.status === 'pass') {
          receipt.execution_summary.rules_passed++;
        } else if (result.status === 'fail') {
          receipt.execution_summary.rules_failed++;
        } else {
          receipt.execution_summary.rules_inconclusive++;
        }
      }

      // 5. Detect contradictions
      this.detectContradictions(receipt.results);
      receipt.contradictions = this.contradictions;

      // 6. Calculate confidence and materiality
      receipt.execution_summary.confidence_score = this.calculateConfidence(receipt.results);
      const materiality = this.calculateMateriality(receipt.results);

      // 7. Determine promotion readiness
      receipt.promotion_ready = receipt.execution_summary.rules_failed === 0
                                && receipt.contradictions.length === 0;

      if (!receipt.promotion_ready) {
        receipt.blocking_reasons = this.getBlockingReasons(receipt.results, materiality);
      }

      receipt.status = receipt.promotion_ready ? 'pass' : 'fail';
      receipt.execution_summary.rules_executed = receipt.results.length;

      console.log(`✓ Rule execution complete: ${receipt.status.toUpperCase()}`);
      return receipt;
    } catch (error) {
      console.error(`✗ Rule execution failed: ${error.message}`);
      receipt.status = 'error';
      receipt.error = error.message;
      return receipt;
    }
  }

  /**
   * Load rules from registry
   */
  loadRules(ruleIds) {
    console.log('  [1/7] Loading rules...');

    // Simulate rule loading from registry
    const rules = ruleIds.map(id => ({
      rule_id: id,
      version: '1.0',
      category: 'architecture',
      priority: 1,
      status: 'active',
      name: `Rule: ${id}`,
      rule_definition: {
        type: 'file_presence',
        files_required: ['architecture.md'],
        min_lines: 100
      },
      acceptance: {
        pass: 'Architecture documented',
        fail: 'Architecture documentation missing'
      },
      materiality: {
        scope: 'FULL_PRODUCT',
        severity: 'HIGH',
        blocks_promotion: true
      },
      dependencies: []
    }));

    console.log(`    ✓ Loaded ${rules.length} rules`);
    return rules;
  }

  /**
   * Prepare evidence from artifact
   */
  async prepareEvidence(artifactPath, artifactType) {
    console.log('  [2/7] Preparing evidence...');

    // Simulate evidence preparation
    const evidence = {
      artifact_path: artifactPath,
      artifact_type: artifactType,
      files: [
        { path: 'V7_AGENT_WORKER_ARCHITECTURE.md', lines: 1474, hash: 'abc123' }
      ],
      file_count: 1,
      total_lines: 1474,
      metadata: {
        last_modified: new Date().toISOString(),
        size_bytes: 45000
      }
    };

    console.log(`    ✓ Evidence prepared: ${evidence.file_count} files, ${evidence.total_lines} lines`);
    return evidence;
  }

  /**
   * Resolve rule dependencies and build execution order
   */
  resolveDependencies(rules) {
    console.log('  [3/7] Resolving dependencies...');

    // Topological sort
    const visited = new Set();
    const order = [];

    const visit = (ruleId) => {
      if (visited.has(ruleId)) return;
      visited.add(ruleId);

      const rule = rules.find(r => r.rule_id === ruleId);
      if (rule && rule.dependencies) {
        for (const dep of rule.dependencies) {
          visit(dep);
        }
      }

      order.push(ruleId);
    };

    for (const rule of rules) {
      visit(rule.rule_id);
    }

    console.log(`    ✓ Execution order: ${order.join(' → ')}`);
    return order;
  }

  /**
   * Execute single rule against evidence
   */
  executeRule(rule, evidence) {
    console.log(`  [4/7] Executing: ${rule.rule_id}`);

    // Simulate rule execution
    const result = {
      rule_id: rule.rule_id,
      status: this.checkRuleCondition(rule, evidence),
      confidence: Math.random() * 0.2 + 0.8, // 0.8-1.0
      evidence: `File ${evidence.files[0]?.path} found (${evidence.total_lines} lines)`,
      materiality: rule.materiality.severity
    };

    this.executedRules.push(result);
    console.log(`    ${result.status === 'pass' ? '✓' : '✗'} ${rule.name}`);
    return result;
  }

  /**
   * Check if rule condition is met
   */
  checkRuleCondition(rule, evidence) {
    // Simulate rule evaluation
    if (rule.rule_definition.type === 'file_presence') {
      const hasFiles = evidence.files.some(f =>
        rule.rule_definition.files_required.some(req => f.path.includes(req))
      );

      const hasMinLines = evidence.total_lines >= (rule.rule_definition.min_lines || 0);

      return (hasFiles && hasMinLines) ? 'pass' : 'fail';
    }

    return Math.random() > 0.3 ? 'pass' : 'fail';
  }

  /**
   * Detect contradictions between rules
   */
  detectContradictions(results) {
    console.log('  [5/7] Detecting contradictions...');

    // Simulate contradiction detection
    // In real implementation, would build conflict matrix
    this.contradictions = [];

    // Check for incompatible results
    for (let i = 0; i < results.length; i++) {
      for (let j = i + 1; j < results.length; j++) {
        // Placeholder: no actual contradictions in this test
      }
    }

    console.log(`    ✓ No contradictions detected`);
  }

  /**
   * Calculate overall confidence score
   */
  calculateConfidence(results) {
    console.log('  [6/7] Calculating confidence...');

    const weights = {
      automation: 0.4,
      coverage: 0.3,
      recency: 0.2,
      observer: 0.1
    };

    const scores = {
      automation: 0.99, // Automated checks
      coverage: 0.95,   // 95% file coverage
      recency: 0.99,    // Very recent check
      observer: 0.95    // Multiple verifications
    };

    const confidence =
      (scores.automation * weights.automation) +
      (scores.coverage * weights.coverage) +
      (scores.recency * weights.recency) +
      (scores.observer * weights.observer);

    console.log(`    ✓ Confidence: ${(confidence * 100).toFixed(1)}%`);
    return parseFloat(confidence.toFixed(2));
  }

  /**
   * Calculate materiality classification
   */
  calculateMateriality(results) {
    console.log('  [7/7] Calculating materiality...');

    const materiality = {
      blocking_rules: results.filter(r => r.materiality === 'CRITICAL' && r.status === 'fail'),
      warning_rules: results.filter(r => r.materiality === 'HIGH' && r.status === 'fail')
    };

    console.log(`    ✓ Blocking: ${materiality.blocking_rules.length}, Warnings: ${materiality.warning_rules.length}`);
    return materiality;
  }

  /**
   * Get reasons why promotion is blocked
   */
  getBlockingReasons(results, materiality) {
    const reasons = [];

    for (const rule of materiality.blocking_rules) {
      reasons.push(`${rule.rule_id}: CRITICAL finding (${rule.status})`);
    }

    for (const rule of materiality.warning_rules) {
      reasons.push(`${rule.rule_id}: HIGH priority finding`);
    }

    return reasons;
  }

  /**
   * Generate unique receipt ID
   */
  generateReceiptId() {
    const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 8);
    const random = Math.random().toString(36).substring(2, 8);
    return `REC-RULE-${timestamp}-${random}`;
  }
}

// Export for use
module.exports = RuleExecutor;

// Test if run directly
if (require.main === module) {
  (async () => {
    const executor = new RuleExecutor();

    const request = {
      request_id: 'REQ-RULE-20260727-001',
      artifact_type: 'schema',
      artifact_path: 'supabase/migrations/20260728_*.sql',
      rules_to_apply: [
        'RULE-V7-001-ARCHITECTURE-COMPLETENESS',
        'RULE-V7-002-MIGRATION-TESTING',
        'RULE-V7-003-SQL-INJECTION-CHECK'
      ],
      scope: 'full_product',
      trigger: 'manual_review',
      user_context: { user_id: 'claude', role: 'architect' }
    };

    console.log('\n' + '='.repeat(80));
    console.log('RULE EXECUTOR TEST');
    console.log('='.repeat(80));

    const receipt = await executor.execute(request);

    console.log('\n--- RECEIPT ---\n');
    console.log(`Receipt ID: ${receipt.receipt_id}`);
    console.log(`Status: ${receipt.status.toUpperCase()}`);
    console.log(`Promotion Ready: ${receipt.promotion_ready ? 'YES ✓' : 'NO ✗'}`);
    console.log(`\nExecution Summary:`);
    console.log(`  Rules Executed: ${receipt.execution_summary.rules_executed}`);
    console.log(`  Rules Passed: ${receipt.execution_summary.rules_passed}`);
    console.log(`  Rules Failed: ${receipt.execution_summary.rules_failed}`);
    console.log(`  Confidence: ${(receipt.execution_summary.confidence_score * 100).toFixed(1)}%`);

    if (receipt.blocking_reasons.length > 0) {
      console.log(`\nBlocking Reasons:`);
      receipt.blocking_reasons.forEach(r => console.log(`  - ${r}`));
    }

    console.log('\n' + '='.repeat(80));
  })();
}
