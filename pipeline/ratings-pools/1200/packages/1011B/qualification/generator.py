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
STATEMENT = "Legend (one food type per participant), input (1<=n,m<=100, 1<=ai<=100), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    c = {}
    for x in v[2:]:
        c[x] = c.get(x, 0) + 1
    d = 0
    while sum(x // (d + 1) for x in c.values()) >= n:
        d += 1
    return f"{d}\n"


def make(g, n, m, hi=100):
    return fmt([n, m], [g.randint(1, hi) for _ in range(m)])


def cases(g):
    out = [("boundary", "n=m=1", fmt([1, 1], [1])), ("boundary", "n=100 m=1 (0)", fmt([100, 1], [1])),
           ("adversarial", "m<n (0)", make(g, 50, 49)),
           ("maxSize", "n=1 m=100 all same (100)", fmt([1, 100], [100] * 100)), ("maxSize", "n=m=100 all distinct", fmt([100, 100], list(range(1, 101)))),
           ("maxSize", "n=100 m=100 random", make(g, 100, 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 15), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100), g.randint(1, 100)), 30)
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
