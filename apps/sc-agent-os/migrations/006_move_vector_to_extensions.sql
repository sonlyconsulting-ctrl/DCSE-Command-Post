-- Migration 006: Move vector extension from public to extensions schema
-- Applied: 2026-07-15
-- Resolves: Supabase security advisor finding "extension_in_public" for vector
-- Rollback: ALTER EXTENSION vector SET SCHEMA public;

ALTER EXTENSION vector SET SCHEMA extensions;
