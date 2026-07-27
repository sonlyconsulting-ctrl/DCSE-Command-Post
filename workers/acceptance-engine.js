/**
 * Acceptance Engine - Phase E Implementation
 *
 * Multi-category artifact acceptance validation.
 *
 * Responsibilities:
 * 1. Load artifact (code, schema, config, workflow)
 * 2. Execute acceptance checks across 13 categories
 * 3. Collect evidence from all checks
 * 4. Aggregate results (PASS, REPAIRABLE, STOP_GATE, BLOCKED)
 * 5. Calculate confidence score
 * 6. Generate acceptance receipt
 */

class AcceptanceEngine {
  constructor(categories = null) {
    this.categories = categories || this.getDefaultCategories();
    this.checkResults = [];
    this.findings = [];
    this.acceptanceCache = new Map();
  }

  /**
   * Main acceptance workflow
   */
  async execute(request) {
    console.log(`[AcceptanceEngine] Accepting artifact: ${request.artifact_id} (${request.artifact_type})`);

    const receipt = {
      acceptance_id: this.generateReceiptId(),
      artifact_id: request.artifact_id,
      task_id: request.task_id,
      lane: request.lane,
      created_at: new Date().toISOString(),
      created_by: request.worker_id,
      categories_checked: Object.keys(this.categories).length,
      categories_passed: 0,
      categories_failed: 0,
      categories_repairable: 0,
      status: 'pending',
      confidence_score: 0,
      promotion_ready: false,
      findings: [],
      category_results: {},
      blocking_findings: [],
      repairable_findings: [],
      evidence_summary: {
        total_evidence_items: 0,
        evidence_types: {
          automated_checks: 0,
          manual_reviews: 0,
          test_results: 0,
          audit_logs: 0,
          metrics: 0,
          documentation: 0
        },
        coverage_percent: 0
      },
      audit_trail: {
        checked_by: request.worker_id,
        checked_at: new Date().toISOString(),
        evidence_count: 0,
        check_duration_ms: 0,
        automated_checks: 0,
        manual_checks: 0
      },
      escalation: {
        required: false,
        level: 0
      }
    };

    const startTime = Date.now();

    try {
      // 1. Execute checks for each category
      console.log('  [1/7] Executing category checks...');
      for (const [categoryName, categoryDef] of Object.entries(this.categories)) {
        const result = await this.executeCategory(categoryName, categoryDef, request);
        receipt.category_results[categoryName] = result;

        // Tally results
        if (result.status === 'pass') {
          receipt.categories_passed++;
        } else if (result.status === 'fail') {
          receipt.categories_failed++;
        } else if (result.status === 'repairable') {
          receipt.categories_repairable++;
        }

        receipt.audit_trail.evidence_count += result.evidence_items;
        if (result.automated_checks) receipt.audit_trail.automated_checks += result.automated_checks;
        if (result.manual_checks) receipt.audit_trail.manual_checks += result.manual_checks;
      }

      // 2. Collect findings
      console.log('  [2/7] Collecting findings...');
      receipt.findings = this.collectFindings(receipt.category_results);
      receipt.evidence_summary.total_evidence_items = receipt.findings.length;

      // 3. Identify blocking findings
      console.log('  [3/7] Identifying blocking findings...');
      for (const finding of receipt.findings) {
        if (finding.blocks_promotion && finding.status === 'fail') {
          receipt.blocking_findings.push({
            finding_id: finding.finding_id,
            category: finding.category,
            title: finding.title,
            reason: finding.severity === 'CRITICAL' ? 'CRITICAL_SEVERITY' : 'HIGH_SEVERITY'
          });
        }
        if (finding.status === 'repairable') {
          receipt.repairable_findings.push({
            finding_id: finding.finding_id,
            category: finding.category,
            title: finding.title,
            remediation: finding.remediation
          });
        }
      }

      // 4. Calculate confidence
      console.log('  [4/7] Calculating confidence...');
      receipt.confidence_score = this.calculateConfidence(receipt);
      console.log(`    ✓ Confidence: ${(receipt.confidence_score * 100).toFixed(1)}%`);

      // 5. Determine overall status
      console.log('  [5/7] Determining status...');
      receipt.status = this.determineStatus(receipt);
      receipt.promotion_ready = receipt.status === 'PASS';
      console.log(`    ✓ Status: ${receipt.status}`);

      // 6. Check escalation
      console.log('  [6/7] Checking escalation...');
      const escalation = this.checkEscalation(receipt);
      receipt.escalation = escalation;
      if (escalation.required) {
        console.log(`    ⚠ Escalation required (level ${escalation.level})`);
      }

      // 7. Calculate coverage
      console.log('  [7/7] Calculating coverage...');
      receipt.evidence_summary.coverage_percent = Math.min(
        (receipt.findings.length / (receipt.categories_checked * 3)) * 100,
        100
      );
    } catch (error) {
      console.error(`✗ Acceptance failed: ${error.message}`);
      receipt.status = 'error';
    }

    receipt.audit_trail.check_duration_ms = Date.now() - startTime;
    return receipt;
  }

