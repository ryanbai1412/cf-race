from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (rearrange to maximize increasing neighbours), input (1<=n<=1000, 1<=ai<=1000), output present."


def solve(s):
    v = ints(s)
    a = v[1:]
    return f"{len(a) - max(a.count(x) for x in set(a))}\n"


def make(g, n, hi=1000):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1", fmt(1, [1000])), ("boundary", "all equal (0)", fmt(3, [5, 5, 5])),
           ("adversarial", "dominant duplicate", fmt(6, [2, 2, 2, 1, 3, 2])),
           ("maxSize", "n=1000 distinct", fmt(1000, list(range(1000, 0, -1)))), ("maxSize", "n=1000 values 1..2", make(g, 1000, 2)),
           ("maxSize", "n=1000 random", make(g, 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 1000), g.randint(1, 1000)), 30)
    return out
