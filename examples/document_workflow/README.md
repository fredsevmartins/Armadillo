# Import and annotate a synthetic source

This original synthetic text is MIT-licensed and represents no real research result. Run from the repository root with Armadillo installed. Each output must be new; the source is never modified.

```bash
armadillo prepare examples/document_workflow/source.txt --document-id synthetic-sample --title "Synthetic source" --output prepared.json
armadillo annotate prepared.json --node-id claim1 --kind claim --start 0 --end 42 --author reviewer-a --revision round-1 --output claims.json
armadillo annotate claims.json --node-id evidence1 --kind evidence --start 43 --end 79 --supports claim1 --author reviewer-b --revision round-1 --output annotated.json
armadillo audit annotated.json --format markdown --output source-audit.md
armadillo compare claims.json --against annotated.json --format markdown
```

For actual Tamandua reasoning install the optional extra, build the independent pinned checkout, then run:

```bash
armadillo doctor --tamandua-repo ../Tamandua
armadillo audit annotated.json --tamandua-repo ../Tamandua --format markdown
armadillo compare claims.json --against annotated.json --tamandua-repo ../Tamandua --format markdown
```

Expected final audit: SOURCE_LINKED, two source-present nodes. Comparison adds evidence1, gains its declared support for claim1, adds four RDF assertions and one inferred class membership. Presence is not verification of the claim's truth.

Offsets count Unicode codepoints, not bytes. Markdown import preserves markup rather than rendering it. Retain previous JSON files to preserve edit history; last_edit records only the most recent explicit edit and is not an authenticated identity or signed audit log.
