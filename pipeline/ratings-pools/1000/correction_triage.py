"""Inventory independent exclusions without changing the original audit's byte bindings."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def indexed_sources(pid):
    rows = []
    for marker in sorted((HERE / "submissions").glob("*/complete.json")):
        metadata = read(marker)
        name = pid + ".json"
        if name not in metadata["files"]:
            continue
        source = marker.parent / name
        if hashlib.sha256(source.read_bytes()).hexdigest() != metadata["files"][name]:
            raise ValueError(f"pinned index checksum changed: {source}")
        for row in read(source):
            if row["problem_id"].replace("/", "") != pid:
                raise ValueError(f"wrong problem in {source}")
            if row["provenance"] != metadata["source"]:
                raise ValueError(f"unpinned source in {source}")
            rows.append(row)
    seen_ids, seen_hashes = set(), set()
    distinct = []
    for row in sorted(rows, key=lambda r: int(r["submission_id"])):
        digest = hashlib.sha256((row.get("source") or "").encode()).hexdigest()
        if (not row.get("source") or row["submission_id"] in seen_ids
                or digest in seen_hashes):
            continue
        seen_ids.add(row["submission_id"])
        seen_hashes.add(digest)
        distinct.append(row)
    return distinct


def triage(audit):
    result = []
    for pid in audit["excludedIds"]:
        problem = audit["problems"][pid]
        used = {str(ref["submissionId"]) for ref in problem["references"]}
        used_hashes = {ref["sourceHash"] for ref in problem["references"]}
        available = indexed_sources(pid)
        replacements = [row for row in available
                        if str(row["submission_id"]) not in used
                        and hashlib.sha256(row["source"].encode()).hexdigest() not in used_hashes
                        and row.get("testset") == "TESTS"
                        and row.get("programmingLanguage", "").startswith("Python 3")
                        and row.get("verdict") == "WRONG_ANSWER"]
        result.append({"id": pid, "basis": problem["qualificationBasis"],
                       "alreadyProvenWrong": problem["algorithmicIncorrectKilled"],
                       "missingProvenWrong": 5 - problem["algorithmicIncorrectKilled"],
                       "unusedDistinctPythonWrongAnswerRows": len(replacements),
                       "unusedWrongSubmissionIds": [str(r["submission_id"]) for r in replacements],
                       "historicalReasons": problem["reasons"]})
    return sorted(result, key=lambda p: (p["missingProvenWrong"],
                                         -p["unusedDistinctPythonWrongAnswerRows"], p["id"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = read(args.audit)
    if (audit["builderHead"] != "dbdca5cb4e9aedc997cd4ea1f7926d668e3639c3"
            or audit["independentlyValidated"] != 66):
        raise ValueError("unexpected independent audit; inspect before proceeding")
    rows = triage(audit)
    args.output.write_text(json.dumps({
        "auditHead": audit["builderHead"], "auditor": audit["reviewer"],
        "originallyApproved": audit["passedIds"], "held": rows,
        "warning": "Catalog supply is not an algorithmic witness or independent audit."
    }, sort_keys=True, indent=2) + "\n")
    print("held", len(rows), "one-replacement", Counter(r["missingProvenWrong"] for r in rows))
    print("unused candidate counts", [(r["id"], r["unusedDistinctPythonWrongAnswerRows"])
                                      for r in rows if r["missingProvenWrong"] == 1])


if __name__ == "__main__":
    main()
