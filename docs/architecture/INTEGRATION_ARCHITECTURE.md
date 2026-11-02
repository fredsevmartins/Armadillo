# System and integration architecture

Armadillo is a local Python package; Tamandua is an independently maintained Rust CLI. File exchange uses established N-Triples/JSON. No service, database, FFI bridge, message broker or circular dependency is needed.

## Responsibilities

| Capability | Owner | Interface |
|---|---|---|
| Unchanged UTF-8 document import | Armadillo documents | prepare command / input 1.1 |
| Explicit span selection and reviewer metadata | Armadillo documents/core | annotate command |
| Source/link/hash/span validation | Armadillo core | Python and audit CLI |
| Exact presence findings and readable output | Armadillo core/output | Report 1.2 JSON/Markdown |
| Snapshot/document-scoped RDF | Armadillo rdf | N-Triples |
| Same-document version comparison | Armadillo compare | Comparison 1.1 |
| Checkout origin/revision and functional diagnostic | Optional connection module | doctor and --tamandua-repo |
| RDF parsing, RDFS closure and graph impact | Tamandua | reason / plan |
| Optional response correspondence checks | Armadillo adapter with pinned RDFLib | Closure 1.1 / impact 1.0 |

## Main paths

1. prepare reads a bounded regular UTF-8 .txt/.md file without normalization, embeds the original text and records source provenance.
2. annotate validates explicit source spans and creates a new snapshot with author/revision metadata. It never changes the original or silently removes dangling links.
3. audit verifies exact quote presence, declared source supporters and outputs reproducible findings.
4. Optional repository selection verifies local checkout metadata, resolves a build and uses the existing engine. Direct executable selection is explicit operator trust.
5. compare audits both snapshots, requires identical document text, calculates changed nodes/supporters and optionally computes/validates real Tamandua graph impact.
6. Output publication is exclusive and atomic on a filesystem supporting hard links.

## Independence and trust

Standalone application paths use only the standard library. The parser extra is optional and the engine is separately installed/versioned/tested. No runtime GitHub request or source mutation is performed. Local Git metadata checks are not binary attestation. The operator controls the selected executable and document paths.

Quote presence, user labels and RDFS classifications are different observations; none alone establishes scientific truth. No implicit extraction/scoring is introduced.

See [editable diagrams](../diagrams/README.md), [source tutorial](../TUTORIAL.md), [closure contract](../integrations/INTERFACE_CONTRACT.md) and [comparison contract](../integrations/ANNOTATION_COMPARISON.md).
