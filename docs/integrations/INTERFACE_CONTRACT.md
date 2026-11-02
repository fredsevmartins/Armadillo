# Interface contract 1.1

Interface: armadillo-tamandua-cli. Input schema_version "1.0"; report schema_version "1.1".

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

Python adapter timeout defaults to 30 seconds per process, configurable in (0,300]. Capture is bounded during reading: 16 MiB stdout, 64 KiB stderr. Overflow or timeout stops the POSIX process group. This is not a sandbox for a malicious executable. Executable is trusted operator configuration. No automatic migrations, downgrade, normalization or retries. Unknown engine versions/closure fields fail until explicitly verified.

## 1.1 correspondence and source locations

Optional installation requires the pinned RDFLib parser and pyparsing. Parsing is explicitly N-Triples with local data only; no remote JSON-LD/RDF sources are loaded. Parsed assertion sets must equal submitted assertions. Duplicates, assertion/inference overlap, absent inference provenance, unknown rules and invalid references fail. RDF comparison uses parser term equality (including RDFLib typed-literal normalization); the supplied source/annotation JSON and exact-quote findings are never normalized. Blank-node labels are held stable within the submitted exchange, not canonicalized across documents.

Preflight rejects RDF above 2 MiB or 20,000 assertions before launching the executable. Input JSON acceptance does not guarantee generated-RDF/closure acceptance; reduce links or run standalone. Computation/closure limits may still fail. Bounded safe stderr details are retained.

Each finding includes the quote, occurrences (at most ten), and occurrences_truncated. Positions are Unicode codepoints, zero-based [start,end); line/column are one-based, with LF defining line breaks. Overlapping matches are included; context is at most 160 characters per occurrence. No locations are produced for missing quotes. Markdown escapes raw content, including controls/HTML.

Output publication uses a private same-directory temporary file, flush/fsync and an exclusive atomic hard link; collisions never replace data. Unpublished temporary files are removed on handled failures. This requires filesystem hard-link support and is not a guarantee against power-loss/directory durability or an uncatchable process termination.
