# Actual API

No HTTP endpoints exist.

Python interfaces: core.validate(data) returns validated input; core.audit(data) returns report without mutation; rdf.export_nt(data) returns N-Triples; tamandua.reason(nt,binary,timeout=30) returns contract/engine/hash/analytical data. All input/integration failures raise core.AuditError. parse_json rejects duplicate/non-finite JSON; read_file bounds regular UTF-8 files.

See [contract](integrations/INTERFACE_CONTRACT.md). Callers provide JSON-like plain dict/list/string data. Interfaces are version 0.1.0; future compatibility changes require documented migration.

## Report/adapter contract 1.1

`armadillo.contracts.load_schema(name)` loads input/report/adapter JSON Schemas offline. `armadillo.output.write_new(path,text)` publishes complete files with exclusive atomic hard-link creation. `armadillo.output.markdown(report)` renders escaped, human-readable findings. Python callers must preserve the required report fields. Both resource/output schemas are bundled as package data.

`armadillo.compare.compare(before, after, binary=None, timeout=30)` returns comparison 1.0 for the exact same document; optional impact uses the pinned CLI. `armadillo.rdf.export_nt(data, identity="snapshot")` retains existing behavior; identity="document" is explicitly used by comparisons. Read integrations/ANNOTATION_COMPARISON.md before using document-scoped IDs.
