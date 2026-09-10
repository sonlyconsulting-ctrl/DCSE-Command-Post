-- ESCD item transition alignment
-- Task: DCSE-ESCD-001-EXEC-PA-003
-- Purpose: make database lifecycle enforcement exactly match apps/escd/policy/extensions.py.
-- Status: CANDIDATE. Do not apply to production without release approval.

CREATE OR REPLACE FUNCTION dcse_cp.escd_validate_item_transition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, dcse_cp
AS $$
DECLARE allowed boolean := false;
BEGIN
    IF NEW.status = OLD.status THEN
        NEW.updated_at := now();
        RETURN NEW;
    END IF;

    allowed := CASE OLD.status
        WHEN 'captured' THEN NEW.status IN ('triaged','cancelled')
        WHEN 'triaged' THEN NEW.status IN ('planned','active','waiting','watch','approval','cancelled')
        WHEN 'planned' THEN NEW.status IN ('active','waiting','watch','approval','cancelled')
        WHEN 'active' THEN NEW.status IN ('waiting','watch','approval','completed','cancelled')
        WHEN 'waiting' THEN NEW.status IN ('active','watch','approval','cancelled')
        WHEN 'watch' THEN NEW.status IN ('active','waiting','approval','cancelled')
        WHEN 'approval' THEN NEW.status IN ('active','waiting','cancelled')
        WHEN 'completed' THEN NEW.status = 'archived'
        WHEN 'cancelled' THEN NEW.status = 'archived'
        ELSE false
    END;

    IF NOT allowed THEN
        RAISE EXCEPTION 'invalid_item_transition:%->%', OLD.status, NEW.status USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.status = 'completed' THEN
        NEW.completed_at := COALESCE(NEW.completed_at, now());
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

REVOKE ALL ON FUNCTION dcse_cp.escd_validate_item_transition() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION dcse_cp.escd_validate_item_transition() TO authenticated;

/* ROLLBACK: restore the immediately preceding reviewed function body only after explicit DCS authorization. */
