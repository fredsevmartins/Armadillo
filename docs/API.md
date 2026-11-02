# Python API and machine contracts

No HTTP API exists. Modules below are under armadillo, for example `from armadillo.documents import prepare`. Install the package and use the following actual interfaces:

| Interface | Behavior |
|---|---|
| documents.prepare(path, document_id=None, title=None) | Import unchanged UTF-8 .txt/.md into input 1.1 |
| documents.annotate(data, node_id, author, ...) | Return a new explicitly edited input; preserve the original |
| documents.serialize_input(data) | Emit bounded compact JSON that can be read back, including its final newline |
| core.validate(data) | Validate supported input versions and source/span integrity |
| core.audit(data) | Return deterministic report 1.2 without changing the input |
| rdf.export_nt(data, identity="snapshot") | Export N-Triples; document mode is explicit |
| compare.compare(before, after, binary=None, timeout=30) | Same-document comparison 1.1 and optional actual impact |
| tamandua.reason(nt, binary, timeout=30) | Validated optional closure adapter contract 1.1 |
| connection.resolve(binary=None, repository=None, timeout=30) | Resolve an explicitly trusted executable or verified checkout |
| connection.doctor(binary=None, repository=None, timeout=30) | Perform connection diagnostic 1.0 using actual inference |
| contracts.load_schema(name) | Load a bundled JSON Schema offline |
| output.write_new(path, text) | Publish a complete new file without replacement |
| output.markdown(report) | Escape raw content for a human-readable audit |

Input/runtime errors raise core.AuditError; output/filesystem functions can also raise OSError. CLI diagnostics normalize these to error JSON/exit 1. Callers supply plain JSON-like dict/list/string data.

## Version matrix

| Contract | Current |
|---|---|
| Package | 0.2.0, unreleased |
| Input | 1.0 legacy accepted; 1.1 adds optional source/edit/node-author metadata |
| Audit report | 1.2 |
| Closure adapter | 1.1 |
| Comparison | 1.1 |
| Impact wrapper | 1.0 |
| Connection diagnostic | 1.0 |
| Tamandua package | 0.1.0 at the pinned commit |

Input 1.0 remains strict: new metadata requires explicit 1.1 output. Prepared provenance binds the exact embedded source bytes through SHA-256. Node author metadata optionally retains paired selected spans, which must match quote text exactly. JSON Schema does not replace runtime cross-field/link/hash checks.

Sources/arrays are not silently normalized. Hashes represent the defined UTF-8/sorted-key compact JSON encoding, not RFC 8785 or RDF graph-isomorphism canonicalization. RDFLib term comparison has its own typed-literal semantics; exact source quote checks remain codepoint comparisons.

Use [CLI reference](CLI.md), [closure contract](integrations/INTERFACE_CONTRACT.md) and [comparison contract](integrations/ANNOTATION_COMPARISON.md) for detailed behavior.
