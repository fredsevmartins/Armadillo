"""CLI with exclusive output creation and structured errors."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import AuditError, audit, parse_json, read_file, validate
from .rdf import export_nt
from .tamandua import reason


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit source evidence without a network service"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("command", choices=("audit", "export"))
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--tamandua", type=Path, help="Explicit trusted Tamandua executable"
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "export" and args.tamandua:
            raise AuditError("--tamandua is only supported by audit")
        data = validate(parse_json(read_file(args.input)))
        if args.command == "export":
            output = export_nt(data)
        else:
            report = audit(data)
            if args.tamandua:
                report["tamandua"] = reason(export_nt(data), args.tamandua.resolve())
            output = (
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            )
        if args.output:
            # Exclusive creation prevents truncation of inputs and existing results.
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(output)
        else:
            sys.stdout.write(output)
        return 0
    except (AuditError, OSError) as exc:
        print(
            json.dumps({"error": {"code": "AUDIT_FAILED", "message": str(exc)}}),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
