import json, sys, re, html
from pathlib import Path
B = Path.home()/"Documents/cf-pools/1400/state"
for pid in sys.argv[1:]:
    p = B/pid/"source-row.json"
    if not p.exists(): print("##", pid, "NOT PREPARED"); continue
    r = json.loads(p.read_text())
    clean = lambda s: re.sub(r"\s+", " ", (s or "")).strip()
    print(f"## {pid} {r['title']} TL={r['time_limit']} ML={r['memory_limit']} off={len(r['official_tests'])}/{r['testset_size']} gen={r['generated_tests']}")
    print("D:", clean(r["description"])[:1100])
    print("I:", clean(r["input_format"])[:700])
    print("O:", clean(r["output_format"])[:500])
    for e in (r.get("examples") or [])[:2]: print("EX:", repr(e["input"][:150]), "->", repr(e["output"][:80]))
    if r.get("note"): print("N:", clean(r["note"])[:200])
