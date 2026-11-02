#!/usr/bin/env bash
set -euo pipefail
cd /workspace/Armadillo
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install setuptools==84.0.0 wheel==0.48.0 ruff==0.14.3 jsonschema==4.26.0
.venv/bin/python -m pip install --no-build-isolation -e '.[tamandua]'
export CARGO_HOME=/workspace/.armadillo-tools/cargo
export RUSTUP_HOME=/workspace/.armadillo-tools/rustup
export PATH="$CARGO_HOME/bin:$PATH"
if ! command -v rustup >/dev/null 2>&1; then
    installer=$(mktemp /tmp/armadillo-rustup.XXXXXX)
    trap 'rm -f "$installer"' EXIT
    curl --fail --silent --show-error https://sh.rustup.rs -o "$installer"
    sh "$installer" -y --no-modify-path --profile minimal --default-toolchain 1.90.0
fi
rustup toolchain install 1.90.0 --profile minimal
cd /workspace/Tamandua
test "$(git rev-parse HEAD)" = 09970fb8985e6065cc24ff5507a8de161c301ee9
cargo +1.90.0 test --locked --workspace -j 4
cargo +1.90.0 build --locked --bin tamandua -j 4
cd /workspace/Armadillo
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tests/real_tamandua.py -v
.venv/bin/ruff check src tests scripts
.venv/bin/ruff format --check src tests scripts
.venv/bin/python scripts/check_docs.py

.venv/bin/python scripts/check_contracts.py --tamandua /workspace/Tamandua/target/debug/tamandua
