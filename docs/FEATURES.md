# Implemented features and scope

Development package 0.2.0, unreleased. Current functionality is evidence traceability, not automated scientific evaluation.

| Capability | Status | Evidence |
|---|---|---|
| UTF-8 TXT/Markdown import without normalization | Implemented | documents.prepare and source-preservation tests |
| Explicit add/replace/delete span annotations | Implemented | documents.annotate, author/revision metadata and CLI tests |
| Source hash and selected-span integrity | Implemented | core.validate and tampering/stale-span tests |
| Exact quote/link auditing | Implemented | core.audit and reference cases |
| JSON/Markdown with source context | Implemented | core/output, escaping and occurrence tests |
| Offline JSON Schemas | Implemented | Packaged resources and schema workflow validation |
| Atomic no-overwrite output | Implemented | Write/flush/publication failure and collision tests |
| Same-document annotation/support comparison | Implemented | compare and regression cases |
| Actual Tamandua closure and impact | Implemented, optional | Separate pinned real-engine suite |
| Verified source checkout connection | Implemented, optional | doctor and repository-selection tests |
| PDF/automatic extraction/semantic scoring | Not implemented | Outside current release scope |
| Cross-edited-document identity matching | Not implemented | Comparisons reject changed source text |

Current executed evidence and limitations are in [DOCUMENT_WORKFLOW_RESULTS.md](testing/DOCUMENT_WORKFLOW_RESULTS.md). Hosted CI, merge and distribution are separate delivery states.
