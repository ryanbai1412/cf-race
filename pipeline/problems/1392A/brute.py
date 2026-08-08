"""Independent solution: BFS/DFS over reachable array states (tiny n only)."""
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def best(a):
    res = len(a)
    for i in range(len(a) - 1):
        if a[i] != a[i + 1]:
            nxt = a[:i] + (a[i] + a[i + 1],) + a[i + 2:]
            res = min(res, best(nxt))
    return res


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = tuple(int(next(it)) for _ in range(n))
        out.append(str(best(a)))
    sys.stdout.write("\n".join(out) + "\n")


main()
