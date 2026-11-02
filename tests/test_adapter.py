import subprocess
import unittest
from unittest.mock import patch

from armadillo.core import AuditError
from armadillo.tamandua import reason


def completed(text, code=0):
    return subprocess.CompletedProcess([], code, text, "")


class AdapterContractTests(unittest.TestCase):
    """Protocol failure tests with mocks; real engine tests are separate."""

    def test_version_mismatch(self):
        with patch("subprocess.run", return_value=completed("tamandua 9.0.0")):
            with self.assertRaisesRegex(AuditError, "version"):
                reason("", "tamandua")

    def test_timeout(self):
        with patch(
            "subprocess.run", side_effect=subprocess.TimeoutExpired("tamandua", 1)
        ):
            with self.assertRaisesRegex(AuditError, "timed out"):
                reason("", "tamandua")

    def test_runtime_error(self):
        with patch("subprocess.run", return_value=completed("", 1)):
            with self.assertRaisesRegex(AuditError, "command failed"):
                reason("", "tamandua")

    def test_invalid_responses(self):
        cases = [
            "{",
            "{}",
            '{"analytical":{}}',
            '{"analytical":{"asserted":[{}],"inferred":[],"derivations":[]}}',
            '{"analytical":{"asserted":[],"inferred":{},"derivations":[]}}',
            '{"analytical":{"asserted":[],"inferred":[],"derivations":{}}}',
        ]
        for response in cases:
            with self.subTest(response=response):
                with patch(
                    "subprocess.run",
                    side_effect=[completed("tamandua 0.1.0"), completed(response)],
                ):
                    with self.assertRaises(AuditError):
                        reason("", "tamandua")

    def test_invalid_configuration(self):
        for timeout in (0, -1, 301, True, "30", float("nan")):
            with self.subTest(timeout=timeout), self.assertRaises(AuditError):
                reason("", "tamandua", timeout)
