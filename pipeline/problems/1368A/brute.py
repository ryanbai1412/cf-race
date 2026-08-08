"""Independent brute force for 1368A: BFS over (a, b) states exploring both
operations, so no greedy assumption is made. Small n only."""
import sys
from collections import deque


def solve(a, b, n):
    start = (min(a, b), max(a, b))
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        if y > n:
            return d
        for nx, ny in ((x + y, y), (x, x + y)):
            s = (min(nx, ny), max(nx, ny))
            if s not in dist and min(s) <= 4 * n:
                dist[s] = d + 1
                q.append(s)
    raise RuntimeError("unreachable")


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 3 * i]); b = int(data[2 + 3 * i]); n = int(data[3 + 3 * i])
        out.append(solve(a, b, n))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
