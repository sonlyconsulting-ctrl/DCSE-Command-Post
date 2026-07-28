/**
 * v7-worker-token — worker access token endpoint (O1)
 *
 * Brokers a scoped Supabase session for an enrolled, approved worker.
 *
 * POST { "agent_id": "...", "enrollment_secret": "..." }
 *   200 { access_token, refresh_token, expires_at, expires_in, agent_id }
 *   400 malformed request
 *   401 unknown agent, not approved, not enrolled, or bad secret
 *   500 broker failure
 *
 * verify_jwt is intentionally false: this endpoint issues the very token a
 * worker does not yet have. It authenticates callers itself via a bcrypt-hashed
 * enrollment secret checked in the database.
 *
 * Verification goes through public.v7_verify_worker_enrollment, a service-role-only
 * bridge, because v7_worker is deliberately NOT an exposed PostgREST schema.
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

  const { data: checkRows, error: checkError } = await admin.rpc(
    "v7_verify_worker_enrollment",
    { p_agent_id: agentId, p_enrollment_secret: secret },
  );

  if (checkError) {
    console.error(`[v7-worker-token] verification error for ${agentId}: ${checkError.message}`);
    return json({ error: "verification_failed", detail: checkError.message }, 500);
  }

  const check = Array.isArray(checkRows) ? checkRows[0] : checkRows;
  if (!check?.valid) {
    console.warn(`[v7-worker-token] denied ${agentId}: ${check?.reason ?? "unknown"}`);
    return json({ error: "unauthorized" }, 401);
  }

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
