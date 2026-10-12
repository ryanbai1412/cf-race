from genlib import *  # noqa: F401,F403

CHECKER = "n x m table of integers; unique, exact token comparison."
STATEMENT = "Legend (later paint overrides), input (n,m<=5000, nm<=1e5, k<=1e5), output present."


def solve(s):
    v = ints(s)
    n, m, k = v[:3]
    row, col = [(0, 0)] * (n + 1), [(0, 0)] * (m + 1)
    for t in range(k):
        typ, idx, a = v[3 + 3 * t:6 + 3 * t]
        if typ == 1:
            row[idx] = (t + 1, a)
        else:
            col[idx] = (t + 1, a)
    return "".join(" ".join(str(max(row[i], col[j])[1]) for j in range(1, m + 1)) + "\n" for i in range(1, n + 1))


def make(g, n, m, k, hi=10 ** 9):
    ops = []
    for _ in range(k):
        t = g.randint(1, 2)
        ops.append([t, g.randint(1, n if t == 1 else m), g.randint(1, hi)])
    return fmt([n, m, k], *ops)


def cases(g):
    out = [("boundary", "1x1 one op", fmt([1, 1, 1], [1, 1, 5])),
           ("boundary", "nm=1e5 as 1 x 1e5 is invalid (m<=5000): use 20 x 5000", make(g, 20, 5000, 1)),
           ("adversarial", "column then row on same cell (row wins)", fmt([2, 2, 2], [2, 1, 7], [1, 1, 9])),
           ("adversarial", "repainting the same row many times", fmt([1, 3, 4], [1, 1, 1], [1, 1, 2], [2, 2, 3], [1, 1, 4])),
           ("maxSize", "5000 x 20, k=1e5", make(g, 5000, 20, 100000)),
           ("maxSize", "316 x 316, k=1e5", make(g, 316, 316, 100000))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), g.randint(1, 8), 9), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 50), g.randint(1, 50), g.randint(1, 200)), 30)
    return out
