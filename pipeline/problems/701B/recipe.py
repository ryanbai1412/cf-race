from genlib import *  # noqa: F401,F403

CHECKER = "m integers (64-bit); unique, exact token comparison."
STATEMENT = "Legend (cells not attacked after each rook), input (1<=n<=1e5, 1<=m<=min(1e5,n^2), distinct cells), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    rows, cols, out = set(), set(), []
    for i in range(m):
        rows.add(v[2 + 2 * i])
        cols.add(v[3 + 2 * i])
        out.append((n - len(rows)) * (n - len(cols)))
    return " ".join(map(str, out)) + "\n"


def make(g, n, m):
    m = min(m, n * n)
    cells = set()
    while len(cells) < m:
        cells.add((g.randint(1, n), g.randint(1, n)))
    cells = list(cells)
    g.shuffle(cells)
    return fmt([n, m], *cells)


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=m=1", fmt([1, 1], [1, 1])), ("boundary", "n=2 fill board", fmt([2, 4], [1, 1], [1, 2], [2, 1], [2, 2])),
           ("adversarial", "same row repeated", fmt([5, 3], [2, 1], [2, 3], [2, 5])),
           ("maxSize", "n=1e5 m=1 (answer ~1e10, 64-bit)", fmt([N, 1], [N, N])), ("maxSize", "n=1e5 m=1e5 diagonal", fmt([N, N], *[[i, i] for i in range(1, N + 1)])),
           ("maxSize", "n=1e5 m=1e5 random", make(g, N, N)), ("maxSize", "n=316 m=99856 full board", make(g, 316, 316 * 316))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 5)), g.randint(1, n * n)), 100, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(6, N), g.randint(1, 3000)), 30)
    return out
