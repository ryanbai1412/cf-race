from genlib import *  # noqa: F401,F403
from itertools import permutations

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (2x2 sliding puzzle reachability), input (two 2x2 grids each with A, B, C, X once), output present."
ALL = ["".join(p) for p in permutations("ABCX")]


def cyc(a, b):
    order = (a[0] + a[1] + b[1] + b[0]).replace("X", "")
    i = order.index("A")
    return order[i:] + order[:i]


def solve(s):
    t = s.split()
    return "YES\n" if cyc(t[0], t[1]) == cyc(t[2], t[3]) else "NO\n"


def grid(p):
    return [p[:2], p[2:]]


def cases(g):
    out = [("boundary", "identical puzzles", fmt("AB", "CX", "AB", "CX")), ("boundary", "X in every corner same cycle", fmt("XA", "CB", "AB", "XC")),
           ("adversarial", "mirror image (NO)", fmt("AB", "CX", "AC", "BX")),
           ("maxSize", "all 24 tiles positions, first vs last", fmt(*grid(ALL[0]), *grid(ALL[-1])))]
    out += fill(g, lambda g: fmt(*grid(g.choice(ALL)), *grid(g.choice(ALL))), 130)
    return out
