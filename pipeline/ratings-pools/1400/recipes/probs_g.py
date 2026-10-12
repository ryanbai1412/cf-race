import heapq
from bisect import bisect_left, bisect_right
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from lib import *


def J(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


@problem("514B", "n in [1,1000]; x0,y0,xi,yi in [-1e4,1e4]; no trooper at gun; duplicates allowed", 300)
class P514B:
    def V(s):
        L = LR(s)
        n, x0, y0 = L.ints([(1, 1000), (-10**4, 10**4), (-10**4, 10**4)])
        for _ in range(n):
            x, y = L.ints([(-10**4, 10**4)] * 2)
            need((x, y) != (x0, y0), "trooper at gun")
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, x0, y0 = v[:3]
        d = set()
        for i in range(n):
            dx, dy = v[3 + 2 * i] - x0, v[4 + 2 * i] - y0
            g = gcd(abs(dx), abs(dy))
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            d.add((dx, dy))
        return str(len(d))

    def B(s):
        v = list(map(int, s.split()))
        n, x0, y0 = v[:3]
        pts = [(v[3 + 2 * i] - x0, v[4 + 2 * i] - y0) for i in range(n)]
        reps = []
        for p in pts:
            if not any(p[0] * q[1] - p[1] * q[0] == 0 for q in reps):
                reps.append(p)
        return str(len(reps))

    def SMALL(r):
        n = r.randint(1, 8)
        x0, y0 = r.randint(-3, 3), r.randint(-3, 3)
        pts = []
        while len(pts) < n:
            p = (r.randint(-4, 4), r.randint(-4, 4))
            if p != (x0, y0):
                pts.append(p)
        return J((n, x0, y0), *pts)

    def G():
        r = rng("514B")
        big = []
        while len(big) < 1000:
            p = (r.randint(-10**4, 10**4), r.randint(-10**4, 10**4))
            if p != (0, 0):
                big.append(p)
        coll = [(k, -k) for k in range(1, 501)] + [(-k, k) for k in range(1, 501)]
        return [("boundary", "n=1", "1 0 0\n1 1\n"), ("boundary", "gun at corner, trooper at opposite corner", "1 -10000 -10000\n10000 10000\n"),
                ("maxSize", "1000 random troopers full range", J((1000, 0, 0), *big)),
                ("maxSize", "1000 troopers on one line through gun both sides", J((1000, 0, 0), *coll)),
                ("adversarial", "opposite directions share a line; vertical/horizontal", "4 0 0\n0 5\n0 -3\n7 0\n-2 0\n"),
                ("adversarial", "all troopers stacked at one point", J((1000, 5, 5), *[(6, 7)] * 1000)),
                ("adversarial", "nearly collinear large coordinates", "3 -10000 -10000\n10000 9999\n9999 9998\n10000 10000\n")]


@problem("518B", "|s| in [1,2e5], |s|<=|t|<=2e5, letters only", 0)
class P518B:
    def V(s):
        L = LR(s)
        a = L.word(LOWER + UPPER, 1, 2 * 10**5)
        b = L.word(LOWER + UPPER, len(a), 2 * 10**5)
        L.done()

    def S(s):
        a, b = s.split()
        ca, cb = Counter(a), Counter(b)
        yay = 0
        for ch in list(ca):
            m = min(ca[ch], cb[ch])
            yay += m
            ca[ch] -= m
            cb[ch] -= m
        wh = 0
        for ch in list(ca):
            m = min(ca[ch], cb[ch.swapcase()])
            wh += m
            ca[ch] -= m
            cb[ch.swapcase()] -= m
        return f"{yay} {wh}"

    def SMALL(r):
        al = r.choice(["aA", "abAB", LOWER + UPPER])
        n = r.randint(1, 8)
        return "".join(r.choice(al) for _ in range(n)) + "\n" + "".join(r.choice(al) for _ in range(r.randint(n, 10))) + "\n"

    def G():
        r = rng("518B")
        al = LOWER + UPPER
        return [("boundary", "length 1 exact", "a\na\n"), ("boundary", "length 1 wrong case", "a\nA\n"),
                ("boundary", "length 1 no match", "a\nb\n"),
                ("maxSize", "|s|=|t|=2e5 random letters", "".join(r.choice(al) for _ in range(200000)) + "\n" + "".join(r.choice(al) for _ in range(200000)) + "\n"),
                ("maxSize", "|s|=1, |t|=2e5", "Z\n" + "z" * 199999 + "Z\n"),
                ("adversarial", "case swaps only, YAY must be taken first", "aAbB\nAaBb\n"),
                ("adversarial", "taking WHOOPS first would lose YAY", "aA\nAX\n")]


@problem("525B", "|s| in [2,2e5] lowercase; m in [1,1e5]; 1<=a_i, 2a_i<=|s|", 300)
class P525B:
    def V(s):
        L = LR(s)
        w = L.word(LOWER, 2, 2 * 10**5)
        m, = L.ints([(1, 10**5)])
        L.same(m, 1, len(w) // 2)
        L.done()

    def S(s):
        t = s.split()
        w, m = list(t[0]), int(t[1])
        n = len(w)
        cnt = [0] * (n // 2 + 2)
        for x in t[2:2 + m]:
            cnt[int(x)] += 1
        par = 0
        for i in range(1, n // 2 + 1):
            par ^= cnt[i] & 1
            if par:
                w[i - 1], w[n - i] = w[n - i], w[i - 1]
        return "".join(w)

    def B(s):
        t = s.split()
        w = t[0]
        for x in t[2:]:
            a = int(x)
            w = w[:a - 1] + w[a - 1:len(w) - a + 1][::-1] + w[len(w) - a + 1:]
        return w

    def SMALL(r):
        n = r.randint(2, 9)
        m = r.randint(1, 6)
        return "".join(r.choice("abc") for _ in range(n)) + f"\n{m}\n" + " ".join(str(r.randint(1, n // 2)) for _ in range(m)) + "\n"

    def G():
        r = rng("525B")
        n = 200000
        w = "".join(r.choice(LOWER) for _ in range(n))
        return [("boundary", "|s|=2 one reversal", "ab\n1\n1\n"), ("boundary", "odd length, middle stays", "abc\n1\n1\n"),
                ("maxSize", "|s|=2e5, m=1e5 random a", w + "\n100000\n" + " ".join(str(r.randint(1, n // 2)) for _ in range(100000)) + "\n"),
                ("maxSize", "|s|=2e5, m=1e5 all a=1", w + "\n100000\n" + " ".join(["1"] * 100000) + "\n"),
                ("adversarial", "a = |s|/2 repeatedly (innermost pair)", w[:10] + "\n3\n5 5 5\n"),
                ("adversarial", "distinct a values cancel pairwise", "abcdefghij\n4\n1 2 2 1\n")]


@problem("548B", "n,m in [1,500], q in [1,5000]; grid of 0/1; queries in range", 200)
class P548B:
    def V(s):
        L = LR(s)
        n, m, q = L.ints([(1, 500), (1, 500), (1, 5000)])
        for _ in range(n):
            L.same(m, 0, 1)
        for _ in range(q):
            L.ints([(1, n), (1, m)])
        L.done()

    def S(s):
        v = s.split()
        n, m, q = int(v[0]), int(v[1]), int(v[2])
        g = [[v[3 + i * m + j] == "1" for j in range(m)] for i in range(n)]

        def best(row):
            b = c = 0
            for x in row:
                c = c + 1 if x else 0
                if c > b:
                    b = c
            return b
        sc = [best(rw) for rw in g]
        out, p = [], 3 + n * m
        for _ in range(q):
            i, j = int(v[p]) - 1, int(v[p + 1]) - 1
            p += 2
            g[i][j] = not g[i][j]
            sc[i] = best(g[i])
            out.append(str(max(sc)))
        return "\n".join(out)

    def B(s):
        v = list(map(int, s.split()))
        n, m, q = v[:3]
        g = [v[3 + i * m:3 + (i + 1) * m] for i in range(n)]
        out, p = [], 3 + n * m
        for _ in range(q):
            g[v[p] - 1][v[p + 1] - 1] ^= 1
            p += 2
            out.append(str(max(max((len(x) for x in "".join(map(str, rw)).split("0")), default=0) for rw in g)))
        return "\n".join(out)

    def SMALL(r):
        n, m, q = r.randint(1, 4), r.randint(1, 5), r.randint(1, 6)
        return J((n, m, q), *[[r.randint(0, 1) for _ in range(m)] for _ in range(n)], *[(r.randint(1, n), r.randint(1, m)) for _ in range(q)])

    def G():
        r = rng("548B")
        return [("boundary", "1x1 toggle twice", "1 1 2\n0\n1 1\n1 1\n"),
                ("maxSize", "500x500, q=5000 random", J((500, 500, 5000), *[[r.randint(0, 1) for _ in range(500)] for _ in range(500)], *[(r.randint(1, 500), r.randint(1, 500)) for _ in range(5000)])),
                ("maxSize", "500x500 all ones, q=5000 toggles on one row", J((500, 500, 5000), *[[1] * 500 for _ in range(500)], *[(1, r.randint(1, 500)) for _ in range(5000)])),
                ("adversarial", "score drops to 0 after toggling only one", "1 3 1\n0 1 0\n1 2\n"),
                ("adversarial", "max row changes between rows", "2 3 3\n1 1 0\n1 0 0\n1 2\n2 2\n2 3\n")]


@problem("581C", "n in [1,1e5], k in [0,1e7], a_i in [0,100]", 300)
class P581C:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 10**5), (0, 10**7)])
        L.same(n, 0, 100)
        L.done()

    def S(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        tot = sum(x // 10 for x in a)
        need_ = sorted(10 - x % 10 for x in a if x < 100 and x % 10)
        for d in need_:
            if k >= d:
                k -= d
                tot += 1
            else:
                break
        cap = 10 * n - tot
        return str(tot + min(k // 10, cap))

    def B(s):
        v = list(map(int, s.split()))
        n, k, a = v[0], v[1], v[2:]
        best = 0

        def go(i, k, acc):
            nonlocal best
            if i == n:
                best = max(best, acc)
                return
            for add in range(0, min(k, 100 - a[i]) + 1):
                go(i + 1, k - add, acc + (a[i] + add) // 10)
        go(0, k, 0)
        return str(best)

    def SMALL(r):
        n = r.randint(1, 3)
        return J((n, r.randint(0, 25)), [r.choice([r.randint(0, 100), r.randint(85, 100)]) for _ in range(n)])

    def G():
        r = rng("581C")
        return [("boundary", "k=0", "1 0\n55\n"), ("boundary", "all 100, k max", "3 10000000\n100 100 100\n"),
                ("boundary", "all zeros single", "1 10000000\n0\n"),
                ("maxSize", "n=1e5 random, k=1e7", J((100000, 10**7), [r.randint(0, 100) for _ in range(100000)])),
                ("maxSize", "n=1e5 random, k moderate", J((100000, 123456), [r.randint(0, 100) for _ in range(100000)])),
                ("adversarial", "greedy must pick smallest remainders first", "3 6\n19 15 11\n"),
                ("adversarial", "leftover k exceeds total capacity", "2 1000\n99 1\n")]


@problem("602B", "n in [2,1e5]; a_i in [1,1e5]; |a_{i+1}-a_i|<=1", 300)
class P602B:
    def V(s):
        L = LR(s)
        n, = L.ints([(2, 10**5)])
        a = L.same(n, 1, 10**5)
        need(all(abs(x - y) <= 1 for x, y in zip(a, a[1:])), "jump >1")
        L.done()

    def S(s):
        a = list(map(int, s.split()))[1:]
        cnt = Counter()
        best = l = 0
        for r_, x in enumerate(a):
            cnt[x] += 1
            while max(cnt) - min(cnt) > 1:
                cnt[a[l]] -= 1
                if not cnt[a[l]]:
                    del cnt[a[l]]
                l += 1
            best = max(best, r_ - l + 1)
        return str(best)

    def B(s):
        a = list(map(int, s.split()))[1:]
        n = len(a)
        return str(max(j - i + 1 for i in range(n) for j in range(i, n) if max(a[i:j + 1]) - min(a[i:j + 1]) <= 1))

    def SMALL(r):
        n = r.randint(2, 10)
        a = [r.randint(1, 3)]
        for _ in range(n - 1):
            a.append(min(10**5, max(1, a[-1] + r.randint(-1, 1))))
        return J(n, a)

    def G():
        r = rng("602B")
        a = [50000]
        for _ in range(99999):
            a.append(min(10**5, max(1, a[-1] + r.randint(-1, 1))))
        zig = [1 + (i % 2) for i in range(100000)]
        stair = [1 + i // 2 for i in range(100000)]
        return [("boundary", "n=2 equal", "2\n1 1\n"), ("boundary", "n=2 differ by one at max", "2\n100000 99999\n"),
                ("maxSize", "n=1e5 random walk", J(100000, a)), ("maxSize", "n=1e5 alternating 1 2 (answer n)", J(100000, zig)),
                ("adversarial", "staircase 1 1 2 2 3 3 ...", J(100000, stair)),
                ("adversarial", "x x+1 x+2 window must shrink correctly", "7\n1 2 3 2 1 2 3\n")]
