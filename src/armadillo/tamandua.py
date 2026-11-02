"""Optional file/CLI adapter for verified Tamandua 0.1.0."""

import subprocess
import tempfile
from pathlib import Path

from .core import AuditError, digest, fields, parse_json


def _triple(triple):
    fields(triple, ("subject", "predicate", "object"))
    if any(not isinstance(v, str) or not v for v in triple.values()):
        raise AuditError("Incompatible Tamandua triple")
    return tuple(triple[k] for k in ("subject", "predicate", "object"))


def _run(binary, args, timeout):
    try:
        # Trusted operator-selected executable, never a shell command.
        result = subprocess.run(
            [str(binary), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AuditError(
            "Tamandua executable not found; install it or omit --tamandua"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise AuditError(
            "Tamandua timed out; standalone audit remains available"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise AuditError("Cannot execute Tamandua") from exc
    if result.returncode:
        raise AuditError(
            "Tamandua command failed (exit " + str(result.returncode) + ")"
        )
    if len(result.stdout.encode("utf-8")) > 16 * 1024 * 1024:
        raise AuditError("Tamandua response exceeds 16 MiB")
    return result.stdout


def reason(nt, binary, timeout=30):
    if not isinstance(nt, str) or len(nt.encode("utf-8")) > 2 * 1024 * 1024:
        raise AuditError("RDF input must be text of at most 2 MiB")
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or not 0 < timeout <= 300
    ):
        raise AuditError("timeout must be in (0, 300] seconds")
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
    known = {_triple(t) for key in ("asserted", "inferred") for t in analytical[key]}
    for derivation in analytical["derivations"]:
        fields(derivation, ("conclusion", "alternatives"))
        if _triple(derivation["conclusion"]) not in known:
            raise AuditError("Provenance conclusion absent from closure")
        alternatives = derivation["alternatives"]
        if not isinstance(alternatives, list) or not alternatives:
            raise AuditError("Invalid provenance alternatives")
        for alternative in alternatives:
            fields(alternative, ("rule", "premises"))
            if not isinstance(alternative["rule"], str) or not alternative["rule"]:
                raise AuditError("Invalid provenance rule")
            premises = alternative["premises"]
            if not isinstance(premises, list) or len(premises) != 2:
                raise AuditError("Invalid provenance premises")
            if any(_triple(p) not in known for p in premises):
                raise AuditError("Provenance premise absent from closure")
    # Exclude runtime timestamp from deterministic analytical output.
    return {
        "contract_version": "1.0",
        "engine": version,
        "rdf_sha256": digest(nt),
        "analytical": analytical,
    }
