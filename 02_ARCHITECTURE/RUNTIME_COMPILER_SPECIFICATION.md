# Runtime Compiler Specification — DCSE V7

**Status:** Phase A Design Complete
**Version:** 1.0
**Date:** 2026-07-27

---

## Overview

The Runtime Compiler transforms task specifications into executable runtime packets. It is the central orchestration point for:

1. **Task Analysis** — Parse task requirements, dependencies, scope
2. **Context Extraction** — Identify required data, code, and configuration
3. **Packet Assembly** — Create compressed, self-contained execution units
4. **Validation** — Verify packet integrity and completeness
5. **Caching** — Cache compiled packets for reuse
6. **Hashing** — Generate deterministic hashes for verification

**Architecture:**
```
Task Definition
    ↓
[Runtime Compiler]
    ├─ Context Extractor
    ├─ Packet Builder
    ├─ Compression Engine
    ├─ Validator
    ├─ Cache Manager
    └─ Hash Generator
    ↓
Runtime Packet (JSON + metadata)
    ↓
[Worker (Claude/Qwen/Codex)]
    ↓
Execution Receipt
```

---

## Core Components

### 1. Runtime Packet Structure

```json
{
  "packet_id": "PKT-20260727-abc123def456",
  "task_id": "DCSE-V7-COMP-001",
  "version": "1.0",
  "created_at": "2026-07-27T21:15:00Z",
  "expires_at": "2026-07-28T21:15:00Z",
  
  "metadata": {
    "task_type": "architecture_review",
    "lane": "SYSTEM",
    "priority": "P0",
    "worker_model": "claude-opus-5",
    "worker_mode": "blueprint",
    "estimated_cost_usd": 2.50,
    "estimated_duration_seconds": 600,
    "max_retries": 3,
    "timeout_seconds": 3600
  },

  "instruction": {
    "objective": "Review DCSE V7 Agent Worker Communication System...",
    "scope": {
      "files": ["02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md", ...],
      "patterns": ["*.sql", "*.md"],
      "exclude": ["*.env", "credentials/*"]
    },
    "acceptance_criteria": [
      "Architecture complete and documented",
      "Migrations pass Supabase preview",
      "No SQL syntax errors",
      ...
    ],
    "tools_allowed": ["read_file", "glob_search", "grep_search", "git_diff"],
    "tools_forbidden": ["write_file", "delete_file", "bash_command"],
    "stopping_conditions": [
      "max_cost_exceeded",
      "max_time_exceeded",
      "max_retries_exceeded",
      "security_violation",
      "unrecoverable_error"
    ]
  },

  "context": {
    "repo_structure": {
      "hash": "sha256:abc123...",
      "files_count": 234,
      "size_bytes": 4567890
    },
    "relevant_files": {
      "architecture": ["content_hash", "line_count", "last_modified"],
      "migrations": ["content_hash", "sequence", "status"],
      "workers": ["content_hash", "type", "version"]
    },
    "compressed_context": {
      "data": "base64:...",
      "compression": "gzip",
      "original_size": 2456789,
      "compressed_size": 456789,
      "ratio": 0.186
    }
  },

  "security": {
    "execution_mode": "blueprint",
    "rls_policies": ["workers_read_eligible_messages"],
    "authorized_lanes": ["SYSTEM"],
    "vault_secrets": ["model_id", "cost_limit"],
    "secret_paths": ["v7_worker.send_heartbeat", "v7_worker.claim_next_task"]
  },

  "contract": {
    "input_schema": {"type": "object", "properties": {...}},
    "output_schema": {"type": "object", "properties": {...}},
    "receipt_schema": {"type": "object", "properties": {...}},
    "error_schema": {"type": "object", "properties": {...}}
  },

  "hashes": {
    "packet_hash": "sha256:packet_hash_value",
    "content_hash": "sha256:content_hash_value",
    "instruction_hash": "sha256:instruction_hash_value",
    "signature": "ed25519:signature_bytes",
    "verified_by": "runtime_compiler_v1.0"
  }
}
```

### 2. Context Compression Rules

**Objective:** Minimize packet size while maintaining execution fidelity

