from genlib import *  # noqa: F401,F403

CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (touch at least one house, no overlap), input (1<=n,t<=1000, -1000<=xi<=1000, 1<=ai<=1000, houses don't overlap), output present."


def solve(s):
    v = ints(s)
    n, t = v[0], v[1]
    h = sorted((2 * v[2 + 2 * i] - v[3 + 2 * i], 2 * v[2 + 2 * i] + v[3 + 2 * i]) for i in range(n))
    c = 2
    for (_, r), (l, _) in zip(h, h[1:]):
        gap = l - r
        c += 2 if gap > 2 * t else 1 if gap == 2 * t else 0
    return f"{c}\n"


def make(g, n, amax=1000):
    for _ in range(1000):
        hs, occ = [], []
        for _ in range(n * 20):
            if len(hs) == n:
                break
            x, a = g.randint(-1000, 1000), g.randint(1, amax)
            l, r = 2 * x - a, 2 * x + a
            if all(r <= L or l >= R for L, R in occ):
                occ.append((l, r))
                hs.append([x, a])
        if len(hs) == n:
            g.shuffle(hs)
            return hs
    raise RuntimeError("could not place houses")


def cases(g):
    out = [("boundary", "n=1 t=1", fmt([1, 1], [0, 1])), ("boundary", "n=t=1000-ish extreme coordinates", fmt([2, 1000], [-1000, 1000], [1000, 1000])),
           ("adversarial", "gap exactly t (one position)", fmt([2, 2], [0, 4], [5, 2])),
           ("adversarial", "touching houses (gap 0)", fmt([2, 3], [0, 2], [2, 2])),
           ("adversarial", "half-integer gap boundary", fmt([2, 1], [0, 1], [1, 1])),
           ("maxSize", "n=1000 unit houses at -1000..998 spaced", fmt([1000, 1], *[[x, 1] for x in range(-1000, 1000, 2)])),
           ("maxSize", "n=1000 random small houses", fmt([1000, 1], *make(g, 1000, 1)))]
    out += fill(g, lambda g: fmt([n := g.randint(1, 6), g.randint(1, 6)], *make(g, n, 6)), 80, reason="small random")
    out += fill(g, lambda g: fmt([n := g.randint(1, 60), g.randint(1, 1000)], *make(g, n, 30)), 30)
    return out
