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
STATEMENT = "Legend (choose suggested subarrays to maximise happiness), input (1<=n,m<=100, -100<=ai<=100, 1<=l<=r<=n, repeats allowed), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    a = v[2:2 + n]
    q = v[2 + n:]
    return f"{sum(max(0, sum(a[q[2 * i] - 1:q[2 * i + 1]])) for i in range(m))}\n"


def make(g, n, m, lo=-100, hi=100):
    segs = []
    for _ in range(m):
        l = g.randint(1, n)
        segs.append([l, g.randint(l, n)])
    return fmt([n, m], [g.randint(lo, hi) for _ in range(n)], *segs)


def cases(g):
    out = [("boundary", "n=m=1 negative", fmt([1, 1], [-100], [1, 1])), ("boundary", "n=m=1 zero", fmt([1, 1], [0], [1, 1])),
           ("adversarial", "all negative", make(g, 10, 10, -100, -1)), ("adversarial", "repeated full segment", fmt([3, 3], [100, -1, 100], [1, 3], [1, 3], [1, 3])),
           ("maxSize", "n=m=100 all 100 full", fmt([100, 100], [100] * 100, *[[1, 100]] * 100)), ("maxSize", "n=m=100 random", make(g, 100, 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 6), -5, 5), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(7, 100), g.randint(1, 100)), 25)
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
