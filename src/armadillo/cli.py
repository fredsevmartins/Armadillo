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
from .documents import prepare, annotate, serialize_input
from .connection import resolve, doctor


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit source evidence without a network service"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "command",
        choices=(
            "audit",
            "export",
            "schema",
            "compare",
            "prepare",
            "annotate",
            "doctor",
        ),
    )
    parser.add_argument("input", type=Path, nargs="?")
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
    parser.add_argument(
        "--tamandua-repo",
        type=Path,
        help="Verified independent Tamandua source checkout",
    )
    parser.add_argument("--document-id")
    parser.add_argument("--title")
    parser.add_argument("--node-id")
    parser.add_argument(
        "--author", help="Explicit author or reviewer alias for this annotation"
    )
    parser.add_argument("--revision")
    parser.add_argument("--kind", choices=("claim", "evidence"))
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--supports", nargs="*")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 300:
            raise AuditError("timeout must be in (0, 300] seconds")
        if args.command != "doctor" and args.input is None:
            raise AuditError("This command requires an input path or schema name")
        if args.command == "doctor" and (
            args.input is not None or args.format != "json"
        ):
            raise AuditError("doctor accepts no input file and returns JSON")
        if (
            any(v is not None for v in (args.document_id, args.title))
            and args.command != "prepare"
        ):
            raise AuditError("--document-id and --title are only supported by prepare")
        if (
            any(
                v is not None
                for v in (
                    args.node_id,
                    args.author,
                    args.revision,
                    args.kind,
                    args.start,
                    args.end,
                    args.supports,
                )
            )
            or args.replace
            or args.delete
        ) and args.command != "annotate":
            raise AuditError(
                "Annotation editing options are only supported by annotate"
            )
        if args.command in ("prepare", "annotate", "schema", "export") and (
            args.tamandua or args.tamandua_repo
        ):
            raise AuditError(
                "Tamandua options are supported by audit, compare and doctor"
            )
        if args.command in ("prepare", "annotate") and args.format != "json":
            raise AuditError(
                "prepare and annotate produce JSON inputs; audit them for Markdown reports"
            )
        if args.against is not None and args.command != "compare":
            raise AuditError("--against is only supported by compare")
        if args.command == "export" and (args.tamandua or args.format != "json"):
            raise AuditError(
                "--tamandua and --format markdown are only supported by audit"
            )
        if args.command == "doctor":
            output = (
                json.dumps(
                    doctor(args.tamandua, args.tamandua_repo, args.timeout),
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            )
        elif args.command == "prepare":
            output = serialize_input(prepare(args.input, args.document_id, args.title))
        elif args.command == "annotate":
            if args.node_id is None:
                raise AuditError("annotate requires --node-id")
            data = parse_json(read_file(args.input))
            result = annotate(
                data,
                args.node_id,
                args.author,
                args.kind,
                args.start,
                args.end,
                args.supports,
                args.revision,
                args.replace,
                args.delete,
            )
            output = serialize_input(result)
        elif args.command == "compare":
            if args.against is None:
                raise AuditError("compare requires --against PROPOSED.json")
            before = parse_json(read_file(args.input))
            after = parse_json(read_file(args.against))
            report = compare(
                before,
                after,
                resolve(args.tamandua, args.tamandua_repo, args.timeout),
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
            binary = resolve(args.tamandua, args.tamandua_repo, args.timeout)
            if binary:
                report["tamandua"] = reason(export_nt(data), binary, args.timeout)
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
