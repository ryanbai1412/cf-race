import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (unordered couples with opposite t, 0 pairs with 0), input (1<=n<=1e5, -10<=ti<=10), output present."


def solve(s):
    v = ints(s)
    c = {}
    for x in v[1:]:
        c[x] = c.get(x, 0) + 1
    z = c.get(0, 0)
    return f"{z * (z - 1) // 2 + sum(c.get(x, 0) * c.get(-x, 0) for x in range(1, 11))}\n"


def arr(g, n, lo=-10, hi=10):
    return fmt(n, [g.randint(lo, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 zero", fmt(1, [0])), ("boundary", "n=2 opposite extremes", fmt(2, [-10, 10])),
           ("adversarial", "only positives", fmt(4, [1, 2, 3, 10])),
           ("maxSize", "n=1e5 all zeros (64-bit answer)", fmt(100000, [0] * 100000)),
           ("maxSize", "n=1e5 half 10 half -10 (2.5e9)", fmt(100000, [10, -10] * 50000)),
           ("maxSize", "n=1e5 random", arr(g, 100000))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), -3, 3), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000)), 30)
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
