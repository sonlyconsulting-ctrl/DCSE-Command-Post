import { createClient } from "npm:@supabase/supabase-js@2.110.7";

const allowedOrigin = (origin: string | null) => {
  if (!origin) return "https://vow-and-go-review.vercel.app";
  if (/^https:\/\/vow-and-go-review(?:-[a-z0-9-]+)?\.vercel\.app$/i.test(origin)) return origin;
  if (/^http:\/\/(127\.0\.0\.1|localhost):\d+$/i.test(origin)) return origin;
  return "https://vow-and-go-review.vercel.app";
};

const corsHeaders = (origin: string | null) => ({
  "Access-Control-Allow-Origin": allowedOrigin(origin),
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Vary": "Origin",
});

const json = (body: unknown, status: number, origin: string | null) => new Response(JSON.stringify(body), {
  status,
  headers: { ...corsHeaders(origin), "Content-Type": "application/json", "Cache-Control": "no-store" },
});

Deno.serve(async (request) => {
  const origin = request.headers.get("origin");
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders(origin) });
  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405, origin);

  const authorization = request.headers.get("authorization");
  if (!authorization?.startsWith("Bearer ")) return json({ error: "Authentication required" }, 401, origin);

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const publishableKey = Deno.env.get("SUPABASE_ANON_KEY");
  if (!supabaseUrl || !publishableKey) return json({ error: "Function environment is incomplete" }, 503, origin);

  const client = createClient(supabaseUrl, publishableKey, {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { headers: { Authorization: authorization } },
  });
  const { data: userData, error: userError } = await client.auth.getUser();
  if (userError || !userData.user) return json({ error: "Invalid or expired session" }, 401, origin);

  let payload: Record<string, unknown>;
  try { payload = await request.json(); } catch { return json({ error: "Invalid JSON" }, 400, origin); }
  const subject = String(payload.subject || "").trim().slice(0, 180);
  const details = String(payload.details || "").trim().slice(0, 5000);
  if (subject.length < 3 || details.length < 3) return json({ error: "Subject and details are required" }, 400, origin);

  const { data: saved, error: saveError } = await client.rpc("vow_go_feedback_submit", {
    p_payload: { ...payload, subject, details },
  });
  if (saveError) return json({ error: saveError.message }, 403, origin);

  const resendKey = Deno.env.get("RESEND_API_KEY");
  const fromAddress = Deno.env.get("VOW_GO_FEEDBACK_FROM");
  if (!resendKey || !fromAddress) {
    await client.rpc("vow_go_feedback_delivery_update", { p_feedback_id: saved.feedback_id, p_status: "not_configured", p_provider_message_id: null });
    return json({ confirmation_id: saved.confirmation_id, stored: true, email_status: "not_configured" }, 202, origin);
  }

  const emailResponse = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${resendKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: fromAddress,
      to: ["sonlyconsulting@gmail.com"],
      subject: `[Vow & Go ${saved.confirmation_id}] ${subject}`,
      text: `${details}\n\nType: ${String(payload.type || "other")}\nSeverity: ${String(payload.severity || "normal")}\nSubmitted by: ${userData.user.email || userData.user.id}`,
    }),
  });
  const emailResult = await emailResponse.json().catch(() => ({}));
  const emailStatus = emailResponse.ok ? "sent" : "failed";
  await client.rpc("vow_go_feedback_delivery_update", { p_feedback_id: saved.feedback_id, p_status: emailStatus, p_provider_message_id: emailResult.id || null });
  return json({ confirmation_id: saved.confirmation_id, stored: true, email_status: emailStatus }, emailResponse.ok ? 200 : 202, origin);
});
