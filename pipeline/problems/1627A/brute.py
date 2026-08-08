"""Independent brute force: BFS over grid states applying real operations."""
import sys
from collections import deque


def solve(n, m, r, c, grid):
    start = tuple(grid)
    if start[r - 1][c - 1] == "B":
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        st, d = q.popleft()
        for i in range(n):
            for j in range(m):
                if st[i][j] != "B":
                    continue
                # paint row i
                nxt = list(st)
                nxt[i] = "B" * m
                tn = tuple(nxt)
                if tn[r - 1][c - 1] == "B":
                    return d + 1
                if tn not in seen:
                    seen.add(tn)
                    q.append((tn, d + 1))
                # paint column j
                nxt = [row[:j] + "B" + row[j + 1 :] for row in st]
                tn = tuple(nxt)
                if tn[r - 1][c - 1] == "B":
                    return d + 1
                if tn not in seen:
                    seen.add(tn)
                    q.append((tn, d + 1))
    return -1


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n, m, r, c = (int(x) for x in data[idx : idx + 4])
        idx += 4
        grid = data[idx : idx + n]
        idx += n
        print(solve(n, m, r, c, grid))


main()
