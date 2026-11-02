import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[1] / "examples/tamandua_integration/input.json"
)


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "armadillo.cli", *map(str, args)],
        capture_output=True,
        text=True,
    )


class EndToEndTests(unittest.TestCase):
    def test_standalone(self):
        result = run("audit", EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "SOURCE_LINKED")

    def test_export(self):
        result = run("export", EXAMPLE)
        self.assertEqual(result.returncode, 0)
        self.assertIn("declaredSupports", result.stdout)

    def test_output_preservation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "result.json"
            self.assertEqual(run("audit", EXAMPLE, "--output", target).returncode, 0)
            original = target.read_bytes()
            self.assertEqual(run("audit", EXAMPLE, "--output", target).returncode, 1)
            self.assertEqual(target.read_bytes(), original)
        original = EXAMPLE.read_bytes()
        self.assertEqual(run("audit", EXAMPLE, "--output", EXAMPLE).returncode, 1)
        self.assertEqual(EXAMPLE.read_bytes(), original)

    def test_missing_tamandua_is_explicit_failure(self):
        result = run("audit", EXAMPLE, "--tamandua", "/missing/tamandua")
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "executable not found", json.loads(result.stderr)["error"]["message"]
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(run("audit", EXAMPLE).returncode, 0)

    def test_malformed_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"schema_version":"2"}')
            result = run("audit", path)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stderr)["error"]["code"], "AUDIT_FAILED")

    def test_export_rejects_integration_flag(self):
        self.assertEqual(run("export", EXAMPLE, "--tamandua", "x").returncode, 1)
