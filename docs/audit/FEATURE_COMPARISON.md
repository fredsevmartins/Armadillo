# Feature comparison

| Capability | Armadillo baseline | Reference source evidence | Final MVP status |
|---|---|---|---|
| Source traceability | Missing | argument_graph.rs, verify.rs | Already implemented: core.audit |
| Manual graph input | Missing | argument_graph.rs | Already implemented: schema 1.0 |
| Automated extraction | Missing | extract.rs, llm.rs | Missing; outside MVP |
| Document scoring | Missing | scoring.rs, gate.rs | Not applicable to traceability-only MVP |
| RDF exchange | Missing | argument_graph.rs, rules.rs | Already implemented: export_nt |
| Explainable reasoning | Missing | open-ontologies dependency | Partially implemented: optional RDFS; no OWL |
| Tamandua adapter | Missing | No verified native mechanism | Already implemented and real-tested |
| Reproducibility metadata | Missing | report.rs | Already implemented: SHA-256 |
| PDF/MCP/UI | Missing | ingest.rs, mcp, visualize.rs | Missing; outside MVP |
| Additional engine versions | Missing | Not applicable | Planned; compatibility tests required |
| Scientific truth validation | Missing | README claims not reproduced | Not applicable; no truth claims |

Already implemented refers to the final MVP, not the empty baseline. Source evidence is not benchmark replication. Exact inspected commits are recorded in companion audit documents.
