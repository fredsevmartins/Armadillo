import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from armadillo.core import AuditError, audit, parse_json
from armadillo.output import markdown, write_new
from armadillo.process import run
from armadillo.tamandua import preflight, reason


class ReliabilityTests(unittest.TestCase):
    def test_partial_write_cleanup(self):
        import tempfile as temp_module

        original = temp_module.NamedTemporaryFile

        class FailingWriter:
            def __init__(self, *args, **kwargs):
                self.stream = original(*args, **kwargs)
                self.name = self.stream.name

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return self.stream.__exit__(*args)

            def write(self, text):
                self.stream.write(text[:20])
                self.stream.flush()
                raise OSError("simulated partial write")

        with tempfile.TemporaryDirectory() as directory:
            with patch("armadillo.output.tempfile.NamedTemporaryFile", FailingWriter):
                with self.assertRaises(OSError):
                    write_new(Path(directory) / "report", "x" * 100)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_json_exponent_overflow(self):
        for text in ("1e999", "-1e999", '{"value":1e999}'):
            with self.subTest(text=text), self.assertRaises(AuditError):
                parse_json(text)
        self.assertEqual(parse_json("1.25"), 1.25)

    def test_atomic_flush_failure_and_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "report.json"
            with patch(
                "armadillo.output.os.fsync",
                side_effect=OSError("simulated write failure"),
            ):
                with self.assertRaises(OSError):
                    write_new(target, "complete report")
            self.assertEqual(list(Path(directory).iterdir()), [])
            write_new(target, "complete report")
            self.assertEqual(target.read_text(), "complete report")

    def test_collision_and_symlink_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "report"
            target.write_text("existing")
            with self.assertRaises(FileExistsError):
                write_new(target, "replacement")
            link = Path(directory) / "link"
            link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                write_new(link, "replacement")
            self.assertEqual(target.read_text(), "existing")
            self.assertEqual(len(list(Path(directory).iterdir())), 2)

    def test_publish_failure_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("armadillo.output.os.link", side_effect=OSError("no links")):
                with self.assertRaises(OSError):
                    write_new(Path(directory) / "report", "content")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_locations_unicode_overlap_and_truncation(self):
        data = {
            "schema_version": "1.0",
            "document": "🐟\naaaa",
            "nodes": [{"id": "e", "kind": "evidence", "quote": "aa", "supports": []}],
        }
        finding = audit(data)["findings"][0]
        self.assertEqual(
            [
                (o["start"], o["end"], o["line"], o["column"])
                for o in finding["occurrences"]
            ],
            [(2, 4, 2, 1), (3, 5, 2, 2), (4, 6, 2, 3)],
        )
        data["document"] = "a" * 1000
        finding = audit(data)["findings"][0]
        self.assertEqual(len(finding["occurrences"]), 10)
        self.assertTrue(finding["occurrences_truncated"])
        self.assertTrue(all(len(o["context"]) <= 160 for o in finding["occurrences"]))

    def test_markdown_escapes_untrusted_markup(self):
        quote = "<script>alert(1)</script>\n# Fake heading"
        report = audit(
            {
                "schema_version": "1.0",
                "document": quote,
                "nodes": [
                    {"id": "e", "kind": "evidence", "quote": quote, "supports": []}
                ],
            }
        )
        text = markdown(report)
        self.assertNotIn("<script>", text)
        self.assertNotIn("\n# Fake heading", text)
        self.assertIn("Location: line 1, column 1", text)

    def test_process_stream_limits(self):
        for stream in ("stdout", "stderr"):
            with (
                self.subTest(stream=stream),
                self.assertRaisesRegex(AuditError, "capture limit"),
            ):
                run(
                    sys.executable,
                    ["-c", f"import sys; sys.{stream}.write('x'*100000)"],
                    5,
                    stdout_limit=100,
                    stderr_limit=100,
                )

    def test_process_timeout_and_missing_binary(self):
        with self.assertRaisesRegex(AuditError, "timed out"):
            run(sys.executable, ["-c", "import time; time.sleep(5)"], 0.1)
        with self.assertRaisesRegex(AuditError, "not found"):
            run("/missing/armadillo-tamandua", [], 1)

    def test_process_preserves_safe_diagnostics(self):
        with self.assertRaisesRegex(AuditError, "line 3") as caught:
            run(
                sys.executable,
                ["-c", "import sys; sys.stderr.write('line 3\\x1b[31m'); sys.exit(1)"],
                5,
            )
        self.assertNotIn("\x1b", str(caught.exception))

    def test_process_invalid_utf8(self):
        with self.assertRaisesRegex(AuditError, "Cannot execute"):
            run(sys.executable, ["-c", "import os; os.write(1,b'\\xff')"], 5)

    def mocked_closure(self, analytical):
        with patch(
            "armadillo.tamandua._run",
            side_effect=["tamandua 0.1.0", json.dumps({"analytical": analytical})],
        ):
            return reason("<urn:a> <urn:p> <urn:b> .", "mocked-tamandua")

    def test_nonempty_graph_empty_response(self):
        with self.assertRaisesRegex(AuditError, "do not match"):
            self.mocked_closure({"asserted": [], "inferred": [], "derivations": []})

    def test_response_set_invariants(self):
        t = {"subject": "<urn:a>", "predicate": "<urn:p>", "object": "<urn:b>"}
        for assertions, inferences in (
            ([t, t], []),
            ([t], [t]),
            ([dict(t, object="<urn:other>")], []),
        ):
            with self.subTest(assertions=assertions), self.assertRaises(AuditError):
                self.mocked_closure(
                    {"asserted": assertions, "inferred": inferences, "derivations": []}
                )

    def test_missing_and_invalid_provenance(self):
        t = {"subject": "<urn:a>", "predicate": "<urn:p>", "object": "<urn:b>"}
        inferred = dict(t, object="<urn:c>")
        alternatives = [{"rule": "unknown", "premises": [t, t]}]
        for derivations in (
            [],
            [{"conclusion": inferred, "alternatives": []}],
            [{"conclusion": inferred, "alternatives": alternatives}],
            [
                {
                    "conclusion": dict(t, object="<urn:absent>"),
                    "alternatives": alternatives,
                }
            ],
        ):
            with self.subTest(derivations=derivations), self.assertRaises(AuditError):
                self.mocked_closure(
                    {
                        "asserted": [t],
                        "inferred": [inferred],
                        "derivations": derivations,
                    }
                )

    def test_preflight_boundaries(self):
        with self.assertRaisesRegex(AuditError, "2 MiB"):
            preflight(" " * (2 * 1024 * 1024 + 1))
        self.assertEqual(preflight(" " * (2 * 1024 * 1024)), set())
        valid = "".join(f"<urn:a{i}> <urn:p> <urn:b> .\n" for i in range(20000))
        self.assertEqual(len(preflight(valid)), 20000)
        with self.assertRaisesRegex(AuditError, "20000"):
            preflight(valid + "<urn:extra> <urn:p> <urn:b> .\n")

    def test_dense_graph_preflight_no_process(self):
        from armadillo.rdf import export_nt

        data = {"schema_version": "1.0", "document": "x", "nodes": []}
        data["nodes"] = [
            {"id": f"c{i}", "kind": "claim", "quote": "x", "supports": []}
            for i in range(200)
        ]
        data["nodes"] += [
            {
                "id": f"e{i}",
                "kind": "evidence",
                "quote": "x",
                "supports": [f"c{j}" for j in range(200)],
            }
            for i in range(100)
        ]
        with patch("armadillo.tamandua._run") as runner:
            with self.assertRaisesRegex(AuditError, "reduce links"):
                reason(export_nt(data), "mocked-tamandua")
            runner.assert_not_called()
