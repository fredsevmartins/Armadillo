# Interpretation, limits and support

## Meaning of results

SOURCE_LINKED is a source-presence/declared-link observation. REVIEW_REQUIRED identifies missing quotations, empty graphs or claims without source-present declared evidence. Neither is a truth value or document-quality grade.

No automated argument extraction, PDF ingestion, external fact checking, statistical calibration, scoring, OWL reasoning or causal inference is implemented. Annotation authors are caller-provided metadata, not verified identities. last_edit is a latest-edit record, not a complete signed history.

Selected spans are validated against exact source text. Reports show a bounded set of matching occurrences, not proof that repeated sentences are independent evidence. Markdown source is not rendered or fetched.

## Capacity and resource boundaries

| Boundary | Limit/behavior |
|---|---|
| Source/input JSON | Regular UTF-8 file, at most 1 MiB; entire canonical input also at most 1 MiB |
| Annotation graph | At most 1,000 nodes |
| Displayed matches | First ten overlapping matches per quote; explicit truncation |
| Context | At most 160 codepoints per displayed occurrence |
| Generated integration RDF | At most 2 MiB and 20,000 assertions before launch |
| Changes JSON | At most 2 MiB |
| Process capture | 16 MiB stdout and 64 KiB stderr, bounded during reading |
| Per-process timeout | Default 30 seconds, configurable (0,300] |
| Tamandua closure | Engine limits also apply, including 20,000 closure triples |

A valid standalone JSON graph can expand beyond integration limits. No graph is silently truncated; reduce links or run standalone. Preflight does not guarantee closure/computation limits will pass.

## Comparison and identity

Comparisons require exactly identical document text. Document-scoped node IDs are stable only within that document and rely on user-maintained node identity. Automatic correspondence across edited documents is not implemented. Default standalone RDF export remains snapshot-scoped.

## Platform and publication

Linux x86_64/Python 3.12 is locally verified. Python 3.11/3.13 are included in CI definitions but hosted execution must be confirmed. Integration subprocess capture requires POSIX. Native Windows integration and other standalone systems remain unverified.

Atomic output creation requires filesystem hard-link support. Handled failures remove unpublished temporary files; SIGKILL/power-loss cleanup and full directory durability are not guaranteed. The trusted engine has caller privileges; capture/timeout checks are not a sandbox.

Version 0.2.0 is unreleased. Hosted CI, package publication and a GitHub release require their own evidence and authorization.
