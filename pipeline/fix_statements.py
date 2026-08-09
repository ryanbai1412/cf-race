#!/usr/bin/env python3
"""Repair formatting artifacts in imported problem statements.

The HuggingFace import (``import_hf.py``) wraps every source paragraph in a
single ``<p>``, so markdown bullet/number lists survive as literal ``- item``
and ``1. item`` lines that render as one run-on paragraph. It also leaves a few
stray markdown artifacts (``**bold**``, ``` `code` ```, ``$math$``) behind.

Usage::

    python pipeline/fix_statements.py --dry-run            # report only
    python pipeline/fix_statements.py 1385A 1417A          # fix these ids
    python pipeline/fix_statements.py --all                # fix everything

Requires NEXT_PUBLIC_SUPABASE_URL (or SUPABASE_URL) and
SUPABASE_SERVICE_ROLE_KEY in the environment.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ITEM_RE = re.compile(r"^\s*(?:([-*])|(\d+)\.)\s+(\S.*)$")
PARA_RE = re.compile(r"<p>((?:[^<]|<(?!/p>))*)</p>")


def _split_list(text: str) -> str | None:
    """Turn a paragraph whose lines are markdown list items into <ul>/<ol>.

    Returns None when the paragraph is not a list.
    """
    lines = text.split("\n")
    items: list[tuple[str, str]] = []
    for line in lines:
        m = ITEM_RE.match(line)
        if not m:
            return None
        items.append(("ul" if m.group(1) else "ol", m.group(3).rstrip()))
    if len(items) < 2 and not items:
        return None
    kind = items[0][0]
    if any(k != kind for k, _ in items):
        return None
    body = "".join(f"<li>{t}</li>\n" for _, t in items)
    return f"<{kind}>\n{body}</{kind}>"


def fix_markdown_lists(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        out = _split_list(m.group(1))
        return out if out is not None else m.group(0)

    return PARA_RE.sub(repl, html)


def fix_markdown_inline(html: str) -> str:
    """Convert leftover markdown emphasis/code spans to HTML."""
    html = re.sub(r"(?<![\\*])\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"(?<![`\\])`([^`\n]+)`(?!`)", r"<code>\1</code>", html)
    return html


def fix_display_math(html: str) -> str:
    r"""Repair display math mangled into ``\(\)...\(\)\)``.

    A source ``$$...$$`` block had each ``$`` rewritten to ``\(...\)``, which
    leaves the delimiters themselves inside the math and makes KaTeX bail.
    """
    return re.sub(
        r"\\\(\\\(\\\)([\s\S]*?)\\\(\\\)\\\)",
        lambda m: "\\[" + m.group(1).strip() + "\\]",
        html,
    )


# Entities that must be decoded inside math: KaTeX only decodes &lt; &gt; &amp;.
MATH_ENTITIES = [("&quot;", '"'), ("&#x27;", "'"), ("&#39;", "'")]


def fix_math_entities(html: str) -> str:
    """Decode quote entities inside TeX spans so KaTeX can parse them."""

    def repl(m: re.Match[str]) -> str:
        tex = m.group(2)
        for ent, ch in MATH_ENTITIES:
            tex = tex.replace(ent, ch)
        return m.group(1) + tex + m.group(3)

    html = re.sub(r"(\\\()([\s\S]*?)(\\\))", repl, html)
    return re.sub(r"(\\\[)([\s\S]*?)(\\\])", repl, html)


def fix_texttt_underscores(html: str) -> str:
    r"""Escape literal underscores in quoted ``\texttt{"..."}`` string literals.

    Unescaped ``_`` there is a subscript to KaTeX and aborts the whole span.
    """

    def repl(m: re.Match[str]) -> str:
        return "\\texttt{\"" + re.sub(r"(?<!\\)_", r"\\_", m.group(1)) + "\"}"

    return re.sub(r'\\texttt\{"([^"{}]*)"\}', repl, html)


def fix_figure_urls(html: str) -> str:
    """Point figures at the origin that still serves them.

    Statement figures were captured as ``codeforces.com/proxy/espresso.cfcom/<h>.png``,
    a path that now 404s; the images live on ``espresso.codeforces.com``.
    """
    return re.sub(
        r"https?://codeforces\.com/proxy/espresso\.cfcom/",
        "https://espresso.codeforces.com/",
        html,
    )


def fix_statement(html: str) -> str:
    if not html:
        return html
    out = fix_figure_urls(html)
    out = fix_display_math(out)
    out = fix_math_entities(out)
    out = fix_texttt_underscores(out)
    out = fix_markdown_lists(out)
    out = fix_markdown_inline(out)
    return out


def _supabase() -> tuple[str, str]:
    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    return url.rstrip("/"), key


def _request(method: str, path: str, key: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(path, data=data, method=method)
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "return=minimal")
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="problem ids to fix (default: --all)")
    ap.add_argument("--all", action="store_true", help="process every problem")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()

    url, key = _supabase()
    rows = _request("GET", f"{url}/rest/v1/problems?select=id,statement_html&order=id.asc", key)
    if args.ids:
        wanted = set(args.ids)
        rows = [r for r in rows if r["id"] in wanted]
    elif not args.all:
        sys.exit("pass problem ids or --all")

    changed = 0
    for row in rows:
        before = row["statement_html"] or ""
        after = fix_statement(before)
        if after == before:
            continue
        changed += 1
        print(("would fix " if args.dry_run else "fixed ") + row["id"])
        if not args.dry_run:
            q = urllib.parse.quote(row["id"], safe="")
            _request(
                "PATCH",
                f"{url}/rest/v1/problems?id=eq.{q}",
                key,
                {"statement_html": after},
            )
    print(f"{changed}/{len(rows)} statements {'need fixes' if args.dry_run else 'updated'}")


if __name__ == "__main__":
    main()
