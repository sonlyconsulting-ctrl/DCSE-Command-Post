# SC Agent OS Chat Transport Repair

Status: Review
Date: 2026-07-29
Scope: SC Agent OS authenticated chat only

## Verified defect

The existing authenticated wrapper consumed the POST body and then reconstructed the request by copying the consumed request object onto a new Readable stream. That copied internal stream state could prevent the downstream chat handler from receiving a complete end event, leaving Vercel requests open until the 300-second platform timeout.

## Repair

A dedicated `/api/chat` handler now:

- authenticates the operator through the existing Supabase session cookies;
- reads and validates the request body once;
- injects provider credentials only on the server;
- sends requests directly to OpenAI, Anthropic, Gemini, Qwen, or Ollama;
- applies a bounded upstream timeout, default 60 seconds;
- returns explicit authentication, configuration, provider, timeout, and local Ollama errors;
- limits body size and message count;
- preserves the existing login, reset, dashboard, and sidebar code paths.

`vercel.json` routes only `/api/chat` to the dedicated handler before the existing catch-all rewrites. No other route behavior changes.

## Validation target

- Node syntax check for `api/chat.js`
- Authenticated OpenAI round trip
- Unauthenticated rejection before provider access
- Ollama unavailable-state handling
- Vercel preview build
- Manual authenticated preview test

## Exclusions

- No Supabase schema or data changes
- No authentication weakening
- No provider keys in browser code
- No sidebar or navigation changes
- No production merge or deployment in this review branch
