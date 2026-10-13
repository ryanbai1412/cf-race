"""Rebuild excluded packages additively with independently reviewable public references."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

from correction_triage import HERE, indexed_sources, read

sys.path.insert(0, str(HERE.parents[1]))
from pool_contract import digest, manifest, write_json
from pool_sandbox import COMPILER_FLAGS, EXECUTION_VERSION, IMAGE, run
from pool_sources import sha_file


BASE = HERE / "recovery-v2" / "1000"


def original_bytes(pid):
    package = HERE / "packages" / pid
    evidence = read(HERE / "evidence" / (pid + ".json"))
    if manifest(package) != evidence["files"] or digest(evidence["files"]) != evidence["packageHash"]:
        raise ValueError(f"original evidence invalid for {pid}")
    return package, evidence


def get_code(pid, old, replacement):
    sid = str(old["submissionId"])
    if replacement and sid in replacement:
        row = next((r for r in indexed_sources(pid) if str(r["submission_id"]) == sid), None)
        if row is None or row["verdict"] != "WRONG_ANSWER" or row["testset"] != "TESTS":
            raise ValueError(f"missing public incorrect submission {pid}/{sid}")
        record = {"submissionId": sid, "sourceHash": hashlib.sha256(row["source"].encode()).hexdigest(),
                  "expected": row["verdict"], "language": row["programmingLanguage"],
                  "source": row["provenance"],
                  "url": f"https://codeforces.com/contest/{row['contestId']}/submission/{sid}",
                  "code": row["source"]}
    else:
        record = read(HERE / "state" / pid / "sources" / f"{sid}.json")
    if record["sourceHash"] != hashlib.sha256(record["code"].encode()).hexdigest():
        raise ValueError(f"source hash mismatch {pid}/{sid}")
    if old["sourceHash"] != record["sourceHash"]:
        raise ValueError(f"unreviewed source code {pid}/{sid}")
    return record


def apply(pid, audit, replacement):
    finding = audit["problems"][pid]
    if finding["approved"] or finding["algorithmicIncorrectKilled"] != 4:
        raise ValueError(f"expected an audit-held, four-genuine-reference package: {pid}")
    package, original = original_bytes(pid)
    for key, name in (("harnessHash", "pool_harness.py"), ("checkerHash", "checker.py"),
                      ("runnerHash", "pool_sandbox.py")):
        if original["sandbox"][key] != sha_file(HERE.parents[1] / name):
            raise ValueError(f"execution implementation changed: {key}; do not reuse historical bindings")
    if (finding["packageHash"] != original["packageHash"]
            or finding["evidenceHash"] != digest(original)):
        raise ValueError(f"stale original audit: {pid}")
    excluded = set(replacement.get("excludePreviouslyClaimed", []))
    selected = [r for r in finding["references"] if str(r["submissionId"]) not in excluded
                and (r["expected"] == "OK" or r.get("algorithmicWrongAnswer") is True)]
    replacements = {str(r["submissionId"]): r for r in
                    [replacement] + replacement.get("additionalReplacements", [])}
    available = indexed_sources(pid)
    known_ids = {str(r["submissionId"]) for r in finding["references"]}
    known_hashes = {r["sourceHash"] for r in finding["references"]}
    for new_sid, renewed in replacements.items():
        row = next((r for r in available if str(r["submission_id"]) == new_sid), None)
        if row is None:
            raise ValueError(f"replacement not in pinned source index: {pid}/{new_sid}")
        new_hash = hashlib.sha256(row["source"].encode()).hexdigest()
        if new_hash != renewed["sourceHash"] or new_sid in known_ids or new_hash in known_hashes:
            raise ValueError(f"duplicate or changed replacement {pid}/{new_sid}")
        selected.append({"submissionId": new_sid, "sourceHash": new_hash, "expected": row["verdict"]})
        known_ids.add(new_sid)
        known_hashes.add(new_hash)
    if len(selected) != 10 or sum(s["expected"] == "OK" for s in selected) != 5:
        raise ValueError(f"expected 5 accepted/5 proposed wrong: {pid}")
    target = BASE / "packages" / pid
    if target.exists():
        if manifest(target) != original["files"]:
            raise ValueError(f"recovery package bytes changed: {pid}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package, target)
        if manifest(target) != original["files"]:
            raise ValueError(f"copy mismatch: {pid}")
    tests = [{"name": p.stem, "input": p.read_bytes(), "output": p.with_suffix(".out").read_bytes()}
             for p in sorted((target / "tests").glob("*.in"))]
    meta = read(target / "meta.json")
    reruns = []
    for original_ref in selected:
        source = get_code(pid, original_ref, replacements)
        source_path = BASE / "state" / pid / "sources" / (source["submissionId"] + ".json")
        source_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(source_path, source)
        run_path = BASE / "state" / pid / "runs" / (source["submissionId"] + ".json")
        if run_path.exists():
            cached = read(run_path)
            if (cached["packageHash"] != original["packageHash"]
                    or cached["sourceHash"] != source["sourceHash"]
                    or cached["image"] != IMAGE
                    or cached["executionVersion"] != EXECUTION_VERSION
                    or cached["compilerFlags"] != COMPILER_FLAGS):
                raise ValueError(f"stale replay cache: {pid}/{source['submissionId']}")
            result = cached["result"]
        else:
            result = run(source["code"], source["language"], tests,
                         meta["timeLimitMs"] / 1000, int(meta["memoryLimitMb"]))
            write_json(run_path, {"sourceHash": source["sourceHash"],
                                  "packageHash": original["packageHash"], "image": IMAGE,
                                  "executionVersion": EXECUTION_VERSION,
                                  "compilerFlags": COMPILER_FLAGS, "result": result})
        expected = "AC" if source["expected"] == "OK" else "WA"
        if result["verdict"] != expected or not result["compiled"]:
            raise ValueError(f"unqualified replay {pid}/{source['submissionId']}: {result['verdict']}")
        witness = (replacements[source["submissionId"]]["test"] if source["submissionId"] in replacements
                   else replacement.get("retainedWitnessOverrides", {}).get(source["submissionId"]))
        if witness:
            case = next((r for r in result["runs"] if r["test"] == witness), None)
            if not case or case["verdict"] != "WA" or case["exitCode"] != 0 or case["timeout"]:
                raise ValueError(f"replacement witness not reproduced on original test bytes: {pid}/{witness}")
            if finding["qualificationBasis"] == "generated" and result["failedTest"] != witness:
                raise ValueError(f"generated basis needs genuine first failure: {pid}/{result['failedTest']}")
            if result["failedTest"] != witness:
                result = {**result, "executionFirstFailedTest": result["failedTest"], "failedTest": witness}
        reruns.append({k: source[k] for k in ("submissionId", "sourceHash", "expected", "language", "source", "url")} | result)
        print(pid, source["submissionId"], result["verdict"], result.get("failedTest"), flush=True)
    old_invalid = [r for r in finding["references"] if r["expected"] != "OK"
                   and (not r.get("algorithmicWrongAnswer") or str(r["submissionId"]) in excluded)]
    evidence = {**original, "submissions": reruns,
                "excludedSubmissions": original["excludedSubmissions"] + [
                    {"id": r["submissionId"], "reason": "rejected by independent algorithmic-WA audit", "sourceHash": r["sourceHash"]}
                    for r in old_invalid],
                "status": "execution-passed", "acceptedContradiction": False,
                "failurePointerPolicy": "Official-basis references may point to a later normally terminating mathematical witness; raw replay first failure remains in executionFirstFailedTest and state. Generated-basis references retain the first failure.",
                "auditStatus": "fresh independent algorithmic review required"}
    if manifest(target) != original["files"]:
        raise ValueError(f"package changed during replay: {pid}")
    output = BASE / "evidence" / (pid + ".json")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and read(output) != evidence:
        historical = read(output)
        write_json(BASE / "state" / pid / "evidence-history" / (digest(historical) + ".json"), historical)
    write_json(output, evidence)
    (BASE / "review").mkdir(parents=True, exist_ok=True)
    write_json(BASE / "review" / (pid + ".json"), {
        "id": pid, "priorPackageHash": original["packageHash"],
        "priorEvidenceHash": digest(original), "priorAuditor": finding["reviewer"],
        "priorAuditApproved": False, "priorAuditReasons": finding["reasons"],
        "replacement": replacement, "replayEvidenceHash": digest(evidence),
        "auditStatus": "different-agent review required"})
    return {"id": pid, "status": "execution-passed; not independently audited",
            "packageHash": evidence["packageHash"], "evidenceHash": digest(evidence)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--replacements", type=Path, required=True)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    print(json.dumps(apply(args.id, read(args.audit), read(args.replacements)[args.id])), flush=True)


if __name__ == "__main__":
    main()