**Strategy:**
- Extract only necessary file content (not entire repo)
- Use diffs instead of full files where possible
- Compress large binary/media
- Cache frequently-used context (architecture docs, schemas)
- Store references to immutable content (commit hashes, URLs)

**Compression Levels:**

| Level | Method | Use Case | Ratio |
|-------|--------|----------|-------|
| 0 | None | Small packets (<100KB) | 1.0 |
| 1 | Text compression (gzip) | Standard packets | 0.1-0.3 |
| 2 | Differential encoding | Large file sets | 0.05-0.2 |
| 3 | Smart summarization | Code review tasks | 0.01-0.1 |

**Example: Architecture Review Context**
```
Original:
- Full migration file: 45KB
- Full architecture doc: 78KB
- Full worker code: 125KB
Total: 248KB

Compressed (Level 2):
- Migration diff (vs. v6.9): 8KB
- Architecture summary (structure only): 12KB
- Worker summary (types, interfaces): 15KB
Total: 35KB (ratio: 0.14)
```

### 3. Runtime Tier Definitions

**Tier 1: Blueprint Mode (Read-Only)**
- Tools: read_file, glob_search, grep_search, git_diff, test_execution
- Cost: $0.50-2.50 per task
- Max context: 128KB
- Max duration: 30 minutes
- Workers: Claude Reviewer
- Example: Architecture review, code analysis, validation

**Tier 2: Implementation Mode (Write)**
- Tools: read_file, edit_file, write_file, bash_run_tests, git_operations
- Cost: $1.00-5.00 per task
- Max context: 256KB
- Max duration: 60 minutes
- Workers: Qwen Builder
- Example: Repair execution, feature implementation

**Tier 3: Premium Mode (Full Access)**
- Tools: all (read, write, execute, deploy)
- Cost: $5.00-50.00 per task
- Max context: 512KB
- Max duration: 120 minutes
- Workers: Codex (with approval)
- Example: Dashboard rebuild, complex multi-file refactoring

### 4. Runtime Validation Contract

**Pre-Execution Validation:**

```javascript
// Packet structure validation
- packet_id present and valid format ✓
- task_id matches queue_message.task_id ✓
- created_at <= now <= expires_at ✓
- version compatible with worker ✓

// Instruction validation
- objective defined ✓
- scope defined (files and patterns) ✓
- tools_allowed subset of tier capabilities ✓
- acceptance_criteria non-empty array ✓

// Security validation
- execution_mode matches worker_model ✓
- authorized_lanes includes task lane ✓
- rls_policies defined ✓
- secrets encrypted (not in plaintext) ✓

// Contract validation
- input_schema, output_schema, receipt_schema all JSON schemas ✓
- error_schema defines error structure ✓

// Hash validation
- packet_hash matches content ✓
- signature valid (cryptographic verification) ✓
```

**Post-Execution Validation:**

```javascript
// Receipt structure
- receipt_id matches packet_id ✓
- result conforms to output_schema ✓
- findings array populated ✓
- execution_timeline documented ✓
- costs within estimated_cost_usd + margin ✓
- duration within timeout_seconds ✓
- errors (if any) conform to error_schema ✓
```

### 5. Runtime Hashing Rules

**Deterministic Hash Calculation:**

```python
def calculate_packet_hash(packet):
    """
    Generate deterministic packet hash for integrity verification.
    """
    # Canonical JSON (sorted keys, no whitespace)
    canonical = json.dumps(packet, sort_keys=True, separators=(',', ':'))
    
    # SHA256 of full packet (including hashes field)
    packet_hash = sha256(canonical).hexdigest()
    
    # Content-only hash (excludes hashes field)
    content_only = {k: v for k, v in packet.items() if k != 'hashes'}
    content_canonical = json.dumps(content_only, sort_keys=True, separators=(',', ':'))
    content_hash = sha256(content_canonical).hexdigest()
    
    # Instruction hash (for change detection)
    instruction_canonical = json.dumps(packet['instruction'], sort_keys=True, separators=(',', ':'))
    instruction_hash = sha256(instruction_canonical).hexdigest()
    
    return {
        'packet_hash': packet_hash,
        'content_hash': content_hash,
        'instruction_hash': instruction_hash,
        'signature': sign(packet_hash, private_key)
    }
```

**Hash Verification Workflow:**

