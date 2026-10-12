import json,sys
sys.path.insert(0,"/home/ubuntu/repos/cf-race/pipeline")
from pool_sources import download, parquet_rows
from pathlib import Path
inv=json.load(open("/home/ubuntu/Documents/cf-pools/1400/inventory.json"))
c=[i for i in inv["items"] if not i["exclusions"] and i["officialComplete"] is True]
want={i["sourceId"]:i for i in c}
bypath={}
for i in c: bypath.setdefault(i["source"]["path"],[]).append(i)
Path("rows").mkdir(exist_ok=True)
for path,items in bypath.items():
    e={"path":path,"size":items[0]["source"]["bytes"],"lfs":{"oid":items[0]["source"]["sha256"]}}
    ids={i["sourceId"] for i in items}
    for r in parquet_rows(download("open-r1/codeforces",e,str(Path.home()/".cache/cf-race-pool"))):
        if r["id"] in ids:
            json.dump(r,open(f"rows/{r['id'].replace('/','')}.json","w"))
