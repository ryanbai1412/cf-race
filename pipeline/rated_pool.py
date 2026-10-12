"""Deterministic resumable per-rating inventory -> evidence -> publication dry-run."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tarfile

from common import api
from import_hf import build_statement
from pool_contract import (RATINGS, VERSION, digest, manifest, pairs, publication_gate,
                           read_json, row_gate, verify_evidence, write_json)
from pool_sources import (PINS, download, generated_tests, parquet_rows, provenance,
                          sha_file, submissions, tree)
from pool_sandbox import IMAGE, kind, run

METADATA_COLUMNS = ["id", "aliases", "contest_id", "index", "rating", "title", "tags",
                    "generated_checker", "generated_tests", "official_tests_complete",
                    "testset_size", "input_mode", "interaction_format"]


def normalized_id(value):
    if not re.fullmatch(r"[0-9]+/[A-Z][0-9]?", value):
        raise ValueError(f"invalid source problem ID: {value}")
    return value.replace("/", "")


def inventory(args):
    base = Path(args.workspace) / str(args.rating)
    api_path = base / "api-problems.json"
    if not api_path.exists() or args.refresh_api:
        write_json(api_path, api("problemset.problems")["problems"])
    problems = read_json(api_path)
    lookup = {f"{p.get('contestId')}/{p['index']}": p for p in problems
              if p.get("contestId") and p.get("type") == "PROGRAMMING"}
    items, seen, source_files = [], set(), []
    counts = Counter()
    for prefix in ("data",):
        for entry in tree("open-r1/codeforces", prefix):
            if not entry["path"].endswith(".parquet"):
                continue
            if args.shards and entry["path"] not in args.shards:
                continue
            source = provenance("open-r1/codeforces", entry)
            source_files.append(source)
            for row in parquet_rows(download("open-r1/codeforces", entry, args.cache), METADATA_COLUMNS):
                p = lookup.get(row["id"])
                if not p or p.get("rating") != args.rating:
                    continue
                aliases = {row["id"], *(row.get("aliases") or [])}
                if aliases & seen:
                    counts["duplicate-alias"] += 1
                    continue
                seen.update(aliases)
                reasons = []
                if row.get("generated_checker"):
                    reasons.append("unaudited-special-checker")
                if row.get("interaction_format") or row.get("input_mode") != "stdio":
                    reasons.append("unsupported-io")
                if not row.get("official_tests_complete") and not row.get("generated_tests"):
                    reasons.append("incomplete-tests-no-generated-suite")
                item = {"id": normalized_id(row["id"]), "sourceId": row["id"], "aliases": sorted(aliases),
                        "rating": p["rating"], "datasetRating": row["rating"], "name": p["name"],
                        "tags": sorted(p.get("tags", [])), "source": source,
                        "officialComplete": row["official_tests_complete"],
                        "officialCount": row["testset_size"], "generatedCount": row["generated_tests"],
                        "exclusions": reasons}
                items.append(item)
                counts.update(reasons)
    items.sort(key=lambda r: (bool(r["exclusions"]), not r["officialComplete"],
                              int(re.match(r"[0-9]+", r["id"])[0]), r["id"]))
    value = {"schemaVersion": VERSION, "rating": args.rating, "target": args.target, "pins": PINS,
             "apiSnapshotHash": sha_file(api_path), "sources": source_files, "items": items,
             "metadataEligible": sum(not i["exclusions"] for i in items),
             "exclusionCounts": dict(counts), "scope": "partial-shards" if args.shards else "all-default-shards",
             "validatedCount": 0}
    write_json(base / "inventory.json", value)
    return {"inventory": str(base / "inventory.json"), "total": len(items),
            "metadataEligible": value["metadataEligible"], "validatedCount": 0, "exclusions": dict(counts)}


def locations(args):
    base = Path(args.workspace) / str(args.rating)
    if not args.id or not re.fullmatch(r"[0-9]+[A-Z][0-9]?", args.id):
        raise ValueError("stage needs --id <contestId+index>")
    return base, base / "packages" / args.id, base / "state" / args.id


def prepare(args):
    base, package, state = locations(args)
    inv = read_json(base / "inventory.json")
    if inv["rating"] != args.rating or inv["pins"] != PINS:
        raise ValueError("inventory rating/pin mismatch")
    if sha_file(base / "api-problems.json") != inv["apiSnapshotHash"]:
        raise ValueError("changed API snapshot")
    item = next(i for i in inv["items"] if i["id"] == args.id)
    if item["exclusions"]:
        raise ValueError(", ".join(item["exclusions"]))
    entry = {"path": item["source"]["path"], "size": item["source"]["bytes"],
             "lfs": {"oid": item["source"]["sha256"]}}
    row = next(r for r in parquet_rows(download("open-r1/codeforces", entry, args.cache))
               if r["id"] == item["sourceId"])
    row_gate(row)
    row["rating"] = item["rating"]
    row["tags"] = item["tags"]
    write_json(state / "source-row.json", row)
    temp = base / "packages" / (args.id + ".partial")
    if temp.exists():
        shutil.rmtree(temp)
    (temp / "samples").mkdir(parents=True)
    (temp / "statement.html").write_text(build_statement(row), encoding="utf-8")
    for i, pair in enumerate(row["examples"], 1):
        for ext, key in (("in", "input"), ("out", "output")):
            (temp / "samples" / f"{i:04d}.{ext}").write_text(pair[key], encoding="utf-8")
    meta = {"id": args.id, "name": item["name"], "rating": item["rating"], "tags": item["tags"],
            "timeLimitMs": int(row["time_limit"] * 1000), "memoryLimitMb": int(row["memory_limit"]),
            "multiTest": bool(re.search(r"number of test cases", row["input_format"], re.I)),
            "specialJudge": False, "floatEps": None, "raceTimerSec": 180, "touristTimeMs": None,
            "poolPipeline": VERSION, "source": "open-r1/codeforces"}
    write_json(temp / "meta.json", meta)
    attribution = {"pins": PINS, "apiRating": item["rating"], "apiSnapshotHash": inv["apiSnapshotHash"],
                   "sourceId": row["id"], "aliases": item["aliases"], "statement": item["source"],
                   "statementRowHash": digest(row), "codeforcesUrl": f"https://codeforces.com/problemset/problem/{row['id']}",
                   "attribution": "Codeforces contest authors; open-r1/CodeForces (Penedo et al., 2025).",
                   "licenseNotes": "Dataset cards declare CC-BY-4.0 metadata and ODC-By prose; preserve both upstream cards and submission attribution."}
    write_json(temp / "provenance.json", attribution)
    if package.exists():
        shutil.rmtree(package)
    temp.rename(package)
    write_json(state / "prepare.json", {"status": "prepared", "sourceRowHash": digest(row), "inventoryHash": digest(inv)})
    return {"id": args.id, "status": "prepared", "officialCount": len(row["official_tests"])}


def generate(args):
    base, package, state = locations(args)
    prepared = read_json(state / "prepare.json")
    if prepared["inventoryHash"] != digest(read_json(base / "inventory.json")):
        raise ValueError("inventory changed since prepare")
    row = read_json(state / "source-row.json")
    if digest(row) != prepared["sourceRowHash"]:
        raise ValueError("changed prepared source")
    row_gate(row)
    generated, source = generated_tests(row, args.cache)
    if generated:
        pairs(generated)
    extra = pairs(read_json(args.extra_tests)) if args.extra_tests else []
    all_tests = [("official", p) for p in row["official_tests"]] + [("open-r1-generated", p) for p in generated] + [("worker-generated", p) for p in extra]
    out = package / "tests.partial"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    records = []
    for i, (origin, pair) in enumerate(all_tests, 1):
        name = f"{i:04d}"
        for ext, key in (("in", "input"), ("out", "output")):
            (out / f"{name}.{ext}").write_text(pair[key], encoding="utf-8")
        records.append({"name": name, "origin": origin, "inputHash": sha_file(out / f"{name}.in"),
                        "outputHash": sha_file(out / f"{name}.out")})
    if (package / "tests").exists():
        shutil.rmtree(package / "tests")
    out.rename(package / "tests")
    attribution = read_json(package / "provenance.json")
    attribution["tests"] = {"officialIncluded": len(row["official_tests"]),
                            "officialComplete": row["official_tests_complete"],
                            "officialAdvertised": row["testset_size"], "generatedIncluded": len(generated),
                            "generatedAdvertised": row["generated_tests"], "generatedSource": source,
                            "extraTestsHash": sha_file(args.extra_tests) if args.extra_tests else None, "pairs": records}
    write_json(package / "provenance.json", attribution)
    files = manifest(package)
    write_json(state / "generate.json", {"status": "generated", "sourceRowHash": digest(row),
                                        "packageHash": digest(files), "files": files, "testCount": len(records)})
    return {"id": args.id, "status": "generated", "testCount": len(records),
            "official": len(row["official_tests"]), "openR1Generated": len(generated), "extra": len(extra), "packageHash": digest(files)}


def validate(args):
    base, package, state = locations(args)
    generated = read_json(state / "generate.json")
    if read_json(state / "prepare.json")["inventoryHash"] != digest(read_json(base / "inventory.json")):
        raise ValueError("inventory changed since prepare")
    files = manifest(package)
    if generated["files"] != files or generated["packageHash"] != digest(files):
        raise ValueError("changed package since generate")
    coverage = read_json(args.coverage) if args.coverage else {}
    if coverage.get("packageHash") != digest(files):
        raise ValueError("coverage review must bind current packageHash")
    names = {p.stem for p in (package / "tests").glob("*.in")}
    for key in ("boundary", "adversarial", "maxSize"):
        entries = coverage.get(key)
        if not isinstance(entries, list) or not entries or any(e.get("test") not in names or not e.get("reason") for e in entries):
            raise ValueError(f"coverage needs named tests and reasons: {key}")
    if any(not coverage.get(k) for k in ("inputConstraints", "checkerSemantics", "statementComplete")):
        raise ValueError("coverage missing constraints/checker/statement review")
    row = read_json(state / "source-row.json")
    if digest(row) != generated["sourceRowHash"]:
        raise ValueError("changed source since generate")
    available, source_files = submissions(row["id"], args.cache, args.all_submissions)
    tests = [{"name": p.stem, "input": p.read_bytes(), "output": p.with_suffix(".out").read_bytes()}
             for p in sorted((package / "tests").glob("*.in"))]
    meta = read_json(package / "meta.json")
    accepted, incorrect, skipped = [], [], []
    source_hashes, ids = set(), set()
    validator = args.validator
    for s in sorted(available, key=lambda s: int(s["submission_id"])):
        source_hash = hashlib.sha256((s.get("source") or "").encode()).hexdigest()
        if (not s.get("source") or s.get("testset") != "TESTS" or kind(s.get("programmingLanguage", "")) is None or
                s.get("verdict") not in ("OK", "WRONG_ANSWER", "TIME_LIMIT_EXCEEDED") or
                source_hash in source_hashes or s["submission_id"] in ids):
            skipped.append({"id": s["submission_id"], "reason": "unsupported/duplicate/nonfinal-source"})
            continue
        group = accepted if s["verdict"] == "OK" else incorrect
        if len(group) >= 5:
            continue
        source_hashes.add(source_hash)
        ids.add(s["submission_id"])
        source_record = {"submissionId": s["submission_id"], "sourceHash": source_hash, "expected": s["verdict"],
                         "language": s["programmingLanguage"], "source": s["provenance"],
                         "url": f"https://codeforces.com/contest/{s['contestId']}/submission/{s['submission_id']}"}
        write_json(state / "sources" / f"{s['submission_id']}.json", {**source_record, "code": s["source"]})
        cache_path = state / "runs" / f"{s['submission_id']}.json"
        run_key = digest({"packageHash": digest(files), "sourceHash": source_hash, "image": IMAGE,
                          "harnessHash": sha_file(Path(__file__).with_name("pool_harness.py")),
                          "runnerHash": sha_file(Path(__file__).with_name("pool_sandbox.py"))})
        cached = read_json(cache_path) if cache_path.exists() else None
        try:
            if cached and cached.get("runKey") == run_key:
                result = cached["result"]
            else:
                result = run(s["source"], s["programmingLanguage"], tests, meta["timeLimitMs"] / 1000, meta["memoryLimitMb"])
                write_json(cache_path, {"runKey": run_key, "result": result})
            if result["compiled"] and ((s["verdict"] == "OK" and result["verdict"] == "AC") or
                                       (s["verdict"] != "OK" and result["verdict"] in ("WA", "TLE"))):
                group.append({**source_record, **result})
            else:
                skipped.append({**source_record, "reason": "not independently confirmed", "result": result})
        except (RuntimeError, ValueError) as exc:
            skipped.append({**source_record, "reason": str(exc)})
            if "infrastructure" in str(exc) or "unavailable" in str(exc):
                break
    evidence = {"schemaVersion": VERSION, "id": args.id, "rating": args.rating,
                "validator": validator, "files": files, "packageHash": digest(files), "testCount": len(tests),
                "coverage": coverage, "submissions": accepted + incorrect, "excludedSubmissions": skipped,
                "sourceFiles": source_files, "stages": ["prepare", "generate", "validate"],
                "sandbox": {"image": IMAGE, "network": "none", "bounded": True,
                            "harnessHash": sha_file(Path(__file__).with_name("pool_harness.py")),
                            "runnerHash": sha_file(Path(__file__).with_name("pool_sandbox.py"))},
                "status": "execution-passed" if len(accepted) == 5 and len(incorrect) == 5 else "incomplete"}
    if manifest(package) != files:
        raise ValueError("package changed during validation")
    write_json(base / "evidence" / f"{args.id}.json", evidence)
    return {"id": args.id, "status": evidence["status"], "accepted": len(accepted), "incorrect": len(incorrect),
            "excluded": len(skipped), "evidenceHash": digest(evidence), "validated": False,
            "next": "independent audit signoff required"}


def report(args):
    base = Path(args.workspace) / str(args.rating)
    inv = read_json(base / "inventory.json")
    result = {"rating": args.rating, "target": inv["target"], "inventoryCount": len(inv["items"]),
              "validatedCount": 0, "executionPassed": 0, "exclusions": inv["exclusionCounts"], "packages": []}
    for item in inv["items"]:
        if not (base / "packages" / item["id"]).exists():
            continue
        entry = {"id": item["id"], "validated": False}
        try:
            evidence = read_json(base / "evidence" / f"{item['id']}.json")
            result["executionPassed"] += evidence.get("status") == "execution-passed"
            verify_evidence(base / "packages" / item["id"], evidence, read_json(base / "audits" / f"{item['id']}.json"))
            entry["validated"] = True
            result["validatedCount"] += 1
        except (OSError, ValueError, KeyError) as exc:
            entry["reason"] = str(exc)
        result["packages"].append(entry)
    write_json(base / "report.json", result)
    return result


def publish_dry_run(args):
    base, package, state = locations(args)
    gate = publication_gate(package, Path(args.workspace), require_approval=False)
    if gate["legacy"]:
        raise ValueError("legacy maintenance exemption is never new validation")
    return {"id": args.id, "remoteWrites": False, "objects": [f"{args.id}/{p}" for p in gate["files"]], **gate}


def archive(args):
    base, package, state = locations(args)
    output = Path(args.output)
    files = manifest(package)
    with tarfile.open(output, "w:gz") as tar:
        tar.add(package, arcname=f"{args.rating}/packages/{args.id}")
        tar.add(state, arcname=f"{args.rating}/state/{args.id}")
        for category in ("evidence", "audits"):
            path = base / category / f"{args.id}.json"
            if path.exists():
                tar.add(path, arcname=f"{args.rating}/{category}/{args.id}.json")
    value = {"archive": output.name, "sha256": sha_file(output), "bytes": output.stat().st_size,
             "packageHash": digest(files), "files": files, "pins": PINS}
    write_json(str(output) + ".provenance.json", value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("inventory", "prepare", "generate", "validate", "report", "publish-dry-run", "archive"))
    parser.add_argument("--rating", type=int, choices=RATINGS, default=800)
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--workspace", default="pipeline/ratings")
    parser.add_argument("--cache", default=str(Path.home() / ".cache" / "cf-race-pool"))
    parser.add_argument("--id")
    parser.add_argument("--shards", nargs="+")
    parser.add_argument("--refresh-api", action="store_true")
    parser.add_argument("--extra-tests")
    parser.add_argument("--coverage")
    parser.add_argument("--all-submissions", action="store_true")
    parser.add_argument("--validator", default="pipeline-worker")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = {"inventory": inventory, "prepare": prepare, "generate": generate, "validate": validate,
                  "report": report, "publish-dry-run": publish_dry_run, "archive": archive}[args.stage](args)
        print(json.dumps(result, indent=2, sort_keys=True))
        if args.stage == "validate" and result["status"] != "execution-passed":
            return 2
    except (OSError, ValueError, KeyError, RuntimeError, StopIteration) as exc:
        print(json.dumps({"stage": args.stage, "rating": args.rating, "id": args.id, "status": "blocked", "reason": str(exc)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
