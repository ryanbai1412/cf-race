from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum valid TL or -1; unique, exact token comparison."
STATEMENT = "Legend lists all TL conditions incl. minimality, input (1<=n,m<=100, 1<=ai,bi<=100), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    a, b = v[2:2 + n], v[2 + n:]
    t = max(2 * min(a), max(a))
    return f"{t if t < min(b) else -1}\n"


def make(g, n, m, hi=100):
    return fmt([n, m], [g.randint(1, hi) for _ in range(n)], [g.randint(1, hi) for _ in range(m)])


def cases(g):
    out = [("boundary", "n=m=1 minimal values", fmt([1, 1], [1], [1])), ("boundary", "n=m=1 valid", fmt([1, 1], [1], [3])),
           ("adversarial", "TL equals a wrong solution time (-1)", fmt([2, 1], [3, 5], [6])),
           ("adversarial", "max(a) exceeds 2*min(a)", fmt([3, 2], [2, 9, 3], [10, 11])),
           ("adversarial", "2*min(a) exceeds max(a)", fmt([3, 2], [40, 41, 42], [81, 90])),
           ("maxSize", "n=m=100 all 100 (-1)", fmt([100, 100], [100] * 100, [100] * 100)),
           ("maxSize", "n=m=100 valid answer", fmt([100, 100], [g.randint(25, 50) for _ in range(100)], [g.randint(51, 100) * 0 + 100 for _ in range(100)]))]
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100)), 50)
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), 20), 70, reason="small random")
    return out
