import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from armadillo.connection import (
    SUPPORTED_COMMIT,
    _identity,
    doctor,
    repository_binary,
    resolve,
)
from armadillo.core import AuditError


class ConnectionTests(unittest.TestCase):
    def test_remote_identity_without_disclosing_userinfo(self):
        self.assertEqual(
            _identity("https://synthetic:dummy@github.com/fredsevmartins/Tamandua.git"),
            "fredsevmartins/tamandua",
        )
        self.assertEqual(
            _identity("git@github.com:fredsevmartins/Tamandua.git"),
            "fredsevmartins/tamandua",
        )
        self.assertIsNone(
            _identity("https://github.com.attacker.invalid/fredsevmartins/Tamandua")
        )

    def test_explicit_choice_and_timeout_validation(self):
        with self.assertRaises(AuditError):
            resolve("binary", "repo")
        with self.assertRaises(AuditError):
            doctor()
        for timeout in (0, -1, float("inf"), float("nan"), True, "30"):
            with self.subTest(timeout=timeout), self.assertRaises(AuditError):
                resolve(repository="missing", timeout=timeout)

    def test_checkout_revision_origin_dirty_and_build_guards(self):
        # Mocked local Git metadata; real checkout/binary checks are in the real suite.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = [
                str(root),
                "https://github.com/fredsevmartins/Tamandua.git",
                SUPPORTED_COMMIT,
                "",
            ]
            with (
                patch("armadillo.connection.run", side_effect=base),
                self.assertRaisesRegex(AuditError, "not built"),
            ):
                repository_binary(root)
            executable = root / "target/debug/tamandua"
            executable.parent.mkdir(parents=True)
            executable.write_text("synthetic test placeholder, never executed")
            with patch("armadillo.connection.run", side_effect=base):
                self.assertEqual(
                    repository_binary(root), (executable, SUPPORTED_COMMIT)
                )
            for values in (
                [str(root), "https://github.com/other/other.git"],
                [str(root), base[1], "a" * 40],
                [str(root), base[1], SUPPORTED_COMMIT, " M Cargo.toml"],
            ):
                with (
                    self.subTest(values=values),
                    patch("armadillo.connection.run", side_effect=values),
                    self.assertRaises(AuditError),
                ):
                    repository_binary(root)
