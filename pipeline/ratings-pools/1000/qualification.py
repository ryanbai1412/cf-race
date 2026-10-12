"""Bind generated suites to a separate, attributed public accepted oracle."""
import hashlib
import json

from pool_contract import read_json,write_json
from pool_generation import sandbox
from pool_sandbox import kind,run


def generator(pid,here):
    modules = ("input_layout","recipes","additional","generated_recipes","replenish")
    review = read_json(here/"statement-review.json")
    sources = {}
    for name in modules:
        code = (here/f"{name}.py").read_text()
        if name=="additional":
            code = code.replace('json.loads(Path(__file__).with_name("statement-review.json").read_text())',repr(review))
        sources[name] = code
    module = "replenish" if pid in __import__("replenish").IDS else "generated_recipes"
    return ("import json,sys,types\n"
            f"SOURCES={sources!r}\n"
            "for name,code in SOURCES.items():\n"
            "    m=types.ModuleType(name)\n"
            "    m.__file__='/work/'+name+'.py'\n"
            "    sys.modules[name]=m\n"
            "    exec(compile(code,m.__file__,'exec'),m.__dict__)\n"
            "assert int(sys.stdin.readline())==0\n"
            f"pairs=sys.modules[{module!r}].extras({pid!r})\n"
            "print(json.dumps([{'input':p['input'],'output':p['output']} for p in pairs],sort_keys=True))\n")


def qualify(pid,base,cache,here):
    import worker
    semantics = read_json(base/"semantics"/f"{pid}.json")
    if not semantics["passed"] or semantics["recipeHash"]!=worker.recipe_hash(pid):
        raise ValueError("constraint/oracle checks failed or stale; keep upstream contradiction quarantined")
    row = read_json(base/"state"/pid/"source-row.json")
    if row["official_tests_complete"]:
        return {"id":pid,"status":"official-basis-no-qualification-needed"}
    proofs = base/"qualification-sources"/pid
    proofs.mkdir(parents=True,exist_ok=True)
    source = generator(pid,here)
    (proofs/"generator.py").write_text(source)
    prior = read_json(base/"evidence"/f"{pid}.json") if (base/"evidence"/f"{pid}.json").exists() else {}
    used = {s["sourceHash"] for s in prior.get("submissions",[])}
    inventory = read_json(base/"inventory.json")
    source_ids = [i["sourceId"] for i in inventory["items"] if not worker.rated_pool.inventory_blockers(i)]
    available,_ = worker.source_submissions(row["id"],str(cache),True,base/"submissions",source_ids)
    candidates = [s for s in available if s.get("verdict")=="OK" and s.get("testset")=="TESTS" and
                  (s.get("programmingLanguage","").startswith("GNU C++") or s.get("programmingLanguage","").startswith("Python 3")) and
                  s.get("source") and hashlib.sha256(s["source"].encode()).hexdigest() not in used]
    tests = [{"name":p.stem,"input":p.read_bytes(),"output":p.with_suffix('.out').read_bytes()} for p in sorted((base/"packages"/pid/"tests").glob('*.in'))]
    attempts = []
    oracle = None
    for s in sorted(candidates,key=lambda x:int(x["submission_id"]),reverse=True)[:8]:
        result = run(s["source"],s["programmingLanguage"],tests,row["time_limit"],row["memory_limit"])
        record = {"submissionId":s["submission_id"],"sourceHash":hashlib.sha256(s["source"].encode()).hexdigest(),
                  "language":s["programmingLanguage"],"source":s["provenance"],"result":result}
        attempts.append(record)
        write_json(proofs/"oracle-attempts.json",{"sandbox":sandbox(),"attempts":attempts,"counted":False})
        if result["compiled"] and result["verdict"]=="AC":
            oracle = s
            break
    if oracle is None:
        raise ValueError("no distinct additional public accepted oracle passed all supplied tests")
    path = proofs/("oracle.cpp" if kind(oracle["programmingLanguage"])=="cpp" else "oracle.py")
    path.write_text(oracle["source"])
    review_url = f"https://codeforces.com/contest/{oracle['contestId']}/submission/{oracle['submission_id']}"
    write_json(proofs/"source.json",{"source":oracle["provenance"],"submissionId":oracle["submission_id"],"language":oracle["programmingLanguage"],
                                    "sourceHash":hashlib.sha256(oracle["source"].encode()).hexdigest(),"url":review_url,
                                    "attribution":"Public Codeforces submission; upstream dataset identifies submission, not author handle. This is independently sourced code, not a different-agent audit."})
    args = worker.arguments(pid,base,cache)
    args.generator_source = str(proofs/"generator.py")
    args.generator_language = "Python 3"
    args.generator_author = args.validator
    args.oracle_source = str(path)
    args.oracle_language = oracle["programmingLanguage"]
    args.oracle_author = f"codeforces-submission:{oracle['submission_id']}"
    args.oracle_review_url = review_url
    args.seed = 0
    args.exhaustive_domain_size = None
    args.exhaustive_domain = None
    result = worker.rated_pool.generate(args)
    write_json(proofs/"generate-result.json",result)
    return worker.inspect_generated(pid,base,args,result)
