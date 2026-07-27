#!/usr/bin/env node

/**
 * DCSE V7 Claude Reviewer Worker
 *
 * Blueprint Mode (Read-Only) autonomous agent for:
 * - Architecture review
 * - Code inspection
 * - Schema validation
 * - Security analysis
 * - Acceptance testing
 *
 * Approved tools:
 * - File reading (Read)
 * - Glob search (Glob)
 * - Grep search (Grep)
 * - Git diff inspection
 * - Non-modifying test execution
 * - Supabase RPC for queue operations
 *
 * First assignment: DCSE V7 COMP 001 - Review PR #14
 */

const Anthropic = require("@anthropic-ai/sdk");
const { createClient } = require("@supabase/supabase-js");
const fs = require("fs");
const path = require("path");
const YAML = require("yaml");
const { spawn } = require("child_process");

const AGENT_ID = "AGENT-CLAUDE-REVIEWER-01@STAGING";
const REPO_ROOT = path.resolve(__dirname, "..");

// Error classification
const ErrorClass = {
  TRANSIENT: "transient",
  KNOWN_REPAIRABLE: "known_repairable",
  AUTHORIZATION: "authorization",
  CONTEXT_MISSING: "context_missing",
  SECURITY_STOPGATE: "security_stopgate",
  COST_LIMIT: "cost_limit",
  UNKNOWN: "unknown"
};

// Task lifecycle states
const TaskState = {
  CLAIMED: "claimed",
  EXECUTING: "executing",
  AWAITING_VALIDATION: "awaiting_validation",
  REVIEW_READY: "review_ready",
  ARCHIVED: "archived"
};

/**
 * Load model configuration from registry
 */
function loadModelRegistry() {
  const registryPath = path.join(REPO_ROOT, "02_ARCHITECTURE", "MODEL_REGISTRY.yaml");
  const yaml = fs.readFileSync(registryPath, "utf8");
  return YAML.parse(yaml);
}

/**
 * Get approved model ID (never hardcode)
 */
function getApprovedModel() {
  const registry = loadModelRegistry();
  const config = registry.models.claude_architecture_reviewer;

  // Verify environment hasn't cached stale model
  const envModel = process.env.CLAUDE_REVIEWER_MODEL;
  if (envModel && envModel !== config.approved_model_id) {
    console.warn(
      `[${AGENT_ID}] Environment model ${envModel} differs from registry ${config.approved_model_id}`
    );
  }

  return config.approved_model_id;
}

/**
 * Initialize Supabase via Edge Function RPC (never direct service-role)
 */
async function initSupabaseWorkerClient() {
  const supabaseUrl = process.env.SUPABASE_URL;
  const workerToken = process.env.WORKER_ACCESS_TOKEN; // From Edge Function, scoped auth

  if (!supabaseUrl || !workerToken) {
    throw new Error("SUPABASE_URL and WORKER_ACCESS_TOKEN required (service-role forbidden)");
  }

  // Use anon key or bearer token from Edge Function, never service-role
  return createClient(supabaseUrl, workerToken, {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  });
}

/**
 * Claim next eligible task from pgmq queue
 */
async function claimNextTask(supabase) {
  try {
    const { data, error } = await supabase.rpc("claim_next_task", {
      p_agent_id: AGENT_ID
    });

    if (error) {
      console.error(`[${AGENT_ID}] RPC error claiming task:`, error);
      return null;
    }

    if (data) {
      console.log(`[${AGENT_ID}] Claimed task:`, data.task_id);
      return data;
    }

    return null;
  } catch (err) {
    console.error(`[${AGENT_ID}] Exception claiming task:`, err);
    return null;
  }
}

/**
 * Renew heartbeat and task lease (called every 5 minutes during execution)
 */
async function renewHeartbeat(supabase, taskId, metrics = {}) {
  try {
    const { data, error } = await supabase.rpc("send_heartbeat", {
      p_agent_id: AGENT_ID,
      p_status: "running",
      p_current_task_id: taskId,
      p_metrics: JSON.stringify(metrics)
    });

    if (error) {
      return { success: false, error, class: ErrorClass.TRANSIENT };
    }

    console.log(`[${AGENT_ID}] Heartbeat renewed for task ${taskId}`);
    return { success: true, data };
  } catch (err) {
    return { success: false, error: err, class: ErrorClass.TRANSIENT };
  }
}

/**
 * Execute tool with Blueprint Mode constraints
 * Only approved read-only and inspection tools
 */
