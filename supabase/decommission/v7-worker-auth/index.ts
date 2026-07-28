/**
 * CR-SEC-001 decommission payload for the obsolete v7-worker-auth endpoint.
 *
 * This intentionally preserves the deployed route long enough to return a
 * deterministic safe failure while removing every token-minting capability.
 * The canonical broker is v7-worker-token.
 */

const responseBody = JSON.stringify({
  error: "endpoint_decommissioned",
  replacement: "v7-worker-token",
});

Deno.serve(() =>
  new Response(responseBody, {
    status: 410,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  })
);
