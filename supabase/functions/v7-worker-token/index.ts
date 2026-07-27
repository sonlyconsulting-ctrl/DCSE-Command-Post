/**
 * v7-worker-token — worker access token endpoint (O1)
 *
 * Brokers a scoped Supabase session for an enrolled, approved worker.
 *
 * POST { "agent_id": "...", "enrollment_secret": "..." }
 *   200 { access_token, refresh_token, expires_at, expires_in, agent_id }
 *   400 malformed request
 *   401 unknown agent, not approved, not enrolled, or bad secret
 *   500 sign-in broker failure
 *
 * Why this exists:
 *   workers/claude-reviewer-worker.js refuses the service-role key by design and
 *   requires a WORKER_ACCESS_TOKEN. Nothing deployed could mint one, which is
 *   blocker B2. This endpoint closes that gap.
 *
 * Security properties:
 *   - The enrollment secret is never stored in plaintext; only a bcrypt hash is
 *     held in v7_worker.agent_identity.
 *   - Approval status is re-checked at every token request, so revoking an agent
 *     (status -> suspended) stops new tokens immediately.
 *   - The returned token carries app_metadata.agent_id, which is written only by
 *     service_role. The database derives worker identity solely from that claim,
 *     so a token cannot assert an agent it was not issued for.
 *   - The service-role key never leaves this function.
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return json({ error: "method_not_allowed" }, 405);
  }

  let agentId: string | undefined;
  let secret: string | undefined;
  try {
    const body = await req.json();
    agentId = typeof body?.agent_id === "string" ? body.agent_id : undefined;
    secret = typeof body?.enrollment_secret === "string" ? body.enrollment_secret : undefined;
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  if (!agentId || !secret) {
    return json({ error: "agent_id and enrollment_secret are required" }, 400);
  }

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  // 1. Verify enrollment + approval in the database.
  const { data: checkRows, error: checkError } = await admin
    .schema("v7_worker")
    .rpc("verify_worker_enrollment", {
      p_agent_id: agentId,
      p_enrollment_secret: secret,
    });

  if (checkError) {
    console.error(`[v7-worker-token] verification error for ${agentId}: ${checkError.message}`);
    return json({ error: "verification_failed" }, 500);
  }

  const check = Array.isArray(checkRows) ? checkRows[0] : checkRows;
  if (!check?.valid) {
    // Deliberately coarse to the caller; the precise reason is logged, not returned.
    console.warn(`[v7-worker-token] denied ${agentId}: ${check?.reason ?? "unknown"}`);
    return json({ error: "unauthorized" }, 401);
  }

  // 2. Broker a session for the bound auth user using the presented secret,
  //    which is also that user's password. The anon client is used so the
  //    returned token carries the ordinary authenticated role, never service_role.
  const authClient = createClient(SUPABASE_URL, ANON_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const { data: session, error: signInError } = await authClient.auth.signInWithPassword({
    email: check.auth_email,
    password: secret,
  });

  if (signInError || !session?.session) {
    console.error(`[v7-worker-token] sign-in failed for ${agentId}: ${signInError?.message}`);
    return json({ error: "session_broker_failed" }, 500);
  }

  console.log(`[v7-worker-token] issued token for ${agentId}`);

  return json(
    {
      agent_id: agentId,
      access_token: session.session.access_token,
      refresh_token: session.session.refresh_token,
      expires_at: session.session.expires_at,
      expires_in: session.session.expires_in,
    },
    200,
  );
});
