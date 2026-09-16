alter table dcse_cp.escd_provider_config
  drop constraint if exists escd_provider_config_provider_check;

alter table dcse_cp.escd_provider_config
  add constraint escd_provider_config_provider_check
  check (provider = any (array['openai'::text,'gemini'::text,'openrouter'::text,'anthropic'::text]));

insert into dcse_cp.escd_provider_config(
  provider, enabled, model, timeout_seconds, max_output_tokens, thinking_level, secret_name
)
values(
  'anthropic',
  true,
  'claude-3-7-sonnet-20250219',
  45,
  1024,
  null,
  'escd/anthropic/api_key'
)
on conflict (provider) do nothing;
