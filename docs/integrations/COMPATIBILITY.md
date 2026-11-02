# Compatibility

| Component | Supported / verified |
|---|---|
| Armadillo package | 0.2.0, unreleased |
| Input contracts | 1.0 legacy and 1.1 with explicit metadata |
| Report / comparison | 1.2 / 1.1 |
| Closure / impact / connection | 1.1 / 1.0 / 1.0 |
| Python | Requires 3.11+; locally verified 3.12.14 |
| Tamandua | 0.1.0, commit 09970fb8985e6065cc24ff5507a8de161c301ee9 |
| Rust | 1.90.0 locked build/test |
| Optional parser | RDFLib 7.1.4, pyparsing 3.3.2 |
| Runtime integration platform | POSIX; Linux x86_64 verified |
| Other OS / hosted Python versions | Not independently confirmed by local tests |

Unknown engine versions and checkout revisions are rejected until verified. Historical dominox package naming is accepted for the actual Tamandua CLI, without requiring the separate DominoX project.

The checkout diagnostic verifies origin/revision/working-tree state and actual behavior, not binary build attestation. --tamandua allows an explicitly trusted separately installed executable; it reports no checkout provenance.

The current branch is not a published release. See [current results](../testing/DOCUMENT_WORKFLOW_RESULTS.md) and [installation](../INSTALLATION.md).
