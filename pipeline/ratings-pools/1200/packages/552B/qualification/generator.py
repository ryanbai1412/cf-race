import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer digit count; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n<=1e9), output present."


def solve(s):
    n = int(s)
    total, d, start = 0, 1, 1
    while start <= n:
        total += (min(n, start * 10 - 1) - start + 1) * d
        d += 1
        start *= 10
    return f"{total}\n"


def cases(g):
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=9", fmt(9)), ("boundary", "n=10", fmt(10)),
           ("adversarial", "n=99999999", fmt(99999999)), ("adversarial", "n=100000000", fmt(100000000)),
           ("maxSize", "n=1e9 maximum", fmt(10 ** 9)), ("maxSize", "n=999999999", fmt(999999999))]
    out += [("random", "power of ten boundary", fmt(10 ** k + dlt)) for k in range(1, 9) for dlt in (-1, 1)]
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** 9)), 70)
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** g.randint(1, 8))), 40, reason="random magnitude")
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
