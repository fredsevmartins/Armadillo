# Annotation comparison execution results

Date: 2026-11-02. Continuation branch: feat/reliable-evidence-reports; base hardening commits f32f5b6 and 6ce9d3e. No merge or release is claimed here.

Implemented standalone same-document annotation comparison, declared source-support changes, document-scoped stable RDF identities and optional actual Tamandua impact planning. Existing snapshot exports and audit input hashes remain unchanged.

## Executed outcomes

- Full standalone suite: 50 test methods passed, zero failed/skipped (includes six comparison cases).
- Actual pinned Tamandua suite: nine methods passed, zero failed/skipped (includes removal/repeatability and addition/no-op impact).
- Contract validation: four offline schemas and five representative input/report/comparison workflows, including actual engine outputs, passed.
- CLI walkthrough: evidence removal produces SOURCE_LINKED → REVIEW_REQUIRED, lost supporter evidence1, four removed assertions, one invalidated and one unchanged inference.
- Targeted inconsistent-plan tests reject mismatched version/hash/changes, proposed graphs/counts, impact sets/entities and explanation coverage.

Subcases are not extra method counts; 59 unique tests is the combined standalone/real total. Comparison tests confirm input preservation and reject changed document text. Node reordering alone is not treated as modification. Tests of malformed plan replies are simulated and are not evidence of actual Tamandua failures.

Run commands from /workspace/Armadillo with installed extras:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tests/real_tamandua.py -v
.venv/bin/python scripts/check_contracts.py --tamandua /workspace/Tamandua/target/debug/tamandua
.venv/bin/ruff check src tests scripts
.venv/bin/ruff format --check src tests scripts
.venv/bin/python scripts/check_docs.py
```

Earlier atomic I/O, bounded capture, parser advisory scan, source-location and clean-wheel results are recorded in [HARDENING_RESULTS.md](HARDENING_RESULTS.md). Full scientific evaluation, document ingestion/extraction, cross-document semantic matching, hosted CI evidence and release publication remain outside these verified capabilities. The graph impact is real RDFS subset reasoning, not evidence entailment or causality.

Final packaging checks also passed: wheel rebuilt, reinstalled into an isolated standalone environment, and the comparison CLI plus bundled comparison schema ran outside the source checkout. The complete updated managed setup passed all 50 standalone and nine actual-engine tests, Ruff, local links/seven diagram sources and the four-schema workflow validator. Hosted Actions were not observed.
