"""Repair only 404A/465B/29A, separately from the immutable recovery35."""
import argparse
import base64
import hashlib
from pathlib import Path
import shutil

import worker
from archive import files, write_archive, verify_archive
from checker import check
from correction_cases_batch04 import IDS, answer, cases, generator_source
from correction_replay import BASE as PRIOR, HERE
from correction_triage import indexed_sources, read
from correction_witnesses import inspect
from pool_contract import digest, manifest, verify_evidence, write_json
from pool_generation import sandbox, verify_generated
from pool_sandbox import COMPILER_FLAGS, EXECUTION_VERSION, IMAGE, kind, run
from pool_sources import PINS, sha_file

BASE = HERE / "repair-batch04" / "1000"
EXCLUDED = "7730183"
REPLACEMENT = "7736795"
ORACLE = "6068285"


def frozen_locks():
    roots = (HERE / "packages", HERE / "evidence", HERE / "audits", PRIOR)
    return {str(root.relative_to(HERE)): {
        path.relative_to(root).as_posix(): {"sha256": sha_file(path), "bytes": path.stat().st_size}
        for path in files(root)} for root in roots if root.exists()}


def lock_history():
    path = BASE / "frozen-locks.json"
    locked = frozen_locks()
    if path.exists() and read(path) != locked:
        raise ValueError("original package/evidence/cache/audit bytes changed")
    if not path.exists():
        write_json(path, locked)
    return digest(locked)


def source_row(pid, sid, verdict):
    matches = [row for row in indexed_sources(pid) if str(row["submission_id"]) == sid]
    if len(matches) != 1:
        raise ValueError(f"source absent/ambiguous: {pid}/{sid}")
    row = matches[0]
    if (row["testset"] != "TESTS" or row["verdict"] != verdict or kind(row["programmingLanguage"]) is None
            or row["provenance"]["revision"] != PINS["open-r1/codeforces-submissions"]):
        raise ValueError("unsupported or unpinned source")
    return row


def source_record(row):
    sid = str(row["submission_id"])
    return {"submissionId": sid, "sourceHash": hashlib.sha256(row["source"].encode()).hexdigest(),
            "language": row["programmingLanguage"], "expected": row["verdict"], "source": row["provenance"],
            "url": f"https://codeforces.com/contest/{row['contestId']}/submission/{sid}", "code": row["source"]}


def selected_sources(pid):
    prior = read(PRIOR / "evidence" / f"{pid}.json")
    result = []
    for ref in prior["submissions"]:
        if pid == "465B" and str(ref["submissionId"]) == EXCLUDED:
            continue
        source = read(PRIOR / "state" / pid / "sources" / f"{ref['submissionId']}.json")
        pinned = source_record(source_row(pid, str(ref["submissionId"]), ref["expected"]))
        if ({k: v for k, v in source.items() if k != "source"} !=
                {k: v for k, v in pinned.items() if k != "source"} or pinned["sourceHash"] != ref["sourceHash"]):
            raise ValueError("retained public bytes/provenance changed")
        attributed = []
        for marker in (HERE / "submissions").glob("*/complete.json"):
            metadata = read(marker)
            if metadata["source"] == source["source"] and f"{pid}.json" in metadata["files"]:
                attributed.extend(read(marker.parent / f"{pid}.json"))
        if not any(str(row["submission_id"]) == source["submissionId"] and row["source"] == source["code"]
                   and row["provenance"] == source["source"] for row in attributed):
            raise ValueError("retained source attribution absent from pinned index")
        result.append(source)
    if pid == "465B":
        result.append(source_record(source_row(pid, REPLACEMENT, "WRONG_ANSWER")))
    if (len(result) != 10 or sum(r["expected"] == "OK" for r in result) != 5
            or len({r["sourceHash"] for r in result}) != 10 or len({r["submissionId"] for r in result}) != 10):
        raise ValueError("need five distinct accepted and five wrong sources")
    return result


