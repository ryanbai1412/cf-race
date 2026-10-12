from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (per-chapter time decreases by one per subject, never below 1), input (1<=n,x<=1e5, 1<=ci<=1e5), output present."


def solve(s):
    v = ints(s)
    n, x = v[0], v[1]
    total = 0
    for c in sorted(v[2:]):
        total += c * x
        x = max(1, x - 1)
    return f"{total}\n"


def make(g, n, x, hi=10 ** 5):
    return fmt([n, x], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=x=1", fmt([1, 1], [1])), ("boundary", "x=1 floor already", make(g, 5, 1, 10)),
           ("adversarial", "sorting matters", fmt([3, 3], [100, 1, 50])),
           ("maxSize", "n=x=1e5, ci=1e5 (answer ~5e14, 64-bit)", fmt([N, N], [N] * N)), ("maxSize", "n=1e5 x=1e5 random", make(g, N, N)),
           ("maxSize", "n=1e5 x=1", make(g, N, 1))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 8), 10), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 3000), g.randint(1, N)), 30)
    return out
