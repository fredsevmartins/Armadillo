"""Validate offline schemas and representative outputs; requires jsonschema."""

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from armadillo.contracts import load_schema
from armadillo.core import audit
from armadillo.compare import compare
from armadillo.rdf import export_nt
from armadillo.tamandua import reason

parser = argparse.ArgumentParser()
parser.add_argument("--tamandua")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
schemas = {
    name: load_schema(name) for name in ("input", "report", "adapter", "comparison")
}
for schema in schemas.values():
    Draft202012Validator.check_schema(schema)
inputs = [json.loads((root / "examples/tamandua_integration/input.json").read_text())]
inputs += [
    json.loads(path.read_text())["input"]
    for path in (root / "examples/audit_cases").glob("*.json")
]
for data in inputs:
    Draft202012Validator(schemas["input"]).validate(data)
    report = audit(data)
    if args.tamandua:
        report["tamandua"] = reason(export_nt(data), args.tamandua)
        Draft202012Validator(schemas["adapter"]).validate(report["tamandua"])
    Draft202012Validator(schemas["report"]).validate(report)
    comparison = compare(data, data, args.tamandua)
    Draft202012Validator(schemas["comparison"]).validate(comparison)
print(
    f"PASS: 4 schemas and {len(inputs)} representative input/report/comparison workflows; real adapter="
    + str(bool(args.tamandua))
)
