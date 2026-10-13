"""Package immutable recovery evidence and verify original audit bindings."""
import argparse
import json
from pathlib import Path

from archive import files, sha, verify_archive, write_archive
from correction_replay import BASE, HERE, original_bytes
from correction_triage import read


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch", required=True)
    args = parser.parse_args()
    if not args.output_dir.is_dir():
        raise ValueError("output directory must already exist")
    audit = read(args.audit)
    locked = {}
    from pool_contract import digest, manifest
    pointer_corrections = {row["problem"]: row for row in audit["evidencePointerCorrections"]}
    for pid in audit["passedIds"]:
        package, original = original_bytes(pid)
        finding = audit["problems"][pid]
        prior_hash = digest(original)
        if prior_hash != finding["evidenceHash"] and (
                pid not in pointer_corrections
                or pointer_corrections[pid]["formerEvidenceHash"] != prior_hash):
            raise ValueError(f"unexplained audit/evidence mismatch: {pid}")
        locked[pid] = {"packageHash": original["packageHash"],
                       "originalEvidenceHash": prior_hash,
                       "auditorEvidenceHash": finding["evidenceHash"],
                       "pointerCorrection": pointer_corrections.get(pid)}
        if finding["packageHash"] != original["packageHash"]:
            raise ValueError(f"release-held original package changed: {pid}")
    ids = sorted(path.stem for path in (BASE / "evidence").glob("*.json"))
    if not ids:
        raise ValueError("no completed correction evidence")
    renewed = {}
    observations = read(HERE / "correction_source_observations.json")
    proposed = read(HERE / "correction_replacements_batch02.json")
    for pid in ids:
        _, original = original_bytes(pid)
        package = BASE / "packages" / pid
        evidence = read(BASE / "evidence" / f"{pid}.json")
        review = read(BASE / "review" / f"{pid}.json")
        if (pid in audit["passedIds"] or manifest(package) != original["files"]
                or evidence["packageHash"] != original["packageHash"]
                or evidence["files"] != original["files"]
                or review["replayEvidenceHash"] != digest(evidence)
                or review["priorEvidenceHash"] != digest(original)
                or review["auditStatus"] != "different-agent review required"):
            raise ValueError(f"recovery package/evidence binding mismatch: {pid}")
        witnesses = read(BASE / "review" / f"{pid}-witnesses.json")
        wrong = {str(r["submissionId"]): r for r in evidence["submissions"] if r["expected"] != "OK"}
        notes = observations["defects"].get(pid, {})
        if pid in proposed:
            candidate = proposed[pid]
            for new in [candidate] + candidate.get("additionalReplacements", []):
                new_id = new["submissionId"]
                if (new_id not in wrong or new["sourceHash"] != wrong[new_id]["sourceHash"]
                        or any(r["submissionId"] == new_id for r in original["submissions"])):
                    raise ValueError(f"unbound replacement source: {pid}/{new_id}")
                notes = {**notes, new_id: new["defect"]}
        if (not notes or not set(notes) <= set(wrong)
                or {r["submissionId"] for r in witnesses} != set(wrong)):
            raise ValueError(f"incomplete builder source observations/witnesses: {pid}")
        for witness in witnesses:
            if (not witness["potentialSemanticMismatch"]
                    or witness["sourceHash"] != wrong[witness["submissionId"]]["sourceHash"]
                    or witness["inputHash"] != sha(package / "tests" / (witness["test"] + ".in"))
                    or witness["expectedOutputHash"] != sha(package / "tests" / (witness["test"] + ".out"))):
                raise ValueError(f"unproven normally terminating semantic witness: {pid}")
        if pid in proposed:
            for new in [proposed[pid]] + proposed[pid].get("additionalReplacements", []):
                if not any(w["submissionId"] == new["submissionId"] and w["test"] == new["test"]
                           for w in witnesses):
                    raise ValueError(f"wrong selected mathematical witness: {pid}")
        renewed[pid] = {"packageHash": evidence["packageHash"],
                        "priorEvidenceHash": review["priorEvidenceHash"],
                        "newEvidenceHash": digest(evidence),
                        "builderSourceObservations": sorted(notes),
                        "retainedSourceReferencesNeedingFreshReview": sorted(set(wrong) - set(notes)),
                        "freshIndependentDefectAudit": False}
    selected = list(files(BASE)) + [p for p in HERE.iterdir() if p.is_file() and p.suffix in (".py", ".json", ".md")]
    for pid in ids:
        selected.extend(files(HERE / "qualification-sources" / pid))
        for category in ("extras", "semantics", "coverage"):
            selected.extend(files(HERE / category / (pid + ".json")))
    selected.extend(files(HERE / "tests"))
    target = args.output_dir / f"rating-1000-{args.batch}.tar.gz"
    if target.exists():
        raise ValueError("immutable archive already exists; choose a new batch name")
    record = write_archive(target, selected)
    record["verification"] = verify_archive(target, record)
    replay = target.with_name(target.stem + ".reproduced.tar.gz")
    second = write_archive(replay, selected)
    if (record["sha256"], record["bytes"]) != (second["sha256"], second["bytes"]):
        raise ValueError("nonreproducible recovery archive")
    replay.unlink()
    provenance = {"rating": 1000, "originalAuditHead": audit["builderHead"],
                  "originalAuditReviewer": audit["reviewer"],
                  "releaseValidatedBaseline": 1,
                  "priorMechanicallyPassingButReleaseHeld": len(locked),
                  "unchangedPriorReleaseHeldBindings": locked,
                  "originallyExcluded": audit["excludedIds"],
                  "newRecovery": renewed,
                  "auditStatus": "new recovery needs a DIFFERENT source-level auditor; no new validation claimed",
                  "archive": record}
    output = args.output_dir / f"rating-1000-{args.batch}.provenance.json"
    output.write_text(json.dumps(provenance, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"archive": str(target), "sha256": sha(target),
                      "bytes": record["bytes"], "members": len(record["files"]),
                      "recoveryIds": ids, "provenance": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
