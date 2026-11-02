# End-to-end Tamandua tutorial

Follow the [connection guide](integrations/TAMANDUA.md) to install both projects and build the pinned engine. Run the [document quick start](QUICKSTART.md) to produce claims.json and annotated.json without editing the source.

## 1. Check the connection

```bash
armadillo doctor --tamandua-repo ../Tamandua
```

Expected: CONNECTED, the verified checkout commit, engine "dominox 0.1.0" and actual-rdfs-subclass-inference. The diagnostic is functional evidence, not binary provenance attestation.

## 2. Audit with actual graph reasoning

```bash
armadillo audit annotated.json --tamandua-repo ../Tamandua --format markdown --output connected-review.md
```

The report retains source provenance, selected spans and explicit annotation authors. The example yields SOURCE_LINKED with nine assertions and two inferred ArgumentNode memberships. Exact quote presence and graph membership do not establish truth.

## 3. Compare annotation versions

```bash
armadillo compare claims.json --against annotated.json --tamandua-repo ../Tamandua --format markdown --output connected-impact.md
armadillo compare claims.json --against annotated.json --tamandua-repo ../Tamandua --output connected-impact.json
```

Expected: evidence1 added, claim1 gains a declared source-present supporter, four added RDF assertions and one new class-membership inference. JSON includes the native plan, affected entities and explanation paths. Reversing the files removes that evidence and invalidates its classification; no-longer-derivable does not mean false.

## 4. Verify independently

```bash
python -m unittest discover -s tests -v
python tests/real_tamandua.py -v
python scripts/check_contracts.py --tamandua ../Tamandua/target/debug/tamandua
```

The real suite checks source-checkout connection, document preparation/authorship, closure, removal/addition/no-op plans, literal roundtrips and repeated analytical equality. It fails if required prerequisites are absent. For alternate test paths set TAMANDUA_BINARY and TAMANDUA_REPOSITORY explicitly; neither variable is required by the application.

## Common failures

Wrong repository/revision or tracked changes: use the verified clean checkout without discarding user work. Missing executable: build the engine. Unsupported version or invalid reply: stop and investigate; do not disable validation. Limit/timeout: reduce input or increase the per-process timeout within its bounds. Need standalone review: omit the Tamandua option. Existing output: choose a new path.

These steps execute the existing CLI, not a mock server or unimplemented endpoint.
