# Armadillo documentation

![Armadillo product artwork featuring an armadillo scientist in the Brazilian Cerrado](../assets/armadillo-banner.png)

*Product artwork. The implemented workflow and its limitations are described below.*

## The problem this product addresses

Researchers and reviewers need to explain which source passages were used to support a claim, who annotated them and what changed between revisions. When that information lives in disconnected notes, reviews are difficult to reproduce and changes in evidence are easy to overlook.

## How it works

Armadillo preserves an original text/Markdown document, lets reviewers annotate exact claim/evidence spans, checks quotation presence and declared links, and generates reproducible reports with source context and authorship metadata. Comparing snapshots exposes changes in annotations and declared support. Optional integration with the independently installed Tamandua CLI adds actual RDF closure, graph-impact calculations and explanation paths.

The result is an inspectable source-to-annotation-to-report workflow. It does not replace expert review or prove scientific truth. Current capabilities require manual annotation; automated extraction, search and grading remain outside the implemented scope.

Version 0.2.0 is available as source on main, without a published package release. This index points to current instructions; older reports remain historical engineering evidence.

## Use Armadillo

- [Quick start](QUICKSTART.md): import a document, select source spans and generate a report.
- [Installation](INSTALLATION.md): standalone, optional integration and troubleshooting.
- [User tutorial](TUTORIAL.md): source integrity, annotation revisions and review.
- [CLI reference](CLI.md): commands, options, errors and output behavior.
- [Scientific assumptions](SCIENTIFIC_ASSUMPTIONS.md): what source/graph observations do not establish.
- [Limitations](LIMITATIONS.md): what the findings do and do not establish.

## Connect Tamandua

- [Connection guide](integrations/TAMANDUA.md): repository, exact revision, build, diagnostic and real workflows.
- [Integration tutorial](TAMANDUA_TUTORIAL.md): complete executable walkthrough.
- [RDF/closure contract](integrations/INTERFACE_CONTRACT.md): parsing, response validation and limits.
- [Comparison contract](integrations/ANNOTATION_COMPARISON.md): stable IDs, graph changes and explanations.
- [Compatibility](integrations/COMPATIBILITY.md): software and schema versions.

## Develop and validate

- [Developer guide](DEVELOPER_GUIDE.md) and [actual API](API.md).
- [Architecture](architecture/INTEGRATION_ARCHITECTURE.md) and [editable diagrams](diagrams/README.md).
- [Dependency inventory](DEPENDENCIES.md), [test strategy](testing/TEST_STRATEGY.md) and [current results](testing/DOCUMENT_WORKFLOW_RESULTS.md).
- [Release checklist](RELEASE_CHECKLIST.md), [decisions](DECISIONS.md) and [roadmap](ROADMAP.md).

## Project context and historical records

- [Product vision](PRODUCT_VISION.md) and [features](FEATURES.md).
- [Initial Armadillo audit](audit/REPOSITORY_AUDIT.md), [Tamandua audit](audit/TAMANDUA_AUDIT.md), [reference analysis](audit/REFERENCE_ANALYSIS.md) and [comparison](audit/FEATURE_COMPARISON.md).
- Earlier [implementation report](IMPLEMENTATION_REPORT.md), [hardening results](testing/HARDENING_RESULTS.md) and [comparison results](testing/COMPARISON_RESULTS.md) describe their recorded commits, not the latest counts or delivery state.
