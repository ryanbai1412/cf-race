from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import combinations
from collections import deque
from math import gcd
from collections import Counter
from itertools import permutations, product
from lib import *


def J(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def beautiful(t):
    return set(t) <= set("01") and t.count("1") <= 1 and (t == "0" or t.startswith("1"))


@problem("614B", "n in [1,1e5]; non-negative ai without leading zeros; >=n-1 beautiful; total length <=1e5", 300)
class P614B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 10**5)])
        a = L.line().split()
        need(len(a) == n, "count")
        for t in a:
            need(t.isdigit() and (t == "0" or t[0] != "0"), "leading zero")
        need(sum(not beautiful(t) for t in a) <= 1, "two non-beautiful")
        need(sum(len(t) for t in a) <= 10**5, "total length")
        L.done()

    def S(s):
        a = s.split()[1:]
        if "0" in a:
            return "0"
        head, z = "1", 0
        for t in a:
            if beautiful(t):
                z += len(t) - 1
            else:
                head = t
        return head + "0" * z

    def B(s):
        p = 1
        for t in s.split()[1:]:
            p *= int(t)
        return str(p)

    def SMALL(r):
        n = r.randint(1, 6)
        a = [r.choice(["1", "10", "100", "0" if r.random() < 0.1 else "1000"]) for _ in range(n)]
        if r.random() < 0.7:
            a[r.randrange(n)] = str(r.choice([r.randint(2, 999), r.randint(1, 10**6), 11, 101]))
        return J(n, a)

    def G():
        r = rng("614B")
        return [("boundary", "n=1 single zero", "1\n0\n"), ("boundary", "n=1 non-beautiful", "1\n7\n"),
                ("boundary", "all ones", J(5, ["1"] * 5)),
                ("maxSize", "n=1e5 all '1' (total length 1e5)", J(100000, ["1"] * 100000)),
                ("maxSize", "one huge 10^99999 power", J(1, "1" + "0" * 99999)),
                ("maxSize", "long non-beautiful plus many tens", "49900\n" + " ".join(["10"] * 49899 + ["2" + "3" * 99]) + "\n"),
                ("adversarial", "non-beautiful 11 and 101 looking digits", "3\n11 10 100\n"),
                ("adversarial", "zero among long numbers", "3\n" + "1" + "0" * 500 + " 0 12345\n"),
                ("adversarial", "non-beautiful is last and has zeros", "3\n10 1 1200\n")]


@problem("670D1", "n,k in [1,1000]; ai,bi in [1,1000]", 300)
class P670D1:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 1000), (1, 1000)])
        L.same(n, 1, 1000)
        L.same(n, 1, 1000)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k = v[:2]
        a, b = v[2:2 + n], v[2 + n:2 + 2 * n]
        lo, hi = 0, 3000
        while lo < hi:
            c = (lo + hi + 1) // 2
            if sum(max(0, x * c - y) for x, y in zip(a, b)) <= k:
                lo = c
            else:
                hi = c - 1
        return str(lo)

    def B(s):
        v = list(map(int, s.split()))
        n, k = v[:2]
        a, b = v[2:2 + n], v[2 + n:2 + 2 * n]
        c = 0
        while True:
            need_ = 0
            for x, y in zip(a, b):
                if y >= x:
                    y -= x
                else:
                    need_ += x - y
                    y = 0
            if need_ > k:
                return str(c)
            k -= need_
            b = [max(0, y - x) for x, y in zip(a, b)]
            c += 1

    def SMALL(r):
        n = r.randint(1, 5)
        return J((n, r.randint(1, 30)), [r.randint(1, 8) for _ in range(n)], [r.randint(1, 30) for _ in range(n)])

    def G():
        r = rng("670D1")
        return [("boundary", "all minimal", "1 1\n1\n1\n"), ("boundary", "single max a, max b, max k", "1 1000\n1000\n1000\n"),
                ("boundary", "a=1,b=1000,k=1000 -> 2000", "1 1000\n1\n1000\n"),
                ("maxSize", "n=1000 random", J((1000, 1000), [r.randint(1, 1000) for _ in range(1000)], [r.randint(1, 1000) for _ in range(1000)])),
                ("maxSize", "n=1000 all a=1 b=1000 k=1000", J((1000, 1000), [1] * 1000, [1000] * 1000)),
                ("adversarial", "powder insufficient for even one", J((3, 1), [1000, 1000, 1000], [1, 1, 1])),
                ("adversarial", "one bottleneck ingredient", J((3, 7), [1, 1, 5], [100, 100, 3]))]


@problem("632B", "n in [1,5e5]; pi in [1,1e9]; string of A/B of length n", 300)
class P632B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 5 * 10**5)])
        L.same(n, 1, 10**9)
        w = L.word("AB", n, n)
        L.done()

    def S(s):
        t = s.split()
        n = int(t[0])
        p = list(map(int, t[1:1 + n]))
        w = t[1 + n]
        base = sum(x for x, c in zip(p, w) if c == "B")
        best, d = base, 0
        for x, c in zip(p, w):
            d += x if c == "A" else -x
            best = max(best, base + d)
        d = 0
        for x, c in zip(reversed(p), reversed(w)):
            d += x if c == "A" else -x
            best = max(best, base + d)
        return str(best)

    def B(s):
        t = s.split()
        n = int(t[0])
        p = list(map(int, t[1:1 + n]))
        w = t[1 + n]
        fl = {"A": "B", "B": "A"}
        cands = [w] + [("".join(fl[c] for c in w[:i]) + w[i:]) for i in range(1, n + 1)] + [w[:i] + "".join(fl[c] for c in w[i:]) for i in range(n)]
        return str(max(sum(x for x, c in zip(p, u) if c == "B") for u in cands))

    def SMALL(r):
        n = r.randint(1, 8)
        return J(n, [r.randint(1, 20) for _ in range(n)], "".join(r.choice("AB") for _ in range(n)))

    def G():
        r = rng("632B")
        n = 500000
        return [("boundary", "n=1 A", "1\n1000000000\nA\n"), ("boundary", "n=1 B", "1\n1\nB\n"),
                ("maxSize", "n=5e5 all A max p (answer 5e14)", J(n, [10**9] * n, "A" * n)),
                ("maxSize", "n=5e5 random", J(n, [r.randint(1, 10**9) for _ in range(n)], "".join(r.choice("AB") for _ in range(n)))),
                ("maxSize", "n=5e5 all B (do nothing)", J(n, [r.randint(1, 10**9) for _ in range(n)], "B" * n)),
                ("adversarial", "best is a suffix, prefix flips lose", "5\n9 1 1 1 9\nBAAAA\n"),
                ("adversarial", "best is a prefix", "4\n5 5 1 1\nAABB\n")]


