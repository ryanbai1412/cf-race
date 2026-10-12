import sys, json, hashlib, collections
from pathlib import Path
sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from pool_sandbox import kind
base = Path.home()/"Documents/cf-pools/1400"
inv = json.load(open(base/"inventory.json"))
el = {i["sourceId"]: i for i in inv["items"] if not i["exclusions"]}
cnt = {k: [set(), set()] for k in el}
for shard in (base/"submissions").iterdir():
    for f in shard.glob("*.json"):
        if f.name == "complete.json": continue
        for s in json.loads(f.read_text()):
            pid = s["problem_id"]
            if pid not in cnt: continue
            if not s.get("source") or s.get("testset") != "TESTS" or kind(s.get("programmingLanguage","")) is None: continue
            v = s.get("verdict")
            if v not in ("OK","WRONG_ANSWER","TIME_LIMIT_EXCEEDED"): continue
            h = hashlib.sha256(s["source"].encode()).hexdigest()
            cnt[pid][v != "OK"].add(h)
out = {el[k]["id"]: {"acc": len(a), "inc": len(b), "officialComplete": el[k]["officialComplete"], "official": el[k]["officialCount"], "generated": el[k]["generatedCount"]} for k,(a,b) in cnt.items()}
json.dump(out, open(Path.home()/"Documents/w1400/subcounts.json","w"), indent=1, sort_keys=True)
ok = [k for k,v in out.items() if v["acc"]>=5 and v["inc"]>=5]
print("eligible", len(out), "5/5 raw", len(ok), "complete&5/5", sum(out[k]["officialComplete"] is True for k in ok))
print("acc<5", sum(v["acc"]<5 for v in out.values()), "inc<5", sum(v["inc"]<5 for v in out.values()))
