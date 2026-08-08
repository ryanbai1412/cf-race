"""Central scraper: statements + AC/WA/TLE submission sources for a list of problems.

Usage: CF_JSESSIONID=... python3 pipeline/central_scrape.py <ids.json> [--start N]

For each problem id:
  1. scrape statement + samples (skips if problems/<id>/meta.json exists)
  2. pull submission metadata via official CF API (contest.status)
  3. fetch up to 5 viewable sources per verdict (AC/WA/TLE) via browser_fetch
Writes pipeline/submissions/<id>/<VERDICT>_<subId>.<cpp|py> and meta.json.
Progress log: pipeline/central_scrape_progress.jsonl
"""
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from common import PIPELINE_DIR, PROBLEMS_DIR, api, split_problem_id
import scrape as scrape_mod
import stealth_fetch

common.fetch_proxy = lambda path, **kw: stealth_fetch.fetch(path, "div.problem-statement")
scrape_mod.fetch_proxy = common.fetch_proxy
common.API_BASE = common.PROXY_BASE + "/api"
common._session.cookies.update(common.PROXY_COOKIE)

WANT = {"OK": 5, "WRONG_ANSWER": 5, "TIME_LIMIT_EXCEEDED": 5}
VERDICT_NAME = {"OK": "AC", "WRONG_ANSWER": "WA", "TIME_LIMIT_EXCEEDED": "TLE"}
MAX_CANDIDATES = 40
PROGRESS = os.path.join(PIPELINE_DIR, "central_scrape_progress.jsonl")


def lang_ok(lang: str):
    if "C++" in lang and "GNU" in lang:
        return "cpp"
    if "Python 3" in lang and "PyPy" not in lang:
        return "py"
    return None


def scrape_statement(pid: str):
    if os.path.exists(os.path.join(PROBLEMS_DIR, pid, "meta.json")):
        return "exists"
    scrape_mod.scrape(pid)
    return "scraped"


def pull_submissions(pid: str):
    contest_id, index = split_problem_id(pid)
    outdir = os.path.join(PIPELINE_DIR, "submissions", pid)
    meta_path = os.path.join(outdir, "meta.json")
    if os.path.exists(meta_path):
        return json.load(open(meta_path))
    os.makedirs(outdir, exist_ok=True)

    rows = []
    start = 1
    while start < 20000:
        chunk = api("contest.status", contestId=contest_id, **{"from": start}, count=5000)
        rows.extend(r for r in chunk if r.get("problem", {}).get("index") == index)
        if len(chunk) < 5000:
            break
        start += 5000
        time.sleep(0.5)

    by_verdict = {v: [] for v in WANT}
    for r in rows:
        v = r.get("verdict")
        if v in by_verdict and lang_ok(r.get("programmingLanguage", "")):
            by_verdict[v].append(r)

    rng = random.Random(pid)
    saved = []
    for v, want in WANT.items():
        cands = by_verdict[v]
        rng.shuffle(cands)
        got = 0
        for r in cands[:MAX_CANDIDATES]:
            if got >= want:
                break
            sid = r["id"]
            src = stealth_fetch.fetch_text(f"/contest/{contest_id}/submission/{sid}")
            if not src or src.strip() == "N/A" or len(src.strip()) < 5:
                continue
            ext = lang_ok(r["programmingLanguage"])
            fn = f"{VERDICT_NAME[v]}_{sid}.{ext}"
            with open(os.path.join(outdir, fn), "w") as f:
                f.write(src)
            saved.append({"submissionId": sid, "verdict": VERDICT_NAME[v],
                          "language": r["programmingLanguage"], "file": fn})
            got += 1
            time.sleep(1.0)

    with open(meta_path, "w") as f:
        json.dump(saved, f, indent=1)
    return saved


def main():
    ids = json.load(open(sys.argv[1]))
    start_at = 0
    if "--start" in sys.argv:
        start_at = int(sys.argv[sys.argv.index("--start") + 1])
    for i, pid in enumerate(ids[start_at:], start_at):
        rec = {"i": i, "id": pid, "ts": time.time()}
        try:
            rec["statement"] = scrape_statement(pid)
            subs = pull_submissions(pid)
            rec["subs"] = {v: sum(1 for s in subs if s["verdict"] == v)
                           for v in ("AC", "WA", "TLE")}
            rec["ok"] = True
        except Exception as e:
            rec["ok"] = False
            rec["error"] = f"{type(e).__name__}: {e}"[:300]
        with open(PROGRESS, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
