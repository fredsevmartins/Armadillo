"""Optional file/CLI adapter for verified Tamandua 0.1.0."""

import tempfile
from pathlib import Path

from .core import AuditError, digest, fields, parse_json
from .process import run as _run


def _triple(triple):
    fields(triple, ("subject", "predicate", "object"))
    if any(not isinstance(v, str) or not v for v in triple.values()):
        raise AuditError("Incompatible Tamandua triple")
    return tuple(triple[k] for k in ("subject", "predicate", "object"))


def _rdf_set(text):
    if not text.strip():
        return set()
    try:
        from rdflib import Graph, BNode
    except ImportError as exc:
        raise AuditError(
            "Install optional integration dependencies: pip install 'armadillo-evidence[tamandua]'"
        ) from exc
    try:

        class Labels(dict):
            def get(self, key, default=None):
                return BNode(key)

        return set(Graph().parse(data=text, format="nt", bnode_context=Labels()))
    except Exception as exc:
        raise AuditError("Invalid N-Triples input/response: " + str(exc)[:500]) from exc


def preflight(nt):
    if not isinstance(nt, str):
        raise AuditError("RDF input must be text")
    try:
        size = len(nt.encode("utf-8"))
    except UnicodeError as exc:
        raise AuditError("RDF input must contain valid Unicode") from exc
    if size > 2 * 1024 * 1024:
        raise AuditError(
            f"Integration RDF exceeds 2 MiB ({size} bytes); reduce links or run without --tamandua"
        )
    triples = _rdf_set(nt)
    if len(triples) > 20000:
        raise AuditError(
            "Integration exceeds 20000 asserted triples; reduce links or run standalone"
        )
    return triples


def reason(nt, binary, timeout=30):
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or not 0 < timeout <= 300
    ):
        raise AuditError("timeout must be in (0, 300] seconds")
    submitted = preflight(nt)
    version = _run(binary, ["--version"], timeout).strip()
    if version != "dominox 0.1.0" and version != "tamandua 0.1.0":
        raise AuditError("Unsupported Tamandua version; expected 0.1.0")
    with tempfile.TemporaryDirectory(prefix="armadillo-") as directory:
        graph = Path(directory) / "graph.nt"
        graph.write_text(nt, encoding="utf-8")
        response = parse_json(_run(binary, ["reason", str(graph)], timeout))
    if not isinstance(response, dict) or not isinstance(
        response.get("analytical"), dict
    ):
        raise AuditError("Incompatible Tamandua response envelope")
    analytical = response["analytical"]
    if set(analytical) != {"asserted", "inferred", "derivations"}:
        raise AuditError("Incompatible Tamandua closure fields")
    for key in ("asserted", "inferred"):
        if not isinstance(analytical[key], list):
            raise AuditError("Incompatible Tamandua triple list")
        for triple in analytical[key]:
            _triple(triple)
    if not isinstance(analytical["derivations"], list):
        raise AuditError("Incompatible Tamandua provenance")
    sets = {}
    for key in ("asserted", "inferred"):
        raw = [_triple(t) for t in analytical[key]]
        if len(raw) != len(set(raw)):
            raise AuditError("Duplicate triples in Tamandua " + key)
        text = "\n".join(" ".join(t) + " ." for t in raw)
        parsed = _rdf_set(text)
        if len(parsed) != len(raw):
            raise AuditError("Noncanonical or duplicate RDF terms in Tamandua response")
        sets[key] = parsed
    if sets["asserted"] != submitted:
        raise AuditError("Tamandua assertions do not match submitted graph")
    if sets["asserted"] & sets["inferred"]:
        raise AuditError("Tamandua asserted and inferred sets overlap")
    if len(sets["asserted"]) + len(sets["inferred"]) > 20000:
        raise AuditError("Tamandua closure exceeds 20000 triples")
    known = {_triple(t) for key in ("asserted", "inferred") for t in analytical[key]}
    conclusions = set()
    for derivation in analytical["derivations"]:
        fields(derivation, ("conclusion", "alternatives"))
        conclusion = _triple(derivation["conclusion"])
        if conclusion in conclusions:
            raise AuditError("Duplicate provenance conclusion")
        conclusions.add(conclusion)
        if conclusion not in known:
            raise AuditError("Provenance conclusion absent from closure")
        alternatives = derivation["alternatives"]
        if not isinstance(alternatives, list) or not alternatives:
            raise AuditError("Invalid provenance alternatives")
        for alternative in alternatives:
            fields(alternative, ("rule", "premises"))
            if alternative["rule"] not in (
                "subclass-transitivity",
                "subproperty-transitivity",
                "class-membership",
                "property-propagation",
                "domain",
                "range",
            ):
                raise AuditError("Invalid provenance rule")
            premises = alternative["premises"]
            if not isinstance(premises, list) or len(premises) != 2:
                raise AuditError("Invalid provenance premises")
            if any(_triple(p) not in known for p in premises):
                raise AuditError("Provenance premise absent from closure")
    if not {_triple(t) for t in analytical["inferred"]} <= conclusions:
        raise AuditError("Missing provenance for inferred triples")
    # Exclude runtime timestamp from deterministic analytical output.
    return {
        "contract_version": "1.1",
        "engine": version,
        "rdf_sha256": digest(nt),
        "analytical": analytical,
    }
