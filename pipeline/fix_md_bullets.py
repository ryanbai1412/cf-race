#!/usr/bin/env python3
"""Fix literal markdown bullet lines left inside <p> blocks of problems.statement_html.

The HF import (import_hf.py) split statements into <p> blocks on blank lines,
leaving markdown bullet lists as literal "- item" lines inside a paragraph.
This converts consecutive "- " lines within a <p> into a proper <ul><li> list,
keeping any non-bullet leading/trailing lines as separate <p> blocks.

Usage:
  python3 pipeline/fix_md_bullets.py [--dry-run] [id ...]

Requires NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env vars.
Without ids, scans all problems and fixes every affected one.
"""
import json
import os
import re
import sys
import urllib.request

P_RE = re.compile(r"<p>(.*?)</p>", re.S)
BULLET_RE = re.compile(r"^- (.*)$")


def fix_paragraph(inner: str) -> str:
    lines = inner.split("\n")
    if not any(BULLET_RE.match(l.strip()) for l in lines):
        return f"<p>{inner}</p>"
    out = []
    buf_text = []
    buf_items = []

    def flush_text():
        if buf_text:
            out.append("<p>" + "\n".join(buf_text) + "</p>")
            buf_text.clear()

    def flush_items():
        if buf_items:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in buf_items) + "</ul>")
            buf_items.clear()

    for line in lines:
        m = BULLET_RE.match(line.strip())
        if m:
            flush_text()
            item = m.group(1)
            # strip trailing comma/period-only separators left from prose lists? keep as-is
            buf_items.append(item)
        elif line.strip() == "":
            flush_items()
            flush_text()
        elif buf_items:
            # continuation of the previous bullet item
            buf_items[-1] += " " + line.strip()
        else:
            buf_text.append(line)
    flush_items()
    flush_text()
    return "\n".join(out)


def fix_html(h: str) -> str:
    return P_RE.sub(lambda m: fix_paragraph(m.group(1)), h)


def main():
    url = os.environ["NEXT_PUBLIC_SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    args = sys.argv[1:]
    dry = "--dry-run" in args
    ids = [a for a in args if not a.startswith("--")]

    def get(path):
        req = urllib.request.Request(f"{url}/rest/v1/{path}",
                                     headers={"apikey": key, "Authorization": f"Bearer {key}"})
        return json.load(urllib.request.urlopen(req))

    rows = []
    off = 0
    while True:
        batch = get(f"problems?select=id,statement_html&order=id.asc&offset={off}&limit=200")
        rows += batch
        if len(batch) < 200:
            break
        off += 200
    if ids:
        rows = [r for r in rows if r["id"] in ids]

    fixed = 0
    for r in rows:
        h = r["statement_html"] or ""
        nh = fix_html(h)
        if nh == h:
            continue
        fixed += 1
        print(("DRY " if dry else "FIX ") + r["id"])
        if dry:
            continue
        data = json.dumps({"statement_html": nh}).encode()
        req = urllib.request.Request(
            f"{url}/rest/v1/problems?id=eq.{r['id']}", data=data, method="PATCH",
            headers={"apikey": key, "Authorization": f"Bearer {key}",
                     "Content-Type": "application/json", "Prefer": "return=minimal"})
        urllib.request.urlopen(req)
    print(f"{fixed} problems {'would be ' if dry else ''}updated")


if __name__ == "__main__":
    main()
