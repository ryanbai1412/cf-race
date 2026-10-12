from genlib import *  # noqa: F401,F403

CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (hexagon with sides a,b,c,a,b,c), input (2<=a,b,c<=1000), output present."


def solve(s):
    a, b, c = ints(s)
    return f"{a * b + b * c + c * a - a - b - c + 1}\n"


def cases(g):
    out = [("boundary", "all minimal", fmt([2, 2, 2])), ("boundary", "one side minimal", fmt([2, 1000, 1000])),
           ("adversarial", "two sides minimal", fmt([1000, 2, 2])), ("adversarial", "permuted sides", fmt([3, 2, 1000])),
           ("maxSize", "all maximal", fmt([1000, 1000, 1000])), ("maxSize", "near maximal", fmt([999, 1000, 998]))]
    out += fill(g, lambda g: fmt([g.randint(2, 1000) for _ in range(3)]), 70)
    out += fill(g, lambda g: fmt([g.randint(2, 10) for _ in range(3)]), 50, reason="small sides")
    return out
