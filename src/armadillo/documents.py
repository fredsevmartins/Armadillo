"""Prepare unchanged source text and explicitly authored span annotations."""

import copy
from pathlib import Path

from .core import AuditError, MAX_BYTES, canonical, digest, read_file, validate


def serialize_input(data):
    """Produce an input file that can be read back within the file byte cap."""
    validate(data)
    text = canonical(data) + "\n"
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise AuditError(
            "Serialized input exceeds 1 MiB including its final newline; reduce source or annotations"
        )
    return text


def prepare(path, document_id=None, title=None):
    path = Path(path)
    extension = path.suffix.lower().lstrip(".")
    if extension not in ("txt", "md"):
        raise AuditError(
            "prepare supports UTF-8 .txt and .md files; PDF is not supported"
        )
    text = read_file(path)
    provenance = {
        "source_name": path.name,
        "source_format": extension,
        "source_sha256": digest(text),
    }
    if document_id is not None:
        provenance["document_id"] = document_id
    if title is not None:
        provenance["title"] = title
    return validate(
        {
            "schema_version": "1.1",
            "document": text,
            "nodes": [],
            "provenance": provenance,
        }
    )


def annotate(
    data,
    node_id,
    author,
    kind=None,
    start=None,
    end=None,
    supports=None,
    revision=None,
    replace=False,
    delete=False,
):
    validate(data)
    if not isinstance(author, str) or not author.strip():
        raise AuditError(
            "annotate requires a nonblank --author (a reviewer alias is sufficient)"
        )
    if replace and delete:
        raise AuditError("--replace and --delete are mutually exclusive")
    if supports is not None and not isinstance(supports, list):
        raise AuditError("supports must be an explicit list of claim ids")
    result = copy.deepcopy(data)
    result["schema_version"] = "1.1"
    result["last_edit"] = {
        "author": author,
        "action": "delete" if delete else "replace" if replace else "add",
        "node_id": node_id,
    }
    if revision is not None:
        result["last_edit"]["revision"] = revision
    existing = next(
        (i for i, n in enumerate(result["nodes"]) if n["id"] == node_id), None
    )
    if delete:
        if any(v is not None for v in (kind, start, end, supports, revision)):
            raise AuditError("--delete only accepts node id and author")
        if existing is None:
            raise AuditError("Cannot delete an unknown node")
        result["nodes"].pop(existing)
    else:
        if (existing is not None) != replace:
            raise AuditError(
                "Existing nodes require --replace; --replace requires an existing node"
            )
        if (
            type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= len(data["document"])
        ):
            raise AuditError(
                "Select a nonempty Unicode codepoint range 0 <= start < end <= document length"
            )
        targets = supports
        if targets is None:
            targets = result["nodes"][existing]["supports"] if replace else []
        node = {
            "id": node_id,
            "kind": kind,
            "quote": data["document"][start:end],
            "supports": list(targets),
            "annotation": {"author": author, "start": start, "end": end},
        }
        if revision is not None:
            node["annotation"]["revision"] = revision
        if replace:
            result["nodes"][existing] = node
        else:
            result["nodes"].append(node)
    # Dangling links are errors: never delete or rewrite a user's support links implicitly.
    return validate(result)
