"""Shared helpers for the problem pipeline.

- Codeforces official API (works directly): https://codeforces.com/api/
- HTML pages (statement, submission source) go through the proxy
  https://cf-p.vercel.app which mirrors codeforces.com paths exactly.
"""
import json
import os
import re
import time
import urllib.parse

import requests

PROXY_BASE = "https://cf-p.vercel.app"
API_BASE = "https://codeforces.com/api"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
PROXY_COOKIE = {
    "CF_PROXY_AUTH_TOKEN": "0c87d670f6808e0f1c5cc6117052e06e4bdd7d66e78c791f7c16d487a08a2d56"
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(REPO_ROOT, "problems")
PIPELINE_DIR = os.path.join(REPO_ROOT, "pipeline")

_session = requests.Session()
_session.headers["User-Agent"] = UA


def fetch_proxy(path: str, retries: int = 4, sleep: float = 2.0) -> str:
    """Fetch an HTML page from the CF proxy. `path` is a codeforces.com path."""
    url = PROXY_BASE + path
    last = None
    for attempt in range(retries):
        r = _session.get(url, cookies=PROXY_COOKIE, timeout=60)
        last = r
        if r.status_code == 200 and "problem-statement" in r.text or (
            r.status_code == 200 and "Just a moment" not in r.text and "CF Proxy" not in r.text[:2000]
        ):
            return r.text
        time.sleep(sleep * (attempt + 1))
    raise RuntimeError(f"proxy fetch failed for {path}: status={last.status_code}")


def api(method: str, **params) -> dict:
    """Call the official Codeforces API. Returns the `result` field."""
    qs = urllib.parse.urlencode(params)
    url = f"{API_BASE}/{method}?{qs}" if qs else f"{API_BASE}/{method}"
    for attempt in range(5):
        r = _session.get(url, timeout=60)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "OK":
                return data["result"]
        time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"CF API call failed: {method} {params}")


def split_problem_id(problem_id: str):
    """'1927A' -> (1927, 'A')"""
    m = re.match(r"^(\d+)([A-Z][0-9]?)$", problem_id)
    if not m:
        raise ValueError(f"bad problem id: {problem_id}")
    return int(m.group(1)), m.group(2)


def load_meta(problem_id: str) -> dict:
    with open(os.path.join(PROBLEMS_DIR, problem_id, "meta.json")) as f:
        return json.load(f)
