"""Load bundled offline JSON Schemas without filesystem paths or network calls."""

import json
from importlib.resources import files

from .core import AuditError


def load_schema(name):
    if name not in ("input", "report", "adapter"):
        raise AuditError("Schema name must be input, report or adapter")
    return json.loads(
        files("armadillo")
        .joinpath("schemas", name + ".schema.json")
        .read_text(encoding="utf-8")
    )
