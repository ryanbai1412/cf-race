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
STATEMENT = "Legend, input (1<=n<=3e5, |ai|<=1e9), output present."


def solve(s):
    v = ints(s)
    a = sorted(v[1:])
    return f"{sum(abs(x - i) for i, x in enumerate(a, 1))}\n"


def arr(g, n, lo, hi):
    return fmt(n, [g.randint(lo, hi) for _ in range(n)])


def cases(g):
    B = 10 ** 9
    out = [("boundary", "n=1 already 1", fmt(1, [1])), ("boundary", "n=1 extreme negative", fmt(1, [-B])),
           ("boundary", "n=1 extreme positive", fmt(1, [B])),
           ("adversarial", "already a permutation in reverse", fmt(5, [5, 4, 3, 2, 1])),
           ("adversarial", "all equal duplicates", fmt(6, [3] * 6)),
           ("adversarial", "answer exceeds 32 bits", fmt(5, [-B] * 5)),
           ("maxSize", "n=3e5 values at +-1e9 (64-bit answer)", arr(g, 300000, -B, B)),
           ("maxSize", "n=3e5 small values", arr(g, 300000, -9, 9))]
    out += fill(g, lambda g: arr(g, g.randint(1, 50), -60, 60), 70, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 2000), -B, B), 40, reason="medium random wide values")
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
