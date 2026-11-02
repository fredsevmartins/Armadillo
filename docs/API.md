# Actual API

No HTTP endpoints exist.

Python interfaces: core.validate(data) returns validated input; core.audit(data) returns report without mutation; rdf.export_nt(data) returns N-Triples; tamandua.reason(nt,binary,timeout=30) returns contract/engine/hash/analytical data. All input/integration failures raise core.AuditError. parse_json rejects duplicate/non-finite JSON; read_file bounds regular UTF-8 files.

See [contract](integrations/INTERFACE_CONTRACT.md). Callers provide JSON-like plain dict/list/string data. Interfaces are version 0.1.0; future compatibility changes require documented migration.