async function executeBlueprintTool(toolName, toolInput) {
  const approvedTools = {
    read_file: (input) => {
      // Restrict to repo paths only
      const filePath = path.resolve(REPO_ROOT, input.path);
      if (!filePath.startsWith(REPO_ROOT)) {
        throw new Error(`Path traversal rejected: ${input.path}`);
      }
      return fs.readFileSync(filePath, "utf8");
    },

    glob_search: async (input) => {
      return new Promise((resolve, reject) => {
        const glob = require("glob");
        glob(input.pattern, { cwd: REPO_ROOT }, (err, files) => {
          if (err) reject(err);
          else resolve(files);
        });
      });
    },

    grep_search: async (input) => {
      return new Promise((resolve, reject) => {
        const grep = spawn("grep", [
          "-r",
          "-n",
          input.pattern,
          input.path || REPO_ROOT
        ]);
        let output = "";
        grep.stdout.on("data", (data) => { output += data; });
        grep.on("close", (code) => resolve(output));
      });
    },

    git_diff: async (input) => {
      return new Promise((resolve, reject) => {
        const git = spawn("git", [
          "diff",
          "--no-index",
          input.from || "HEAD",
          input.to || "."
        ], { cwd: REPO_ROOT });
        let output = "";
        git.stdout.on("data", (data) => { output += data; });
        git.on("close", (code) => resolve(output));
      });
    },

    test_execution: async (input) => {
      // Only non-modifying tests (validation, linting, type-check)
      const allowedTests = ["test", "lint", "type-check", "validate"];
      if (!allowedTests.includes(input.test_name)) {
        throw new Error(`Test '${input.test_name}' not in allowlist: ${allowedTests.join(", ")}`);
      }

      return new Promise((resolve, reject) => {
        const proc = spawn("npm", ["run", input.test_name], { cwd: REPO_ROOT });
        let output = "";
        proc.stdout.on("data", (data) => { output += data; });
        proc.on("close", (code) => resolve(output));
      });
    }
  };

  if (!approvedTools[toolName]) {
    throw new Error(`Tool '${toolName}' not in Blueprint Mode allowlist`);
  }

  return approvedTools[toolName](toolInput);
}

/**
 * Classify error for retry logic
 */
function classifyError(error) {
  const msg = error.message || String(error);

  if (msg.includes("timeout") || msg.includes("ECONNREFUSED")) {
    return ErrorClass.TRANSIENT;
  }
  if (msg.includes("ENOENT") || msg.includes("not found")) {
    return ErrorClass.CONTEXT_MISSING;
  }
  if (msg.includes("AUTHORIZATION") || msg.includes("permission")) {
    return ErrorClass.AUTHORIZATION;
  }
  if (msg.includes("SECURITY") || msg.includes("stopgate")) {
    return ErrorClass.SECURITY_STOPGATE;
  }
  if (msg.includes("cost") || msg.includes("limit")) {
    return ErrorClass.COST_LIMIT;
  }

  return ErrorClass.UNKNOWN;
}

/**
 * Submit task result and findings
 * Do NOT release claim immediately - mark for validation
 */
async function submitResult(supabase, taskId, findings) {
  try {
    const { data, error } = await supabase
      .from("result_submission")
      .insert({
        task_id: taskId,
        agent_id: AGENT_ID,
        result_data: findings,
        submission_status: "pending_validation",
        submitted_at: new Date().toISOString()
      });

    if (error) {
      return { success: false, error, class: ErrorClass.KNOWN_REPAIRABLE };
    }

    console.log(`[${AGENT_ID}] Result submitted for ${taskId}`);
    return { success: true, data };
  } catch (err) {
    return { success: false, error: err, class: ErrorClass.UNKNOWN };
  }
}

/**
 * Create repair task for Qwen (based on Blueprint findings)
 * Only authorized via v7_worker schema
 */
async function createRepairTask(supabase, findingId, repairDescription, lane) {
  try {
    const { data, error } = await supabase.rpc("create_repair_task", {
      p_finding_id: findingId,
      p_agent_id: AGENT_ID,
      p_description: repairDescription,
      p_lane: lane || "SC", // default to SC lane
      p_task_type: "repair"
    });

    if (error) {
      return { success: false, error };
    }

    console.log(`[${AGENT_ID}] Repair task created: ${data.task_id}`);
    return { success: true, data };
  } catch (err) {
    return { success: false, error: err };
  }
}

/**
 * Main execution loop with heartbeat renewal
 */
