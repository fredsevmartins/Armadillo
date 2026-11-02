# Editable diagrams

Implemented MVP, not future proposals. Mermaid source files are editable. Rendering is not independently validated by a Mermaid CLI.

## system

[Source](system.mmd)

```mermaid
flowchart LR
  Input[Annotated JSON] --> Core[core.validate and core.audit]
  Core --> Report[JSON findings and hashes]
  Core --> RDF[rdf.export_nt]
  RDF --> Adapter[Optional tamandua.reason]
  Adapter --> Report
```

## integration

[Source](integration.mmd)

```mermaid
sequenceDiagram
  participant U as Operator
  participant A as Armadillo adapter
  participant T as Tamandua CLI
  U->>A: Explicit executable and N-Triples
  A->>T: --version
  T-->>A: dominox 0.1.0
  A->>A: Private temporary graph.nt
  A->>T: reason graph.nt
  T-->>A: JSON closure and derivations
  A->>A: Validate, drop timestamp, clean temporary file
  A-->>U: Analytical payload
```

## data-flow

[Source](data-flow.mmd)

```mermaid
flowchart TD
  J[Bounded UTF-8 JSON] --> V[Schema and reference validation]
  V --> Q[Exact quote presence]
  Q --> S[Source-present supporters]
  S --> R[Report and hashes]
  V --> N[N-Triples assertions]
  Q --> N
  N --> T[Optional Tamandua RDFS closure]
  T --> R
```

## workflow

[Source](workflow.mmd)

```mermaid
flowchart TD
  I[Install Python package] --> P[Prepare document and manual annotations]
  P --> A[Run audit]
  A --> D{Enable Tamandua?}
  D -->|No| R[Inspect findings]
  D -->|Yes| T[Run pinned trusted CLI]
  T --> R
  R --> O[Create new report]
```

## errors

[Source](errors.mmd)

```mermaid
flowchart TD
  I[Input] --> V{Valid schema and links?}
  V -->|No| E[stderr JSON and exit 1]
  V -->|Yes| A[Compute audit]
  A --> D{Engine requested?}
  D -->|No| R[Return findings]
  D -->|Yes| T{Version and closure valid?}
  T -->|No| E
  T -->|Yes| R
  E --> F[Correct input or omit integration and rerun]
```

## testing

[Source](testing.mmd)

```mermaid
flowchart LR
  U[Core unit cases] --> C[Validation audit and RDF]
  M[Mock protocol failures] --> A[Optional adapter]
  E[CLI subprocess tests] --> C
  E --> A
  R[Separate real suite] --> T[Pinned Tamandua binary]
  T --> A
  D[Documentation checks] --> Docs[Local links and diagram sources]
```

## Annotation comparison

[Editable source](comparison.mmd) shows standalone diffs and the optional actual Tamandua impact exchange. It is implemented; no scientific-entailment claim is implied.
