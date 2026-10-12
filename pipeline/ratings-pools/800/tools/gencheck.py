"""Check a generated-basis recipe against every upstream sample/official/open-r1 pair and its own generator output."""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))
from checker import check


def main(pid, state_root, gen_root):
    spec = importlib.util.spec_from_file_location("recipe", HERE.parent / "genrecipes" / f"{pid}.py")
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    row = json.loads((Path(state_root) / pid / "source-row.json").read_text())
    failures, counts = [], {}
    for kind in ("examples", "official_tests", "generated_tests"):
        group = row.get(kind)
        if not isinstance(group, list):
            continue
        for i, t in enumerate(group):
            inp = t["input"].replace("\r\n", "\n")
            counts[kind] = counts.get(kind, 0) + 1
            try:
                recipe.validate(inp)
            except AssertionError as e:
                failures.append({"kind": kind, "index": i, "stage": "validate", "error": str(e), "input": inp[:80]})
                continue
            if not check(t["output"], recipe.solve(inp)):
                failures.append({"kind": kind, "index": i, "stage": "solve", "input": inp[:80]})
    out = json.loads((Path(gen_root) / pid / "out.json").read_text())
    print(json.dumps({"id": pid, "counts": counts, "generated": len(out), "distinct": len({p["input"] for p in out}),
                      "nFailures": len(failures), "failures": failures[:5]}))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
