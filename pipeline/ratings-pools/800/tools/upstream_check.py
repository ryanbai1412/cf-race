"""Check every upstream pair (samples, official, open-r1 generated) against a generated-basis recipe's validate().

The foundation generate stage checks oracle outputs but not statement constraints on upstream inputs, so a package can
otherwise carry malformed open-r1 generated tests. Violations are recorded in diagnostics/ID-upstream-constraints.json
and the candidate is quarantined; upstream bytes are never repaired or dropped."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))
from rated_pool import generated_tests


def check(pid, workspace, cache):
    path = HERE.parent / "genrecipes" / f"{pid}.py"
    spec = importlib.util.spec_from_file_location("recipe", path)
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    row = json.loads((Path(workspace) / "800" / "state" / pid / "source-row.json").read_text())
    official = row.get("official_tests") or []
    generated, _ = generated_tests(row, cache)
    violations, counts, number = [], {}, 0
    for origin, tests in (("sample", row["examples"]), ("official", official), ("open-r1-generated", generated)):
        counts[origin] = len(tests)
        for i, pair in enumerate(tests):
            test = None if origin == "sample" else f"{number + 1:04d}"
            number += origin != "sample"
            inp = pair["input"].replace("\r\n", "\n")
            try:
                recipe.validate(inp)
            except AssertionError as exc:
                try:
                    recipe.validate("\n".join(line.rstrip() for line in inp.split("\n")))
                    kind = "whitespace-only"
                except AssertionError:
                    kind = "constraint"
                violations.append({"origin": origin, "index": i, "test": test, "error": str(exc), "kind": kind,
                                   "inputSha256": hashlib.sha256(pair["input"].encode()).hexdigest(),
                                   "inputBytes": len(pair["input"].encode())})
    out = HERE.parent / "diagnostics" / f"{pid}-upstream-constraints.json"
    report = {"id": pid, "recipeSha256": hashlib.sha256(path.read_bytes()).hexdigest(), "constraints": recipe.CONSTRAINTS,
              "counts": counts, "violations": violations,
              "violationKinds": {k: sum(v["kind"] == k for v in violations) for k in ("constraint", "whitespace-only")},
              "decision": "Quarantined: upstream inputs violate the statement constraints. Not repaired, truncated or "
                          "dropped; not counted." if violations else None}
    if violations:
        out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    else:
        out.unlink(missing_ok=True)
    return {"id": pid, "status": "quarantined" if violations else "pass", "nViolations": len(violations),
            "first": violations[:2], "counts": counts}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, nargs="+")
    p.add_argument("--workspace", required=True)
    p.add_argument("--cache", default=str(Path.home() / ".cache" / "cf-race-pool"))
    a = p.parse_args()
    results = [check(pid, a.workspace, a.cache) for pid in a.id]
    print(json.dumps(results if len(results) > 1 else results[0]))
    sys.exit(1 if any(r["status"] != "pass" for r in results) else 0)
