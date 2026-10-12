from genlib import *  # noqa: F401,F403

CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (cut into two non-empty pieces), input (1<=n<=1e5, |ai|<=1e4), output present."


def solve(s):
    v = ints(s)
    a = v[1:]
    t, p, c = sum(a), 0, 0
    for x in a[:-1]:
        p += x
        c += 2 * p == t
    return f"{c}\n"


def arr(g, n, hi):
    return fmt(n, [g.randint(-hi, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 (0 cuts)", fmt(1, [5])), ("boundary", "n=2 equal", fmt(2, [-10000, -10000])),
           ("adversarial", "all zeros (n-1 cuts)", fmt(8, [0] * 8)), ("adversarial", "odd total", fmt(3, [1, 1, 1])),
           ("maxSize", "n=1e5 all zeros", fmt(100000, [0] * 100000)), ("maxSize", "n=1e5 random", arr(g, 100000, 10000)),
           ("maxSize", "n=1e5 alternating +-1e4", fmt(100000, [10000 * (-1) ** i for i in range(100000)]))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), 2), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000), g.choice([1, 10000])), 30)
    return out
