"""Portable data-only correction checks; --replay executes public sources only in Docker."""
import argparse
import hashlib
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pipeline"))
from correction_cases_batch04 import answer
from pool_contract import digest, manifest, read_json, verify_evidence
from pool_generation import sandbox, verify_generated
from pool_sandbox import run


def verify(base, replay=False):
    delivery = read_json(base / "delivery.json")
    assert delivery["validatedCount"] == delivery["publicationApproved"] == 0
    for pid in delivery["ids"]:
        package = base / "packages" / pid
        evidence = read_json(base / "evidence" / f"{pid}.json")
        binding = delivery["bindings"][pid]
        assert binding["packageHash"] == digest(manifest(package)) == evidence["packageHash"]
        assert binding["evidenceHash"] == digest(evidence)
        assert binding["coverageHash"] == digest(evidence["coverage"])
        assert binding["approved"] is binding["independentlyValidated"] is False
        assert sandbox() == evidence["sandbox"]
        provenance = read_json(package / "provenance.json")
        for function, args, barrier in ((verify_evidence, (package, evidence, {}), "audit is stale"),
                (verify_generated, (package, evidence["files"], provenance["tests"]["pairs"], evidence, {}),
                 "generated basis not explicitly declared in evidence/audit")):
            try:
                function(*args)
            except ValueError as exc:
                assert str(exc) == barrier, str(exc)
            else:
                raise AssertionError("independent audit barrier failed open")
        tests = []
        for p in sorted((package / "tests").glob("*.in")):
            assert answer(pid, p.read_text()).split() == p.with_suffix(".out").read_text().split(), p
            tests.append({"name": p.stem, "input": p.read_bytes(), "output": p.with_suffix(".out").read_bytes()})
        selected = read_json(base / "selection" / f"{pid}.json")
        refs = {ref["submissionId"]: ref for ref in evidence["submissions"]}
        assert len(selected) == len(refs) == 10
        for source in selected:
            ref = refs[source["submissionId"]]
            assert source["sourceHash"] == ref["sourceHash"] == hashlib.sha256(source["code"].encode()).hexdigest()
            assert source["source"] == ref["source"] and source["expected"] == ref["expected"]
            if replay:
                meta = read_json(package / "meta.json")
                result = run(source["code"], source["language"], tests, meta["timeLimitMs"] / 1000, int(meta["memoryLimitMb"]))
                assert result["verdict"] == ("AC" if source["expected"] == "OK" else "WA")
                assert result["testsRun"] == len(tests)
        print(pid, len(tests), "tests: unsigned data bindings pass; no independent approval")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=HERE.parent)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    verify(args.base, args.replay)
