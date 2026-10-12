import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Ascending list of all valid x (or -1); the set is unique, exact token comparison."
STATEMENT = "Legend, input (1<=y,k,n<=1e9, n/k<=1e5), output present."


def solve(s):
    y, k, n = ints(s)
    first = k - y % k
    xs = range(first, n - y + 1, k)
    return (" ".join(map(str, xs)) if len(xs) else "-1") + "\n"


def rand(g, hi, ratio=1000):
    k = g.randint(1, hi)
    n = g.randint(1, min(10 ** 9, k * ratio))
    return fmt([g.randint(1, 10 ** 9 if g.random() < 0.3 else n), k, n])


def cases(g):
    out = [("boundary", "all ones (-1)", fmt([1, 1, 1])), ("boundary", "y=1 k=1 n=2 single x", fmt([1, 1, 2])),
           ("boundary", "y > n (-1)", fmt([10 ** 9, 1, 1])),
           ("adversarial", "y multiple of k (first x is k)", fmt([12, 6, 40])),
           ("adversarial", "x+y exactly n", fmt([4, 5, 10])),
           ("adversarial", "y=n-1 huge k (-1)", fmt([10 ** 9 - 1, 10 ** 9, 10 ** 9])),
           ("maxSize", "n/k = 1e5 exactly, y=1", fmt([1, 10000, 10 ** 9])),
           ("maxSize", "k=1 n=1e5", fmt([1, 1, 100000])),
           ("maxSize", "k=1e4 n=1e9 y=9999", fmt([9999, 10000, 10 ** 9]))]
    out += fill(g, lambda g: rand(g, 100), 50, reason="small k")
    out += fill(g, lambda g: rand(g, 10 ** 9), 40, reason="large k")
    out += fill(g, lambda g: fmt([g.randint(1, 30), g.randint(1, 10), g.randint(1, 60)]), 30, reason="tiny")
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
