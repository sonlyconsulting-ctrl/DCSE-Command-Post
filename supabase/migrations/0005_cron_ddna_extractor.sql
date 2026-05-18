-- Migration: 0005_cron_ddna_extractor
-- GATE: DCS approval + JWT provisioning required before applying.
-- Prerequisites: Migration 0004 must be applied first (ddna_extraction_runs table).
--
-- Registers the ddna-extractor-daily pg_cron job.
-- The edge function URL and service-role key are injected at runtime via
-- Supabase Vault secrets; do NOT hard-code credentials here.
--
-- DCS must confirm:
--   1. Desired schedule (default below: 02:00 UTC daily)
--   2. Timezone (default: UTC)
--   3. Edge function JWT has been provisioned and stored in Vault as
--      'ddna_extractor_jwt'

-- Requires pg_cron and pg_net extensions to be enabled in the dashboard.

select cron.schedule(
  'ddna-extractor-daily',
  '0 2 * * *',   -- 02:00 UTC every day — adjust after DCS confirms timezone
  $$
    select net.http_post(
      url     := current_setting('app.supabase_url') || '/functions/v1/dcse_trigger_ddna_extraction',
      headers := jsonb_build_object(
        'Content-Type',  'application/json',
        'Authorization', 'Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'ddna_extractor_jwt')
      ),
      body    := jsonb_build_object(
        'triggered_by', 'cron',
        'run_date',     current_date::text
      )
    );
  $$
);
