import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (components linked by shared row/column), input (1<=n<=100, 1<=x,y<=1000, distinct), output present."


def solve(s):
    v = ints(s)
    n = v[0]
    pts = [(v[1 + 2 * i], v[2 + 2 * i]) for i in range(n)]
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for i in range(n):
        for j in range(i):
            if pts[i][0] == pts[j][0] or pts[i][1] == pts[j][1]:
                par[find(i)] = find(j)
    return f"{len({find(i) for i in range(n)}) - 1}\n"


def make(g, n, hi):
    hi = max(hi, 10)
    pts = set()
    while len(pts) < n:
        pts.add((g.randint(1, hi), g.randint(1, hi)))
    pts = list(pts)
    g.shuffle(pts)
    return fmt(n, *pts)


def cases(g):
    out = [("boundary", "n=1", fmt(1, [1, 1])), ("boundary", "corner coordinates", fmt(2, [1, 1], [1000, 1000])),
           ("adversarial", "chain connected only transitively", fmt(4, [1, 1], [1, 5], [7, 5], [7, 9])),
           ("maxSize", "n=100 diagonal (answer 99)", fmt(100, *[[i * 10, i * 10] for i in range(1, 101)])),
           ("maxSize", "n=100 random wide", make(g, 100, 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), 5), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.choice([30, 1000])), 30)
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
