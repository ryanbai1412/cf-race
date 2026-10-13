import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Count then increasing index list; the set is unique, exact token comparison (empty second line optional)."
STATEMENT = "Legend, input (2<=n<=2e5, 1<=ai<=1000), output present."


def solve(s):
    v = ints(s)
    n, a = v[0], v[1:]
    t = sum(a)
    idx = [i for i, x in enumerate(a, 1) if x * n == t]
    return f"{len(idx)}\n" + (" ".join(map(str, idx)) + "\n" if idx else "")


def arr(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=2 equal", fmt(2, [1, 1])), ("boundary", "n=2 different (0)", fmt(2, [1, 2])),
           ("adversarial", "mean is non-integer", fmt(3, [1, 1, 2])),
           ("adversarial", "single element equals mean", fmt(5, [1, 2, 3, 4, 5])),
           ("maxSize", "n=2e5 all 1000 (all indices)", fmt(200000, [1000] * 200000)),
           ("maxSize", "n=2e5 random", arr(g, 200000, 1000))]
    out += fill(g, lambda g: arr(g, g.randint(2, 8), 3), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(2, 2000), g.choice([2, 1000])), 30)
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
