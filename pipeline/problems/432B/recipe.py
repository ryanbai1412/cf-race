from genlib import *  # noqa: F401,F403

CHECKER = "n lines of two integers in input order; unique, exact token comparison."
STATEMENT = "Legend (away team switches to home kit on colour clash), input (2<=n<=1e5, 1<=xi,yi<=1e5, xi!=yi), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    xs, ys = v[1::2], v[2::2]
    cnt = {}
    for x in xs:
        cnt[x] = cnt.get(x, 0) + 1
    return "".join(f"{n - 1 + cnt.get(y, 0)} {n - 1 - cnt.get(y, 0)}\n" for y in ys)


def team(g, hi):
    x = g.randint(1, hi)
    y = g.randint(1, hi - 1)
    return [x, y + (y >= x)]


def make(g, n, hi):
    return fmt(n, *[team(g, hi) for _ in range(n)])


def cases(g):
    M = 10 ** 5
    out = [("boundary", "n=2 swapped kits", fmt(2, [1, 2], [2, 1])), ("boundary", "n=2 no clashes", fmt(2, [1, 2], [3, 4])),
           ("adversarial", "every away colour equals every other home colour", fmt(4, [1, 2], [1, 2], [1, 2], [1, 2])),
           ("adversarial", "colours at max value", fmt(3, [M, M - 1], [M - 1, M], [M, 1])),
           ("maxSize", "n=1e5 all home colour 1, away 2 (64-bit safe)", fmt(M, *[[1, 2]] * M)),
           ("maxSize", "n=1e5 random colours", make(g, M, M))]
    out += fill(g, lambda g: make(g, g.randint(2, 10), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(2, 1000), g.randint(2, 100)), 30, reason="medium random")
    return out
