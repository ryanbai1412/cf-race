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
STATEMENT = "Legend defines splitting game, input (1<=n<=3e5, 1<=ai<=1e6), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    a = sorted(v[1:])
    return f"{sum(x * min(i + 2, n) for i, x in enumerate(a))}\n"


def arr(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    M = 10 ** 6
    out = [("boundary", "n=1", fmt(1, [10])), ("boundary", "n=2", fmt(2, [1, M])),
           ("adversarial", "all equal", fmt(5, [7] * 5)), ("adversarial", "descending input", fmt(6, [6, 5, 4, 3, 2, 1])),
           ("maxSize", "n=3e5 all 1e6 (answer > 4e16)", fmt(300000, [M] * 300000)),
           ("maxSize", "n=3e5 random", arr(g, 300000, M))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), 20), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000), M), 30, reason="medium random")
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
