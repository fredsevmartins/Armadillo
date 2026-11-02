# Reliability and report implementation results

First-phase evidence. Current functionality and counts are in [DOCUMENT_WORKFLOW_RESULTS.md](DOCUMENT_WORKFLOW_RESULTS.md).

Date: 2026-11-02. Branch: feat/reliable-evidence-reports. Baseline: fc8a966b7f71bb9d5aef6c0dcb5db884549d3b11. This is an unreleased continuation of the evidence-traceability MVP, not automated scientific evaluation.

## Implemented

- Optional pinned RDFLib 7.1.4 / pyparsing 3.3.2 parser for N-Triples preflight and submitted/returned assertion correspondence. Standalone runtime still has no third-party dependencies.
- Rejection of duplicate triples, asserted/inferred overlap, unknown provenance rules, unknown premise/conclusion references and absent inference provenance. Blank-node labels stay stable within an exchange.
- Integration preflight at 2 MiB RDF and 20,000 assertions before process launch. These do not guarantee closure/computation budgets; engine errors retain bounded safe diagnostics.
- POSIX subprocess capture bounded while reading: 16 MiB stdout and 64 KiB stderr; timeout/overflow failures clean the process group. Trusted executable configuration remains necessary.
- Complete report publication through same-directory private temporary file, flush/fsync and exclusive atomic hard-link creation. No overwrites; handled partial-write, flush and publication failures remove unpublished temporary files. Hard-link filesystem support is required. No power-loss or SIGKILL cleanup guarantee is made.
- Finite JSON numeric exponent validation.
- Report schema 1.1: quotes, up to ten overlapping Unicode-codepoint match ranges and bounded context, one-based lines/columns and explicit truncation flags. Missing quotes have no locations. Existing input schema remains 1.0; adapter contract is 1.1.
- Escaped Markdown reports via --format markdown; validated adapter timeout via --timeout; offline schema export via armadillo schema input/report/adapter.
- Three bundled JSON Schemas, representative synthetic fixtures, post-merge tutorial corrections, CI artifact uploads and clean standalone wheel checks.

## Executed verification

| Command / check | Outcome |
|---|---|
| python -m unittest discover -s tests -v | PASS: 44 tests, zero failed/skipped |
| python tests/real_tamandua.py -v | PASS: 7 actual-engine tests, zero failed/skipped |
| Ruff check and format --check | PASS locally |
| python scripts/check_contracts.py --tamandua /workspace/Tamandua/target/debug/tamandua | PASS: 3 schemas and 5 input/report workflows, including actual adapter data |
| Editable package installation and wheel build | PASS |
| Clean standalone wheel install outside checkout, Markdown audit and offline schema export | PASS |
| pip check | PASS |
| pip-audit -r requirements-integration.txt --no-deps --disable-pip --progress-spinner off --format json | PASS: rdflib 7.1.4 and pyparsing 3.3.2, zero known vulnerabilities returned |

There are 51 unique unit/protocol/process/CLI/real-engine test methods; subtests and schema workflow checks are not counted as extra methods. Existing original tests were retained and updated for the new process boundary and earlier RDF preflight. Initial failures during development were old mock targets and an outdated expected error string; they were corrected to test the actual new boundary. No assertions or required checks were disabled.

The optional-parser audit checked exactly the two pinned integration packages against the service available at execution time, not the entire development environment, Rust engine dependencies or an absence of all security defects. No scientific accuracy or coverage percentage is claimed.

## Representative workflows

examples/audit_cases contains original synthetic data plus independently specified expected statuses:

- multiple-claims: one declared source-supported claim, one unsupported claim → REVIEW_REQUIRED.
- missing-evidence: fabricated quote absent from document → REVIEW_REQUIRED.
- unicode-repeated: two occurrences of an astral-Unicode quote → SOURCE_LINKED under the documented presence contract.
- contradictory-label: a manually declared supporter contradicts the claim → SOURCE_LINKED because both quotations occur. This deliberately demonstrates that semantic support/truth is not evaluated.

The fixture files wrap input and expected assertions; extract the input object before passing them to the CLI. The original examples/tamandua_integration/input.json remains directly executable.

## Performance

Current 500-node synthetic benchmark, Python 3.12.14 on Linux x86_64, one warmup and 20 timed audits with tracemalloc: median 0.024290579 seconds, minimum 0.020143737, maximum 0.030658115, peak tracked Python allocations 702,772 bytes. This now includes source-location/context generation and is not equivalent work to the earlier report-only benchmark. No comparative scientific or optimization claim follows.

## Delivery and remaining limits

Implementation remains on feat/reliable-evidence-reports for review; this report does not claim a merge or release. CI definitions are improved but hosted results require actual GitHub evidence. The previous API attempts returned Forbidden; local tests are not remote CI confirmation. Mermaid source rendering, native Windows integration, Rust advisory scanning, cross-Python hosted execution and external distribution publication remain unverified.

This first hardening phase does not add LLM extraction, PDF ingestion, grading or truth validation. Subsequent same-document stable identities and actual impact planning are documented in [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md). Those are separate product work. Source-present labels and declared support remain deliberately transparent. Review and explicitly approve release publication separately.
