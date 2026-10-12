from genlib import *  # noqa: F401,F403

CHECKER = "Yes/No decision; unique, exact token comparison."
STATEMENT = "Legend (two same-colour spheres -> one of another colour), input (0..1e6 each), output present."


def solve(s):
    a, b, c, x, y, z = ints(s)
    have = sum((h - n) // 2 for h, n in ((a, x), (b, y), (c, z)) if h > n)
    need = sum(n - h for h, n in ((a, x), (b, y), (c, z)) if n > h)
    return ("Yes" if have >= need else "No") + "\n"


def rand(g, hi):
    return fmt([g.randint(0, hi) for _ in range(3)], [g.randint(0, hi) for _ in range(3)])


def cases(g):
    M = 10 ** 6
    out = [("boundary", "all zero", fmt([0, 0, 0], [0, 0, 0])), ("boundary", "need one from nothing", fmt([0, 0, 0], [0, 0, 1])),
           ("boundary", "two spheres make one", fmt([2, 0, 0], [0, 0, 1])),
           ("adversarial", "odd surplus 3 gives only one", fmt([3, 0, 0], [0, 1, 1])),
           ("adversarial", "surplus must not be counted for deficit colour", fmt([5, 6, 1], [2, 7, 2])),
           ("maxSize", "max surplus covers max deficit? (No)", fmt([M, M, 0], [0, 0, M])),
           ("maxSize", "max surplus exactly enough", fmt([M, M, 0], [0, 0, M])),
           ("maxSize", "max needs all equal", fmt([M, M, M], [M, M, M]))]
    out += fill(g, lambda g: rand(g, M), 50)
    out += fill(g, lambda g: rand(g, 6), 70, reason="small counts")
    return out
