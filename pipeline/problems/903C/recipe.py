from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (nest strictly smaller boxes), input (1<=n<=5000, 1<=ai<=1e9), output present."


def solve(s):
    a = ints(s)[1:]
    return f"{max(a.count(x) for x in set(a))}\n"


def make(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1", fmt(1, [10 ** 9])), ("boundary", "all equal", fmt(4, [7] * 4)),
           ("adversarial", "distinct", fmt(3, [1, 2, 3])), ("maxSize", "n=5000 all equal", fmt(5000, [10 ** 9] * 5000)),
           ("maxSize", "n=5000 distinct", fmt(5000, list(range(1, 5001)))), ("maxSize", "n=5000 random", make(g, 5000, 50))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 5000), g.choice([3, 100, 10 ** 9])), 25)
    return out
