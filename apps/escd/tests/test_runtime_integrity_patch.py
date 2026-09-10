from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATCH = (ROOT / "supabase/migrations/20260910_escd_runtime_integrity_patch.sql").read_text()
API = (ROOT / "apps/escd/api/index.py").read_text()
REPO = (ROOT / "apps/escd/runtime/repository.py").read_text()


def test_history_and_evidence_are_append_only_for_authenticated_runtime():
    assert "GRANT SELECT, INSERT ON dcse_cp.escd_job_events TO authenticated" in PATCH
    assert "GRANT SELECT, INSERT ON dcse_cp.escd_evidence TO authenticated" in PATCH
    assert "GRANT SELECT, INSERT ON dcse_cp.escd_briefing_acks TO authenticated" in PATCH
    assert "GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_jobs TO authenticated" in PATCH
    assert "GRANT SELECT, INSERT, UPDATE ON dcse_cp.escd_approvals TO authenticated" in PATCH


def test_approval_binding_is_immutable_and_transition_guarded():
    assert "escd_validate_approval_update" in PATCH
    assert "approval_binding_immutable" in PATCH
    assert "approval_decision_immutable_without_transition" in PATCH
    assert "authenticated_approval_decision_required" in PATCH
    assert "approval_expired" in PATCH
    assert "WHEN 'pending' THEN NEW.status IN ('approved','rejected','expired','withdrawn')" in PATCH
    assert "WHEN 'approved' THEN NEW.status = 'revoked'" in PATCH


def test_material_binding_fields_are_guarded():
    for field in [
        "job_id",
        "approval_type",
        "action_key",
        "payload_fingerprint",
        "conditions",
        "requested_by_user_id",
        "requested_at",
        "expires_at",
    ]:
        assert f"NEW.{field} IS DISTINCT FROM OLD.{field}" in PATCH


def test_approval_read_uses_repository_safe_lookup():
    assert "approval = repo.get_approval(approval_id)" in API
    assert 'repo._call("GET", f"escd_approvals?id=eq.{approval_id}' not in API
    assert "def get_approval(self, approval_id: str)" in REPO
    assert 'parse.quote(str(approval_id), safe="")' in REPO
