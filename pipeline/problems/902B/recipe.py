from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (subtree painting, minimum steps), input (2<=n<=1e4, 1<=pi<i, 1<=ci<=n), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    p = [0, 0] + v[1:n]
    c = [0] + v[n:2 * n]
    return f"{1 + sum(c[i] != c[p[i]] for i in range(2, n + 1))}\n"


def make(g, n, colors):
    return fmt(n, [g.randint(max(1, i - 3) if g.random() < 0.5 else 1, i - 1) for i in range(2, n + 1)], [g.randint(1, min(colors, n)) for _ in range(n)])


def cases(g):
    N = 10 ** 4
    out = [("boundary", "n=2 same", fmt(2, [1], [1, 1])), ("boundary", "n=2 differ", fmt(2, [1], [2, 1])),
           ("maxSize", "n=1e4 chain alternating", fmt(N, list(range(1, N)), [1 + i % 2 for i in range(N)])),
           ("maxSize", "n=1e4 star", fmt(N, [1] * (N - 1), list(range(1, N + 1)))), ("maxSize", "n=1e4 random", make(g, N, N)),
           ("adversarial", "all same colour", fmt(5, [1, 1, 2, 3], [4, 4, 4, 4, 4]))]
    out += fill(g, lambda g: make(g, g.randint(2, 8), 3), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.randint(1, 5)), 25)
    return out
