from genlib import *  # noqa: F401,F403
from itertools import accumulate

CHECKER = "m integers, one per question; unique, exact token comparison."
STATEMENT = "Legend defines both question types, input (1<=n,m<=1e5, 1<=vi<=1e9, 1<=l<=r<=n), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    a = v[1:1 + n]
    p = [0, *accumulate(a)], [0, *accumulate(sorted(a))]
    q = v[2 + n:]
    return "".join(f"{p[q[i] - 1][q[i + 2]] - p[q[i] - 1][q[i + 1] - 1]}\n" for i in range(0, len(q), 3))


def query(g, n):
    l = g.randint(1, n)
    return [g.randint(1, 2), l, g.randint(l, n)]


def make(g, n, m, hi=10 ** 9):
    return fmt(n, [g.randint(1, hi) for _ in range(n)], m, *[query(g, n) for _ in range(m)])


def cases(g):
    B = 10 ** 9
    out = [("boundary", "n=m=1 type 1", fmt(1, [5], 1, [1, 1, 1])), ("boundary", "n=m=1 type 2", fmt(1, [B], 1, [2, 1, 1])),
           ("adversarial", "unsorted vs sorted differ", fmt(3, [3, 1, 2], 2, [1, 1, 1], [2, 1, 1])),
           ("maxSize", "n=m=1e5 all 1e9, full ranges (64-bit sums)", fmt(100000, [B] * 100000, 100000, *[[1 + i % 2, 1, 100000] for i in range(100000)])),
           ("maxSize", "n=1e5 random values, m=2e4", make(g, 100000, 20000))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), g.randint(1, 10), 20), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 500), g.randint(1, 500)), 30, reason="medium random")
    return out