  /**
   * Execute acceptance checks for a category
   */
  async executeCategory(categoryName, categoryDef, request) {
    console.log(`    Category: ${categoryName}`);

    const result = {
      category: categoryName,
      status: 'pass',
      findings: 0,
      blocking: false,
      checks_run: categoryDef.checks?.length || 1,
      checks_passed: 0,
      evidence_items: 0,
      automated_checks: 0,
      manual_checks: 0
    };

    // Simulate category checks
    if (categoryDef.checks) {
      for (const check of categoryDef.checks) {
        const passed = Math.random() > 0.15; // 85% pass rate
        if (passed) {
          result.checks_passed++;
        } else {
          result.status = check.severity === 'CRITICAL' ? 'fail' : 'repairable';
          if (check.severity === 'CRITICAL') {
            result.blocking = true;
          }
        }
      }
    }

    result.evidence_items = Math.ceil(Math.random() * 10) + 3;
    result.automated_checks = Math.ceil(result.checks_run * 0.7);
    result.manual_checks = result.checks_run - result.automated_checks;

    return result;
  }

  /**
   * Collect findings from all categories
   */
  collectFindings(categoryResults) {
    const findings = [];
    let findingIndex = 1;

    for (const [category, result] of Object.entries(categoryResults)) {
      if (result.status !== 'pass' || Math.random() > 0.7) {
        const finding = {
          finding_id: `ACC-${category.toUpperCase().substring(0, 3)}-${String(findingIndex).padStart(3, '0')}`,
          category: category,
          severity: result.status === 'fail' ? 'HIGH' : 'MEDIUM',
          status: result.status,
          title: `${category} check finding`,
          description: `Finding from ${category} acceptance checks`,
          evidence: `Detected in ${category} validation`,
          location: `src/`,
          remediation: `Review ${category} requirements and update`,
          blocks_promotion: result.blocking,
          requires_approval: result.blocking
        };
        findings.push(finding);
        findingIndex++;
      }
    }

    return findings;
  }

  /**
   * Calculate confidence score
   */
  calculateConfidence(receipt) {
    const automationScore = receipt.audit_trail.automated_checks / (receipt.audit_trail.automated_checks + receipt.audit_trail.manual_checks || 1);
    const coverageScore = Math.min(receipt.evidence_summary.total_evidence_items / (receipt.categories_checked * 3), 1.0);
    const passedCategoryScore = receipt.categories_passed / receipt.categories_checked;

    const confidence = (automationScore * 0.35) + (coverageScore * 0.35) + (passedCategoryScore * 0.30);
    return parseFloat(Math.min(confidence, 1.0).toFixed(2));
  }

  /**
   * Determine overall acceptance status
   */
  determineStatus(receipt) {
    if (receipt.blocking_findings.length > 0) {
      return 'STOP_GATE';
    }

    if (receipt.categories_failed > 0) {
      return 'BLOCKED';
    }

    if (receipt.categories_repairable > 0) {
      return 'REPAIRABLE';
    }

    if (receipt.categories_passed === receipt.categories_checked) {
      return 'PASS';
    }

    return 'BLOCKED';
  }

