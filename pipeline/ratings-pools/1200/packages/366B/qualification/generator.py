import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single task index; ties broken by smallest index, so unique; exact token comparison."
STATEMENT = "Legend (told off every k-th task cyclically), input (1<=k<=n<=1e5, k|n, 1<=ai<=1e3), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a = v[2:]
    sums = [sum(a[i::k]) for i in range(k)]
    return f"{sums.index(min(sums)) + 1}\n"


def make(g, n, k, hi=1000):
    return fmt([n, k], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=k=1", fmt([1, 1], [5])), ("boundary", "k=n (min element index)", fmt([4, 4], [3, 1, 1, 2])),
           ("adversarial", "tie must pick smallest index", fmt([4, 2], [2, 2, 2, 2])),
           ("maxSize", "n=1e5 k=1", make(g, N, 1)), ("maxSize", "n=1e5 k=1e5", make(g, N, N)),
           ("maxSize", "n=1e5 k=2 all 1000 (tie)", fmt([N, 2], [1000] * N)), ("maxSize", "n=1e5 k=400", make(g, N, 400))]
    def small(g):
        k = g.randint(1, 6)
        return make(g, k * g.randint(1, 4), k, 3)
    out += fill(g, small, 80, reason="small random")
    def mid(g):
        k = g.randint(1, 50)
        return make(g, k * g.randint(1, 60), k)
    out += fill(g, mid, 30)
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
