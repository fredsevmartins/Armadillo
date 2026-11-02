# Decisions

1. Python 3.11+ and stdlib runtime fit bounded file processing; the baseline had no existing stack.
2. Manual annotation avoids inventing unvalidated extraction/scoring; exact matching has independently testable semantics.
3. No native Armadillo integration existed. Rust library integration would require bindings; standard N-Triples through the existing Tamandua CLI is simpler than HTTP listener management.
4. No shared library: Armadillo owns audit/serialization, Tamandua owns reasoning; install-time dependencies remain independent.
5. Pin engine version and commit; reject unknown versions/schema. Requested integration failures are explicit; standalone requires omitting the flag.
6. Preserve inputs, no silent normalization/fallback, no truth labels; omit volatile timestamps.
7. Original new code under MIT, reference acknowledged without copying.
8. Preserve Git history, use a descriptive branch and grouped commits; no merge or release without approval.