@problem("710B", "n in [1,3e5]; xi in [-1e9,1e9]", 300)
class P710B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 3 * 10**5)])
        L.same(n, -10**9, 10**9)
        L.done()

    def S(s):
        x = sorted(map(int, s.split()[1:]))
        return str(x[(len(x) - 1) // 2])

    def B(s):
        x = list(map(int, s.split()[1:]))
        best = None
        for c in range(min(x), max(x) + 1):
            v = sum(abs(c - y) for y in x)
            if best is None or v < best[0]:
                best = (v, c)
        return str(best[1])

    def SMALL(r):
        n = r.randint(1, 7)
        return J(n, [r.randint(-6, 6) for _ in range(n)])

    def G():
        r = rng("710B")
        n = 300000
        return [("boundary", "n=1 min", "1\n-1000000000\n"), ("boundary", "n=2 extremes leftmost", "2\n1000000000 -1000000000\n"),
                ("maxSize", "n=3e5 random full range", J(n, [r.randint(-10**9, 10**9) for _ in range(n)])),
                ("maxSize", "n=3e5 all equal", J(n, [7] * n)),
                ("adversarial", "even n unsorted, leftmost median", "4\n10 -5 3 3\n"),
                ("adversarial", "n=3e5 descending", J(n, list(range(n, 0, -1))))]


@problem("604B", "1<=n<=2k<=1e5; 1<=s1<=...<=sn<=1e6", 300)
class P604B:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 10**5), (1, 10**5)])
        need(n <= 2 * k <= 10**5, "n<=2k<=1e5")
        a = L.same(n, 1, 10**6)
        need(a == sorted(a), "not sorted")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        p = max(0, n - k)
        best = a[-1]
        for i in range(p):
            best = max(best, a[i] + a[2 * p - 1 - i])
        return str(best)

    def B(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        best = None

        def go(rest, boxes, cur):
            nonlocal best
            if not rest:
                if best is None or cur < best:
                    best = cur
                return
            if boxes == 0:
                return
            x, rest2 = rest[0], rest[1:]
            go(rest2, boxes - 1, max(cur, x))
            for j in range(len(rest2)):
                go(rest2[:j] + rest2[j + 1:], boxes - 1, max(cur, x + rest2[j]))
        go(a, k, 0)
        return str(best)

    def SMALL(r):
        k = r.randint(1, 4)
        n = r.randint(1, 2 * k)
        return J((n, k), sorted(r.randint(1, 20) for _ in range(n)))

    def G():
        r = rng("604B")
        return [("boundary", "n=k=1", "1 1\n1\n"), ("boundary", "n=1 big k", "1 50000\n1000000\n"),
                ("maxSize", "n=2k=1e5 random", J((100000, 50000), sorted(r.randint(1, 10**6) for _ in range(100000)))),
                ("maxSize", "n=2k all 1e6 (answer 2e6)", J((100000, 50000), [10**6] * 100000)),
                ("maxSize", "n=k=1e5/2 singles only", J((50000, 50000), sorted(r.randint(1, 10**6) for _ in range(50000)))),
                ("adversarial", "largest single dominates pairs", "3 2\n1 1 100\n"),
                ("adversarial", "pairing must match smallest with largest paired", "6 4\n1 2 3 4 50 60\n")]


@problem("637C", "n in [1,1000]; distinct six-digit codes (leading zeros allowed)", 0)
class P637C:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 1000)])
        c = [L.word("0123456789", 6, 6) for _ in range(n)]
        need(len(set(c)) == n, "duplicate")
        L.done()

    def S(s):
        c = s.split()[1:]
        d = 12
        for i in range(len(c)):
            for j in range(i):
                h = sum(x != y for x, y in zip(c[i], c[j]))
                if h < d:
                    d = h
        return "6" if len(c) == 1 else str((d - 1) // 2)

    def SMALL(r):
        n = r.randint(1, 6)
        return J(n, *r.sample([f"{x:06d}" for x in r.sample(range(10**6), 30)], n))

    def G():
        r = rng("637C")
        codes = [f"{x:06d}" for x in r.sample(range(10**6), 1000)]
        far = [f"{d}" * 6 for d in range(10)]
        return [("boundary", "n=1 answer 6", "1\n000000\n"), ("boundary", "n=2 differ in all 6", "2\n000000\n999999\n"),
                ("maxSize", "n=1000 random codes", J(1000, *codes)),
                ("maxSize", "n=1000 consecutive (distance 1)", J(1000, *[f"{x:06d}" for x in range(1000)])),
                ("adversarial", "ten codes pairwise distance 6", J(10, *far)),
                ("adversarial", "minimum distance 2 -> 0", "3\n000000\n000011\n111111\n"),
                ("adversarial", "minimum distance 4 -> 1", "2\n123456\n100006\n")]


@problem("612C", "non-empty string of <>{}[]() with length <=1e6", 300)
class P612C:
    def V(s):
        L = LR(s)
        L.word("<>{}[]()", 1, 10**6)
        L.done()

    def S(s):
        w = s.split()[0]
        pair = {")": "(", "]": "[", "}": "{", ">": "<"}
        st, c = [], 0
        for ch in w:
            if ch in pair:
                if not st:
                    return "Impossible"
                if st.pop() != pair[ch]:
                    c += 1
            else:
                st.append(ch)
        return "Impossible" if st else str(c)

    def B(s):
        w = s.split()[0]
        n = len(w)
        if n % 2:
            return "Impossible"
        op = "<{[("
        cl = ">}])"
        INF = 10**9
        dp = [[0 if l > r else INF for r in range(n)] for l in range(n + 1)]
        for ln in range(2, n + 1, 2):
            for l in range(n - ln + 1):
                r = l + ln - 1
                if w[l] in op:
                    for m in range(l + 1, r + 1, 2):
                        if w[m] in cl:
                            cost = 0 if op.index(w[l]) == cl.index(w[m]) else 1
                            inner = dp[l + 1][m - 1] if l + 1 <= m - 1 else 0
                            rest = dp[m + 1][r] if m + 1 <= r else 0
                            dp[l][r] = min(dp[l][r], cost + inner + rest)
        return "Impossible" if dp[0][n - 1] >= INF else str(dp[0][n - 1])

    def SMALL(r):
        return "".join(r.choice(r.choice(["<>{}[]()", "([)]", "(("])) for _ in range(r.randint(1, 10))) + "\n"

    def G():
        r = rng("612C")
        half = 500000
        opens = "".join(r.choice("<{[(") for _ in range(half))
        cls = "".join(r.choice(">}])") for _ in range(half))
        return [("boundary", "single char", "(\n"), ("boundary", "single close", ">\n"), ("boundary", "pair ok", "()\n"),
                ("maxSize", "1e6 deep nesting random kinds", opens + cls + "\n"),
                ("maxSize", "1e6 alternating pairs '()' ", "()" * half + "\n"),
                ("maxSize", "1e6 random brackets", "".join(r.choice("<>{}[]()") for _ in range(10**6)) + "\n"),
                ("maxSize", "1e6 all opens", "(" * 10**6 + "\n"),
                ("adversarial", "balanced count but wrong order", ")(\n"),
                ("adversarial", "extra open at end", "()()(\n")]


@problem("665B", "n,k in [1,100], m in [1,k]; initial row is permutation of 1..k; orders distinct items", 300)
class P665B:
    def V(s):
        L = LR(s)
        n, m, k = L.ints([(1, 100), (1, 100), (1, 100)])
        need(m <= k, "m>k")
        p = L.same(k, 1, k)
        need(len(set(p)) == k, "not distinct")
        for _ in range(n):
            o = L.same(m, 1, k)
            need(len(set(o)) == m, "order not distinct")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, m, k = v[:3]
        row = v[3:3 + k]
        t, p = 0, 3 + k
        for _ in range(n * m):
            x = v[p]
            p += 1
            i = row.index(x)
            t += i + 1
            row.pop(i)
            row.insert(0, x)
        return str(t)

    def B(s):
        v = list(map(int, s.split()))
        n, m, k = v[:3]
        pos = {x: i + 1 for i, x in enumerate(v[3:3 + k])}
        t = 0
        for x in v[3 + k:]:
            q = pos[x]
            t += q
            for y in pos:
                if pos[y] < q:
                    pos[y] += 1
            pos[x] = 1
        return str(t)

    def SMALL(r):
        k = r.randint(1, 6)
        n, m = r.randint(1, 4), r.randint(1, k)
        p = list(range(1, k + 1))
        r.shuffle(p)
        return J((n, m, k), p, *[r.sample(range(1, k + 1), m) for _ in range(n)])

    def G():
        r = rng("665B")
        p = list(range(1, 101))
        r.shuffle(p)
        return [("boundary", "n=m=k=1", "1 1 1\n1\n1\n"),
                ("maxSize", "n=k=m=100 random", J((100, 100, 100), p, *[r.sample(range(1, 101), 100) for _ in range(100)])),
                ("maxSize", "n=k=m=100 reverse orders (worst positions)", J((100, 100, 100), list(range(1, 101)), *[list(range(100, 0, -1))] * 100)),
                ("adversarial", "same item repeatedly accessed across orders", J((5, 1, 3), [3, 2, 1], *[[1]] * 5)),
                ("adversarial", "item at last position each time", J((3, 3, 3), [1, 2, 3], [3, 2, 1], [1, 2, 3], [3, 1, 2]))]


@problem("748C", "n in [1,2e5]; protocol of n letters from LRUD", 300)
class P748C:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 2 * 10**5)])
        L.word("LRUD", n, n)
        L.done()

    def S(s):
        w = s.split()[1]
        opp = {"L": "R", "R": "L", "U": "D", "D": "U"}
        cnt, cur = 1, set()
        for ch in w:
            if opp[ch] in cur:
                cnt += 1
                cur = set()
            cur.add(ch)
        return str(cnt)

    def B(s):
        w = s.split()[1]
        n = len(w)
        pos = [(0, 0)]
        dd = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}
        for ch in w:
            x, y = pos[-1]
            pos.append((x + dd[ch][0], y + dd[ch][1]))
        INF = 10**9
        f = [0] + [INF] * n
        for j in range(1, n + 1):
            for i in range(j):
                if abs(pos[j][0] - pos[i][0]) + abs(pos[j][1] - pos[i][1]) == j - i:
                    f[j] = min(f[j], f[i] + 1)
        return str(f[n])

    def SMALL(r):
        n = r.randint(1, 12)
        return J(n, "".join(r.choice(r.choice(["LRUD", "RU", "LR"])) for _ in range(n)))

    def G():
        r = rng("748C")
        n = 200000
        return [("boundary", "n=1", "1\nL\n"), ("boundary", "n=2 reversal", "2\nUD\n"),
                ("maxSize", "n=2e5 random", J(n, "".join(r.choice("LRUD") for _ in range(n)))),
                ("maxSize", "n=2e5 LRLR... answer n", J(n, "LR" * (n // 2))),
                ("maxSize", "n=2e5 staircase RU answer 1", J(n, "RU" * (n // 2))),
                ("adversarial", "turn back after two perpendicular moves", "3\nRUL\n"),
                ("adversarial", "long run then reverse", J(6, "RRRLLL"))]


@problem("797B", "n in [1,1e5]; ai in [-1e4,1e4]; some subsequence has odd sum", 300)
class P797B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 10**5)])
        a = L.same(n, -10**4, 10**4)
        need(any(x % 2 for x in a), "no odd element")
        L.done()

    def S(s):
        a = list(map(int, s.split()))[1:]
        tot = sum(x for x in a if x > 0)
        if tot % 2:
            return str(tot)
        best = None
        for x in a:
            if x % 2:
                v = tot - x if x > 0 else tot + x
                if best is None or v > best:
                    best = v
        return str(best)

    def B(s):
        a = list(map(int, s.split()))[1:]
        n = len(a)
        best = None
        for m in range(1, 1 << n):
            v = sum(a[i] for i in range(n) if m >> i & 1)
            if v % 2 and (best is None or v > best):
                best = v
        return str(best)

    def SMALL(r):
        n = r.randint(1, 9)
        a = [r.randint(-9, 9) for _ in range(n)]
        if not any(x % 2 for x in a):
            a[r.randrange(n)] = r.choice([-7, -1, 3])
        return J(n, a)

    def G():
        r = rng("797B")
        n = 100000
        return [("boundary", "n=1 negative odd", "1\n-10000\n".replace("-10000", "-9999")),
                ("boundary", "n=1 positive odd", "1\n9999\n"),
                ("maxSize", "n=1e5 random", J(n, [r.randint(-10**4, 10**4) for _ in range(n)])),
                ("maxSize", "n=1e5 all 10000 except one -9999", J(n, [10**4] * (n - 1) + [-9999])),
                ("maxSize", "n=1e5 all -9999", J(n, [-9999] * n)),
                ("adversarial", "even total, best to add largest nonpositive odd", "3\n4 6 -1\n"),
                ("adversarial", "even total, best to drop smallest positive odd", "4\n3 5 -7 2\n"),
                ("adversarial", "zeros and one odd", "4\n0 0 -3 0\n")]


@problem("757B", "n in [1,1e5]; si in [1,1e5]", 300)
class P757B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 10**5)])
        L.same(n, 1, 10**5)
        L.done()

    def S(s):
        a = list(map(int, s.split()))[1:]
        M = max(a)
        c = [0] * (M + 1)
        for x in a:
            c[x] += 1
        best = 1
        for d in range(2, M + 1):
            t = sum(c[d::d])
            if t > best:
                best = t
        return str(best)

    def B(s):
        a = list(map(int, s.split()))[1:]
        n = len(a)
        best = 1
        for m in range(1, 1 << n):
            g, k = 0, 0
            for i in range(n):
                if m >> i & 1:
                    g, k = gcd(g, a[i]), k + 1
            if k > 1 and g != 1:
                best = max(best, k)
        return str(best)

    def SMALL(r):
        n = r.randint(1, 9)
        return J(n, [r.randint(1, 30) for _ in range(n)])

    def G():
        r = rng("757B")
        n = 100000
        return [("boundary", "n=1 s=1", "1\n1\n"), ("boundary", "all ones -> 1", "4\n1 1 1 1\n"),
                ("maxSize", "n=1e5 random", J(n, [r.randint(1, 10**5) for _ in range(n)])),
                ("maxSize", "n=1e5 all 1e5", J(n, [10**5] * n)),
                ("maxSize", "n=1e5 distinct 1..1e5", J(n, list(range(1, n + 1)))),
                ("adversarial", "pairwise coprime primes -> 1", "5\n2 3 5 7 11\n"),
                ("adversarial", "best divisor is large prime", "5\n99991 99991 2 3 99991\n")]


