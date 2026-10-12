from genlib import *  # noqa: F401,F403

CHECKER = "Single integer digit count; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n<=1e9), output present."


def solve(s):
    n = int(s)
    total, d, start = 0, 1, 1
    while start <= n:
        total += (min(n, start * 10 - 1) - start + 1) * d
        d += 1
        start *= 10
    return f"{total}\n"


def cases(g):
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=9", fmt(9)), ("boundary", "n=10", fmt(10)),
           ("adversarial", "n=99999999", fmt(99999999)), ("adversarial", "n=100000000", fmt(100000000)),
           ("maxSize", "n=1e9 maximum", fmt(10 ** 9)), ("maxSize", "n=999999999", fmt(999999999))]
    out += [("random", "power of ten boundary", fmt(10 ** k + dlt)) for k in range(1, 9) for dlt in (-1, 1)]
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** 9)), 70)
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** g.randint(1, 8))), 40, reason="random magnitude")
    return out
