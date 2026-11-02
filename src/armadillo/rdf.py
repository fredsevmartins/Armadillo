"""Small deterministic N-Triples export; no external RDF parser required."""

from .core import audit, validate

NS = "https://w3id.org/armadillo-evidence/"
TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
SUBCLASS = "http://www.w3.org/2000/01/rdf-schema#subClassOf"


def export_nt(data, identity="snapshot"):
    validate(data)
    report = audit(data)
    if identity not in ("snapshot", "document"):
        from .core import AuditError

        raise AuditError("RDF identity must be snapshot or document")
    key = "input_sha256" if identity == "snapshot" else "document_sha256"
    root = "urn:sha256:" + report[key] + ":"
    rows = []

    def iri(s, p, o):
        rows.append(f"<{s}> <{p}> <{o}> .")

    for kind in ("Claim", "Evidence"):
        iri(NS + kind, SUBCLASS, NS + "ArgumentNode")
    for node in data["nodes"]:
        subject = root + node["id"]
        iri(subject, TYPE, NS + node["kind"].title())
        escapes = {'"': '\\"', "\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"}
        literal = (
            '"'
            + "".join(
                escapes.get(c, f"\\u{ord(c):04x}" if ord(c) < 32 else c)
                for c in node["quote"]
            )
            + '"'
        )
        rows.append(f"<{subject}> <{NS}quote> {literal} .")
        for target in node["supports"]:
            iri(subject, NS + "declaredSupports", root + target)
    # Declared links remain distinct from source-presence findings.
    for finding in report["findings"]:
        if finding["quote_found"]:
            iri(root + finding["id"], TYPE, NS + "SourcePresentNode")
    return "\n".join(sorted(rows)) + "\n"
