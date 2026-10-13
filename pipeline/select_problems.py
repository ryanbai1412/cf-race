"""Select random rated-800 problems from contests in the last ~3 years.

Prints candidate problem ids (contestId+index), newest-contest info included.
Prefers problems NOT tagged 'constructive algorithms' (proxy for
special-judge / multiple-answers problems).

Usage: python3 pipeline/select_problems.py [count] [seed]
"""
import argparse
import random
import sys
import time

from common import api

def candidates(years: float = 3.0, rating: int = 800, now=None):
    contests = api("contest.list", gym="false")
    cutoff = (time.time() if now is None else now) - years * 365 * 86400
    recent = {c["id"]: c["name"] for c in contests
              if c.get("phase") == "FINISHED"
              and c.get("startTimeSeconds", 0) >= cutoff}
    problems = api("problemset.problems")["problems"]
    out = []
    for p in problems:
        if p.get("rating") != rating:
            continue
        if p.get("contestId") not in recent:
            continue
        if p.get("type") != "PROGRAMMING":
            continue
        tags = set(p.get("tags", []))
        out.append({
            "id": f"{p['contestId']}{p['index']}",
            "name": p["name"],
            "rating": p["rating"],
            "tags": sorted(tags),
            "constructive": "constructive algorithms" in tags,
            "contest": recent[p["contestId"]],
        })
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("count", nargs="?", type=int, default=20)
    parser.add_argument("seed", nargs="?", type=int, default=20260802)
    parser.add_argument("--rating", type=int, default=800)
    parser.add_argument("--years", type=float, default=3)
    args = parser.parse_args()
    count, seed = args.count, args.seed
    cands = candidates(years=args.years, rating=args.rating)
    non_constructive = [c for c in cands if not c["constructive"]]
    rng = random.Random(seed)
    picks = rng.sample(non_constructive, min(count, len(non_constructive)))
    print(f"# {len(cands)} rated-{args.rating} problems in last {args.years:g}y; "
          f"{len(non_constructive)} non-constructive; showing {len(picks)}")
    for c in picks:
        print(f"{c['id']}\t{c['name']}\t[{', '.join(c['tags'])}]\t({c['contest']})")
