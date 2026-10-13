import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (row limited by its weakest tooth), input (1<=m<=n<=1000, 0<=k<=1e6, every row non-empty), output present."


def solve(s):
    v = ints(s)
    n, m, k = v[:3]
    low = {}
    for i in range(n):
        r, c = v[3 + 2 * i], v[4 + 2 * i]
        low[r] = min(low.get(r, c), c)
    return f"{min(k, sum(low.values()))}\n"


def make(g, n, m, k, hi):
    rows = list(range(1, m + 1)) + [g.randint(1, m) for _ in range(n - m)]
    g.shuffle(rows)
    return fmt([n, m, k], *[[r, g.randint(0, hi)] for r in rows])


def cases(g):
    M = 10 ** 6
    out = [("boundary", "n=m=1 k=0", fmt([1, 1, 0], [1, 5])), ("boundary", "viability 0", fmt([1, 1, 10], [1, 0])),
           ("adversarial", "weakest tooth limits row", fmt([3, 1, 100], [1, 50], [1, 2], [1, 70])),
           ("maxSize", "n=m=1000 all 1e6, k=1e6", fmt([1000, 1000, M], *[[i, M] for i in range(1, 1001)])),
           ("maxSize", "n=1000 m=1 k=1e6", make(g, 1000, 1, M, M)), ("maxSize", "n=1000 m=500 random", make(g, 1000, 500, g.randint(0, M), M))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 6)), g.randint(1, n), g.randint(0, 30), 10), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 1000)), g.randint(1, n), g.randint(0, M), M), 30)
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
