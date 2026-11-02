# Validation matrix

| Requirement | Evidence | Status |
|---|---|---|
| Install/run independently | Editable/wheel install and example | See test results |
| Source matching / absent evidence | Core reference/fabrication cases | PASS |
| Schema/references | Invalid input subcases | PASS |
| Preserve inputs/results | Immutability and exclusive output | PASS |
| Missing engine / recovery | CLI missing/standalone tests | PASS |
| Actual RDF inference | Real suite and pinned binary | PASS |
| Version/schema mismatch | Mock-only adapter cases | PASS |
| Malformed RDF | Actual-engine rejection | PASS |
| Timeout/unexpected failure | Mock protocol cases | PASS |
| Repeatability | Core and real analytical equality | PASS |
| Scientific truth/scoring | Not implemented | NOT EXECUTED, not applicable |
| Reference benchmark replication | Outside MVP | NOT EXECUTED |
| External vulnerability scanning | Separate activity | NOT EXECUTED |
| Hosted GitHub Actions | Workflow defined, remote status unverified | NOT EXECUTED |
| Merge/release | Requires explicit authorization | NOT EXECUTED |

Unique counts appear in TEST_RESULTS.md. Regression/security invariants overlap core/CLI tests, not additional invented cases. Zero-test targets are never coverage.
