# Document workflow and repository-connection results

Date: 2026-11-02. Package: 0.2.0, unreleased. Development branch: feat/reliable-evidence-reports; this phase starts from 38d3803949e903e03d662ff947e62f3e380291e9. No release/merge/hosted-CI success is implied.

## Delivered capabilities

UTF-8 TXT/Markdown preparation, explicit add/replace/delete span annotation, original source hashes, reviewer/revision/selected-span metadata, latest-edit provenance, exact-quote reports, same-document comparison and verified connection to the independent Tamandua checkout. Input 1.0 remains supported; new metadata uses input 1.1, report 1.2 and comparison 1.1. Closure/impact contracts remain 1.1/1.0; connection diagnostic is 1.0.

Professional English documentation now has a navigation index, quick start, installation/CLI/API references, executable reviewer tutorial, actual Tamandua build/connection guide, compatibility/limits/dependencies, scientific assumptions, architecture diagrams and release checklist. Historical evidence is explicitly distinguished from current instructions.

## Executed tests

| Module / suite | Executed | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| test_adapter | 5 | 5 | 0 | 0 |
| test_cli | 6 | 6 | 0 | 0 |
| test_compare | 6 | 6 | 0 | 0 |
| test_connection | 3 | 3 | 0 | 0 |
| test_core | 12 | 12 | 0 | 0 |
| test_documents | 10 | 10 | 0 | 0 |
| test_reliability | 16 | 16 | 0 | 0 |
| test_reports | 5 | 5 | 0 | 0 |
| real_tamandua | 11 | 11 | 0 | 0 |
| **Total unique test methods** | **74** | **74** | **0** | **0** |

Commands: python -m unittest discover -s tests -v (63 cases) and python tests/real_tamandua.py -v (11 cases). Subtests and additional workflow checks are not added to the unique count. Mocked repository metadata/protocol cases are not presented as real engine tests.

Relevant cases verify unchanged UTF-8/BOM/CRLF, explicit codepoint selections, repeated selected quotes, stale-span/source tampering rejection, reviewer metadata, explicit replacements/removals, dangling-link errors, no input mutation, atomic output failure cleanup, bounded process capture and same-document comparisons.

## Actual Tamandua connection

Repository: https://github.com/fredsevmartins/Tamandua. Verified local/remote source commit: 09970fb8985e6065cc24ff5507a8de161c301ee9. The repository's application source was not modified. The existing built 0.1.0 CLI reports "dominox 0.1.0"; separate DominoX code is not required.

doctor --tamandua-repo /workspace/Tamandua returned CONNECTED after local origin/root/revision/clean-tracked-tree checks and an actual subclass inference. Direct executable selection also passed, correctly reporting no checkout provenance. Binary version/behavior checks do not attest how a binary was built.

Imported and authored source audited as SOURCE_LINKED with nine assertions and two inferred class memberships. Comparing a claim-only snapshot with its evidence-added snapshot produced four added assertions and one new inference. Removal/no-op and repeated analytical comparisons also passed in the real suite.

## Additional checks

- Ruff static check and format validation passed.
- Five bundled/public JSON Schemas and eight legacy/new input/report/comparison workflows validated, including actual connection/closure/impact outputs.
- scripts/check_quickstart.py executed the documented preparation, annotation, replacement, deletion, audit and comparison commands with unchanged source bytes and disposable new destinations.
- Clean wheel installation outside the checkout passed the entire standalone tutorial with no optional runtime packages. After installing the two pinned optional wheels, the same clean environment passed the actual repository-connected tutorial.
- Wheel metadata/version and bundled resources were built successfully. Final wheel SHA-256 at this check: e20d7f4b1108702ca7bc4b0526fdec80bec5d6219d0121b312e5febbab2307fb. Rebuilds may differ; compare the actual artifact being distributed.
- All nine editable Mermaid sources parsed successfully using Mermaid 11.4.1 with JSDOM 26.1.0. The initial bare-Node attempt lacked the required DOM; after supplying a DOM, all syntax checks passed. This is syntax validation, not browser rendering/layout proof.

Reproduction commands are in the developer guide. The package audit for unchanged optional RDFLib/pyparsing pins found no known vulnerabilities at the recorded query time (see parser-audit.json); it did not audit all Rust/build/documentation-tool dependencies. No scientific accuracy or coverage percentage is claimed.

## Delivery boundary

GitHub native Git read access worked for both repositories. API access to GitHub Actions still returned Forbidden, so hosted run outcomes could not be confirmed. The implementation remains a review branch until explicitly merged; package/GitHub release publication requires separate authorization. New-task cloud restoration and browser-rendered diagram output are not claimed.

Automatic PDF/argument extraction, semantic scoring, cross-edited-document matching, authenticated collaboration/history and scientific validity assessment remain outside the delivered workflow. Current development is ready for review with those explicit boundaries.

Final managed setup also passed the independent Tamandua suite (14 reasoning tests, recorded separately from the 74 Armadillo tests), all application checks, source-checkout diagnostic and connected quick-start workflow. Boundary regressions verify generated JSON can be read back at the file byte cap, and replacement preserves existing support links unless the caller explicitly provides a new list.
