"""Scrape a Codeforces problem: statement.html (sanitized, MathJax-friendly),
samples/, and meta.json skeleton.

Usage: python3 pipeline/scrape.py 1927A [1927B ...]
"""
import json
import os
import re
import sys

from bs4 import BeautifulSoup

from common import PROBLEMS_DIR, fetch_proxy, split_problem_id


def _pre_text(pre) -> str:
    """Extract text from a sample <pre>, handling test-example-line divs."""
    divs = pre.find_all("div", class_="test-example-line")
    if divs:
        text = "\n".join(d.get_text() for d in divs)
    else:
        text = pre.get_text()
    text = text.replace("\r\n", "\n").strip("\n")
    return text + "\n"


def _mathjax_friendly(html: str) -> str:
    """Convert CF's $$$...$$$ / $$$$$$...$$$$$$ delimiters to \\(..\\) / \\[..\\]."""

    def toggle(s: str, delim: str, open_d: str, close_d: str) -> str:
        parts = s.split(delim)
        out = [parts[0]]
        for i, p in enumerate(parts[1:]):
            out.append(open_d if i % 2 == 0 else close_d)
            out.append(p)
        return "".join(out)

    html = toggle(html, "$$$$$$", "\\[", "\\]")
    html = toggle(html, "$$$", "\\(", "\\)")
    return html


def _fix_urls(soup) -> None:
    for tag in soup.find_all(["img", "a"]):
        attr = "src" if tag.name == "img" else "href"
        val = tag.get(attr)
        if not val:
            continue
        val = re.sub(r"^(https?:)?//cf-p\.vercel\.app(/cf-p\.vercel\.app/proxy/[a-z.]+)?",
                     "https://codeforces.com", val)
        if val.startswith("/"):
            val = "https://codeforces.com" + val
        tag[attr] = val


def scrape(problem_id: str) -> dict:
    contest_id, index = split_problem_id(problem_id)
    html = fetch_proxy(f"/problemset/problem/{contest_id}/{index}")
    soup = BeautifulSoup(html, "html.parser")
    stmt = soup.find("div", class_="problem-statement")
    if stmt is None:
        raise RuntimeError(f"no problem-statement div for {problem_id}")

    title = stmt.find("div", class_="title").get_text().strip()
    name = re.sub(r"^[A-Z][0-9]?\.\s*", "", title)
    tl_text = stmt.find("div", class_="time-limit").get_text()
    ml_text = stmt.find("div", class_="memory-limit").get_text()
    tl_ms = int(float(re.search(r"([\d.]+)\s*second", tl_text).group(1)) * 1000)
    ml_mb = int(re.search(r"(\d+)\s*megabyte", ml_text).group(1))

    samples = []
    sample_tests = stmt.find("div", class_="sample-tests")
    for st in sample_tests.find_all("div", class_="sample-test"):
        inputs = st.find_all("div", class_="input")
        outputs = st.find_all("div", class_="output")
        for inp, out in zip(inputs, outputs):
            samples.append((_pre_text(inp.find("pre")), _pre_text(out.find("pre"))))

    input_spec = stmt.find("div", class_="input-specification")
    multi_test = bool(input_spec and re.search(
        r"number of test cases", input_spec.get_text(), re.I))

    for s in stmt.find_all("script"):
        s.decompose()
    _fix_urls(stmt)
    statement_html = _mathjax_friendly(str(stmt))

    out_dir = os.path.join(PROBLEMS_DIR, problem_id)
    os.makedirs(os.path.join(out_dir, "samples"), exist_ok=True)
    with open(os.path.join(out_dir, "statement.html"), "w") as f:
        f.write(statement_html)
    for i, (sin, sout) in enumerate(samples, 1):
        with open(os.path.join(out_dir, "samples", f"{i}.in"), "w") as f:
            f.write(sin)
        with open(os.path.join(out_dir, "samples", f"{i}.out"), "w") as f:
            f.write(sout)

    meta_path = os.path.join(out_dir, "meta.json")
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
    meta = {
        "id": problem_id,
        "name": name,
        "rating": meta.get("rating", 800),
        "timeLimitMs": tl_ms,
        "memoryLimitMb": ml_mb,
        "multiTest": multi_test,
        "specialJudge": meta.get("specialJudge", False),
        "floatEps": meta.get("floatEps"),
        "raceTimerSec": meta.get("raceTimerSec", 180),
        "touristTimeMs": meta.get("touristTimeMs"),
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    print(f"{problem_id}: '{name}' tl={tl_ms}ms ml={ml_mb}MB samples={len(samples)} multiTest={multi_test}")
    return meta


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        scrape(pid)
