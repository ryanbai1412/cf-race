"""Build reproducible rating-800 audit archives: one foundation `archive` per package with evidence, then a deterministic
bundle of those archives, generated-qualification inputs (generator/oracle sources, logs), worker recipes/tools, inventory,
exclusions and the worker report, plus a SHA-256 manifest of every bundled file."""
import gzip
import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
POOL = REPO / "pipeline/ratings-pools/800"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def add_tree(tar, root, arcroot, manifest):
    for path in [root, *sorted(root.rglob("*"))] if root.is_dir() else [root]:
        if "__pycache__" in path.parts or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        name = arcroot if rel == "." else f"{arcroot}/{rel}"
        info = tar.gettarinfo(str(path), arcname=name)
        info.mtime = info.uid = info.gid = 0
        info.uname = info.gname = ""
        info.mode = 0o755 if path.is_dir() else 0o644
        if path.is_file():
            manifest[name] = {"sha256": sha(path), "bytes": path.stat().st_size}
            with path.open("rb") as content:
                tar.addfile(info, content)
        else:
            tar.addfile(info)


def main(workspace, out_dir, *ids):
    base, out = Path(workspace) / "800", Path(out_dir)
    per = out / "packages"
    per.mkdir(parents=True, exist_ok=True)
    ids = ids or sorted(p.stem for p in (base / "evidence").glob("*.json"))
    for pid in ids:
        subprocess.run([sys.executable, "pipeline/rated_pool.py", "archive", "--rating", "800", "--id", pid,
                        "--workspace", workspace, "--output", str(per / f"{pid}.tar.gz")],
                       cwd=REPO, check=True, stdout=subprocess.DEVNULL)
    manifest = {}
    bundle = out / "rated-800-audit-bundle.tar.gz"
    with bundle.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as z, \
            tarfile.open(fileobj=z, mode="w") as tar:
        add_tree(tar, per, "packages", manifest)
        for pid in ids:
            gq = base / "gen-qualification" / pid
            if gq.exists():
                add_tree(tar, gq, f"gen-qualification/{pid}", manifest)
        for sub in ("recipes", "genrecipes", "tools"):
            add_tree(tar, POOL / sub, f"worker/{sub}", manifest)
        for name in ("inventory.json", "api-problems.json", "report.json"):
            if (base / name).exists():
                add_tree(tar, base / name, f"workspace/{name}", manifest)
        add_tree(tar, POOL / "exclusions.json", "worker/exclusions.json", manifest)
        report = out / "worker-report.json"
        if report.exists():
            add_tree(tar, report, "worker-report.json", manifest)
    prov = {"bundle": bundle.name, "sha256": sha(bundle), "bytes": bundle.stat().st_size, "packages": list(ids),
            "commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip(),
            "files": manifest}
    (out / "rated-800-audit-bundle.provenance.json").write_text(json.dumps(prov, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: prov[k] for k in ("bundle", "sha256", "bytes", "commit")} | {"nPackages": len(ids), "nFiles": len(manifest)}))


if __name__ == "__main__":
    main(*sys.argv[1:])
