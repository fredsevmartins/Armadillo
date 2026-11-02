"""Non-mutating annotation comparison and optional real Tamandua impact plan."""

import tempfile
from pathlib import Path

from .core import AuditError, audit, canonical, digest, fields, parse_json, validate
from .process import run
from .rdf import export_nt
from .tamandua import _triple, reason


def _triples(values):
    if not isinstance(values, list):
        raise AuditError("Invalid impact triple array")
    result = {_triple(t) for t in values}
    if len(result) != len(values):
        raise AuditError("Duplicate impact triples")
    return result


def _records(values):
    return [dict(zip(("subject", "predicate", "object"), t)) for t in sorted(values)]


def _validate_plan(report, before, after, nt, changes):
    required = (
        "engine_version",
        "reasoning_profile",
        "graph_id",
        "input_sha256",
        "proposed_assertions",
        "proposed_inferences",
        "baseline_asserted",
        "baseline_inferred",
        "proposed_asserted",
        "proposed_inferred",
        "changes",
        "impact",
        "explanations",
        "invalidated_explanations",
    )
    if not isinstance(report, dict) or not set(required) <= report.keys():
        raise AuditError("Incompatible Tamandua impact report")
    if report["engine_version"] != "0.1.0" or report["changes"] != changes:
        raise AuditError("Tamandua impact version/changes mismatch")
    if report["input_sha256"] != digest(nt) or report["graph_id"] != "sha256:" + digest(
        nt
    ):
        raise AuditError("Tamandua impact source hash mismatch")
    a0, i0 = (_triples(before[key]) for key in ("asserted", "inferred"))
    a1, i1 = (_triples(after[key]) for key in ("asserted", "inferred"))
    if (
        _triples(report["proposed_assertions"]) != a1
        or _triples(report["proposed_inferences"]) != i1
    ):
        raise AuditError("Tamandua proposed graph does not match requested annotations")
    for name, expected in (
        ("baseline_asserted", len(a0)),
        ("baseline_inferred", len(i0)),
        ("proposed_asserted", len(a1)),
        ("proposed_inferred", len(i1)),
    ):
        if type(report[name]) is not int or report[name] != expected:
            raise AuditError("Tamandua impact count mismatch: " + name)
    expected = {
        "added_assertions": a1 - a0,
        "removed_assertions": a0 - a1,
        "new_inferences": i1 - (a0 | i0),
        "invalidated_inferences": i0 - (a1 | i1),
        "unchanged_inferences": i0 & i1,
    }
    expected["affected_relationships"] = set().union(
        *(
            expected[k]
            for k in (
                "added_assertions",
                "removed_assertions",
                "new_inferences",
                "invalidated_inferences",
            )
        )
    )
    impact = report["impact"]
    fields(impact, (*expected, "affected_entities"))
    for key, triples in expected.items():
        if _triples(impact[key]) != triples:
            raise AuditError("Tamandua impact set mismatch: " + key)
    entities = {
        term
        for triple in expected["affected_relationships"]
        for term in triple
        if term.startswith(("<", "_:"))
    }
    if impact["affected_entities"] != sorted(entities):
        raise AuditError("Tamandua affected entities mismatch")
    for key, roots, status in (
        ("explanations", expected["new_inferences"], "inferred"),
        (
            "invalidated_explanations",
            expected["invalidated_inferences"],
            "no-longer-derivable",
        ),
    ):
        explanations = report[key]
        if not isinstance(explanations, list) or len(explanations) != len(roots):
            raise AuditError("Tamandua impact explanation coverage mismatch")
        seen = set()
        for explanation in explanations:
            fields(explanation, ("triple", "status", "alternatives", "truncated"))
            seen.add(_triple(explanation["triple"]))
            if (
                explanation["status"] != status
                or type(explanation["truncated"]) is not bool
            ):
                raise AuditError("Invalid Tamandua explanation status")
        if seen != roots:
            raise AuditError("Tamandua impact explanation roots mismatch")


