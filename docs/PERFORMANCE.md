# Performance baseline

Historical baseline evidence for fc8a966. Current hardening results: [HARDENING_RESULTS.md](testing/HARDENING_RESULTS.md).

Measured 2026-11-02 with python scripts/benchmark.py on Linux 6.18.57 x86_64, glibc 2.41, Python 3.12.14. Synthetic 500 nodes: 250 claims, 250 evidence nodes, fixed short document; one warmup and 20 repeated audits. The script asserts SOURCE_LINKED and times validation, hashing and audit together. tracemalloc remains enabled during timing.

Observed median 0.016413108 seconds, minimum 0.014979232, maximum 0.017611134; peak Python allocation tracked across loop 342,588 bytes. This is not whole-process RSS, independent-source extraction throughput or a scientific benchmark. Shared-host timing varies. The measurement does not justify optimization; no speculative caching or parallelism added.

Real integration includes two process launches and temporary-file exchange. Correctness/repeatability were verified, but integration latency and process RSS were not benchmarked. No comparative performance claim against the reference or Tamandua.