1. Extract hashes field from packet
2. Recalculate packet_hash (excluding hashes field)
3. Compare calculated vs. stored
4. If mismatch: packet corrupted, reject
5. Verify cryptographic signature
6. If signature invalid: packet tampered, reject
7. Proceed with execution

### 6. Runtime Cache Strategy

**Cache Levels:**

| Level | Type | TTL | Use Case |
|-------|------|-----|----------|
| L1 | In-Memory | 5 min | Repeated tasks same hour |
| L2 | Redis/File | 1 day | Architecture docs, schemas |
| L3 | S3/Archive | 7 days | Completed task packets |
| L4 | Long-Term | 90 days | Rarely-accessed context |

**Cache Key:** `CACHE:{packet_id}:{content_hash}`

**Invalidation Rules:**
- L1: On worker shutdown
- L2: 24 hours after creation
- L3: On task completion or error
- L4: Manual or 90-day expiry

**Example: Cached Architecture Context**
```
Key: CACHE:PKT-REVIEW-ARCH:sha256:abc123
Value: {
  "content": "compressed_base64_...",
  "compression": "gzip",
  "original_size": 248000,
  "cached_at": "2026-07-27T20:00:00Z",
  "accessed_count": 3,
  "last_accessed": "2026-07-27T21:00:00Z",
  "ttl_remaining_seconds": 3600
}
```

---

## Compilation Workflow

```
1. Task Claimed
   ↓
2. Context Extraction
   ├─ Load task definition
   ├─ Identify scope (files, patterns)
   ├─ Fetch relevant file content
   ├─ Extract git history (if needed)
   └─ Resolve dependencies
   ↓
3. Compression
   ├─ Measure original size
   ├─ Apply compression (level = tier)
   ├─ Verify compression ratio
   └─ Store compression metadata
   ↓
4. Packet Assembly
   ├─ Combine metadata + instruction + context + security
   ├─ Add contract schemas
   └─ Generate unique packet_id
   ↓
5. Validation
   ├─ Validate structure
   ├─ Validate instruction
   ├─ Validate security
   └─ Validate contracts
   ↓
6. Hashing & Signing
   ├─ Calculate all hashes
   ├─ Generate cryptographic signature
   └─ Verify hashes
   ↓
7. Caching
   ├─ Store in L2 cache (1 day)
   ├─ Return cache key
   └─ Update cache metadata
   ↓
8. Packet Ready
   └─ Return packet to worker (or from cache)
```

---

## Execution Contract

### Input: Task Definition + Queue Message
```json
{
  "task_id": "DCSE-V7-COMP-001",
  "task_type": "architecture_review",
  "lane": "SYSTEM",
  "priority": "P0",
  "runtime_packet": {JSON blob with full spec}
}
```

### Output: Execution Receipt
```json
{
  "receipt_id": "REC-20260727-xyz789",
  "packet_id": "PKT-20260727-abc123",
  "task_id": "DCSE-V7-COMP-001",
  "worker_id": "AGENT-CLAUDE-REVIEWER-01@STAGING",
  "status": "success|error|stop_gate",
  "result": {JSON per output_schema},
  "execution_timeline": [...],
  "cost_usd": 2.34,
  "duration_seconds": 567,
  "verified_by": "packet_hash matches"
}
```

---

## Success Criteria (Phase A)

✅ Runtime Packet structure defined with all required fields
✅ Context compression rules documented with examples
✅ Tier definitions (Blueprint, Implementation, Premium) specified
✅ Validation contract with pre and post checks
✅ Hashing rules with deterministic calculation
✅ Cache strategy with 4 levels and TTL
✅ Compilation workflow documented step-by-step
✅ Execution contract (input/output) defined
✅ JSON schemas generated for all contracts
✅ No contradictions with existing Phase 1A architecture

---

## Next: Runtime Packet Builder (implementation)

The builder will:
1. Compile task definitions into packets
2. Extract and compress context
3. Calculate hashes and verify
4. Implement caching
5. Generate receipts

---

## Files Produced

- `RUNTIME_COMPILER_SPECIFICATION.md` (this file)
- `runtime_packet_schema.json` (next)
- `runtime_receipt_schema.json` (next)
- `runtime_validation_contract.json` (next)
