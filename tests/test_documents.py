import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from armadillo.core import AuditError, audit, validate
from armadillo.documents import annotate, prepare, serialize_input


class DocumentTests(unittest.TestCase):
    def test_generated_input_file_byte_boundary(self):
        from armadillo.core import MAX_BYTES, canonical, parse_json

        data = {"schema_version": "1.0", "document": "", "nodes": []}
        overhead = len(canonical(data).encode("utf-8"))
        data["document"] = "x" * (MAX_BYTES - overhead - 1)
        output = serialize_input(data)
        self.assertEqual(len(output.encode("utf-8")), MAX_BYTES)
        self.assertEqual(parse_json(output), data)
        data["document"] += "x"
        with self.assertRaisesRegex(AuditError, "final newline"):
            serialize_input(data)

    def source(self, directory, raw=b"Claim. Evidence."):
        path = Path(directory) / "source.txt"
        path.write_bytes(raw)
        return path

    def test_preserve_utf8_bom_crlf_and_source_hash(self):
        raw = "\ufeff🐟 Claim.\r\nEvidence.\r\n".encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = self.source(directory, raw)
            data = prepare(path, "synthetic-001", "Synthetic source")
            self.assertEqual(data["document"].encode("utf-8"), raw)
            self.assertEqual(
                data["provenance"]["source_sha256"], hashlib.sha256(raw).hexdigest()
            )
            self.assertEqual(data["provenance"]["source_name"], "source.txt")
            self.assertNotIn(directory, json.dumps(data))
            self.assertEqual(path.read_bytes(), raw)

    def test_markdown_preserves_markup_and_rejects_unsupported_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.md"
            path.write_text("# Heading\n\n**Claim**.")
            self.assertEqual(prepare(path)["document"], path.read_text())
            with self.assertRaisesRegex(AuditError, "PDF"):
                prepare(Path(directory) / "source.pdf")

    def test_empty_invalid_and_oversized_source(self):
        with tempfile.TemporaryDirectory() as directory:
            for raw in (b"", b"\xff", b"x" * (1024 * 1024 + 1)):
                with self.subTest(raw_length=len(raw)), self.assertRaises(AuditError):
                    prepare(self.source(directory, raw))

    def test_add_author_and_codepoint_span(self):
        original = {
            "schema_version": "1.0",
            "document": "🐟 Claim. Evidence.",
            "nodes": [],
        }
        before = copy.deepcopy(original)
        claim = annotate(
            original, "c1", "reviewer-a", "claim", 2, 8, revision="round-1"
        )
        full = annotate(claim, "e1", "reviewer-b", "evidence", 9, 18, ["c1"])
        self.assertEqual(full["nodes"][0]["quote"], "Claim.")
        self.assertEqual(full["nodes"][0]["annotation"]["author"], "reviewer-a")
        self.assertEqual(audit(full)["status"], "SOURCE_LINKED")
        self.assertEqual(
            audit(full)["findings"][0]["annotation"]["revision"], "round-1"
        )
        self.assertEqual(original, before)

    def test_invalid_spans_and_blank_author(self):
        data = {"schema_version": "1.0", "document": "abc", "nodes": []}
        for start, end in ((-1, 1), (0, 0), (2, 1), (0, 4), (True, 2), (0.5, 2)):
            with self.subTest(start=start, end=end), self.assertRaises(AuditError):
                annotate(data, "c", "reviewer", "claim", start, end)
        with self.assertRaisesRegex(AuditError, "author"):
            annotate(data, "c", " ", "claim", 0, 1)
        with self.assertRaisesRegex(AuditError, "explicit list"):
            annotate(data, "e", "reviewer", "evidence", 0, 1, supports="c")

    def test_selected_repeated_quote_and_stale_span(self):
        data = {"schema_version": "1.0", "document": "repeat repeat", "nodes": []}
        data = annotate(data, "c", "reviewer", "claim", 7, 13)
        self.assertEqual(data["nodes"][0]["annotation"]["start"], 7)
        self.assertEqual(len(audit(data)["findings"][0]["occurrences"]), 2)
        data["nodes"][0]["annotation"]["start"] = 6
        with self.assertRaisesRegex(AuditError, "span"):
            validate(data)

    def test_explicit_replace_delete_and_dangling_links(self):
        data = {"schema_version": "1.0", "document": "Claim. Evidence.", "nodes": []}
        data = annotate(data, "c", "a", "claim", 0, 6)
        data = annotate(data, "e", "b", "evidence", 7, 16, ["c"])
        with self.assertRaises(AuditError):
            annotate(data, "c", "a", "claim", 0, 6)
        replaced = annotate(data, "e", "c", "evidence", 7, 16, [], replace=True)
        self.assertEqual(replaced["last_edit"]["action"], "replace")
        kept = annotate(data, "e", "c", "evidence", 7, 16, replace=True)
        self.assertEqual(kept["nodes"][1]["supports"], ["c"])
        with self.assertRaises(AuditError):
            annotate(data, "c", "a", delete=True)
        deleted = annotate(data, "e", "a", delete=True)
        self.assertEqual(
            deleted["last_edit"], {"author": "a", "action": "delete", "node_id": "e"}
        )
        self.assertEqual(audit(deleted)["status"], "REVIEW_REQUIRED")
        self.assertEqual(len(data["nodes"]), 2)
        with self.assertRaises(AuditError):
            annotate(data, "absent", "a", delete=True)

    def test_legacy_schema_stays_strict_and_source_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            data = prepare(self.source(directory))
            data["document"] += " altered"
            with self.assertRaisesRegex(AuditError, "Source hash"):
                validate(data)
        legacy = {
            "schema_version": "1.0",
            "document": "a",
            "nodes": [],
            "last_edit": {},
        }
        with self.assertRaises(AuditError):
            validate(legacy)

    def test_cli_document_to_review_workflow(self):
        def command(*args):
            result = subprocess.run(
                [sys.executable, "-m", "armadillo.cli", *map(str, args)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return result

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = self.source(directory)
            empty, claims, full, report = (
                root / name
                for name in ("empty.json", "claims.json", "full.json", "review.md")
            )
            command("prepare", source, "--document-id", "demo", "--output", empty)
            command(
                "annotate",
                empty,
                "--node-id",
                "c",
                "--kind",
                "claim",
                "--start",
                0,
                "--end",
                6,
                "--author",
                "reviewer",
                "--output",
                claims,
            )
            command(
                "annotate",
                claims,
                "--node-id",
                "e",
                "--kind",
                "evidence",
                "--start",
                7,
                "--end",
                16,
                "--supports",
                "c",
                "--author",
                "reviewer",
                "--output",
                full,
            )
            command("audit", full, "--format", "markdown", "--output", report)
            self.assertIn("SOURCE_LINKED", report.read_text())
            self.assertIn("Source provenance", report.read_text())
            self.assertEqual(source.read_bytes(), b"Claim. Evidence.")
            self.assertEqual(
                json.loads(command("compare", claims, "--against", full).stdout)[
                    "added_nodes"
                ],
                ["e"],
            )
