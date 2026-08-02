"""Validate generated tests against real Codeforces submissions.

For a problem, fetches ~5 accepted and ~5 rejected (WA/TLE) public
submissions (metadata via the official API, source code via the proxy),
runs them locally against problems/<id>/tests/, and checks that:
  - every AC submission passes all tests
  - every WA/TLE submission fails at least one test

Sources are cached in pipeline/cache/<id>/ so reruns don't re-scrape.
Results are appended as JSON lines to pipeline/cache/validation.jsonl.

Usage: python3 pipeline/validate.py 1927A [...]
"""
import glob
import html as html_mod
import json
import os
import re
import subprocess
import sys
import tempfile
import time

from bs4 import BeautifulSoup

from checker import check
from common import PIPELINE_DIR, PROBLEMS_DIR, api, fetch_proxy, load_meta, split_problem_id

CACHE = os.path.join(PIPELINE_DIR, "cache")
N_AC = 5
N_REJ = 5


def lang_kind(verdict_lang: str):
    """Map a CF language name to a local runner kind, or None to skip."""
    if verdict_lang.startswith("GNU C++"):
        return "cpp"
    if "PyPy" in verdict_lang:
        return None  # timing characteristics differ too much from CPython
    if verdict_lang.startswith("Python 3"):
        return "py"
    return None


def pick_submissions(problem_id: str):
    contest_id, index = split_problem_id(problem_id)
    subs = api("contest.status", contestId=contest_id, **{"from": 1, "count": 25000})
    ac, rej = [], []
    for s in subs:
        if s["problem"]["index"] != index:
            continue
        if s.get("testset") not in ("TESTS",):
            continue
        kind = lang_kind(s.get("programmingLanguage", ""))
        if kind is None:
            continue
        v = s.get("verdict")
        entry = {
            "id": s["id"],
            "contestId": contest_id,
            "verdict": v,
            "lang": s["programmingLanguage"],
            "kind": kind,
        }
        if v == "OK" and len(ac) < N_AC:
            ac.append(entry)
        elif v in ("WRONG_ANSWER", "TIME_LIMIT_EXCEEDED") and len(rej) < N_REJ:
            # for TLE prefer to keep timing meaningful: skip py TLE (CPython
            # local perf is comparable, keep them) — keep all
            rej.append(entry)
        if len(ac) >= N_AC and len(rej) >= N_REJ:
            break
    return ac, rej


def fetch_source(contest_id: int, submission_id: int) -> str:
    cache_dir = os.path.join(CACHE, "sources")
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"{contest_id}_{submission_id}.txt")
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    page = fetch_proxy(f"/contest/{contest_id}/submission/{submission_id}")
    soup = BeautifulSoup(page, "html.parser")
    pre = soup.find("pre", id="program-source-text")
    if pre is None:
        raise RuntimeError(f"no source found for submission {submission_id}")
    src = html_mod.unescape(pre.get_text())
    with open(path, "w") as f:
        f.write(src)
    time.sleep(1.0)  # be gentle on the proxy
    return src


def build(kind: str, src: str, workdir: str):
    if kind == "py":
        path = os.path.join(workdir, "sol.py")
        with open(path, "w") as f:
            f.write(src)
        return ["python3", path], True
    path = os.path.join(workdir, "sol.cpp")
    binary = os.path.join(workdir, "sol")
    with open(path, "w") as f:
        f.write(src)
    r = subprocess.run(["g++", "-O2", "-std=c++20", "-o", binary, path],
                       capture_output=True, text=True)
    return ([binary], True) if r.returncode == 0 else (None, False)


def run_against_tests(cmd, problem_id: str, tl_ms: int, float_eps=None):
    """Returns (verdict, failed_test) — verdict in AC/WA/TLE/RE."""
    tests = sorted(glob.glob(os.path.join(PROBLEMS_DIR, problem_id, "tests", "*.in")))
    # python gets the customary multiplier CF uses for interpreted langs
    limit_s = tl_ms / 1000.0 * (3 if cmd[0] == "python3" else 1) + 1.0
    for tin in tests:
        tout = tin[:-3] + ".out"
        with open(tin) as f:
            data = f.read()
        try:
            r = subprocess.run(cmd, input=data, capture_output=True, text=True,
                               timeout=limit_s)
        except subprocess.TimeoutExpired:
            return "TLE", os.path.basename(tin)
        if r.returncode != 0:
            return "RE", os.path.basename(tin)
        with open(tout) as f:
            expected = f.read()
        if not check(expected, r.stdout, float_eps):
            return "WA", os.path.basename(tin)
    return "AC", None


def validate(problem_id: str) -> dict:
    meta = load_meta(problem_id)
    ac, rej = pick_submissions(problem_id)
    results = {"id": problem_id, "name": meta["name"], "ac": [], "rej": [], "ok": True}
    for group, entries in (("ac", ac), ("rej", rej)):
        for e in entries:
            src = fetch_source(e["contestId"], e["id"])
            with tempfile.TemporaryDirectory() as wd:
                cmd, built = build(e["kind"], src, wd)
                if not built:
                    verdict, failed = "CE", None
                else:
                    verdict, failed = run_against_tests(
                        cmd, problem_id, meta["timeLimitMs"], meta.get("floatEps"))
            expected_ok = verdict == "AC" if group == "ac" else verdict != "AC"
            if not expected_ok:
                results["ok"] = False
            results[group].append({
                "submission": e["id"], "lang": e["lang"], "cfVerdict": e["verdict"],
                "localVerdict": verdict, "failedTest": failed, "asExpected": expected_ok,
            })
            print(f"  {problem_id} sub {e['id']} ({e['lang']}) CF={e['verdict']} "
                  f"local={verdict}{' test '+failed if failed else ''} "
                  f"{'OK' if expected_ok else 'MISMATCH'}")
    os.makedirs(CACHE, exist_ok=True)
    with open(os.path.join(CACHE, "validation.jsonl"), "a") as f:
        f.write(json.dumps(results) + "\n")
    print(f"{problem_id}: {'PASS' if results['ok'] else 'FAIL'}")
    return results


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        validate(pid)
