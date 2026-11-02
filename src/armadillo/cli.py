"""CLI with exclusive output creation and structured errors."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import AuditError, audit, parse_json, read_file, validate
from .rdf import export_nt
from .tamandua import reason
from .output import markdown, write_new
from .contracts import load_schema
from .compare import compare, markdown as comparison_markdown


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit source evidence without a network service"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("command", choices=("audit", "export", "schema", "compare"))
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--against", type=Path, help="Proposed annotation JSON for compare"
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--timeout",
        type=float,
        default=30,
        help="Tamandua timeout per process, in (0, 300] seconds",
    )
    parser.add_argument(
        "--tamandua", type=Path, help="Explicit trusted Tamandua executable"
    )
    args = parser.parse_args(argv)
    try:
        if args.against is not None and args.command != "compare":
            raise AuditError("--against is only supported by compare")
        if args.command == "export" and (args.tamandua or args.format != "json"):
            raise AuditError(
                "--tamandua and --format markdown are only supported by audit"
            )
        if args.command == "compare":
            if args.against is None:
                raise AuditError("compare requires --against PROPOSED.json")
            before = parse_json(read_file(args.input))
            after = parse_json(read_file(args.against))
            report = compare(
                before,
                after,
                args.tamandua.resolve() if args.tamandua else None,
                args.timeout,
            )
            output = (
                comparison_markdown(report)
                if args.format == "markdown"
                else json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)
                + "\n"
            )
        elif args.command == "schema":
            if args.tamandua or args.format != "json":
                raise AuditError("Schema export only supports JSON without Tamandua")
            output = json.dumps(load_schema(str(args.input)), indent=2) + "\n"
        elif args.command == "export":
            data = validate(parse_json(read_file(args.input)))
            output = export_nt(data)
        else:
            data = validate(parse_json(read_file(args.input)))
            report = audit(data)
            if args.tamandua:
                report["tamandua"] = reason(
                    export_nt(data), args.tamandua.resolve(), args.timeout
                )
            output = (
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            )
            if args.format == "markdown":
                output = markdown(report)
        if args.output:
            write_new(args.output, output)
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
