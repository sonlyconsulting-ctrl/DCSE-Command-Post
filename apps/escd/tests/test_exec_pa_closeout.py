from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

from apps.escd.runtime.repository import SupabaseRLSClient
from apps.escd.runtime.source_links import ensure_item_source


class SourceLinkRepositoryTests(unittest.TestCase):
    def test_source_link_is_idempotent_and_structured(self):
        class FakeRepo(SupabaseRLSClient):
            def __init__(self):
                self.stored = None
                self.posts = 0

            def _call(self, method, path, payload=None):
                if method == "GET" and path.startswith("escd_item_sources?"):
                    return [self.stored] if self.stored else []
                if method == "POST" and path == "escd_item_sources":
                    self.posts += 1
                    self.stored = {**payload, "id": "s1"}
                    return [self.stored]
                raise AssertionError((method, path, payload))

        repo = FakeRepo()
        args = dict(
            source_link_key="source-key",
            item_id="item-1",
            source_system="gmail",
            source_id="message-1",
            source_ref="gmail:message-1",
        )
        first = ensure_item_source(repo, **args)
        second = ensure_item_source(repo, **args)
        self.assertEqual(first, second)
        self.assertEqual(repo.posts, 1)
        self.assertEqual(first["source_system"], "gmail")
        self.assertEqual(first["source_id"], "message-1")
        self.assertEqual(first["source_ref"], "gmail:message-1")


class CombinedTrancheStaticTests(unittest.TestCase):
    def setUp(self):
        self.api = (ROOT / "apps/escd/api/index.py").read_text()
        self.ui = (ROOT / "apps/escd/web/index.html").read_text()
        self.source_mig = (ROOT / "supabase/migrations/20260910_escd_exec_pa_source_links.sql").read_text()
        self.alignment = (ROOT / "supabase/migrations/20260910_escd_exec_pa_transition_alignment.sql").read_text()
        self.policy = (ROOT / "apps/escd/policy/extensions.py").read_text()

    def test_intake_persists_structured_source_for_new_and_deduped_items(self):
        self.assertIn("from apps.escd.runtime.source_links import ensure_item_source", self.api)
        self.assertGreaterEqual(self.api.count("ensure_item_source("), 2)
        self.assertIn('"source_link": source_link', self.api)

    def test_source_links_are_rls_and_append_only(self):
        self.assertIn("ALTER TABLE dcse_cp.escd_item_sources ENABLE ROW LEVEL SECURITY", self.source_mig)
        self.assertIn("ALTER TABLE dcse_cp.escd_item_sources FORCE ROW LEVEL SECURITY", self.source_mig)
        self.assertIn("GRANT SELECT, INSERT ON dcse_cp.escd_item_sources TO authenticated", self.source_mig)
        self.assertNotIn("GRANT UPDATE", self.source_mig)
        self.assertNotIn("GRANT DELETE", self.source_mig)
        self.assertIn("captured_by_user_id = auth.uid()", self.source_mig)

    def test_ui_surfaces_existing_combined_build_plan_without_unsafe_rendering(self):
        for queue in ("NOW", "APPROVAL", "WAITING", "WATCH", "BACKLOG"):
            self.assertIn(queue, self.ui)
        self.assertIn('/intake', self.ui)
        self.assertIn('/commands/parse', self.ui)
        self.assertIn('/executive-stream', self.ui)
        self.assertNotIn("innerHTML", self.ui)
        self.assertIn("textContent", self.ui)
        self.assertIn("No execution performed.", self.ui)

    def test_transition_alignment_tracks_approved_policy_edges(self):
        expected = [
            "WHEN 'captured' THEN NEW.status IN ('triaged','cancelled')",
            "WHEN 'triaged' THEN NEW.status IN ('planned','active','waiting','watch','approval','cancelled')",
            "WHEN 'planned' THEN NEW.status IN ('active','waiting','watch','approval','cancelled')",
            "WHEN 'active' THEN NEW.status IN ('waiting','watch','approval','completed','cancelled')",
            "WHEN 'waiting' THEN NEW.status IN ('active','watch','approval','cancelled')",
            "WHEN 'watch' THEN NEW.status IN ('active','waiting','approval','cancelled')",
            "WHEN 'approval' THEN NEW.status IN ('active','waiting','cancelled')",
        ]
        for edge in expected:
            self.assertIn(edge, self.alignment)
        self.assertIn('"triaged": {"planned", "active", "waiting", "watch", "approval", "cancelled"}', self.policy)
        self.assertIn('"waiting": {"active", "watch", "approval", "cancelled"}', self.policy)
        self.assertIn('"watch": {"active", "waiting", "approval", "cancelled"}', self.policy)
        self.assertIn('"approval": {"active", "waiting", "cancelled"}', self.policy)

    def test_no_out_of_plan_runtime_expansion(self):
        combined = (self.api + self.ui + self.source_mig + self.alignment).lower()
        self.assertNotIn("dcs_employment", combined)
        self.assertNotIn("ddna_runtime_mode", combined)
        self.assertNotIn("supabase_service_role_key", combined)


if __name__ == "__main__":
    unittest.main()
