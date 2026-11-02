import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

from armadillo.core import AuditError, audit, parse_json, read_file, validate
from armadillo.rdf import export_nt

EXAMPLE = (
    Path(__file__).resolve().parents[1] / "examples/tamandua_integration/input.json"
)


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE.read_text())

    def test_reference_case(self):
        result = audit(self.data)
        self.assertEqual(result["status"], "SOURCE_LINKED")
        self.assertEqual(
            result["counts"], {"nodes": 2, "claims": 1, "missing_quotes": 0}
        )
        self.assertEqual(
            result["findings"][0]["source_present_supporters"], ["evidence1"]
        )

    def test_fabricated_quote_cannot_support(self):
        self.data["nodes"][1]["quote"] = "fabricated"
        result = audit(self.data)
        self.assertEqual(result["unsupported_claims"], ["claim1"])
        self.assertEqual(result["counts"]["missing_quotes"], 1)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")

    def test_empty_graph_requires_review(self):
        self.data["nodes"] = []
        self.assertEqual(audit(self.data)["status"], "REVIEW_REQUIRED")

    def test_missing_claim_quote_requires_review(self):
        self.data["nodes"][0]["quote"] = "absent"
        self.assertEqual(audit(self.data)["status"], "REVIEW_REQUIRED")

    def test_no_mutation_and_repeatability(self):
        original = copy.deepcopy(self.data)
        self.assertEqual(audit(self.data), audit(self.data))
        self.assertEqual(self.data, original)
        self.assertEqual(export_nt(self.data), export_nt(self.data))

    def test_unicode_exactness(self):
        self.data["document"] = "café 🐟"
        self.data["nodes"] = [
            {"id": "c", "kind": "claim", "quote": "cafe\u0301", "supports": []}
        ]
        self.assertFalse(audit(self.data)["findings"][0]["quote_found"])

    def test_digest_changes_with_input(self):
        before = audit(self.data)
        self.data["document"] += " "
        after = audit(self.data)
        self.assertNotEqual(before["input_sha256"], after["input_sha256"])
        self.assertNotEqual(before["document_sha256"], after["document_sha256"])

    def test_invalid_inputs(self):
        mutations = [
            lambda d: d.pop("document"),
            lambda d: d.update(schema_version="2.0"),
            lambda d: d.update(extra=True),
            lambda d: d.update(document=""),
            lambda d: d.update(nodes={}),
            lambda d: d["nodes"].append(d["nodes"][0]),
            lambda d: d["nodes"][0].update(id="../../x"),
            lambda d: d["nodes"][0].update(kind="unknown"),
            lambda d: d["nodes"][0].update(quote=" "),
            lambda d: d["nodes"][1].update(supports=["unknown"]),
            lambda d: d["nodes"][1].update(supports=["evidence1"]),
            lambda d: d["nodes"][1].update(supports=["claim1", "claim1"]),
            lambda d: d["nodes"][0].update(supports=["claim1"]),
            lambda d: d.update(document="\ud800"),
            lambda d: d.update(nodes=[{}] * 1001),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = copy.deepcopy(self.data)
                mutate(data)
                with self.assertRaises(AuditError):
                    validate(data)

    def test_strict_json(self):
        for text in ('{"x":1,"x":2}', "{", "NaN", "Infinity"):
            with self.subTest(text=text), self.assertRaises(AuditError):
                parse_json(text)

    def test_file_limits_and_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input"
            for content in (b"a" * (1024 * 1024 + 1), b"\xff"):
                path.write_bytes(content)
                with self.assertRaises(AuditError):
                    read_file(path)
            with self.assertRaises(AuditError):
                read_file(Path(directory) / "missing")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX only")
    def test_fifo_does_not_block(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fifo"
            os.mkfifo(path)
            with self.assertRaises(AuditError):
                read_file(path)

    def test_rdf_escaping(self):
        self.data["nodes"][0]["quote"] = '"\\b\n\t\b\f🐟'
        nt = export_nt(self.data)
        self.assertIn("\\u0008", nt)
        self.assertIn("\\u000c", nt)
        self.assertIn("🐟", nt)
        self.assertNotIn("\x08", nt)
