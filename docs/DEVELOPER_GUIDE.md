# Developer guide

src/armadillo/core.py: validation, source presence and hashes. rdf.py: N-Triples serialization. tamandua.py: optional trusted subprocess adapter. cli.py: installed command. No HTTP server/native shared library.

Install editable; run python -m unittest discover -s tests -v, python scripts/check_docs.py, ruff check src tests scripts and ruff format --check src tests scripts. Install Ruff with python -m pip install ruff==0.14.3. Build with python -m pip wheel --no-deps . --wheel-dir dist.

Real integration: python tests/real_tamandua.py -v requires actual pinned engine and fails rather than skipping missing setup. test_core.py covers invariants, test_cli.py subprocess workflows, test_adapter.py mock-only protocol failures. scripts/benchmark.py measures synthetic 500-node auditing, not scientific accuracy.

New validation must preserve immutability, deterministic hashes and explicit errors. New engine support requires actual contract tests. Matching/serialization changes require schema/contract decisions. No randomness is used.

Each cloud task is already isolated: use existing checkouts; do not create worktrees unless explicitly requested. Keep public docs in English and synthetic fixtures free of private data.
