"""Authored-recipe checks for rating-800 packages.

Each recipes/<ID>.py defines:
  CONSTRAINTS, UNIQUENESS, STATEMENT: review notes (strings)
  validate(inp): raise AssertionError unless inp satisfies every statement constraint
  solve(inp) -> str: authored reference (independent of downloaded programs)
  extra() -> [(category, reason, input)]: deterministic boundary/adversarial/maxSize inputs

check: validates every sample/official/open-r1 generated input and compares the authored
reference with each upstream expected output under the judge token checker; writes
extra-<ID>.json (outputs from the reference) and recipe-report-<ID>.json.
coverage: after `rated_pool.py generate --extra-tests`, binds the current packageHash.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE.parent.parent))
from checker import check  # noqa: E402
from pool_contract import digest, manifest, read_json, write_json  # noqa: E402
from pool_sources import generated_tests, sha_file  # noqa: E402

CATEGORIES = ("boundary", "adversarial", "maxSize")


def norm(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def load(pid):
    if str(HERE / "tools") not in sys.path:
        sys.path.insert(0, str(HERE / "tools"))
    path = HERE / "recipes" / f"{pid}.py"
    spec = importlib.util.spec_from_file_location(f"recipe_{pid}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, sha_file(path)


def check_recipe(args):
    pid = args.id
    recipe, recipe_hash = load(pid)
    row = read_json(Path(args.workspace) / "800" / "state" / pid / "source-row.json")
    generated, _ = generated_tests(row, args.cache)
    suites = [("sample", row["examples"]), ("official", row["official_tests"]), ("open-r1-generated", generated)]
    records, failures = [], []
    for origin, tests in suites:
        for i, pair in enumerate(tests):
            inp, expected = norm(pair["input"]), pair["output"]
            entry = {"origin": origin, "index": i, "inputHash": hashlib.sha256(pair["input"].encode()).hexdigest(),
                     "outputHash": hashlib.sha256(pair["output"].encode()).hexdigest()}
            try:
                recipe.validate(inp)
                entry["constraints"] = "ok"
            except Exception as exc:  # noqa: BLE001
                entry["constraints"] = f"violation: {exc!r}"
                failures.append(entry)
            try:
                got = recipe.solve(inp)
                entry["oracle"] = "match" if check(expected, got) else "mismatch"
            except Exception as exc:  # noqa: BLE001
                entry["oracle"] = f"error: {exc!r}"
            if entry["oracle"] != "match" and entry not in failures:
                failures.append(entry)
            records.append(entry)
    existing = {}
    for origin, offset, tests in (("official", 0, row["official_tests"]),
                                  ("open-r1-generated", len(row["official_tests"]), generated)):
        for i, pair in enumerate(tests):
            existing.setdefault(norm(pair["input"]), f"{offset + i + 1:04d}")
    base = len(row["official_tests"]) + len(generated)
    extras, extra_records, added = [], [], {}
    for category, reason, inp in recipe.extra():
        if category not in CATEGORIES:
            raise ValueError(f"bad category {category}")
        recipe.validate(inp)
        out = recipe.solve(inp)
        if not out.strip():
            raise ValueError("empty reference output")
        record = {"category": category, "reason": reason, "inputHash": hashlib.sha256(inp.encode()).hexdigest(),
                  "outputHash": hashlib.sha256(out.encode()).hexdigest(), "inputBytes": len(inp.encode())}
        if inp in existing:
            record.update(test=existing[inp], origin="upstream-duplicate")
        else:
            if inp not in added:
                extras.append({"input": inp, "output": out})
                added[inp] = f"{base + len(extras):04d}"
            record.update(test=added[inp], origin="worker-generated")
        extra_records.append(record)
    report = {"id": pid, "recipeHash": recipe_hash, "checkerHash": sha_file(HERE.parent.parent / "checker.py"),
              "sourceRowHash": digest(row), "counts": {o: len(t) for o, t in suites},
              "upstreamChecks": records, "failures": failures, "extras": extra_records,
              "status": "pass" if not failures and all(any(r["category"] == c for r in extra_records) for c in CATEGORIES) else "fail"}
    extra_path = HERE / "extra-tests" / f"{pid}.json"
    if extras:
        write_json(extra_path, extras)
    else:
        extra_path.unlink(missing_ok=True)
    write_json(HERE / "recipe-reports" / f"{pid}.json", report)
    return {"id": pid, "status": report["status"], "failures": failures[:5], "nFailures": len(failures),
            "extras": len(extras), "counts": report["counts"]}


def coverage(args):
    pid = args.id
    recipe, recipe_hash = load(pid)
    report = read_json(HERE / "recipe-reports" / f"{pid}.json")
    if report["status"] != "pass" or report["recipeHash"] != recipe_hash:
        raise ValueError("recipe report missing/stale/failing")
    package = Path(args.workspace) / "800" / "packages" / pid
    files = manifest(package)
    prov = read_json(package / "provenance.json")["tests"]
    extra_path = HERE / "extra-tests" / f"{pid}.json"
    if prov["extraTestsHash"] != (sha_file(extra_path) if extra_path.exists() else None):
        raise ValueError("package was not generated from current extra tests")
    for rec in report["extras"]:
        name = rec["test"]
        if rec["origin"] == "worker-generated" and (files[f"tests/{name}.in"]["sha256"] != rec["inputHash"] or
                                                    files[f"tests/{name}.out"]["sha256"] != rec["outputHash"]):
            raise ValueError(f"extra test {name} bytes differ from recipe report")
        if f"tests/{name}.in" not in files:
            raise ValueError(f"missing test {name}")
    counts = report["counts"]
    value = {"packageHash": digest(files), "recipeHash": recipe_hash, "recipeReportHash": sha_file(HERE / "recipe-reports" / f"{pid}.json")}
    for category in CATEGORIES:
        value[category] = [{"test": r["test"], "reason": r["reason"] + ("" if r["origin"] == "worker-generated" else " (input already in upstream suite)")}
                           for r in report["extras"] if r["category"] == category]
        if not value[category]:
            raise ValueError(f"no {category} test")
    value["inputConstraints"] = (f"Authored validate() asserts: {recipe.CONSTRAINTS} It accepted all {counts['sample']} samples, "
                                 f"{counts['official']} official and {counts['open-r1-generated']} open-r1 generated inputs, and all "
                                 f"{sum(r['origin'] == 'worker-generated' for r in report['extras'])} distinct worker-generated inputs "
                                 f"(categorized inputs already present upstream reference the upstream test).")
    value["checkerSemantics"] = (f"{recipe.UNIQUENESS} The authored reference reproduced every upstream expected output "
                                 f"under the token/YES-NO checker; worker outputs come from that reference and are re-checked against five accepted programs.")
    value["statementComplete"] = recipe.STATEMENT
    value["testBasis"] = {"officialIncluded": prov["officialIncluded"], "officialAdvertised": prov["officialAdvertised"],
                          "officialComplete": prov["officialComplete"], "openR1Generated": prov["generatedIncluded"],
                          "workerGenerated": len({r["test"] for r in report["extras"] if r["origin"] == "worker-generated"})}
    write_json(HERE / "coverage" / f"{pid}.json", value)
    return {"id": pid, "packageHash": value["packageHash"], **{c: len(value[c]) for c in CATEGORIES}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("check", "coverage"))
    parser.add_argument("--id", required=True)
    parser.add_argument("--workspace", default=str(HERE.parent))
    parser.add_argument("--cache", default=str(Path.home() / ".cache" / "cf-race-pool"))
    args = parser.parse_args()
    result = (check_recipe if args.stage == "check" else coverage)(args)
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("status", "pass") == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
