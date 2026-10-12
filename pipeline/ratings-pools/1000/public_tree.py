"""Replay immutable public LFS catalogs without repeating rate-limited listing requests."""
import json
from pathlib import Path

from pool_sources import PINS, tree as live_tree

CACHE = json.loads(Path(__file__).with_name("public-tree-cache.json").read_text())
if CACHE["pins"] != PINS or CACHE["schemaVersion"] != 1:
    raise ValueError("public catalog revision mismatch")


def cached_tree(dataset, prefix):
    key = dataset + ":" + prefix
    if key not in CACHE["trees"]:
        return live_tree(dataset, prefix)
    return CACHE["trees"][key]
