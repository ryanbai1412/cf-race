"""Fail-closed evidence contract shared by all rating workers and publishers."""
import hashlib
import json
import os
from pathlib import Path
import re

from pool_sources import PINS, sha_file

VERSION = 1
RATINGS = (800, 1000, 1200, 1400, 1600)
ROOT = Path(__file__).resolve().parent.parent
LEGACY = Path(__file__).with_name("legacy_800.json")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.partial")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def manifest(package):
    package = Path(package)
    result = {}
    for path in sorted(package.rglob("*")):
        if path.is_symlink():
            raise ValueError("symlinks are forbidden in packages")
        if path.is_file():
            rel = path.relative_to(package).as_posix()
            if not (rel in ("meta.json", "statement.html", "provenance.json") or
                    re.fullmatch(r"(?:samples|tests)/[0-9]+\.(?:in|out)", rel)):
                raise ValueError(f"unexpected package byte: {rel}")
            result[rel] = {"sha256": sha_file(path), "bytes": path.stat().st_size}
    if not all(k in result for k in ("meta.json", "statement.html", "provenance.json")):
        raise ValueError("incomplete package")
    test_ins = {k[:-3] for k in result if k.startswith("tests/") and k.endswith(".in")}
    test_outs = {k[:-4] for k in result if k.startswith("tests/") and k.endswith(".out")}
    if not test_ins or test_ins != test_outs:
        raise ValueError("missing or unpaired tests")
    if any(result[p]["bytes"] == 0 for p in result if p.startswith(("tests/", "samples/"))):
        raise ValueError("empty test file")
    sample_ins = {k[:-3] for k in result if k.startswith("samples/") and k.endswith(".in")}
    sample_outs = {k[:-4] for k in result if k.startswith("samples/") and k.endswith(".out")}
    if not sample_ins or sample_ins != sample_outs:
        raise ValueError("missing or unpaired samples")
    for name in sorted(test_ins | sample_ins):
        pairs([{"input": (package / f"{name}.in").read_text(encoding="utf-8"),
                "output": (package / f"{name}.out").read_text(encoding="utf-8")}])
    sample_hashes = {(result[f"{name}.in"]["sha256"], result[f"{name}.out"]["sha256"]) for name in sample_ins}
    if all((result[f"{name}.in"]["sha256"], result[f"{name}.out"]["sha256"]) in sample_hashes for name in test_ins):
        raise ValueError("samples-only package suite")
    return result


def pairs(tests):
    if not isinstance(tests, list) or not tests:
        raise ValueError("empty/missing tests")
    for pair in tests:
        for side in ("input", "output"):
            value = pair.get(side)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"missing/empty {side}")
            if re.search(r"(?im)(?:^\s*\.\.\.\s*$|\[truncated\]|output truncated|input truncated)", value):
                raise ValueError("truncated test pair")
    return tests


def row_gate(row):
    for field in ("description", "input_format", "output_format", "title", "id"):
        if not row.get(field):
            raise ValueError(f"missing source {field}")
    if row.get("generated_checker"):
        raise ValueError("unaudited special checker; token judge cannot support it")
    if row.get("interaction_format") or row.get("input_mode") != "stdio":
        raise ValueError("unsupported interactive/file IO")
    if row.get("time_limit", 0) <= 0 or row.get("memory_limit", 0) <= 0:
        raise ValueError("invalid resource limits")
    pairs(row.get("official_tests"))
    pairs(row.get("examples"))
    if row.get("official_tests_complete") is True:
        if len(row["official_tests"]) != row.get("testset_size"):
            raise ValueError("official completeness/count mismatch")
    elif not row.get("generated_tests"):
        raise ValueError("incomplete official tests and no full generated suite")
    if set((p["input"], p["output"]) for p in row["official_tests"]).issubset(
            {(p["input"], p["output"]) for p in row["examples"]}):
        raise ValueError("samples-only suite")


