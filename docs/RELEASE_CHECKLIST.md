# Release checklist

0.2.0 is available as source on main. A packaged release remains unpublished; this checklist does not authorize a release or package publication.

## Required evidence

- Review all changes against main and preserve project history.
- Confirm standalone and actual-engine tests, schema validation, documentation checks and static/format checks.
- Inspect hosted CI results for the exact release commit and supported Python versions.
- Build a wheel, inspect metadata/bundled schemas/license and test installation outside the source checkout without optional dependencies.
- Install the optional parser extra and verify doctor, audit and comparison against the pinned independent Tamandua checkout.
- Execute the published quick-start/tutorial commands in a new output directory.
- Record tested versions, limits, unresolved issues and relevant dependency/advisory checks.
- Review license/attribution, synthetic fixtures and absence of private user data.
- Update changelog, compatibility table and version consistently.

## Delivery

Merge only with explicit authorization. Tag/publish a GitHub release or package only with explicit release authorization. Attach verified artifacts and their checksums if distribution is approved. Do not claim hosted CI success, public package availability or new-task cloud restoration from local checks alone.

The original master prompt's full scientific document-evaluation ambition remains larger than this traceability release; do not label missing extraction/scoring/scientific validation as delivered.
