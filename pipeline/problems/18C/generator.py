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
STATEMENT = "Legend (cut into two non-empty pieces), input (1<=n<=1e5, |ai|<=1e4), output present."


def solve(s):
    v = ints(s)
    a = v[1:]
    t, p, c = sum(a), 0, 0
    for x in a[:-1]:
        p += x
        c += 2 * p == t
    return f"{c}\n"


def arr(g, n, hi):
    return fmt(n, [g.randint(-hi, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 (0 cuts)", fmt(1, [5])), ("boundary", "n=2 equal", fmt(2, [-10000, -10000])),
           ("adversarial", "all zeros (n-1 cuts)", fmt(8, [0] * 8)), ("adversarial", "odd total", fmt(3, [1, 1, 1])),
           ("maxSize", "n=1e5 all zeros", fmt(100000, [0] * 100000)), ("maxSize", "n=1e5 random", arr(g, 100000, 10000)),
           ("maxSize", "n=1e5 alternating +-1e4", fmt(100000, [10000 * (-1) ** i for i in range(100000)]))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), 2), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000), g.choice([1, 10000])), 30)
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
