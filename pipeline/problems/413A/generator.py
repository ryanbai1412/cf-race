import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Correct/Incorrect decision; unique, exact token comparison."
STATEMENT = "Legend, input (1<=m<n<=100, 1<=min<max<=100, 1<=ti<=100), output present."


def solve(s):
    v = ints(s)
    n, m, lo, hi = v[:4]
    t = v[4:]
    if min(t) < lo or max(t) > hi:
        return "Incorrect\n"
    need = (lo not in t) + (hi not in t)
    return ("Correct" if need <= n - m else "Incorrect") + "\n"


def rand(g, spread=3):
    n = g.randint(2, 100)
    m = g.randint(1, n - 1)
    lo = g.randint(1, 99)
    hi = g.randint(lo + 1, 100)
    t = [g.randint(max(1, lo - spread), min(100, hi + spread)) if g.random() < 0.2 else g.randint(lo, hi) for _ in range(m)]
    return fmt([n, m, lo, hi], t)


def cases(g):
    out = [("boundary", "n=2 m=1 min reported", fmt([2, 1, 1, 2], [1])), ("boundary", "n=2 m=1 middle missing both (Incorrect)", fmt([3, 2, 1, 3], [2, 2])),
           ("boundary", "min=1 max=100", fmt([3, 1, 1, 100], [50])),
           ("adversarial", "one slot but both extremes missing", fmt([4, 3, 10, 20], [15, 15, 15])),
           ("adversarial", "temperature below min", fmt([5, 2, 10, 20], [9, 15])),
           ("adversarial", "temperature above max", fmt([5, 2, 10, 20], [21, 15])),
           ("maxSize", "n=100 m=99 both extremes present", fmt([100, 99, 1, 100], [1] + [50] * 97 + [100])),
           ("maxSize", "n=100 m=99 one extreme missing", fmt([100, 99, 1, 100], [1] + [50] * 98))]
    out += fill(g, rand, 80)
    out += fill(g, lambda g: rand(g, 0), 40, reason="in-range random")
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
