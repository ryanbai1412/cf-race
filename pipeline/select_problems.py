"""Select random rated-800 problems from contests in the last ~3 years.

Prints candidate problem ids (contestId+index), newest-contest info included.
Prefers problems NOT tagged 'constructive algorithms' (proxy for
special-judge / multiple-answers problems).

Usage: python3 pipeline/select_problems.py [count] [seed]
"""
import random
import sys
import time

from common import api

def candidates(years: float = 3.0):
    contests = api("contest.list", gym="false")
    cutoff = time.time() - years * 365 * 86400
    recent = {c["id"]: c["name"] for c in contests
              if c.get("phase") == "FINISHED"
              and c.get("startTimeSeconds", 0) >= cutoff}
    problems = api("problemset.problems")["problems"]
    out = []
    for p in problems:
        if p.get("rating") != 800:
            continue
        if p.get("contestId") not in recent:
            continue
        if p.get("type") != "PROGRAMMING":
            continue
        tags = set(p.get("tags", []))
        out.append({
            "id": f"{p['contestId']}{p['index']}",
            "name": p["name"],
            "tags": sorted(tags),
            "constructive": "constructive algorithms" in tags,
            "contest": recent[p["contestId"]],
        })
    return out


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20260802
    cands = candidates()
    non_constructive = [c for c in cands if not c["constructive"]]
    rng = random.Random(seed)
    picks = rng.sample(non_constructive, min(count, len(non_constructive)))
    print(f"# {len(cands)} rated-800 problems in last 3y; "
          f"{len(non_constructive)} non-constructive; showing {len(picks)}")
    for c in picks:
        print(f"{c['id']}\t{c['name']}\t[{', '.join(c['tags'])}]\t({c['contest']})")
