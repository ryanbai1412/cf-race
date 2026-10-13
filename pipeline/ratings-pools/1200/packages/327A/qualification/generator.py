import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single maximal integer; unique, exact token comparison."
STATEMENT = "Legend (exactly one non-empty flip), input (1<=n<=100, ai in {0,1}), output present."


def solve(s):
    v = ints(s)[1:]
    ones = sum(v)
    best = max(sum(1 if x == 0 else -1 for x in v[i:j + 1]) for i in range(len(v)) for j in range(i, len(v)))
    return f"{ones + best}\n"


def arr(g, n, p=0.5):
    return fmt(n, [1 if g.random() < p else 0 for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 value 1 (must flip, answer 0)", fmt(1, [1])), ("boundary", "n=1 value 0", fmt(1, [0])),
           ("adversarial", "all ones: forced loss of one", fmt(100, [1] * 100)),
           ("adversarial", "all zeros", fmt(100, [0] * 100)),
           ("adversarial", "alternating", fmt(100, [i % 2 for i in range(100)])),
           ("maxSize", "n=100 mostly ones", arr(g, 100, 0.9)), ("maxSize", "n=100 random", arr(g, 100))]
    out += fill(g, lambda g: arr(g, g.randint(1, 100), g.random()), 70)
    out += fill(g, lambda g: arr(g, g.randint(1, 12)), 50, reason="tiny")
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
