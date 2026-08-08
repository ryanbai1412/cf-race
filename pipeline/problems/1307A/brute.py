import sys
from functools import lru_cache


def solve(n, d, a):
    # BFS over states for tiny inputs
    start = tuple(a)
    seen = {start}
    frontier = {start}
    best = a[0]
    for _ in range(d):
        nxt = set()
        for st in frontier:
            for i in range(n):
                if st[i] == 0:
                    continue
                for j in (i - 1, i + 1):
                    if 0 <= j < n:
                        ns = list(st)
                        ns[i] -= 1
                        ns[j] += 1
                        ns = tuple(ns)
                        if ns not in seen:
                            seen.add(ns)
                            nxt.add(ns)
        frontier = nxt
        for st in frontier:
            best = max(best, st[0])
        if not frontier:
            break
    return best


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, d = int(data[idx]), int(data[idx + 1]); idx += 2
        a = [int(data[idx + i]) for i in range(n)]; idx += n
        out.append(solve(n, d, a))
    print("\n".join(map(str, out)))


main()
