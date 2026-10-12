import sys, json
from pathlib import Path
sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from pool_sources import submissions
from pool_contract import read_json
base = Path.home()/"Documents/cf-pools/1400"
ids = [i["sourceId"] for i in read_json(base/"inventory.json")["items"] if not i["exclusions"]]
res, src = submissions(ids[0], str(Path.home()/".cache/cf-race-pool"), True, base/"submissions", ids)
print(len(res), len(src))
