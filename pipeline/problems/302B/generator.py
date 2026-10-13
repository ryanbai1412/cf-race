import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


from bisect import bisect_left

CHECKER = "m song indices; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n,m<=1e5, total duration<=1e9, strictly increasing valid moments), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    pref, t = [], 0
    for i in range(n):
        t += v[2 + 2 * i] * v[3 + 2 * i]
        pref.append(t)
    return "".join(f"{bisect_left(pref, x) + 1}\n" for x in v[2 + 2 * n:])


def make(g, n, m, total):
    rows, used = [], 0
    for i in range(n):
        left = total - used - (n - i - 1)
        c = g.randint(1, max(1, min(left, total // n * 2)))
        t = g.randint(1, max(1, (left // c) if g.random() < 0.3 else max(1, min(left // c, 3))))
        rows.append([c, t])
        used += c * t
    m = min(m, used)
    return fmt([n, m], *rows, sorted(g.sample(range(1, used + 1), m)))


def cases(g):
    out = [("boundary", "n=m=1 total 1", fmt([1, 1], [1, 1], [1])),
           ("boundary", "single song duration 1e9, last minute", fmt([1, 1], [1, 10 ** 9], [10 ** 9])),
           ("adversarial", "moments at song boundaries", fmt([3, 6], [1, 2], [2, 1], [1, 3], [1, 2, 3, 4, 5, 7])),
           ("maxSize", "n=m=1e5 unit songs", fmt([100000, 100000], *[[1, 1]] * 100000, list(range(1, 100001)))),
           ("maxSize", "n=1e5 m=1e5 total near 1e9", make(g, 100000, 100000, 10 ** 9))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 8), 30), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 1000)), g.randint(1, 1000), g.randint(n, 10 ** 9)), 30)
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
