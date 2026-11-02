# Interface contract 1.0

Interface: armadillo-tamandua-cli. Input/report schema_version "1.0".

## Input

Exactly schema_version, document, nodes. document is a nonblank string. nodes contains up to 1,000 objects, each with exactly id, kind, quote, supports. IDs match [A-Za-z][A-Za-z0-9_-]{0,63}, unique. kind is claim/evidence, quote nonblank, supports a unique array of existing claim IDs. Claims have empty supports. Empty graph is allowed and requires review.

Reject unknown/duplicate keys, invalid Unicode, non-finite JSON constants, wrong types, dangling links and unknown version. File/canonical input limit 1 MiB. JSON fields never provide paths or commands. See [JSON Schema](../../schemas/input.schema.json); cross-node uniqueness/references and byte limits are extra runtime checks.

## RDF and invocation

Standard UTF-8 N-Triples. Vocabulary https://w3id.org/armadillo-evidence/ is an identifier, not a runtime URL dependency or claim of registered ownership. Subjects: urn:sha256:CANONICAL_INPUT_HASH:NODE_ID. Claim/Evidence subclasses of ArgumentNode; rdf:type, quote, declaredSupports and SourcePresentNode encode assertions and findings separately. Quotes are escaped, original content preserved.

EXECUTABLE --version must return exactly "dominox 0.1.0" (actual binary) or "tamandua 0.1.0". EXECUTABLE reason PRIVATE_ABSOLUTE_GRAPH.nt returns a JSON envelope with analytical exactly asserted, inferred, derivations. Triples contain nonempty subject/predicate/object strings in canonical engine spelling. Derivations require known conclusion and nonempty alternatives with rule and two known premises. Schema/reference membership is validated; the operator-selected engine is trusted for RDF semantics.

## Report

schema_version, software_version, input_sha256, document_sha256, status, counts, unsupported_claims, findings, limitations. SHA-256 covers UTF-8 document and sorted-key compact JSON input, respectively. Arrays remain ordered; no Unicode normalization or claim of RFC 8785 canonicalization.

SOURCE_LINKED requires nonempty nodes, all quotes present and every claim with source-present declared evidence. REVIEW_REQUIRED otherwise. Evidence-only graphs can be source-linked. Reused quotes/support labels do not prove independent evidence or truth.

Optional tamandua object: contract_version, engine, rdf_sha256, analytical. Engine execution_timestamp_unix_seconds omitted. Inference adds class memberships, not semantic evidence verification.

## Errors and compatibility

Exit 1, stderr JSON {error:{code:"AUDIT_FAILED",message:"..."}}. Argparse invocation errors use exit 2. Requested integration failure returns no success report; omit --tamandua for standalone. Output creation is exclusive.

Python adapter timeout defaults to 30 seconds per process, configurable in (0,300]. Captured stdout checked against 16 MiB after capture: this does not hard-limit memory or sandbox a malicious executable. Executable is trusted operator configuration. No automatic migrations, downgrade, normalization or retries. Unknown engine versions/closure fields fail until explicitly verified.
