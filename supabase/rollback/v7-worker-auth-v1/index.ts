/**
 * Supabase Edge Function: v7-worker-auth
 *
 * Provides scoped authentication for autonomous worker agents.
 * Workers receive a time-limited, capability-scoped token instead of
 * the service-role key (which must never leave the server).
 *
 * Usage:
 *   POST /functions/v1/v7-worker-auth
 *   Body: { agent_id: "AGENT-CLAUDE-01@DEVICE", capabilities: ["read_queue", "write_results"] }
 *   Returns: { access_token: "...", expires_in: 3600, scope: [...] }
 */

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import * as jose from "https://deno.land/x/jose@v5.1.0/index.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const JWT_SECRET = Deno.env.get("JWT_SECRET") || SUPABASE_SERVICE_ROLE_KEY;

// Approved agent capabilities per role
const AGENT_CAPABILITIES = {
  "AGENT-CLAUDE-REVIEWER-01@STAGING": {
    scopes: ["read_v7_worker_queues", "read_dcse_cp_schema", "write_v7_worker_results", "write_v7_worker_heartbeats"],
    max_tokens: 8192,
    tools: ["read_file", "glob_search", "grep_search", "git_diff", "test_execution"]
  },
  "AGENT-CLAUDE-IMPLEMENTATION-01@STAGING": {
    scopes: ["read_v7_worker_queues", "write_dcse_cp_schema", "write_v7_worker_results"],
    max_tokens: 4096,
    tools: ["read_file", "edit_file", "write_file", "bash_execution", "git_operations"]
  },
  "AGENT-QWEN-BUILDER-01@DEVICE": {
    scopes: ["read_v7_worker_queues", "write_v7_worker_results"],
    max_tokens: 4096,
    tools: ["shell_exec", "file_io"]
  }
};

const DEFAULT_TOKEN_EXPIRY = 3600; // 1 hour

async function generateWorkerToken(
  agentId: string,
  capabilities: string[]
): Promise<{ access_token: string; expires_in: number; scope: string[] }> {
  if (!AGENT_CAPABILITIES[agentId]) {
    throw new Error(`Agent ${agentId} not in allowlist`);
  }

  const approved = AGENT_CAPABILITIES[agentId];
  const requestedScopes = capabilities || approved.scopes;

  // Verify requested scopes are in approved set
  const validScopes = requestedScopes.filter(s => approved.scopes.includes(s));
  if (validScopes.length === 0) {
    throw new Error(`No valid scopes requested for ${agentId}`);
  }

  // Generate JWT with scoped claims
  const now = Math.floor(Date.now() / 1000);
  const expiresAt = now + DEFAULT_TOKEN_EXPIRY;

  const token = await new jose.SignJWT({
    agent_id: agentId,
    scope: validScopes,
    max_tokens: approved.max_tokens,
    tools: approved.tools,
    aud: "v7-worker-queue"
  })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt(now)
    .setExpirationTime(expiresAt)
    .sign(new TextEncoder().encode(JWT_SECRET));

  return {
    access_token: token,
    expires_in: DEFAULT_TOKEN_EXPIRY,
    scope: validScopes
  };
}

serve(async (req) => {
  // Only POST allowed
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const body = await req.json();
    const { agent_id, capabilities } = body;

    if (!agent_id) {
      return new Response(
        JSON.stringify({ error: "agent_id required" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    const result = await generateWorkerToken(agent_id, capabilities);

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    console.error("Error:", error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }
});
