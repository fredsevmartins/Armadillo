# Quick start

Install Armadillo and activate its virtual environment as described in [installation](INSTALLATION.md). Run commands from the repository root. Each destination below must be new.

## 1. Import unchanged source text

```bash
armadillo prepare examples/document_workflow/source.txt --document-id synthetic-sample --title "Synthetic source" --output prepared.json
```

The source is copied into input schema 1.1 without newline, Unicode or Markdown normalization. Provenance records its basename, format and SHA-256; no absolute path or inferred author is stored.

## 2. Add a claim

```bash
armadillo annotate prepared.json --node-id claim1 --kind claim --start 0 --end 42 --author reviewer-a --revision round-1 --output claims.json
```

The selected quote is exactly "The synthetic sample contains three items." Offsets are zero-based Unicode codepoints with the end excluded. Node IDs are user-maintained identities, not automatically generated semantic matches.

## 3. Add declared evidence

```bash
armadillo annotate claims.json --node-id evidence1 --kind evidence --start 43 --end 79 --supports claim1 --author reviewer-b --revision round-1 --output annotated.json
```

This explicitly labels "A manual count recorded three items." as supporting claim1. Armadillo checks the source span and link structure; it does not decide that the evidence proves the claim.

## 4. Review and compare

```bash
armadillo audit annotated.json --format markdown --output review.md
armadillo compare claims.json --against annotated.json --format markdown
```

Expected audit: SOURCE_LINKED, two source-present quotations. The comparison reports evidence1 added and gained declared support for claim1. Previous JSON snapshots remain unchanged.

## 5. Connect the optional reasoner

After building the [independent Tamandua checkout](integrations/TAMANDUA.md):

```bash
python -m pip install '.[tamandua]'
armadillo doctor --tamandua-repo ../Tamandua
armadillo audit annotated.json --tamandua-repo ../Tamandua --format markdown
armadillo compare claims.json --against annotated.json --tamandua-repo ../Tamandua --format markdown
```

The diagnostic must report CONNECTED after a real subclass inference. In the comparison, Tamandua adds four graph assertions and one class-membership inference. This is graph reasoning, not scientific truth validation.

See the [tutorial](TUTORIAL.md) for replacements, deletions and history, and the [CLI reference](CLI.md) for all commands.
