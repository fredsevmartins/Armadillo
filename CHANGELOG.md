# Changelog

## 0.1.0 — unreleased

Original manual source-evidence auditing, deterministic provenance, RDF export and optional actual Tamandua CLI adapter. Strict validation, preserved inputs, standalone/real tests, tutorials, diagrams and CI definition. Baseline contained only project name. No release published.

## Unreleased hardening (report/adapter contract 1.1)

- Validate returned assertion correspondence, RDF set/provenance invariants and integration input limits using optional pinned RDFLib parsing.
- Bound both process streams while reading; retain safe diagnostics and clean process groups on failure.
- Publish new reports atomically; remove unpublished files on write errors and preserve collisions.
- Reject numeric exponent overflow. Add exact source locations/context and escaped Markdown reports.
- Bundle offline input/report/adapter schemas, representative fixtures and regression tests; define clean wheel/artifact CI checks.
