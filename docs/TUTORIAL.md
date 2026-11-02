# Source-evidence tutorial

Install using [installation](INSTALLATION.md). Commands run from the repository root.

1. Read examples/tamandua_integration/input.json: synthetic document, claim sentence and evidence sentence linked to claim1. The embedded document has no hidden filesystem dependency.
2. Run armadillo audit examples/tamandua_integration/input.json. Inspect SOURCE_LINKED, counts, hashes, quote_found and source_present_supporters.
3. Add --output audit-result.json to create a new report. Existing destinations are refused.
4. Copy the example and replace the evidence quote with "A fabricated sentence". Audit that copy: expected REVIEW_REQUIRED, missing_quotes 1 and unsupported_claims ["claim1"]. Keep original inputs unchanged.
5. Run armadillo export examples/tamandua_integration/input.json --output argument.nt. Inspect standard N-Triples.
6. Follow [Tamandua tutorial](TAMANDUA_TUTORIAL.md) for optional actual inference.

Matching is case/whitespace/codepoint-sensitive. Location uniqueness and semantic relevance are not checked. Repeated sentences do not establish independent evidence. No numeric units or scores are transformed.

## Inspect source positions and Markdown

Run `armadillo audit examples/tamandua_integration/input.json --format markdown`. Quote locations use Unicode codepoints rather than UTF-8 bytes, zero-based [start,end) ranges and one-based lines/columns. At most ten overlapping matches are displayed, with explicit truncation. Save with `--output NEW_REPORT.md`; filesystem hard links must be supported.

Additional labeled fixtures live in examples/audit_cases. They wrap the executable JSON as `input` alongside expected audit findings; use Python json.load to write that input object to a new file before running the CLI. Contradictory user-labeled support deliberately remains a source-presence finding, not semantic approval.
