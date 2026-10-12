from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (raise factors by 1 per coin until distinct), input (1<=n<=3000, 1<=ai<=n), output present."


def solve(s):
    v = ints(s)
    cost, nxt = 0, 0
    for a in sorted(v[1:]):
        nxt = max(nxt, a)
        cost += nxt - a
        nxt += 1
    return f"{cost}\n"


def make(g, n, hi=None):
    return fmt(n, [g.randint(1, hi or n) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1", fmt(1, [1])), ("boundary", "already distinct", fmt(3, [3, 1, 2])),
           ("adversarial", "all equal n", fmt(4, [4, 4, 4, 4])),
           ("maxSize", "n=3000 all 3000 (max cost)", fmt(3000, [3000] * 3000)), ("maxSize", "n=3000 all 1", fmt(3000, [1] * 3000)),
           ("maxSize", "n=3000 random", make(g, 3000))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 8)), g.randint(1, n)), 100, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000)), 30)
    return out
