import json
import subprocess
import sys
import unittest
from pathlib import Path

from armadillo.contracts import load_schema
from armadillo.core import audit

ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def test_representative_fixtures(self):
        from armadillo.rdf import export_nt

        for path in (ROOT / "examples/audit_cases").glob("*.json"):
            case = json.loads(path.read_text())
            with self.subTest(case=path.name):
                before = json.dumps(case["input"], sort_keys=True)
                report = audit(case["input"])
                self.assertEqual(report["status"], case["expected"]["status"])
                self.assertEqual(
                    report["unsupported_claims"], case["expected"]["unsupported_claims"]
                )
                self.assertEqual(
                    report["counts"]["missing_quotes"],
                    case["expected"]["missing_quotes"],
                )
                self.assertEqual(report, audit(case["input"]))
                self.assertEqual(export_nt(case["input"]), export_nt(case["input"]))
                self.assertEqual(before, json.dumps(case["input"], sort_keys=True))

    def test_offline_schemas_match_published_sources(self):
        for name in ("input", "report", "adapter", "comparison"):
            self.assertEqual(
                load_schema(name),
                json.loads((ROOT / "schemas" / (name + ".schema.json")).read_text()),
            )

    def test_schema_cli(self):
        result = subprocess.run(
            [sys.executable, "-m", "armadillo.cli", "schema", "report"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), load_schema("report"))

    def test_markdown_cli(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "armadillo.cli",
                "audit",
                str(ROOT / "examples/tamandua_integration/input.json"),
                "--format",
                "markdown",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Location: line 1, column 1", result.stdout)
        self.assertIn("does not establish truth", result.stdout)

    def test_missing_quote_has_no_locations(self):
        report = audit(
            {
                "schema_version": "1.0",
                "document": "present",
                "nodes": [
                    {"id": "c", "kind": "claim", "quote": "missing", "supports": []}
                ],
            }
        )
        finding = report["findings"][0]
        self.assertEqual(finding["occurrences"], [])
        self.assertFalse(finding["occurrences_truncated"])
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
