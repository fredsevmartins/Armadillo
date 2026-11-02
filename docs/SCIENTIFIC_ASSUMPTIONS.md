# Scientific and interpretive assumptions

Armadillo currently performs deterministic source traceability and structural graph exchange. It does not implement a validated scientific score, statistical model, automated fact checker or causal inference system.

## Observations and non-observations

| Observation | Supported interpretation | Unsupported interpretation |
|---|---|---|
| A quote occurs in source | Exact substring presence | The quoted statement is true |
| A user labels evidence as supporting a claim | A declared relationship exists | The evidence logically entails the claim |
| Multiple nodes repeat a quote | Multiple annotations reference matching text | Independent corroborating sources exist |
| Tamandua infers a class membership | Its bounded RDFS rules derive that triple | Scientific causality or document quality is established |
| An inference is invalidated by a graph plan | No longer derivable under the proposed assertions/rules | The proposition is false |
| A source hash matches | Embedded UTF-8 bytes match the recorded digest | The author/source is authentic or trusted |

## Status cases

An empty annotation graph requires review. Claims without source-present declared evidence require review. Missing quotes require review. A nonempty evidence-only graph can be SOURCE_LINKED because there are no unsupported claims to check. Contradictory user-labeled evidence can also be SOURCE_LINKED if all quotations occur. These follow the explicit presence contract, not a semantic approval policy.

Selected source spans, author labels and revisions improve reviewability. Author labels are not authentication, and last_edit is not a complete signed audit history. Preserve versioned inputs for reproducibility.

## Numerical and data integrity

No numeric scientific calculations or unit conversions are performed. There is no score, calibration curve, confidence interval or random seed. Hashes identify defined byte/serialization representations, not universal semantic equivalence. Tests of discrete source/span/graph outcomes use exact expected values rather than invented numerical tolerances.

UTF-8 source content is not normalized. Codepoint offsets differ from byte positions, grapheme clusters and rendered PDF/Markdown locations. Metadata/graph changes are explicit, and source text changes require a new prepared snapshot. RDF parser term comparison does not normalize the original source used by the quote audit.

## Future evaluation

Argument extraction, semantic support assessment or grading would require a documented method, appropriately licensed labeled data, independent reference cases, error analysis and human review. Reference-project claims/benchmarks are not inherited validation evidence. These capabilities remain unimplemented and must not be advertised as delivered.
