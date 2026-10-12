"""Write the coverage record for a generated-basis rating-800 package from its genrecipe."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT.parents[1]))
from pool_contract import digest, manifest, read_json, write_json
from pool_sources import sha_file

CATEGORIES = ("boundary", "adversarial", "maxSize")


def load(pid):
    path = ROOT / "genrecipes" / f"{pid}.py"
    spec = importlib.util.spec_from_file_location(f"gen_{pid}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, sha_file(path)


def coverage(pid, workspace):
    recipe, recipe_hash = load(pid)
    package = Path(workspace) / "800" / "packages" / pid
    files = manifest(package)
    prov = read_json(package / "provenance.json")
    if prov.get("qualification", {}).get("basis") != "generated":
        raise ValueError("package is not generated-basis")
    generation = read_json(package / "qualification" / "generation.json")
    authored = [r for r in prov["tests"]["pairs"] if r["origin"] == "worker-generated"]
    by_input = {r["inputHash"]: r["name"] for r in authored}
    value = {"packageHash": digest(files), "genRecipeHash": recipe_hash,
             "generatorSourceHash": generation.get("sourceHash")}
    for category in CATEGORIES:
        value[category] = []
        for cat, reason, inp in recipe.extra():
            if cat != category:
                continue
            name = by_input.get(hashlib.sha256(inp.encode()).hexdigest())
            if name is None:
                raise ValueError(f"authored {category} case missing from package: {reason}")
            value[category].append({"test": name, "reason": reason})
        if not value[category]:
            raise ValueError(f"no {category} test")
    supplementary = {k: sum(r["origin"] == k for r in prov["tests"]["pairs"]) for k in ("official", "open-r1-generated")}
    value["inputConstraints"] = (f"Generator validate() asserts {recipe.CONSTRAINTS} before emitting each of the "
                                 f"{len(authored)} distinct authored inputs; the same validator accepted every upstream sample, "
                                 f"{supplementary['official']} supplementary official and {supplementary['open-r1-generated']} open-r1 generated inputs.")
    value["checkerSemantics"] = (f"{recipe.UNIQUENESS} Authored outputs come from the worker reference and every supplied pair "
                                 "was re-checked by the separately sourced oracle in the sandbox under the token checker.")
    value["statementComplete"] = recipe.STATEMENT
    value["testBasis"] = {"basis": "generated", "officialIncluded": prov["tests"]["officialIncluded"],
                          "officialAdvertised": prov["tests"]["officialAdvertised"], "officialComplete": prov["tests"]["officialComplete"],
                          "officialRole": prov["tests"]["officialRole"], "openR1Generated": prov["tests"]["generatedIncluded"],
                          "workerGenerated": len(authored), "generatorMode": generation.get("mode")}
    out = ROOT / "coverage" / f"{pid}.json"
    write_json(out, value)
    return {"id": pid, "packageHash": value["packageHash"], **{c: len(value[c]) for c in CATEGORIES}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()
    print(json.dumps(coverage(args.id, args.workspace), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