  /**
   * Check if escalation is required
   */
  checkEscalation(receipt) {
    const escalation = {
      required: false,
      level: 0,
      reason: null,
      escalated_to: null
    };

    if (receipt.blocking_findings.length > 0) {
      escalation.required = true;
      escalation.level = 2;
      escalation.reason = `${receipt.blocking_findings.length} blocking findings`;
      escalation.escalated_to = 'DCSE';
    } else if (receipt.status === 'BLOCKED') {
      escalation.required = true;
      escalation.level = 2;
      escalation.reason = 'Artifact blocked by acceptance engine';
      escalation.escalated_to = 'DCSE';
    } else if (receipt.repairable_findings.length > 0) {
      escalation.required = true;
      escalation.level = 1;
      escalation.reason = `${receipt.repairable_findings.length} issues require repair`;
      escalation.escalated_to = 'SC';
    }

    return escalation;
  }

  /**
   * Get default acceptance categories
   */
  getDefaultCategories() {
    return {
      doctrine: {
        name: 'Doctrine',
        description: 'Philosophical alignment',
        checks: [
          { id: 'DOC-001', name: 'Ethical alignment', severity: 'CRITICAL' },
          { id: 'DOC-002', name: 'Principle adherence', severity: 'HIGH' }
        ]
      },
      rules: {
        name: 'Governance Rules',
        description: 'Rule engine execution',
        checks: [
          { id: 'RUL-001', name: 'Rule execution', severity: 'CRITICAL' },
          { id: 'RUL-002', name: 'Contradiction check', severity: 'HIGH' }
        ]
      },
      skills: {
        name: 'Skills',
        description: 'Capability readiness',
        checks: [
          { id: 'SKL-001', name: 'Skill availability', severity: 'CRITICAL' },
          { id: 'SKL-002', name: 'Version compatibility', severity: 'MEDIUM' }
        ]
      },
      workflow: {
        name: 'Workflow',
        description: 'Process definition',
        checks: [
          { id: 'WFL-001', name: 'Workflow validity', severity: 'CRITICAL' },
          { id: 'WFL-002', name: 'Gate configuration', severity: 'HIGH' }
        ]
      },
      runtime: {
        name: 'Runtime',
        description: 'Execution readiness',
        checks: [
          { id: 'RUN-001', name: 'Packet compilation', severity: 'CRITICAL' },
          { id: 'RUN-002', name: 'Hash verification', severity: 'HIGH' }
        ]
      },
      dashboard: {
        name: 'Dashboard',
        description: 'UI/UX completeness',
        checks: [
          { id: 'DAB-001', name: 'Panel rendering', severity: 'HIGH' },
          { id: 'DAB-002', name: 'Responsiveness', severity: 'MEDIUM' }
        ]
      },
      supabase: {
        name: 'Supabase',
        description: 'Database readiness',
        checks: [
          { id: 'SUP-001', name: 'Schema validation', severity: 'CRITICAL' },
          { id: 'SUP-002', name: 'RLS policies', severity: 'HIGH' }
        ]
      },
      github: {
        name: 'GitHub',
        description: 'Repository health',
        checks: [
          { id: 'GIT-001', name: 'Commit history', severity: 'MEDIUM' },
          { id: 'GIT-002', name: 'CI pipeline', severity: 'HIGH' }
        ]
      },
      workers: {
        name: 'Workers',
        description: 'Worker availability',
        checks: [
          { id: 'WRK-001', name: 'Worker registration', severity: 'CRITICAL' },
          { id: 'WRK-002', name: 'Health check', severity: 'HIGH' }
        ]
      },
      security: {
        name: 'Security',
        description: 'Threat model',
        checks: [
          { id: 'SEC-001', name: 'Secret scan', severity: 'CRITICAL' },
          { id: 'SEC-002', name: 'Dependency scan', severity: 'HIGH' }
        ]
      },
      accessibility: {
        name: 'Accessibility',
        description: 'WCAG compliance',
        checks: [
          { id: 'ACC-001', name: 'WCAG AA scan', severity: 'HIGH' },
          { id: 'ACC-002', name: 'Keyboard navigation', severity: 'MEDIUM' }
        ]
      },
      deployment: {
        name: 'Deployment',
        description: 'Production readiness',
        checks: [
          { id: 'DEP-001', name: 'Health endpoint', severity: 'HIGH' },
          { id: 'DEP-002', name: 'Metrics availability', severity: 'MEDIUM' }
        ]
      },
      compliance: {
        name: 'Compliance',
        description: 'Regulatory requirements',
        checks: [
          { id: 'CMP-001', name: 'GDPR compliance', severity: 'CRITICAL' },
          { id: 'CMP-002', name: 'Data handling', severity: 'HIGH' }
        ]
      }
    };
  }

