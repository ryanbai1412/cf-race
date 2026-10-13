import sys, json, base64
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from pool_sandbox import run
B = Path("/home/ubuntu/Documents/cf-pools/1400")
def scan(pid):
    ev = json.loads((B / "evidence" / f"{pid}.json").read_text())
    row = json.loads((B / "state" / pid / "source-row.json").read_text())
    tl, ml = row["time_limit"], int(row["memory_limit"])
    out = []
    for s in ev["submissions"]:
        if s["expected"] == "OK":
            continue
        t = s["failedTest"]
        inp = (B / "packages" / pid / "tests" / f"{t}.in").read_bytes()
        exp = (B / "packages" / pid / "tests" / f"{t}.out").read_bytes()
        if b"\r" not in inp:
            out.append((s["submissionId"], t, "noCR"))
            continue
        code = json.loads((B / "state" / pid / "sources" / f"{s['submissionId']}.json").read_text())["code"]
        r = run(code, s["language"], [{"name": t, "input": inp.replace(b"\r\n", b"\n").replace(b"\r", b""), "output": exp}], tl, ml)
        out.append((s["submissionId"], t, "LF:" + str(r.get("verdict"))))
    bad = [o for o in out if o[2] == "LF:AC"]
    return pid, ("ARTIFACT" if bad else "ok"), out
ids = sys.argv[1:]
with ThreadPoolExecutor(3) as ex:
    for pid, st, out in ex.map(scan, ids):
        print(pid, st, out, flush=True)
