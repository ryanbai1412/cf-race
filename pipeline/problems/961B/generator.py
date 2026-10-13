import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (keep awake k consecutive minutes once), input (1<=k<=n<=1e5, 1<=ai<=1e4, ti in {0,1}), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a, t = v[2:2 + n], v[2 + n:2 + 2 * n]
    base = sum(x for x, y in zip(a, t) if y)
    gain = [x if not y else 0 for x, y in zip(a, t)]
    w = best = sum(gain[:k])
    for i in range(k, n):
        w += gain[i] - gain[i - k]
        best = max(best, w)
    return f"{base + best}\n"


def make(g, n, k, p=0.5, hi=10 ** 4):
    return fmt([n, k], [g.randint(1, hi) for _ in range(n)], [int(g.random() < p) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=k=1 asleep", fmt([1, 1], [5], [0])), ("boundary", "n=k=1 awake", fmt([1, 1], [5], [1])),
           ("adversarial", "k=n", make(g, 6, 6)), ("adversarial", "all awake", fmt([3, 2], [1, 2, 3], [1, 1, 1])),
           ("maxSize", "n=1e5 all asleep k=n", fmt([N, N], [10 ** 4] * N, [0] * N)), ("maxSize", "n=1e5 random", make(g, N, 777)), ("maxSize", "n=1e5 k=1", make(g, N, 1))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 8)), g.randint(1, n), g.random(), 9), 90, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(9, 3000)), g.randint(1, n), g.random()), 25)
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
