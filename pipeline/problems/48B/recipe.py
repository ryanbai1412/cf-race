from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (a x b or b x a lot), input (1<=n,m<=50, 0/1 grid, 1<=a,b<=50, at least one orientation fits), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    grid = [v[2 + i * m:2 + (i + 1) * m] for i in range(n)]
    a, b = v[2 + n * m:]
    best = None
    for h, w in ((a, b), (b, a)):
        for i in range(n - h + 1):
            for j in range(m - w + 1):
                c = sum(sum(row[j:j + w]) for row in grid[i:i + h])
                best = c if best is None else min(best, c)
    return f"{best}\n"


def make(g, n, m, p=0.5):
    grid = [[int(g.random() < p) for _ in range(m)] for _ in range(n)]
    while True:
        a, b = g.randint(1, max(n, m)), g.randint(1, max(n, m))
        if (a <= n and b <= m) or (a <= m and b <= n):
            return fmt([n, m], *grid, [a, b])


def cases(g):
    out = [("boundary", "1x1 tree", fmt([1, 1], [1], [1, 1])), ("boundary", "only rotated fits", fmt([1, 3], [1, 0, 1], [3, 1])),
           ("adversarial", "unrotated orientation better", fmt([2, 3], [1, 1, 0], [1, 1, 0], [2, 1])),
           ("maxSize", "50x50 all trees whole lot", fmt([50, 50], *[[1] * 50] * 50, [50, 50])), ("maxSize", "50x50 random 7x31", make(g, 50, 50)),
           ("maxSize", "50x50 random lot", fmt([50, 50], *[[g.randint(0, 1) for _ in range(50)] for _ in range(50)], [25, 13]))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), g.random()), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 50), g.randint(1, 50), g.random()), 30)
    return out
