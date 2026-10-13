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
STATEMENT = "Legend (nest strictly smaller boxes), input (1<=n<=5000, 1<=ai<=1e9), output present."


def solve(s):
    a = ints(s)[1:]
    return f"{max(a.count(x) for x in set(a))}\n"


def make(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1", fmt(1, [10 ** 9])), ("boundary", "all equal", fmt(4, [7] * 4)),
           ("adversarial", "distinct", fmt(3, [1, 2, 3])), ("maxSize", "n=5000 all equal", fmt(5000, [10 ** 9] * 5000)),
           ("maxSize", "n=5000 distinct", fmt(5000, list(range(1, 5001)))), ("maxSize", "n=5000 random", make(g, 5000, 50))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 5000), g.choice([3, 100, 10 ** 9])), 25)
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
