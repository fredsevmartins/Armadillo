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
        with self.assertRaisesRegex(AuditError, "command failed"):
            reason("this is not RDF", BINARY)

    def test_unicode_control_and_escaped_literal_roundtrip(self):
        text = '🐟 " \\b \n \t \x08 \x0c'
        self.data["nodes"][0]["quote"] = text
        self.data["document"] += text
        result = reason(export_nt(self.data), BINARY)
        self.assertEqual(len(result["analytical"]["asserted"]), 9)

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
