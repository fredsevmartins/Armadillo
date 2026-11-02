# Armadillo

Armadillo checks whether manually annotated claims and evidence quote an original document, produces reproducible reports, and optionally sends the argument graph to Tamandua for explainable RDF reasoning. It runs locally without AI credentials, databases or network services.

This independent implementation follows the traceability objective of Brain in the Fish. It does not reproduce automated extraction, learned scoring, OWL reasoning or scientific performance claims.

## Capabilities

Strict versioned JSON, exact Unicode substring matching, validated evidence links, missing-quote and unsupported-claim findings, SHA-256 provenance, deterministic JSON/N-Triples and optional real Tamandua CLI integration. New reports are published atomically without overwriting existing files; write failures remove unpublished temporary files.

SOURCE_LINKED means all supplied quotes occur in the document and each claim has a declared evidence supporter whose quote occurs. It does **not** establish truth, entailment, source independence, quality or scientific validity. Other valid inputs produce REVIEW_REQUIRED.

## Installation and quick start

Python 3.11+; no runtime dependencies. From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
armadillo audit examples/tamandua_integration/input.json
armadillo audit examples/tamandua_integration/input.json --format markdown
armadillo export examples/tamandua_integration/input.json
```

Expected audit: SOURCE_LINKED, two nodes, one claim, zero missing quotes. Use --output NEW_FILE to retain a report. Never redirect stdout over an input.

## Architecture and Tamandua

JSON → validation → exact-quote audit → report. Optional branch: N-Triples → Tamandua CLI → analytical closure/provenance. Integration never changes the audit verdict.

```bash
python -m pip install '.[tamandua]'
armadillo audit examples/tamandua_integration/input.json --tamandua ../Tamandua/target/debug/tamandua
```

Build the pinned compatible binary using the [Tamandua tutorial](docs/TAMANDUA_TUTORIAL.md). No HTTP server is needed. See [architecture](docs/architecture/INTEGRATION_ARCHITECTURE.md), [contract](docs/integrations/INTERFACE_CONTRACT.md) and [diagrams](docs/diagrams/README.md).

## Reports and offline schemas

Report schema 1.1 includes original quotes, up to ten overlapping match locations with bounded context, zero-based Unicode codepoint ranges [start,end), and one-based lines/columns. Occurrences beyond ten are explicitly marked truncated. Use `--format markdown` for a reviewable report and `--output NEW_FILE` to retain it. No claim/evidence labels or source text are transformed.

`armadillo schema input`, `armadillo schema report` and `armadillo schema adapter` export bundled schemas offline. Input schema remains 1.0; the optional adapter contract is now 1.1. See [hardening validation](docs/testing/HARDENING_RESULTS.md) for current evidence.

## Tests and documentation

```bash
python -m pip install '.[tamandua]' ruff==0.14.3
python -m unittest discover -s tests -v
python scripts/check_docs.py
python tests/real_tamandua.py -v
```

The last suite requires the actual compatible binary and fails if missing. Mock protocol tests are separate and do not prove real integration. See [test results](docs/testing/TEST_RESULTS.md), [installation](docs/INSTALLATION.md), [user tutorial](docs/TUTORIAL.md), [developer guide](docs/DEVELOPER_GUIDE.md), [features](docs/FEATURES.md) and [roadmap](docs/ROADMAP.md).

## Limitations

Manual UTF-8 JSON only, bounded to 1 MiB and 1,000 nodes. No PDF reader, LLM extraction, grading, web fact checking, HTTP API or UI. Matching performs no whitespace/Unicode normalization. Support relationships are user assertions, not semantic proof. Tamandua implements a bounded RDFS subset, not OWL or scientific causation. Linux/Python 3.12 is locally verified; other declared CI versions await execution.

## Open source

MIT © 2026 Armadillo contributors; [license](LICENSE), [contributing](CONTRIBUTING.md), [conduct](CODE_OF_CONDUCT.md), [security](SECURITY.md).

Technical inspiration: [Brain in the Fish](https://github.com/fabio-rovai/brain-in-the-fish), MIT © 2026 Fabio Rovai. No reference source, datasets, documentation or assets were copied. [Tamandua](https://github.com/fredsevmartins/Tamandua), MIT © 2026 Tamandua contributors, is separately installed and optional. These are independent personal projects, not Kinetix products.

## Compare annotations and trace graph impact

```bash
armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --format markdown
# Optional: install .[tamandua] and build the compatible engine first
armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --tamandua ../Tamandua/target/debug/tamandua --format markdown
```

Compare node additions/removals/modifications and lost/gained declared source supporters without changing inputs. Optional Tamandua impact uses stable identities within the same unchanged document and verifies the proposed graph and impact sets. Changed document text is explicitly rejected. This does not assess scientific truth or causal evidence. See the [comparison tutorial and contract](docs/integrations/ANNOTATION_COMPARISON.md) and [current test results](docs/testing/COMPARISON_RESULTS.md). Offline schema: `armadillo schema comparison`.
