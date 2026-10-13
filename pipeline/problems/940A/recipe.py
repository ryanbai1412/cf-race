from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (remove min points for diameter <= d), input (1<=n<=100, 0<=d<=100, 1<=xi<=100), output present."


def solve(s):
    v = ints(s)
    n, d = v[0], v[1]
    x = v[2:2 + n]
    return f"{n - max(sum(lo <= y <= lo + d for y in x) for lo in x)}\n"


def make(g, n, d, hi=100):
    return fmt([n, d], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1", fmt([1, 0], [100])), ("boundary", "d=0 duplicates", fmt([4, 0], [5, 5, 6, 5])), ("boundary", "d=100", make(g, 100, 100)),
           ("adversarial", "spread extremes d=98", fmt([3, 98], [1, 100, 2])), ("maxSize", "n=100 d=0 random", make(g, 100, 0)),
           ("maxSize", "n=100 d=50", make(g, 100, 50))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(0, 5), 10), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 100), g.randint(0, 100)), 25)
    return out
