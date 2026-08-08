"""Independent solution: search for a permutation whose merge yields a.

Greedy-free check: p must be a permutation of 1..n; verify by trying to split
`a` into two identical subsequences equal to p, using DP over candidate p.
Only used for stress testing on tiny n.
"""
import itertools
import sys


def is_merge(a, p):
    """Can a be split into two subsequences both equal to p?"""
    n = len(p)
    # dp over (i, j) = how many of p matched by copy1 / copy2
    states = {(0, 0)}
    for x in a:
        nxt = set()
        for i, j in states:
            if i < n and p[i] == x:
                nxt.add((i + 1, j))
            if j < n and p[j] == x:
                nxt.add((i, j + 1))
        states = nxt
        if not states:
            return False
    return (n, n) in states


def solve(a, n):
    for p in itertools.permutations(range(1, n + 1)):
        if is_merge(a, list(p)):
            return list(p)
    return None


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(2 * n)]
        out.append(" ".join(map(str, solve(a, n))))
    sys.stdout.write("\n".join(out) + "\n")


main()
