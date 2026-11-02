# Tamandua tutorial

Executed against the actual pinned engine. Use existing sibling checkouts where available and preserve local work; no Git worktrees are needed.

## Install both projects

```bash
git clone https://github.com/fredsevmartins/Armadillo.git
git clone https://github.com/fredsevmartins/Tamandua.git
git -C Tamandua checkout 09970fb8985e6065cc24ff5507a8de161c301ee9
rustup toolchain install 1.90.0 --profile minimal
cd Tamandua
cargo +1.90.0 test --locked --workspace -j 4
cargo +1.90.0 build --locked --bin tamandua -j 4
cd ../Armadillo
git switch feat/evidence-audit-tamandua
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
```

Use the implementation branch until merged. No frontend/MCP installation required.

## Run and inspect

```bash
armadillo audit examples/tamandua_integration/input.json --tamandua ../Tamandua/target/debug/tamandua
python tests/real_tamandua.py -v
```

Expected SOURCE_LINKED, nine assertions, two inferred ArgumentNode memberships, nonempty direct derivations, contract_version 1.0 and rdf_sha256. The actual binary reports engine "dominox 0.1.0"; do not install separate DominoX.

For a nonsibling binary use --tamandua PATH; only the real test suite uses TAMANDUA_BINARY as an optional override. Runtime needs no network.

## Handle errors and test

Missing executable: build and pass the correct path. Version mismatch: use pinned commit, do not disable guard. Timeout: reduce input. Invalid RDF/schema: inspect contract and run real suite. Existing report: choose a new name. Standalone recovery: omit --tamandua explicitly.

Real suite tests inference, invalid RDF, Unicode/control literals, deterministic output and full integrated CLI. Standalone mock tests cover timeout, mismatched versions/schema and unexpected exits; mocks do not count as real integration evidence.
