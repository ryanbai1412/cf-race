"""Upload problem packages to the Supabase Storage bucket `problems` and
upsert a row per problem into the `problems` table (if it exists).

Env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY.
Usage: python3 pipeline/upload_supabase.py [problemId ...]   (default: all)
"""
import json
import mimetypes
import os
import sys

import requests

from common import PROBLEMS_DIR, load_meta
from pool_contract import publication_gate
from pathlib import Path
import hashlib

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
HEADERS = {"Authorization": f"Bearer {KEY}", "apikey": KEY}
BUCKET = "problems"


def ensure_bucket():
    r = requests.get(f"{URL}/storage/v1/bucket/{BUCKET}", headers=HEADERS)
    if r.status_code == 200:
        return
    r = requests.post(f"{URL}/storage/v1/bucket", headers=HEADERS,
                      json={"id": BUCKET, "name": BUCKET, "public": False})
    r.raise_for_status()
    print(f"created private bucket '{BUCKET}'")


def package_snapshot(problem_id: str):
    root = Path(PROBLEMS_DIR) / problem_id
    gate = publication_gate(root)
    snapshot = {p.relative_to(root).as_posix(): p.read_bytes()
                for p in sorted(root.rglob("*")) if p.is_file()}
    if not gate["legacy"]:
        actual = {p: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for p, data in snapshot.items()}
        if actual != gate["files"]:
            raise ValueError("package changed after publication gate")
    return snapshot


def upload_package(problem_id: str, snapshot=None):
    root = os.path.join(PROBLEMS_DIR, problem_id)
    snapshot = snapshot if snapshot is not None else package_snapshot(problem_id)
    n = 0
    for name, data in snapshot.items():
        rel = f"{problem_id}/{name}"
        ctype = mimetypes.guess_type(name)[0] or "text/plain"
        r = requests.post(f"{URL}/storage/v1/object/{BUCKET}/{rel}",
                          headers={**HEADERS, "Content-Type": ctype, "x-upsert": "true"}, data=data)
        r.raise_for_status()
        n += 1
    print(f"{problem_id}: uploaded {n} files")


def table_exists() -> bool:
    r = requests.get(f"{URL}/rest/v1/problems?limit=1", headers=HEADERS)
    return r.status_code == 200


def upsert_row(problem_id: str, snapshot=None):
    snapshot = snapshot if snapshot is not None else package_snapshot(problem_id)
    meta = json.loads(snapshot["meta.json"])
    statement = snapshot["statement.html"].decode()
    samples = [{"input": data.decode(), "output": snapshot[name[:-3] + ".out"].decode()}
               for name, data in snapshot.items() if name.startswith("samples/") and name.endswith(".in")]
    row = {
        "id": meta["id"],
        "name": meta["name"],
        "rating": meta["rating"],
        "time_limit_ms": meta["timeLimitMs"],
        "memory_limit_mb": meta["memoryLimitMb"],
        "multi_test": meta["multiTest"],
        "special_judge": meta["specialJudge"],
        "float_eps": meta["floatEps"],
        "race_timer_sec": meta["raceTimerSec"],
        "statement_html": statement,
        "samples": samples,
        # tourist_time_ms is intentionally omitted: it is maintained by the
        # tourist-recording pipeline and must not be clobbered here
    }
    r = requests.post(
        f"{URL}/rest/v1/problems?on_conflict=id", headers={
            **HEADERS, "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal"},
        data=json.dumps(row))
    if r.status_code >= 300:
        raise RuntimeError(f"upsert {problem_id}: {r.status_code} {r.text}")
    print(f"{problem_id}: row upserted")


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(
        d for d in os.listdir(PROBLEMS_DIR)
        if d != "dev"
        and os.path.exists(os.path.join(PROBLEMS_DIR, d, "statement.html")))
    snapshots = {pid: package_snapshot(pid) for pid in ids}
    ensure_bucket()
    have_table = table_exists()
    if not have_table:
        print("NOTE: no 'problems' table found — skipping row inserts")
    for pid in ids:
        upload_package(pid, snapshots[pid])
        if have_table:
            upsert_row(pid, snapshots[pid])
