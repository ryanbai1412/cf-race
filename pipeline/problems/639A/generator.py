import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "YES/NO per type-2 query; unique, exact token comparison."
STATEMENT = "Legend (display top-k online friends by t), input (1<=n,q<=1.5e5, 1<=k<=min(6,n), distinct t, each id online at most once), output present."


def solve(s):
    v = ints(s)
    n, k, q = v[:3]
    t = v[3:3 + n]
    shown, out = [], []
    for i in range(q):
        typ, idx = v[3 + n + 2 * i], v[4 + n + 2 * i]
        if typ == 1:
            shown.append(idx)
            if len(shown) > k:
                shown.remove(min(shown, key=lambda j: t[j - 1]))
        else:
            out.append("YES" if idx in shown else "NO")
    return "".join(x + "\n" for x in out)


def make(g, n, k, q, hi=10 ** 9):
    t = g.sample(range(1, hi + 1), n)
    offline = list(range(1, n + 1))
    g.shuffle(offline)
    qs = []
    for _ in range(q):
        if offline and g.random() < 0.5:
            qs.append([1, offline.pop()])
        else:
            qs.append([2, g.randint(1, n)])
    return fmt([n, k, q], t, *qs)


def cases(g):
    N = 150000
    out = [("boundary", "n=k=q=1 query only", fmt([1, 1, 1], [5], [2, 1])), ("boundary", "n=k=1 online then check", fmt([1, 1, 2], [5], [1, 1], [2, 1])),
           ("adversarial", "k=1 newcomer worse than shown", fmt([2, 1, 4], [10, 5], [1, 1], [1, 2], [2, 1], [2, 2])),
           ("maxSize", "n=q=1.5e5 k=6 random", make(g, N, 6, N)), ("maxSize", "n=q=1.5e5 k=1", make(g, N, 1, N, 2 * N)),
           ("adversarial", "increasing t online in order k=6", fmt([2000, 6, 3000], list(range(1, 2001)), *[[1, i] for i in range(1, 1001)], *[[2, g.randint(1, 1000)] for _ in range(2000)]))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 8)), g.randint(1, min(6, n)), g.randint(1, 10), 20), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 2000)), g.randint(1, min(6, n)), g.randint(1, 2000)), 30)
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
