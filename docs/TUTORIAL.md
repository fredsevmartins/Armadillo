# Reviewing documents with source annotations

Start with the executable [quick start](QUICKSTART.md). The included source is synthetic, MIT-licensed and contains no private data or real scientific finding.

## Source integrity

prepare accepts UTF-8 .txt and .md files. It preserves BOMs, CRLF/LF endings, whitespace, markup and Unicode codepoints. Markdown is imported as source text, not rendered or interpreted. Links, images and embedded HTML are never fetched.

The source SHA-256 must match the embedded document. Changing the document while keeping stale provenance fails validation. Create a new prepared snapshot for edited documents. The 1 MiB limit applies to the entire serialized input, including annotations/metadata; a source near that limit may leave insufficient room for annotations.

## Span selection

annotate takes explicit [start,end) codepoint offsets. A fish emoji counts as one Python Unicode codepoint, not four UTF-8 bytes; combining marks remain separate codepoints. Blank or out-of-range selections fail. The selected span is retained in annotation metadata and must still exactly identify the quote.

Reports list up to ten overlapping occurrences with bounded context. That list describes all displayed matches, while annotation.start/end identifies the user's selected occurrence. No normalization or relevance inference occurs.

## Revisions and removals

Adding an existing ID fails. Use --replace to explicitly replace an existing annotation and provide its new selection and kind. Omitted --supports preserves existing links; provide --supports with no IDs to clear links explicitly:

```bash
armadillo annotate annotated.json --node-id evidence1 --kind evidence --start 43 --end 79 --supports claim1 --author reviewer-c --revision round-2 --replace --output revised.json
armadillo annotate revised.json --node-id evidence1 --author reviewer-c --delete --output without-evidence.json
armadillo compare revised.json --against without-evidence.json --format markdown
```

The removal produces REVIEW_REQUIRED for claim1 because its declared source-present supporter is gone. Deleting a claim still referenced by evidence is rejected; revise those links explicitly first. Links are never silently discarded.

Author/revision values are caller-provided labels, not authenticated identities. last_edit records the latest edit only. Keep each JSON snapshot and use version control for full history; Armadillo is not a signed journal, database or collaboration server.

## Interpret the report

SOURCE_LINKED requires a nonempty graph, present quotes and source-present declared evidence for every claim. REVIEW_REQUIRED identifies an empty graph, absent quote or unsupported claim. Both are valid audit outcomes, with exit 0. Input/runtime failures return exit 1.

A contradictory evidence sentence can still be source-present. Repeated text is not independent evidence. Absence from the annotation graph is not proof of falsity. No score, statistical unit conversion, causal inference or scientific validation is performed.

## Export and optional reasoning

Use `armadillo export annotated.json --output graph.nt` for standard N-Triples. The standalone export uses snapshot identities. Same-document comparison uses explicit document-scoped identities so unchanged nodes survive annotation edits.

Use [Tamandua integration](TAMANDUA_TUTORIAL.md) for actual closure, impact sets and direct explanation paths. Keep JSON reports for complete analytical details; Markdown prioritizes human review.
