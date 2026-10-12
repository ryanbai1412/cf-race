from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (start next to computer 1, crack when holding >= ai pieces), input (1<=n<=1000, 0<=ai<n, solvable), output present."


def sweeps(a):
    n, have, done, k = len(a), 0, [False] * len(a), 0
    order = list(range(n))
    while have < n:
        before = have
        for i in order:
            if not done[i] and a[i] <= have:
                done[i] = True
                have += 1
        if have == before:
            return None
        k += 1
        order.reverse()
    return k - 1


def solve(s):
    return f"{sweeps(ints(s)[1:])}\n"


def make(g, n, hi=None):
    while True:
        a = [g.randint(0, (n - 1) if hi is None else min(hi, n - 1)) for _ in range(n)]
        if sweeps(a) is not None:
            return fmt(n, a)


def cases(g):
    out = [("boundary", "n=1", fmt(1, [0])), ("boundary", "n=2 second needs 1", fmt(2, [0, 1])),
           ("adversarial", "must return to left end", fmt(3, [0, 2, 0])),
           ("adversarial", "zig-zag every sweep", fmt(5, [4, 2, 3, 0, 1])),
           ("maxSize", "n=1000 strictly increasing requirements", fmt(1000, list(range(1000)))),
           ("maxSize", "n=1000 maximal zig-zag", fmt(1000, [n for pair in zip(range(1, 1000, 2), range(0, 1000, 2)) for n in pair][::-1])),
           ("maxSize", "n=1000 random solvable", make(g, 1000))]
    out += fill(g, lambda g: make(g, g.randint(4, 12)), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 1000)), g.randint(0, n)), 30)
    return out
