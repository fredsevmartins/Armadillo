# Compatibility

| Component | Support / evidence |
|---|---|
| Armadillo | 0.1.0; input 1.0, report/adapter 1.1 |
| Python | Requires 3.11+; locally tested 3.12.14 |
| Tamandua | 0.1.0; commit 09970fb8985e6065cc24ff5507a8de161c301ee9 |
| Rust | 1.90.0 locked Tamandua build |
| Other engines/versions | Rejected, unverified |
| OS | Linux x86_64 tested; macOS/Windows not executed |
| CI | Python 3.11/3.12/3.13 plus pinned real integration defined; remote execution unverified |

Zero runtime Python dependencies. Tamandua retains its Cargo.lock and separate lifecycle. Historical dominox package naming does not require the owner's separate DominoX project.

Optional parser pins: RDFLib 7.1.4 and pyparsing 3.3.2; install the tamandua extra. POSIX process capture is required for integration; Windows is not supported for that adapter yet.
