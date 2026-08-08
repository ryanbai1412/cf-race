"""Independent brute force: BFS over volumes (never negative), small values."""
import sys
from collections import deque

STEPS = (-5, -2, -1, 1, 2, 5)


def bfs(a, b, cap):
    if a == b:
        return 0
    dist = {a: 0}
    q = deque([a])
    while q:
        v = q.popleft()
        for s in STEPS:
            u = v + s
            if u < 0 or u > cap or u in dist:
                continue
            dist[u] = dist[v] + 1
            if u == b:
                return dist[u]
            q.append(u)
    return -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        out.append(bfs(a, b, max(a, b) + 10))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
