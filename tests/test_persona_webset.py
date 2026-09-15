"""
DCSE Persona Web Set Test Suite
Task ID: DCSE-PERSONA-WEBSET-20260915-01
Parent Issue: #121 / #116

Validates:
1. Matrix schema, required fields, and 17-record count
2. Parity of internal D10 mapping artifact
3. Coverage of image specs for generatable/decision-required personas
4. Generation and validity of Atlas index and all 17 detail routes
5. Strict D10 privacy & secrecy: zero leakage of internal D10 tokens to public HTML
6. Uniqueness of slugs and nicknames
7. Presence of all required governed sections on detail pages
8. Bidirectional navigation links (Atlas <-> detail routes)
9. Semantic structure and accessibility attributes
10. Meaningful differentiation (zero boilerplate duplication)
"""

import unittest
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GOV_PERSONAS_DIR = BASE_DIR / "governance" / "v7.2" / "personas"
SPECS_DIR = GOV_PERSONAS_DIR / "specs"
PERSONAS_DIR = BASE_DIR / "personas"
MATRIX_PATH = GOV_PERSONAS_DIR / "PERSONA_GOVERNED_MATRIX_V1.json"
MAPPING_JSON_PATH = GOV_PERSONAS_DIR / "INTERNAL_PERSONA_D10_MAPPING_20260915.json"

INTERNAL_D10_RESTRICTED_TOKENS = [
    "Tas",
    "Dex, Paul, Jack",
    "Podcast Buddies",
    "Leslie & Camelia",
    "Shy & Crystal",
    "JJr",
    "Fred & Clarence",
    "BMP",
    "Henry/Elizabeth",
    "Non-Profit/Church Leaders",
    "X5O Solutions",
    "X5O",
    "Ivan (IC)",
    "IC",
    "Gen Z (GN, Nic, ASP)",
    "Tina & Lisa",
    "Mik",
    "Tamyra Kelly",
    "LC Ward",
]

class TestPersonaWebSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MATRIX_PATH.exists():
            raise FileNotFoundError(f"Matrix file not found: {MATRIX_PATH}")
        with open(MATRIX_PATH, "r", encoding="utf-8") as f:
            cls.matrix_data = json.load(f)
        cls.personas = cls.matrix_data.get("personas", [])

    def test_01_matrix_schema_and_count(self):
        self.assertEqual(len(self.personas), 17, "Expected exactly 17 personas in matrix")
        required_keys = [
            "id", "internal_d10_id", "public_nickname", "public_slug", "cluster",
            "cluster_label", "source_refs", "essence", "intended_outcome", "motivations",
            "frictions", "interaction_style", "tech_media_preference", "trust_factors",
            "avoid_factors", "move_forward_guidance", "relevant_governed_pathways",
            "visual_state", "asset_ids", "image_generation_requirement",
            "public_safe_status", "unresolved_rights_evidence", "svg_icon"
        ]
        for p in self.personas:
            for k in required_keys:
                self.assertIn(k, p, f"Persona {p.get('id')} missing key: {k}")
                if k not in ["unresolved_rights_evidence", "image_generation_requirement"]:
                    self.assertTrue(p[k], f"Persona {p.get('id')} has empty field {k}")

    def test_02_internal_d10_mapping_parity(self):
        self.assertTrue(MAPPING_JSON_PATH.exists(), f"Mapping file missing: {MAPPING_JSON_PATH}")
        with open(MAPPING_JSON_PATH, "r", encoding="utf-8") as f:
            mapping_data = json.load(f)
        mappings = mapping_data.get("mappings", [])
        self.assertEqual(len(mappings), 17)
        for p, m in zip(self.personas, mappings):
            self.assertEqual(p["id"], m["id"])
            self.assertEqual(p["internal_d10_id"], m["internal_d10_id"])
            self.assertEqual(p["public_slug"], m["public_slug"])
            self.assertEqual(p["public_nickname"], m["public_nickname"])

    def test_03_image_specs_coverage(self):
        for p in self.personas:
            req = p.get("image_generation_requirement")
            if req:
                spec_file = SPECS_DIR / req
                self.assertTrue(spec_file.exists(), f"Missing image spec file: {spec_file}")
                content = spec_file.read_text(encoding="utf-8")
                self.assertIn(p["public_slug"], content)
                self.assertIn("prohibited_inferences", content)
                self.assertIn("no real client likeness", content)

    def test_04_all_17_routes_generated(self):
        atlas_index = PERSONAS_DIR / "index.html"
        self.assertTrue(atlas_index.exists(), f"Missing Atlas landing page: {atlas_index}")
        for p in self.personas:
            slug = p["public_slug"]
            detail_page = PERSONAS_DIR / slug / "index.html"
            self.assertTrue(detail_page.exists(), f"Missing detail page for {slug}: {detail_page}")
            self.assertGreater(detail_page.stat().st_size, 1000, f"Detail page {slug} is suspiciously small")

    def test_05_strict_d10_leakage_isolation(self):
        all_html_files = list(PERSONAS_DIR.glob("**/*.html"))
        self.assertEqual(len(all_html_files), 18, f"Expected 18 HTML files (1 Atlas + 17 detail), found {len(all_html_files)}")

        leaks = []
        for html_file in all_html_files:
            content = html_file.read_text(encoding="utf-8")
            for token in INTERNAL_D10_RESTRICTED_TOKENS:
                # Use regex with word boundaries where appropriate to avoid false positives
                pattern = r"\b" + re.escape(token) + r"\b"
                if re.search(pattern, content, re.IGNORECASE):
                    # Check if false positive
                    leaks.append((str(html_file.relative_to(BASE_DIR)), token))

        self.assertEqual(len(leaks), 0, f"Detected D10 internal tokens leaked into public HTML: {leaks}")

    def test_06_unique_slugs_and_nicknames(self):
        slugs = [p["public_slug"] for p in self.personas]
        nicknames = [p["public_nickname"] for p in self.personas]
        self.assertEqual(len(slugs), len(set(slugs)), "Duplicate slug detected")
        self.assertEqual(len(nicknames), len(set(nicknames)), "Duplicate nickname detected")

    def test_07_required_sections_present(self):
        required_headers = [
            "What This Person Is Trying to Accomplish",
            "Core Motivations",
            "Common Friction & Barriers",
            "Preferred Interaction Style",
            "Technology & Media Preference",
            "What Earns Trust",
            "What Creates Friction (Avoid)",
            "What Helps Them Move Forward",
            "Relevant Governed Pathways"
        ]
        for p in self.personas:
            detail_page = PERSONAS_DIR / p["public_slug"] / "index.html"
            content = detail_page.read_text(encoding="utf-8")
            for h in required_headers:
                self.assertIn(h, content, f"Missing section '{h}' in {p['public_slug']}/index.html")

    def test_08_bidirectional_links(self):
        atlas_page = PERSONAS_DIR / "index.html"
        atlas_content = atlas_page.read_text(encoding="utf-8")
        for p in self.personas:
            slug = p["public_slug"]
            detail_link = f"./{slug}/index.html"
            self.assertIn(detail_link, atlas_content, f"Atlas index missing link to {detail_link}")

            detail_page = PERSONAS_DIR / slug / "index.html"
            detail_content = detail_page.read_text(encoding="utf-8")
            self.assertIn('href="../index.html"', detail_content, f"Detail page {slug} missing back link to Atlas")

    def test_09_semantic_and_accessibility(self):
        for p in self.personas:
            detail_page = PERSONAS_DIR / p["public_slug"] / "index.html"
            content = detail_page.read_text(encoding="utf-8")
            self.assertIn("<header", content)
            self.assertIn("<main", content)
            self.assertIn("<footer", content)
            self.assertIn("<article", content)
            self.assertIn("<nav", content)
            self.assertIn('aria-label="Breadcrumb"', content)
            self.assertIn(f"<title>{p['public_nickname']} | DCSE Persona Essence</title>", content)

    def test_10_differentiation_no_boilerplate_duplication(self):
        essences = set(p["essence"] for p in self.personas)
        outcomes = set(p["intended_outcome"] for p in self.personas)
        motivations = set(p["motivations"] for p in self.personas)
        frictions = set(p["frictions"] for p in self.personas)
        styles = set(p["interaction_style"] for p in self.personas)
        forwards = set(p["move_forward_guidance"] for p in self.personas)

        self.assertEqual(len(essences), 17, "Identical essence statement detected between personas")
        self.assertEqual(len(outcomes), 17, "Identical intended outcome detected between personas")
        self.assertEqual(len(motivations), 17, "Identical motivation detected between personas")
        self.assertEqual(len(frictions), 17, "Identical friction detected between personas")
        self.assertEqual(len(styles), 17, "Identical interaction style detected between personas")
        self.assertEqual(len(forwards), 17, "Identical move forward guidance detected between personas")

if __name__ == "__main__":
    unittest.main()
