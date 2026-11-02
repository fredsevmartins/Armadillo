# Connect Armadillo to Tamandua

Armadillo uses the actual CLI of [fredsevmartins/Tamandua](https://github.com/fredsevmartins/Tamandua) through standard N-Triples and JSON. The projects remain independently installed, tested, versioned and published. No shared database, Rust/Python binding, API account or circular dependency is introduced.

## Compatible source

Verified commit: [09970fb8985e6065cc24ff5507a8de161c301ee9](https://github.com/fredsevmartins/Tamandua/tree/09970fb8985e6065cc24ff5507a8de161c301ee9), package version 0.1.0, built with Rust 1.90.0. The actual binary reports "dominox 0.1.0" because of historical package naming. This is not a dependency on the separate DominoX repository.

## Install/build the independent checkout

Use existing checkouts when present and preserve local work. For a new sibling checkout:

```bash
git clone https://github.com/fredsevmartins/Tamandua.git ../Tamandua
git -C ../Tamandua checkout 09970fb8985e6065cc24ff5507a8de161c301ee9
rustup toolchain install 1.90.0 --profile minimal
cd ../Tamandua
cargo +1.90.0 test --locked --workspace -j 4
cargo +1.90.0 build --locked --bin tamandua -j 4
cd ../Armadillo
python -m pip install '.[tamandua]'
```

No frontend/MCP build or HTTP server is needed. Never reset a user's working tree to satisfy a revision guard.

## Verify and connect

```bash
armadillo doctor --tamandua-repo ../Tamandua
armadillo audit examples/tamandua_integration/input.json --tamandua-repo ../Tamandua --format markdown
armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --tamandua-repo ../Tamandua --format markdown
```

doctor requires the checkout root, expected GitHub origin, verified commit and no tracked changes. It then checks a real subclass inference and reports CONNECTED. A dirty checkout is rejected; preserve your work and choose the supported clean checkout, or explicitly trust a custom executable with --tamandua. Version/functional checks do not cryptographically attest how a binary was built.

For a packaged binary without a source checkout:

```bash
armadillo doctor --tamandua /absolute/path/to/tamandua
```

This validates version and behavior, with checkout_commit null. It cannot verify source origin.

## Runtime exchange and integrity

The adapter creates private temporary files, checks the version, invokes reason or plan without a shell, validates RDF sets/response invariants and removes runtime timestamps from analytical results. Both process streams are bounded while reading, and timeout/failure cleanup stops the POSIX process group.

No runtime network call, remote repository write or graph application occurs. Repository checks inspect only local Git metadata; GitHub access is used separately for checkout/update operations.

Source-present claims and user-declared support remain distinct from RDFS classification. Graph impact does not prove evidentiary entailment, scientific truth or causality.

## Contracts and verification

- [Closure/serialization contract](INTERFACE_CONTRACT.md).
- [Comparison/impact contract](ANNOTATION_COMPARISON.md).
- [Compatibility matrix](COMPATIBILITY.md).
- [Complete tutorial](../TAMANDUA_TUTORIAL.md).
- [Current executed results](../testing/DOCUMENT_WORKFLOW_RESULTS.md).

The CI definition checks out this exact Tamandua commit, builds/tests it and runs the real integration suite. Hosted success must be inspected independently; local success alone does not prove it.
