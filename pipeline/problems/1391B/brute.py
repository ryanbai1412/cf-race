"""Independent solution: brute force over small grids.

Tries every subset of changed cells (by increasing size) and simulates luggage
from every cell to check functionality. Only usable for tiny grids.
"""
import itertools
import sys


def functional(g, n, m):
    for si in range(n):
        for sj in range(m):
            i, j = si, sj
            for _ in range(n + m + 2):
                if (i, j) == (n - 1, m - 1):
                    break
                if g[i][j] == "R":
                    j += 1
                else:
                    i += 1
                if i >= n or j >= m:
                    break
            else:
                return False
            if (i, j) != (n - 1, m - 1):
                return False
    return True


def solve(g, n, m):
    cells = [(i, j) for i in range(n) for j in range(m) if (i, j) != (n - 1, m - 1)]
    for k in range(len(cells) + 1):
        for sub in itertools.combinations(cells, k):
            h = [row[:] for row in g]
            for i, j in sub:
                h[i][j] = "D" if h[i][j] == "R" else "R"
            if functional(h, n, m):
                return k
    return -1


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        g = [list(next(it)) for _ in range(n)]
        out.append(str(solve(g, n, m)))
    sys.stdout.write("\n".join(out) + "\n")


main()
