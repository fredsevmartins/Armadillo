# Executed test results

Date: 2026-11-02. Linux 6.18.57 x86_64, glibc 2.41, Python 3.12.14; Tamandua commit 09970fb8985e6065cc24ff5507a8de161c301ee9, Rust 1.90.0.

## Commands and outcomes

| Command from Armadillo root unless noted | Status | Actual result |
|---|---|---|
| python -m unittest discover -s tests -v | PASS | 23 tests, zero failed/skipped |
| python tests/real_tamandua.py -v | PASS | 5 actual-engine tests, zero failed/skipped |
| cargo test --locked --workspace -j 4 (Tamandua root) | PASS | 14 reasoning tests, zero failed/ignored |
| cargo build --locked --offline --bin tamandua -j 4 (Tamandua root) | PASS | Executable built |
| pip install --no-build-isolation --no-deps -e . | PASS | Editable package installed |
| pip wheel --no-build-isolation --no-deps . --wheel-dir dist | PASS | Wheel built |
| ruff check src tests scripts | PASS | No findings after removing unused import |
| ruff format --check src tests scripts | PASS | 11 files formatted |

The initial Ruff check found one unused import; it was removed and the check rerun successfully. No test failure was hidden or disabled. Subsequent distribution/docs/setup checks are recorded in the delivery report.

## Required category table

| Test category | Executed | Passed | Failed | Blocked |
|---|---:|---:|---:|---:|
| Unit | 12 | 12 | 0 | 0 |
| Integration | 9 | 9 | 0 | 0 |
| End-to-end | 7 | 7 | 0 | 0 |
| Regression | 2 | 2 | 0 | 0 |
| Scientific | 0 | 0 | 0 | 0 |
| Security | 7 | 7 | 0 | 0 |

28 unique Armadillo cases: 12 core + 5 mock adapter + 6 CLI + 5 actual engine. Integration above groups five mock protocol cases and four actual-engine cases; end-to-end groups six standalone CLI cases and the real integrated CLI case. Regression/security rows overlap these cases, not additional tests. Subtests are not counted separately. Tamandua's 14 existing cases are separate.

Regression tags: no_mutation_and_repeatability, reference_case. Security tags: invalid_inputs, strict_json, file_limits_and_encoding, fifo_does_not_block, rdf_escaping, output_preservation, invalid_responses.

Scientific numerical verification: NOT EXECUTED / not applicable; no scientific scoring algorithm implemented. Reference benchmark suite, external vulnerability/advisory scanning, Mermaid rendering and hosted Actions: NOT EXECUTED. No coverage percentage claimed.

## Real integration evidence

Synthetic input yielded nine assertions and two inferred ArgumentNode memberships with direct provenance. Expected claim membership was computed independently from the exported Claim subclass axiom. Repeat analytical results were exactly equal. Malformed RDF returned engine error; astral Unicode and control-character literal import succeeded. Requested missing-engine failure was explicit and standalone rerun remained functional.

Exact source presence does not validate truth, causality or document quality. No hidden network/AI service was used.
