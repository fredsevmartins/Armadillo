# Synthetic example

input.json is original synthetic MIT data, not a real study. Follow docs/TAMANDUA_TUTORIAL.md from repository root. Expected SOURCE_LINKED, two source-present nodes, one claim; actual engine yields nine assertions and two ArgumentNode inferences. None establishes scientific truth.

Directly executable before.json and after.json demonstrate evidence removal from the same document. Run `armadillo compare examples/tamandua_integration/before.json --against examples/tamandua_integration/after.json --format markdown` from the repository root; add --tamandua PATH for actual impact reasoning. Expected lost supporter: evidence1; source status becomes REVIEW_REQUIRED.
