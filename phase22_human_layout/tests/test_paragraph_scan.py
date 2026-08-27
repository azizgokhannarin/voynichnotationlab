import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "paragraph_scan.py"
SPEC = importlib.util.spec_from_file_location("paragraph_scan", MODULE_PATH)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class ParagraphScanTests(unittest.TestCase):
    def test_parser_and_summary_keep_boundaries_separate_from_glyphs(self):
        fixture = """#=IVTFF Eva- 2.0 M 5
<f1r> <! $I=H $L=A >
<f1r.1,@P0> <%>pchey.daiin
<f1r.2,+P0> qokey.dam<$>
<f1r.3,+P0> <%>daiin.chedy<$>
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.txt"
            path.write_text(fixture, encoding="latin-1")
            lines = MOD.parse_ivtff(path)
        self.assertEqual(sum(x.paragraph_start for x in lines), 2)
        self.assertEqual(sum(x.paragraph_end for x in lines), 2)
        summary = MOD.summarize_eva(lines)
        self.assertEqual(summary["direct_gallows_at_first_token"]["paragraph_start"]["count"], 1)
        self.assertEqual(summary["terminal_m_at_physical_line_end"]["paragraph_end"]["count"], 1)

    def test_boundary_agreement_uses_locus_identity(self):
        a = [MOD.Line("f1r", "f1r.1", "P0", "H", True, False, ("p",))]
        b = [MOD.Line("f1r", "f1r.1", "P0", "H", True, False, ("x",))]
        self.assertEqual(MOD.boundary_agreement(a, b, "paragraph_start")["jaccard"], 1.0)

    def test_terminal_profiles_separate_paragraph_from_line_end(self):
        lines = [
            MOD.Line("f1r", "f1r.1", "P0", "H", True, True, ("dain",)),
            MOD.Line("f1r", "f1r.2", "P0", "H", False, False, ("dam",)),
        ]
        summary = MOD.summarize_eva(lines)
        self.assertEqual(summary["terminal_character_profiles"]["n"]["paragraph_end"]["count"], 1)
        self.assertEqual(summary["terminal_character_profiles"]["m"]["other_running_line"]["count"], 1)

    def test_quire20_audit_keeps_stars_and_paragraphs_separate(self):
        parsed = {
            "A": [MOD.Line("f1r", "f1r.1", "P0", "S", True, True, ("p",))],
            "B": [MOD.Line("f1r", "f1r.1", "P0", "S", False, False, ("x",))],
        }
        fixture = {
            "source": {"url": "https://example.invalid"},
            "page_star_counts": {"f1r": 2},
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "stars.json"
            import json

            path.write_text(json.dumps(fixture), encoding="utf-8")
            audit = MOD.quire20_boundary_audit(parsed, path)
        self.assertEqual(audit["totals"]["stars"], 2)
        self.assertEqual(audit["totals"]["A_paragraph_starts"], 1)
        self.assertEqual(audit["totals"]["stars_minus_B"], 2)


if __name__ == "__main__":
    unittest.main()
