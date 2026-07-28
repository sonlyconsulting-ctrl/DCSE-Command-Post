/**
 * v7-result-bridge — HTTP entry point for the result bridge (B4)
 *
 * Bridges v7_worker.result_submission -> dcse_cp.agent_task_events.
 *
 * The bridging logic itself lives in SQL (v7_worker.bridge_pending_results),
 * reached here through public.v7_run_result_bridge, which is service_role only.
 * Keeping the logic in the database means:
 *   - the pg_cron job can run it without an HTTP callout, so no service-role key
 *     has to be stored in the database for pg_net to authenticate;
 *   - task resolution, event-type mapping and acknowledgement all happen in one
 *     transaction per submission.
 *
 * This function exists for external and manual invocation.
 *
 * Replaces an earlier version that could not have worked: it wrote
 * submission.task_id (TEXT) straight into dcse_cp.agent_task_events.task_id
 * (UUID NOT NULL, FK to agent_tasks), and passed worker event types straight
 * into a CHECK-constrained column. Both are handled in SQL now.
 *
 * POST /functions/v1/v7-result-bridge   { "limit": 25 }
 *   200 { status, processed, failed, skipped, duration_ms, receipt_id }
 *   401 caller is not service_role
 *   500 bridge error
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  // Only the service role may drive the bridge. verify_jwt=true admits any valid
  // project JWT, including anon, so the role claim is checked explicitly.
  const auth = req.headers.get("Authorization") ?? "";
  const token = auth.replace(/^Bearer\s+/i, "");
  let role: string | undefined;
  try {
    const payload = JSON.parse(atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
    role = payload?.role;
  } catch {
    return json({ error: "unauthorized" }, 401);
  }
  if (role !== "service_role") {
    console.warn(`[v7-result-bridge] refused caller with role=${role}`);
    return json({ error: "unauthorized" }, 401);
  }

  let limit = 25;
  try {
    const body = await req.json();
    if (Number.isInteger(body?.limit)) limit = body.limit;
  } catch {
    // empty body is fine; use the default
  }

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const { data, error } = await admin.rpc("v7_run_result_bridge", { p_limit: limit });

  if (error) {
    console.error(`[v7-result-bridge] bridge error: ${error.message}`);
    return json({ status: "error", error: error.message }, 500);
  }

  const row = Array.isArray(data) ? data[0] : data;
  console.log(
    `[v7-result-bridge] cycle complete: processed=${row?.processed} failed=${row?.failed} skipped=${row?.skipped}`,
  );

  return json({
    status: (row?.failed ?? 0) > 0 ? "partial" : "success",
    processed: row?.processed ?? 0,
    failed: row?.failed ?? 0,
    skipped: row?.skipped ?? 0,
    duration_ms: row?.duration_ms ?? 0,
    receipt_id: row?.receipt_id ?? null,
  }, 200);
});