def verify_evidence(package, evidence, audit):
    meta = read_json(Path(package) / "meta.json")
    files = manifest(package)
    if evidence.get("schemaVersion") != VERSION or evidence.get("id") != meta["id"]:
        raise ValueError("evidence identity/version mismatch")
    if meta.get("rating") not in RATINGS or evidence.get("rating") != meta["rating"]:
        raise ValueError("rating mismatch")
    if evidence.get("files") != files or evidence.get("packageHash") != digest(files):
        raise ValueError("changed package bytes")
    if evidence.get("status") != "execution-passed" or evidence.get("stages") != ["prepare", "generate", "validate"]:
        raise ValueError("interrupted/incomplete stages")
    if evidence.get("acceptedContradiction") is not False:
        raise ValueError("accepted-source contradiction remains unresolved")
    if meta.get("specialJudge") or meta.get("floatEps") is not None:
        raise ValueError("unsupported checker")
    provenance = read_json(Path(package) / "provenance.json")
    if provenance.get("pins") != PINS or provenance.get("apiRating") != meta["rating"]:
        raise ValueError("missing pinned provenance/API rating")
    suite = provenance.get("tests", {})
    records = suite.get("pairs", [])
    if len({r["name"] for r in records}) != len(records):
        raise ValueError("duplicate test identities")
    if evidence.get("testCount") != len(records) or len(records) != len([p for p in files if p.startswith("tests/") and p.endswith(".in")]):
        raise ValueError("test count mismatch")
    for record in records:
        for ext, key in (("in", "inputHash"), ("out", "outputHash")):
            if files.get(f"tests/{record['name']}.{ext}", {}).get("sha256") != record[key]:
                raise ValueError("test pair/provenance mismatch")
    if not suite.get("officialIncluded") or suite.get("generatedIncluded") != suite.get("generatedAdvertised"):
        raise ValueError("incomplete source test suite")
    origins = {key: sum(r.get("origin") == key for r in records) for key in ("official", "open-r1-generated", "worker-generated")}
    if (origins["official"] != suite["officialIncluded"] or
            origins["open-r1-generated"] != suite["generatedIncluded"] or sum(origins.values()) != len(records)):
        raise ValueError("test origin/count mismatch")
    if suite.get("officialComplete") is not True:
        raise ValueError("incomplete official tests; generated coverage cannot replace missing official pairs")
    if suite["officialIncluded"] != suite.get("officialAdvertised"):
        raise ValueError("official test count mismatch")
    coverage = evidence.get("coverage", {})
    for key in ("boundary", "adversarial", "maxSize", "inputConstraints", "checkerSemantics", "statementComplete"):
        if not coverage.get(key):
            raise ValueError(f"missing independently reviewed coverage: {key}")
    if coverage.get("packageHash") != evidence["packageHash"]:
        raise ValueError("coverage belongs to different package")
    for key in ("boundary", "adversarial", "maxSize"):
        entries = coverage[key]
        if not isinstance(entries, list) or any(not e.get("reason") or f"tests/{e.get('test')}.in" not in files for e in entries):
            raise ValueError("coverage names unavailable tests")
    runs = evidence.get("submissions", [])
    hashes, identities = set(), set()
    for run in runs:
        if run.get("sourceHash") in hashes or run.get("submissionId") in identities:
            raise ValueError("duplicate submission evidence")
        hashes.add(run.get("sourceHash"))
        identities.add(run.get("submissionId"))
        if not re.fullmatch(r"[a-f0-9]{64}", run.get("sourceHash", "")) or not run.get("source"):
            raise ValueError("missing source provenance")
        if run["source"].get("revision") != PINS["open-r1/codeforces-submissions"] or run["source"].get("dataset") != "open-r1/codeforces-submissions":
            raise ValueError("unpinned submission evidence")
        if run.get("compiled") is not True or run.get("infrastructureError"):
            raise ValueError("compile/infrastructure failure is not validation")
        results = run.get("runs", [])
        if len(results) != evidence["testCount"] or [r.get("test") for r in results] != [r["name"] for r in records]:
            raise ValueError("incomplete per-test run evidence")
        if any(not re.fullmatch(r"[a-f0-9]{64}", r.get("outputHash", "")) for r in results):
            raise ValueError("missing output checksums")
        if run.get("expected") == "OK":
            if run.get("verdict") != "AC" or run.get("testsRun") != evidence["testCount"]:
                raise ValueError("accepted submission did not pass entire suite")
            if any(r.get("verdict") != "AC" or r.get("exitCode") != 0 or r.get("timeout") for r in results):
                raise ValueError("accepted per-test evidence contradicts verdict")
        elif run.get("expected") in ("WRONG_ANSWER", "TIME_LIMIT_EXCEEDED"):
            if run.get("verdict") not in ("WA", "TLE") or not run.get("failedTest"):
                raise ValueError("incorrect solution was not killed by valid test")
            if not any(r.get("test") == run["failedTest"] and r.get("verdict") in ("WA", "TLE") for r in results):
                raise ValueError("missing counterexample evidence")
        else:
            raise ValueError("unsupported external verdict")
    if sum(r["expected"] == "OK" for r in runs) < 5 or sum(r["expected"] != "OK" for r in runs) < 5:
        raise ValueError("fewer than 5 accepted/5 incorrect independent sources")
    sandbox = evidence.get("sandbox", {})
    from pool_sandbox import IMAGE
    if sandbox.get("image") != IMAGE or sandbox.get("network") != "none" or sandbox.get("bounded") is not True:
        raise ValueError("missing isolated bounded sandbox evidence")
    for key in ("harnessHash", "runnerHash", "checkerHash"):
        if not re.fullmatch(r"[a-f0-9]{64}", sandbox.get(key, "")):
            raise ValueError(f"missing validation implementation checksum: {key}")
    if audit.get("evidenceHash") != digest(evidence) or audit.get("packageHash") != evidence["packageHash"]:
        raise ValueError("audit is stale")
    if (audit.get("approved") is not True or not audit.get("reviewer") or
            audit["reviewer"] == evidence.get("validator") or not audit.get("reviewUrl")):
        raise ValueError("missing independent audit signoff")
    for key in ("sourceAttribution", "fullTests", "coverage", "fiveAcceptedFiveIncorrect", "noSpecialChecker", "hashes"):
        if audit.get("checks", {}).get(key) is not True:
            raise ValueError(f"audit did not sign off {key}")
    return files


