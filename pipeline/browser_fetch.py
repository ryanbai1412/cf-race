"""Fetch CF pages that sit behind the JS anti-bot check (e.g. submission
source pages) using a real Chrome over CDP + Playwright.

Submission sources require a logged-in session: set CF_JSESSIONID in the
environment to the JSESSIONID cookie of a logged-in codeforces.com session.

Usage: python3 pipeline/browser_fetch.py <cf-path> <outfile>
Also importable: fetch(path) -> html (reuses one browser page per process).
"""
import os
import sys
import time

from playwright.sync_api import sync_playwright

from common import PROXY_BASE, PROXY_COOKIE

CDP = "http://localhost:29229"

_state = {}


def _page():
    if not PROXY_COOKIE:
        raise RuntimeError(
            "CF_PROXY_AUTH_TOKEN must be set to fetch HTML through the proxy"
        )
    if "page" in _state and not _state["page"].is_closed():
        return _state["page"]
    if "pw" not in _state:
        _state["pw"] = sync_playwright().start()
        _state["browser"] = _state["pw"].chromium.connect_over_cdp(CDP)
    ctx = _state["browser"].contexts[0]
    cookies = [{
        "name": "CF_PROXY_AUTH_TOKEN",
        "value": PROXY_COOKIE["CF_PROXY_AUTH_TOKEN"],
        "domain": "cf-p.vercel.app",
        "path": "/",
    }]
    jsid = os.environ.get("CF_JSESSIONID", "").strip()
    if jsid:
        cookies.append({"name": "JSESSIONID", "value": jsid,
                        "domain": "cf-p.vercel.app", "path": "/"})
    ctx.add_cookies(cookies)
    _state["page"] = ctx.new_page()
    return _state["page"]


def fetch(path: str, wait_selector: str = "#program-source-text", timeout_s: int = 40) -> str:
    page = _page()
    page.goto(PROXY_BASE + path, timeout=timeout_s * 1000, wait_until="domcontentloaded")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            if page.locator(wait_selector).count() > 0:
                break
        except Exception:
            pass
        time.sleep(1.0)
    return page.content()


def fetch_text(path: str, selector: str = "#program-source-text", timeout_s: int = 40):
    """Fetch a page and return the rendered inner text of `selector` (preserves
    line breaks even after CF's prettifier rewrites the <pre>), or None."""
    page = _page()
    page.goto(PROXY_BASE + path, timeout=timeout_s * 1000, wait_until="domcontentloaded")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            if page.locator(selector).count() > 0:
                return page.locator(selector).inner_text().replace("\xa0", " ")
        except Exception:
            pass
        time.sleep(1.0)
    reset_page()
    return None


def reset_page():
    page = _state.pop("page", None)
    if page is not None:
        try:
            page.close()
        except Exception:
            pass


if __name__ == "__main__":
    html = fetch(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(html)
    print(len(html))
