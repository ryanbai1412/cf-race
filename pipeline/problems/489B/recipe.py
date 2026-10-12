from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (pair skills differ by at most one), input (1<=n,m<=100, skills 1..100), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    a = sorted(v[1:1 + n])
    b = sorted(v[2 + n:])
    i = j = k = 0
    while i < len(a) and j < len(b):
        if abs(a[i] - b[j]) <= 1:
            k += 1
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return f"{k}\n"


def make(g, n, m, hi=100):
    return fmt(n, [g.randint(1, hi) for _ in range(n)], m, [g.randint(1, hi) for _ in range(m)])


def cases(g):
    out = [("boundary", "n=m=1 equal", fmt(1, [1], 1, [1])), ("boundary", "n=m=1 differ by 2", fmt(1, [1], 1, [3])),
           ("adversarial", "greedy order matters", fmt(2, [2, 3], 2, [1, 2])),
           ("adversarial", "chain 1 2 3 vs 2 3 4", fmt(3, [1, 2, 3], 3, [2, 3, 4])),
           ("maxSize", "n=m=100 all equal", fmt(100, [50] * 100, 100, [50] * 100)),
           ("maxSize", "n=m=100 random", make(g, 100, 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 8), 10), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100)), 30)
    return out