def _impact(before_data, after_data, binary, timeout):
    # Stable identities are opt-in for same-document comparisons only.
    before_nt = export_nt(before_data, identity="document")
    after_nt = export_nt(after_data, identity="document")
    before = reason(before_nt, binary, timeout)["analytical"]
    after = reason(after_nt, binary, timeout)["analytical"]
    a0, a1 = _triples(before["asserted"]), _triples(after["asserted"])
    changes = {"add": _records(a1 - a0), "remove": _records(a0 - a1)}
    payload = canonical(changes)
    if len(payload.encode("utf-8")) > 2 * 1024 * 1024:
        raise AuditError("Impact changes exceed 2 MiB; reduce links")
    with tempfile.TemporaryDirectory(prefix="armadillo-impact-") as directory:
        graph, delta = Path(directory) / "graph.nt", Path(directory) / "changes.json"
        graph.write_text(before_nt, encoding="utf-8")
        delta.write_text(payload, encoding="utf-8")
        envelope = parse_json(
            run(binary, ["plan", str(graph), "--changes", str(delta)], timeout)
        )
    if not isinstance(envelope, dict) or not isinstance(
        envelope.get("analytical"), dict
    ):
        raise AuditError("Incompatible Tamandua impact envelope")
    report = envelope["analytical"]
    _validate_plan(report, before, after, before_nt, changes)
    return {
        "contract_version": "1.0",
        "identity_policy": "document-sha256-and-node-id",
        "baseline_rdf_sha256": digest(before_nt),
        "proposed_rdf_sha256": digest(after_nt),
        "analytical": report,
    }


def compare(before, after, binary=None, timeout=30):
    validate(before)
    validate(after)
    if before["document"] != after["document"]:
        raise AuditError(
            "Comparison requires the exact same document; use separate audits for changed documents"
        )
    b, a = audit(before), audit(after)
    old, new = ({n["id"]: n for n in data["nodes"]} for data in (before, after))

    def normalized(node):
        return dict(node, supports=sorted(node["supports"]))

    modified = sorted(
        k for k in old.keys() & new.keys() if normalized(old[k]) != normalized(new[k])
    )
    old_claims, new_claims = (
        {n["id"]: n for n in result["findings"] if n["kind"] == "claim"}
        for result in (b, a)
    )
    support_changes = []
    for claim_id in sorted(old_claims.keys() | new_claims.keys()):
        previous, proposed = old_claims.get(claim_id), new_claims.get(claim_id)
        previous_supporters = (
            set(previous["source_present_supporters"]) if previous else set()
        )
        proposed_supporters = (
            set(proposed["source_present_supporters"]) if proposed else set()
        )
        previous_presence = previous["quote_found"] if previous else None
        proposed_presence = proposed["quote_found"] if proposed else None
        if (
            previous_supporters != proposed_supporters
            or previous_presence != proposed_presence
        ):
            support_changes.append(
                {
                    "claim_id": claim_id,
                    "lost_supporters": sorted(
                        previous_supporters - proposed_supporters
                    ),
                    "gained_supporters": sorted(
                        proposed_supporters - previous_supporters
                    ),
                    "quote_found_before": previous_presence,
                    "quote_found_after": proposed_presence,
                }
            )
    report = {
        "comparison_version": "1.0",
        "document_sha256": b["document_sha256"],
        "baseline_input_sha256": b["input_sha256"],
        "proposed_input_sha256": a["input_sha256"],
        "added_nodes": sorted(new.keys() - old.keys()),
        "removed_nodes": sorted(old.keys() - new.keys()),
        "modified_nodes": modified,
        "claim_support_changes": support_changes,
        "baseline_audit": b,
        "proposed_audit": a,
        "limitations": "Same-document annotation changes only. Node ids are user-maintained identities. Declared support and RDF classification are not truth, causality or evidentiary entailment.",
    }
    if binary is not None:
        report["tamandua_impact"] = _impact(before, after, binary, timeout)
    return report


def markdown(report):
    lines = [
        "# Armadillo annotation comparison",
        "",
        "Document SHA-256: " + report["document_sha256"],
        "",
        "Baseline: **" + report["baseline_audit"]["status"] + "**",
        "",
        "Proposed: **" + report["proposed_audit"]["status"] + "**",
    ]
    for key in ("added_nodes", "removed_nodes", "modified_nodes"):
        lines += [
            "",
            key.replace("_", " ").title() + ": " + (", ".join(report[key]) or "none"),
        ]
    for change in report["claim_support_changes"]:
        lines += [
            "",
            "Declared source support for "
            + change["claim_id"]
            + ": lost "
            + (", ".join(change["lost_supporters"]) or "none")
            + "; gained "
            + (", ".join(change["gained_supporters"]) or "none")
            + f"; quote found {change['quote_found_before']} → {change['quote_found_after']}",
        ]
    if "tamandua_impact" in report:
        impact = report["tamandua_impact"]["analytical"]["impact"]
        lines += ["", "## Tamandua graph impact"]
        for key in (
            "added_assertions",
            "removed_assertions",
            "new_inferences",
            "invalidated_inferences",
            "unchanged_inferences",
        ):
            lines += ["", key.replace("_", " ").title() + ": " + str(len(impact[key]))]
        lines += [
            "",
            "Full graph changes and explanation paths are in the JSON comparison output.",
        ]
    return "\n".join(lines + ["", report["limitations"]]) + "\n"
