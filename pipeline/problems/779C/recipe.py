from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (buy at least k now, minimise total), input (1<=n<=2e5, 0<=k<=n, 1<=ai,bi<=1e4), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a, b = v[2:2 + n], v[2 + n:2 + 2 * n]
    d = sorted(x - y for x, y in zip(a, b))
    return f"{sum(b) + sum(x for i, x in enumerate(d) if i < k or x < 0)}\n"


def make(g, n, k=None, hi=10 ** 4):
    return fmt([n, g.randint(0, n) if k is None else k], [g.randint(1, hi) for _ in range(n)], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 2 * 10 ** 5
    out = [("boundary", "n=1 k=0", fmt([1, 0], [5], [3])), ("boundary", "n=1 k=1", fmt([1, 1], [5], [3])),
           ("adversarial", "k=n all now cheaper later", fmt([3, 3], [10, 10, 10], [1, 1, 1])), ("adversarial", "k=0 all cheaper now", fmt([3, 0], [1, 1, 1], [9, 9, 9])),
           ("maxSize", "n=2e5 k=n max", fmt([N, N], [10 ** 4] * N, [1] * N)), ("maxSize", "n=2e5 random", make(g, N)), ("maxSize", "n=2e5 k=0", make(g, N, 0))]
    out += fill(g, lambda g: make(g, g.randint(1, 7), None, 8), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(8, 3000)), 25)
    return out
