from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (two continuous sectors, minimal difference), input (1<=n<=360, 1<=ai<=360, sum 360), output present."


def solve(s):
    a = ints(s)[1:]
    n, best = len(a), 360
    for i in range(n):
        t = 0
        for j in range(n):
            t += a[(i + j) % n]
            best = min(best, abs(360 - 2 * t))
    return f"{best}\n"


def split(g, parts):
    cuts = sorted(g.sample(range(1, 360), parts - 1))
    return [b - a for a, b in zip([0] + cuts, cuts + [360])]


def cases(g):
    out = [("boundary", "n=1", fmt(1, [360])), ("boundary", "n=2 halves", fmt(2, [180, 180])),
           ("adversarial", "one huge piece", fmt(2, [359, 1])), ("adversarial", "wraparound best", fmt(4, [170, 30, 150, 10])),
           ("maxSize", "n=360", fmt(360, [1] * 360))]
    out += fill(g, lambda g: fmt((p := g.randint(1, 8)), split(g, p)), 90, reason="small random")
    out += fill(g, lambda g: fmt((p := g.randint(9, 359)), split(g, p)), 25)
    return out