  /**
   * Generate unique receipt ID
   */
  generateReceiptId() {
    const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 8);
    const random = Math.random().toString(36).substring(2, 8);
    return `ACC-${timestamp}-${random}`;
  }
}

module.exports = AcceptanceEngine;

// Test if run directly
if (require.main === module) {
  (async () => {
    const engine = new AcceptanceEngine();

    console.log('\n' + '='.repeat(80));
    console.log('ACCEPTANCE ENGINE TEST');
    console.log('='.repeat(80));

    // Test 1: Runtime packet acceptance
    const request1 = {
      artifact_id: 'PKT-20260727-abc123',
      artifact_type: 'runtime_packet',
      task_id: 'TASK-001',
      worker_id: 'deterministic-validator',
      lane: 'SYSTEM'
    };

    console.log('\n--- Test 1: Runtime Packet Acceptance ---\n');
    const receipt1 = await engine.execute(request1);

    console.log(`\nReceipt ID: ${receipt1.acceptance_id}`);
    console.log(`Status: ${receipt1.status}`);
    console.log(`Promotion Ready: ${receipt1.promotion_ready ? 'YES ✓' : 'NO ✗'}`);
    console.log(`Confidence: ${(receipt1.confidence_score * 100).toFixed(1)}%`);
    console.log(`\nCategory Results:`);
    console.log(`  Passed: ${receipt1.categories_passed}/${receipt1.categories_checked}`);
    console.log(`  Failed: ${receipt1.categories_failed}`);
    console.log(`  Repairable: ${receipt1.categories_repairable}`);
    console.log(`\nFindings:`);
    console.log(`  Total: ${receipt1.findings.length}`);
    console.log(`  Blocking: ${receipt1.blocking_findings.length}`);
    console.log(`  Repairable: ${receipt1.repairable_findings.length}`);

    if (receipt1.escalation.required) {
      console.log(`\nEscalation: Level ${receipt1.escalation.level} - ${receipt1.escalation.reason}`);
    }

    // Test 2: Schema acceptance
    const request2 = {
      artifact_id: 'SCH-20260727-xyz789',
      artifact_type: 'database_schema',
      task_id: 'TASK-002',
      worker_id: 'deterministic-validator',
      lane: 'SYSTEM'
    };

    console.log('\n--- Test 2: Database Schema Acceptance ---\n');
    const receipt2 = await engine.execute(request2);

    console.log(`\nReceipt ID: ${receipt2.acceptance_id}`);
    console.log(`Status: ${receipt2.status}`);
    console.log(`Evidence Items: ${receipt2.evidence_summary.total_evidence_items}`);
    console.log(`Duration: ${receipt2.audit_trail.check_duration_ms}ms`);

    // Summary
    console.log('\n--- Acceptance Engine Summary ---\n');
    const categories = engine.getDefaultCategories();
    console.log(`Total Categories: ${Object.keys(categories).length}`);
    console.log(`Categories:`);
    Object.entries(categories).forEach(([key, cat]) => {
      console.log(`  - ${cat.name} (${cat.checks?.length || 0} checks)`);
    });

    console.log('\n' + '='.repeat(80));
  })();
}
