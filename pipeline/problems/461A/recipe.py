from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend defines splitting game, input (1<=n<=3e5, 1<=ai<=1e6), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    a = sorted(v[1:])
    return f"{sum(x * min(i + 2, n) for i, x in enumerate(a))}\n"


def arr(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    M = 10 ** 6
    out = [("boundary", "n=1", fmt(1, [10])), ("boundary", "n=2", fmt(2, [1, M])),
           ("adversarial", "all equal", fmt(5, [7] * 5)), ("adversarial", "descending input", fmt(6, [6, 5, 4, 3, 2, 1])),
           ("maxSize", "n=3e5 all 1e6 (answer > 4e16)", fmt(300000, [M] * 300000)),
           ("maxSize", "n=3e5 random", arr(g, 300000, M))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), 20), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000), M), 30, reason="medium random")
    return out
