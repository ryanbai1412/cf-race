"""Generated-basis pipeline for one rating-800 candidate: prepare, generate (worker generator + attributed public
oracle), coverage, validate. The oracle is one fixed public accepted submission chosen deterministically from the
newest end of the pool, away from the oldest accepted sources that validate counts. A failing oracle quarantines the
candidate; we never try another oracle to find agreement."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(REPO / "pipeline"))
from pool_contract import read_json, write_json
from pool_sandbox import kind
from pool_sources import submissions
import rated_pool

RESERVED_OLDEST = 25
AUTHOR = "rated-800-worker"


def stage(*argv):
    proc = subprocess.run([sys.executable, *argv], cwd=REPO, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"{argv[0]} {argv[1] if len(argv) > 1 else ''} failed: {(proc.stderr or proc.stdout)[-600:]}")
    return proc.stdout


def pick_oracle(pid, workspace, cache):
    base = Path(workspace) / "800"
    row = read_json(base / "state" / pid / "source-row.json")
    source_ids = [i["sourceId"] for i in read_json(base / "inventory.json")["items"] if not rated_pool.inventory_blockers(i)]
    available, _ = submissions(row["id"], cache, True, base / "submissions", source_ids)
    accepted, seen = [], set()
    for s in sorted(available, key=lambda s: int(s["submission_id"])):
        h = hashlib.sha256((s.get("source") or "").encode()).hexdigest()
        if s.get("source") and s.get("testset") == "TESTS" and s.get("verdict") == "OK" and kind(s.get("programmingLanguage", "")) and h not in seen:
            seen.add(h)
            accepted.append((s, h))
    pool = accepted[RESERVED_OLDEST:]
    if not pool:
        raise ValueError(f"only {len(accepted)} distinct accepted sources; none left beyond the validator range")
    cpp = [x for x in pool if kind(x[0]["programmingLanguage"]) == "cpp"]
    s, h = (cpp or pool)[-1]
    return s, h, len(accepted)


def qualify(pid, workspace, cache, seed):
    base = Path(workspace) / "800"
    out = base / "gen-qualification" / pid
    out.mkdir(parents=True, exist_ok=True)
    log = {"id": pid}
    stage("pipeline/rated_pool.py", "prepare", "--rating", "800", "--id", pid, "--workspace", workspace, "--cache", cache)
    stage(str(HERE / "build_generator.py"), "--id", pid, "--output", str(out / "generator.py"))
    s, h, n_accepted = pick_oracle(pid, workspace, cache)
    ext = "cpp" if kind(s["programmingLanguage"]) == "cpp" else "py"
    (out / f"oracle.{ext}").write_text(s["source"])
    url = f"https://codeforces.com/contest/{s['contestId']}/submission/{s['submission_id']}"
    log["oracle"] = {"submissionId": s["submission_id"], "sourceHash": h, "language": s["programmingLanguage"], "url": url,
                     "source": s["provenance"], "distinctAcceptedAvailable": n_accepted, "reservedOldest": RESERVED_OLDEST,
                     "attribution": "Public Codeforces submission (open-r1/codeforces-submissions); not a different-agent audit."}
    write_json(out / "oracle-source.json", log["oracle"])
    common = ["--rating", "800", "--id", pid, "--workspace", workspace, "--cache", cache]
    log["generate"] = json.loads(stage("pipeline/rated_pool.py", "generate", *common,
                                       "--generator-source", str(out / "generator.py"), "--generator-language", "Python 3",
                                       "--generator-author", AUTHOR, "--seed", str(seed),
                                       "--oracle-source", str(out / f"oracle.{ext}"), "--oracle-language", s["programmingLanguage"],
                                       "--oracle-author", f"codeforces-submission:{s['submission_id']}", "--oracle-review-url", url))
    log["coverage"] = json.loads(stage(str(HERE / "gen_coverage.py"), "--id", pid, "--workspace", workspace))
    log["validate"] = json.loads(stage("pipeline/rated_pool.py", "validate", *common, "--coverage", str(ROOT / "coverage" / f"{pid}.json"),
                                       "--all-submissions", "--validator", AUTHOR))
    evidence = read_json(base / "evidence" / f"{pid}.json")
    log["oracleCollidesWithCounted"] = any(r["sourceHash"] == h for r in evidence["submissions"])
    write_json(out / "qualify-log.json", log)
    return log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--cache", default=str(Path.home() / ".cache" / "cf-race-pool"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    try:
        log = qualify(args.id, args.workspace, args.cache, args.seed)
    except (ValueError, RuntimeError) as exc:
        print(json.dumps({"id": args.id, "status": "blocked", "reason": str(exc)}))
        return 2
    v = log["validate"]
    print(json.dumps({"id": args.id, "status": v.get("status"), "oracle": log["oracle"]["submissionId"],
                      "collision": log["oracleCollidesWithCounted"], "packageHash": log["generate"]["packageHash"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
