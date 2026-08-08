"""Independent brute force: try every k-colouring of the conflict graph for
small n (k = 1, then 2, ...), where i~j iff |a_i - a_j| = 1."""
import itertools
import sys


def solve(a):
    n = len(a)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)
             if abs(a[i] - a[j]) == 1]
    for k in range(1, n + 1):
        for colors in itertools.product(range(k), repeat=n):
            if all(colors[i] != colors[j] for i, j in edges):
                return k
    return n


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    q = int(data[p])
    p += 1
    out = []
    for _ in range(q):
        n = int(data[p])
        p += 1
        a = list(map(int, data[p:p + n]))
        p += n
        out.append(solve(a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
