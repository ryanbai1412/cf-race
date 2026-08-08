"""Independent solution: exhaustive search over subsets of walls for tiny grids.
Breaks walls (internal + perimeter) and checks every cell can reach the outside;
returns the minimum number of broken walls found.
"""
import sys
from itertools import combinations


def walls(a, b):
    out = []
    outside = (-1, -1)
    for i in range(a):
        for j in range(b):
            if i + 1 < a:
                out.append(((i, j), (i + 1, j)))
            if j + 1 < b:
                out.append(((i, j), (i, j + 1)))
            if i == 0:
                out.append(((i, j), outside))
            if i == a - 1:
                out.append(((i, j), outside))
            if j == 0:
                out.append(((i, j), outside))
            if j == b - 1:
                out.append(((i, j), outside))
    return out


def ok(a, b, chosen):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in chosen:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    root = find((-1, -1))
    return all(find((i, j)) == root for i in range(a) for j in range(b))


def solve(a, b):
    ws = walls(a, b)
    for k in range(a * b + 1):
        for chosen in combinations(ws, k):
            if ok(a, b, chosen):
                return k
    return -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 2 * i]); b = int(data[2 + 2 * i])
        out.append(str(solve(a, b)))
    sys.stdout.write("\n".join(out) + "\n")


main()
