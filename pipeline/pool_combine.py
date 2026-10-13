"""Local, data-only reconstruction and cross-pool evidence replay."""
import argparse
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
            any(p in ("..", ".") for p in name.split("/")) or
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
    destination.mkdir(parents=True)
    files, seen, expanded = {}, set(), 0
    try:
        with tarfile.open(archive, "r|gz") as stream:
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


def replay(index, root, output):
    root = Path(root).resolve()
    seen, entries, counts = set(), [], {str(r): 0 for r in RATINGS}
    empty = root / "empty-publication-approval.json"
    write_json(empty, {})
    for entry in index["entries"]:
        pid, rating = entry["id"], entry["rating"]
        if not re.fullmatch(r"[1-9][0-9]*[A-Z][0-9]*", pid) or pid in seen or rating not in RATINGS:
            raise ValueError("invalid, aliased or duplicate cross-pool identity")
        seen.add(pid)
        paths = {key: root / relative_name(entry[key]) for key in ("package", "evidence", "audit")}
        evidence, audit = read_json(paths["evidence"]), read_json(paths["audit"])
        meta = read_json(paths["package"] / "meta.json")
        if meta.get("id") != pid or meta.get("rating") != rating:
            raise ValueError("index/package rating identity mismatch")
        for key, value in (("packageHash", evidence["packageHash"]),
                           ("evidenceHash", digest(evidence)), ("auditHash", digest(audit))):
            if entry[key] != value:
                raise ValueError(f"index binding changed: {pid}/{key}")
        verify_evidence(paths["package"], evidence, audit)
        wrong = [r for r in evidence["submissions"] if r["expected"] != "OK"]
        if len(wrong) < 5 or any(r["verdict"] != "WA" for r in wrong):
            raise ValueError("technical pool requires five algorithmic WA references, not timeouts")
        dry = publication_gate(paths["package"], paths["evidence"].parent.parent.parent,
                               require_approval=False)
        if dry["legacy"]:
            raise ValueError("legacy allowance is not validation")
        try:
            publication_gate(paths["package"], paths["evidence"].parent.parent.parent,
                             approval_path=empty, require_approval=True)
        except ValueError as error:
            if "explicit content-bound publication approval required" not in str(error):
                raise
        else:
            raise ValueError("empty publication approval unexpectedly allowed")
        counts[str(rating)] += 1
        entries.append({"id": pid, "rating": rating, **{k: dry[k] for k in
                        ("packageHash", "evidenceHash", "auditHash")}})
    report = {"schemaVersion": 1, "technicalCounts": counts,
              "technicalTotal": len(entries), "shortfalls": {r: max(0, 100 - n) for r, n in counts.items()},
              "publicationApproved": 0, "published": 0, "publicCodeExecuted": False,
              "dryGatesPassed": len(entries), "emptyApprovalsRejected": len(entries),
              "indexHash": digest(index), "entries": entries}
    write_json(output, report)
    return report


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
        result = replay(read_json(args.index), args.root, args.output)
        print(json.dumps({k: v for k, v in result.items() if k != "entries"}))


if __name__ == "__main__":
    main()
