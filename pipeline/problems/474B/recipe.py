from genlib import *  # noqa: F401,F403
from bisect import bisect_left

CHECKER = "m pile indices; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n<=1e5, 1<=ai<=1e3, sum<=1e6, 1<=m<=1e5, 1<=qi<=sum), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    pref, t = [], 0
    for a in v[1:1 + n]:
        t += a
        pref.append(t)
    return "".join(f"{bisect_left(pref, q) + 1}\n" for q in v[2 + n:])


def make(g, n, m, hi=1000):
    a = [g.randint(1, hi) for _ in range(n)]
    while sum(a) > 10 ** 6:
        a = [max(1, x // 2) for x in a]
    total = sum(a)
    return fmt(n, a, m, [g.randint(1, total) for _ in range(m)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=m=1", fmt(1, [1], 1, [1])), ("boundary", "queries at pile ends", fmt(3, [2, 1, 3], 4, [2, 3, 4, 6])),
           ("maxSize", "n=1e5 piles of 10 (sum 1e6), m=1e5 at sum", fmt(N, [10] * N, N, [10 ** 6] * N)),
           ("maxSize", "n=1000 piles of 1000, m=1e5 random", make(g, 1000, N)), ("maxSize", "n=1e5 random, m=1e5", make(g, N, N, 10)),
           ("adversarial", "all piles size 1", fmt(5, [1] * 5, 5, [5, 4, 3, 2, 1]))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 6), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 2000), g.randint(1, 2000)), 30)
    return out
