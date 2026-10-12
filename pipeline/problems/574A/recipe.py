from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend, input (2<=n<=100, 1<=ai<=1000), output present."


def solve(s):
    v = ints(s)[1:]
    me, rest = v[0], v[1:]
    k = 0
    while me <= max(rest):
        i = rest.index(max(rest))
        rest[i] -= 1
        me += 1
        k += 1
    return f"{k}\n"


def cases(g):
    out = [("boundary", "n=2 already winning", fmt(2, [2, 1])), ("boundary", "n=2 tie", fmt(2, [1, 1])),
           ("adversarial", "Limak minimal, all others equal maximal", fmt(100, [1] + [1000] * 99)),
           ("adversarial", "one huge opponent", fmt(3, [1, 1000, 1])),
           ("maxSize", "n=100 all 1000", fmt(100, [1000] * 100)), ("maxSize", "n=100 random", fmt(100, [g.randint(1, 1000) for _ in range(100)]))]
    out += fill(g, lambda g: (lambda n: fmt(n, [g.randint(1, 1000) for _ in range(n)]))(g.randint(2, 100)), 60)
    out += fill(g, lambda g: (lambda n: fmt(n, [g.randint(1, 10) for _ in range(n)]))(g.randint(2, 8)), 60, reason="small")
    return out
