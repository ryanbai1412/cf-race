"""Pinned, content-addressed public data. No credentials or proxy fallback."""
import hashlib
import json
import os
from pathlib import Path
import re
import time
import requests

PROBLEMS_REVISION = "fbe3f6e903ee854eec2e69e9d96d0306cde59baf"
SUBMISSIONS_REVISION = "07e7bf31f284b0e90e02dfc7ab675d5821e1c068"
PINS = {"open-r1/codeforces": PROBLEMS_REVISION,
        "open-r1/codeforces-submissions": SUBMISSIONS_REVISION}


def sha_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get(url, **kwargs):
    last = None
    for attempt in range(4):
        try:
            response = requests.get(url, timeout=120, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"public download failed: {url}: {last}")


def tree(dataset, prefix):
    url = f"https://huggingface.co/api/datasets/{dataset}/tree/{PINS[dataset]}/{prefix}"
    result = []
    while url:
        response = get(url)
        result.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return sorted((r for r in result if r["type"] == "file"), key=lambda r: r["path"])


def download(dataset, entry, cache):
    expected = entry.get("lfs", {}).get("oid")
    if not expected or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ValueError("source must have upstream LFS SHA256")
    dest = Path(cache) / dataset.replace("/", "--") / PINS[dataset] / entry["path"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size == entry["size"] and sha_file(dest) == expected:
        return dest
    url = f"https://huggingface.co/datasets/{dataset}/resolve/{PINS[dataset]}/{entry['path']}"
    tmp = dest.with_name(dest.name + f".{os.getpid()}.partial")
    try:
        with get(url, stream=True) as response, tmp.open("wb") as f:
            for chunk in response.iter_content(1024 * 1024):
                f.write(chunk)
        if tmp.stat().st_size != entry["size"] or sha_file(tmp) != expected:
            raise ValueError(f"source size/hash mismatch: {entry['path']}")
        os.replace(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)
    return dest


def parquet_rows(path, columns=None):
    import pyarrow.parquet as pq
    for batch in pq.ParquetFile(path).iter_batches(batch_size=32, columns=columns):
        yield from batch.to_pylist()


def provenance(dataset, entry):
    return {"dataset": dataset, "revision": PINS[dataset], "path": entry["path"],
            "sha256": entry["lfs"]["oid"], "bytes": entry["size"],
            "url": f"https://huggingface.co/datasets/{dataset}/resolve/{PINS[dataset]}/{entry['path']}"}


def generated_tests(row, cache):
    count = row.get("generated_tests")
    if not isinstance(count, int) or count < 0:
        raise ValueError("missing generated test count")
    if count == 0:
        return [], None
    name = f"generated_tests/test_cases_{int(row['contest_id']):04d}.parquet"
    entry = next((e for e in tree("open-r1/codeforces", "generated_tests") if e["path"] == name), None)
    if entry is None:
        raise ValueError(f"advertised generated tests unavailable: {name}")
    tests = [r for r in parquet_rows(download("open-r1/codeforces", entry, cache))
             if r["problem_id"] == row["id"]]
    index_key = "test_case_i" if tests and "test_case_i" in tests[0] else "test_i"
    tests.sort(key=lambda r: r[index_key])
    if len(tests) != count or len({r[index_key] for r in tests}) != count:
        raise ValueError("generated test count/identity mismatch")
    return tests, provenance("open-r1/codeforces", entry)


def submissions(pid, cache, all_submissions=False):
    dataset = "open-r1/codeforces-submissions"
    prefixes = ["data"] if all_submissions else ["selected_accepted", "selected_incorrect"]
    result, sources = [], []
    for prefix in prefixes:
        for entry in tree(dataset, prefix):
            if not entry["path"].endswith(".parquet"):
                continue
            source = provenance(dataset, entry)
            sources.append(source)
            for row in parquet_rows(download(dataset, entry, cache)):
                if row["problem_id"] == pid:
                    row["provenance"] = source
                    result.append(row)
    return result, sources
