"""Independent brute force: BFS from (r,c) on small grids, take max distance."""
import sys
from collections import deque


def brute(n, m, r, c):
    dist = [[-1] * m for _ in range(n)]
    dist[r - 1][c - 1] = 0
    q = deque([(r - 1, c - 1)])
    best = 0
    while q:
        i, j = q.popleft()
        best = max(best, dist[i][j])
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and dist[ni][nj] < 0:
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))
    return best


def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        n, m, r, c = map(int, data[1 + 4 * i:5 + 4 * i])
        out.append(str(brute(n, m, r, c)))
    print("\n".join(out))


main()
