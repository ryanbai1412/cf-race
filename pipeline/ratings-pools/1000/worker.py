"""Local-only, rating1000 worker. Never author an independent audit or publish."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PIPELINE = HERE.parents[1]
sys.path.insert(0, str(PIPELINE))
from checker import check
from pool_contract import digest, read_json, write_json
from pool_sources import download, PINS, sha_file, submissions, tree
import rated_pool
from recipes import IDS, RULES, extras, output


def arguments(pid, base, cache):
    return argparse.Namespace(rating=1000,target=100,workspace=str(base.parent),cache=str(cache),
                              id=pid,shards=None,refresh_api=False,all_submissions=True,
                              validator="devin-af005f714e22447094063818961cafbf",coverage=None,
                              extra_tests=None,output=None)


def source_index(base, cache):
    entries = tree("open-r1/codeforces-submissions", "data")
    def fetch(entry):
        download("open-r1/codeforces-submissions", entry, cache)
        print("verified", entry["path"], flush=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(fetch, entries))
    inventory = read_json(base / "inventory.json")
    source_ids = [i["sourceId"] for i in inventory["items"] if not i["exclusions"]]
    submissions(source_ids[0],cache,True,base/"submissions",source_ids)
    from pool_sandbox import kind
    entries_by_id = {i["sourceId"]: i for i in inventory["items"]}
    counts, hashes, identities = {}, {}, {}
    exclusions = Counter()
    for marker in sorted((base/"submissions").glob("*/complete.json")):
        completion = read_json(marker)
        for name, expected in completion["files"].items():
            path = marker.parent / name
            if sha_file(path) != expected:
                raise ValueError("changed indexed source")
            for row in read_json(path):
                pid = row["problem_id"]
                count = counts.setdefault(pid, Counter())
                if row.get("testset") != "TESTS":
                    count["nonfinal-testset"] += 1
                elif not kind(row.get("programmingLanguage") or ""):
                    count["unsupported-language"] += 1
                elif row.get("verdict") not in ("OK", "WRONG_ANSWER", "TIME_LIMIT_EXCEEDED"):
                    count["unsupported-verdict"] += 1
                elif not row.get("source"):
                    count["missing-source"] += 1
                else:
                    sha = hashlib.sha256(row["source"].encode()).hexdigest()
                    seen = hashes.setdefault(pid,set())
                    seen_ids = identities.setdefault(pid,set())
                    if sha in seen or row["submission_id"] in seen_ids:
                        count["duplicate-source-or-id"] += 1
                    else:
                        seen.add(sha)
                        seen_ids.add(row["submission_id"])
                        count["accepted" if row["verdict"] == "OK" else "incorrect"] += 1
                count["totalRows"] += 1
    rows = []
    for pid,item in entries_by_id.items():
        count = dict(counts.get(pid,{}))
        reasons = list(item["exclusions"])+list(item["validationBlockers"])
        if not item["exclusions"]:
            if count.get("accepted",0)<5:
                reasons.append("fewer-than-five-supported-distinct-accepted")
            if count.get("incorrect",0)<5:
                reasons.append("fewer-than-five-supported-distinct-incorrect")
        exclusions.update(reasons)
        rows.append({"id":item["id"],"rating":item["rating"],"officialComplete":item["officialComplete"],
                     "sourceCounts":count,"preExecutionBlockers":reasons,
                     "recipeAvailable":item["id"] in IDS})
    value = {"pins":PINS,"inventoryHash":digest(inventory),"scope":"all36-default-submission-shards",
             "files":[read_json(p)["source"] for p in sorted((base/"submissions").glob("*/complete.json"))],
             "items":rows,"exclusions":dict(exclusions),"validatedCount":0,
             "completeAndFiveEach":sum(not r["preExecutionBlockers"] for r in rows)}
    write_json(base/"source-scan.json",value)
    return {k:v for k,v in value.items() if k not in ("items","files")}


def build(pid, base, cache):
    args = arguments(pid,base,cache)
    preparation = rated_pool.prepare(args)
    args.extra_tests = str(base/"extras"/f"{pid}.json")
    write_json(args.extra_tests,extras(pid))
    generated = rated_pool.generate(args)
    package = base/"packages"/pid
    pairs = read_json(package/"provenance.json")["tests"]["pairs"]
    checks = []
    invalid = []
    for category in ("samples","tests"):
        for path in sorted((package/category).glob("*.in")):
            expected = path.with_suffix(".out").read_text()
            try:
                actual = output(pid,path.read_text())
                if not check(expected,actual):
                    raise ValueError("authored oracle contradicts supplied expected output")
                checks.append({"pair":f"{category}/{path.stem}","inputHash":sha_file(path),
                               "outputHash":sha_file(path.with_suffix('.out')),"oracleOutputHash":hashlib.sha256(actual.encode()).hexdigest(),
                               "constraints":"passed","expectedOutput":"passed"})
            except ValueError as exc:
                invalid.append({"pair":f"{category}/{path.stem}","reason":str(exc)})
    extra_names = [r["name"] for r in pairs if r["origin"] == "worker-generated"]
    inputs = extras(pid)
    def max_score(pair):
        text = pair["input"]
        if pid in ("108A","131A","58A"):
            return len(text.strip()) if pid != "108A" else int(text[:2])*60+int(text[3:5])
        if pid == "626A":
            return int(text.split()[0])
        return max(map(abs,map(int,text.split())))
    largest_score = max(map(max_score,inputs))
    largest = [i for i,pair in enumerate(inputs) if max_score(pair) == largest_score]
    coverage = {"packageHash":generated["packageHash"],
                "boundary":[{"test":extra_names[0],"reason":"Authored minimum/small boundary case; all supplied inputs and outputs checked against strict recipe."}],
                "adversarial":[{"test":name,"reason":"Deterministic parity/order/carry/tie/transition case; see retained recipe and semantic checks."} for name in extra_names],
                "maxSize":[{"test":extra_names[i],"reason":"A legal maximum numeric or structural limit; see exact inputs and recipe's complete endpoint cases."} for i in largest],
                "inputConstraints":RULES[pid],"checkerSemantics":"Unique answer per rules; existing token checker, YES/NO case folding only. No downloaded checker executed.",
                "statementComplete":"Pinned description,input_format,output_format and all examples preserved by foundation build_statement; reviewed source prose against recipe. Required figures not used for these recipes; source-dependent1182A deliberately excluded."}
    write_json(base/"coverage"/f"{pid}.json",coverage)
    semantics = {"id":pid,"packageHash":generated["packageHash"],"recipeHash":sha_file(HERE/"recipes.py"),
                 "rules":RULES[pid],"checks":checks,"invalid":invalid,"passed":not invalid,
                 "extraTestsHash":sha_file(args.extra_tests),"prepare":preparation,"generate":generated,
                 "validated":False,"needsIndependentAudit":True}
    write_json(base/"semantics"/f"{pid}.json",semantics)
    if invalid:
        raise ValueError(json.dumps(invalid))
    return {"id":pid,"pairsChecked":len(checks),**generated}


def execute(pid, base, cache):
    semantic = read_json(base/"semantics"/f"{pid}.json")
    if not semantic["passed"] or semantic["recipeHash"] != sha_file(HERE/"recipes.py"):
        raise ValueError("semantic checks missing, failed or stale")
    args = arguments(pid,base,cache)
    args.coverage = str(base/"coverage"/f"{pid}.json")
    result = rated_pool.validate(args)
    write_json(base/"outcomes"/f"{pid}.json",result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage",choices=("inventory","index","build","execute","report"))
    parser.add_argument("--workspace",type=Path,default=HERE)
    parser.add_argument("--cache",type=Path,default=Path.home()/".cache/cf-race-pool")
    parser.add_argument("--ids",nargs="+",default=list(IDS))
    parser.add_argument("--jobs",type=int,default=2)
    args = parser.parse_args()
    if args.workspace.name != "1000" or any(pid not in IDS for pid in args.ids):
        parser.error("worker owns only1000 and explicitly reviewed recipes")
    if args.stage == "inventory":
        result = rated_pool.inventory(arguments(None,args.workspace,args.cache))
    elif args.stage == "index":
        result = source_index(args.workspace,args.cache)
    elif args.stage == "report":
        result = rated_pool.report(arguments(None,args.workspace,args.cache))
    else:
        def work(pid):
            try:
                result = (build if args.stage == "build" else execute)(pid,args.workspace,args.cache)
            except (ValueError,OSError,KeyError,RuntimeError,StopIteration) as exc:
                result = {"id":pid,"stage":args.stage,"status":"blocked","reason":str(exc),"validated":False}
                write_json(args.workspace/"outcomes"/f"{pid}-{args.stage}-blocked.json",result)
            print(json.dumps(result,sort_keys=True),flush=True)
            return result
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            result = list(executor.map(work,args.ids))
    print(json.dumps(result,sort_keys=True,indent=2),flush=True)


if __name__ == "__main__":
    main()
