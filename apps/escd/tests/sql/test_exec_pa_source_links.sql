\set ON_ERROR_STOP on

SET ROLE authenticated;
SET "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';

-- Reuse the item created by test_exec_pa_migration.sql and attach two independent source identities.
INSERT INTO dcse_cp.escd_item_sources (
  source_link_key, item_id, source_system, source_id, source_ref
) VALUES (
  'source-link-1',
  '20000000-0000-0000-0000-000000000001',
  'gmail',
  'message-1',
  'gmail:message-1'
),(
  'source-link-2',
  '20000000-0000-0000-0000-000000000001',
  'github',
  'issue-1',
  'github:issue-1'
);

DO $$
BEGIN
  IF (SELECT count(*) FROM dcse_cp.escd_item_sources WHERE item_id = '20000000-0000-0000-0000-000000000001') <> 2 THEN
    RAISE EXCEPTION 'structured_source_provenance_not_preserved';
  END IF;

  BEGIN
    EXECUTE 'UPDATE dcse_cp.escd_item_sources SET source_ref = ''tampered'' WHERE source_link_key = ''source-link-1''';
    RAISE EXCEPTION 'item_source_update_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;

  BEGIN
    EXECUTE 'DELETE FROM dcse_cp.escd_item_sources WHERE source_link_key = ''source-link-1''';
    RAISE EXCEPTION 'item_source_delete_privilege_was_not_blocked';
  EXCEPTION
    WHEN insufficient_privilege THEN NULL;
  END;
END $$;

RESET ROLE;