@problem("799B", "n,m in [1,2e5]; distinct pi in [1,1e9]; colors in [1,3]", 300)
class P799B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 2 * 10**5)])
        p = L.same(n, 1, 10**9)
        need(len(set(p)) == n, "prices not distinct")
        L.same(n, 1, 3)
        L.same(n, 1, 3)
        m, = L.ints([(1, 2 * 10**5)])
        L.same(m, 1, 3)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n = v[0]
        p, a, b = v[1:1 + n], v[1 + n:1 + 2 * n], v[1 + 2 * n:1 + 3 * n]
        c = v[2 + 3 * n:]
        order = sorted(range(n), key=lambda i: p[i])
        lists = {k: [i for i in order if a[i] == k or b[i] == k] for k in (1, 2, 3)}
        ptr = {1: 0, 2: 0, 3: 0}
        sold = [False] * n
        out = []
        for k in c:
            L_ = lists[k]
            while ptr[k] < len(L_) and sold[L_[ptr[k]]]:
                ptr[k] += 1
            if ptr[k] == len(L_):
                out.append(-1)
            else:
                i = L_[ptr[k]]
                sold[i] = True
                out.append(p[i])
        return " ".join(map(str, out))

    def B(s):
        v = list(map(int, s.split()))
        n = v[0]
        p, a, b = v[1:1 + n], v[1 + n:1 + 2 * n], v[1 + 2 * n:1 + 3 * n]
        left = set(range(n))
        out = []
        for k in v[2 + 3 * n:]:
            ok = [i for i in left if a[i] == k or b[i] == k]
            if ok:
                i = min(ok, key=lambda i: p[i])
                left.remove(i)
                out.append(p[i])
            else:
                out.append(-1)
        return " ".join(map(str, out))

    def SMALL(r):
        n, m = r.randint(1, 6), r.randint(1, 8)
        return J(n, r.sample(range(1, 50), n), [r.randint(1, 3) for _ in range(n)], [r.randint(1, 3) for _ in range(n)], m, [r.randint(1, 3) for _ in range(m)])

    def G():
        r = rng("799B")
        n = 200000
        p = r.sample(range(1, 10**9 + 1), n)
        return [("boundary", "n=m=1 no match", "1\n5\n1\n1\n1\n2\n"), ("boundary", "n=m=1 match back", "1\n1000000000\n1\n3\n1\n3\n"),
                ("maxSize", "n=m=2e5 random", J(n, p, [r.randint(1, 3) for _ in range(n)], [r.randint(1, 3) for _ in range(n)], n, [r.randint(1, 3) for _ in range(n)])),
                ("maxSize", "n=m=2e5 all color 1 buyers color 1 then -1s", J(n, p, [1] * n, [1] * n, n, [1] * (n // 2) + [2] * (n // 2))),
                ("adversarial", "shirt sold via front then not available via back", "2\n1 2\n1 2\n2 1\n3\n2 1 2\n"),
                ("adversarial", "more buyers than shirts", "1\n7\n2\n3\n4\n3 2 3 1\n")]


@problem("713A", "t in [1,1e5]; + / - ai in [0,1e18) without leading zeros; ? pattern of 0/1 length 1..18; removals valid; >=1 query", 300)
class P713A:
    def V(s):
        L = LR(s)
        t, = L.ints([(1, 10**5)])
        ms, q = Counter(), 0
        for _ in range(t):
            ts = L.line().split()
            need(len(ts) == 2 and ts[0] in "+-?", "bad op")
            if ts[0] == "?":
                need(1 <= len(ts[1]) <= 18 and set(ts[1]) <= set("01"), "pattern")
                q += 1
            else:
                x = intok(ts[1], 0, 10**18 - 1)
                if ts[0] == "+":
                    ms[x] += 1
                else:
                    need(ms[x] > 0, "remove missing")
                    ms[x] -= 1
        need(q >= 1, "no query")
        L.done()

    def S(s):
        rows = s.split("\n")
        t = int(rows[0])
        cnt = Counter()
        out = []
        for row in rows[1:1 + t]:
            op, x = row.split()
            if op == "?":
                out.append(str(cnt[x.lstrip("0")]))
            else:
                key = "".join(str(int(d) & 1) for d in x).lstrip("0")
                cnt[key] += 1 if op == "+" else -1
        return "\n".join(out)

    def B(s):
        rows = s.split("\n")
        t = int(rows[0])
        ms = []
        out = []
        for row in rows[1:1 + t]:
            op, x = row.split()
            if op == "+":
                ms.append(int(x))
            elif op == "-":
                ms.remove(int(x))
            else:
                pat = x.zfill(18)
                out.append(str(sum(all(int(d) % 2 == int(c) for d, c in zip(str(y).zfill(18), pat)) for y in ms)))
        return "\n".join(out)

    def SMALL(r):
        t = r.randint(1, 10)
        ms, rows = [], []
        for _ in range(t - 1):
            k = r.random()
            if k < 0.45 or (k < 0.65 and not ms):
                x = r.choice([r.randint(0, 99), r.randint(0, 10**18 - 1)])
                ms.append(x)
                rows.append(f"+ {x}")
            elif k < 0.65:
                x = r.choice(ms)
                ms.remove(x)
                rows.append(f"- {x}")
            else:
                rows.append("? " + "".join(r.choice("01") for _ in range(r.randint(1, 4))))
        rows.append("? " + "".join(r.choice("01") for _ in range(r.randint(1, 18))))
        return J(t, *rows)

    def G():
        r = rng("713A")
        t = 100000
        rows, ms = [], []
        for i in range(t - 1):
            k = r.random()
            if k < 0.5 or not ms:
                x = r.randint(0, 10**18 - 1)
                ms.append(x)
                rows.append(f"+ {x}")
            elif k < 0.6:
                j = r.randrange(len(ms))
                ms[j], ms[-1] = ms[-1], ms[j]
                rows.append(f"- {ms.pop()}")
            else:
                rows.append("? " + "".join(r.choice("01") for _ in range(r.randint(1, 18))))
        rows.append("? " + "0" * 18)
        same = ["+ 0"] * 50000 + ["? 0"] * 49999 + ["? 000000000000000000"]
        return [("boundary", "single query empty multiset", "1\n? 0\n"),
                ("boundary", "max value 999..9 vs pattern 18 ones", "2\n+ 999999999999999999\n? 111111111111111111\n"),
                ("maxSize", "t=1e5 random mixed", J(t, *rows)),
                ("maxSize", "t=1e5 zeros added then queried", J(t, *same)),
                ("adversarial", "pattern leading zeros and short numbers", "5\n+ 1\n+ 241\n? 1\n? 00001\n? 101\n"),
                ("adversarial", "add/remove same value repeatedly", "6\n+ 12\n+ 12\n- 12\n? 10\n- 12\n? 10\n")]


@problem("762B", "a,b,c in [0,1e5]; m in [0,3e5]; vali in [1,1e9]; type USB or PS/2", 300)
class P762B:
    def V(s):
        L = LR(s)
        L.ints([(0, 10**5)] * 3)
        m, = L.ints([(0, 3 * 10**5)])
        for _ in range(m):
            ts = L.line().split()
            need(len(ts) == 2 and ts[1] in ("USB", "PS/2"), "bad mouse")
            intok(ts[0], 1, 10**9)
        L.done()

    def S(s):
        t = s.split()
        a, b, c, m = map(int, t[:4])
        u = sorted(int(t[4 + 2 * i]) for i in range(m) if t[5 + 2 * i] == "USB")
        p = sorted(int(t[4 + 2 * i]) for i in range(m) if t[5 + 2 * i] == "PS/2")
        rest = sorted(u[a:] + p[b:])[:c]
        chosen = u[:a] + p[:b] + rest
        return f"{len(chosen)} {sum(chosen)}"

    def B(s):
        t = s.split()
        a, b, c, m = map(int, t[:4])
        mice = [(int(t[4 + 2 * i]), t[5 + 2 * i]) for i in range(m)]
        best = (0, 0)
        for mk in range(1 << m):
            sel = [mice[i] for i in range(m) if mk >> i & 1]
            nu = sum(1 for _, k in sel if k == "USB")
            np_ = len(sel) - nu
            if max(0, nu - a) + max(0, np_ - b) <= c:
                cand = (len(sel), -sum(v for v, _ in sel))
                best = max(best, cand)
        return f"{best[0]} {-best[1]}"

    def SMALL(r):
        m = r.randint(0, 8)
        return J((r.randint(0, 3), r.randint(0, 3), r.randint(0, 3)), m, *[(r.randint(1, 20), r.choice(["USB", "PS/2"])) for _ in range(m)])

    def G():
        r = rng("762B")
        m = 300000
        return [("boundary", "m=0", "0 0 0\n0\n"), ("boundary", "no computers", "0 0 0\n2\n5 USB\n6 PS/2\n"),
                ("boundary", "only both-port computers", "0 0 2\n3\n5 USB\n1 PS/2\n4 USB\n"),
                ("maxSize", "m=3e5 random, a=b=c=1e5", J((10**5, 10**5, 10**5), m, *[(r.randint(1, 10**9), r.choice(["USB", "PS/2"])) for _ in range(m)])),
                ("maxSize", "m=3e5 all 1e9 USB (overflow sum 1e14)", J((10**5, 10**5, 10**5), m, *[(10**9, "USB")] * m)),
                ("adversarial", "leftovers merge across types for c", "1 1 2\n6\n10 USB\n1 USB\n2 USB\n9 PS/2\n3 PS/2\n4 PS/2\n"),
                ("adversarial", "fewer mice than computers", "5 5 5\n2\n7 PS/2\n8 USB\n")]


@problem("719B", "n in [1,1e5]; string of b/r length n", 300)
class P719B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 10**5)])
        L.word("br", n, n)
        L.done()

    def S(s):
        w = s.split()[1]
        best = None
        for first in "br":
            x = y = 0
            for i, ch in enumerate(w):
                want = first if i % 2 == 0 else ("r" if first == "b" else "b")
                if ch != want:
                    if ch == "r":
                        x += 1
                    else:
                        y += 1
            v = max(x, y)
            best = v if best is None else min(best, v)
        return str(best)

    def B(s):
        w = s.split()[1]
        n = len(w)
        goals = {"".join("br"[(i + f) % 2] for i in range(n)) for f in (0, 1)}
        dist = {w: 0}
        dq = deque([w])
        while dq:
            u = dq.popleft()
            if u in goals:
                return str(dist[u])
            nxt = []
            for i in range(n):
                nxt.append(u[:i] + ("r" if u[i] == "b" else "b") + u[i + 1:])
                for j in range(i + 1, n):
                    if u[i] != u[j]:
                        l = list(u)
                        l[i], l[j] = l[j], l[i]
                        nxt.append("".join(l))
            for v in nxt:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    dq.append(v)

    def SMALL(r):
        n = r.randint(1, 8)
        return J(n, "".join(r.choice("br") for _ in range(n)))

    def G():
        r = rng("719B")
        n = 100000
        return [("boundary", "n=1", "1\nb\n"), ("boundary", "n=2 same", "2\nrr\n"),
                ("maxSize", "n=1e5 random", J(n, "".join(r.choice("br") for _ in range(n)))),
                ("maxSize", "n=1e5 all b", J(n, "b" * n)),
                ("maxSize", "n=1e5 pairs bbrr (swaps)", J(n, "bbrr" * (n // 4))),
                ("adversarial", "swap beats repaint", "4\nrbbr\n"),
                ("adversarial", "already alternating starting r", "5\nrbrbr\n")]


@problem("816B", "1<=k<=n<=2e5, q in [1,2e5]; 1<=li<=ri<=2e5; 1<=a<=b<=2e5", 200)
class P816B:
    def V(s):
        L = LR(s)
        n, k, q = L.ints([(1, 2 * 10**5)] * 3)
        need(k <= n, "k>n")
        for _ in range(n + q):
            l, r_ = L.ints([(1, 2 * 10**5)] * 2)
            need(l <= r_, "l>r")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k, q = v[:3]
        M = 200002
        d = [0] * M
        for i in range(n):
            d[v[3 + 2 * i]] += 1
            d[v[4 + 2 * i] + 1] -= 1
        pre = [0] * M
        c = 0
        for t in range(1, M):
            c += d[t]
            pre[t] = pre[t - 1] + (c >= k)
        p = 3 + 2 * n
        return "\n".join(str(pre[v[p + 2 * j + 1]] - pre[v[p + 2 * j] - 1]) for j in range(q))

    def B(s):
        v = list(map(int, s.split()))
        n, k, q = v[:3]
        rec = [(v[3 + 2 * i], v[4 + 2 * i]) for i in range(n)]
        p = 3 + 2 * n
        out = []
        for j in range(q):
            a, b = v[p + 2 * j], v[p + 2 * j + 1]
            out.append(str(sum(sum(l <= t <= r_ for l, r_ in rec) >= k for t in range(a, b + 1))))
        return "\n".join(out)

    def SMALL(r):
        n, q = r.randint(1, 5), r.randint(1, 5)
        def seg(hi):
            a, b = r.randint(1, hi), r.randint(1, hi)
            return (min(a, b), max(a, b))
        return J((n, r.randint(1, n), q), *[seg(15) for _ in range(n)], *[seg(15) for _ in range(q)])

    def G():
        r = rng("816B")
        N = 200000
        def seg():
            a, b = r.randint(1, N), r.randint(1, N)
            return (min(a, b), max(a, b))
        return [("boundary", "n=k=q=1 full range", "1 1 1\n1 200000\n1 200000\n"),
                ("boundary", "point recipe at max", "1 1 1\n200000 200000\n199999 200000\n"),
                ("maxSize", "n=q=2e5 random k=1000", J((N, 1000, N), *[seg() for _ in range(N)], *[seg() for _ in range(N)])),
                ("maxSize", "n=q=2e5 all full range k=n", J((N, N, N), *[(1, N)] * N, *[seg() for _ in range(N)])),
                ("adversarial", "touching endpoints counted inclusive", "2 2 2\n1 5\n5 9\n5 5\n1 9\n"),
                ("adversarial", "k=n with one disjoint recipe -> 0", "3 3 1\n1 10\n2 9\n11 12\n1 200000\n")]


@problem("920C", "n in [2,2e5]; permutation of 1..n; string of n-1 0/1", 300)
class P920C:
    def V(s):
        L = LR(s)
        n, = L.ints([(2, 2 * 10**5)])
        a = L.same(n, 1, 2 * 10**5)
        need(sorted(a) == list(range(1, n + 1)), "not permutation")
        L.word("01", n - 1, n - 1)
        L.done()

    def S(s):
        t = s.split()
        n = int(t[0])
        a = list(map(int, t[1:1 + n]))
        w = t[1 + n]
        mx = 0
        for i in range(n - 1):
            mx = max(mx, a[i])
            if w[i] == "0" and mx > i + 1:
                return "NO"
        return "YES"

    def B(s):
        t = s.split()
        n = int(t[0])
        a = list(map(int, t[1:1 + n]))
        w = t[1 + n]
        ch = True
        while ch:
            ch = False
            for i in range(n - 1):
                if w[i] == "1" and a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
                    ch = True
        return "YES" if a == sorted(a) else "NO"

    def SMALL(r):
        n = r.randint(2, 8)
        a = list(range(1, n + 1))
        r.shuffle(a)
        if r.random() < 0.3:
            a.sort()
        return J(n, a, "".join(r.choice("01") if r.random() < 0.6 else "1" for _ in range(n - 1)))

    def G():
        r = rng("920C")
        n = 200000
        a = list(range(1, n + 1))
        blocks = []
        i = 0
        while i < n:
            ln = min(n - i, r.randint(1, 50))
            b = a[i:i + ln]
            r.shuffle(b)
            blocks.append((b, ln))
            i += ln
        arr = [x for b, _ in blocks for x in b]
        w = "".join("1" * (ln - 1) + "0" for _, ln in blocks)[:n - 1]
        shuffled = a[:]
        r.shuffle(shuffled)
        return [("boundary", "n=2 swapped, forbidden", "2\n2 1\n0\n"), ("boundary", "n=2 swapped, allowed", "2\n2 1\n1\n"),
                ("maxSize", "n=2e5 block-shuffled matching segments YES", J(n, arr, w)),
                ("maxSize", "n=2e5 reversed all allowed YES", J(n, a[::-1], "1" * (n - 1))),
                ("maxSize", "n=2e5 random perm with one 0 NO", J(n, shuffled, "1" * (n // 2) + "0" + "1" * (n - 2 - n // 2))),
                ("maxSize", "n=2e5 sorted all forbidden YES", J(n, a, "0" * (n - 1))),
                ("adversarial", "element must cross a forbidden edge late", "5\n1 3 2 5 4\n1011\n")]


@problem("81A", "single line of 1..2e5 lowercase letters; result non-empty", 300)
class P81A:
    def V(s):
        L = LR(s)
        w = L.word(LOWER, 1, 2 * 10**5)
        L.done()
        st = []
        for ch in w:
            if st and st[-1] == ch:
                st.pop()
            else:
                st.append(ch)
        need(st, "empty result")

    def S(s):
        st = []
        for ch in s.split()[0]:
            if st and st[-1] == ch:
                st.pop()
            else:
                st.append(ch)
        return "".join(st)

    def B(s):
        w = s.split()[0]
        while True:
            for i in range(len(w) - 1):
                if w[i] == w[i + 1]:
                    w = w[:i] + w[i + 2:]
                    break
            else:
                return w

    def SMALL(r):
        while True:
            w = "".join(r.choice("ab") for _ in range(r.randint(1, 12)))
            st = []
            for ch in w:
                if st and st[-1] == ch:
                    st.pop()
                else:
                    st.append(ch)
            if st:
                return w + "\n"

    def G():
        r = rng("81A")
        half = "".join(r.choice(LOWER) for _ in range(99999))
        return [("boundary", "single letter", "z\n"), ("boundary", "triple collapses to one", "aaa\n"),
                ("maxSize", "palindrome-collapse 2e5-1 to single middle", half + "q" + half[::-1] + "\n"),
                ("maxSize", "2e5 random over 'ab' (non-empty)", "a" + "".join(r.choice("ab") for _ in range(199998)) + "c\n"),
                ("maxSize", "2e5 alternating no removals", "ab" * 100000 + "\n"),
                ("adversarial", "cascade abba then remaining", "xabbay\n"), ("adversarial", "sample-like nested", "abccbaz\n")]


@problem("928B", "n in [1,1e5], k in [0,n]; 0<=ai<i", 200)
class P928B:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 10**5), (0, 10**5)])
        need(k <= n, "k>n")
        a = L.same(n, 0, n)
        need(all(a[i] < i + 1 for i in range(n)), "ai>=i")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        res = [0] * (n + 1)
        for x in range(1, n + 1):
            lo, hi = max(1, x - k), min(n, x + k)
            y = a[x - 1]
            if y == 0:
                res[x] = hi - lo + 1
            else:
                yhi = min(n, y + k)
                res[x] = res[y] + (hi - lo + 1) - max(0, yhi - lo + 1)
        return " ".join(map(str, res[1:]))

    def B(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        out = []
        for t in range(1, n + 1):
            seen, x = set(), t
            while True:
                seen.update(range(max(1, x - k), min(n, x + k) + 1))
                if a[x - 1] == 0:
                    break
                x = a[x - 1]
            out.append(len(seen))
        return " ".join(map(str, out))

    def SMALL(r):
        n = r.randint(1, 9)
        return J((n, r.randint(0, n)), [r.randint(0, i) for i in range(n)])

    def G():
        r = rng("928B")
        n = 100000
        return [("boundary", "n=1 k=0", "1 0\n0\n"), ("boundary", "n=1 k=1", "1 1\n0\n"),
                ("maxSize", "n=1e5 chain to previous, k=0 (answer i)", J((n, 0), list(range(n)))),
                ("maxSize", "n=1e5 random links k=3", J((n, 3), [r.randint(0, i) for i in range(n)])),
                ("maxSize", "n=1e5 k=n all no links", J((n, n), [0] * n)),
                ("maxSize", "n=1e5 random links k=500", J((n, 500), [r.randint(max(0, i - 2000), i) for i in range(n)])),
                ("adversarial", "overlapping windows along chain", "5 1\n0 1 2 3 4\n"),
                ("adversarial", "link skips far back, disjoint windows", "6 1\n0 0 0 0 0 1\n")]


@problem("804B", "string of a/b with length 1..1e6", 300)
class P804B:
    def V(s):
        L = LR(s)
        L.word("ab", 1, 10**6)
        L.done()

    def S(s):
        MOD = 10**9 + 7
        ans, b = 0, 0
        for ch in reversed(s.split()[0]):
            if ch == "b":
                b += 1
            else:
                ans = (ans + b) % MOD
                b = b * 2 % MOD
        return str(ans)

    def B(s):
        w = s.split()[0]
        c = 0
        while "ab" in w:
            w = w.replace("ab", "bba", 1)
            c += 1
        return str(c % (10**9 + 7))

    def SMALL(r):
        return "".join(r.choice("ab") for _ in range(r.randint(1, 7))) + "\n"

    def G():
        r = rng("804B")
        n = 10**6
        return [("boundary", "single a", "a\n"), ("boundary", "single b", "b\n"), ("boundary", "ab", "ab\n"),
                ("maxSize", "1e6 a's then... a^999999 b (modular wrap)", "a" * 999999 + "b\n"),
                ("maxSize", "1e6 random", "".join(r.choice("ab") for _ in range(n)) + "\n"),
                ("maxSize", "1e6 b's then a's (answer 0)", "b" * 500000 + "a" * 500000 + "\n"),
                ("adversarial", "aabb", "aabb\n"), ("adversarial", "baba", "baba\n")]


@problem("888C", "1<=|s|<=1e5 lowercase", 300)
class P888C:
    def V(s):
        L = LR(s)
        L.word(LOWER, 1, 10**5)
        L.done()

    def S(s):
        w = s.split()[0]
        n = len(w)
        last, gap = {}, {}
        for i, ch in enumerate(w):
            gap[ch] = max(gap.get(ch, 0), i - last.get(ch, -1))
            last[ch] = i
        return str(min(max(gap[c], n - last[c]) for c in gap))

    def B(s):
        w = s.split()[0]
        n = len(w)
        for k in range(1, n + 1):
            for c in set(w):
                if all(c in w[i:i + k] for i in range(n - k + 1)):
                    return str(k)

    def SMALL(r):
        return "".join(r.choice(r.choice(["ab", "abc", LOWER])) for _ in range(r.randint(1, 10))) + "\n"

    def G():
        r = rng("888C")
        n = 10**5
        return [("boundary", "single char", "q\n"), ("boundary", "two distinct", "ab\n"),
                ("maxSize", "1e5 random 26 letters", "".join(r.choice(LOWER) for _ in range(n)) + "\n"),
                ("maxSize", "1e5 same letter", "z" * n + "\n"),
                ("maxSize", "1e5 one 'a' in middle among b's", "b" * 49999 + "a" + "b" * 50000 + "\n"),
                ("adversarial", "best char limited by tail gap", "abbbbbbba\n"), ("adversarial", "alphabet once", LOWER + "\n")]


@problem("79B", "n,m in [1,4e4]; k,t in [1,1e3]; distinct waste cells; queries in grid", 300)
class P79B:
    def V(s):
        L = LR(s)
        n, m, k, t = L.ints([(1, 4 * 10**4), (1, 4 * 10**4), (1, 1000), (1, 1000)])
        w = [tuple(L.ints([(1, n), (1, m)])) for _ in range(k)]
        need(len(set(w)) == k, "duplicate waste")
        for _ in range(t):
            L.ints([(1, n), (1, m)])
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, m, k, t = v[:4]
        waste = sorted((v[4 + 2 * i] - 1) * m + v[5 + 2 * i] - 1 for i in range(k))
        ws = set(waste)
        names = ["Carrots", "Kiwis", "Grapes"]
        out, p = [], 4 + 2 * k
        for j in range(t):
            c = (v[p + 2 * j] - 1) * m + v[p + 2 * j + 1] - 1
            out.append("Waste" if c in ws else names[(c - bisect_left(waste, c)) % 3])
        return "\n".join(out)

    def B(s):
        v = list(map(int, s.split()))
        n, m, k, t = v[:4]
        ws = {(v[4 + 2 * i], v[5 + 2 * i]) for i in range(k)}
        lab, c = {}, 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if (i, j) not in ws:
                    lab[(i, j)] = ["Carrots", "Kiwis", "Grapes"][c % 3]
                    c += 1
        p = 4 + 2 * k
        return "\n".join(lab.get((v[p + 2 * j], v[p + 2 * j + 1]), "Waste") for j in range(t))

    def SMALL(r):
        n, m = r.randint(1, 5), r.randint(1, 5)
        cells = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]
        k = r.randint(1, len(cells))
        t = r.randint(1, 6)
        return J((n, m, k, t), *r.sample(cells, k), *[r.choice(cells) for _ in range(t)])

    def G():
        r = rng("79B")
        N = 40000
        ws = set()
        while len(ws) < 1000:
            ws.add((r.randint(1, N), r.randint(1, N)))
        ws = sorted(ws)
        qs = [r.choice(ws) if r.random() < 0.3 else (r.randint(1, N), r.randint(1, N)) for _ in range(1000)]
        return [("boundary", "1x1 waste queried", "1 1 1 1\n1 1\n1 1\n"),
                ("maxSize", "4e4x4e4 k=t=1000 random", J((N, N, 1000, 1000), *ws, *qs)),
                ("maxSize", "last cell queries after waste near end", J((N, N, 1, 3), (N, N - 1), (N, N), (N, N - 1), (1, 1))),
                ("adversarial", "waste in first row shifts later rows", "2 3 2 4\n1 1\n1 2\n1 3\n2 1\n2 2\n2 3\n")]


@problem("929A", "n in [2,1000], k in [1,1e5]; 0<=x1<...<xn<=1e5", 300)
class P929A:
    def V(s):
        L = LR(s)
        n, k = L.ints([(2, 1000), (1, 10**5)])
        x = L.same(n, 0, 10**5)
        need(all(a < b for a, b in zip(x, x[1:])), "not increasing")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k, x = v[0], v[1], v[2:]
        cnt, cur, i = 1, 0, 0
        while x[n - 1] - x[cur] > k:
            j = cur
            while j + 1 < n and x[j + 1] - x[cur] <= k:
                j += 1
            if j == cur:
                return "-1"
            cur = j
            cnt += 1
        return str(cnt)

    def B(s):
        v = list(map(int, s.split()))
        n, k, x = v[0], v[1], v[2:]
        dist = [None] * n
        dist[0] = 0
        dq = deque([0])
        while dq:
            u = dq.popleft()
            for w in range(n):
                if dist[w] is None and 0 < abs(x[w] - x[u]) <= k:
                    dist[w] = dist[u] + 1
                    dq.append(w)
        return str(dist[n - 1] if dist[n - 1] is not None else -1)

    def SMALL(r):
        n = r.randint(2, 8)
        return J((n, r.randint(1, 6)), sorted(r.sample(range(0, 25), n)))

    def G():
        r = rng("929A")
        return [("boundary", "n=2 reachable exact k", "2 100000\n0 100000\n"), ("boundary", "n=2 unreachable", "2 1\n0 2\n"),
                ("maxSize", "n=1000 step 100 k=100", J((1000, 100), [i * 100 for i in range(1000)])),
                ("maxSize", "n=1000 random k=500", J((1000, 500), sorted(r.sample(range(0, 10**5 + 1), 1000)))),
                ("maxSize", "n=1000 k=1e5 answer 1", J((1000, 10**5), sorted(r.sample(range(0, 10**5 + 1), 1000)))),
                ("adversarial", "gap in the middle", "4 3\n0 3 7 9\n"), ("adversarial", "greedy farthest needed", "5 4\n0 1 4 5 8\n")]


@problem("994B", "n in [1,1e5], 0<=k<=min(n-1,10); distinct pi in [1,1e9]; ci in [0,1e9]", 300)
class P994B:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 10**5), (0, 10)])
        need(k <= n - 1, "k>n-1")
        p = L.same(n, 1, 10**9)
        need(len(set(p)) == n, "powers not distinct")
        L.same(n, 0, 10**9)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k = v[:2]
        p, c = v[2:2 + n], v[2 + n:2 + 2 * n]
        res = [0] * n
        best = []
        for i in sorted(range(n), key=lambda i: p[i]):
            res[i] = c[i] + sum(best)
            best.append(c[i])
            best.sort(reverse=True)
            del best[k:]
        return " ".join(map(str, res))

    def B(s):
        v = list(map(int, s.split()))
        n, k = v[:2]
        p, c = v[2:2 + n], v[2 + n:2 + 2 * n]
        return " ".join(str(c[i] + sum(sorted((c[j] for j in range(n) if p[j] < p[i]), reverse=True)[:k])) for i in range(n))

    def SMALL(r):
        n = r.randint(1, 8)
        return J((n, r.randint(0, min(n - 1, 10))), r.sample(range(1, 30), n), [r.randint(0, 9) for _ in range(n)])

    def G():
        r = rng("994B")
        n = 100000
        return [("boundary", "n=1 k=0 max coins", "1 0\n1000000000\n1000000000\n"), ("boundary", "k=0 everyone keeps own", "3 0\n3 1 2\n5 6 7\n"),
                ("maxSize", "n=1e5 k=10 random", J((n, 10), r.sample(range(1, 10**9 + 1), n), [r.randint(0, 10**9) for _ in range(n)])),
                ("maxSize", "n=1e5 k=10 all coins 1e9 (sum 1.1e10)", J((n, 10), r.sample(range(1, 10**9 + 1), n), [10**9] * n)),
                ("adversarial", "strongest has zero coins, weaker rich", "4 2\n10 1 2 3\n0 9 8 7\n"),
                ("adversarial", "zero coins everywhere", "3 2\n1 2 3\n0 0 0\n")]


