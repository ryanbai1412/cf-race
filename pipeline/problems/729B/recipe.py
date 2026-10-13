from genlib import *  # noqa: F401,F403

CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (empty cell with an actor somewhere in the chosen direction), input (1<=n,m<=1000, 0/1, at least one actor), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    a = [v[2 + i * m:2 + (i + 1) * m] for i in range(n)]
    total = 0
    for row in (a + [list(c) for c in zip(*a)]):
        ones = sum(row)
        if not ones:
            continue
        seen = 0
        for x in row:
            if x:
                seen += 1
            else:
                total += (seen > 0) + (seen < ones)
    return f"{total}\n"


def make(g, n, m, p=0.3):
    a = [[int(g.random() < p) for _ in range(m)] for _ in range(n)]
    a[g.randrange(n)][g.randrange(m)] = 1
    return fmt([n, m], *a)


def cases(g):
    out = [("boundary", "1x1 actor (0)", fmt([1, 1], [1])), ("boundary", "1x2", fmt([1, 2], [0, 1])),
           ("adversarial", "single actor in centre", fmt([3, 3], [0, 0, 0], [0, 1, 0], [0, 0, 0])),
           ("maxSize", "1000x1000 single actor corner", fmt([1000, 1000], *([[1] + [0] * 999] + [[0] * 1000] * 999))),
           ("maxSize", "1000x1000 random sparse", make(g, 1000, 1000, 0.001)), ("maxSize", "1000x1000 all actors (0)", fmt([1000, 1000], *[[1] * 1000] * 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), g.random()), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100), g.random()), 30)
    return out
