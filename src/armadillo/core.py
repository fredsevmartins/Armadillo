"""Strict input validation and deterministic evidence-presence audit."""

import hashlib
import json
import os
import re
import stat

from . import __version__

MAX_BYTES = 1024 * 1024
MAX_NODES = 1000
ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,63}\Z")


class AuditError(ValueError):
    """A safe, user-facing input or integration failure."""


def read_file(path):
    """Read bounded regular UTF-8 files; never interpret paths from JSON."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
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


def parse_json(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs,
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
    fields(data, ("schema_version", "document", "nodes"))
    if data["schema_version"] != "1.0":
        raise AuditError("Unsupported input schema_version; expected 1.0")
    _text(data["document"], "document")
    nodes = data["nodes"]
    if not isinstance(nodes, list) or len(nodes) > MAX_NODES:
        raise AuditError("nodes must be an array of at most 1000 entries")
    ids = set()
    for node in nodes:
        fields(node, ("id", "kind", "quote", "supports"))
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
        }
        if node["kind"] == "claim":
            finding["source_present_supporters"] = sorted(supporters[node["id"]])
        findings.append(finding)
    missing = sum(not found for found in verified.values())
    unsupported = sorted(k for k, v in supporters.items() if not v)
    return {
        "schema_version": "1.0",
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
