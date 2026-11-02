# Features

Implemented: JSON schema 1.0; duplicate-key/type/id/reference validation; 1 MiB and 1,000-node limits; exact Unicode quotes; unsupported claims; deterministic JSON/hashes; N-Triples; exclusive output creation; optional pinned real Tamandua CLI.

Commands: armadillo audit INPUT [--output NEW_FILE] [--tamandua EXECUTABLE]; armadillo export INPUT [--output NEW_FILE]; armadillo --version.

Exit 0 means valid analysis/export including REVIEW_REQUIRED; exit 1 means input/runtime/integration error; argparse exit 2 means invocation error. No HTTP API, scoring, extraction, randomization, persistent storage or required environment variables.

Current hardening adds report schema 1.1 with source quotes/locations/context, Markdown output, offline schema export and bounded/validated optional integration. Commands additionally accept `--format markdown` and `--timeout SECONDS`; `armadillo schema input|report|adapter` exports bundled schemas. Install the optional parser with `pip install ".[tamandua]"`; standalone remains dependency-free. See testing/HARDENING_RESULTS.md.
