from genlib import *  # noqa: F401,F403

CHECKER = "Yes/No; unique, exact token comparison."
STATEMENT = "Legend (every non-leaf has >=3 leaf children), input (3<=n<=1000, 1<=pi<=i, root has >=2 children), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    par = [0, 0] + v[1:n]
    kids = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        kids[par[i]].append(i)
    for u in range(1, n + 1):
        if kids[u] and sum(1 for w in kids[u] if not kids[w]) < 3:
            return "No\n"
    return "Yes\n"


def spruce(g, n, break_it=False):
    par = [0, 0]
    inner = [1]
    while len(par) - 1 < n:
        u = g.choice(inner)
        for _ in range(3):
            if len(par) - 1 < n:
                par.append(u)
        if len(par) - 1 < n and g.random() < 0.3:
            inner.append(len(par) - 1)
    if break_it and n > 3:
        par[-1] = g.randint(1, n - 1)
    return par


def make(g, n, mode):
    if mode == "spruce":
        par = spruce(g, n, g.random() < 0.4)
    else:
        par = [0, 0, 1, 1] + [g.randint(1, i - 1) for i in range(4, n + 1)]
    par = par[:n + 1]
    if sum(1 for i in range(2, n + 1) if par[i] == 1) < 2:
        par[2] = par[3] = 1
    return fmt(n, *par[2:])


def cases(g):
    out = [("boundary", "n=3 root two leaves (No)", fmt(3, 1, 1)), ("boundary", "n=4 star (Yes)", fmt(4, 1, 1, 1)),
           ("adversarial", "inner child with two leaves", fmt(7, 1, 1, 1, 2, 2, 2)), ("adversarial", "inner child three leaves", fmt(8, 1, 1, 1, 2, 2, 2, 2)),
           ("maxSize", "n=1000 star", fmt(1000, *[1] * 999)), ("maxSize", "n=1000 spruce", make(g, 1000, "spruce")), ("maxSize", "n=1000 random", make(g, 1000, "random"))]
    out += fill(g, lambda g: make(g, g.randint(4, 14), g.choice(["spruce", "random"])), 110, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(13, 1000), g.choice(["spruce", "spruce", "random"])), 25)
    return out
