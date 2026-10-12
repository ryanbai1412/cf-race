import json
import os
from pathlib import Path
import sys
import time

PIPELINE = Path(__file__).resolve().parents[3]
if str(PIPELINE) not in sys.path:
    sys.path.append(str(PIPELINE))
import pool_sources  # noqa: E402

TREE_CACHE = Path.home() / ".cache" / "cf-race-pool" / "tree"
_tree = pool_sources.tree


def tree(dataset, prefix):
    """Listings are taken at immutable pinned revisions, so caching them is exact; every
    downloaded file is still verified against its upstream LFS SHA256 by pool_sources.download."""
    path = TREE_CACHE / dataset.replace("/", "--") / pool_sources.PINS[dataset] / (prefix.replace("/", "--") + ".json")
    if path.exists():
        return json.loads(path.read_text())
    for attempt in range(6):
        try:
            result = _tree(dataset, prefix)
            break
        except RuntimeError:
            if attempt == 5:
                raise
            time.sleep(60 * (attempt + 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.partial")
    tmp.write_text(json.dumps(result))
    os.replace(tmp, path)
    return result


pool_sources.tree = tree

if __name__ == "__main__":
    import rated_pool
    rated_pool.tree = tree
    sys.argv = [str(PIPELINE / "rated_pool.py"), *sys.argv[1:]]
    rated_pool.main()