@problem("958D1", "m in [1,2e5]; each line (a+b)/c with positive integers of up to two digits", 300)
class P958D1:
    def V(s):
        import re
        L = LR(s)
        m, = L.ints([(1, 2 * 10**5)])
        for _ in range(m):
            mm = re.fullmatch(r"\(([1-9][0-9]?)\+([1-9][0-9]?)\)/([1-9][0-9]?)", L.line().strip())
            need(mm is not None, "bad expression")
        L.done()

    def S(s):
        import re
        rows = s.split("\n")
        m = int(rows[0])
        keys = []
        for row in rows[1:1 + m]:
            a, b, c = map(int, re.findall(r"\d+", row))
            g = gcd(a + b, c)
            keys.append(((a + b) // g, c // g))
        cnt = Counter(keys)
        return " ".join(str(cnt[x]) for x in keys)

    def B(s):
        import re
        rows = s.split("\n")
        m = int(rows[0])
        vals = [Fraction(int(a) + int(b), int(c)) for a, b, c in (re.findall(r"\d+", r) for r in rows[1:1 + m])]
        return " ".join(str(sum(v == w for w in vals)) for v in vals)

    def SMALL(r):
        m = r.randint(1, 8)
        return J(m, *[f"({r.randint(1, 12)}+{r.randint(1, 12)})/{r.randint(1, 12)}" for _ in range(m)])

    def G():
        r = rng("958D1")
        m = 200000
        return [("boundary", "m=1 minimal", "1\n(1+1)/1\n"), ("boundary", "m=1 maximal digits", "1\n(99+99)/99\n"),
                ("maxSize", "m=2e5 random", J(m, *[f"({r.randint(1, 99)}+{r.randint(1, 99)})/{r.randint(1, 99)}" for _ in range(m)])),
                ("maxSize", "m=2e5 all identical", J(m, *["(50+50)/10"] * m)),
                ("adversarial", "equal values different forms", "4\n(1+1)/2\n(3+2)/5\n(10+10)/20\n(1+2)/2\n"),
                ("adversarial", "integer vs fraction collisions", "3\n(4+4)/4\n(1+1)/1\n(3+3)/2\n")]


@problem("995B", "n in [1,100]; 2n integers each 1..n appears exactly twice", 300)
class P995B:
    def V(s):
        L = LR(s)
        n, = L.ints([(1, 100)])
        a = L.same(2 * n, 1, n)
        need(all(v == 2 for v in Counter(a).values()) and len(set(a)) == n, "not pairs")
        L.done()

    def S(s):
        a = list(map(int, s.split()))[1:]
        c = 0
        while a:
            j = a.index(a[0], 1)
            c += j - 1
            a = a[1:j] + a[j + 1:]
        return str(c)

    def B(s):
        a = tuple(map(int, s.split()))[1:]
        def good(t):
            return all(t[i] == t[i + 1] for i in range(0, len(t), 2))
        dist = {a: 0}
        dq = deque([a])
        while dq:
            u = dq.popleft()
            if good(u):
                return str(dist[u])
            for i in range(len(u) - 1):
                l = list(u)
                l[i], l[i + 1] = l[i + 1], l[i]
                v = tuple(l)
                if v not in dist:
                    dist[v] = dist[u] + 1
                    dq.append(v)

    def SMALL(r):
        n = r.randint(1, 4)
        a = list(range(1, n + 1)) * 2
        r.shuffle(a)
        return J(n, a)

    def G():
        r = rng("995B")
        a = list(range(1, 101)) * 2
        r.shuffle(a)
        return [("boundary", "n=1", "1\n1 1\n"),
                ("maxSize", "n=100 random", J(100, a)),
                ("maxSize", "n=100 1..100 1..100 (max swaps)", J(100, list(range(1, 101)) * 2)),
                ("maxSize", "n=100 reversed mirror", J(100, list(range(1, 101)) + list(range(100, 0, -1)))),
                ("adversarial", "already paired", "3\n2 2 1 1 3 3\n"), ("adversarial", "interleaved", "2\n1 2 1 2\n")]


@problem("975C", "n,q in [1,2e5]; ai in [1,1e9]; ki in [1,1e14]", 200)
class P975C:
    def V(s):
        L = LR(s)
        n, q = L.ints([(1, 2 * 10**5)] * 2)
        L.same(n, 1, 10**9)
        L.same(q, 1, 10**14)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, q = v[:2]
        a, ks = v[2:2 + n], v[2 + n:2 + n + q]
        pre = [0]
        for x in a:
            pre.append(pre[-1] + x)
        dmg, out = 0, []
        for k in ks:
            dmg += k
            if dmg >= pre[n]:
                dmg = 0
                out.append(n)
            else:
                out.append(n - (bisect_right(pre, dmg) - 1))
        return "\n".join(map(str, out))

    def B(s):
        v = list(map(int, s.split()))
        n, q = v[:2]
        a, ks = v[2:2 + n], v[2 + n:2 + n + q]
        hp = a[:]
        out = []
        for k in ks:
            i = n - len([h for h in hp if h > 0])
            i = next((j for j in range(n) if hp[j] > 0), n)
            while k and i < n:
                d = min(k, hp[i])
                hp[i] -= d
                k -= d
                if hp[i] == 0:
                    i += 1
            if i == n:
                hp = a[:]
            out.append(sum(h > 0 for h in hp))
        return "\n".join(map(str, out))

    def SMALL(r):
        n, q = r.randint(1, 5), r.randint(1, 6)
        return J((n, q), [r.randint(1, 5) for _ in range(n)], [r.randint(1, 12) for _ in range(q)])

    def G():
        r = rng("975C")
        N = 200000
        return [("boundary", "n=q=1 exact kill", "1 1\n5\n5\n"), ("boundary", "n=q=1 overkill max k", "1 1\n1\n100000000000000\n"),
                ("maxSize", "n=q=2e5 random", J((N, N), [r.randint(1, 10**9) for _ in range(N)], [r.randint(1, 10**14) for _ in range(N)])),
                ("maxSize", "n=q=2e5 small arrows slow progress", J((N, N), [10**9] * N, [r.randint(1, 10**9) for _ in range(N)])),
                ("maxSize", "n=q=2e5 a=1 k=1", J((N, N), [1] * N, [1] * N)),
                ("adversarial", "kill exactly at boundary between warriors", "3 3\n2 2 2\n2 2 2\n"),
                ("adversarial", "partial damage carries over", "2 3\n5 5\n3 3 3\n")]


@problem("934A", "n,m in [2,50]; all values in [-1e9,1e9]", 300)
class P934A:
    def V(s):
        L = LR(s)
        n, m = L.ints([(2, 50), (2, 50)])
        L.same(n, -10**9, 10**9)
        L.same(m, -10**9, 10**9)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, m = v[:2]
        a, b = v[2:2 + n], v[2 + n:]
        best = [max(x * y for y in b) for x in a]
        best.sort()
        return str(best[-2])

    def B(s):
        v = list(map(int, s.split()))
        n, m = v[:2]
        a, b = v[2:2 + n], v[2 + n:]
        return str(min(max(a[i] * y for i in range(n) if i != h for y in b) for h in range(n)))

    def SMALL(r):
        n, m = r.randint(2, 5), r.randint(2, 5)
        return J((n, m), [r.randint(-5, 5) for _ in range(n)], [r.randint(-5, 5) for _ in range(m)])

    def G():
        r = rng("934A")
        B = 10**9
        return [("boundary", "all -1e9 (product 1e18)", J((2, 2), [-B, -B], [-B, -B])),
                ("boundary", "mixed extremes", J((2, 2), [-B, B], [-B, B])),
                ("maxSize", "n=m=50 random full range", J((50, 50), [r.randint(-B, B) for _ in range(50)], [r.randint(-B, B) for _ in range(50)])),
                ("maxSize", "n=m=50 all zeros", J((50, 50), [0] * 50, [0] * 50)),
                ("adversarial", "hiding largest is not optimal with negatives", "3 2\n-10 1 2\n-5 1\n"),
                ("adversarial", "duplicate maxima", "3 2\n7 7 1\n3 2\n")]


@problem("987C", "n in [3,3000]; si in [1,1e9]; ci in [1,1e8]", 300)
class P987C:
    def V(s):
        L = LR(s)
        n, = L.ints([(3, 3000)])
        L.same(n, 1, 10**9)
        L.same(n, 1, 10**8)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n = v[0]
        a, c = v[1:1 + n], v[1 + n:]
        INF = float("inf")
        best = INF
        for j in range(n):
            l = min((c[i] for i in range(j) if a[i] < a[j]), default=INF)
            rr = min((c[k] for k in range(j + 1, n) if a[k] > a[j]), default=INF)
            best = min(best, l + c[j] + rr)
        return "-1" if best == INF else str(best)

    def B(s):
        v = list(map(int, s.split()))
        n = v[0]
        a, c = v[1:1 + n], v[1 + n:]
        cands = [c[i] + c[j] + c[k] for i, j, k in combinations(range(n), 3) if a[i] < a[j] < a[k]]
        return str(min(cands)) if cands else "-1"

    def SMALL(r):
        n = r.randint(3, 8)
        return J(n, [r.randint(1, 6) for _ in range(n)], [r.randint(1, 20) for _ in range(n)])

    def G():
        r = rng("987C")
        n = 3000
        return [("boundary", "n=3 increasing max costs", "3\n1 2 3\n100000000 100000000 100000000\n"), ("boundary", "n=3 equal sizes", "3\n5 5 5\n1 1 1\n"),
                ("maxSize", "n=3000 random", J(n, [r.randint(1, 10**9) for _ in range(n)], [r.randint(1, 10**8) for _ in range(n)])),
                ("maxSize", "n=3000 decreasing -> -1", J(n, list(range(n, 0, -1)), [1] * n)),
                ("maxSize", "n=3000 few distinct sizes", J(n, [r.randint(1, 3) for _ in range(n)], [r.randint(1, 10**8) for _ in range(n)])),
                ("adversarial", "cheap triple must be strictly increasing", "5\n1 1 2 2 3\n1 100 100 1 1\n")]
