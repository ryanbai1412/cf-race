from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (simplify prepared problems), input (1<=n,m<=3000, a strictly increasing, b non-decreasing, values<=1e6), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    a, b = v[2:2 + n], v[2 + n:]
    j = matched = 0
    for x in a:
        while j < m and b[j] < x:
            j += 1
        if j < m:
            matched += 1
            j += 1
    return f"{n - matched}\n"


def make(g, n, m, hi=10 ** 6):
    hi = max(hi, n)
    return fmt([n, m], sorted(g.sample(range(1, hi + 1), n)), sorted(g.randint(1, hi) for _ in range(m)))


def cases(g):
    M = 10 ** 6
    out = [("boundary", "n=m=1 equal", fmt([1, 1], [1], [1])), ("boundary", "n=m=1 too simple prepared", fmt([1, 1], [M], [M - 1])),
           ("adversarial", "one large b must not cover several a", fmt([3, 1], [1, 2, 3], [M])),
           ("adversarial", "all b too small", fmt([3, 5], [10, 20, 30], [1, 2, 3, 4, 9])),
           ("maxSize", "n=m=3000 values up to 1e6", make(g, 3000, 3000)),
           ("maxSize", "n=3000 m=1 (answer n-1 or n)", make(g, 3000, 1)),
           ("maxSize", "n=1 m=3000", make(g, 1, 3000))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 8), 12), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 3000), g.randint(1, 3000)), 30)
    return out
