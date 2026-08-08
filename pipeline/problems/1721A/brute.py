"""BFS brute force over pixel states with the literal move rule."""
import sys
from collections import deque


def solve(px):
    alphabet = sorted(set(px) | {"z" if "z" not in px else "a"})
    start = tuple(px)
    if len(set(start)) == 1:
        return 0
    dist = {start: 0}
    q = deque([start])
    while q:
        st = q.popleft()
        d = dist[st]
        # choose 1 or 2 pixels of the same color, paint to another color
        subsets = []
        for i in range(4):
            subsets.append((i,))
            for j in range(i + 1, 4):
                if st[i] == st[j]:
                    subsets.append((i, j))
        for sub in subsets:
            cur = st[sub[0]]
            for c in alphabet:
                if c == cur:
                    continue
                nxt = list(st)
                for i in sub:
                    nxt[i] = c
                nxt = tuple(nxt)
                if nxt not in dist:
                    dist[nxt] = d + 1
                    if len(set(nxt)) == 1:
                        return d + 1
                    q.append(nxt)
    raise AssertionError


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[1 + 2 * i] + data[2 + 2 * i]
        out.append(solve(list(s)))
    print("\n".join(map(str, out)))


main()
