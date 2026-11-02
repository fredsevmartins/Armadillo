# Product vision

## Problem

Document reviews lose traceability when claims, quotations, declared evidence links and revision decisions are scattered across notes. Reviewers need to inspect the original passage and reproduce how an annotation or its supporting relationships changed.

## Approach

Armadillo preserves the source text and its hash, captures explicit source-span annotations with reviewer labels, verifies quotation presence and link structure, and exports reproducible reports. Same-document comparisons expose changes in annotations and declared support; optional Tamandua integration supplies actual graph reasoning and impact explanations.

## Intended users and boundaries

Researchers, technical reviewers and maintainers of evidence-based documentation can use the local CLI without a database or AI account. The current implementation is a manual source-traceability tool, not a validated scientific assessor. Presence is not truth, and a declared support link is not proof of entailment.

Success means reviewers can locate the cited text, understand missing-source findings, preserve prior snapshots and reproduce a comparison. Automated extraction, search and grading require their own implementation and evaluation before being presented as capabilities.
