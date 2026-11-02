# Source-evidence tutorial

Install using [installation](INSTALLATION.md). Commands run from the repository root.

1. Read examples/tamandua_integration/input.json: synthetic document, claim sentence and evidence sentence linked to claim1. The embedded document has no hidden filesystem dependency.
2. Run armadillo audit examples/tamandua_integration/input.json. Inspect SOURCE_LINKED, counts, hashes, quote_found and source_present_supporters.
3. Add --output audit-result.json to create a new report. Existing destinations are refused.
4. Copy the example and replace the evidence quote with "A fabricated sentence". Audit that copy: expected REVIEW_REQUIRED, missing_quotes 1 and unsupported_claims ["claim1"]. Keep original inputs unchanged.
5. Run armadillo export examples/tamandua_integration/input.json --output argument.nt. Inspect standard N-Triples.
6. Follow [Tamandua tutorial](TAMANDUA_TUTORIAL.md) for optional actual inference.

Matching is case/whitespace/codepoint-sensitive. Location uniqueness and semantic relevance are not checked. Repeated sentences do not establish independent evidence. No numeric units or scores are transformed.
