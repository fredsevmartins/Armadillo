# Dependency inventory

## Application

Standalone preparation, manual annotation, audit, comparison, reporting and schema export use Python 3.11+ standard library modules. There are no required third-party runtime dependencies.

Optional tamandua extra:

| Package | Pin | License | Purpose |
|---|---|---|---|
| RDFLib | 7.1.4 | BSD-3-Clause | Parse local N-Triples and compare submitted/returned RDF term sets |
| pyparsing | 3.3.2 | MIT | RDFLib dependency, pinned for reproducibility |

requirements-integration.txt records the same optional pins. Dependencies are separately installed, not vendored or relicensed. Their original notices and licenses remain applicable.

## Independent Tamandua

Source repository: https://github.com/fredsevmartins/Tamandua. MIT-licensed pinned commit 09970fb8985e6065cc24ff5507a8de161c301ee9, package 0.1.0, tested Rust 1.90.0. Its own Cargo.lock and licenses govern its dependencies. Armadillo does not depend on separate DominoX code or reference-project source/data/assets.

## Development tools

Ruff 0.14.3, jsonschema 4.26.0, setuptools 84.0.0 and wheel 0.48.0 are the managed setup's tested tools; the general build backend permits setuptools>=77. Git is needed for source checkout diagnostics. Rust/Cargo are needed only to build/test Tamandua.

pip-audit 2.9.0 was used to query the two optional parser pins. The recorded result found no known vulnerabilities at execution time; it is not a complete application, build-tool or Rust security certification. See [historical scanner evidence](testing/parser-audit.json).

Optional documentation syntax tooling uses Mermaid 11.4.1 and JSDOM 26.1.0 in a temporary external npm prefix. They are not runtime/package dependencies and were not included in the Python parser advisory scan.
