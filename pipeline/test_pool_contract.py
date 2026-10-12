import json
import tempfile
import unittest
from pathlib import Path

from pool_contract import manifest, pairs, publication_gate, row_gate


class PoolContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.package = Path(self.tmp.name) / "problem"
        (self.package / "tests").mkdir(parents=True)
        (self.package / "samples").mkdir()
        (self.package / "meta.json").write_text(json.dumps({"id": "123A", "rating": 1200}))
        (self.package / "provenance.json").write_text("{}")
        (self.package / "statement.html").write_text("statement")
        (self.package / "samples/1.in").write_text("1\n")
        (self.package / "samples/1.out").write_text("2\n")
        (self.package / "tests/1.in").write_text("1\n")
        (self.package / "tests/1.out").write_text("2\n")

    def test_sample_only_never_qualifies(self):
        with self.assertRaisesRegex(ValueError, "samples-only"):
            manifest(self.package)

    def test_extra_test_pair_is_not_independent_evidence(self):
        (self.package / "tests/2.in").write_text("3\n")
        (self.package / "tests/2.out").write_text("4\n")
        self.assertIn("tests/2.in", manifest(self.package))
        with self.assertRaises(FileNotFoundError):
            publication_gate(self.package, evidence_root=Path(self.tmp.name) / "missing")

    def test_missing_output_fails_closed(self):
        (self.package / "tests/2.in").write_text("3\n")
        with self.assertRaisesRegex(ValueError, "unpaired"):
            manifest(self.package)

    def test_symlink_and_unlisted_files_fail(self):
        (self.package / "tests/2.in").write_text("3\n")
        (self.package / "tests/2.out").write_text("4\n")
        (self.package / "tests/ref.in").symlink_to(self.package / "samples/1.in")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            manifest(self.package)
        (self.package / "tests/ref.in").unlink()
        (self.package / "bad.py").write_text("print('unexpected')")
        with self.assertRaisesRegex(ValueError, "unexpected package byte"):
            manifest(self.package)

    def test_truncated_pairs_are_rejected(self):
        for input_text in ["...", "[truncated]", "input truncated", "output truncated", "   "]:
            with self.subTest(input_text=input_text):
                with self.assertRaises(ValueError):
                    pairs([{"input": input_text, "output": "hello"}])

    def test_incomplete_official_tests_require_generated_basis(self):
        row = {
            "id": "123A", "title": "Example", "description": "Description", "input_format": "numbers",
            "output_format": "number", "interaction_format": None, "input_mode": "stdio",
            "time_limit": 2, "memory_limit": 256, "generated_checker": False,
            "official_tests": [{"input": "1", "output": "2"}],
            "examples": [{"input": "1", "output": "2"}], "official_tests_complete": False,
        }
        with self.assertRaises(ValueError):
            row_gate(row)
        row_gate(row, allow_authored=True)
        row["generated_checker"] = "checker"
        with self.assertRaisesRegex(ValueError, "checker"):
            row_gate(row, allow_authored=True)


if __name__ == "__main__":
    unittest.main()
