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
git switch main
python3 -m venv .venv
. .venv/bin/activate
python -m pip install '.[tamandua]'
```

Use main after this implementation has been merged; before that, use the implementation branch documented in HARDENING_RESULTS.md. No frontend/MCP installation required.

## Run and inspect

```bash
armadillo audit examples/tamandua_integration/input.json --tamandua ../Tamandua/target/debug/tamandua
python tests/real_tamandua.py -v
```

Expected SOURCE_LINKED, nine assertions, two inferred ArgumentNode memberships, nonempty direct derivations, contract_version 1.1 and rdf_sha256. The actual binary reports engine "dominox 0.1.0"; do not install separate DominoX.

For a nonsibling binary use --tamandua PATH; only the real test suite uses TAMANDUA_BINARY as an optional override. Runtime needs no network.

## Handle errors and test

Missing executable: build and pass the correct path. Version mismatch: use pinned commit, do not disable guard. Timeout: reduce input. Invalid RDF/schema: inspect contract and run real suite. Existing report: choose a new name. Standalone recovery: omit --tamandua explicitly.

Real suite tests inference, invalid RDF, Unicode/control literals, deterministic output and full integrated CLI. Standalone mock tests cover timeout, mismatched versions/schema and unexpected exits; mocks do not count as real integration evidence.

## Current reliability contract

Use --timeout SECONDS in (0,300] and --format markdown for readable output. The optional parser checks submitted versus returned RDF assertions, set separation, duplicate triples and provenance coverage. Generated RDF is preflighted at 2 MiB and 20,000 assertions; closure/computation limits can still fail with engine diagnostics. Both process streams are capped while reading (16 MiB stdout, 64 KiB stderr), and the process group is stopped on failure. Only POSIX integration is supported.
