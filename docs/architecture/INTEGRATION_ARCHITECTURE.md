# Integration architecture

| Responsibility | Owner | Interface |
|---|---|---|
| Validation, presence, findings, hashes | Armadillo core | Python/JSON CLI |
| Serialization | Armadillo rdf | Standard N-Triples |
| Version/process/schema checks | Optional adapter | Trusted executable and private file |
| Parsing, closure, direct provenance | Tamandua | reason FILE |
| Interchange grammar | Shared standards | N-Triples, JSON |
| Scientific scoring | Neither MVP component | Not implemented |

Independent installation, versioning, tests and publication. No Tamandua source change or circular dependency. Enable via --tamandua. The adapter creates private temporary graph.nt, invokes the existing CLI without a shell, validates responses, removes temporary files and embeds analytical data. No network or persistent service.

Native integration was absent in the baseline. Direct Rust library access would require FFI; existing structured file exchange is simpler. HTTP was evaluated and adds startup/availability concerns without MVP benefit.

See [contract](../integrations/INTERFACE_CONTRACT.md), [compatibility](../integrations/COMPATIBILITY.md), [diagrams](../diagrams/README.md).
