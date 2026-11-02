# Installation

Python 3.11+, venv and pip. Zero runtime dependencies, services or credentials. Linux x86_64/Python 3.12.14 verified; other systems not locally tested.

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
armadillo --version
armadillo audit examples/tamandua_integration/input.json
python -m unittest discover -s tests -v
```

Use pip install -e . for development. Build backend requires setuptools>=77; normal pip build isolation installs it. Managed environment offline installation uses existing setuptools 84.0.0 and wheel 0.48.0 with --no-build-isolation. Ruff 0.14.3 is optional development tooling. [Tamandua tutorial](TAMANDUA_TUTORIAL.md) covers the optional engine.

Verification: version 0.1.0, SOURCE_LINKED example, two nodes, one claim. REVIEW_REQUIRED is a successful finding. JSON error diagnostics go to stderr; choose a new output filename if one exists. Check Python/setuptools versions on build failure; never bypass TLS/checksums. Omit --tamandua if only standalone analysis is needed.

## Optional integration dependencies and cloud helper

Install the optional parser with `python -m pip install ".[tamandua]"`. RDFLib 7.1.4 and pyparsing 3.3.2 are pinned; the standalone runtime remains dependency-free. Install these extras before running the full test suite, which includes protocol tests. `scripts/setup.sh` is specifically for the managed /workspace cloud layout and builds the independent Tamandua checkout; it is not the standalone installer. Integration is currently POSIX-only.

Offline schemas are bundled in the wheel: run `armadillo schema report`. Report 1.1 adds quote locations/context; input stays 1.0.
