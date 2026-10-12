from bisect import bisect_right
from collections import Counter, deque
from itertools import combinations, permutations, product
from math import gcd
from lib import *


def nums(s):
    return list(map(int, s.split()))


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def f(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        a, b = self.f(a), self.f(b)
        if a == b:
            return False
        self.p[a] = b
        return True


@problem("277A", "n,m in [2,100]; each employee: k in [0,m] then k distinct languages in [1,m]", 0)
class P277A:
    def V(s):
        L = LR(s)
        n, m = L.ints([(2, 100), (2, 100)])
        for _ in range(n):
            t = L.line().split()
            need(t)
            k = intok(t[0], 0, m)
            need(len(t) == k + 1)
            langs = [intok(x, 1, m) for x in t[1:]]
            need(len(set(langs)) == k)
        L.done()

    def S(s):
        v = nums(s)
        n, m = v[0], v[1]
        d = DSU(n + m + 1)
        i, anyk = 2, False
        for e in range(n):
            k = v[i]
            for x in v[i + 1:i + 1 + k]:
                d.u(e, n + x)
                anyk = True
            i += k + 1
        if not anyk:
            return str(n)
        return str(len({d.f(e) for e in range(n)}) - 1)

    def G():
        r = rng("277A")
        rows = []
        for _ in range(100):
            k = r.randint(0, 3)
            rows.append(" ".join(map(str, [k] + r.sample(range(1, 101), k))))
        return [("boundary", "nobody knows any language", "2 2\n0\n0\n"), ("boundary", "one knows, one not", "2 2\n1 1\n0\n"),
                ("maxSize", "100x100 everybody knows everything", "100 100\n" + "\n".join("100 " + " ".join(map(str, range(1, 101))) for _ in range(100)) + "\n"),
                ("maxSize", "100x100 sparse random", "100 100\n" + "\n".join(rows) + "\n"),
                ("adversarial", "all know zero except n=100", "100 100\n" + "\n".join(["0"] * 100) + "\n"),
                ("adversarial", "disjoint language islands", "4 4\n1 1\n1 2\n1 3\n1 4\n")]


@problem("279B", "n in [1,1e5], t in [1,1e9]; a_i in [1,1e4]", 300)
class P279B:
    def V(s):
        L = LR(s)
        n, t = L.ints([(1, 10 ** 5), (1, 10 ** 9)])
        L.same(n, 1, 10 ** 4)
        L.done()

    def S(s):
        v = nums(s)
        n, t, a = v[0], v[1], v[2:]
        best = l = cur = 0
        for r in range(n):
            cur += a[r]
            while cur > t:
                cur -= a[l]
                l += 1
            best = max(best, r - l + 1)
        return str(best)

    def B(s):
        v = nums(s)
        n, t, a = v[0], v[1], v[2:]
        best = 0
        for i in range(n):
            tot = 0
            for j in range(i, n):
                tot += a[j]
                if tot > t:
                    break
                best = max(best, j - i + 1)
        return str(best)

    def SMALL(r):
        n = r.randint(1, 8)
        return f"{n} {r.randint(1, 30)}\n" + " ".join(str(r.randint(1, 10)) for _ in range(n)) + "\n"

    def G():
        r = rng("279B")
        N = 10 ** 5
        return [("boundary", "n=1 can't read", "1 1\n2\n"), ("boundary", "n=1 exactly t", "1 5\n5\n"),
                ("maxSize", "n=1e5 t=1e9 reads all", f"{N} 1000000000\n" + " ".join(["10000"] * N) + "\n"),
                ("maxSize", "n=1e5 random", f"{N} 500000\n" + " ".join(str(r.randint(1, 10 ** 4)) for _ in range(N)) + "\n"),
                ("adversarial", "best window at end", "6 10\n9 9 9 1 2 3\n")]


@problem("289B", "n,m in [1,100]; d in [1,1e4]; a in [1,1e4]", 0)
class P289B:
    def V(s):
        L = LR(s)
        n, m, d = L.ints([(1, 100), (1, 100), (1, 10 ** 4)])
        for _ in range(n):
            L.same(m, 1, 10 ** 4)
        L.done()

    def S(s):
        v = nums(s)
        d, a = v[2], sorted(v[3:])
        if any((x - a[0]) % d for x in a):
            return "-1"
        med = a[len(a) // 2]
        return str(sum(abs(x - med) // d for x in a))

    def G():
        r = rng("289B")
        return [("boundary", "1x1", "1 1 1\n1\n"), ("boundary", "impossible residue", "1 2 3\n1 2\n"),
                ("maxSize", "100x100 d=1 extremes", "100 100 1\n" + "\n".join(" ".join("1" if (i + j) % 2 else "10000" for j in range(100)) for i in range(100)) + "\n"),
                ("maxSize", "100x100 d=7 same residue random", "100 100 7\n" + "\n".join(" ".join(str(3 + 7 * r.randint(0, 1427)) for _ in range(100)) for _ in range(100)) + "\n"),
                ("adversarial", "one cell breaks residue", "2 2 2\n2 4\n6 7\n")]


@problem("315A", "n in [1,100]; a_i,b_i in [1,1000]", 0)
class P315A:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 100)])[0]
        for _ in range(n):
            L.same(2, 1, 1000)
        L.done()

    def S(s):
        v = nums(s)
        n = v[0]
        ab = [(v[1 + 2 * i], v[2 + 2 * i]) for i in range(n)]
        return str(sum(1 for i, (a, _) in enumerate(ab) if not any(j != i and ab[j][1] == a for j in range(n))))

    def G():
        return [("boundary", "single self-opening bottle cannot open itself", "1\n5 5\n"), ("boundary", "two identical self bottles", "2\n5 5\n5 5\n"),
                ("maxSize", "n=100 chain", "100\n" + "\n".join(f"{i} {i + 1}" for i in range(1, 101)) + "\n"),
                ("maxSize", "n=100 all same", "100\n" + "\n".join(["1000 1000"] * 100) + "\n"),
                ("adversarial", "self-loop plus others", "3\n1 1\n2 1\n3 2\n")]


@problem("358A", "n in [1,1000]; distinct x in [-1e6,1e6]", 300)
class P358A:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 1000)])[0]
        x = L.same(n, -10 ** 6, 10 ** 6)
        need(len(set(x)) == n)
        L.done()

    def S(s):
        x = nums(s)[1:]
        seg = [tuple(sorted(x[i:i + 2])) for i in range(len(x) - 1)]
        for i in range(len(seg)):
            a, b = seg[i]
            for j in range(i + 2, len(seg)):
                c, d = seg[j]
                if a < c < b < d or c < a < d < b:
                    return "yes"
        return "no"

    def B(s):
        x = nums(s)[1:]
        seg = [tuple(sorted(x[i:i + 2])) for i in range(len(x) - 1)]
        for (a, b), (c, d) in combinations(seg, 2):
            if (a < c < b < d) or (c < a < d < b):
                return "yes"
        return "no"

    def SMALL(r):
        n = r.randint(1, 7)
        return f"{n}\n" + " ".join(map(str, r.sample(range(-10, 11), n))) + "\n"

    def G():
        r = rng("358A")
        sp = []
        lo, hi = -10 ** 6, 10 ** 6
        for i in range(500):
            sp += [lo + i, hi - i]
        return [("boundary", "n=1", "1\n0\n"), ("boundary", "n=3", "3\n-1000000 1000000 0\n"),
                ("maxSize", "n=1000 nested spiral (no)", "1000\n" + " ".join(map(str, sp)) + "\n"),
                ("maxSize", "n=1000 random (yes)", "1000\n" + " ".join(map(str, r.sample(range(-10 ** 6, 10 ** 6 + 1), 1000))) + "\n"),
                ("maxSize", "n=1000 sorted", "1000\n" + " ".join(str(i * 1000) for i in range(1000)) + "\n"),
                ("adversarial", "intersection only between last and first", "4\n0 10 5 15\n")]


