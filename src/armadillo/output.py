"""Publish complete reports without ever replacing an existing destination."""

import os
import tempfile
from pathlib import Path


def write_new(path, text):
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=".armadillo-",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        # Atomic creation, unlike replace/rename this cannot overwrite a collision.
        os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _code(text):
    # JSON escapes controls/newlines; HTML escapes avoid active tags in Markdown.
    import html
    import json

    return "<code>" + html.escape(json.dumps(text, ensure_ascii=False)) + "</code>"


def markdown(report):
    lines = [
        "# Armadillo source-evidence audit",
        "",
        "Status: **" + report["status"] + "**",
        "",
        "Document SHA-256: " + report["document_sha256"],
        "",
        "Input SHA-256: " + report["input_sha256"],
        "",
        "Presence and declared links only; this report does not establish truth or entailment.",
    ]
    if "provenance" in report:
        lines += ["", "## Source provenance"]
        for key, value in report["provenance"].items():
            lines += ["", key + ": " + _code(value)]
    if "last_edit" in report:
        lines += ["", "Last annotation edit: " + _code(report["last_edit"])]
    for finding in report["findings"]:
        lines += [
            "",
            "## " + finding["id"],
            "",
            "Kind: " + finding["kind"],
            "",
            "Quote: " + _code(finding["quote"]),
            "",
            "Quote found: " + str(finding["quote_found"]),
        ]
        if "annotation" in finding:
            lines += ["", "Annotation: " + _code(finding["annotation"])]
        if "source_present_supporters" in finding:
            lines += [
                "",
                "Declared source-present supporters: "
                + (", ".join(finding["source_present_supporters"]) or "none"),
            ]
        for span in finding["occurrences"]:
            lines += [
                "",
                f"Location: line {span['line']}, column {span['column']}; "
                f"character range [{span['start']}, {span['end']})",
                "",
                "Context: " + _code(span["context"]),
            ]
        if finding["occurrences_truncated"]:
            lines += ["", "Additional matches omitted (first 10 displayed)."]
    if "tamandua" in report:
        engine = report["tamandua"]
        lines += [
            "",
            "## Optional Tamandua reasoning",
            "",
            "Engine: " + _code(engine["engine"]),
            "",
            "Asserted triples: " + str(len(engine["analytical"]["asserted"])),
            "",
            "Inferred triples: " + str(len(engine["analytical"]["inferred"])),
            "",
            "Inspect the JSON report for full closure and direct provenance.",
        ]
    return "\n".join(lines) + "\n"
