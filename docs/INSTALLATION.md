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