@problem("38C", "n,l in [1,100]; a_i in [1,100]", 0)
class P38C:
    def V(s):
        L = LR(s)
        n, l = L.ints([(1, 100), (1, 100)])
        L.same(n, 1, 100)
        L.done()

    def S(s):
        v = nums(s)
        l, a = v[1], v[2:]
        return str(max([d * sum(x // d for x in a) for d in range(l, 101)] + [0]))

    def G():
        r = rng("38C")
        return [("boundary", "l > all lengths", "3 100\n1 2 99\n"), ("boundary", "single stripe l=1", "1 1\n1\n"),
                ("maxSize", "n=100 all 100, l=1", "100 1\n" + " ".join(["100"] * 100) + "\n"),
                ("maxSize", "n=100 random", "100 7\n" + " ".join(str(r.randint(1, 100)) for _ in range(100)) + "\n"),
                ("adversarial", "only l=100 piece exists", "2 100\n100 99\n")]


@problem("413C", "1<=n<=100, 1<=m<=min(n,30); a in [1,1e7]; m distinct auction indices", 300)
class P413C:
    def V(s):
        L = LR(s)
        n, m = L.ints([(1, 100), (1, 30)])
        need(m <= n)
        L.same(n, 1, 10 ** 7)
        b = L.same(m, 1, n)
        need(len(set(b)) == m)
        L.done()

    def S(s):
        v = nums(s)
        n, m = v[0], v[1]
        a = v[2:2 + n]
        auc = set(v[2 + n:])
        cur = sum(a[i] for i in range(n) if i + 1 not in auc)
        for x in sorted((a[i - 1] for i in auc), reverse=True):
            cur = cur + max(cur, x)
        return str(cur)

    def B(s):
        v = nums(s)
        n, m = v[0], v[1]
        a = v[2:2 + n]
        auc = set(v[2 + n:])
        best = 0
        for order in permutations(range(n)):
            cur = 0
            for i in order:
                cur += max(cur, a[i]) if i + 1 in auc else a[i]
            best = max(best, cur)
        return str(best)

    def SMALL(r):
        n = r.randint(1, 5)
        m = r.randint(1, n)
        return f"{n} {m}\n" + " ".join(str(r.randint(1, 20)) for _ in range(n)) + "\n" + " ".join(map(str, r.sample(range(1, n + 1), m))) + "\n"

    def G():
        r = rng("413C")
        return [("boundary", "n=m=1", "1 1\n10000000\n1\n"), ("maxSize", "n=100 m=30 max prices (doubling to ~1e18)", "100 30\n" + " ".join(["10000000"] * 100) + "\n" + " ".join(map(str, range(1, 31))) + "\n"),
                ("maxSize", "n=100 m=30 random", "100 30\n" + " ".join(str(r.randint(1, 10 ** 7)) for _ in range(100)) + "\n" + " ".join(map(str, r.sample(range(1, 101), 30))) + "\n"),
                ("adversarial", "auction price exceeds points, take it first", "3 2\n1 1 100\n2 3\n")]


@problem("417B", "n in [1,1e5]; x in [0,1e5], k in [1,1e5]", 300)
class P417B:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 10 ** 5)])[0]
        for _ in range(n):
            L.ints([(0, 10 ** 5), (1, 10 ** 5)])
        L.done()

    def S(s):
        v = nums(s)
        cnt = {}
        for i in range(v[0]):
            x, k = v[1 + 2 * i], v[2 + 2 * i]
            c = cnt.get(k, 0)
            if x > c:
                return "NO"
            if x == c:
                cnt[k] = c + 1
        return "YES"

    def B(s):
        v = nums(s)
        seen = {}
        for i in range(v[0]):
            x, k = v[1 + 2 * i], v[2 + 2 * i]
            if x > 0 and (x - 1) not in seen.get(k, set()):
                return "NO"
            seen.setdefault(k, set()).add(x)
        return "YES"

    def SMALL(r):
        n = r.randint(1, 8)
        return f"{n}\n" + "".join(f"{r.randint(0, 3)} {r.randint(1, 2)}\n" for _ in range(n))

    def G():
        N = 10 ** 5
        return [("boundary", "single x=0", "1\n0 1\n"), ("boundary", "single x=1", "1\n1 1\n"),
                ("maxSize", "1e5 increasing for one participant", f"{N}\n" + "".join(f"{i} 100000\n" for i in range(N))),
                ("maxSize", "1e5 one gap at end", f"{N}\n" + "".join(f"{i} 7\n" for i in range(N - 1)) + f"{N} 7\n"),
                ("adversarial", "repeated x allowed", "4\n0 1\n0 1\n1 1\n0 1\n")]


@problem("41B", "n,b in [1,2000]; a_i in [1,2000]", 300)
class P41B:
    def V(s):
        L = LR(s)
        n, b = L.ints([(1, 2000), (1, 2000)])
        L.same(n, 1, 2000)
        L.done()

    def S(s):
        v = nums(s)
        b, a = v[1], v[2:]
        best, mn = b, a[0]
        for x in a[1:]:
            best = max(best, (b // mn) * x + b % mn)
            mn = min(mn, x)
        return str(best)

    def B(s):
        v = nums(s)
        b, a = v[1], v[2:]
        best = b
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                for c in range(b // a[i] + 1):
                    best = max(best, b - c * a[i] + c * a[j])
        return str(best)

    def SMALL(r):
        n = r.randint(1, 6)
        return f"{n} {r.randint(1, 30)}\n" + " ".join(str(r.randint(1, 15)) for _ in range(n)) + "\n"

    def G():
        r = rng("41B")
        return [("boundary", "n=1", "1 2000\n1\n"), ("maxSize", "n=2000 buy 1 sell 2000", "2000 2000\n1 " + " ".join(["2000"] * 1999) + "\n"),
                ("maxSize", "n=2000 decreasing", "2000 2000\n" + " ".join(str(2000 - i) for i in range(2000)) + "\n"),
                ("maxSize", "n=2000 random", "2000 1999\n" + " ".join(str(r.randint(1, 2000)) for _ in range(2000)) + "\n"),
                ("adversarial", "price higher than budget at start", "3 5\n7 1 6\n")]


@problem("437C", "n in [1,1000], m in [0,2000]; v in [0,1e5]; edges x!=y, no duplicate pairs", 0)
class P437C:
    def V(s):
        L = LR(s)
        n, m = L.ints([(1, 1000), (0, 2000)])
        L.same(n, 0, 10 ** 5)
        seen = set()
        for _ in range(m):
            x, y = L.same(2, 1, n)
            need(x != y and frozenset((x, y)) not in seen)
            seen.add(frozenset((x, y)))
        L.done()

    def S(s):
        v = nums(s)
        n, m = v[0], v[1]
        w = v[2:2 + n]
        e = v[2 + n:]
        return str(sum(min(w[e[2 * i] - 1], w[e[2 * i + 1] - 1]) for i in range(m)))

    def G():
        r = rng("437C")
        es = set()
        while len(es) < 2000:
            x, y = r.sample(range(1, 1001), 2)
            es.add((min(x, y), max(x, y)))
        return [("boundary", "n=1 m=0", "1 0\n100000\n"), ("boundary", "zero values", "2 1\n0 0\n1 2\n"),
                ("maxSize", "n=1000 m=2000 max values", "1000 2000\n" + " ".join(["100000"] * 1000) + "\n" + "\n".join(f"{x} {y}" for x, y in sorted(es)) + "\n"),
                ("maxSize", "n=1000 m=2000 random", "1000 2000\n" + " ".join(str(r.randint(0, 10 ** 5)) for _ in range(1000)) + "\n" + "\n".join(f"{y} {x}" for x, y in sorted(es)) + "\n"),
                ("adversarial", "star", "5 4\n1 100 100 100 100\n1 2\n1 3\n1 4\n1 5\n")]


@problem("441B", "n,v in [1,3000]; a_i,b_i in [1,3000]", 300)
class P441B:
    def V(s):
        L = LR(s)
        n, v = L.ints([(1, 3000), (1, 3000)])
        for _ in range(n):
            L.same(2, 1, 3000)
        L.done()

    def S(s):
        x = nums(s)
        n, v = x[0], x[1]
        f = [0] * 3003
        for i in range(n):
            f[x[2 + 2 * i]] += x[3 + 2 * i]
        tot, carry = 0, 0
        for d in range(1, 3002):
            take = min(v, carry)
            rest = v - take
            today = min(rest, f[d])
            tot += take + today
            carry = f[d] - today
        return str(tot)

    def B(s):
        x = nums(s)
        n, v = x[0], x[1]
        trees = sorted((x[2 + 2 * i], x[3 + 2 * i]) for i in range(n))
        cap = {}
        tot = 0
        rem = [b for _, b in trees]
        for d in range(1, 3003):
            c = v
            for i, (a, b) in enumerate(trees):
                if a == d - 1 and c:
                    t = min(c, rem[i])
                    rem[i] -= t
                    c -= t
                    tot += t
            for i, (a, b) in enumerate(trees):
                if a == d and c:
                    t = min(c, rem[i])
                    rem[i] -= t
                    c -= t
                    tot += t
        return str(tot)

    def SMALL(r):
        n = r.randint(1, 5)
        return f"{n} {r.randint(1, 6)}\n" + "".join(f"{r.randint(1, 5)} {r.randint(1, 8)}\n" for _ in range(n))

    def G():
        r = rng("441B")
        return [("boundary", "n=1 v=1", "1 1\n1 1\n"), ("boundary", "fruit on day 3000 needs day 3001", "1 1\n3000 2\n"),
                ("maxSize", "n=3000 all same day max", "3000 3000\n" + "".join("3000 3000\n" for _ in range(3000))),
                ("maxSize", "n=3000 random", "3000 1500\n" + "".join(f"{r.randint(1, 3000)} {r.randint(1, 3000)}\n" for _ in range(3000))),
                ("adversarial", "carry-over must be taken first", "2 3\n1 5\n2 3\n")]


@problem("445B", "n in [1,50]; 0<=m<=n(n-1)/2; pairs x<y distinct", 0)
class P445B:
    def V(s):
        L = LR(s)
        n, m = L.ints([(1, 50), (0, 1225)])
        need(m <= n * (n - 1) // 2)
        seen = set()
        for _ in range(m):
            x, y = L.same(2, 1, n)
            need(x < y and (x, y) not in seen)
            seen.add((x, y))
        L.done()

    def S(s):
        v = nums(s)
        n, m = v[0], v[1]
        d = DSU(n + 1)
        c = sum(d.u(v[2 + 2 * i], v[3 + 2 * i]) for i in range(m))
        return str(2 ** c)

    def G():
        return [("boundary", "n=1 m=0", "1 0\n"), ("boundary", "n=50 m=0", "50 0\n"),
                ("maxSize", "n=50 complete graph -> 2^49 needs 64-bit", "50 1225\n" + "\n".join(f"{i} {j}" for i in range(1, 51) for j in range(i + 1, 51)) + "\n"),
                ("maxSize", "n=50 path", "50 49\n" + "\n".join(f"{i} {i + 1}" for i in range(1, 50)) + "\n"),
                ("adversarial", "two components", "4 2\n1 2\n3 4\n")]


@problem("479C", "n in [1,5000]; 1<=b<a<=1e9", 300)
class P479C:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 5000)])[0]
        for _ in range(n):
            a, b = L.same(2, 1, 10 ** 9)
            need(b < a)
        L.done()

    def S(s):
        v = nums(s)
        ex = sorted((v[1 + 2 * i], v[2 + 2 * i]) for i in range(v[0]))
        cur = 0
        for a, b in ex:
            cur = b if b >= cur else a
        return str(cur)

    def B(s):
        v = nums(s)
        ex = [(v[1 + 2 * i], v[2 + 2 * i]) for i in range(v[0])]
        best = None
        for perm in permutations(ex):
            if any(perm[i][0] > perm[i + 1][0] for i in range(len(perm) - 1)):
                continue
            for ch in product((0, 1), repeat=len(perm)):
                days = [p[c] for p, c in zip(perm, ch)]
                if all(days[i] <= days[i + 1] for i in range(len(days) - 1)):
                    best = days[-1] if best is None else min(best, days[-1])
        return str(best)

    def SMALL(r):
        n = r.randint(1, 5)
        out = []
        for _ in range(n):
            a = r.randint(2, 8)
            out.append(f"{a} {r.randint(1, a - 1)}")
        return f"{n}\n" + "\n".join(out) + "\n"

    def G():
        r = rng("479C")
        rows = []
        for _ in range(5000):
            a = r.randint(2, 10 ** 9)
            rows.append(f"{a} {r.randint(1, a - 1)}")
        return [("boundary", "n=1", "1\n1000000000 999999999\n"), ("maxSize", "n=5000 random", "5000\n" + "\n".join(rows) + "\n"),
                ("maxSize", "n=5000 equal a, decreasing b", "5000\n" + "\n".join(f"1000000000 {10 ** 9 - 1 - i}" for i in range(5000)) + "\n"),
                ("adversarial", "ties in a resolved by smaller b first", "3\n5 4\n5 1\n5 3\n")]


@problem("492C", "n in [1,1e5]; r in [1,1e9]; avg in [1,min(r,1e6)]; a_i in [1,r], b_i in [1,1e6]", 300)
class P492C:
    def V(s):
        L = LR(s)
        n, r, avg = L.ints([(1, 10 ** 5), (1, 10 ** 9), (1, 10 ** 6)])
        need(avg <= r)
        for _ in range(n):
            L.ints([(1, r), (1, 10 ** 6)])
        L.done()

    def S(s):
        v = nums(s)
        n, r, avg = v[:3]
        ex = sorted((v[4 + 2 * i], v[3 + 2 * i]) for i in range(n))
        need_ = avg * n - sum(a for _, a in ex)
        cost = 0
        for b, a in ex:
            if need_ <= 0:
                break
            t = min(need_, r - a)
            cost += t * b
            need_ -= t
        return str(cost)

    def B(s):
        v = nums(s)
        n, r, avg = v[:3]
        ex = [(v[3 + 2 * i], v[4 + 2 * i]) for i in range(n)]
        best = None
        for inc in product(*[range(r - a + 1) for a, _ in ex]):
            if sum(a + d for (a, _), d in zip(ex, inc)) >= avg * n:
                c = sum(d * b for (_, b), d in zip(ex, inc))
                best = c if best is None else min(best, c)
        return str(best)

    def SMALL(r_):
        n = r_.randint(1, 3)
        r = r_.randint(1, 5)
        return f"{n} {r} {r_.randint(1, r)}\n" + "".join(f"{r_.randint(1, r)} {r_.randint(1, 9)}\n" for _ in range(n))

    def G():
        r = rng("492C")
        N = 10 ** 5
        return [("boundary", "already enough", "1 1 1\n1 1000000\n"), ("maxSize", "n=1e5 r=1e9 avg=1e6 all a=1 b=1e6 (answer ~1e17)", f"{N} 1000000000 1000000\n" + "".join(f"1 1000000\n" for _ in range(N))),
                ("maxSize", "n=1e5 random", f"{N} 1000000 500000\n" + "".join(f"{r.randint(1, 10 ** 6)} {r.randint(1, 10 ** 6)}\n" for _ in range(N))),
                ("adversarial", "cheapest exam capped by r", "2 5 5\n4 1\n1 100\n")]


@problem("493B", "n in [1,2e5]; a_i in [-1e9,1e9], nonzero; one per line", 300)
class P493B:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 2 * 10 ** 5)])[0]
        for _ in range(n):
            need(L.ints([(-10 ** 9, 10 ** 9)])[0] != 0)
        L.done()

    def S(s):
        a = nums(s)[1:]
        f = [x for x in a if x > 0]
        g = [-x for x in a if x < 0]
        if sum(f) != sum(g):
            return "first" if sum(f) > sum(g) else "second"
        if f != g:
            return "first" if f > g else "second"
        return "first" if a[-1] > 0 else "second"

    def B(s):
        a = nums(s)[1:]
        f = [x for x in a if x > 0]
        g = [-x for x in a if x < 0]
        if sum(f) != sum(g):
            return "first" if sum(f) > sum(g) else "second"
        for x, y in zip(f, g):
            if x != y:
                return "first" if x > y else "second"
        if len(f) != len(g):
            return "first" if len(f) > len(g) else "second"
        return "first" if a[-1] > 0 else "second"

    def SMALL(r):
        n = r.randint(1, 7)
        return f"{n}\n" + "".join(f"{r.choice([-1, 1]) * r.randint(1, 3)}\n" for _ in range(n))

    def G():
        N = 2 * 10 ** 5
        return [("boundary", "n=1 second", "1\n-1\n"), ("maxSize", "2e5 max values sum overflow 32-bit, equal sequences, last decides", f"{N}\n" + "".join(f"{10 ** 9 if i % 2 == 0 else -10 ** 9}\n" for i in range(N))),
                ("maxSize", "2e5 prefix-longer wins", f"{N}\n" + "".join("1000000000\n" for _ in range(N // 2)) + "".join("-1000000000\n" for _ in range(N // 2 - 2)) + "-1000000000\n-1000000000\n"),
                ("adversarial", "equal sums, lexicographic differs late", "4\n1\n2\n-1\n-2\n".replace("-2\n", "-2\n")),
                ("adversarial", "equal sums, longer sequence wins", "4\n2\n-1\n-1\n2\n".replace("4\n2\n-1\n-1\n2\n", "3\n-2\n1\n1\n"))]


@problem("505B", "2<=n<=100, 1<=m<=100; edges a<b, c in [1,m], no duplicate (a,b,c); q in [1,100]; u!=v", 0)
class P505B:
    def V(s):
        L = LR(s)
        n, m = L.ints([(2, 100), (1, 100)])
        seen = set()
        for _ in range(m):
            a, b, c = L.ints([(1, n), (1, n), (1, m)])
            need(a < b and (a, b, c) not in seen)
            seen.add((a, b, c))
        q = L.ints([(1, 100)])[0]
        for _ in range(q):
            u, v = L.same(2, 1, n)
            need(u != v)
        L.done()

    def S(s):
        x = nums(s)
        n, m = x[0], x[1]
        ds = {}
        for i in range(m):
            a, b, c = x[2 + 3 * i:5 + 3 * i]
            ds.setdefault(c, DSU(n + 1)).u(a, b)
        q = x[2 + 3 * m]
        out = []
        for i in range(q):
            u, v = x[3 + 3 * m + 2 * i], x[4 + 3 * m + 2 * i]
            out.append(str(sum(d.f(u) == d.f(v) for d in ds.values())))
        return "\n".join(out)

    def G():
        r = rng("505B")
        es = set()
        while len(es) < 100:
            a, b = sorted(r.sample(range(1, 101), 2))
            es.add((a, b, r.randint(1, 100)))
        qs = "\n".join(" ".join(map(str, r.sample(range(1, 101), 2))) for _ in range(100))
        chain = "\n".join(f"{i} {i + 1} 1" for i in range(1, 100))
        return [("boundary", "n=2 one edge", "2 1\n1 2 1\n1\n2 1\n"),
                ("maxSize", "n=100 m=100 random colors", "100 100\n" + "\n".join(f"{a} {b} {c}" for a, b, c in sorted(es)) + f"\n100\n{qs}\n"),
                ("maxSize", "single color chain across all vertices", f"100 100\n{chain}\n1 100 100\n100\n" + "\n".join(f"1 {i}" for i in range(2, 101)) + "\n100 1\n"),
                ("adversarial", "same pair different colors", "3 3\n1 2 1\n1 2 2\n2 3 3\n2\n1 2\n1 3\n")]
