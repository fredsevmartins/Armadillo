# Armadillo

Armadillo helps reviewers trace manually annotated claims and evidence back to the exact text of a document. Import a UTF-8 text or Markdown file, annotate source spans, inspect a reproducible report, and optionally use [Tamandua](https://github.com/fredsevmartins/Tamandua) to explain graph changes.

**Development version: 0.2.0, unreleased.** Current improvements are on `feat/reliable-evidence-reports`; they are not yet merged into `main`. Source presence and declared support do not establish truth, causality or scientific validity.

[Documentation](docs/README.md) · [Quick start](docs/QUICKSTART.md) · [Tamandua connection](docs/integrations/TAMANDUA.md) · [CLI reference](docs/CLI.md) · [Validation](docs/testing/DOCUMENT_WORKFLOW_RESULTS.md)

## What works

- Import .txt and .md without normalizing Unicode, markup or line endings.
- Add, explicitly replace or delete annotations using source offsets and a reviewer alias.
- Preserve source hashes, selected spans, annotation authors/revisions and the most recent edit.
- Audit exact quote presence and declared evidence links; export JSON, Markdown and N-Triples.
- Compare annotations of the same document with stable document-scoped graph identities.
- Connect explicitly to the independent Tamandua checkout for real closure, impact plans and explanations.
- Refuse output collisions and publish complete files atomically.
- Export bundled JSON Schemas offline.

## Install from this development checkout

Python 3.11+ is required. Standalone auditing has no third-party runtime dependencies.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
armadillo --version
```

For a fresh clone of the current development work, see [installation](docs/INSTALLATION.md).

## Document to review

Run from the repository root. Choose new output filenames on every run.

```bash
armadillo prepare examples/document_workflow/source.txt --document-id synthetic-sample --output prepared.json
armadillo annotate prepared.json --node-id claim1 --kind claim --start 0 --end 42 --author reviewer-a --output claims.json
armadillo annotate claims.json --node-id evidence1 --kind evidence --start 43 --end 79 --supports claim1 --author reviewer-b --output annotated.json
armadillo audit annotated.json --format markdown --output review.md
armadillo compare claims.json --against annotated.json --format markdown
```

Expected final audit: SOURCE_LINKED with two source-present quotations. The comparison identifies the new evidence and gained declared support. Positions count Unicode codepoints, with zero-based [start,end) ranges; the text is not converted to byte offsets or normalized.

## Connect Tamandua

Build the separately maintained [compatible checkout](docs/integrations/TAMANDUA.md), then:

```bash
python -m pip install '.[tamandua]'
armadillo doctor --tamandua-repo ../Tamandua
armadillo audit annotated.json --tamandua-repo ../Tamandua --format markdown
armadillo compare claims.json --against annotated.json --tamandua-repo ../Tamandua --format markdown
```

The diagnostic checks the selected repository, pinned source revision and an actual RDFS subclass inference. No HTTP server, API key, database or separate DominoX project is required. Neither project installs or imports the other's application code.

## Verify

```bash
python -m pip install '.[tamandua]' ruff==0.14.3 jsonschema==4.26.0
python -m unittest discover -s tests -v
python tests/real_tamandua.py -v
python scripts/check_docs.py
python scripts/check_contracts.py --tamandua ../Tamandua/target/debug/tamandua
```

The real suite requires the pinned source checkout and executable; missing integration prerequisites fail explicitly. Local results are not proof of hosted CI execution. See [current results](docs/testing/DOCUMENT_WORKFLOW_RESULTS.md).

## Boundaries

Armadillo currently handles manual evidence traceability. It does not extract arguments automatically, read PDFs, score document quality, fact-check external sources or validate scientific conclusions. Contradictory user-labeled evidence can still be source-present. Comparisons require identical document text. Annotation authors are caller-provided labels, not authenticated identities; preserve prior JSON snapshots for history.

Linux/Python 3.12 is locally verified. Tamandua process integration requires POSIX; other standalone platforms remain unverified. Inputs are limited to 1 MiB including serialized metadata and 1,000 nodes. See [limits](docs/LIMITATIONS.md) and [security](SECURITY.md).

## Open source

Original implementation: MIT © 2026 Armadillo contributors. [License](LICENSE) · [Contributing](CONTRIBUTING.md) · [Conduct](CODE_OF_CONDUCT.md) · [Changelog](CHANGELOG.md).

Technical inspiration: [Brain in the Fish](https://github.com/fabio-rovai/brain-in-the-fish), MIT © 2026 Fabio Rovai. No reference source, datasets, documentation or assets were copied. Tamandua is independently maintained and MIT-licensed. These are personal open-source projects, not Kinetix products.
