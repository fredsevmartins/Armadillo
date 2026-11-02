# Editable architecture and workflow diagrams

All diagrams describe implemented behavior. No scientific inference, remote service or future component is implied. Each source is editable Mermaid; all nine sources passed Mermaid syntax parsing as recorded in the latest test results. Browser rendering/layout is not claimed.

## System

[Editable source](system.mmd)

```mermaid
flowchart LR
    Source[UTF-8 TXT or Markdown] --> Prepare[documents.prepare]
    Prepare --> JSON[Versioned JSON annotations]
    JSON --> Edit[documents.annotate]
    Edit --> Audit[core.audit]
    JSON --> Audit
    JSON --> Compare[compare.compare]
    Audit --> Reports[JSON or Markdown]
    Compare --> Reports
    Audit --> RDF[rdf.export_nt]
    RDF --> Adapter[Optional local CLI adapter]
    Compare --> Adapter
    Repo[Explicit Tamandua checkout or binary] --> Connection[connection.resolve]
    Connection --> Adapter
    Adapter --> Reports
```

## Documents

[Editable source](documents.mmd)

```mermaid
flowchart TD
    Source[UTF-8 TXT or Markdown] --> Prepare[prepare: preserve source and hash]
    Prepare --> Snapshot[Input 1.1 snapshot]
    Snapshot --> Select[Explicit codepoint span and reviewer alias]
    Select --> Edit[annotate: add, replace or delete]
    Edit --> Validate[Validate spans, links and source integrity]
    Validate --> New[New versioned snapshot]
    New --> Audit[Exact quote audit]
    Snapshot --> Compare[Compare same-document snapshots]
    New --> Compare
    Audit --> Report[JSON or escaped Markdown]
    Compare --> Report
```

## Connection

[Editable source](connection.mmd)

```mermaid
sequenceDiagram
    participant User
    participant Armadillo
    participant Git as Local Git metadata
    participant Tamandua as Independent Tamandua CLI
    User->>Armadillo: doctor with explicit checkout
    Armadillo->>Git: Root, origin, revision and tracked changes
    Git-->>Armadillo: Verified clean pinned checkout
    Armadillo->>Armadillo: Resolve release or debug executable
    Armadillo->>Tamandua: Version and local subclass check
    Tamandua-->>Armadillo: Closure and provenance
    Armadillo->>Armadillo: Verify expected inference
    Armadillo-->>User: CONNECTED diagnostic
```

## Integration

[Editable source](integration.mmd)

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

## Data Flow

[Editable source](data-flow.mmd)

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

## Workflow

[Editable source](workflow.mmd)

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

## Errors

[Editable source](errors.mmd)

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

## Testing

[Editable source](testing.mmd)

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

## Comparison

[Editable source](comparison.mmd)

```mermaid
sequenceDiagram
  participant U as User
  participant A as Armadillo compare
  participant T as Tamandua CLI
  U->>A: Baseline and proposed annotations
  A->>A: Validate same document and audit both
  A->>A: Compare node and declared support changes
  opt Explicit Tamandua integration
    A->>A: Export document-scoped stable identities
    A->>T: Version and reason baseline
    A->>T: Version and reason proposed
    A->>A: Build canonical add/remove delta
    A->>T: Plan baseline with changes
    T-->>A: Proposed graph, impact and explanations
    A->>A: Validate sets, counts, hashes and roots
  end
  A-->>U: Deterministic JSON or Markdown
```
