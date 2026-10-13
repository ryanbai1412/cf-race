"""Local, data-only reconstruction and cross-pool evidence replay."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile

from pool_contract import RATINGS, digest, publication_gate, read_json, verify_evidence, write_json
from pool_sources import sha_file


def relative_name(name):
    parts = PurePosixPath(name).parts
    if (not parts or name.startswith("/") or "\\" in name or
            any(p in ("", "..", ".") for p in name.split("/")) or
            any(":" in p for p in parts)):
        raise ValueError(f"unsafe archive path: {name}")
    return PurePosixPath(*parts).as_posix()


def extract(archive, destination, expected_sha256, max_bytes=8 * 1024 ** 3,
            max_members=150000):
    archive, destination = Path(archive), Path(destination)
    if not re.fullmatch(r"[a-f0-9]{64}", expected_sha256) or sha_file(archive) != expected_sha256:
        raise ValueError("archive SHA256 mismatch")
    if destination.exists():
        raise ValueError("extraction destination must not exist")
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("symlink in extraction destination")
    destination.mkdir(parents=True)
    files, seen, expanded = {}, set(), 0
    try:
        with gzip.open(archive, "rb") as compressed, tarfile.open(fileobj=compressed, mode="r|") as stream:
            for member in stream:
                name = relative_name(member.name.rstrip("/"))
                if name in seen or len(seen) >= max_members:
                    raise ValueError("duplicate member or member limit exceeded")
                seen.add(name)
                if not member.isfile() and not member.isdir():
                    raise ValueError("only regular files and directories are allowed")
                expanded += member.size
                if expanded > max_bytes or member.size < 0:
                    raise ValueError("expanded archive size limit exceeded")
                target = destination / name
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                h = hashlib.sha256()
                size = 0
                with stream.extractfile(member) as source, target.open("xb") as output:
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        output.write(chunk)
                        h.update(chunk)
                        size += len(chunk)
                if size != member.size:
                    raise ValueError("truncated archive member")
                files[name] = {"sha256": h.hexdigest(), "bytes": size}
            trailing_bytes = 0
            for chunk in iter(lambda: compressed.read(1024 * 1024), b""):
                trailing_bytes += len(chunk)
                if expanded + trailing_bytes > max_bytes:
                    raise ValueError("expanded archive size limit exceeded")
        return {"archiveSHA256": expected_sha256, "expandedBytes": expanded,
                "members": len(seen), "files": files}
    except Exception:
        shutil.rmtree(destination)
        raise


def verify_manifest(root, declared, ignored=()):
    root = Path(root)
    actual = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink in restored evidence")
        if path.is_file():
            name = path.relative_to(root).as_posix()
            if name not in ignored:
                actual[name] = {"sha256": sha_file(path), "bytes": path.stat().st_size}
    if set(actual) != set(declared):
        raise ValueError("manifest member set mismatch")
    for name, record in declared.items():
        relative_name(name)
        if actual[name] != record:
            raise ValueError(f"manifest hash/size mismatch: {name}")
    return len(actual)


def decision_record(entry, root):
    binding = entry["decision"]
    path = root / relative_name(binding["path"])
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.resolve().is_relative_to(root):
        raise ValueError("unsafe decision path")
    record = read_json(path)
    for key in binding["selector"]:
        record = record[key]
    if digest(record) != binding["recordHash"]:
        raise ValueError("current independent decision changed")
    if (record.get("approved") is False or record.get("primaryAuditApproved") is False or
            record.get("nativeAudit", {}).get("approved") is False):
        raise ValueError("current independent decision excludes candidate")
    if not (record.get("approved") is True or record.get("technicalState") == "qualified" or
            record.get("status") == "technical-pass" or record.get("outcome") == "TECHNICAL" or
            record.get("primaryVerdict") == "VALIDATED"):
        raise ValueError("current independent decision excludes candidate")
    if record.get("id", entry["id"]) != entry["id"]:
        raise ValueError("decision identity mismatch")
    for key in ("packageHash", "evidenceHash"):
        if record.get(key) != entry[key]:
            raise ValueError("decision belongs to different content")
    audit_hash = record.get("auditHash", record.get("auditDigest", record.get("primaryAuditHash",
                            record.get("nativeAudit", {}).get("auditHash", digest(record)))))
    if audit_hash != entry["auditHash"]:
        raise ValueError("decision belongs to different audit")
    return record


def replay(index, root, output):
    root = Path(root).resolve()
    seen, entries, counts = set(), [], {str(r): 0 for r in RATINGS}
    def local(name):
        path = root / relative_name(name)
        if any(p.is_symlink() for p in (path, *path.parents)) or not path.resolve().is_relative_to(root):
            raise ValueError("unsafe restored evidence path")
        return path

    for record in index.get("reviewArtifacts", []):
        if sha_file(local(record["path"])) != record["sha256"]:
            raise ValueError("changed independent review artifact")
    inventory = {}
    for row in index["decisions"]:
        pid = row["id"]
        if (not re.fullmatch(r"[1-9][0-9]*[A-Z][0-9]*", pid) or
                row["rating"] not in RATINGS or pid in inventory):
            raise ValueError("invalid, aliased or duplicate inventory identity")
        inventory[pid] = row
        binding = row["record"]
        record = read_json(local(binding["path"]))
        for key in binding["selector"]:
            record = record[key]
        if digest(record) != binding["recordHash"]:
            raise ValueError("inventory decision bytes changed")
    empty = local(index["emptyApproval"])
    if read_json(empty) != {}:
        raise ValueError("dry-run approval must be empty")
    source_count = 0
    for entry in index["entries"]:
        pid, rating = entry["id"], entry["rating"]
        if not re.fullmatch(r"[1-9][0-9]*[A-Z][0-9]*", pid) or pid in seen or rating not in RATINGS:
            raise ValueError("invalid, aliased or duplicate cross-pool identity")
        seen.add(pid)
        if entry.get("status") != "technical-validated":
            raise ValueError("provisional, rejected or held candidate in technical list")
        row = inventory.get(pid, {})
        if (row.get("status") != "technical-validated" or row.get("rating") != rating or
                row.get("record") != entry["decision"]):
            raise ValueError("technical list/inventory disagreement")
        decision_record(entry, root)
        paths = {key: local(entry[key]) for key in ("package", "evidence", "audit")}
        evidence, audit = read_json(paths["evidence"]), read_json(paths["audit"])
        meta = read_json(paths["package"] / "meta.json")
        if meta.get("id") != pid or meta.get("rating") != rating:
            raise ValueError("index/package rating identity mismatch")
        for key, value in (("packageHash", evidence["packageHash"]),
                           ("evidenceHash", digest(evidence)), ("auditHash", digest(audit))):
            if entry[key] != value:
                raise ValueError(f"index binding changed: {pid}/{key}")
        verify_evidence(paths["package"], evidence, audit)
        sources = {str(r["submissionId"]): r for r in entry["sources"]}
        runs = {str(r["submissionId"]): r for r in evidence["submissions"]}
        if len(sources) != len(entry["sources"]) or set(sources) != set(runs):
            raise ValueError("missing/duplicate source-byte bindings")
        for sid, record in sources.items():
            path = local(record["path"])
            source = read_json(path)
            if (sha_file(path) != record["sha256"] or str(source["submissionId"]) != sid or
                    hashlib.sha256(source["code"].encode()).hexdigest() != runs[sid]["sourceHash"] or
                    source["sourceHash"] != runs[sid]["sourceHash"] or source["source"] != runs[sid]["source"]):
                raise ValueError("changed public source bytes/attribution")
            source_count += 1
        wrong = [r for r in evidence["submissions"] if r["expected"] != "OK"]
        if len(wrong) < 5:
            raise ValueError("technical pool requires five independently reviewed incorrect references")
        analysis = audit.get("incorrectAnalysis", {})
        if any(analysis.get(str(r["submissionId"]), {}).get("kind") != "wrong-answer" or
               not analysis[str(r["submissionId"])].get("reason") for r in wrong):
            raise ValueError("missing independent algorithmic wrong-answer analysis")
        evidence_root = local(entry["evidenceRoot"])
        if (paths["evidence"] != evidence_root / str(rating) / "evidence" / f"{pid}.json" or
                paths["audit"] != evidence_root / str(rating) / "audits" / f"{pid}.json"):
            raise ValueError("gate paths must bind the indexed evidence and audit")
        dry = publication_gate(paths["package"], evidence_root,
                               require_approval=False)
        if dry["legacy"]:
            raise ValueError("legacy allowance is not validation")
        try:
            publication_gate(paths["package"], evidence_root,
                             approval_path=empty, require_approval=True)
        except ValueError as error:
            if "explicit content-bound publication approval required" not in str(error):
                raise
        else:
            raise ValueError("empty publication approval unexpectedly allowed")
        counts[str(rating)] += 1
        entries.append({"id": pid, "rating": rating, **{k: dry[k] for k in
                        ("packageHash", "evidenceHash", "auditHash")}})
    if seen != {pid for pid, row in inventory.items() if row["status"] == "technical-validated"}:
        raise ValueError("technical inventory entries omitted from replay")
    report = {"schemaVersion": 2, "technicalCounts": counts,
              "technicalTotal": len(entries), "shortfalls": {r: max(0, 100 - n) for r, n in counts.items()},
              "publicationApprovalGrantedByReplay": False,
              "productionPublicationPerformedByReplay": False,
              "publicationStatusQueried": False, "publicCodeExecuted": False,
              "sourceBindingsVerified": source_count,
              "dryGatesPassed": len(entries), "emptyApprovalsRejected": len(entries),
              "indexHash": digest(index), "entries": entries}
    write_json(output, report)
    return report


def replay_snapshot(snapshot, root, output):
    root = Path(root).resolve()
    path = root / relative_name(snapshot["bundleIndex"])
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.resolve().is_relative_to(root):
        raise ValueError("unsafe snapshot index path")
    index = read_json(path)
    if sha_file(path) != snapshot["bundleIndexFileSHA256"] or digest(index) != snapshot["bundleIndexHash"]:
        raise ValueError("snapshot index bytes changed")
    packages = [{k: entry[k] for k in ("id", "rating", "packageHash", "evidenceHash", "auditHash")}
                for entry in index["entries"]]
    counts = {str(r): sum(entry["rating"] == r for entry in packages) for r in RATINGS}
    if packages != snapshot["technicalPackages"] or counts != snapshot["technicalCounts"]:
        raise ValueError("snapshot package ledger/count disagreement")
    return replay(index, root, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    unpack = commands.add_parser("extract")
    unpack.add_argument("archive", type=Path)
    unpack.add_argument("destination", type=Path)
    unpack.add_argument("--sha256", required=True)
    unpack.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("replay")
    check.add_argument("index", type=Path)
    check.add_argument("--root", type=Path, required=True)
    check.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "extract":
        result = extract(args.archive, args.destination, args.sha256)
        write_json(args.output, result)
        print(json.dumps({k: v for k, v in result.items() if k != "files"}))
    else:
        index = read_json(args.index)
        run = replay_snapshot if "bundleIndex" in index else replay
        result = run(index, args.root, args.output)
        print(json.dumps({k: v for k, v in result.items() if k != "entries"}))


if __name__ == "__main__":
    main()
