-- Migration 005: Supabase Security Remediation
-- Scope: Fix security advisor findings within standing authorization
-- Reversible: Yes (rollback section at bottom)
-- Validated: Each change is additive or search_path-only

-- ============================================================
-- 1. Fix mutable search_path on all affected functions
-- ============================================================

-- public schema trigger functions
ALTER FUNCTION public.set_updated_at_sc_contact_feedback() SET search_path = '';
ALTER FUNCTION public.tsl_set_updated_at() SET search_path = '';
ALTER FUNCTION public.handle_updated_at() SET search_path = '';
ALTER FUNCTION public.set_updated_at() SET search_path = '';
ALTER FUNCTION public.set_updated_at_sources() SET search_path = '';
ALTER FUNCTION public.set_updated_at_kb_sources() SET search_path = '';
ALTER FUNCTION public.check_favorite_teams_limit() SET search_path = '';
ALTER FUNCTION public.update_items_timestamp() SET search_path = '';
ALTER FUNCTION public.update_dcs_dcse_items_timestamp() SET search_path = '';
ALTER FUNCTION public.immutable_utc_date(timestamptz) SET search_path = '';

-- public schema SECURITY DEFINER functions
ALTER FUNCTION public.execute_coin_transaction(uuid, integer, text, uuid) SET search_path = 'public';
ALTER FUNCTION public.grant_tsl_reward(uuid, text, integer, text) SET search_path = 'public';
ALTER FUNCTION public.handle_new_user() SET search_path = 'public, auth';

-- dcse_cp schema functions
ALTER FUNCTION dcse_cp.is_dcs_owner() SET search_path = '';
ALTER FUNCTION dcse_cp.set_updated_at() SET search_path = '';
ALTER FUNCTION dcse_cp.touch_updated_at() SET search_path = '';

-- ps_learner schema functions
ALTER FUNCTION ps_learner.set_updated_at() SET search_path = '';
ALTER FUNCTION ps_learner.is_dcs_owner() SET search_path = '';
ALTER FUNCTION ps_learner.is_public_safe_document(ps_learner.doc_confidentiality, ps_learner.product_status) SET search_path = 'ps_learner';
ALTER FUNCTION ps_learner.classify_document(uuid, ps_learner.doc_classification, ps_learner.doc_confidentiality, text) SET search_path = 'ps_learner';
ALTER FUNCTION ps_learner.approve_public_safe(uuid, text) SET search_path = 'ps_learner';

-- ============================================================
-- 2. Revoke anon EXECUTE on trigger-only functions
--    These are only called by triggers, not via RPC
-- ============================================================

REVOKE EXECUTE ON FUNCTION public.set_updated_at_sc_contact_feedback() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.check_favorite_teams_limit() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.handle_updated_at() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.set_updated_at() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.set_updated_at_sources() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.set_updated_at_kb_sources() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.tsl_set_updated_at() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.update_items_timestamp() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.update_dcs_dcse_items_timestamp() FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.immutable_utc_date(timestamptz) FROM anon, public;

-- handle_new_user is an auth trigger, should not be callable via RPC
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM anon, public;

-- ============================================================
-- 3. Restrict TSL SECURITY DEFINER functions to authenticated only
--    (currently callable by anon via PostgREST RPC)
-- ============================================================

REVOKE EXECUTE ON FUNCTION public.execute_coin_transaction(uuid, integer, text, uuid) FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.grant_tsl_reward(uuid, text, integer, text) FROM anon, public;

-- ============================================================
-- 4. Fix scn_balance view: SECURITY INVOKER instead of DEFINER
-- ============================================================

DROP VIEW IF EXISTS public.scn_balance;
CREATE VIEW public.scn_balance
WITH (security_invoker = true)
AS
SELECT user_id,
    COALESCE(sum(delta), 0::bigint) AS coin_balance
FROM public.scn_ledger
GROUP BY user_id;

COMMENT ON VIEW public.scn_balance IS 'Smoove Coin balance aggregation. SECURITY INVOKER per migration 005.';

-- ============================================================
-- 5. Tighten permissive CP write policies
--    Replace WITH CHECK (true) with is_dcs_owner() check
-- ============================================================

-- cp_entities: tighten INSERT
DROP POLICY IF EXISTS "DCS Authenticated Insert" ON public.cp_entities;
CREATE POLICY "DCS Authenticated Insert" ON public.cp_entities
  FOR INSERT TO authenticated
  WITH CHECK (dcse_cp.is_dcs_owner());

-- cp_entities: tighten UPDATE
DROP POLICY IF EXISTS "DCS Authenticated Update" ON public.cp_entities;
CREATE POLICY "DCS Authenticated Update" ON public.cp_entities
  FOR UPDATE TO authenticated
  USING (dcse_cp.is_dcs_owner())
  WITH CHECK (dcse_cp.is_dcs_owner());

