# Security policy

For the current unreleased 0.2.0 development version use GitHub private vulnerability reporting if enabled, or the owner's available private contact. No dedicated response SLA. Do not post private documents/credentials in issues.

Untrusted JSON is strictly validated; regular UTF-8 files are bounded and outputs exclusively created. No pickle/eval/shell/network is used. Files are operator-selected: this CLI is not a multi-user path sandbox. Never redirect stdout onto inputs. JSON fields supply no paths/commands.

Tamandua executable is trusted operator configuration with caller privileges. Bounded capture and timeouts stop overproducing/overdue POSIX process groups but do not sandbox malicious binaries or bound the engine own memory. Temporary graph files contain source quotes in private directories; protect the host. Engine limits/licensing remain independent.

No required secrets/environment files. Python runtime dependencies are empty; this is not proof of no vulnerabilities. External dependency/advisory scans are not claimed.

Reports include original quoted text/context; treat them as sensitive as the source. New output/temp files use private temporary-file permissions and exclusive atomic publication. Optional RDF parsing accepts local N-Triples only. Audit labels remain presence findings, not truth.

Imported source hashes and selected spans detect stale/mismatched content but do not authenticate document authors. Reviewer aliases/revisions are user assertions, not signed identities; retain previous snapshots for history. Source-name metadata is never opened as a file. Repository diagnostics require a clean verified checkout, but do not attest binary build provenance.
