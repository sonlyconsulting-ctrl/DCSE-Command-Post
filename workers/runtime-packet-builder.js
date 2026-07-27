/**
 * Runtime Packet Builder - Phase A Implementation
 *
 * Transforms task specifications into executable runtime packets.
 *
 * Responsibilities:
 * 1. Parse task definitions and requirements
 * 2. Extract and compress context (repo structure, relevant files)
 * 3. Assemble runtime packets with metadata and contracts
 * 4. Calculate deterministic hashes for verification
 * 5. Implement caching for packet reuse
 * 6. Validate complete packet structure
 *
 * Usage:
 *   const builder = new RuntimePacketBuilder();
 *   const packet = await builder.compile(taskDefinition);
 *   const verified = await builder.verify(packet);
 */

const crypto = require('crypto');
const { createHash } = require('crypto');

class RuntimePacketBuilder {
  constructor() {
    this.version = '1.0';
    this.cache = new Map(); // L1 in-memory cache
    this.compressionLevel = 1; // Default: gzip compression
  }

  /**
   * Main compilation workflow
   */
  async compile(taskDefinition) {
    console.log(`[RuntimePacketBuilder] Compiling task: ${taskDefinition.task_id}`);

    // Check cache first (L1)
    const cacheKey = this.getCacheKey(taskDefinition);
    if (this.cache.has(cacheKey)) {
      console.log(`  ✓ Cache hit (L1)`);
      return this.cache.get(cacheKey);
    }

    try {
      // 1. Extract context
      const context = await this.extractContext(taskDefinition);

      // 2. Compress context
      const compressedContext = this.compressContext(context);

      // 3. Assemble packet
      const packet = this.assemblePacket(taskDefinition, compressedContext);

      // 4. Validate packet
      const isValid = this.validatePacket(packet);
      if (!isValid) {
        throw new Error('Packet validation failed');
      }

      // 5. Calculate hashes
      packet.hashes = this.calculateHashes(packet);

      // 6. Sign packet
      packet.hashes.signature = this.signPacket(packet.hashes.packet_hash);

      // 7. Cache result (L1)
      this.cache.set(cacheKey, packet);

      console.log(`✓ Packet compiled: ${packet.packet_id}`);
      return packet;
    } catch (error) {
      console.error(`✗ Compilation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Extract relevant context for the task
   */
  async extractContext(taskDef) {
    console.log('  [1/6] Extracting context...');

    // Simulate context extraction
    // In real implementation, this would:
    // - Read repository structure
    // - Load file contents based on scope
    // - Fetch git history if needed
    // - Resolve dependencies

    const context = {
      repo_structure: {
        hash: this.hashString('repo_structure_data'),
        files_count: 234,
        size_bytes: 4567890
      },
      relevant_files: {
        architecture: {
          content_hash: this.hashString('architecture_content'),
          line_count: 450,
          last_modified: new Date().toISOString()
        },
        migrations: {
          content_hash: this.hashString('migrations_content'),
          line_count: 1474,
          last_modified: new Date().toISOString()
        },
        workers: {
          content_hash: this.hashString('workers_content'),
          line_count: 3200,
          last_modified: new Date().toISOString()
        }
      },
      raw_content: 'File content simulation...',
      original_size: 248000
    };

    return context;
  }

  /**
   * Compress context based on tier level
   */
  compressContext(context) {
    console.log('  [2/6] Compressing context...');

    // Simulate compression
    const original = context.raw_content;
    const compressed = Buffer.from(original).toString('base64');

    return {
      data: compressed,
      compression: 'gzip',
      original_size: context.original_size,
      compressed_size: Math.floor(context.original_size * 0.15),
      ratio: 0.15
    };
  }

  /**
   * Assemble complete runtime packet
   */
  assemblePacket(taskDef, compressedContext) {
    console.log('  [3/6] Assembling packet...');

    const now = new Date();
    const expiresAt = new Date(now.getTime() + 24 * 60 * 60 * 1000); // 24 hours

    const packet = {
      packet_id: this.generatePacketId(),
      task_id: taskDef.task_id,
      version: this.version,
      created_at: now.toISOString(),
      expires_at: expiresAt.toISOString(),

      metadata: {
        task_type: taskDef.task_type || 'architecture_review',
        lane: taskDef.lane || 'SYSTEM',
        priority: taskDef.priority || 'P0',
        worker_model: this.selectWorkerModel(taskDef),
        worker_mode: this.selectWorkerMode(taskDef),
        estimated_cost_usd: taskDef.estimated_cost_usd || 2.50,
        estimated_duration_seconds: taskDef.estimated_duration_seconds || 600,
        max_retries: taskDef.max_retries || 3,
        timeout_seconds: taskDef.timeout_seconds || 3600
      },

      instruction: {
        objective: taskDef.objective,
        scope: {
          files: taskDef.scope?.files || [],
          patterns: taskDef.scope?.patterns || ['*.md', '*.sql', '*.js'],
          exclude: taskDef.scope?.exclude || ['*.env', 'credentials/*']
        },
        acceptance_criteria: taskDef.acceptance_criteria || [],
        tools_allowed: this.getToolsForMode(taskDef.worker_mode),
        tools_forbidden: this.getForbiddenTools(taskDef.worker_mode),
        stopping_conditions: [
          'max_cost_exceeded',
          'max_time_exceeded',
          'max_retries_exceeded',
          'security_violation',
          'unrecoverable_error'
        ]
      },

      context: {
        repo_structure: {
          hash: 'sha256:repo_hash',
          files_count: 234,
          size_bytes: 4567890
        },
        relevant_files: {
          architecture: {
            content_hash: 'sha256:arch_hash',
            line_count: 450,
            last_modified: new Date().toISOString()
          }
        },
        compressed_context: compressedContext
      },

      security: {
        execution_mode: taskDef.worker_mode || 'blueprint',
        rls_policies: ['workers_read_eligible_messages'],
        authorized_lanes: [taskDef.lane || 'SYSTEM'],
        vault_secrets: ['model_id', 'cost_limit'],
        secret_paths: ['v7_worker.send_heartbeat', 'v7_worker.claim_next_task']
      },

      contract: {
        input_schema: {
          type: 'object',
          properties: {
            task_id: { type: 'string' },
            instruction: { type: 'string' }
          }
        },
        output_schema: {
          type: 'object',
          properties: {
            findings: { type: 'array' },
            status: { type: 'string' }
          }
        },
        receipt_schema: {
          type: 'object',
          properties: {
            receipt_id: { type: 'string' },
            status: { type: 'string' }
          }
        },
        error_schema: {
          type: 'object',
          properties: {
            error_type: { type: 'string' },
            error_message: { type: 'string' }
          }
        }
      },

      hashes: {} // Will be populated after validation
    };

    return packet;
  }

  /**
   * Validate complete packet structure
   */
  validatePacket(packet) {
    console.log('  [4/6] Validating packet...');

    const checks = [
      { name: 'packet_id format', pass: /^PKT-\d{8}-[a-f0-9]{32}$/.test(packet.packet_id) },
      { name: 'task_id present', pass: !!packet.task_id },
      { name: 'version present', pass: !!packet.version },
      { name: 'metadata complete', pass: !!packet.metadata?.task_type },
      { name: 'instruction present', pass: !!packet.instruction?.objective },
      { name: 'context present', pass: !!packet.context },
      { name: 'security configured', pass: !!packet.security?.execution_mode },
      { name: 'contract schemas defined', pass: !!packet.contract?.output_schema },
      { name: 'tools_allowed non-empty', pass: packet.instruction.tools_allowed.length > 0 },
      { name: 'acceptance_criteria non-empty', pass: packet.instruction.acceptance_criteria.length > 0 }
    ];

    for (const check of checks) {
      console.log(`    ${check.pass ? '✓' : '✗'} ${check.name}`);
      if (!check.pass) return false;
    }

    return true;
  }

  /**
   * Calculate all packet hashes
   */
  calculateHashes(packet) {
    console.log('  [5/6] Calculating hashes...');

    // Canonical JSON (sorted keys, no whitespace)
    const canonical = JSON.stringify(packet, Object.keys(packet).sort(), undefined);

    // Packet hash (full content)
    const packetHash = this.hashString(canonical);

    // Content hash (excluding hashes field)
    const contentOnly = { ...packet, hashes: undefined };
    const contentCanonical = JSON.stringify(contentOnly, Object.keys(contentOnly).sort());
    const contentHash = this.hashString(contentCanonical);

    // Instruction hash
    const instructionCanonical = JSON.stringify(packet.instruction);
    const instructionHash = this.hashString(instructionCanonical);

    return {
      packet_hash: `sha256:${packetHash}`,
      content_hash: `sha256:${contentHash}`,
      instruction_hash: `sha256:${instructionHash}`,
      signature: 'ed25519:signature_placeholder',
      verified_by: `runtime_compiler_v${this.version}`
    };
  }

  /**
   * Verify packet integrity
   */
  verify(packet) {
    console.log(`[RuntimePacketBuilder] Verifying packet: ${packet.packet_id}`);

    // Recalculate hashes
    const recalculated = this.calculateHashes(packet);

    // Compare
    const match = recalculated.packet_hash === packet.hashes.packet_hash;

    if (match) {
      console.log('✓ Packet verification passed');
    } else {
      console.error('✗ Packet integrity check failed');
    }

    return match;
  }

  /**
   * Helper: Generate unique packet ID
   */
  generatePacketId() {
    const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 8);
    const random = crypto.randomBytes(16).toString('hex');
    return `PKT-${timestamp}-${random}`;
  }

  /**
   * Helper: Generate cache key
   */
  getCacheKey(taskDef) {
    return `CACHE:${taskDef.task_id}:${taskDef.task_type}`;
  }

  /**
   * Helper: Hash string using SHA256
   */
  hashString(str) {
    return createHash('sha256').update(str).digest('hex');
  }

  /**
   * Helper: Sign packet hash
   */
  signPacket(hash) {
    // Placeholder for cryptographic signing
    return `ed25519:${crypto.randomBytes(64).toString('hex')}`;
  }

  /**
   * Helper: Select worker model based on task
   */
  selectWorkerModel(taskDef) {
    const mode = taskDef.worker_mode || 'blueprint';
    switch (mode) {
      case 'blueprint':
        return 'claude-opus-5';
      case 'implementation':
        return 'qwen-max-latest';
      case 'premium':
        return 'claude-opus-5';
      default:
        return 'claude-opus-5';
    }
  }

  /**
   * Helper: Select worker mode based on task type
   */
  selectWorkerMode(taskDef) {
    const type = taskDef.task_type || 'architecture_review';
    if (type === 'architecture_review' || type === 'validate_schema') {
      return 'blueprint';
    } else if (type === 'implement_feature' || type === 'repair_code') {
      return 'implementation';
    } else if (type === 'compile_runtime' || type === 'execute_workflow') {
      return 'premium';
    }
    return 'blueprint';
  }

  /**
   * Helper: Get allowed tools for mode
   */
  getToolsForMode(mode) {
    const tools = {
      blueprint: ['read_file', 'glob_search', 'grep_search', 'git_diff', 'test_execution'],
      implementation: ['read_file', 'edit_file', 'write_file', 'bash_run_tests', 'git_operations'],
      premium: ['read_file', 'edit_file', 'write_file', 'bash_execution', 'git_operations', 'deploy']
    };
    return tools[mode] || tools.blueprint;
  }

  /**
   * Helper: Get forbidden tools for mode
   */
  getForbiddenTools(mode) {
    const forbidden = {
      blueprint: ['edit_file', 'write_file', 'delete_file', 'bash_command', 'deploy'],
      implementation: ['delete_file', 'bash_command', 'deploy'],
      premium: []
    };
    return forbidden[mode] || [];
  }

  /**
   * Cache statistics
   */
  cacheStats() {
    return {
      cache_size: this.cache.size,
      entries: Array.from(this.cache.keys())
    };
  }
}

// Export for use in other modules
module.exports = RuntimePacketBuilder;

// Test if run directly
if (require.main === module) {
  (async () => {
    const builder = new RuntimePacketBuilder();

    // Test task definition
    const taskDef = {
      task_id: 'DCSE-V7-COMP-001',
      task_type: 'architecture_review',
      lane: 'SYSTEM',
      priority: 'P0',
      worker_mode: 'blueprint',
      objective: 'Review DCSE V7 Agent Worker Communication System',
      scope: {
        files: ['02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md'],
        patterns: ['*.sql', '*.md'],
        exclude: ['*.env', 'credentials/*']
      },
      acceptance_criteria: [
        'Architecture complete',
        'Migrations pass',
        'No SQL errors'
      ],
      estimated_cost_usd: 2.50,
      estimated_duration_seconds: 600
    };

    console.log('\n' + '='.repeat(80));
    console.log('RUNTIME PACKET BUILDER TEST');
    console.log('='.repeat(80));

    try {
      const packet = await builder.compile(taskDef);
      console.log('\n✓ Packet compilation successful\n');
      console.log(`  Packet ID: ${packet.packet_id}`);
      console.log(`  Task ID: ${packet.task_id}`);
      console.log(`  Worker: ${packet.metadata.worker_model} (${packet.metadata.worker_mode})`);
      console.log(`  Cost: $${packet.metadata.estimated_cost_usd}`);
      console.log(`  Compression: ${packet.context.compressed_context.ratio} ratio`);
      console.log(`  Hashes: ${Object.keys(packet.hashes).join(', ')}`);

      // Verify
      const verified = builder.verify(packet);
      console.log(`\n  Verification: ${verified ? '✓ PASSED' : '✗ FAILED'}`);

      console.log('\n' + '='.repeat(80));
    } catch (error) {
      console.error(`✗ Test failed: ${error.message}`);
      process.exit(1);
    }
  })();
}
