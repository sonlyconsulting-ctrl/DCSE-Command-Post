# ESCD MVP 006 Provider Bindings

The browser never stores or transmits provider secrets.

Required Preview server variables:
- OPENAI_API_KEY
- GEMINI_API_KEY or GOOGLE_API_KEY
- SUPABASE_URL / NEXT_PUBLIC_SUPABASE_URL
- SUPABASE_ANON_KEY / NEXT_PUBLIC_SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY for canonical asset reads
- DDNA_SUPABASE_URL
- DDNA_SUPABASE_SERVICE_ROLE_KEY

Optional model overrides:
- ESCD_OPENAI_MODEL
- ESCD_GEMINI_MODEL

Deferred:
- ANTHROPIC_API_KEY is not consumed by ESCD MVP 006.
- Mistral/Ollama is not consumed by ESCD MVP 006.
