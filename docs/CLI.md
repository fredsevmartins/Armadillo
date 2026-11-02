# Command-line reference

Run `armadillo --help` for available options and `armadillo --version` for the installed package version. All commands operate locally; only installation/builds require package downloads.

| Command | Input | Purpose |
|---|---|---|
| prepare SOURCE.txt | UTF-8 .txt/.md | Create input schema 1.1 with empty nodes and source provenance |
| annotate INPUT.json | Valid schema 1.0/1.1 | Add, explicitly replace or delete a manual annotation |
| audit INPUT.json | Valid schema 1.0/1.1 | Produce report schema 1.2 |
| export INPUT.json | Valid schema 1.0/1.1 | Export standard N-Triples using snapshot identity |
| compare BEFORE.json --against AFTER.json | Same exact document | Produce comparison 1.1 and optional real graph impact |
| schema NAME | input, report, adapter, comparison, connection | Export a bundled JSON Schema offline |
| doctor | Explicit Tamandua selection | Verify a real local reasoning connection |

## Output

--output NEW_FILE atomically publishes a complete private file without replacing existing data. Without it, results go to stdout. audit/compare accept --format json (default) or --format markdown. prepare, annotate, schema and doctor return JSON; export returns N-Triples.

Do not redirect stdout over an input file: shell redirection happens before the application can protect it. Output publication requires same-filesystem hard-link support. It does not guarantee cleanup after SIGKILL or full directory durability across power loss.

## Preparation and editing

prepare accepts optional --document-id and --title. Source name/format/hash are recorded without absolute paths.

annotate requires --node-id and --author. For add/replace supply --kind claim|evidence, --start N and --end N; evidence may use --supports CLAIM_ID ... . --revision is an optional explicit label. On replacement, omitted --supports preserves existing links; --supports with no IDs explicitly clears them. Existing IDs require --replace; --replace cannot invent a missing ID. --delete accepts the ID and author without span/kind/support/revision options. It rejects dangling links. Existing input schema 1.0 is upgraded explicitly to 1.1 in the new output.

## Optional connection

audit, compare and doctor accept one of:

- --tamandua EXECUTABLE: a trusted separately installed binary.
- --tamandua-repo CHECKOUT: the verified independent source checkout.

These options are mutually exclusive. Checkout selection requires Git, the expected origin and pinned clean source revision, then finds target/release/tamandua or target/debug/tamandua. It does not build, clone, reset or modify a checkout. doctor runs an actual subclass-inference check. Binary selection alone cannot attest repository origin or build provenance.

--timeout SECONDS accepts a finite number in (0,300], default 30, per process. A comparison normally makes five engine processes; repository checks add local Git commands. It is not an overall wall-clock deadline. Integration requires POSIX.

## Exit and errors

| Exit | Meaning |
|---|---|
| 0 | Successful operation, including REVIEW_REQUIRED findings |
| 1 | Input, schema, option-combination, file or integration failure |
| 2 | argparse invocation error, such as unknown command/option or invalid argument type |

Application failures use stderr JSON with error.code AUDIT_FAILED and a useful message. Requested Tamandua failures do not silently downgrade to standalone; omit the option to run standalone explicitly.
