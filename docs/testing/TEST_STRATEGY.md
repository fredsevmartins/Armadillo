# Test strategy

## Baselines

The original Armadillo checkout contained only README.md and no tests. Historical baseline reports identify the commits and checks they actually executed. Do not infer current release readiness from those snapshots.

## Application tests

Use unittest for validators, exact expected source matches, SHA-256/source preservation, Unicode/CRLF/BOM handling, selected-span integrity, provenance/author metadata, explicit replacement/deletion, dangling-link rejection and input immutability.

Exercise CLI operations through subprocesses, including document preparation to annotation, report generation and comparison. Verify output collisions and simulated partial-write/flush/publication errors leave existing data unchanged and remove unpublished artifacts.

Protocol tests deliberately simulate malformed/inconsistent replies and are not proof of real engine integration. Separate actual-process cases verify bounded stdout/stderr capture, timeouts and safe diagnostics.

## Actual integration

The separate real suite requires the compatible Tamandua source checkout and executable. It verifies origin/revision connection, actual subclass inference, imported/authored document audit, same-document impact plans, no-op/add/remove cases, exact literal roundtrips and repeated analytical equality. Missing prerequisites fail, never silently skip.

Repository checks use actual Git metadata in the real suite. Mocked metadata guards cover wrong origin, dirty checkout, incompatible revision and absent build separately.

## Schemas and distribution

Check all bundled/public schema resources for equality. Validate schemas and representative legacy/new input, report, comparison and connection outputs with jsonschema. Runtime cross-field/hash/graph invariants remain mandatory beyond JSON Schema.

Build/install wheels in clean environments outside the source checkout. Verify standalone import/annotation/audit/schema export without optional parser packages; separately install the extra and test the actual engine. CI definitions include multiple Python versions and an explicitly pinned engine checkout. Hosted success needs independent evidence.

## Scientific and security boundaries

No numerical scientific score/model is implemented, so no scientific accuracy, calibration or coverage percentage is claimed. Exact discrete expectations use equality rather than arbitrary floating tolerances.

Relevant input, output, process and provenance failures are tested. Dependency/advisory queries, parser syntax checks and platform support are reported with their actual scope. No test count is a security certification, and a repeated quoted sentence is not independent scientific evidence.