def oracle_record(pid, selected):
    if pid == "404A":
        record = source_record(source_row(pid, ORACLE, "OK"))
    else:
        prior = read(HERE / "qualification-sources" / pid / "source.json")
        record = source_record(source_row(pid, str(prior["submissionId"]), "OK"))
        if record["sourceHash"] != prior["sourceHash"]:
            raise ValueError("prior oracle source changed")
    if record["sourceHash"] in {r["sourceHash"] for r in selected}:
        raise ValueError("sixth public oracle overlaps validation sources")
    return record


def build(pid, cache):
    lock_history()
    package = BASE / "packages" / pid
    prior = read(PRIOR / "evidence" / f"{pid}.json")
    if manifest(PRIOR / "packages" / pid) != prior["files"]:
        raise ValueError("prior recovery evidence mismatch")
    if package.exists() and manifest(package) != prior["files"]:
        raise ValueError("do not overwrite generated correction bytes; resume execute/archive instead")
    history = BASE / "history" / pid
    shutil.copytree(PRIOR / "packages" / pid, history / "package", dirs_exist_ok=True)
    for category in ("evidence", "review"):
        for path in (PRIOR / category).glob(f"{pid}*.json"):
            shutil.copy2(path, history / path.name)
    shutil.copytree(PRIOR / "state" / pid / "sources", history / "sources", dirs_exist_ok=True)
    shutil.copytree(HERE / "qualification-sources" / pid, history / "qualification-sources", dirs_exist_ok=True)
    package.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PRIOR / "packages" / pid, package, dirs_exist_ok=True)
    for name in ("prepare.json", "source-row.json"):
        destination = BASE / "state" / pid / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HERE / "state" / pid / name, destination)
    inventory = BASE / "inventory.json"
    if not inventory.exists():
        shutil.copy2(HERE / "inventory.json", inventory)
        shutil.copy2(HERE / "api-problems.json", BASE / "api-problems.json")
    selected = selected_sources(pid)
    oracle = oracle_record(pid, selected)
    proofs = BASE / "qualification-sources" / pid
    proofs.mkdir(parents=True)
    generator = generator_source(pid, (package / "qualification" / "generator.py").read_text())
    (proofs / "generator.py").write_text(generator)
    oracle_path = proofs / ("oracle.cpp" if kind(oracle["language"]) == "cpp" else "oracle.py")
    oracle_path.write_text(oracle["code"])
    write_json(proofs / "source.json", {**oracle, "attribution": "Sixth pinned public accepted source; NOT an agent audit"})
    write_json(BASE / "selection" / f"{pid}.json", selected)
    args = worker.arguments(pid, BASE, cache)
    args.generator_source, args.generator_language, args.generator_author = str(proofs / "generator.py"), "Python 3", args.validator
    args.oracle_source, args.oracle_language = str(oracle_path), oracle["language"]
    args.oracle_author, args.oracle_review_url = f"codeforces-submission:{oracle['submissionId']}", oracle["url"]
    args.seed, args.exhaustive_domain_size, args.exhaustive_domain = 0, None, None
    generated = worker.rated_pool.generate(args)
    write_json(proofs / "generate-result.json", generated)
    for name, record in prior["files"].items():
        if name.startswith(("tests/", "samples/")) and sha_file(package / name) != record["sha256"]:
            raise ValueError("old test/sample bytes not retained unchanged")
    coverage = {**prior["coverage"], "packageHash": generated["packageHash"]}
    for key in ("boundary", "adversarial", "maxSize"):
        coverage[key] = list(coverage[key])
    inputs = {}
    for path in sorted((package / "tests").glob("*.in")):
        inputs.setdefault(path.read_text(), path.stem)
    for case in cases(pid):
        name = inputs[case["input"]]
        for category in case["categories"]:
            coverage[category].append({"test": name, "reason": case["reason"]})
    coverage["correctionScope"] = {
        "404A": "Positional sixth oracle; row-count-preserving counterexamples; exhaustive binary minimum grid",
        "465B": "Replace debug-input-overwrite source7730183 with algorithmic wrong source7736795",
        "29A": "Both coordinate endpoints, both maximum signed distances, actual separation20000 atn2/n100"
    }[pid]
    write_json(BASE / "coverage" / f"{pid}.json", coverage)
    checks = []
    for category in ("samples", "tests"):
        for path in sorted((package / category).glob("*.in")):
            actual = answer(pid, path.read_text())
            if not check(path.with_suffix(".out").read_text(), actual):
                raise ValueError(f"constraint/mathematical mismatch {pid}/{category}/{path.stem}")
            checks.append({"pair": f"{category}/{path.stem}", "inputHash": sha_file(path),
                           "outputHash": sha_file(path.with_suffix(".out")), "constraints": "passed", "output": "passed"})
    write_json(BASE / "semantics" / f"{pid}.json", {"passed": True, "packageHash": generated["packageHash"],
               "recipeHash": sha_file(HERE / "correction_cases_batch04.py"), "checks": checks,
               "independentAudit": False, "validated": False})
    if pid == "404A":
        old_oracle = read(history / "qualification-sources" / "source.json")
        bad = (history / "package" / "qualification" / "oracle.py").read_text()
        witness = next(c for c in cases(pid) if "Row-count-preserving" in c["reason"])
        result = run(bad, old_oracle["language"], [{"name": "row-count-position-counterexample",
                     "input": witness["input"].encode(), "output": witness["output"].encode()}], 1, 256, capture=True)
        if result["verdict"] != "WA" or result["runs"][0]["exitCode"] != 0 or result["runs"][0]["timeout"]:
            raise ValueError("old oracle defect not reproduced")
        write_json(BASE / "diagnostics" / "404A-rejected-oracle.json", {
            "source": old_oracle, "sourceHash": hashlib.sha256(bad.encode()).hexdigest(), "witness": witness,
            "actual": base64.b64decode(result["runs"][0]["output"]).decode(), "result": result, "counted": False})
    if pid == "465B":
        write_json(BASE / "diagnostics" / "465B-excluded-debug.json", {
            "source": read(history / "sources" / f"{EXCLUDED}.json"), "reason": "Overwrites read input with literal debug fixture",
            "replacement": REPLACEMENT, "replacementDefect": "mailList is never reset after the first zero, so every subsequent unread item costs2 even within a contiguous unread block", "counted": False})
    lock_history()
    print(pid, "qualified", generated["testCount"], flush=True)


