"""Import problem statements from the open-r1/codeforces HF dataset into our
/solo problem-package format (problems/<id>/statement.html, samples/, meta.json).

Usage: python3 pipeline/import_hf.py <ids.json>
Skips problems that already have problems/<id>/meta.json.
"""
import html
import json
import os
import re
import sys

import datasets

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PROBLEMS_DIR


def md_to_html(text: str) -> str:
    """Convert the dataset's markdown-ish statement text into simple HTML with
    MathJax \\(..\\) delimiters (dataset uses $...$ / $$...$$)."""
    if not text:
        return ""
    t = html.escape(text)
    t = re.sub(r"\$\$\$?(.+?)\$\$\$?", lambda m: "\\(" + m.group(1) + "\\)", t, flags=re.S)
    t = re.sub(r"\$(.+?)\$", lambda m: "\\(" + m.group(1) + "\\)", t, flags=re.S)
    paras = [p.strip() for p in t.split("\n\n") if p.strip()]
    return "\n".join(f"<p>{p}</p>" for p in paras)


def build_statement(row) -> str:
    parts = ['<div class="problem-statement">']
    parts.append(f'<div class="header"><div class="title">{html.escape(row["title"])}</div>')
    tl = row.get("time_limit")
    ml = row.get("memory_limit")
    if tl:
        parts.append(f'<div class="time-limit">time limit per test: {tl} s</div>')
    if ml:
        parts.append(f'<div class="memory-limit">memory limit per test: {int(ml)} MB</div>')
    parts.append("</div>")
    parts.append(md_to_html(row.get("description") or ""))
    if row.get("input_format"):
        parts.append('<div class="input-specification"><div class="section-title">Input</div>')
        parts.append(md_to_html(row["input_format"]))
        parts.append("</div>")
    if row.get("output_format"):
        parts.append('<div class="output-specification"><div class="section-title">Output</div>')
        parts.append(md_to_html(row["output_format"]))
        parts.append("</div>")
    if row.get("note"):
        parts.append('<div class="note"><div class="section-title">Note</div>')
        parts.append(md_to_html(row["note"]))
        parts.append("</div>")
    parts.append("</div>")
    return "\n".join(parts)


def import_row(row):
    pid = f"{row['contest_id']}{row['index']}"
    pdir = os.path.join(PROBLEMS_DIR, pid)
    if os.path.exists(os.path.join(pdir, "meta.json")):
        return "exists"
    os.makedirs(os.path.join(pdir, "samples"), exist_ok=True)
    with open(os.path.join(pdir, "statement.html"), "w") as f:
        f.write(build_statement(row))
    samples = row.get("examples") or []
    for i, ex in enumerate(samples, 1):
        with open(os.path.join(pdir, "samples", f"{i}.in"), "w") as f:
            f.write((ex.get("input") or "").rstrip("\n") + "\n")
        with open(os.path.join(pdir, "samples", f"{i}.out"), "w") as f:
            f.write((ex.get("output") or "").rstrip("\n") + "\n")
    name = re.sub(r"^[A-Z][0-9]?\.\s*", "", row["title"])
    meta = {
        "id": pid,
        "name": name,
        "rating": row.get("rating"),
        "tags": row.get("tags") or [],
        "timeLimitMs": int(float(row.get("time_limit") or 1) * 1000),
        "memoryLimitMb": int(row.get("memory_limit") or 256),
        "multiTest": None,
        "specialJudge": bool(row.get("generated_checker")),
        "floatEps": None,
        "raceTimerSec": 180,
        "touristTimeMs": None,
        "source": "open-r1/codeforces",
    }
    with open(os.path.join(pdir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    return "imported"


def main():
    want = set(json.load(open(sys.argv[1])))
    ds = datasets.load_dataset("open-r1/codeforces", split="train")
    seen = {}
    for row in ds:
        pid = f"{row['contest_id']}{row['index']}"
        if pid in want and pid not in seen:
            seen[pid] = import_row(row)
    counts = {}
    for v in seen.values():
        counts[v] = counts.get(v, 0) + 1
    print("done:", counts)
    print("missing:", sorted(want - set(seen)))


if __name__ == "__main__":
    main()
