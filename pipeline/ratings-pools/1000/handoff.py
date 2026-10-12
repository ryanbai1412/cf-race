"""Report current-byte mechanical gates without creating or impersonating an audit."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1])]
from pool_contract import digest, manifest, read_json, verify_evidence, write_json
from pool_generation import sandbox, verify_generated
from pool_sources import PINS
import worker


def expected_missing_audit(call, expected):
    try:
        call()
    except ValueError as exc:
        return str(exc) == expected, str(exc)
    return False, "unexpected success without audit"


def main():
    inventory = read_json(HERE / "inventory.json")
    scan = read_json(HERE / "source-scan.json")
    records, ready, problems = [], [], sorted(set(worker.IDS))
    for pid in problems:
        package = HERE / "packages" / pid
        semantic = read_json(HERE / "semantics" / f"{pid}.json")
        evidence_path = HERE / "evidence" / f"{pid}.json"
        provenance = read_json(package / "provenance.json")
        basis = provenance.get("qualification", {}).get("basis", "official" if provenance["tests"].get("officialComplete") else "unqualified")
        record = {"id": pid, "qualificationBasis": basis, "semanticPassed": semantic["passed"],
                  "constraintsInvalid": semantic["invalid"], "validated": False, "audit": "different-agent audit required"}
        if not evidence_path.exists():
            record.update(status="no-execution-evidence", readyForIndependentAudit=False)
        else:
            evidence = read_json(evidence_path)
            files = manifest(package)
            record.update(status=evidence["status"], evidenceHash=digest(evidence), packageHash=digest(files),
                          accepted=sum(s["expected"] == "OK" for s in evidence["submissions"]),
                          incorrect=sum(s["expected"] != "OK" for s in evidence["submissions"]),
                          testCount=evidence["testCount"], acceptedContradiction=evidence["acceptedContradiction"])
            checks = {"currentSandbox": evidence["sandbox"] == sandbox(),
                      "currentRecipe": semantic["recipeHash"] == worker.recipe_hash(pid),
                      "currentSemanticBytes": semantic["packageHash"] == digest(files),
                      "semanticPassed": semantic["passed"], "sourceBytes": True}
            for submission in evidence["submissions"]:
                paths = list((HERE / "state" / pid / "sources").glob(str(submission["submissionId"]) + ".*"))
                if len(paths) != 1:
                    checks["sourceBytes"] = False
                    continue
                source = read_json(paths[0])
                checks["sourceBytes"] &= (hashlib.sha256(source["code"].encode()).hexdigest() == submission["sourceHash"]
                                          and all(source[key] == submission[key] for key in ("submissionId", "expected", "source", "sourceHash", "url")))
            checks["preAuditEvidence"], record["evidenceGate"] = expected_missing_audit(
                lambda: verify_evidence(package, evidence, {}), "audit is stale")
            if basis == "generated":
                checks["preAuditGeneratedProof"], record["generatedGate"] = expected_missing_audit(
                    lambda: verify_generated(package, files, provenance["tests"]["pairs"], evidence, {}),
                    "generated basis not explicitly declared in evidence/audit")
            record["mechanicalChecks"] = checks
            record["readyForIndependentAudit"] = all(checks.values())
            if record["readyForIndependentAudit"] and pid != "691A":
                ready.append(pid)
        record["deduplicatedExternal691A"] = pid == "691A"
        records.append(record)
    source_eligible = [p["id"] for p in scan["items"] if p["sourceCounts"].get("accepted", 0) >= 5 and p["sourceCounts"].get("incorrect", 0) >= 5]
    reports = [read_json(HERE / name) for name in ("selfcheck-report.json", "extended-selfcheck-report.json", "further-selfcheck-report.json")]
    summary = {"rating": 1000, "target": 100, "apiCandidates": len(inventory["items"]),
               "metadataEligible": inventory["metadataEligible"], "completeSourceEligible": inventory["completeSourceEligible"],
               "fiveAcceptedFiveIncorrectSupply": len(source_eligible), "recipes": len(problems),
               "semanticPassed": sum(r["semanticPassed"] for r in records), "semanticBlocked": sum(not r["semanticPassed"] for r in records),
               "qualificationBases": dict(Counter(r["qualificationBasis"] for r in records)),
               "executionStatuses": dict(Counter(r["status"] for r in records)),
               "mechanicallyCurrentExecutionPassed": sum(r.get("readyForIndependentAudit", False) for r in records),
               "auditReadyDistinctExcludingExternal691A": len(ready), "readyByBasis": dict(Counter(r["qualificationBasis"] for r in records if r["id"] in ready)),
               "workerAuditedCount": 0, "workerValidatedCount": 0,
               "recipeSelfchecksPassed": all(r["passed"] for r in reports),
               "recipeCrosschecks": sum(r["totalCrossChecks"] for r in reports)}
    value = {"schemaVersion": 1, "pins": PINS, "summary": summary, "auditReadyIds": ready, "problems": records,
             "external691A": {"status": "independently audited by foundation; not included in workerValidatedCount",
                              "archiveSHA256": "5d8d5f42fef6a82910a500cd01461791b6b9060b93c557bfe36e2c6f76ac83b2",
                              "packageHash": "297b17e6ed78262ef261ef0470ae599f71bbd577b1adce5ceaf0dfa8fa0c6969",
                              "evidenceHash": "7186ccd6f4b7464df492284528244001f8dc20df6a3a799146ba7cb849a7ad08",
                              "handling": "Do not regenerate external bytes or reuse its audit for this worker's different package."},
             "remainingGates": ["A different agent must independently inspect statements, exact constraints, single-answer semantics, boundary/max/adversarial coverage and oracle correctness.",
                                "Generated-basis incorrect sources require a per-submission algorithmic defect/counterexample audit; observed runtime rejection alone is insufficient.",
                                "Rerun public programs only in the pinned offline bounded sandbox, then sign current package/evidence hashes.",
                                "143A permits any solution in its statement; independently verify unique solvability using the exhaustive distinct-grid check before approving token comparison."],
             "reproduction": ["python3 pipeline/ratings-pools/1000/tests/test_recipes.py", "python3 pipeline/ratings-pools/1000/tests/test_extended.py", "python3 pipeline/ratings-pools/1000/tests/test_further.py", "python3 pipeline/ratings-pools/1000/handoff.py"]}
    write_json(HERE / "handoff-report.json", value)
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
