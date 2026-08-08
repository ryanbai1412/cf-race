"""Independent brute force: BFS over states for tiny arrays."""
import sys
from collections import deque
from itertools import combinations


def bfs(a):
    start = tuple(a)
    if len(set(start)) == 1:
        return 0
    lim = max(a) + max(a) - min(a)
    seen = {start}
    q = deque([(start, 0)])
    while q:
        st, d = q.popleft()
        n = len(st)
        for k in range(1, n + 1):
            for idxs in combinations(range(n), k):
                nxt = list(st)
                for i in idxs:
                    nxt[i] += 1
                if max(nxt) > lim:
                    continue
                tnxt = tuple(nxt)
                if len(set(tnxt)) == 1:
                    return d + 1
                if tnxt not in seen:
                    seen.add(tnxt)
                    q.append((tnxt, d + 1))
    raise AssertionError


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        print(bfs(a))


main()
