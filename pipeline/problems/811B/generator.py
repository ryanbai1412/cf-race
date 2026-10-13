import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "m lines Yes/No; unique, exact token comparison."
STATEMENT = "Legend (sort subsegment, has p_x changed), input (1<=n,m<=1e4, permutation, 1<=l<=x<=r<=n), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    p = v[2:2 + n]
    q = [v[2 + n + 3 * i:5 + n + 3 * i] for i in range(m)]
    events = []
    for i, (l, r, x) in enumerate(q):
        events.append((l - 1, -1, i))
        events.append((r, 1, i))
    events.sort()
    cnt = [0] * m
    bit = [0] * (n + 1)
    pos = 0
    for at, sign, i in events:
        while pos < at:
            j = p[pos]
            while j <= n:
                bit[j] += 1
                j += j & -j
            pos += 1
        t, c = p[q[i][2] - 1] - 1, 0
        while t > 0:
            c += bit[t]
            t -= t & -t
        cnt[i] += sign * c
    return "".join("Yes\n" if q[i][0] + cnt[i] == q[i][2] else "No\n" for i in range(m))


def make(g, n, m):
    p = list(range(1, n + 1))
    g.shuffle(p)
    qs = []
    for _ in range(m):
        l = g.randint(1, n)
        r = g.randint(l, n)
        qs.append([l, r, g.randint(l, r)])
    return fmt([n, m], p, *qs)


def cases(g):
    N = 10 ** 4
    out = [("boundary", "n=m=1", fmt([1, 1], [1], [1, 1, 1])), ("boundary", "sorted permutation", fmt([4, 2], [1, 2, 3, 4], [1, 4, 2], [2, 3, 3])),
           ("adversarial", "reversed full sorts", fmt([5, 3], [5, 4, 3, 2, 1], [1, 5, 3], [1, 5, 1], [1, 5, 5])),
           ("maxSize", "n=m=1e4 full segments", fmt([N, N], list(range(N, 0, -1)), *[[1, N, x] for x in range(1, N + 1)])),
           ("maxSize", "n=m=1e4 random", make(g, N, N))]
    out += fill(g, lambda g: make(g, g.randint(1, 7), g.randint(1, 7)), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(8, 500), g.randint(1, 500)), 25)
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
