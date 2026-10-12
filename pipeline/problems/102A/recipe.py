from genlib import *  # noqa: F401,F403
from itertools import combinations

CHECKER = "Single minimum integer or -1; unique, exact token comparison."
STATEMENT = "Legend (three pairwise-matching items), input (3<=n<=100, 0<=m<=n(n-1)/2, distinct pairs), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    a = v[2:2 + n]
    adj = [set() for _ in range(n + 1)]
    for i in range(m):
        x, y = v[2 + n + 2 * i], v[3 + n + 2 * i]
        adj[x].add(y)
        adj[y].add(x)
    best = -1
    for x in range(1, n + 1):
        for y in adj[x]:
            if y > x:
                for z in adj[x] & adj[y]:
                    if z > y:
                        c = a[x - 1] + a[y - 1] + a[z - 1]
                        best = c if best < 0 else min(best, c)
    return f"{best}\n"


def make(g, n, p, hi=10 ** 6):
    e = [[x, y] if g.random() < 0.5 else [y, x] for x, y in combinations(range(1, n + 1), 2) if g.random() < p]
    g.shuffle(e)
    return fmt([n, len(e)], [g.randint(1, hi) for _ in range(n)], *e)


def cases(g):
    out = [("boundary", "n=3 m=0", fmt([3, 0], [1, 2, 3])), ("boundary", "n=3 triangle", fmt([3, 3], [1, 2, 3], [1, 2], [2, 3], [3, 1])),
           ("adversarial", "path without triangle", fmt([4, 3], [1, 1, 1, 1], [1, 2], [2, 3], [3, 4])),
           ("adversarial", "cheap items not in a triangle", fmt([5, 4], [1, 1, 9, 9, 9], [1, 2], [3, 4], [4, 5], [5, 3])),
           ("maxSize", "n=100 complete graph, max prices", make(g, 100, 1.0, 10 ** 6)),
           ("maxSize", "n=100 dense random", make(g, 100, 0.5))]
    out += fill(g, lambda g: make(g, g.randint(3, 8), g.random(), 20), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(3, 100), g.random() * 0.2), 30)
    return out