def execute(pid):
    lock_history()
    package = BASE / "packages" / pid
    semantic = read(BASE / "semantics" / f"{pid}.json")
    current = manifest(package)
    if (not semantic["passed"] or semantic["packageHash"] != digest(current)
            or semantic["recipeHash"] != sha_file(HERE / "correction_cases_batch04.py")):
        raise ValueError("stale semantic proof")
    prior = read(PRIOR / "evidence" / f"{pid}.json")
    selected = read(BASE / "selection" / f"{pid}.json")
    meta = read(package / "meta.json")
    tests = [{"name": p.stem, "input": p.read_bytes(), "output": p.with_suffix(".out").read_bytes()}
             for p in sorted((package / "tests").glob("*.in"))]
    results = []
    for source in selected:
        sid = source["submissionId"]
        write_json(BASE / "state" / pid / "sources" / f"{sid}.json", source)
        run_key = digest({"packageHash": digest(current), "sourceHash": source["sourceHash"], "sandbox": sandbox()})
        path = BASE / "state" / pid / "runs" / f"{sid}-{run_key}.json"
        if path.exists():
            cached = read(path)
            if cached["runKey"] != run_key:
                raise ValueError("stale bounded replay")
            result = cached["result"]
        else:
            result = run(source["code"], source["language"], tests, meta["timeLimitMs"] / 1000, int(meta["memoryLimitMb"]))
            write_json(path, {"runKey": run_key, "sandbox": sandbox(), "result": result})
        results.append({k: v for k, v in source.items() if k != "code"} | result)
        if not result["compiled"] or result["verdict"] != ("AC" if source["expected"] == "OK" else "WA"):
            write_json(BASE / "diagnostics" / f"{pid}-failed-replay-{sid}.json", results[-1])
            raise ValueError(f"unqualified {pid}/{sid}: {result['verdict']}")
        print(pid, sid, result["verdict"], result.get("failedTest"), flush=True)
    excluded = list(prior["excludedSubmissions"])
    if pid == "465B":
        excluded.append({"id": EXCLUDED, "reason": "Input overwritten with debug fixture, not an algorithmic witness"})
    evidence = {**prior, "files": current, "packageHash": digest(current), "testCount": len(tests),
                "coverage": read(BASE / "coverage" / f"{pid}.json"), "submissions": results,
                "excludedSubmissions": excluded, "sandbox": sandbox(), "status": "execution-passed",
                "acceptedContradiction": False, "auditStatus": "fresh DIFFERENT-agent audit required"}
    write_json(BASE / "evidence" / f"{pid}.json", evidence)
    witnesses = inspect(pid, BASE)
    if len(witnesses) != 5 or any(not w["potentialSemanticMismatch"] for w in witnesses):
        raise ValueError("fewer than five normal original/LF semantic wrong witnesses")
    write_json(BASE / "review" / f"{pid}.json", {
        "id": pid, "previousPackageHash": prior["packageHash"], "previousEvidenceHash": digest(prior),
        "packageHash": digest(current), "evidenceHash": digest(evidence), "coverageHash": digest(evidence["coverage"]),
        "auditStatus": "fresh DIFFERENT-agent source/constraint/oracle/coverage audit required", "approved": False,
        "independentlyValidated": False, "witnessesHash": sha_file(BASE / "review" / f"{pid}-witnesses.json"),
        "sourceHashes": {r["submissionId"]: r["sourceHash"] for r in results}})
    if manifest(package) != current:
        raise ValueError("package changed during replay")
    lock_history()


