"""Execute the documented public CLI in an isolated output directory."""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from armadillo import __version__

parser = argparse.ArgumentParser()
parser.add_argument("--tamandua-repo", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / "examples/document_workflow/source.txt"
original = source.read_bytes()
connection = (
    ["--tamandua-repo", str(args.tamandua_repo.resolve())] if args.tamandua_repo else []
)

with tempfile.TemporaryDirectory(prefix="armadillo-tutorial-") as directory:
    output = Path(directory)

    def command(*arguments):
        result = subprocess.run(
            [sys.executable, "-m", "armadillo.cli", *map(str, arguments)],
            cwd=output,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise SystemExit(result.stderr)
        return result.stdout

    assert command("--version").strip() == __version__
    prepared, claims, full, revised, removed = (
        output / n
        for n in (
            "prepared.json",
            "claims.json",
            "annotated.json",
            "revised.json",
            "removed.json",
        )
    )
    command(
        "prepare",
        source,
        "--document-id",
        "synthetic-sample",
        "--title",
        "Synthetic source",
        "--output",
        prepared,
    )
    command(
        "annotate",
        prepared,
        "--node-id",
        "claim1",
        "--kind",
        "claim",
        "--start",
        0,
        "--end",
        42,
        "--author",
        "reviewer-a",
        "--revision",
        "round-1",
        "--output",
        claims,
    )
    command(
        "annotate",
        claims,
        "--node-id",
        "evidence1",
        "--kind",
        "evidence",
        "--start",
        43,
        "--end",
        79,
        "--supports",
        "claim1",
        "--author",
        "reviewer-b",
        "--revision",
        "round-1",
        "--output",
        full,
    )
    report = json.loads(command("audit", full, *connection))
    assert report["status"] == "SOURCE_LINKED"
    assert report["provenance"]["source_sha256"] == hashlib.sha256(original).hexdigest()
    assert report["findings"][0]["annotation"]["start"] == 0
    markdown = command("audit", full, "--format", "markdown", *connection)
    assert "Source provenance" in markdown and "reviewer-a" in markdown
    command(
        "annotate",
        full,
        "--node-id",
        "evidence1",
        "--kind",
        "evidence",
        "--start",
        43,
        "--end",
        79,
        "--supports",
        "claim1",
        "--author",
        "reviewer-c",
        "--revision",
        "round-2",
        "--replace",
        "--output",
        revised,
    )
    command(
        "annotate",
        revised,
        "--node-id",
        "evidence1",
        "--author",
        "reviewer-c",
        "--delete",
        "--output",
        removed,
    )
    comparison = json.loads(
        command("compare", revised, "--against", removed, *connection)
    )
    assert comparison["removed_nodes"] == ["evidence1"]
    assert comparison["proposed_audit"]["status"] == "REVIEW_REQUIRED"
    if connection:
        assert json.loads(command("doctor", *connection))["status"] == "CONNECTED"
        impact = comparison["tamandua_impact"]["analytical"]["impact"]
        assert len(impact["removed_assertions"]) == 4
        assert len(impact["invalidated_inferences"]) == 1
    assert json.loads(command("schema", "input"))["oneOf"]
    assert json.loads(prepared.read_text())["document"].encode("utf-8") == original
assert source.read_bytes() == original
print(
    f"PASS: documented prepare/annotate/replace/delete/audit/compare CLI; version {__version__}; actual connection={bool(connection)}"
)
