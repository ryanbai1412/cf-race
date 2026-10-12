import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


from itertools import combinations

CHECKER = "Single integer count of rounds; unique, exact token comparison."
STATEMENT = "Legend (repeatedly remove all degree-1 vertices at once), input (1<=n<=100, simple graph), output present."


def solve(s):
    v = ints(s)
    n, m = v[0], v[1]
    adj = [set() for _ in range(n + 1)]
    for i in range(m):
        a, b = v[2 + 2 * i], v[3 + 2 * i]
        adj[a].add(b)
        adj[b].add(a)
    rounds = 0
    while True:
        leaves = [x for x in range(1, n + 1) if len(adj[x]) == 1]
        if not leaves:
            return f"{rounds}\n"
        rounds += 1
        for x in leaves:
            for y in adj[x]:
                adj[y].discard(x)
            adj[x] = set()


def emit(g, n, edges):
    e = [list(p) if g.random() < 0.5 else list(p)[::-1] for p in edges]
    g.shuffle(e)
    return fmt([n, len(e)], *e)


def rand_graph(g, n, p):
    return emit(g, n, [x for x in combinations(range(1, n + 1), 2) if g.random() < p])


def tree(g, n):
    return [(g.randint(1, i - 1), i) for i in range(2, n + 1)]


def cases(g):
    out = [("boundary", "n=1 m=0", fmt([1, 0])), ("boundary", "n=2 single lace", fmt([2, 1], [1, 2])),
           ("adversarial", "triangle (no leaves)", fmt([3, 3], [1, 2], [2, 3], [3, 1])),
           ("adversarial", "path of 6 (rounds from both ends)", emit(g, 6, [(i, i + 1) for i in range(1, 6)])),
           ("maxSize", "n=100 path (answer 50)", emit(g, 100, [(i, i + 1) for i in range(1, 100)])),
           ("maxSize", "n=100 complete graph", rand_graph(g, 100, 1.0)),
           ("maxSize", "n=100 random tree", emit(g, 100, tree(g, 100)))]
    out += fill(g, lambda g: rand_graph(g, g.randint(1, 9), g.random() * 0.5), 60, reason="small random graph")
    out += fill(g, lambda g: emit(g, (n := g.randint(2, 100)), tree(g, n)), 30, reason="random tree")
    out += fill(g, lambda g: rand_graph(g, g.randint(10, 100), 0.03), 25, reason="sparse random graph")
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