def publication_gate(package, evidence_root=None, approval_path=None, require_approval=True):
    package = Path(package)
    meta = read_json(package / "meta.json")
    if meta.get("rating") is None and package.resolve().is_relative_to(ROOT / "problems" / "dev"):
        return {"legacy": True}
    if meta.get("rating") == 800 and meta["id"] in read_json(LEGACY) and not meta.get("poolPipeline"):
        return {"legacy": True}
    root = Path(evidence_root or os.environ.get("RATED_POOL_EVIDENCE_ROOT", ROOT / "pipeline" / "ratings"))
    base = root / str(meta["rating"])
    evidence = read_json(base / "evidence" / f"{meta['id']}.json")
    audit = read_json(base / "audits" / f"{meta['id']}.json")
    files = verify_evidence(package, evidence, audit)
    if require_approval:
        approval = read_json(approval_path or os.environ.get("RATED_POOL_APPROVAL", ""))
        if (approval.get("action") != "publish" or not approval.get("approvedBy") or not approval.get("approvalUrl") or
                approval.get("packages", {}).get(meta["id"]) != {"packageHash": digest(files), "evidenceHash": digest(evidence), "auditHash": digest(audit)}):
            raise ValueError("explicit content-bound publication approval required")
    return {"legacy": False, "files": files, "packageHash": digest(files),
            "evidenceHash": digest(evidence), "auditHash": digest(audit)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(publication_gate(Path(args.package).resolve(), require_approval=not args.dry_run)))
