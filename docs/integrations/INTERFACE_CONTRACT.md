# RDF closure adapter contract 1.1

Interface: armadillo-tamandua-cli. This contract covers optional local N-Triples exchange; source/audit metadata versioning is described separately below. It is not an HTTP API.

## Source input and validation

Input 1.0 requires exactly schema_version, document and nodes. Input 1.1 additionally allows provenance, last_edit and per-node annotation metadata. Both require nonblank UTF-8 document text and at most 1,000 nodes. Nodes require unique IDs matching [A-Za-z][A-Za-z0-9_-]{0,63}, kind claim/evidence, nonblank quote and unique supports references to existing claims. Claims cannot have support targets.

Input 1.1 author/revision labels are explicit user assertions. Optional paired selected offsets must be integers and must exactly identify the quote in the document. Imported source provenance includes name, txt/md format and SHA-256 matching the embedded UTF-8 source. last_edit records author, action and node ID, not a signed/full history.

Files and canonical serialized input are capped at 1 MiB. Duplicate/unknown JSON fields, non-finite numeric values, malformed Unicode, invalid spans, dangling references and unsupported versions fail. JSON Schema is bundled; runtime validation additionally checks cross-field/link/hash constraints. Source metadata is never interpreted as a file path or executable.

## RDF representation

UTF-8 N-Triples, vocabulary https://w3id.org/armadillo-evidence/. This URI is an identifier, not a runtime destination or a claim of registered/resolvable ownership.

Claim/Evidence are subclasses of ArgumentNode. Each node has rdf:type and a quote literal; declaredSupports records user assertions and SourcePresentNode records exact presence findings. Author metadata is retained in audit JSON rather than assigned unsupported semantic meaning in RDF.

Default snapshot subjects are urn:sha256:INPUT_HASH:NODE_ID. Same-document comparison explicitly uses document-hash subjects as described in the [impact contract](ANNOTATION_COMPARISON.md). No source text, quote or user ID is silently rewritten.

## Process and response

Version must be exactly "dominox 0.1.0" (actual audited package spelling) or "tamandua 0.1.0". Invoke reason PRIVATE_GRAPH.nt using an explicit trusted executable, without a shell or network.

The analytical envelope requires asserted, inferred and derivations arrays. Triples have subject/predicate/object strings in the engine's RDF spelling. Submitted and returned parsed assertion sets must match. Reject duplicate triples, asserted/inferred overlap, unknown rule names, invalid provenance references and missing inference provenance. Literal comparison uses the pinned RDFLib parser's RDF term semantics; exact source presence itself is never normalized.

Derived facts remain engine conclusions under its limited RDFS profile. The adapter does not independently prove recursive scientific/evidentiary validity.

Output wrapper: contract_version 1.1, engine, rdf_sha256 and analytical. Runtime timestamps are omitted. Unknown response fields/versions are rejected where the strict closure contract applies.

## Limits and failures

Preflight rejects RDF over 2 MiB or 20,000 assertions before process launch. JSON input validity does not guarantee generated RDF or closure acceptance. The engine's own closure/work/provenance limits still apply.

Capture is bounded during reading: 16 MiB stdout, 64 KiB stderr. Timeout defaults to 30 seconds per process, configurable in (0,300]. Failure/overflow cleanup stops the POSIX process group and removes temporary files. Bounded safe engine diagnostics are retained. The trusted executable still has caller privileges; this is not a malicious-program sandbox or a hard engine-memory cap.

Requested integration errors return no successful report; explicitly omit the option for standalone. CLI failures use stderr JSON and exit 1; invalid invocation can use exit 2.

## Audit output and publication

Current audit report is schema 1.2: version/software/hash metadata, status/counts, findings, unsupported_claims and limitations; optional source/edit/author metadata is preserved. Each finding includes quote, quote_found, at most ten overlapping occurrences, codepoint ranges [start,end), one-based LF lines/columns, context up to 160 codepoints and an explicit truncation flag.

SOURCE_LINKED means nonempty annotations, all quotations present and source-present declared evidence for each claim. REVIEW_REQUIRED otherwise. Neither label verifies truth or causal/semantic support.

Report hashes use SHA-256 over exact UTF-8 source and sorted-key compact JSON input. Array order remains significant. No claim of RFC 8785/RDF-isomorphism canonicalization is made.

New outputs use private same-directory temporary files, flush/fsync and exclusive atomic hard-link creation. Handled failures remove unpublished temporary files. Existing destinations are never replaced. Hard-link filesystem support is required; power-loss directory durability and uncatchable-process cleanup are outside this guarantee.
