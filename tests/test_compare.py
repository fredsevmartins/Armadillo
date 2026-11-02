import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from armadillo.compare import compare
from armadillo.compare import _validate_plan
from armadillo.core import digest
from armadillo.core import AuditError
from armadillo.rdf import export_nt

ROOT = Path(__file__).resolve().parents[1]


class ComparisonTests(unittest.TestCase):
    def test_reject_inconsistent_impact_reports(self):
        triple = {"subject": "<urn:a>", "predicate": "<urn:p>", "object": "<urn:b>"}
        before = {"asserted": [triple], "inferred": []}
        after = {"asserted": [], "inferred": []}
        nt = "<urn:a> <urn:p> <urn:b> .\n"
        changes = {"add": [], "remove": [triple]}
        report = {
            "engine_version": "0.1.0",
            "reasoning_profile": "test profile",
            "graph_id": "sha256:" + digest(nt),
            "input_sha256": digest(nt),
            "changes": changes,
            "baseline_asserted": 1,
            "baseline_inferred": 0,
            "proposed_asserted": 0,
            "proposed_inferred": 0,
            "proposed_assertions": [],
            "proposed_inferences": [],
            "explanations": [],
            "invalidated_explanations": [],
            "impact": {
                "added_assertions": [],
                "removed_assertions": [triple],
                "new_inferences": [],
                "invalidated_inferences": [],
                "unchanged_inferences": [],
                "affected_relationships": [triple],
                "affected_entities": ["<urn:a>", "<urn:b>", "<urn:p>"],
            },
        }
        _validate_plan(report, before, after, nt, changes)
        for mutate in (
            lambda r: r.update(baseline_asserted=True),
            lambda r: r.update(input_sha256="wrong"),
            lambda r: r.update(engine_version="9.0"),
            lambda r: r.update(proposed_assertions=[triple]),
            lambda r: r["impact"].update(removed_assertions=[]),
            lambda r: r["impact"].update(affected_entities=[]),
            lambda r: r.update(explanations=[{}]),
        ):
            corrupted = copy.deepcopy(report)
            mutate(corrupted)
            with self.subTest(mutate=mutate), self.assertRaises(AuditError):
                _validate_plan(corrupted, before, after, nt, changes)

    def setUp(self):
        self.before = json.loads(
            (ROOT / "examples/tamandua_integration/input.json").read_text()
        )
        self.after = copy.deepcopy(self.before)
        self.after["nodes"] = self.after["nodes"][:1]

    def test_standalone_removal_and_input_preservation(self):
        original = copy.deepcopy((self.before, self.after))
        result = compare(self.before, self.after)
        self.assertEqual(result["removed_nodes"], ["evidence1"])
        self.assertEqual(
            result["claim_support_changes"],
            [
                {
                    "claim_id": "claim1",
                    "lost_supporters": ["evidence1"],
                    "gained_supporters": [],
                    "quote_found_before": True,
                    "quote_found_after": True,
                }
            ],
        )
        self.assertEqual(result["proposed_audit"]["unsupported_claims"], ["claim1"])
        self.assertEqual(result["baseline_audit"]["status"], "SOURCE_LINKED")
        self.assertEqual(result["proposed_audit"]["status"], "REVIEW_REQUIRED")
        self.assertNotIn("tamandua_impact", result)
        self.assertEqual((self.before, self.after), original)
        self.assertEqual(result, compare(self.before, self.after))

    def test_identity_stable_in_document_mode(self):
        old = export_nt(self.before, identity="document")
        new = export_nt(self.after, identity="document")
        for line in new.splitlines():
            self.assertIn(line, old.splitlines())
        self.assertNotEqual(export_nt(self.before), export_nt(self.after))

    def test_document_change_rejected(self):
        self.after["document"] += " changed"
        with self.assertRaisesRegex(AuditError, "exact same document"):
            compare(self.before, self.after)

    def test_modified_added_and_order_only(self):
        after = copy.deepcopy(self.before)
        after["nodes"][0]["quote"] = "missing quote"
        after["nodes"].append(
            {"id": "e2", "kind": "evidence", "quote": "items", "supports": []}
        )
        result = compare(self.before, after)
        self.assertEqual(result["modified_nodes"], ["claim1"])
        self.assertEqual(result["added_nodes"], ["e2"])
        after = copy.deepcopy(self.before)
        after["nodes"].reverse()
        self.assertEqual(compare(self.before, after)["modified_nodes"], [])

    def test_cli_comparison_and_option_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            proposed = Path(directory) / "after.json"
            proposed.write_text(json.dumps(self.after))
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "armadillo.cli",
                    "compare",
                    str(ROOT / "examples/tamandua_integration/input.json"),
                    "--against",
                    str(proposed),
                    "--format",
                    "markdown",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Removed Nodes: evidence1", result.stdout)
            result = subprocess.run(
                [sys.executable, "-m", "armadillo.cli", "compare", str(proposed)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("requires --against", result.stderr)
