"""Rating-1200 worker driver for the foundation generated-qualification basis.

precheck: host-side self-check of pipeline/problems/<ID>/recipe.py (authored reference vs every upstream pair,
          >=100 distinct authored inputs, generator output size) -- diagnostic only.
run:      build generator.py, then rated_pool.py generate (sandboxed generator twice + independent oracle over
          every supplied pair) -> coverage -> validate (5 accepted / 5 incorrect external programs).
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve()
POOL = HERE.parents[2]
PIPELINE = HERE.parents[3]
sys.path.insert(0, str(PIPELINE))
sys.path.insert(0, str(HERE.parent))
from build import build, labelled  # noqa: E402
from checker import check  # noqa: E402
from pool_contract import read_json, write_json  # noqa: E402
import tree_cache  # noqa: E402,F401
from pool_sources import generated_tests  # noqa: E402

RATING = 1200
SEED = 1200
KINDS = ("boundary", "adversarial", "maxSize")
GENERATOR_AUTHOR = "devin-1200-worker (https://staging.itsdev.in/sessions/444752a56bd9498fb7a8974d04ca5237)"
VALIDATOR = "devin-1200-pool-validator (https://staging.itsdev.in/sessions/444752a56bd9498fb7a8974d04ca5237)"
ORACLES = POOL / str(RATING) / "oracles.json"
CACHE = str(Path.home() / ".cache" / "cf-race-pool")


def load(pid):
    path = PIPELINE / "problems" / pid / "recipe.py"
    spec = importlib.util.spec_from_file_location(f"recipe_{pid}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def upstream(pid):
    row = read_json(POOL / str(RATING) / "state" / pid / "source-row.json")
    generated, _ = generated_tests(row, CACHE)
    return row, [("official", p) for p in row["official_tests"]] + [("open-r1-generated", p) for p in generated]


def precheck(pid):
    recipe = load(pid)
    row, pairs = upstream(pid)
    mismatches = []
    for i, (origin, pair) in enumerate(pairs + [("example", e) for e in row["examples"]], 1):
        got = recipe.solve(pair["input"])
        if not check(pair["output"], got):
            mismatches.append({"index": i, "origin": origin, "input": pair["input"][:200],
                               "expected": pair["output"][:100], "got": got[:100]})
    start = time.time()
    cases = labelled(recipe, SEED)
    payload = json.dumps([{"input": t, "output": recipe.solve(t)} for _, _, t in cases])
    kinds = {k: sum(c[0] == k for c in cases) for k in KINDS + ("random",)}
    return {"id": pid, "upstream": len(pairs), "mismatches": mismatches[:3], "mismatchCount": len(mismatches),
            "distinct": len(cases), "kinds": kinds, "bytes": len(payload), "hostSeconds": round(time.time() - start, 2),
            "ok": not mismatches and len(cases) >= 100 and len(payload) < 7_000_000 and all(kinds[k] for k in KINDS)}


def coverage(pid, recipe, package_hash, offset, oracle):
    entries = {k: [] for k in KINDS}
    cases = labelled(recipe, SEED)
    for i, (kind, reason, _) in enumerate(cases, offset + 1):
        if kind in entries:
            entries[kind].append({"test": f"{i:04d}", "reason": reason})
    basis = (f"Every supplied pair ({offset} upstream supplementary + {len(cases)} authored) was executed by the "
             f"independently authored oracle ({oracle['author']}), which strictly validates all statement constraints "
             f"and exits nonzero on violation, and reproduced the expected output under the problem limits in the "
             f"bounded sandbox (qualification/oracle.json). Authored inputs come from pipeline/problems/{pid}/recipe.py cases().")
    return {"packageHash": package_hash, **entries, "inputConstraints": basis,
            "checkerSemantics": recipe.CHECKER, "statementComplete": recipe.STATEMENT}


def cli(stage, pid, extra=()):
    command = [sys.executable, str(HERE.parent / "tree_cache.py"), stage, "--rating", str(RATING), "--id", pid,
               "--workspace", str(POOL), "--cache", CACHE, *extra]
    proc = subprocess.run(command, capture_output=True, text=True, cwd=PIPELINE)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"status": "blocked", "reason": (proc.stdout + proc.stderr)[-1500:]}


def run(pid):
    oracle = read_json(ORACLES)[pid]
    recipe = load(pid)
    generator = build(pid)
    language = "GNU C++17 7.3.0" if oracle["file"].endswith(".cpp") else "Python 3"
    gen = cli("generate", pid, ["--generator-source", str(generator), "--generator-author", GENERATOR_AUTHOR,
                                "--seed", str(SEED), "--oracle-source", str(PIPELINE / "problems" / pid / oracle["file"]),
                                "--oracle-language", language, "--oracle-author", oracle["author"],
                                "--oracle-review-url", oracle["reviewUrl"]])
    if gen.get("status") != "generated":
        return {"id": pid, "stage": "generate", **gen}
    path = POOL / str(RATING) / "coverage" / f"{pid}.json"
    write_json(path, coverage(pid, recipe, gen["packageHash"], gen["official"] + gen["openR1Generated"], oracle))
    res = cli("validate", pid, ["--coverage", str(path), "--validator", VALIDATOR, "--all-submissions"])
    return {"id": pid, "stage": "validate", "tests": gen["testCount"],
            **{k: res.get(k) for k in ("status", "accepted", "incorrect", "excluded", "reason", "qualificationBasis")}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("precheck", "run"))
    parser.add_argument("ids", nargs="+")
    args = parser.parse_args()
    for pid in args.ids:
        try:
            result = precheck(pid) if args.stage == "precheck" else run(pid)
        except Exception as exc:  # one recipe bug must not stop the batch
            result = {"id": pid, "status": "error", "reason": repr(exc)[:600]}
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
