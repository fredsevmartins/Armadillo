"""Bound both process streams during capture (supported runtime: POSIX)."""

import os
import selectors
import signal
import subprocess
import time

from .core import AuditError


def run(binary, args, timeout, stdout_limit=16 * 1024 * 1024, stderr_limit=64 * 1024):
    if os.name != "posix":
        raise AuditError("Tamandua integration currently requires a POSIX platform")
    process = None
    completed = False
    try:
        process = subprocess.Popen(
            [str(binary), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        chunks = {"stdout": bytearray(), "stderr": bytearray()}
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, "stdout")
            selector.register(process.stderr, selectors.EVENT_READ, "stderr")
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise AuditError(
                        "Tamandua timed out; standalone audit remains available"
                    )
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    target = chunks[key.data]
                    limit = stdout_limit if key.data == "stdout" else stderr_limit
                    if len(target) + len(chunk) > limit:
                        raise AuditError(
                            "Tamandua " + key.data + " exceeds capture limit"
                        )
                    target.extend(chunk)
            try:
                code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired as exc:
                raise AuditError("Tamandua timed out") from exc
        stdout = chunks["stdout"].decode("utf-8")
        stderr = chunks["stderr"].decode("utf-8", errors="replace")
        if code:
            # Escape terminal controls; retain bounded syntax/limit diagnostics.
            detail = "".join(c if c.isprintable() else " " for c in stderr)[:1000]
            raise AuditError(f"Tamandua command failed (exit {code}): {detail}")
        completed = True
        return stdout
    except FileNotFoundError as exc:
        raise AuditError(
            "Tamandua executable not found; install it or omit --tamandua"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise AuditError("Cannot execute Tamandua: " + str(exc)) from exc
    finally:
        if process is not None:
            # Also stop descendants holding inherited pipes after parent exit.
            if not completed:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.wait()
            process.stdout.close()
            process.stderr.close()
