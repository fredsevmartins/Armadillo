# Reference analysis

Repository: https://github.com/fabio-rovai/brain-in-the-fish.
Commit ada41c90de336fe21b99bd6f282aa6b66a295f12.
License MIT © 2026 Fabio Rovai, inspected before implementation. No code, datasets, documentation or assets copied.

Cargo workspace: Rust 2024, core/cli/mcp crates v0.1.0. Core requires sibling open-ontologies with embeddings and uses rmcp, Tokio, reqwest, pdf-extract, serde and others.

Source evidence: argument_graph.rs and extract.rs implement argument representation/extraction; gate.rs compares holistic and structural/node-quality scoring with configurable logarithmic tolerance, including no-node/no-evidence branches. validate.rs implements citation, word-count, structure and duplicate checks; its citation year is hardcoded to 2026. Further modules include verify, report, calibrate, firewall and debate.

README workflow: LLM document decomposition → OWL graph → rules/structural metrics → consistency gate. Included datasets, case studies and reported benchmark accuracy were not independently reproduced. Source code license alone is not evidence of dataset redistribution rights.

Reference build/tests: NOT EXECUTED; sibling open-ontologies is absent, and rebuilding it is outside the chosen independent MVP. Module presence establishes source capability, not scientific validation.

Armadillo preserves the source-traceability objective using manual JSON annotation, exact matching and optional Tamandua RDFS closure. It does not approximate scoring, PDF extraction, learned gates, OWL, agents or external fact checking under misleading names.
