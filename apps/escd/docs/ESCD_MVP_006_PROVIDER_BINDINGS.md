# ESCD MVP 006 Provider Bindings

The browser sends a newly entered provider key only to the authenticated ESCD API on the same origin. The server stores it in Supabase Vault, verifies it by reading it back server-side, and returns only credential status. The browser never persists the key or retrieves an existing key.

Required Preview server variables:
- SUPABASE_URL / NEXT_PUBLIC_SUPABASE_URL
- SUPABASE_ANON_KEY / NEXT_PUBLIC_SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY for canonical asset reads
- DDNA_SUPABASE_URL
- DDNA_SUPABASE_SERVICE_ROLE_KEY

Root Command Post and ESCD share SC-Command-Post (`nevgdyfpxdaloacuutal`). The root wrapper and ESCD auth prefer SUPABASE_URL and SUPABASE_ANON_KEY, falling back to the NEXT_PUBLIC names. ESCD privileged calls use SUPABASE_SERVICE_ROLE_KEY, with the historical PABASE_SECRET_KEY fallback. A legacy JWT service credential must declare this same project and the service_role role; actual registry access must also succeed.

Provider keys and model settings are loaded from dcse_cp.escd_provider_config and its service-only Vault RPC on every request. OpenAI/Gemini Vercel keys are not required. Existing environment fallbacks are compatibility-only and must not mask a registry connection failure. ESCD_OPENAI_MODEL and ESCD_GEMINI_MODEL are not consumed by this runtime registry.

Use Save settings to save the model/config and an optional entered replacement key together. Save key only changes the credential. Successful saves show verified Vault status immediately. An unsaved key is retained on failure in the current password input only; switching providers clears it. Neither key nor model changes require a deployment.

OpenRouter is already supported by the registry, UI, and request adapter. Its live registry row is disabled and has no Vault key. Leave it disabled until a key is supplied.

Vercel Preview branch: feature/escd-minimal-mvp-006. Production URLs built from main do not contain the ESCD routes. Do not use a main/production redeployment to validate ESCD Preview, and do not change Production bindings as part of this repair.

Deferred:
- ANTHROPIC_API_KEY is not consumed by ESCD MVP 006.
- Mistral/Ollama is not consumed by ESCD MVP 006.
