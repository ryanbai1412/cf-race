from genlib import *  # noqa: F401,F403

CHECKER = "Single maximal integer; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n<=100, 1<=ai<=100), output present in the pinned source row."


def solve(s):
    a = ints(s)[1:]
    t = sum(a)
    if t % 2:
        return f"{t}\n"
    odd = [x for x in a if x % 2]
    return f"{t - min(odd)}\n" if odd else "0\n"


def arr(g, n, lo=1, hi=100, parity=None):
    v = [g.randint(lo, hi) for _ in range(n)]
    if parity is not None:
        v = [x - (x % 2 != parity) if x > 1 else (1 if parity else 2) for x in v]
    return fmt(n, v)


def cases(g):
    out = [("boundary", "single odd flower", fmt(1, [1])), ("boundary", "single even flower (answer 0)", fmt(1, [2])),
           ("boundary", "single flower 100", fmt(1, [100])),
           ("adversarial", "all even (answer 0)", fmt(100, [100] * 100)),
           ("adversarial", "even total with several odd, drop smallest odd", fmt(4, [99, 3, 5, 7])),
           ("adversarial", "two odd equal to max", fmt(2, [99, 99])),
           ("maxSize", "n=100 all 100 except one 99", fmt(100, [100] * 99 + [99])),
           ("maxSize", "n=100 all 99 (even count, drop one)", fmt(100, [99] * 100)),
           ("maxSize", "n=100 random", arr(g, 100))]
    out += fill(g, lambda g: arr(g, g.randint(1, 100)), 60)
    out += fill(g, lambda g: arr(g, g.randint(1, 10), parity=0), 20, reason="all even")
    out += fill(g, lambda g: arr(g, g.randint(2, 10), 1, 9), 30, reason="small values")
    return out
