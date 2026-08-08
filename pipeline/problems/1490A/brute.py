"""Independent solution: BFS over integer values (bounded) to find the minimum
number of inserted values that connect each adjacent pair densely."""
import sys
from collections import deque

LIMIT = 200


def pair_cost(x, y):
    lo, hi = min(x, y), max(x, y)
    dist = {lo: 0}
    q = deque([lo])
    while q:
        v = q.popleft()
        if max(v, hi) <= 2 * min(v, hi):
            return dist[v]
        for nxt in range(1, LIMIT + 1):
            if max(v, nxt) <= 2 * min(v, nxt) and nxt not in dist:
                dist[nxt] = dist[v] + 1
                q.append(nxt)
    raise RuntimeError("unreachable")


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        out.append(str(sum(pair_cost(a[i], a[i + 1]) for i in range(n - 1))))
    sys.stdout.write("\n".join(out) + "\n")


main()
