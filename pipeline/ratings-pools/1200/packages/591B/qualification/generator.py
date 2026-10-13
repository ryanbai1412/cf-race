import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


import string

CHECKER = "Single string; unique, exact token comparison."
STATEMENT = "Legend (each designer swaps letters x and y), input (1<=n,m<=2e5, lowercase), output present."
L = string.ascii_lowercase


def solve(s):
    t = s.split()
    m, name = int(t[1]), t[2]
    perm = {c: c for c in L}
    pos = {c: c for c in L}
    for i in range(m):
        x, y = t[3 + 2 * i], t[4 + 2 * i]
        px, py = pos[x], pos[y]
        perm[px], perm[py] = y, x
        pos[x], pos[y] = py, px
    return "".join(perm[c] for c in name) + "\n"


def make(g, n, m, alpha=L):
    return fmt([n, m], "".join(g.choice(alpha) for _ in range(n)), *[[g.choice(alpha), g.choice(alpha)] for _ in range(m)])


def cases(g):
    M = 200000
    out = [("boundary", "n=m=1 identity swap", fmt([1, 1], "a", ["a", "a"])), ("boundary", "letter absent from name", fmt([1, 1], "a", ["b", "c"])),
           ("adversarial", "swap then swap back", fmt([3, 2], "abc", ["a", "b"], ["b", "a"])),
           ("maxSize", "n=m=2e5 random", make(g, M, M)), ("maxSize", "n=m=2e5 two letters", make(g, M, M, "ab"))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 6), "abcd"), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 5000), g.randint(1, 5000)), 30)
    return out


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