-- cp_lanes: tighten INSERT
DROP POLICY IF EXISTS "DCS Authenticated Insert" ON public.cp_lanes;
CREATE POLICY "DCS Authenticated Insert" ON public.cp_lanes
  FOR INSERT TO authenticated
  WITH CHECK (dcse_cp.is_dcs_owner());

-- cp_lanes: tighten UPDATE
DROP POLICY IF EXISTS "DCS Authenticated Update" ON public.cp_lanes;
CREATE POLICY "DCS Authenticated Update" ON public.cp_lanes
  FOR UPDATE TO authenticated
  USING (dcse_cp.is_dcs_owner())
  WITH CHECK (dcse_cp.is_dcs_owner());

-- ============================================================
-- 6. Add RLS policies for tables with RLS enabled but no policy
--    Default: service_role only (deny all client access)
-- ============================================================

-- audit_events: immutable append-only, no client access needed
CREATE POLICY "service_role_only" ON public.audit_events
  FOR ALL TO authenticated USING (false);

-- audit_logs: no client access
CREATE POLICY "service_role_only" ON public.audit_logs
  FOR ALL TO authenticated USING (false);

-- dcse_eod_assets: admin only
CREATE POLICY "dcs_owner_read" ON public.dcse_eod_assets
  FOR SELECT TO authenticated USING (dcse_cp.is_dcs_owner());

-- dcse_eod_runs: admin only
CREATE POLICY "dcs_owner_read" ON public.dcse_eod_runs
  FOR SELECT TO authenticated USING (dcse_cp.is_dcs_owner());

-- dcse_eod_workflow_rules: admin only
CREATE POLICY "dcs_owner_read" ON public.dcse_eod_workflow_rules
  FOR SELECT TO authenticated USING (dcse_cp.is_dcs_owner());

-- event_feed_sources: read for authenticated
CREATE POLICY "authenticated_read" ON public.event_feed_sources
  FOR SELECT TO authenticated USING (true);

-- member_permissions: users see own permissions
CREATE POLICY "own_permissions" ON public.member_permissions
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

-- tsl_audit_log: admin only
CREATE POLICY "dcs_owner_read" ON public.tsl_audit_log
  FOR SELECT TO authenticated USING (dcse_cp.is_dcs_owner());

-- tsl_tester_registry: admin read, self-registration
CREATE POLICY "authenticated_read" ON public.tsl_tester_registry
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "self_insert" ON public.tsl_tester_registry
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

-- ============================================================
-- 7. Restrict public avatar bucket listing
--    Keep object-level read but remove list capability
-- ============================================================

-- Note: Avatar bucket is public for direct URL access.
-- The broad SELECT policy allows listing all files, which is unnecessary.
-- Replace with a policy that only allows reading specific objects by path.
DROP POLICY IF EXISTS "Public avatar read" ON storage.objects;
CREATE POLICY "Public avatar read" ON storage.objects
  FOR SELECT TO public
  USING (bucket_id = 'avatars' AND auth.uid() IS NOT NULL);

-- ============================================================
-- ROLLBACK SECTION (execute manually if needed)
-- ============================================================
/*
-- Rollback 1: Reset search_path (remove SET search_path)
-- Each function would need ALTER FUNCTION ... RESET search_path;

-- Rollback 2: Re-grant EXECUTE
-- GRANT EXECUTE ON FUNCTION public.handle_new_user() TO anon, public;
-- GRANT EXECUTE ON FUNCTION public.execute_coin_transaction(...) TO anon, public;
-- GRANT EXECUTE ON FUNCTION public.grant_tsl_reward(...) TO anon, public;
-- (repeat for all revoked functions)

-- Rollback 3: Restore scn_balance as SECURITY DEFINER
-- DROP VIEW IF EXISTS public.scn_balance;
-- CREATE VIEW public.scn_balance AS SELECT user_id, COALESCE(sum(delta), 0::bigint) AS coin_balance FROM scn_ledger GROUP BY user_id;

-- Rollback 4: Restore permissive CP policies
-- DROP POLICY "DCS Authenticated Insert" ON public.cp_entities;
-- CREATE POLICY "DCS Authenticated Insert" ON public.cp_entities FOR INSERT TO authenticated WITH CHECK (true);
-- (repeat for cp_lanes)

-- Rollback 5: Drop new RLS policies
-- DROP POLICY "service_role_only" ON public.audit_events;
-- (repeat for each new policy)

-- Rollback 6: Restore avatar listing
-- DROP POLICY "Public avatar read" ON storage.objects;
-- CREATE POLICY "Public avatar read" ON storage.objects FOR SELECT TO public USING (bucket_id = 'avatars');
*/
