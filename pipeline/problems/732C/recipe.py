from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (arrival/departure any meal boundary, minimise missed meals), input (0<=b,d,s<=1e18, b+d+s>=1), output present."


def solve(s):
    v = ints(s)
    m = max(v)
    return f"{sum(max(0, m - 1 - x) for x in v)}\n"


def cases(g):
    E = 10 ** 18
    out = [("boundary", "1 0 0", fmt([1, 0, 0])), ("boundary", "0 0 1", fmt([0, 0, 1])), ("boundary", "all max", fmt([E, E, E])),
           ("adversarial", "max with zeros", fmt([E, 0, 0])), ("adversarial", "differ by one", fmt([E, E - 1, E - 1])), ("adversarial", "0 1 1", fmt([0, 1, 1])),
           ("maxSize", "max 0 max", fmt([E, 0, E]))]
    out += fill(g, lambda g: fmt([g.randint(0, 4) for _ in range(3)]), 60, reason="small random")
    out += fill(g, lambda g: fmt([g.randint(0, E) for _ in range(3)]), 30)
    out += fill(g, lambda g: fmt([(b := g.randint(1, E)) - g.randint(0, 2) for _ in range(3)]), 25, reason="near-equal large")
    return [c for c in out if sum(ints(c[2])) >= 1]
