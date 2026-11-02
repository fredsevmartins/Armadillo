# Annotation comparison and Tamandua impact contract 1.0

Compare manual annotations of the exact same document without modifying either input. Standalone comparison requires no external package or executable. Optional Tamandua computes actual graph impact using its existing plan command.

## Executable tutorial

From the repository root, after installation:

```bash
armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --format markdown
python -m pip install '.[tamandua]'
armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --tamandua ../Tamandua/target/debug/tamandua --timeout 30 --format markdown
armadillo schema comparison
```

Add --output NEW_REPORT.json (default JSON) or --output NEW_REPORT.md with --format markdown to retain a complete report. Existing files are never replaced. Keep original input JSON and report together for reproducibility.

The example removes evidence1. Expected standalone findings: removed_nodes [evidence1]; claim1 loses that source-present declared supporter; baseline SOURCE_LINKED becomes REVIEW_REQUIRED. Expected real Tamandua result: four removed assertions, one invalidated ArgumentNode inference and one unchanged inference. Reversing before/after adds four assertions and one new inference. Comparing a file with itself produces zero changed relationships.

## Identity and scope

Input documents must match exactly, including whitespace and Unicode. Changed document text is rejected explicitly: use separate audits for it. Users maintain node IDs: reuse an ID only for the same annotation identity; renamed nodes are removals/additions, not automatically matched.

Audit reports and the existing export command retain snapshot identity based on the complete input hash. Comparisons explicitly export with document identity: urn:sha256:DOCUMENT_HASH:NODE_ID. This keeps unchanged node identities stable when only annotations change; it is not identity across edited documents. No hidden cross-document matching or URI rewrite of user files occurs.

Node-order and supports-array order alone do not produce modified-node findings, although the original input SHA-256 still records those JSON array order changes. Claim-support changes list lost/gained source-present declared supporters and quote-presence transitions, using null when the claim does not exist on one side. Source presence is not semantic support.

## Optional engine exchange

The adapter validates both graph closures with the existing reason contract 1.1, derives canonical add/remove triples, then calls Tamandua plan on a private baseline graph and changes JSON. The changes file is capped at 2 MiB. It checks engine version, baseline hash, requested changes, proposed assertions/inferences, counts, impact sets and affected entities against the separately computed closures. Explanation roots, statuses and coverage are checked; recursive explanation semantics remain the trusted engine's responsibility.

Five processes are normally invoked (two version checks, two closures and one plan); --timeout applies per process, not to the whole comparison. Existing stdout/stderr caps, cleanup, version restrictions and input/closure budgets apply. No service or network is used. Requested integration failures are explicit; omit --tamandua for standalone comparison.

Impact semantics follow Tamandua: new inferences are proposed inferred facts absent from all baseline knowledge; invalidated inferences are baseline inferred facts absent from all proposed knowledge. Promotion between assertion/inference categories does not itself mean loss of knowledge. No-longer-derivable is not false. These are graph classifications, not scientific conclusions.

## JSON contract

comparison_version 1.0 requires document_sha256, baseline_input_sha256, proposed_input_sha256, added_nodes, removed_nodes, modified_nodes, claim_support_changes, baseline_audit, proposed_audit and limitations. Both audits follow report schema 1.1. Optional tamandua_impact contains impact contract_version 1.0, identity_policy, both source RDF hashes and the native analytical plan (without runtime timestamp).

The offline comparison schema is bundled in the wheel. Runtime validation additionally checks cross-graph relationships that JSON Schema cannot express. Error behavior matches the audit CLI (exit 1 and JSON stderr; invocation errors use exit 2). Neither source JSON nor the engine's graph is persisted or applied.

## Verification

Run python -m unittest discover -s tests -v and python tests/real_tamandua.py -v. The real suite covers actual removal, addition, no-op, explanation roots and deterministic analytical comparisons. Protocol-corruption tests are simulated and labeled separately. Current results are in [COMPARISON_RESULTS.md](../testing/COMPARISON_RESULTS.md).
