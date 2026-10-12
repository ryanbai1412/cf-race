"""Rating-1400 worker driver: check authored validator/oracle against every supplied pair, brute cross-check,
emit worker-generated tests, run pipeline generate, and write packageHash-bound coverage review."""
import argparse, glob, hashlib, importlib, json, subprocess, sys, time
from pathlib import Path
REPO = Path("/home/ubuntu/repos/cf-race")
W = Path.home() / "Documents/w1400"
BASE = Path.home() / "Documents/cf-pools/1400"
CACHE = str(Path.home() / ".cache/cf-race-pool")
sys.path[:0] = [str(REPO / "pipeline"), str(W / "recipes")]
from pool_sources import generated_tests
from checker import check
import lib
for f in sorted(glob.glob(str(W / "recipes/probs_*.py"))):
    importlib.import_module(Path(f).stem)


def sha(b):
    return hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()


def norm(s):
    return s if s.endswith("\n") else s + "\n"


def build(pid, run_generate=True):
    cls = lib.REG[pid]
    row = json.loads((BASE / "state" / pid / "source-row.json").read_text())
    gen, gsrc = generated_tests(row, CACHE)
    supplied = [("official", t["input"], t["output"]) for t in row["official_tests"]] + \
               [("open-r1-generated", t["input"], t["output"]) for t in gen] + \
               [("example", t["input"], t["output"]) for t in (row.get("examples") or [])]
    report = {"id": pid, "rules": cls.rules, "officialIncluded": len(row["official_tests"]),
              "officialAdvertised": row["testset_size"], "officialComplete": row["official_tests_complete"],
              "generatedIncluded": len(gen), "generatedAdvertised": row["generated_tests"],
              "invalidInputs": [], "oracleMismatches": [], "bruteMismatches": [], "extraInvalid": []}
    t0 = time.time()
    for i, (origin, inp, out) in enumerate(supplied):
        try:
            cls.V(inp)
        except Exception as e:
            report["invalidInputs"].append({"index": i, "origin": origin, "inputHash": sha(inp), "error": str(e)[:200]})
            continue
        got = cls.S(inp)
        if not check(out, got):
            report["oracleMismatches"].append({"index": i, "origin": origin, "inputHash": sha(inp),
                                               "expected": out[:120], "oracle": got[:120]})
    report["suppliedChecked"] = len(supplied)
    if getattr(cls, "B", None) and cls.brute_cases:
        r = lib.rng(pid + "-brute")
        n = 0
        for _ in range(cls.brute_cases):
            inp = cls.SMALL(r)
            try:
                cls.V(inp)
            except Exception as e:
                report["bruteMismatches"].append({"input": inp[:200], "error": "SMALL invalid: " + str(e)[:100]})
                continue
            n += 1
            a, b = cls.S(inp), cls.B(inp)
            if not check(b, a):
                report["bruteMismatches"].append({"input": inp[:200], "oracle": a[:80], "brute": b[:80]})
        report["bruteChecked"] = n
    extras, cov = [], {"boundary": [], "adversarial": [], "maxSize": []}
    base_index = len(row["official_tests"]) + len(gen)
    for cat, reason, inp in cls.G():
        inp = norm(inp)
        try:
            cls.V(inp)
        except Exception as e:
            report["extraInvalid"].append({"reason": reason, "error": str(e)[:200]})
            continue
        out = norm(cls.S(inp))
        extras.append({"input": inp, "output": out})
        cov[cat].append({"test": f"{base_index + len(extras):04d}", "reason": reason, "origin": "worker-generated"})
    report["extraCount"] = len(extras)
    report["oracleSeconds"] = round(time.time() - t0, 2)
    clean = not (report["invalidInputs"] or report["oracleMismatches"] or report["bruteMismatches"] or report["extraInvalid"])
    report["recipeClean"] = clean and all(cov.values())
    (W / "checks" / f"{pid}.json").write_text(json.dumps(report, indent=1, sort_keys=True))
    if not report["recipeClean"] or not run_generate:
        return report
    ep = W / "extra" / f"extra-{pid}.json"
    ep.write_text(json.dumps(extras, indent=1, sort_keys=True))
    res = subprocess.run([sys.executable, str(REPO / "pipeline/rated_pool.py"), "generate", "--rating", "1400", "--target", "100",
                          "--workspace", str(BASE.parent), "--cache", CACHE, "--id", pid, "--extra-tests", str(ep)],
                         capture_output=True, text=True, cwd=REPO)
    if res.returncode:
        report["generateError"] = (res.stderr or res.stdout)[-400:]
        report["recipeClean"] = False
        (W / "checks" / f"{pid}.json").write_text(json.dumps(report, indent=1, sort_keys=True))
        return report
    g = json.loads(res.stdout)
    basis = "official-complete" if row["official_tests_complete"] is True else "generated-full-suite (official truncated: %d/%d included)" % (len(row["official_tests"]), row["testset_size"])
    coverage = {"packageHash": g["packageHash"], **cov,
                "suiteBasis": basis,
                "inputConstraints": {"rules": cls.rules, "validator": f"recipes/{cls.__module__}.py::{cls.__name__}.V",
                                     "suppliedInputsValidated": len(supplied), "extraInputsValidated": len(extras)},
                "checkerSemantics": "token comparison; unique answer per statement review; authored oracle " +
                                    f"{cls.__module__}.{cls.__name__}.S matched all {len(supplied)} supplied outputs" +
                                    (f"; brute {cls.__name__}.B agreed on {report.get('bruteChecked')} random small inputs" if report.get("bruteChecked") else ""),
                "statementComplete": "statement/input/output/examples present in pinned open-r1/codeforces row (row_gate passed)",
                "recipeCheckHash": sha((W / "checks" / f"{pid}.json").read_bytes())}
    cp = W / "coverage" / f"coverage-{pid}.json"
    cp.write_text(json.dumps(coverage, indent=1, sort_keys=True))
    report["generate"] = g
    (W / "checks" / f"{pid}.json").write_text(json.dumps(report, indent=1, sort_keys=True))
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    for pid in a.ids:
        try:
            r = build(pid, not a.check_only)
            print(pid, "CLEAN" if r["recipeClean"] else "DIRTY", "sup", r["suppliedChecked"], "inv", len(r["invalidInputs"]),
                  "mis", len(r["oracleMismatches"]), "brute", len(r["bruteMismatches"]), r.get("bruteChecked", ""), "xinv", len(r["extraInvalid"]),
                  "x", r["extraCount"], r["oracleSeconds"], "s", r.get("generateError", "")[:200], flush=True)
        except Exception as e:
            print(pid, "ERROR", type(e).__name__, str(e)[:300], flush=True)