def archive(output):
    if output is None or not output.is_dir():
        raise ValueError("output directory must already exist")
    lock_history()
    bindings = {}
    for pid in IDS:
        evidence = read(BASE / "evidence" / f"{pid}.json")
        review = read(BASE / "review" / f"{pid}.json")
        if (review["approved"] or review["independentlyValidated"] or manifest(BASE / "packages" / pid) != evidence["files"]
                or digest(evidence) != review["evidenceHash"] or digest(evidence["coverage"]) != review["coverageHash"]
                or sha_file(BASE / "review" / f"{pid}-witnesses.json") != review["witnessesHash"]):
            raise ValueError("stale correction bindings")
        if sha_file(BASE / "review" / f"{pid}-consistency.json") != review["consistencyHash"]:
            raise ValueError("stale consistency/sample proof")
        bindings[pid] = {**review, "testCount": evidence["testCount"], "sandbox": evidence["sandbox"],
                         "sixthOracle": read(BASE / "qualification-sources" / pid / "source.json"),
                         "testHashes": read(BASE / "packages" / pid / "provenance.json")["tests"]["pairs"]}
    write_json(BASE / "delivery.json", {"ids": list(IDS), "rating": 1000, "pins": PINS, "bindings": bindings,
               "validatedCount": 0, "publicationApproved": 0, "frozenHistoryHash": lock_history()})
    tooling = BASE / "tooling" / "pipeline"
    tooling.mkdir(parents=True, exist_ok=True)
    core = list((REPO / "pipeline").glob("pool_*.py")) + [REPO / "pipeline" / name for name in
                                                        ("checker.py", "rated_pool.py", "legacy_800.json")]
    for source in core:
        target_source = tooling / source.name
        if target_source.exists() and sha_file(target_source) != sha_file(source):
            raise ValueError("tooling snapshot changed")
        shutil.copyfile(source, target_source)
    shutil.copyfile(HERE / "correction_cases_batch04.py", tooling / "correction_cases_batch04.py")
    shutil.copyfile(HERE / "verify_batch04.py", BASE / "tooling" / "verify_batch04.py")
    paths = list(files(BASE)) + [p for p in HERE.glob("*.py")] + list(files(HERE / "tests"))
    target = output / "rating-1000-repair-batch04-tooling-v2.tar.gz"
    if target.exists():
        raise ValueError("immutable archive exists; never overwrite")
    record = write_archive(target, paths)
    record["verification"] = verify_archive(target, record)
    replay = output / "rating-1000-repair-batch04-tooling-v2.reproduced.tar.gz"
    second = write_archive(replay, paths)
    if record["sha256"] != second["sha256"] or record["bytes"] != second["bytes"]:
        raise ValueError("archive not reproducible")
    verify_archive(replay, second)
    replay.unlink()
    write_json(output / "rating-1000-repair-batch04-tooling-v2.provenance.json", {
        "archive": record, "reproducedIdentically": True, "ids": list(IDS), "bindings": bindings,
        "validatedCount": 0, "publicationApproved": 0, "pins": PINS,
        "frozenHistoryHash": lock_history(), "auditStatus": "Existing primary68758b must freshly audit; builder never signs"})
    print({"archive": str(target), "sha256": record["sha256"], "bytes": record["bytes"], "members": len(record["files"])}, flush=True)


