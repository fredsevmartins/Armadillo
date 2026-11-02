# Security policy

For 0.1.x use GitHub private vulnerability reporting if enabled, or the owner's available private contact. No dedicated response SLA. Do not post private documents/credentials in issues.

Untrusted JSON is strictly validated; regular UTF-8 files are bounded and outputs exclusively created. No pickle/eval/shell/network is used. Files are operator-selected: this CLI is not a multi-user path sandbox. Never redirect stdout onto inputs. JSON fields supply no paths/commands.

Tamandua executable is trusted operator configuration with caller privileges. Timeout and post-capture size checks do not sandbox malicious binaries or hard-bound peak memory. Temporary graph files contain source quotes in private directories; protect the host. Engine limits/licensing remain independent.

No required secrets/environment files. Python runtime dependencies are empty; this is not proof of no vulnerabilities. External dependency/advisory scans are not claimed.
