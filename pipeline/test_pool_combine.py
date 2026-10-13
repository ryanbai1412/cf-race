import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

from pool_combine import extract, relative_name, replay, replay_snapshot, verify_manifest
from pool_contract import digest, manifest, write_json
from pool_sandbox import COMPILER_FLAGS, EXECUTION_VERSION, IMAGE
from pool_sources import PINS, sha_file


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def archive(self, names, kind=None):
        path = self.root / "archive.tar.gz"
        with tarfile.open(path, "w:gz") as tar:
            for name in names:
                member = tarfile.TarInfo(name)
                member.size = 3
                if kind:
                    member.type = kind
                    member.linkname = "safe"
                    member.size = 0
                tar.addfile(member, io.BytesIO(b"abc"))
        return path

    def unpack(self, path, **kwargs):
        return extract(path, self.root / "restored", sha_file(path), **kwargs)

    def test_round_trip_and_manifest(self):
        path = self.archive(["safe/file"])
        result = self.unpack(path)
        self.assertEqual(verify_manifest(self.root / "restored", result["files"]), 1)
        self.assertEqual((self.root / "restored/safe/file").read_bytes(), b"abc")

    def test_traversal_and_absolute_names(self):
        for name in ("../evil", "/evil", "safe/../../evil", "a/./b", "a\\b", "C:/evil", "a//b", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                relative_name(name)

    def test_bad_hash(self):
        path = self.archive(["safe"])
        with self.assertRaisesRegex(ValueError, "SHA256"):
            extract(path, self.root / "restored", "0" * 64)
        self.assertFalse((self.root / "restored").exists())

    def test_truncated_gzip_even_with_current_sha(self):
        path = self.archive(["safe"])
        path.write_bytes(path.read_bytes()[:-8])
        with self.assertRaises(EOFError):
            self.unpack(path)
        self.assertFalse((self.root / "restored").exists())

    def test_corrupt_gzip_footer_even_with_current_sha(self):
        path = self.archive(["safe"])
        raw = bytearray(path.read_bytes()); raw[-8] ^= 1; path.write_bytes(raw)
        with self.assertRaises(OSError):
            self.unpack(path)
        self.assertFalse((self.root / "restored").exists())

    def test_expansion_after_tar_terminator_is_bounded(self):
        path = self.archive(["safe"])
        raw = gzip.decompress(path.read_bytes()) + b"x" * 20000
        path.write_bytes(gzip.compress(raw))
        with self.assertRaises(ValueError):
            self.unpack(path, max_bytes=1024)

    def test_duplicate_member(self):
        with self.assertRaises(ValueError):
            self.unpack(self.archive(["safe", "safe"]))
        self.assertFalse((self.root / "restored").exists())

    def test_links_and_special_files(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.unpack(self.archive(["safe"], kind))

    def test_size_bound(self):
        with self.assertRaises(ValueError):
            self.unpack(self.archive(["safe"]), max_bytes=2)

    def test_member_bound(self):
        with self.assertRaises(ValueError):
            self.unpack(self.archive(["safe", "other"]), max_members=1)

    def test_existing_destination(self):
        (self.root / "restored").mkdir()
        with self.assertRaises(ValueError):
            self.unpack(self.archive(["safe"]))

    def test_destination_symlink(self):
        (self.root / "link").symlink_to(self.root, target_is_directory=True)
        path = self.archive(["safe"])
        with self.assertRaises(ValueError):
            extract(path, self.root / "link/new", sha_file(path))

    def test_manifest_changed_and_undeclared_bytes(self):
        result = self.unpack(self.archive(["safe"]))
        (self.root / "restored/safe").write_bytes(b"xyz")
        with self.assertRaises(ValueError):
            verify_manifest(self.root / "restored", result["files"])
        (self.root / "restored/safe").write_bytes(b"abc")
        (self.root / "restored/extra").write_bytes(b"extra")
        with self.assertRaises(ValueError):
            verify_manifest(self.root / "restored", result["files"])


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        package = self.root / "content/1200/packages/999999A"
        write_json(package / "meta.json", {"id": "999999A", "rating": 1200, "poolPipeline": 1})
        (package / "statement.html").write_text("<p>toy test fixture</p>")
        for folder, raw, answer in (("tests", b"1\n", b"2\n"), ("samples", b"0\n", b"1\n")):
            (package / folder).mkdir()
            (package / folder / "0001.in").write_bytes(raw)
            (package / folder / "0001.out").write_bytes(answer)
        write_json(package / "provenance.json", {"pins": PINS, "apiRating": 1200, "tests": {
            "officialComplete": True, "officialIncluded": 1, "officialAdvertised": 1,
            "generatedIncluded": 0, "generatedAdvertised": 0, "pairs": [{"name": "0001", "origin": "official",
            "inputHash": hashlib.sha256(b"1\n").hexdigest(), "outputHash": hashlib.sha256(b"2\n").hexdigest()}]}})
        ph = digest(manifest(package))
        coverage = {key: [{"test": "0001", "reason": key}] for key in ("boundary", "adversarial", "maxSize")}
        coverage.update(packageHash=ph, inputConstraints="toy", checkerSemantics="unique", statementComplete="toy")
        submissions, sources = [], []
        attribution = {"dataset": "open-r1/codeforces-submissions", "revision": PINS["open-r1/codeforces-submissions"]}
        for i in range(10):
            sid, code = str(i), str(i)
            sh = hashlib.sha256(code.encode()).hexdigest()
            source = self.root / f"content/1200/state/999999A/sources/{sid}.json"
            write_json(source, {"submissionId": sid, "code": code, "sourceHash": sh, "source": attribution})
            sources.append({"submissionId": sid, "path": source.relative_to(self.root).as_posix(), "sha256": sha_file(source)})
            submissions.append({"submissionId": sid, "sourceHash": sh, "source": attribution,
                "expected": "OK" if i < 5 else "WRONG_ANSWER", "compiled": True,
                "verdict": "AC" if i < 5 else "WA", "failedTest": None if i < 5 else "0001",
                "testsRun": 1, "executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS,
                "runs": [{"test": "0001", "verdict": "AC" if i < 5 else "WA", "exitCode": 0,
                          "timeout": False, "outputHash": "a" * 64}]})
        self.evidence = {"schemaVersion": 1, "id": "999999A", "rating": 1200, "files": manifest(package),
            "packageHash": ph, "status": "execution-passed", "stages": ["prepare", "generate", "validate"],
            "acceptedContradiction": False, "coverage": coverage, "submissions": submissions,
            "testCount": 1, "validator": "author", "sandbox": {"image": IMAGE, "network": "none", "bounded": True,
            "executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS,
            "harnessHash": "a" * 64, "runnerHash": "b" * 64, "checkerHash": "c" * 64}}
        self.audit = {"approved": True, "reviewer": "independent", "reviewUrl": "https://example.com/review",
            "packageHash": ph, "evidenceHash": digest(self.evidence), "checks": {key: True for key in
            ("sourceAttribution", "fullTests", "coverage", "fiveAcceptedFiveIncorrect", "noSpecialChecker", "hashes")},
            "incorrectAnalysis": {str(i): {"kind": "wrong-answer", "reason": "toy arithmetic defect"} for i in range(5, 10)}}
        self.ep = self.root / "content/1200/evidence/999999A.json"
        self.ap = self.root / "content/1200/audits/999999A.json"
        write_json(self.ep, self.evidence)
        write_json(self.ap, self.audit)
        entry = {"id": "999999A", "rating": 1200, "status": "technical-validated", "packageHash": ph,
            "evidenceHash": digest(self.evidence), "auditHash": digest(self.audit), "sources": sources,
            "package": "content/1200/packages/999999A", "evidence": "content/1200/evidence/999999A.json",
            "audit": "content/1200/audits/999999A.json", "evidenceRoot": "content",
            "decision": {"path": "content/1200/audits/999999A.json", "selector": [], "recordHash": digest(self.audit)}}
        self.index = {"entries": [entry], "decisions": [{"id": entry["id"], "rating": 1200,
            "status": "technical-validated", "record": copy.deepcopy(entry["decision"])}], "emptyApproval": "empty.json"}
        write_json(self.root / "empty.json", {})

    def tearDown(self):
        self.temp.cleanup()

    def run_replay(self):
        return replay(self.index, self.root, self.root / "result.json")

    def test_valid_and_empty_approval_rejected(self):
        result = self.run_replay()
        self.assertEqual(result["technicalTotal"], 1)
        self.assertEqual(result["emptyApprovalsRejected"], 1)
        self.assertEqual(result["sourceBindingsVerified"], 10)
        self.assertEqual(result["publicationApproved"], 0)

    def test_duplicate_technical_identity(self):
        self.index["entries"].append(copy.deepcopy(self.index["entries"][0]))
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_duplicate_cross_rating_inventory(self):
        row = copy.deepcopy(self.index["decisions"][0]); row["rating"] = 800
        self.index["decisions"].append(row)
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_alias_and_rating(self):
        for key, value in (("id", "999999/A"), ("id", "0999999A"), ("rating", 1000), ("rating", 900)):
            old = self.index["entries"][0][key]; self.index["entries"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.run_replay()
            self.index["entries"][0][key] = old

    def test_provisional_and_rejected_excluded(self):
        for status in ("provisional", "rejected", "held"):
            self.index["entries"][0]["status"] = status
            with self.subTest(status=status), self.assertRaises(ValueError):
                self.run_replay()

    def test_changed_independent_decision(self):
        self.audit["approved"] = False; write_json(self.ap, self.audit)
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_missing_semantic_review_even_with_current_hashes(self):
        self.audit["incorrectAnalysis"].pop("5")
        write_json(self.ap, self.audit)
        ah = digest(self.audit)
        self.index["entries"][0]["auditHash"] = ah
        self.index["entries"][0]["decision"]["recordHash"] = ah
        self.index["decisions"][0]["record"]["recordHash"] = ah
        with self.assertRaisesRegex(ValueError, "algorithmic"):
            self.run_replay()

    def test_missing_decision(self):
        self.index["decisions"] = []
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_omitted_technical_entry(self):
        self.index["entries"] = []
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_stale_evidence_and_changed_package(self):
        self.evidence["validator"] = "other"; write_json(self.ep, self.evidence)
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_changed_source_bytes(self):
        path = self.root / self.index["entries"][0]["sources"][0]["path"]
        data = json.loads(path.read_text()); data["code"] = "changed"; write_json(path, data)
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_missing_or_duplicate_sources(self):
        sources = self.index["entries"][0]["sources"]
        sources.pop()
        with self.assertRaises(ValueError):
            self.run_replay()
        sources.append(sources[0])
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_gate_root_must_match_indexed_evidence(self):
        self.index["entries"][0]["evidenceRoot"] = "elsewhere"
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_nonempty_approval(self):
        write_json(self.root / "empty.json", {"action": "publish"})
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_changed_review_artifact(self):
        self.index["reviewArtifacts"] = [{"path": self.index["entries"][0]["audit"], "sha256": "0" * 64}]
        with self.assertRaises(ValueError):
            self.run_replay()

    def test_symlink_source_path(self):
        record = self.index["entries"][0]["sources"][0]
        (self.root / "link").symlink_to(self.root / record["path"])
        record["path"] = "link"
        with self.assertRaises(ValueError):
            self.run_replay()

    def snapshot(self):
        write_json(self.root / "index.json", self.index)
        return {"bundleIndex": "index.json", "bundleIndexHash": digest(self.index),
                "bundleIndexFileSHA256": sha_file(self.root / "index.json"),
                "technicalCounts": {str(r): int(r == 1200) for r in (800, 1000, 1200, 1400, 1600)},
                "technicalPackages": [{k: self.index["entries"][0][k] for k in
                                       ("id", "rating", "packageHash", "evidenceHash", "auditHash")} ]}

    def test_snapshot_reconstructs_exact_index(self):
        report = replay_snapshot(self.snapshot(), self.root, self.root / "result.json")
        self.assertEqual(report["technicalTotal"], 1)

    def test_snapshot_changed_hash_and_count(self):
        snapshot = self.snapshot()
        snapshot["bundleIndexHash"] = "0" * 64
        with self.assertRaises(ValueError):
            replay_snapshot(snapshot, self.root, self.root / "result.json")
        snapshot = self.snapshot(); snapshot["technicalCounts"]["800"] = 1
        with self.assertRaises(ValueError):
            replay_snapshot(snapshot, self.root, self.root / "result.json")

    def test_snapshot_changed_package_ledger(self):
        snapshot = self.snapshot(); snapshot["technicalPackages"][0]["auditHash"] = "0" * 64
        with self.assertRaises(ValueError):
            replay_snapshot(snapshot, self.root, self.root / "result.json")

    def test_snapshot_unsafe_path(self):
        snapshot = self.snapshot(); snapshot["bundleIndex"] = "../index.json"
        with self.assertRaises(ValueError):
            replay_snapshot(snapshot, self.root, self.root / "result.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
