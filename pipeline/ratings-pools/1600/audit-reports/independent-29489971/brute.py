import itertools, random, sys, importlib.util, io, contextlib
from functools import lru_cache
def load(p, inp):
    src = open(f"/mine/v{p}.py").read()
    so = io.StringIO()
    class B: buffer = io.BytesIO(inp.encode())
    g = {"__name__": "__main__"}
    old = sys.stdin; sys.stdin = B
    with contextlib.redirect_stdout(so): exec(src, g)
    sys.stdin = old
    return so.getvalue().split()
cnt = {}
# 246D literal definition brute
def b246(n, c, E):
    adj = [[False]*n for _ in range(n)]
    for a, b in E: adj[a][b] = adj[b][a] = True
    best = None
    for k in sorted(set(c)):
        V = [v for v in range(n) if c[v] == k]
        Q = {c[u] for u in range(n) for v in V if adj[v][u] and c[u] != k}
        if best is None or len(Q) > best[0]: best = (len(Q), k)
    return [str(best[1])]
rng = random.Random(246)
for n in range(2, 5):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1, 1 << len(pairs)):
        E = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        for c in itertools.product(range(1, 5), repeat=n):
            inp = f"{n} {len(E)}\n{' '.join(map(str,c))}\n" + "".join(f"{a+1} {b+1}\n" for a, b in E)
            assert load("246D", inp) == b246(n, c, E), inp
            cnt["246D"] = cnt.get("246D", 0) + 1
for _ in range(3000):
    n = rng.randint(2, 9); pairs = list(itertools.combinations(range(n), 2)); rng.shuffle(pairs)
    E = pairs[:rng.randint(1, len(pairs))]; c = [rng.choice([1, 2, 3, 7, 100000]) for _ in range(n)]
    inp = f"{n} {len(E)}\n{' '.join(map(str,c))}\n" + "".join(f"{a+1} {b+1}\n" for a, b in E)
    assert load("246D", inp) == b246(n, c, E), inp; cnt["246D"] += 1
# 525C brute: memoized search over all choices of 4 sticks + reductions
@lru_cache(None)
def f(sticks):
    if len(sticks) < 4: return 0
    first, rest = sticks[0], sticks[1:]
    best = f(rest)
    for j, k, l in itertools.combinations(range(len(rest)), 3):
        others = [rest[j], rest[k], rest[l]]
        remain = tuple(x for i, x in enumerate(rest) if i not in (j, k, l))
        for red in itertools.product((0, 1), repeat=4):
            q = sorted(v - r for v, r in zip([first] + others, red))
            if q[0] == q[1] and q[2] == q[3]:
                best = max(best, q[0] * q[2] + f(remain))
    return best
for n in range(1, 7):
    for s in itertools.combinations_with_replacement(range(2, 7), n):
        for perm in {s, s[::-1]}:
            inp = f"{n}\n{' '.join(map(str, perm))}\n"
            assert load("525C", inp) == [str(f(tuple(sorted(perm))))], inp
            cnt["525C"] = cnt.get("525C", 0) + 1
for _ in range(1500):
    n = rng.randint(4, 9); s = [rng.randint(2, 9) for _ in range(n)]
    inp = f"{n}\n{' '.join(map(str, s))}\n"
    assert load("525C", inp) == [str(f(tuple(sorted(s))))], inp; cnt["525C"] += 1
# 534C brute: enumerate all rolls
for n in range(1, 5):
    for d in itertools.product(range(1, 5), repeat=n):
        rolls = list(itertools.product(*[range(1, x + 1) for x in d]))
        for A in range(n, sum(d) + 1):
            poss = [set() for _ in range(n)]
            for r in rolls:
                if sum(r) == A:
                    for i, v in enumerate(r): poss[i].add(v)
            inp = f"{n} {A}\n{' '.join(map(str, d))}\n"
            assert load("534C", inp) == [str(d[i] - len(poss[i])) for i in range(n)], inp
            cnt["534C"] = cnt.get("534C", 0) + 1
print(cnt)
