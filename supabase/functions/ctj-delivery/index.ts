import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "@supabase/supabase-js";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";

const BUCKET = "sc-ctj-deliverables";
const TTL = 900;

type PackageMeta = {
  filename: string;
  size_bytes: number;
  sha256: string;
};

const PRODUCT_CATALOG: Record<string, PackageMeta> = {
  "CTJ-UNIFIED": {
    filename: "CTJ_Unified_Path_v1.0.zip",
    size_bytes: 5852350,
    sha256: "9F9D77F82A5E8D4CE3D03CBD9AF9D2099D50B2ED497C6D1165A5A3F9DA2F4A53",
  },
  "CTJ-PART-1": {
    filename: "CTJ_Part_1_v1.0.zip",
    size_bytes: 10583,
    sha256: "D8789E10D0CCFFE9BF90BA6AA2D930EB20D898CB88892290E6E82F19A7C0FCA5",
  },
  "CTJ-PART-2": {
    filename: "CTJ_Part_2_v1.0.zip",
    size_bytes: 10158,
    sha256: "71040E9511B261F1E3EC13BB0AD0B5537525966DFDEBD9EF343EA41659C68295",
  },
  "CTJ-PART-3": {
    filename: "CTJ_Part_3_v1.0.zip",
    size_bytes: 9631,
    sha256: "22D75E0A3490C73009F81CDEABA94984F8EE94E23F87C816319504E95EB9A2C2",
  },
  "CTJ-COLLECTION": {
    filename: "CTJ_Keeper_Collection_v1.0.zip",
    size_bytes: 25232,
    sha256: "CC5BD9FFE8BB0B93F02BD2A9B06D6B6778ED53EE6847E9EE0212DC29AE5FBBED",
  },
};

// Keeper Collection entitles access to all three Parts as well
const COLLECTION_INCLUDES = ["CTJ-PART-1", "CTJ-PART-2", "CTJ-PART-3", "CTJ-COLLECTION"];

function isEntitledTo(orderProductCode: string, requestedCode: string): boolean {
  if (orderProductCode === requestedCode) return true;
  // Keeper Collection includes all Parts
  if (orderProductCode === "CTJ-COLLECTION" && COLLECTION_INCLUDES.includes(requestedCode)) return true;
  // Unified Path (legacy test product) does not grant Part access
  return false;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders, status: 204 });
  }

  if (!supabaseUrl || !serviceKey) {
    return Response.json(
      { error: "Delivery service misconfigured", status: "error" },
      { status: 503, headers: corsHeaders }
    );
  }

  const supabase = createClient(supabaseUrl, serviceKey);
  const url = new URL(req.url);

  let sessionId = url.searchParams.get("session_id");
  const action = url.searchParams.get("action") ?? "verify";
  // product_code param allows requesting a specific file when the order covers multiple products
  const requestedProduct = url.searchParams.get("product_code") ?? null;

  if (!sessionId && req.method === "POST") {
    try {
      const body = await req.json();
      if (body && typeof body.session_id === "string") {
        sessionId = body.session_id;
      }
    } catch {
      // ignore json parse error
    }
  }

  if (!sessionId || !sessionId.trim()) {
    return Response.json(
      {
        error: "Missing session_id parameter",
        status: "denied",
        message: "Browser arrival at this endpoint is not proof of purchase. A valid Stripe session_id is required.",
      },
      { status: 400, headers: corsHeaders }
    );
  }

  sessionId = sessionId.trim();

  // Query server-side entitlement ledger
  const { data: order, error: dbError } = await supabase
    .from("sc_ctj_orders")
    .select("id, stripe_checkout_session_id, customer_email, payment_status, fulfillment_status, product_code, amount_total, currency, created_at")
    .eq("stripe_checkout_session_id", sessionId)
    .maybeSingle();

  if (dbError) {
    console.error("Database query error:", dbError);
    return Response.json(
      { error: "Entitlement lookup failure", status: "error" },
      { status: 500, headers: corsHeaders }
    );
  }

  if (!order) {
    return Response.json(
      {
        error: "Entitlement record not found",
        status: "denied",
        message: "Browser arrival at this endpoint is not proof of purchase. No verified order matches the supplied session reference.",
        session_id: sessionId,
      },
      { status: 403, headers: corsHeaders }
    );
  }

  if (order.payment_status !== "paid") {
    return Response.json(
      {
        error: "Payment unconfirmed",
        status: "denied",
        message: "Order found in ledger, but payment status is unconfirmed (unpaid).",
        session_id: sessionId,
        payment_status: order.payment_status,
      },
      { status: 403, headers: corsHeaders }
    );
  }

  if (order.fulfillment_status !== "entitled") {
    return Response.json(
      {
        error: "Fulfillment not active",
        status: "denied",
        message: "Order found, but fulfillment status is not entitled.",
        session_id: sessionId,
        fulfillment_status: order.fulfillment_status,
      },
      { status: 403, headers: corsHeaders }
    );
  }

  // Determine which product file to serve
  const targetCode = requestedProduct ?? order.product_code;

  if (!isEntitledTo(order.product_code, targetCode)) {
    return Response.json(
      {
        error: "Not entitled to requested product",
        status: "denied",
        message: `Order for ${order.product_code} does not entitle access to ${targetCode}.`,
        session_id: sessionId,
        order_product_code: order.product_code,
        requested_product_code: targetCode,
      },
      { status: 403, headers: corsHeaders }
    );
  }

  const meta = PRODUCT_CATALOG[targetCode];
  if (!meta) {
    return Response.json(
      {
        error: "Unknown product code",
        status: "denied",
        message: `Product code ${targetCode} is not recognized.`,
      },
      { status: 400, headers: corsHeaders }
    );
  }

  // Generate signed download URL from private storage bucket
  const { data: signedData, error: signError } = await supabase
    .storage
    .from(BUCKET)
    .createSignedUrl(meta.filename, TTL);

  if (signError || !signedData?.signedUrl) {
    console.error("Signed URL error:", signError);
    return Response.json(
      { error: "Could not generate secure download URL", status: "error" },
      { status: 500, headers: corsHeaders }
    );
  }

  if (action === "download") {
    return Response.redirect(signedData.signedUrl, 302);
  }

  return Response.json(
    {
      status: "entitled",
      session_id: order.stripe_checkout_session_id,
      customer_email: order.customer_email,
      product_code: order.product_code,
      delivered_product_code: targetCode,
      payment_status: order.payment_status,
      fulfillment_status: order.fulfillment_status,
      download_url: signedData.signedUrl,
      expires_in: TTL,
      filename: meta.filename,
      size_bytes: meta.size_bytes,
      sha256: meta.sha256,
    },
    { status: 200, headers: corsHeaders }
  );
});
