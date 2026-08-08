"""Independent brute force: BFS over |a-b| for small differences."""
import sys
from collections import deque


def bfs(d):
    # min moves to reduce difference d to 0 using steps 1..10
    dist = {0: 0}
    q = deque([0])
    while q:
        cur = q.popleft()
        if cur == d:
            return dist[cur]
        for k in range(1, 11):
            for nxt in (cur + k, cur - k):
                if 0 <= nxt <= d + 20 and nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)
    return dist[d]


def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        a = int(data[1 + 2 * i]); b = int(data[2 + 2 * i])
        out.append(str(bfs(abs(a - b))))
    print("\n".join(out))


main()