async function pollAndExecute() {
  const supabase = await initSupabaseWorkerClient();
  const model = getApprovedModel();
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

  console.log(`[${AGENT_ID}] Worker started (model: ${model}, mode: Blueprint)`);

  while (true) {
    try {
      // === CLAIM ===
      const task = await claimNextTask(supabase);
      if (!task) {
        console.log(`[${AGENT_ID}] No tasks. Sleeping 30s...`);
        await sleep(30000);
        continue;
      }

      const taskId = task.task_id;
      const runtimePacket = JSON.parse(task.runtime_packet);

      console.log(`[${AGENT_ID}] === TASK CLAIMED ===`);
      console.log(`  Task ID: ${taskId}`);
      console.log(`  Lane: ${task.lane}`);
      console.log(`  Type: ${task.task_type}`);

      // === HEARTBEAT (initial) ===
      await renewHeartbeat(supabase, taskId, { phase: "claimed" });

      // === EXECUTE with Claude Agent SDK ===
      console.log(`[${AGENT_ID}] === EXECUTING ===`);
      let heartbeatInterval;
      let findings = null;

      try {
        // Start heartbeat renewal every 5 minutes
        heartbeatInterval = setInterval(async () => {
          await renewHeartbeat(supabase, taskId, {
            phase: "executing",
            timestamp: new Date().toISOString()
          });
        }, 300000); // 5 minutes

        // Build Claude message with Blueprint tools
        const toolDefinitions = [
          {
            name: "read_file",
            description: "Read file contents (Blueprint mode)",
            input_schema: {
              type: "object",
              properties: {
                path: { type: "string", description: "Relative path from repo root" }
              },
              required: ["path"]
            }
          },
          {
            name: "glob_search",
            description: "Search for files matching pattern",
            input_schema: {
              type: "object",
              properties: {
                pattern: { type: "string" }
              },
              required: ["pattern"]
            }
          },
          {
            name: "grep_search",
            description: "Search file contents for regex pattern",
            input_schema: {
              type: "object",
              properties: {
                pattern: { type: "string" },
                path: { type: "string" }
              },
              required: ["pattern"]
            }
          },
          {
            name: "test_execution",
            description: "Run approved non-modifying tests (lint, type-check, validate)",
            input_schema: {
              type: "object",
              properties: {
                test_name: {
                  type: "string",
                  enum: ["test", "lint", "type-check", "validate"]
                }
              },
              required: ["test_name"]
            }
          }
        ];

        // Invoke Claude with agentic loop
        let messages = [
          {
            role: "user",
            content: runtimePacket.instruction || runtimePacket
          }
        ];

        let iteration = 0;
        const maxIterations = 10;

        while (iteration < maxIterations) {
          iteration++;
          console.log(`[${AGENT_ID}] Agent iteration ${iteration}/${maxIterations}`);

          const response = await client.messages.create({
            model,
            max_tokens: 8192,
            tools: toolDefinitions,
            messages
          });

          // Process response
          if (response.stop_reason === "end_turn") {
            // Extract final findings
            for (const block of response.content) {
              if (block.type === "text") {
                findings = {
                  findings: block.text,
                  iterations: iteration,
                  timestamp: new Date().toISOString()
                };
              }
            }
            break;
          }

          if (response.stop_reason === "tool_use") {
            // Execute approved tools
            const toolResults = [];

            for (const block of response.content) {
              if (block.type === "tool_use") {
                const toolName = block.name;
                const toolInput = block.input;

                console.log(`[${AGENT_ID}] Tool: ${toolName}`);

                try {
                  const result = await executeBlueprintTool(toolName, toolInput);
                  toolResults.push({
                    type: "tool_result",
                    tool_use_id: block.id,
                    content: result
                  });
                } catch (toolErr) {
                  toolResults.push({
                    type: "tool_result",
                    tool_use_id: block.id,
                    is_error: true,
                    content: `Tool error: ${toolErr.message}`
                  });
                }
              }
            }

            // Continue conversation with tool results
            messages.push({ role: "assistant", content: response.content });
            messages.push({ role: "user", content: toolResults });
          }
        }

        if (!findings) {
          findings = {
            error: "Max iterations exceeded",
            iterations: maxIterations
          };
        }
      } finally {
        if (heartbeatInterval) clearInterval(heartbeatInterval);
      }

      // === SUBMIT RESULT ===
      console.log(`[${AGENT_ID}] === SUBMITTING RESULT ===`);
      const submitRes = await submitResult(supabase, taskId, findings);

      if (!submitRes.success) {
        console.error(`[${AGENT_ID}] Result submission failed (${submitRes.class}):`, submitRes.error);

        if (submitRes.class === ErrorClass.TRANSIENT) {
          console.log(`[${AGENT_ID}] Transient error. Retrying in 5s...`);
          await sleep(5000);
          continue;
        } else if (submitRes.class === ErrorClass.SECURITY_STOPGATE) {
          console.error(`[${AGENT_ID}] SECURITY STOPGATE - halting execution`);
          break;
        }
      }

      // === MARK FOR VALIDATION (do not release immediately) ===
      console.log(`[${AGENT_ID}] Result pending validation. NOT releasing claim yet.`);

      // Task complete but awaiting deterministic validator
      console.log(`[${AGENT_ID}] === TASK AWAITING VALIDATION ===`);

    } catch (err) {
      const errorClass = classifyError(err);
      console.error(`[${AGENT_ID}] Error (${errorClass}):`, err.message);

      if (errorClass === ErrorClass.TRANSIENT || errorClass === ErrorClass.KNOWN_REPAIRABLE) {
        console.log(`[${AGENT_ID}] Retrying in 5s...`);
        await sleep(5000);
      } else if (errorClass === ErrorClass.SECURITY_STOPGATE) {
        console.error(`[${AGENT_ID}] SECURITY STOPGATE - halting`);
        break;
      } else if (errorClass === ErrorClass.AUTHORIZATION) {
        console.error(`[${AGENT_ID}] Authorization failed - check credentials`);
        break;
      } else {
        console.log(`[${AGENT_ID}] Unknown error. Sleeping 30s...`);
        await sleep(30000);
      }
    }
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// Start worker
pollAndExecute().catch(err => {
  console.error(`[${AGENT_ID}] Fatal error:`, err);
  process.exit(1);
});
