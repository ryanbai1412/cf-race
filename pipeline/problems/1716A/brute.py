"""BFS brute force on the line for small n."""
import sys
from collections import deque


def solve(n):
    lo, hi = -80, n + 80
    dist = {0: 0}
    q = deque([0])
    while q:
        x = q.popleft()
        if x == n:
            return dist[x]
        for d in (-3, -2, 2, 3):
            y = x + d
            if lo <= y <= hi and y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    raise AssertionError


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    print("\n".join(str(solve(int(data[i]))) for i in range(1, t + 1)))


main()
