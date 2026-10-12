import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "One of four fixed phrases; unique, exact token comparison."
STATEMENT = "Legend defines bus/ring/star, input (4<=n<=1e5, 3<=m<=1e5, connected simple graph), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    deg = [0] * (n + 1)
    for x in v[2:]:
        deg[x] += 1
    d = sorted(deg[1:])
    if m == n - 1 and d.count(1) == 2 and d.count(2) == n - 2:
        return "bus topology\n"
    if m == n and d.count(2) == n:
        return "ring topology\n"
    if m == n - 1 and d.count(1) == n - 1 and d[-1] == n - 1:
        return "star topology\n"
    return "unknown topology\n"


def emit(g, n, edges):
    p = list(range(1, n + 1))
    g.shuffle(p)
    e = [[p[a - 1], p[b - 1]] if g.random() < 0.5 else [p[b - 1], p[a - 1]] for a, b in edges]
    g.shuffle(e)
    return fmt([n, len(e)], *e)


def bus(n):
    return [(i, i + 1) for i in range(1, n)]


def ring(n):
    return bus(n) + [(n, 1)]


def star(n):
    return [(1, i) for i in range(2, n + 1)]


def tree(g, n, extra=0):
    e = {(g.randint(1, i - 1), i) for i in range(2, n + 1)}
    while len(e) < n - 1 + extra:
        a, b = g.sample(range(1, n + 1), 2)
        if (a, b) not in e and (b, a) not in e:
            e.add((a, b))
    return sorted(e)


def cases(g):
    out = [("boundary", "n=4 bus", emit(g, 4, bus(4))), ("boundary", "n=4 ring", emit(g, 4, ring(4))),
           ("boundary", "n=4 star", emit(g, 4, star(4))),
           ("adversarial", "bus with one extra chord (unknown)", emit(g, 6, bus(6) + [(1, 3)])),
           ("adversarial", "star missing nothing but one leaf re-hung (unknown)", emit(g, 6, star(5) + [(5, 6)])),
           ("adversarial", "ring plus pendant vertex m=n (unknown)", emit(g, 5, ring(4) + [(4, 5)])),
           ("adversarial", "complete graph K4 (unknown)", emit(g, 4, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])),
           ("maxSize", "n=1e5 bus", emit(g, 100000, bus(100000))), ("maxSize", "n=1e5 ring", emit(g, 100000, ring(100000))),
           ("maxSize", "n=1e5 star", emit(g, 100000, star(100000)))]
    for kind in (bus, ring, star):
        out += fill(g, lambda g, k=kind: emit(g, (n := g.randint(4, 40)), k(n)), 20, reason=f"random {kind.__name__}")
    out += fill(g, lambda g: emit(g, (n := g.randint(4, 40)), tree(g, n, g.choice([0, 0, 1, 2]))), 50, reason="random connected graph")
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
