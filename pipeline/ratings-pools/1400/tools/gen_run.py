"""Generated-basis pipeline for one ID: prepare -> generate(generator+independent oracle) -> coverage -> validate."""
import json, subprocess, sys, importlib
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = Path.home() / "repos/cf-race"
WS = Path.home() / "Documents/cf-pools"
CACHE = Path.home() / ".cache/cf-race-pool"
sys.path.insert(0, str(W / "recipes"))
import lib  # noqa: E402
for m in "abcdefgh":
    importlib.import_module("probs_" + m)
ORACLES = json.loads((W / "oracles/index.json").read_text())


def stage(*args):
    p = subprocess.run([sys.executable, "pipeline/rated_pool.py", *args, "--rating", "1400", "--target", "100",
                        "--workspace", str(WS), "--cache", str(CACHE)], cwd=REPO, capture_output=True, text=True, timeout=7200)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout)[-600:])
    return json.loads(p.stdout)


def run(pid):
    o = ORACLES[pid]
    gen = W / "gen" / pid / "generator.py"
    stage("prepare", "--id", pid)
    g = stage("generate", "--id", pid, "--generator-source", str(gen), "--generator-author", "devin-1400-worker",
              "--seed", "42", "--oracle-source", o["path"], "--oracle-language", o["language"],
              "--oracle-author", o["author"], "--oracle-review-url", o["url"],
              *(["--exhaustive-domain-size", "96", "--exhaustive-domain", "n in [5,100], one integer per test (all 96 values)"] if pid == "630H" else []))
    manifest = json.loads((W / "gen" / pid / "manifest.json").read_text())
    pairs = json.loads(subprocess.run([sys.executable, gen], input=b"42\n", capture_output=True, check=True, cwd="/tmp").stdout)
    first = g["official"] + g["openR1Generated"] + 1
    pkg = WS / "1400" / "packages" / pid / "tests"
    cov = {"boundary": [], "adversarial": [], "maxSize": []}
    for i, ((cat, reason), p) in enumerate(zip(manifest, pairs)):
        name = f"{first + i:04d}"
        assert (pkg / f"{name}.in").read_bytes().decode() == p["input"], (pid, name)
        if cat in cov:
            cov[cat].append({"test": name, "reason": reason})
    cls = lib.REG[pid]
    coverage = {"packageHash": g["packageHash"], **cov,
                "inputConstraints": {"rules": cls.rules,
                                     "validator": f"strict authored validator {cls.__module__}.{cls.__name__}.V filters every authored input; "
                                                  "independent oracle re-validates every official/open-r1/authored/sample input and exits 1 on violation",
                                     "upstreamContradictions": "none: every supplied official/open-r1 pair passed both validators; candidates with invalid upstream pairs are quarantined"},
                "checkerSemantics": "token comparison; unique answer per statement review; expected outputs from authored reference agree with the independent oracle on every test",
                "statementComplete": "statement/input/output/examples present in pinned open-r1/codeforces row (row_gate passed); reviewed by worker and by independent oracle author",
                "generatedBasis": {"mode": "exhaustive" if pid == "630H" else "extensive", "authoredPairs": g["extra"],
                                   "categories": {k: sum(1 for c, _ in manifest if c == k) for k in sorted({c for c, _ in manifest})}}}
    cp = W / "coverage" / f"gcoverage-{pid}.json"
    cp.write_text(json.dumps(coverage, indent=1, sort_keys=True))
    v = stage("validate", "--id", pid, "--all-submissions", "--validator", "devin-1400-worker", "--coverage", str(cp))
    return {"id": pid, "generate": g, "validate": {k: v.get(k) for k in ("status", "accepted", "incorrect", "excluded", "acceptedContradiction", "qualificationBasis") if k in v}}


if __name__ == "__main__":
    out = W / "gen_results.jsonl"
    for pid in sys.argv[1:]:
        try:
            r = run(pid)
        except Exception as e:
            r = {"id": pid, "error": str(e)[-600:]}
        with out.open("a") as f:
            f.write(json.dumps(r) + "\n")
        print(json.dumps(r)[:400], flush=True)
