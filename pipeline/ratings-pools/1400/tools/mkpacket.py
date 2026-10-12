import json, sys
from pathlib import Path
B = Path.home() / "Documents/cf-pools/1400/state"
OUT = Path(__file__).resolve().parent / "oracle_req"
for pid in sys.argv[1:]:
    r = json.loads((B / pid / "source-row.json").read_text())
    parts = [f"# {pid}: {r['title']}", f"Time limit: {r['time_limit']} s; memory limit: {r['memory_limit']} MB", "",
             "## Statement", r["description"].strip(), "", "## Input", r["input_format"].strip(), "", "## Output", r["output_format"].strip(), ""]
    for i, e in enumerate(r.get("examples") or [], 1):
        parts += [f"## Example {i} input", "```", e["input"].rstrip("\n"), "```", f"## Example {i} output", "```", e["output"].rstrip("\n"), "```", ""]
    if r.get("note"):
        parts += ["## Note", r["note"].strip(), ""]
    (OUT / f"{pid}.md").write_text("\n".join(parts) + "\n")
