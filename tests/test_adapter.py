import unittest
from pathlib import Path
from unittest.mock import patch

from armadillo.core import AuditError
from armadillo.tamandua import reason


def completed(text, code=0):
    return text


class AdapterContractTests(unittest.TestCase):
    """Protocol failure tests with mocks; real engine tests are separate."""

    def test_version_mismatch(self):
        with patch("armadillo.tamandua._run", return_value=completed("tamandua 9.0.0")):
            with self.assertRaisesRegex(AuditError, "version"):
                reason("", "tamandua")

    def _failure_cleans_graph(self, message):
        paths = []

        def failing_run(binary, args, timeout):
            if args == ["--version"]:
                return "tamandua 0.1.0"
            graph = Path(args[1])
            self.assertTrue(graph.is_file())
            paths.append(graph)
            raise AuditError(message)

        with patch("armadillo.tamandua._run", side_effect=failing_run):
            with self.assertRaisesRegex(AuditError, message):
                reason("", "tamandua")
        self.assertEqual(len(paths), 1)
        self.assertFalse(paths[0].parent.exists())

    def test_timeout(self):
        self._failure_cleans_graph("Tamandua timed out")

    def test_runtime_error(self):
        self._failure_cleans_graph("Tamandua command failed")

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
                    "armadillo.tamandua._run",
                    side_effect=[completed("tamandua 0.1.0"), completed(response)],
                ):
                    with self.assertRaises(AuditError):
                        reason("", "tamandua")

    def test_invalid_configuration(self):
        for timeout in (0, -1, 301, True, "30", float("nan")):
            with self.subTest(timeout=timeout), self.assertRaises(AuditError):
                reason("", "tamandua", timeout)
