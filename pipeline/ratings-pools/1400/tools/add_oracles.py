import json, sys
from pathlib import Path
W = Path("/home/ubuntu/Documents/w1400")
uuid, sess = sys.argv[1], sys.argv[2]
idx = json.loads((W / "oracles/index.json").read_text())
for d in sorted((W / "oracles_raw" / uuid).iterdir()):
    if not d.is_dir():
        continue
    for name, lang in (("oracle.py", "Python 3"), ("oracle.cpp", "C++17")):
        if (d / name).exists():
            assert d.name not in idx, d.name
            idx[d.name] = {"author": f"devin-oracle-session-{sess}", "language": lang, "path": str(d / name),
                           "url": f"https://staging.itsdev.in/sessions/{sess}"}
            print("added", d.name, lang)
(W / "oracles/index.json").write_text(json.dumps(idx, indent=1, sort_keys=True))
print(len(idx))
