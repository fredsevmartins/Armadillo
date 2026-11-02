# Tamandua audit

Repository: https://github.com/fredsevmartins/Tamandua.
Commit: 09970fb8985e6065cc24ff5507a8de161c301ee9.
MIT © 2026 Tamandua contributors; license inspected. Source and lockfiles unchanged.

Cargo.toml defines Rust 2021 workspace v0.1.0: crates/dominox-core and crates/dominox-cli. Historical package naming is not a dependency on the separate DominoX repository. No DominoX checkout is needed.

Core lib.rs uses rio_turtle/rio_api, ordered triple sets and bounded fixed-point reasoning. Six rule families implement subclass/subproperty transitivity, membership/property propagation, domain and range. Closure includes asserted/inferred triples and direct derivations. Impact plans are non-mutating. No OWL, SPARQL, database or causal inference.

CLI main.rs exposes validate, stats, reason, explain, plan, demo, serve. reason FILE accepts .nt/.ttl and returns {execution_timestamp_unix_seconds, analytical:{asserted,inferred,derivations}}. The actual primary executable reports "dominox 0.1.0". Armadillo accepts that verified spelling and "tamandua 0.1.0".

Axum API, React/Vite frontend and Python MCP adapter exist but are unnecessary for chosen file/CLI integration. The API defaults to loopback without authentication, bounds file paths to workspace; CLI uses operator permissions. Graphs are in-memory.

Limits: 2 MiB RDF input, 20,000 closure triples, 100,000 derivations, 20 million rule pair checks. No full RDFS/OWL or truth validation. Timestamps are excluded from reproducibility comparisons.

Execution: existing cargo test --locked --workspace -j 4 passed 14 reasoning tests; zero-test binary/doc targets are not counted. Locked offline binary build passed. Actual Armadillo adapter tests verified subclass inference, provenance, invalid RDF, Unicode/control literals, repeatability and CLI execution; final totals in TEST_RESULTS.md.

Evidence: Cargo manifests; crates/dominox-core/src/lib.rs; crates/dominox-core/tests/reasoning.rs; crates/dominox-cli/src/main.rs; docs/CLI.md, API.md, REASONING_PROFILE.md and LICENSE at the pinned commit.