def verify(pid):
    lock_history()
    package = BASE / "packages" / pid
    evidence = read(BASE / "evidence" / f"{pid}.json")
    provenance = read(package / "provenance.json")
    barriers = ((verify_evidence, (package, evidence, {}), "audit is stale"),
                (verify_generated, (package, evidence["files"], provenance["tests"]["pairs"], evidence, {}),
                 "generated basis not explicitly declared in evidence/audit"))
    for function, arguments, barrier in barriers:
        try:
            function(*arguments)
        except ValueError as exc:
            if str(exc) != barrier:
                raise
        else:
            raise ValueError("missing independent audit did not fail closed")
    selected = read(BASE / "selection" / f"{pid}.json")
    refs = {r["submissionId"]: r for r in evidence["submissions"]}
    meta = read(package / "meta.json")
    tests = [{"name": p.stem, "input": p.read_bytes(), "output": p.with_suffix(".out").read_bytes()}
             for p in sorted((package / "samples").glob("*.in"))]
    sample_records = []
    for source in selected:
        if hashlib.sha256(source["code"].encode()).hexdigest() != refs[source["submissionId"]]["sourceHash"]:
            raise ValueError("changed public source")
        key = digest({"packageHash": evidence["packageHash"], "sourceHash": source["sourceHash"], "sandbox": sandbox()})
        path = BASE / "state" / pid / "sample-runs" / f"{source['submissionId']}-{key}.json"
        if not path.exists():
            result = run(source["code"], source["language"], tests, meta["timeLimitMs"] / 1000, int(meta["memoryLimitMb"]))
            write_json(path, {"runKey": key, "sourceHash": source["sourceHash"], "packageHash": evidence["packageHash"],
                             "sandbox": sandbox(), "result": result})
        record = read(path)
        if record["runKey"] != key or (source["expected"] == "OK" and record["result"]["verdict"] != "AC"):
            raise ValueError("stale sample cache or accepted sample contradiction")
        sample_records.append({"submissionId": source["submissionId"], "sourceHash": source["sourceHash"],
                               "file": path.relative_to(BASE).as_posix(), "fileHash": sha_file(path),
                               "verdict": record["result"]["verdict"], "testsRun": record["result"]["testsRun"]})
    proof = BASE / "review" / f"{pid}-consistency.json"
    write_json(proof, {"packageHash": evidence["packageHash"], "evidenceHash": digest(evidence),
                      "unsignedStructuralProofsPassed": True, "missingAuditFailsClosed": True,
                      "samples": sample_records, "sampleHashes": manifest(package), "independentlyValidated": False})
    review_path = BASE / "review" / f"{pid}.json"
    write_json(review_path, {**read(review_path), "consistencyHash": sha_file(proof)})
    lock_history()
    print(pid, "unsigned proofs consistent, accepted samples pass, no audit signoff", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("build", "execute", "verify", "archive"))
    parser.add_argument("--ids", nargs="+", choices=IDS, default=list(IDS))
    parser.add_argument("--cache", type=Path, default=Path.home() / ".cache/cf-race-pool")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.stage == "archive":
        archive(args.output_dir)
    else:
        for pid in args.ids:
            if args.stage == "build":
                build(pid, args.cache)
            elif args.stage == "verify":
                verify(pid)
            else:
                execute(pid)


if __name__ == "__main__":
    main()
