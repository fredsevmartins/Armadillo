# Installation

## Requirements and support

Python 3.11+ with venv and pip. Linux x86_64/Python 3.12 is locally verified. Standalone runtime has no third-party dependencies. Optional Tamandua integration requires POSIX, Git for checkout verification, its separate Rust build and the pinned RDF parser extra.

Version 0.2.0 is unreleased and has not been published to PyPI. The current code is on the implementation branch:

```bash
git clone --branch feat/reliable-evidence-reports https://github.com/fredsevmartins/Armadillo.git
cd Armadillo
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
armadillo --version
```

Expected version: 0.2.0. Use `python -m pip install -e .` instead for editable development. The build backend requires setuptools>=77. In the prepared managed environment, existing build tooling allows `--no-build-isolation`; normal installation should retain build isolation and TLS verification.

## Verify standalone operation

```bash
armadillo audit examples/tamandua_integration/input.json --format markdown
armadillo schema input
```

The synthetic audit has two nodes, one claim and no missing quote. SOURCE_LINKED describes quotation presence and declared support only.

Follow [quick start](QUICKSTART.md) to import text. No .env file, network service, API key or database is required.

## Optional Tamandua

```bash
python -m pip install '.[tamandua]'
```

This adds RDFLib 7.1.4 and pyparsing 3.3.2. Build and connect the independent checkout using the [connection guide](integrations/TAMANDUA.md). Armadillo never silently builds, resets or downloads Tamandua at runtime.

## Development checks

```bash
python -m pip install '.[tamandua]' ruff==0.14.3 jsonschema==4.26.0
python -m unittest discover -s tests -v
ruff check src tests scripts
ruff format --check src tests scripts
python scripts/check_docs.py
```

The real suite additionally needs the compatible Tamandua checkout/executable. The optional schema validator and Ruff are development tools, not standalone runtime dependencies.

## Managed cloud setup

scripts/setup.sh is specifically for /workspace/Armadillo and /workspace/Tamandua. It installs development dependencies, verifies the pinned source revision, builds Tamandua and executes the validation workflows. It is not the general standalone installer. Each task is already isolated: use existing checkouts and do not create worktrees unless explicitly requested.

## Troubleshooting

| Symptom | Action |
|---|---|
| Command not found | Activate the virtual environment or use .venv/bin/armadillo |
| Existing output destination | Choose a new filename; inputs and reports are never overwritten |
| PDF or non-UTF-8 input | Use UTF-8 .txt/.md; no silent conversion is performed |
| Invalid selected span | Count Unicode codepoints and use a nonempty [start,end) range |
| Source hash mismatch | Preserve the imported document; prepare a new snapshot for changed text |
| Missing optional parser | Install .[tamandua] in the same environment |
| Wrong or dirty Tamandua checkout | Use the verified clean revision without discarding local work |
| Engine not built | Run the documented locked Cargo build in Tamandua |
| Unsupported filesystem publication | Use a local filesystem supporting exclusive hard links |
| Hosted GitHub API Forbidden | Git reads/pushes do not prove API access; remote CI/PR status remains unverified |

No verification checks should be disabled to make installation succeed.
