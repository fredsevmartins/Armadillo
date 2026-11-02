"""Explicit, read-only connection to the independently installed Tamandua checkout."""

import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

from .core import AuditError
from .process import run
from .tamandua import reason

SUPPORTED_COMMIT = "09970fb8985e6065cc24ff5507a8de161c301ee9"
REPOSITORY = "https://github.com/fredsevmartins/Tamandua"


def _identity(remote):
    if remote.startswith("git@github.com:"):
        return remote.split(":", 1)[1].removesuffix(".git").strip("/").lower()
    url = urlsplit(remote)
    if url.scheme in ("https", "ssh") and url.hostname == "github.com":
        return url.path.strip("/").removesuffix(".git").lower()
    return None


def repository_binary(root, timeout=30):
    _timeout(timeout)
    if shutil.which("git") is None:
        raise AuditError(
            "Git is required for checkout verification; use --tamandua for a trusted executable"
        )
    root = Path(root).resolve()
    if not root.is_dir():
        raise AuditError("Tamandua checkout directory not found")
    top = run("git", ["-C", str(root), "rev-parse", "--show-toplevel"], timeout).strip()
    if Path(top).resolve() != root:
        raise AuditError("--tamandua-repo must select the checkout root")
    remote = run(
        "git", ["-C", str(root), "remote", "get-url", "origin"], timeout
    ).strip()
    if _identity(remote) != "fredsevmartins/tamandua":
        raise AuditError(
            "Selected checkout is not the expected GitHub Tamandua repository"
        )
    commit = run("git", ["-C", str(root), "rev-parse", "HEAD"], timeout).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or commit != SUPPORTED_COMMIT:
        raise AuditError(
            "Unverified Tamandua checkout revision; expected " + SUPPORTED_COMMIT
        )
    changes = run(
        "git",
        ["-C", str(root), "status", "--porcelain", "--untracked-files=no"],
        timeout,
    )
    if changes.strip():
        raise AuditError(
            "Tamandua checkout has tracked changes; use --tamandua for an explicitly trusted custom build"
        )
    for profile in ("release", "debug"):
        binary = root / "target" / profile / "tamandua"
        if binary.is_file():
            return binary, commit
    raise AuditError(
        "Tamandua is not built; from its checkout run cargo build --locked --bin tamandua"
    )


def resolve(binary=None, repository=None, timeout=30):
    _timeout(timeout)
    if binary is not None and repository is not None:
        raise AuditError("Choose --tamandua or --tamandua-repo, not both")
    if repository is not None:
        return repository_binary(repository, timeout)[0]
    return Path(binary).resolve() if binary is not None else None


def _timeout(value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0 < value <= 300
    ):
        raise AuditError("timeout must be in (0, 300] seconds")


def doctor(binary=None, repository=None, timeout=30):
    executable = resolve(binary, repository, timeout)
    if executable is None:
        raise AuditError("doctor requires --tamandua PATH or --tamandua-repo CHECKOUT")
    graph = (
        "<urn:armadillo:check:Claim> <http://www.w3.org/2000/01/rdf-schema#subClassOf> "
        "<urn:armadillo:check:Node> .\n<urn:armadillo:check:example> "
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <urn:armadillo:check:Claim> .\n"
    )
    closure = reason(graph, executable, timeout)
    expected = {
        "subject": "<urn:armadillo:check:example>",
        "predicate": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
        "object": "<urn:armadillo:check:Node>",
    }
    if expected not in closure["analytical"]["inferred"]:
        raise AuditError(
            "Tamandua functional check failed: expected subclass inference missing"
        )
    return {
        "connection_version": "1.0",
        "status": "CONNECTED",
        "repository": REPOSITORY,
        "checkout_commit": SUPPORTED_COMMIT if repository is not None else None,
        "engine": closure["engine"],
        "check": "actual-rdfs-subclass-inference",
        "limitations": "Local trusted executable; repository checks do not cryptographically attest the build. No network or source changes.",
    }
