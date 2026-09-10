-- ESCD item source provenance links
-- Task: DCSE-ESCD-001-EXEC-PA-003
-- Status: CANDIDATE. Do not apply to production without release approval.

CREATE TABLE IF NOT EXISTS dcse_cp.escd_item_sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_link_key text NOT NULL UNIQUE,
    item_id uuid NOT NULL REFERENCES dcse_cp.escd_items(id) ON DELETE RESTRICT,
    source_system text NOT NULL,
    source_id text NOT NULL,
    source_ref text NOT NULL,
    captured_by_user_id uuid NOT NULL DEFAULT auth.uid(),
    captured_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (item_id, source_system, source_id)
);

CREATE INDEX IF NOT EXISTS escd_item_sources_item_idx
ON dcse_cp.escd_item_sources(item_id, captured_at DESC, id DESC);

ALTER TABLE dcse_cp.escd_item_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE dcse_cp.escd_item_sources FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS escd_item_sources_dcs_owner ON dcse_cp.escd_item_sources;
CREATE POLICY escd_item_sources_dcs_owner
ON dcse_cp.escd_item_sources
FOR ALL TO authenticated
USING (dcse_cp.is_dcs_owner())
WITH CHECK (dcse_cp.is_dcs_owner() AND captured_by_user_id = auth.uid());

REVOKE ALL ON dcse_cp.escd_item_sources FROM authenticated;
GRANT SELECT, INSERT ON dcse_cp.escd_item_sources TO authenticated;

/* ROLLBACK, only after explicit DCS authorization:
DROP TABLE IF EXISTS dcse_cp.escd_item_sources;
*/
