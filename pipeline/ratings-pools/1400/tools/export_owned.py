"""Sync worker-owned, non-test artifacts into pipeline/ratings-pools/1400 (tests stay gitignored; archived separately)."""
import json, shutil
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = Path.home() / "repos/cf-race"
WS = Path.home() / "Documents/cf-pools/1400"
OUT = REPO / "pipeline/ratings-pools/1400"


def cp(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / ".gitignore").write_text("packages/*/tests/\nstate/\nsubmissions/\n__pycache__/\n*.tar.gz\ntests/\n")
for f in ("inventory.json", "api-problems.json"):
    cp(WS / f, OUT / f)
for f in ("build.py", "gen_run.py", "bundle.py", "add_oracles.py", "index_subs.py", "count_subs.py", "extract.py",
          "mkpacket.py", "samplecheck.py", "stmt.py", "export_owned.py", "pipeline_run.sh", "oracle_batches.json",
          "subcounts.json", "todo1.txt", "gen_results.jsonl"):
    if (W / f).exists():
        cp(W / f, OUT / "tools" / f)
cp(W / "NOTES.md", OUT / "STATUS.md")
for f in (W / "recipes").glob("*.py"):
    cp(f, OUT / "recipes" / f.name)
for f in (W / "checks").glob("*.json"):
    cp(f, OUT / "recipe-checks" / f.name)
for d in sorted((W / "gen").iterdir()):
    for f in ("generator.py", "manifest.json", "build.json"):
        if (d / f).exists():
            cp(d / f, OUT / "generators" / d.name / f)
for f in (W / "coverage").glob("gcoverage-*.json"):
    cp(f, OUT / "coverage" / (f.name[len("gcoverage-"):]))
for f in (W / "coverage").glob("coverage-*.json"):
    cp(f, OUT / "coverage" / "pre-v2" / (f.name[len("coverage-"):]))
idx = json.loads((W / "oracles/index.json").read_text())
rel = {}
for pid, o in sorted(idx.items()):
    src = Path(o["path"])
    dst = OUT / "oracles" / pid / src.name
    cp(src, dst)
    rel[pid] = {**o, "path": str(dst.relative_to(OUT)), "sourceArchive": src.parts[-3]}
(OUT / "oracles/index.json").write_text(json.dumps(rel, indent=1, sort_keys=True) + "\n")
for f in (WS / "evidence").glob("*.json"):
    cp(f, OUT / "evidence" / f.name)
for d in sorted((WS / "packages").iterdir()):
    for f in d.rglob("*"):
        if f.is_file() and "tests" not in f.relative_to(d).parts:
            cp(f, OUT / "packages" / d.name / f.relative_to(d))
print("exported to", OUT)
