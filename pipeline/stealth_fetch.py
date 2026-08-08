"""Fetch codeforces.com pages directly with a stealth browser (patchright).

Requires a logged-in CF cookie string in the file pointed to by CF_COOKIES_FILE
(semicolon-separated "k=v" pairs, e.g. copied from a browser devtools request).
Importable: fetch(path, wait_selector), fetch_text(path, selector).
"""
import os
import time

from patchright.sync_api import sync_playwright

BASE = "https://codeforces.com"
PROFILE = os.path.expanduser("~/patchright-profile")

_state = {}


def _cookies():
    path = os.environ.get("CF_COOKIES_FILE", os.path.expanduser("~/cf_cookies.txt"))
    raw = open(path).read().strip()
    return [
        {"name": k, "value": v, "domain": ".codeforces.com", "path": "/"}
        for k, v in (kv.split("=", 1) for kv in raw.split("; "))
    ]


def _page():
    if "page" in _state and not _state["page"].is_closed():
        return _state["page"]
    if "pw" not in _state:
        _state["pw"] = sync_playwright().start()
        _state["ctx"] = _state["pw"].chromium.launch_persistent_context(
            PROFILE, headless=False, no_viewport=True)
        _state["ctx"].add_cookies(_cookies())
    _state["page"] = _state["ctx"].new_page()
    return _state["page"]


def reset_page():
    page = _state.pop("page", None)
    if page is not None:
        try:
            page.close()
        except Exception:
            pass


def fetch(path: str, wait_selector: str, timeout_s: int = 60) -> str:
    page = _page()
    page.goto(BASE + path, timeout=timeout_s * 1000, wait_until="domcontentloaded")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            if page.locator(wait_selector).count() > 0:
                return page.content()
        except Exception:
            pass
        time.sleep(1.0)
    reset_page()
    raise RuntimeError(f"selector {wait_selector!r} never appeared for {path}")


def fetch_text(path: str, selector: str = "#program-source-text", timeout_s: int = 40):
    page = _page()
    page.goto(BASE + path, timeout=timeout_s * 1000, wait_until="domcontentloaded")
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
