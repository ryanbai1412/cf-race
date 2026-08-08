"""Brute force for tiny grids: enumerate Megan's walks (portals = her visited
cells), then Dijkstra for Stanley with teleports between portals costing 1."""
import heapq
import sys


def solve(n, m):
    if n == 1 and m == 1:
        return 0
    cells = [(r, c) for r in range(n) for c in range(m)]

    def neigh(p):
        r, c = p
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < n and 0 <= c + dc < m:
                yield (r + dr, c + dc)

    best = [10**9]
    limit = n * m + 3  # walks longer than this can't help

    def stanley(portals):
        start, goal = (0, 0), (n - 1, m - 1)
        dist = {start: 0}
        pq = [(0, start)]
        while pq:
            d, p = heapq.heappop(pq)
            if d > dist.get(p, 10**9):
                continue
            if p == goal:
                return d
            nxt = list(neigh(p))
            if p in portals:
                nxt += [q for q in portals if q != p]
            for q in nxt:
                if d + 1 < dist.get(q, 10**9):
                    dist[q] = d + 1
                    heapq.heappush(pq, (d + 1, q))
        return dist.get(goal, 10**9)

    seen = {}

    def dfs(pos, visited, steps):
        if steps > limit or steps >= best[0]:
            return
        key = (pos, visited)
        if seen.get(key, 10**9) <= steps:
            return
        seen[key] = steps
        if pos == (0, m - 1):
            total = steps + stanley(set(visited))
            best[0] = min(best[0], total)
        for q in neigh(pos):
            dfs(q, visited | {q}, steps + 1)

    start = (n - 1, 0)
    dfs(start, frozenset({start}), 0)
    return best[0]


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        out.append(solve(n, m))
    print("\n".join(map(str, out)))


main()
