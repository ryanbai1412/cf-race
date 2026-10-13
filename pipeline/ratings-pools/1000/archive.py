"""Reproducible local evidence archives; never uploads or marks a pool validated."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pool_sources import PINS


def files(path):
    candidates = [path] if path.is_file() else sorted(path.rglob("*")) if path.exists() else []
    for candidate in candidates:
        if candidate.is_symlink():
            raise ValueError(f"symlink forbidden: {candidate}")
        if candidate.is_file() and "__pycache__" not in candidate.parts and candidate.suffix != ".pyc":
            yield candidate


def problem_files(pid):
    paths = []
    for category in ("packages", "state", "qualification-sources"):
        paths.extend(files(HERE / category / pid))
    for category in ("extras", "semantics", "coverage", "evidence"):
        paths.extend(files(HERE / category / f"{pid}.json"))
    paths.extend((HERE / "outcomes").glob(f"{pid}*.json"))
    return sorted(set(paths))


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_archive(output, paths):
    provenance = {}
    with output.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as zipped, tarfile.open(fileobj=zipped, mode="w") as archive:
        for path in sorted(set(paths), key=lambda p: p.relative_to(HERE).as_posix()):
            name = "1000/" + path.relative_to(HERE).as_posix()
            before = sha(path)
            info = archive.gettarinfo(str(path), arcname=name)
            info.mtime = info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o644
            if not info.isfile():
                raise ValueError(f"nonregular archive input: {path}")
            with path.open("rb") as content:
                archive.addfile(info, content)
            if before != sha(path) or info.size != path.stat().st_size:
                raise ValueError(f"archive input changed: {path}")
            provenance[name] = {"sha256": before, "bytes": info.size}
    return {"archive": output.name, "sha256": sha(output), "bytes": output.stat().st_size, "files": provenance}


def verify_archive(output, record):
    if sha(output) != record["sha256"] or output.stat().st_size != record["bytes"]:
        raise ValueError("archive checksum/size mismatch")
    seen = set()
    with tarfile.open(output, "r:gz") as archive:
        for member in archive:
            if (member.name in seen or member.name not in record["files"] or not member.isfile()
                    or not member.name.startswith("1000/") or ".." in PurePosixPath(member.name).parts
                    or (member.uid, member.gid, member.mtime, member.mode) != (0, 0, 0, 0o644)):
                raise ValueError("unsafe or nonreproducible archive member")
            seen.add(member.name)
            checksum, count = hashlib.sha256(), 0
            with archive.extractfile(member) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    checksum.update(chunk)
                    count += len(chunk)
            expected = record["files"][member.name]
            if count != member.size or count != expected["bytes"] or checksum.hexdigest() != expected["sha256"]:
                raise ValueError("archive member hash/size mismatch")
    if seen != set(record["files"]):
        raise ValueError("missing archive members")
    return {"passed": True, "verifiedFiles": len(seen)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--parts", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.parts <= 16:
        parser.error("parts must be between1 and16")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    bundles = {p.name: problem_files(p.name) for p in sorted((HERE / "packages").iterdir()) if p.is_dir()}
    sizes = {pid: sum(p.stat().st_size for p in paths) for pid, paths in bundles.items()}
    groups, totals = [[] for _ in range(args.parts)], [0] * args.parts
    for pid in sorted(bundles, key=lambda x: (-sizes[x], x)):
        index = min(range(args.parts), key=lambda i: (totals[i], i))
        groups[index].append(pid)
        totals[index] += sizes[pid]
    records = []
    for i, group in enumerate(groups, 1):
        name = args.output_dir / f"rating-1000-evidence-part{i:02d}.tar.gz"
        record = write_archive(name, [p for pid in group for p in bundles[pid]])
        record["verification"] = verify_archive(name, record)
        record["problemIds"] = sorted(group)
        records.append(record)
        print(json.dumps({k: record[k] for k in ("archive", "sha256", "bytes", "problemIds")}), flush=True)
    shared = [p for p in HERE.iterdir() if p.is_file() and p.suffix in (".py", ".json", ".md")]
    shared.extend(files(HERE / "tests"))
    shared.extend(files(HERE / "diagnostics"))
    shared_archive = args.output_dir / "rating-1000-provenance-and-diagnostics.tar.gz"
    record = write_archive(shared_archive, shared)
    record["verification"] = verify_archive(shared_archive, record)
    records.append(record)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=HERE, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=HERE, text=True).strip()
    value = {"schemaVersion": 1, "rating": 1000, "branch": branch, "commit": commit,
             "pins": PINS, "validatedCount": 0, "auditStatus": "different-agent audit required",
             "archives": records, "excluded": ["bulk submission index cache; executed code is retained in state/PID/sources", "Python bytecode caches"]}
    (args.output_dir / "rating-1000-archives.provenance.json").write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
