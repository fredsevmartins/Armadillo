"""Strict input validation and deterministic evidence-presence audit."""

import hashlib
import json
import os
import re
import stat
import math
from bisect import bisect_right

from . import __version__

MAX_BYTES = 1024 * 1024
MAX_NODES = 1000
ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,63}\Z")


class AuditError(ValueError):
    """A safe, user-facing input or integration failure."""


def read_file(path):
    """Read bounded regular UTF-8 files; never interpret paths from JSON."""
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(descriptor, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise AuditError("Input must be a regular file")
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise AuditError("Input exceeds 1 MiB")
        return raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise AuditError("Cannot read a regular UTF-8 input file") from exc


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuditError("Duplicate JSON field: " + key)
        result[key] = value
    return result


def _finite_float(text):
    value = float(text)
    if not math.isfinite(value):
        raise AuditError("Non-finite JSON number")
    return value


def parse_json(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_float=_finite_float,
            parse_constant=lambda _: (_ for _ in ()).throw(
                AuditError("Non-finite JSON number")
            ),
        )
    except (ValueError, RecursionError) as exc:
        raise AuditError("Invalid JSON: " + str(exc)[:160]) from exc


def fields(obj, required, optional=()):
    if not isinstance(obj, dict) or not set(required) <= obj.keys():
        raise AuditError("Missing required object fields: " + ", ".join(required))
    if obj.keys() - set(required) - set(optional):
        raise AuditError("Unknown object fields")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise AuditError(label + " must be a nonempty string")
    try:
        value.encode("utf-8")
    except UnicodeError as exc:
        raise AuditError(label + " must contain valid Unicode") from exc


def validate(data):
    fields(data, ("schema_version", "document", "nodes"), ("provenance", "last_edit"))
    version = data["schema_version"]
    if version not in ("1.0", "1.1"):
        raise AuditError("Unsupported input schema_version; expected 1.0 or 1.1")
    if version == "1.0" and ("provenance" in data or "last_edit" in data):
        raise AuditError("provenance and edit metadata require input schema 1.1")
    _text(data["document"], "document")
    if "last_edit" in data:
        edit = data["last_edit"]
        fields(edit, ("author", "action", "node_id"), ("revision",))
        for key, value in edit.items():
            _text(value, "last_edit." + key)
        if edit["action"] not in ("add", "replace", "delete") or not ID.fullmatch(
            edit["node_id"]
        ):
            raise AuditError("Invalid annotation edit metadata")
    if "provenance" in data:
        provenance = data["provenance"]
        fields(
            provenance,
            ("source_name", "source_format", "source_sha256"),
            ("document_id", "title"),
        )
        for key, value in provenance.items():
            _text(value, "provenance." + key)
        if provenance["source_format"] not in ("txt", "md"):
            raise AuditError("source_format must be txt or md")
        if provenance["source_sha256"] != digest(data["document"]):
            raise AuditError(
                "Source hash does not match document; do not edit imported text silently"
            )
    nodes = data["nodes"]
    if not isinstance(nodes, list) or len(nodes) > MAX_NODES:
        raise AuditError("nodes must be an array of at most 1000 entries")
    ids = set()
    for node in nodes:
        fields(
            node,
            ("id", "kind", "quote", "supports"),
            ("annotation",) if version == "1.1" else (),
        )
        if "annotation" in node:
            annotation = node["annotation"]
            fields(annotation, ("author",), ("revision", "start", "end"))
            for key in ("author", "revision"):
                if key in annotation:
                    _text(annotation[key], "annotation." + key)
            if "start" in annotation or "end" in annotation:
                start, end = annotation.get("start"), annotation.get("end")
                if (
                    type(start) is not int
                    or type(end) is not int
                    or not 0 <= start < end <= len(data["document"])
                    or data["document"][start:end] != node["quote"]
                ):
                    raise AuditError(
                        "Annotation span must exactly identify the quoted source text"
                    )
        if not isinstance(node["id"], str) or not ID.fullmatch(node["id"]):
            raise AuditError("Invalid node id")
        if node["id"] in ids:
            raise AuditError("Duplicate node id")
        ids.add(node["id"])
        if node["kind"] not in ("claim", "evidence"):
            raise AuditError("kind must be claim or evidence")
        _text(node["quote"], "quote")
        targets = node["supports"]
        if (
            not isinstance(targets, list)
            or any(not isinstance(t, str) for t in targets)
            or len(targets) != len(set(targets))
        ):
            raise AuditError("supports must be an array of unique ids")
        if node["kind"] == "claim" and targets:
            raise AuditError("Only evidence nodes may support claims in v1")
    claims = {n["id"] for n in nodes if n["kind"] == "claim"}
    for node in nodes:
        if any(t not in claims for t in node["supports"]):
            raise AuditError("supports must reference existing claim ids")
    if len(canonical(data).encode("utf-8")) > MAX_BYTES:
        raise AuditError("Canonical input exceeds 1 MiB")
    return data


def canonical(data):
    return json.dumps(
        data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def audit(data):
    validate(data)
    document = data["document"]
    line_starts = [0] + [i + 1 for i, char in enumerate(document) if char == "\n"]
    verified = {n["id"]: n["quote"] in document for n in data["nodes"]}
    supporters = {n["id"]: [] for n in data["nodes"] if n["kind"] == "claim"}
    for node in data["nodes"]:
        if node["kind"] == "evidence" and verified[node["id"]]:
            for target in node["supports"]:
                supporters[target].append(node["id"])
    findings = []
    for node in sorted(data["nodes"], key=lambda n: n["id"]):
        finding = {
            "id": node["id"],
            "kind": node["kind"],
            "quote_found": verified[node["id"]],
            "quote": node["quote"],
        }
        if "annotation" in node:
            finding["annotation"] = dict(node["annotation"])
        occurrences = []
        cursor = 0
        while len(occurrences) < 10:
            start = document.find(node["quote"], cursor)
            if start < 0:
                break
            line = bisect_right(line_starts, start)
            occurrences.append(
                {
                    "start": start,
                    "end": start + len(node["quote"]),
                    "line": line,
                    "column": start - line_starts[line - 1] + 1,
                    "context": document[max(0, start - 40) : start + 120],
                }
            )
            cursor = start + 1
        finding["occurrences"] = occurrences
        finding["occurrences_truncated"] = (
            bool(occurrences) and document.find(node["quote"], cursor) >= 0
        )
        if node["kind"] == "claim":
            finding["source_present_supporters"] = sorted(supporters[node["id"]])
        findings.append(finding)
    missing = sum(not found for found in verified.values())
    unsupported = sorted(k for k, v in supporters.items() if not v)
    report = {
        "schema_version": "1.2",
        "software_version": __version__,
        "input_sha256": digest(canonical(data)),
        "document_sha256": digest(document),
        "status": "REVIEW_REQUIRED"
        if not findings or missing or unsupported
        else "SOURCE_LINKED",
        "counts": {
            "nodes": len(findings),
            "claims": len(supporters),
            "missing_quotes": missing,
        },
        "unsupported_claims": unsupported,
        "findings": findings,
        "limitations": "Exact substring presence and user-supplied links only; no truth, entailment, scientific validity or quality assessment.",
    }
    if "provenance" in data:
        report["provenance"] = dict(data["provenance"])
    if "last_edit" in data:
        report["last_edit"] = dict(data["last_edit"])
    return report
