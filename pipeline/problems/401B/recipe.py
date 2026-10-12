from genlib import *  # noqa: F401,F403

CHECKER = "Two integers (min, max); unique, exact token comparison."
STATEMENT = "Legend (Div1/Div2 simultaneous rounds, identifiers consecutive), input (1<=x<=4000, 0<=k<4000, valid descriptions), output present."


def solve(s):
    v = ints(s)
    x, k = v[0], v[1]
    used = [False] * (x + 1)
    i = 2
    for _ in range(k):
        if v[i] == 1:
            used[v[i + 1]] = used[v[i + 2]] = True
            i += 3
        else:
            used[v[i + 1]] = True
            i += 2
    lo = hi = run = 0
    for r in range(1, x + 1):
        if r < x and not used[r]:
            run += 1
        else:
            lo += (run + 1) // 2
            hi += run
            run = 0
    return f"{lo} {hi}\n"


def make(g, x, pair_p=0.4, take=0.5):
    groups, r = [], 1
    while r < x:
        if r + 1 < x and g.random() < pair_p:
            groups.append((1, r, r + 1))
            r += 2
        else:
            groups.append((2, r))
            r += 1
    chosen = [grp for grp in groups if g.random() < take]
    g.shuffle(chosen)
    return fmt([x, len(chosen)], *chosen)


def cases(g):
    out = [("boundary", "x=1 k=0", fmt([1, 0])), ("boundary", "x=2 k=0", fmt([2, 0])),
           ("adversarial", "only pair given", fmt([4, 1], [1, 1, 2])), ("adversarial", "odd gap", fmt([5, 1], [2, 4])),
           ("maxSize", "x=4000 k=0", fmt([4000, 0])), ("maxSize", "x=4000 all singles given (k=3999)", fmt([4000, 3999], *[[2, r] for r in range(1, 4000)])),
           ("maxSize", "x=4000 random structure", make(g, 4000)), ("maxSize", "x=4000 all pairs given", make(g, 4000, 1.0, 1.0))]
    out += fill(g, lambda g: make(g, g.randint(1, 15), g.random(), g.random()), 100, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(16, 4000), g.random(), g.random()), 30)
    return out
