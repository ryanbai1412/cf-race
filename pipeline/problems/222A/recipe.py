from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer or -1; unique, exact token comparison."
STATEMENT = "Legend (append k-th, delete first), input (1<=k<=n<=1e5, 1<=ai<=1e5), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a = v[2:]
    if any(x != a[k - 1] for x in a[k - 1:]):
        return "-1\n"
    i = k - 1
    while i > 0 and a[i - 1] == a[k - 1]:
        i -= 1
    return f"{i}\n"


def make(g, n, k, hi, tail=True):
    a = [g.randint(1, hi) for _ in range(n)]
    if tail:
        for i in range(k - 1, n):
            a[i] = a[k - 1]
    return fmt([n, k], a)


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=k=1", fmt([1, 1], [5])), ("boundary", "k=n", fmt([3, 3], [1, 2, 3])),
           ("adversarial", "k=1 not all equal (-1)", fmt([3, 1], [3, 1, 1])),
           ("adversarial", "already all equal (0)", fmt([4, 2], [7, 7, 7, 7])),
           ("maxSize", "n=1e5 k=1e5 distinct prefix", fmt([N, N], list(range(1, N + 1)))),
           ("maxSize", "n=1e5 k=1 all equal", fmt([N, 1], [N] * N)),
           ("maxSize", "n=1e5 k=5e4 tail equal", make(g, N, N // 2, N))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 8)), g.randint(1, n), 3, g.random() < 0.7), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 3000)), g.randint(1, n), g.choice([2, N]), g.random() < 0.8), 30)
    return out
