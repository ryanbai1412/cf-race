"""Summarize the rating-800 workspace into one machine-readable report: per-candidate basis, status, counts, oracle
attribution, hashes, and exclusion reasons. Never upgrades status; validation is only what rated_pool.py report verifies."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None


def main(workspace, logs, out):
    base = Path(workspace) / "800"
    foundation = load(base / "report.json") or {}
    validated = {p["id"]: p for p in foundation.get("packages", [])}
    recipes = {p.stem: "official" for p in (ROOT / "recipes").glob("*.py")}
    recipes.update({p.stem: "generated" for p in (ROOT / "genrecipes").glob("*.py")})
    rows, counts = [], {}
    for pid, basis in sorted(recipes.items()):
        ev = load(base / "evidence" / f"{pid}.json")
        q = load(base / "gen-qualification" / pid / "qualify-log.json") if basis == "generated" else None
        row = {"id": pid, "recipeBasis": basis, "status": "not-run"}
        if ev:
            subs = ev.get("submissions", [])
            row.update({"status": ev.get("status"), "qualificationBasis": ev.get("qualificationBasis"),
                        "packageHash": ev.get("packageHash"), "testCount": ev.get("testCount"),
                        "acceptedContradiction": ev.get("acceptedContradiction"),
                        "accepted": sum(s.get("expected") == "OK" for s in subs),
                        "incorrect": sum(s.get("expected") != "OK" for s in subs),
                        "submissions": [{"id": s["submissionId"], "expected": s.get("expected"), "verdict": s.get("verdict"),
                                         "failedTest": s.get("failedTest"), "sourceHash": s.get("sourceHash"), "url": s.get("url")} for s in subs],
                        "excludedReasons": {}})
            for x in ev.get("excludedSubmissions", []):
                r = x.get("reason", "")[:80]
                row["excludedReasons"][r] = row["excludedReasons"].get(r, 0) + 1
        if q:
            row["oracle"] = q.get("oracle")
        log = Path(logs) / ("gen" if basis == "generated" else "run") / f"{pid}.log"
        if row["status"] == "not-run" and log.exists():
            tail = log.read_text(errors="replace")[-400:]
            last = tail.strip().splitlines()[-1] if tail.strip() else ""
            row["status"], row["blocker"] = ("blocked", last) if '"blocked"' in last else ("in-progress", last)
        row["validated"] = bool(validated.get(pid, {}).get("validated"))
        row["validationGap"] = validated.get(pid, {}).get("reason")
        counts[row["status"]] = counts.get(row["status"], 0) + 1
        rows.append(row)
    report = {"rating": 800, "target": 100, "validatedCount": sum(r["validated"] for r in rows),
              "statusCounts": counts, "recipeCount": len(recipes),
              "byBasis": {b: sum(r["recipeBasis"] == b for r in rows) for b in ("official", "generated")},
              "executionPassedByBasis": {b: sum(r["recipeBasis"] == b and r["status"] == "execution-passed" for r in rows) for b in ("official", "generated")},
              "foundationReport": {k: foundation.get(k) for k in ("validatedCount", "executionPassed", "exclusions", "validatedByBasis", "qualificationAvailability")},
              "note": "execution-passed is NOT validated: a different-agent independent audit of the current bytes is still required.",
              "packages": rows}
    Path(out).write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in ("validatedCount", "statusCounts", "recipeCount", "byBasis", "executionPassedByBasis")}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
