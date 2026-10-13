import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (change one character per second), input (1<=n<=100, valid sizes, b reachable from a), output present."
SIZES = ["M"] + [x * "X" + c for x in range(4) for c in "SL"]


def solve(s):
    t = s.split()
    n = int(t[0])
    a, b = t[1:1 + n], t[1 + n:1 + 2 * n]
    left = {}
    for x in a:
        left[x] = left.get(x, 0) + 1
    for x in b:
        if left.get(x, 0):
            left[x] -= 1
    return f"{sum(left.values())}\n"


def same_len(g, x):
    return g.choice([y for y in SIZES if len(y) == len(x)])


def make(g, n, change=0.5):
    a = [g.choice(SIZES) for _ in range(n)]
    b = [same_len(g, x) if g.random() < change else x for x in a]
    g.shuffle(b)
    return fmt(n, *a, *b)


def cases(g):
    out = [("boundary", "n=1 equal M", fmt(1, "M", "M")), ("boundary", "n=1 XXXS->XXXL", fmt(1, "XXXS", "XXXL")),
           ("adversarial", "same multiset in different order (0)", fmt(3, "S", "XL", "M", "M", "S", "XL")),
           ("adversarial", "S and L swap counts", fmt(4, "S", "S", "L", "L", "L", "L", "L", "S")),
           ("maxSize", "n=100 all different", make(g, 100, 1.0)), ("maxSize", "n=100 all XXXS->XXXL", fmt(100, *["XXXS"] * 100, *["XXXL"] * 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 6)), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.random()), 30)
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
