# Developer guide

## Layout

src/armadillo contains documents (preparation/editing), core (validation/audit), rdf (serialization), compare (annotation/graph impact), connection (checkout diagnostic), tamandua/process (validated optional exchange/bounded capture), output (atomic publication/Markdown), contracts and cli.

schemas contains public JSON Schemas; identical package resources are shipped in src/armadillo/schemas. tests verifies their consistency. examples contains original synthetic workflows. docs separates current instructions from historical audits/results.

## Environment and checks

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[tamandua]' ruff==0.14.3 jsonschema==4.26.0
python -m unittest discover -s tests -v
python tests/real_tamandua.py -v
python scripts/check_contracts.py --tamandua ../Tamandua/target/debug/tamandua
ruff check src tests scripts
ruff format --check src tests scripts
python scripts/check_docs.py
```

The full standalone suite includes optional-parser protocol tests; install the extra for development even though the standalone application does not require it. The real suite requires the compatible source checkout/binary; absence must fail rather than silently skip. Override test locations with TAMANDUA_BINARY and TAMANDUA_REPOSITORY only when needed.

The managed setup script uses /workspace paths and retained tool directories. Each cloud task is already isolated: use existing checkouts; do not create worktrees unless explicitly requested.

## Extension rules

Preserve original input objects/files, deterministic hashes and explicit failure behavior. Never automatically normalize source text, delete user support links, change IDs across edited documents, infer a reviewer identity or downgrade requested integration failures. Metadata is caller-supplied, not authenticated.

New input/report fields must have explicit contract decisions, bundled schema updates and representative tests. New engine revisions require actual tests and a deliberate compatibility-pin update. Do not use mocks as proof of working integration or scientific accuracy.

## Packaging

Build with python -m pip wheel --no-deps . --wheel-dir NEW_ARTIFACT_DIRECTORY. Test the wheel in a clean virtual environment outside the checkout; verify version, bundled schemas and standalone document workflow. Install its optional extra and test the actual reasoner separately. CI defines these activities and artifact uploads, but hosted execution needs independent evidence.

Use [release checklist](RELEASE_CHECKLIST.md), [security policy](../SECURITY.md) and [contributing](../CONTRIBUTING.md).

## Diagram syntax

Development-only optional tools are installed outside the project:

```bash
npm install --prefix /tmp/armadillo-doc-tools --ignore-scripts --no-audit --no-fund mermaid@11.4.1 jsdom@26.1.0
node scripts/check_mermaid.mjs /tmp/armadillo-doc-tools/node_modules
```

This checks actual Mermaid syntax with a DOM for sanitization. It does not prove browser rendering or layout quality. No JavaScript packages are required by the Python application. `python scripts/check_quickstart.py` executes the documented CLI workflow in a temporary output directory; add --tamandua-repo PATH for the actual repository connection.
