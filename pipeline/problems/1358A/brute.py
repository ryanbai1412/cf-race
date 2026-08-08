"""Independent brute force for 1358A: minimum set of lanterns (each covering one
cell or two orthogonally adjacent cells) covering an n x m grid, via BFS over
covered-cell bitmasks. Small grids only (n*m <= 16)."""
import sys
from collections import deque


def solve(n, m):
    cells = n * m
    full = (1 << cells) - 1
    opts = []
    for r in range(n):
        for c in range(m):
            i = r * m + c
            opts.append(1 << i)
            if c + 1 < m:
                opts.append((1 << i) | (1 << (i + 1)))
            if r + 1 < n:
                opts.append((1 << i) | (1 << (i + m)))
    dist = {0: 0}
    q = deque([0])
    while q:
        cur = q.popleft()
        if cur == full:
            return dist[cur]
        for o in opts:
            nxt = cur | o
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return dist[full]


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i]); m = int(data[2 + 2 * i])
        out.append(solve(n, m))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
