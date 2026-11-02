"""Mandatory explicit integration suite: missing binary is a failure, never a skip."""

import json
import os
import unittest
from pathlib import Path

from armadillo.core import AuditError, audit
from armadillo.rdf import NS, TYPE, export_nt
from armadillo.tamandua import reason

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get(
    "TAMANDUA_BINARY", str(ROOT.parent / "Tamandua/target/debug/tamandua")
)


class RealTamanduaTests(unittest.TestCase):
    def test_actual_removal_impact_and_repeatability(self):
        import copy
        from armadillo.compare import compare

        before = json.loads(
            (ROOT / "examples/tamandua_integration/input.json").read_text()
        )
        after = copy.deepcopy(before)
        after["nodes"] = after["nodes"][:1]
        report = compare(before, after, BINARY)
        impact = report["tamandua_impact"]["analytical"]["impact"]
        self.assertEqual(len(impact["removed_assertions"]), 4)
        self.assertEqual(len(impact["invalidated_inferences"]), 1)
        self.assertEqual(len(impact["unchanged_inferences"]), 1)
        self.assertEqual(report, compare(before, after, BINARY))

    def test_actual_addition_and_noop_impact(self):
        import copy
        from armadillo.compare import compare

        full = json.loads(
            (ROOT / "examples/tamandua_integration/input.json").read_text()
        )
        partial = copy.deepcopy(full)
        partial["nodes"] = partial["nodes"][:1]
        addition = compare(partial, full, BINARY)["tamandua_impact"]["analytical"][
            "impact"
        ]
        self.assertEqual(len(addition["added_assertions"]), 4)
        self.assertEqual(len(addition["new_inferences"]), 1)
        noop = compare(full, full, BINARY)["tamandua_impact"]["analytical"]["impact"]
        self.assertEqual(noop["affected_relationships"], [])

    def test_representative_graphs_and_markdown_cli(self):
        for path in (ROOT / "examples/audit_cases").glob("*.json"):
            case = json.loads(path.read_text())
            with self.subTest(case=path.name):
                result = reason(export_nt(case["input"]), BINARY)
                self.assertTrue(result["analytical"]["asserted"])
                self.assertEqual(
                    audit(case["input"])["status"], case["expected"]["status"]
                )

    def setUp(self):
        self.data = json.loads(
            (ROOT / "examples/tamandua_integration/input.json").read_text()
        )

    def test_actual_subclass_inference(self):
        result = reason(export_nt(self.data), BINARY)
        inferred = result["analytical"]["inferred"]
        expected = {
            "subject": "<urn:sha256:" + audit(self.data)["input_sha256"] + ":claim1>",
            "predicate": "<" + TYPE + ">",
            "object": "<" + NS + "ArgumentNode>",
        }
        self.assertIn(expected, inferred)
        self.assertTrue(result["analytical"]["derivations"])

    def test_analytical_repeatability(self):
        nt = export_nt(self.data)
        self.assertEqual(reason(nt, BINARY), reason(nt, BINARY))

    def test_actual_invalid_rdf(self):
        with self.assertRaisesRegex(AuditError, "Invalid N-Triples"):
            reason("this is not RDF", BINARY)
        from armadillo.process import run
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.nt"
            path.write_text("this is not RDF")
            with self.assertRaisesRegex(AuditError, "line 1"):
                run(BINARY, ["reason", str(path)], 30)

    def test_blank_node_exchange(self):
        result = reason('_:a <urn:p> "source" .\n', BINARY)
        self.assertEqual(len(result["analytical"]["asserted"]), 1)

    def test_unicode_control_and_escaped_literal_roundtrip(self):
        text = '🐟 " \\b \n \t \x08 \x0c'
        self.data["nodes"][0]["quote"] = text
        self.data["document"] += text
        result = reason(export_nt(self.data), BINARY)
        self.assertEqual(len(result["analytical"]["asserted"]), 9)
        from rdflib import Graph, Literal

        returned = "\n".join(
            " ".join(t[k] for k in ("subject", "predicate", "object")) + " ."
            for t in result["analytical"]["asserted"]
        )
        graph = Graph().parse(data=returned, format="nt")
        self.assertIn(Literal(text), set(graph.objects()))

    def test_integrated_cli(self):
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "armadillo.cli",
                "audit",
                str(ROOT / "examples/tamandua_integration/input.json"),
                "--tamandua",
                BINARY,
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            len(json.loads(result.stdout)["tamandua"]["analytical"]["inferred"]), 2
        )


if __name__ == "__main__":
    unittest.main()
