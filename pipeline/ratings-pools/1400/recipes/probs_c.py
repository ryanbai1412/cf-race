from collections import deque
from itertools import permutations
from math import isqrt
import random as _random
from lib import *


@problem("485A", "one line a m; 1<=a,m<=1e5", 300)
class P485A:
    def V(s):
        single_ints(s, [(1, 10 ** 5), (1, 10 ** 5)])

    def S(s):
        a, m = map(int, s.split())
        x = a % m
        for _ in range(40):
            if x == 0:
                return "Yes"
            x = 2 * x % m
        return "No"

    def B(s):
        a, m = map(int, s.split())
        x, seen = a, set()
        while x % m and x % m not in seen:
            seen.add(x % m)
            x += x % m
        return "Yes" if x % m == 0 else "No"

    def SMALL(r):
        return f"{r.randint(1, 3000)} {r.randint(1, 3000)}\n"

    def G():
        return [("boundary", "a=m=1", "1 1\n"), ("maxSize", "m=2^16 power of two", "1 65536\n"),
                ("maxSize", "a=m=1e5", "100000 100000\n"), ("adversarial", "m=1e5 not power of two times a", "1 100000\n"),
                ("adversarial", "m=99999 odd", "3 99999\n"), ("adversarial", "a multiple of odd part", "3125 100000\n")]


@problem("489C", "one line m s; 1<=m<=100, 0<=s<=900", 300)
class P489C:
    def V(s):
        single_ints(s, [(1, 100), (0, 900)])

    def S(s):
        m, sm = map(int, s.split())
        if sm == 0:
            return "0 0" if m == 1 else "-1 -1"
        if sm > 9 * m:
            return "-1 -1"
        mx, r = [], sm
        for _ in range(m):
            d = min(9, r)
            mx.append(d)
            r -= d
        mn, r = [], sm
        for i in range(m):
            for d in range(1 if i == 0 else 0, 10):
                if r - d <= 9 * (m - i - 1):
                    mn.append(d)
                    r -= d
                    break
        return "".join(map(str, mn)) + " " + "".join(map(str, mx))

    def B(s):
        m, sm = map(int, s.split())
        lo = 0 if m == 1 else 10 ** (m - 1)
        c = [x for x in range(lo, 10 ** m) if sum(map(int, str(x))) == sm]
        return f"{min(c)} {max(c)}" if c else "-1 -1"

    def SMALL(r):
        m = r.randint(1, 4)
        return f"{m} {r.randint(0, 9 * m + 2)}\n"

    def G():
        return [("boundary", "m=1 s=0", "1 0\n"), ("boundary", "m=2 s=0 impossible", "2 0\n"), ("boundary", "m=1 s=9", "1 9\n"),
                ("maxSize", "m=100 s=900", "100 900\n"), ("maxSize", "m=100 s=1", "100 1\n"), ("adversarial", "m=100 s=899", "100 899\n"),
                ("adversarial", "m=1 s=10 impossible", "1 10\n"), ("adversarial", "m=100 s=0", "100 0\n"), ("maxSize", "m=100 s=450", "100 450\n")]


@problem("507B", "one line r x y x' y'; 1<=r<=1e5, |coords|<=1e5", 0)
class P507B:
    def V(s):
        single_ints(s, [(1, 10 ** 5)] + [(-10 ** 5, 10 ** 5)] * 4)

    def S(s):
        r, x, y, a, b = map(int, s.split())
        d2 = (x - a) ** 2 + (y - b) ** 2
        k = isqrt(d2) // (2 * r)
        while (2 * r * k) ** 2 < d2:
            k += 1
        return str(k)

    def G():
        M = 10 ** 5
        return [("boundary", "same point", "1 0 0 0 0\n"), ("boundary", "exactly one diameter", "5 0 0 10 0\n"),
                ("maxSize", "r=1, opposite corners (distance ~282843)", f"1 {-M} {-M} {M} {M}\n"),
                ("maxSize", "max r tiny distance", f"{M} {M} {M} {M - 1} {M}\n"),
                ("adversarial", "distance just over k diameters", "1 0 0 3 3\n"), ("adversarial", "integer-exact 3-4-5 multiple", "5 0 0 30 40\n"),
                ("adversarial", "squared distance overflows 32-bit", f"3 {-M} {-M} {M} {M - 1}\n")]


@problem("513B1", "one line n m; 1<=n<=8; 1<=m<=cnt_n=2^(n-1)", 0)
class P513B1:
    def f(p):
        return sum(min(p[i:j + 1]) for i in range(len(p)) for j in range(i, len(p)))

    def best(n):
        perms = list(permutations(range(1, n + 1)))
        vals = [P513B1.f(p) for p in perms]
        mx = max(vals)
        return [p for p, v in zip(perms, vals) if v == mx]

    def V(s):
        n, m = single_ints(s, [(1, 8), (1, 128)])
        need(m <= len(P513B1.best(n)))

    def S(s):
        n, m = map(int, s.split())
        return " ".join(map(str, P513B1.best(n)[m - 1]))

    def G():
        return [("boundary", "n=1 m=1", "1 1\n"), ("maxSize", "n=8 last permutation", "8 128\n"), ("maxSize", "n=8 first", "8 1\n"),
                ("adversarial", "n=8 middle m=64", "8 64\n"), ("adversarial", "n=8 m=65", "8 65\n"), ("adversarial", "n=7 m=37", "7 37\n")]


@problem("515C", "n in [1,15]; n digits; at least one digit > 1", 0)
class P515C:
    MAP = {"0": "", "1": "", "2": "2", "3": "3", "4": "322", "5": "5", "6": "53", "7": "7", "8": "7222", "9": "7332"}

    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(1, 15)])[0]
        a = rows[1].strip()
        need(len(a) == n and a.isdigit() and any(c > "1" for c in a))

    def S(s):
        a = lines(s)[1].strip()
        return "".join(sorted("".join(P515C.MAP[c] for c in a), reverse=True))

    def G():
        return [("boundary", "single digit 2", "1\n2\n"), ("boundary", "single 4 expands", "1\n4\n"),
                ("maxSize", "15 nines", "15\n" + "9" * 15 + "\n"), ("maxSize", "15 eights", "15\n" + "8" * 15 + "\n"),
                ("adversarial", "leading zeros and ones", "15\n000000000000012\n"), ("adversarial", "all expansion digits", "15\n987654320198765\n")]


@problem("520B", "one line n m distinct; 1<=n,m<=1e4", 0)
class P520B:
    def V(s):
        n, m = single_ints(s, [(1, 10 ** 4), (1, 10 ** 4)])
        need(n != m)

    def S(s):
        n, m = map(int, s.split())
        dist = {n: 0}
        q = deque([n])
        while q:
            x = q.popleft()
            if x == m:
                return str(dist[x])
            for y in (x - 1, 2 * x):
                if 1 <= y <= 20000 and y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)

    def G():
        return [("boundary", "n=1 m=2", "1 2\n"), ("boundary", "n=2 m=1", "2 1\n"), ("maxSize", "n=1 m=1e4", "1 10000\n"),
                ("maxSize", "n=1e4 m=1", "10000 1\n"), ("adversarial", "odd target requiring overshoot", "3 9999\n"), ("adversarial", "9999 to 10000", "9999 10000\n")]


@problem("534B", "v1 v2 in [1,100]; t in [2,100], d in [0,10]; feasible: |v1-v2| <= (t-1)d", 300)
class P534B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        v1, v2 = ints_line(rows[0], [(1, 100), (1, 100)])
        t, d = ints_line(rows[1], [(2, 100), (0, 10)])
        need(abs(v1 - v2) <= (t - 1) * d)

    def S(s):
        v1, v2, t, d = map(int, s.split())
        return str(sum(min(v1 + i * d, v2 + (t - 1 - i) * d) for i in range(t)))

    def B(s):
        v1, v2, t, d = map(int, s.split())
        best = {v1: v1}
        for i in range(1, t):
            nb = {}
            for v, tot in best.items():
                for w in range(max(0, v - d), v + d + 1):
                    if tot + w > nb.get(w, -1):
                        nb[w] = tot + w
            best = nb
        return str(best[v2])

    def SMALL(r):
        t, d = r.randint(2, 8), r.randint(0, 3)
        v1 = r.randint(1, 10)
        v2 = max(1, v1 + r.randint(-(t - 1) * d, (t - 1) * d))
        return f"{v1} {v2}\n{t} {d}\n"

    def G():
        return [("boundary", "t=2 d=0", "1 1\n2 0\n"), ("maxSize", "max t and d", "100 100\n100 10\n"),
                ("adversarial", "speed difference exactly (t-1)d", "1 100\n100 1\n".replace("100 1\n", "100 1\n")),
                ("adversarial", "d=0 constant", "50 50\n100 0\n"), ("maxSize", "v1=1 v2=1 t=100 d=10 tent", "1 1\n100 10\n")]


@problem("546C", "n in [2,10]; two stacks partitioning cards 1..n (each nonempty)", 0)
class P546C:
    def V(s):
        rows = lines(s)
        need(len(rows) == 3)
        n = ints_line(rows[0], [(2, 10)])[0]
        a = toks(rows[1])
        b = toks(rows[2])
        k1 = intok(a[0], 1, n - 1)
        need(len(a) == k1 + 1)
        k2 = intok(b[0], 1, n - 1)
        need(k1 + k2 == n and len(b) == k2 + 1)
        cards = [intok(x, 1, n) for x in a[1:] + b[1:]]
        need(sorted(cards) == list(range(1, n + 1)))

    def S(s):
        rows = lines(s)
        a = deque(map(int, rows[1].split()[1:]))
        b = deque(map(int, rows[2].split()[1:]))
        seen, fights = set(), 0
        while a and b:
            st = (tuple(a), tuple(b))
            if st in seen:
                return "-1"
            seen.add(st)
            x, y = a.popleft(), b.popleft()
            if x > y:
                a.extend([y, x])
            else:
                b.extend([x, y])
            fights += 1
        return f"{fights} {1 if a else 2}"

    def G():
        r = rng("546C")
        out = []
        for _ in range(4):
            c = list(range(1, 11))
            r.shuffle(c)
            k = r.randint(1, 9)
            out.append(("maxSize", "n=10 random split", f"10\n{k} {' '.join(map(str, c[:k]))}\n{10 - k} {' '.join(map(str, c[k:]))}\n"))
        return [("boundary", "n=2 first wins", "2\n1 2\n1 1\n"), ("boundary", "n=2 second wins", "2\n1 1\n1 2\n"),
                ("adversarial", "n=10 player 1 holds 9 cards", "10\n9 1 2 3 4 5 6 7 8 9\n1 10\n"),
                ("adversarial", "n=10 player 1 holds only 10", "10\n1 10\n9 9 8 7 6 5 4 3 2 1\n")] + out


@problem("550B", "n l r x; 1<=n<=15, 1<=l<=r<=1e9, 1<=x<=1e6; n values c_i in [1,1e6]", 0)
class P550B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n, l, r, x = ints_line(rows[0], [(1, 15), (1, 10 ** 9), (1, 10 ** 9), (1, 10 ** 6)])
        need(l <= r)
        ints_line(rows[1], [(1, 10 ** 6)] * n)

    def S(s):
        v = list(map(int, s.split()))
        n, l, r, x, c = v[0], v[1], v[2], v[3], v[4:]
        cnt = 0
        for mask in range(1, 1 << n):
            sel = [c[i] for i in range(n) if mask >> i & 1]
            if len(sel) >= 2 and l <= sum(sel) <= r and max(sel) - min(sel) >= x:
                cnt += 1
        return str(cnt)

    def G():
        r = rng("550B")
        return [("boundary", "n=1 impossible", "1 1 1 1\n1\n"), ("maxSize", "n=15 all subsets valid range", "15 1 1000000000 1\n" + " ".join(map(str, range(1, 16))) + "\n"),
                ("maxSize", "n=15 max values", "15 1 1000000000 1000000\n" + " ".join(["1000000"] * 14 + ["1"]) + "\n"),
                ("adversarial", "difference exactly x", "2 1 100 9\n1 10\n"), ("adversarial", "sum exactly r", "2 1 11 1\n1 10\n"),
                ("maxSize", "n=15 random", "15 500000 4000000 50000\n" + " ".join(str(r.randint(1, 10 ** 6)) for _ in range(15)) + "\n")]


@problem("630H", "one line n in [5,100]", 0)
class P630H:
    def V(s):
        single_ints(s, [(5, 100)])

    def S(s):
        from math import comb, perm
        n = int(s)
        return str(comb(n, 5) * perm(n, 5))

    def G():
        return [("boundary", "n=5", "5\n"), ("maxSize", "n=100 (near 64-bit)", "100\n"), ("adversarial", "n=99", "99\n")]


@problem("630L", "one line: five-digit positive integer (10000..99999)", 0)
class P630L:
    def V(s):
        single_ints(s, [(10000, 99999)])

    def S(s):
        d = s.strip()
        x = int(d[0] + d[2] + d[4] + d[3] + d[1])
        return str(pow(x, 5, 100000)).rjust(5, "0")

    def G():
        return [("boundary", "minimum 10000 (shuffled has zeros)", "10000\n"), ("maxSize", "maximum 99999", "99999\n"),
                ("adversarial", "result with leading zeros", "10010\n"), ("adversarial", "shuffle exercises every digit", "12345\n")]


@problem("649B", "n m k in [1,1000]; a b in [1, n*m*k], a != b", 300)
class P649B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n, m, k = ints_line(rows[0], [(1, 1000)] * 3)
        a, b = ints_line(rows[1], [(1, n * m * k)] * 2)
        need(a != b)

    def S(s):
        n, m, k, a, b = map(int, s.split())
        pa, fa = (a - 1) // (m * k), (a - 1) % (m * k) // k
        pb, fb = (b - 1) // (m * k), (b - 1) % (m * k) // k
        mv = lambda f: min(5 * f, 10 + f)
        if pa == pb:
            return str(min(5 * abs(fa - fb), 10 + abs(fa - fb)))
        d = abs(pa - pb)
        return str(mv(fa) + 15 * min(d, n - d) + mv(fb))

    def B(s):
        import heapq
        n, m, k, a, b = map(int, s.split())
        pa, fa = (a - 1) // (m * k), (a - 1) % (m * k) // k
        pb, fb = (b - 1) // (m * k), (b - 1) % (m * k) // k
        dist = {(pa, fa, 0): 0}
        h = [(0, pa, fa, 0)]
        while h:
            t, p, f, lift = heapq.heappop(h)
            if t > dist[(p, f, lift)]:
                continue
            if (p, f) == (pb, fb):
                return str(t)
            moves = []
            if lift:
                moves += [(1, p, g, 1) for g in (f - 1, f + 1) if 0 <= g < m] + [(0, p, f, 0)]
            else:
                moves += [(5, p, g, 0) for g in (f - 1, f + 1) if 0 <= g < m] + [(10, p, f, 1)]
                if f == 0:
                    moves += [(15, (p + 1) % n, 0, 0), (15, (p - 1) % n, 0, 0)]
            for c, q, g, l in moves:
                if t + c < dist.get((q, g, l), 1 << 60):
                    dist[(q, g, l)] = t + c
                    heapq.heappush(h, (t + c, q, g, l))

    def SMALL(r):
        n, m, k = r.randint(1, 6), r.randint(1, 8), r.randint(1, 3)
        a = r.randint(1, n * m * k)
        b = r.choice([x for x in range(1, n * m * k + 1) if x != a] or [a])
        return f"{n} {m} {k}\n{a} {b}\n" if a != b else f"2 1 1\n1 2\n"

    def G():
        return [("boundary", "two apartments on one floor", "1 1 2\n1 2\n"), ("boundary", "adjacent floors stairs better", "1 2 1\n1 2\n"),
                ("maxSize", "max house, top floors opposite entrances", "1000 1000 1000\n1000000000 500000000\n"),
                ("maxSize", "max house, first and last apartment (wraparound)", "1000 1000 1000\n1 1000000000\n"),
                ("adversarial", "lift vs stairs tie at 2 floors", "1 1000 1\n1 3\n"), ("adversarial", "lift better at 3 floors", "1 1000 1\n1 4\n"),
                ("adversarial", "even n exact half circle", "1000 1 1\n1 501\n")]


@problem("652A", "h1 < h2 in [1,1e5]; a b in [1,1e5]", 300)
class P652A:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        h1, h2 = ints_line(rows[0], [(1, 10 ** 5)] * 2)
        need(h1 < h2)
        ints_line(rows[1], [(1, 10 ** 5)] * 2)

    def S(s):
        h1, h2, a, b = map(int, s.split())
        h = h1 + 8 * a
        if h >= h2:
            return "0"
        if a <= b:
            return "-1"
        k = 0
        while h < h2:
            h += 12 * (a - b)
            k += 1
        return str(k)

    def B(s):
        h1, h2, a, b = map(int, s.split())
        h, hour, day = h1, 14, 0
        for _ in range(24 * 400):
            if 10 <= hour < 22:
                h += a
                if h >= h2:
                    return str(day)
            else:
                h -= b
            hour += 1
            if hour == 24:
                hour, day = 0, day + 1
        return "-1"

    def SMALL(r):
        h1 = r.randint(1, 200)
        return f"{h1} {r.randint(h1 + 1, 400)}\n{r.randint(1, 20)} {r.randint(1, 20)}\n"

    def G():
        return [("boundary", "reach in first afternoon exactly", "1 9\n1 1\n"), ("boundary", "a=b never progress", "1 100000\n1 1\n"),
                ("maxSize", "net gain 12 per day over 1e5", "1 100000\n2 1\n"), ("adversarial", "missed by 1 first day then a<=b", "1 10\n1 1\n"),
                ("adversarial", "slip under ground then reach", "1 100000\n100000 99999\n"), ("maxSize", "max heights instant", "99999 100000\n100000 100000\n")]


@problem("675B", "one line n a b c d; 1<=n<=1e5; 1<=a,b,c,d<=n", 300)
class P675B:
    def V(s):
        n, a, b, c, d = single_ints(s, [(1, 10 ** 5)] * 5)
        need(max(a, b, c, d) <= n)

    def S(s):
        n, a, b, c, d = map(int, s.split())
        cnt = 0
        for x in range(1, n + 1):
            y, z, w = x + b - c, x + a - d, x + a + b - c - d
            if 1 <= y <= n and 1 <= z <= n and 1 <= w <= n:
                cnt += 1
        return str(cnt * n)

    def B(s):
        n, a, b, c, d = map(int, s.split())
        cnt = 0
        for g in range(1, n + 1):
            for x in range(1, n + 1):
                for y in range(1, n + 1):
                    for z in range(1, n + 1):
                        for w in range(1, n + 1):
                            q = [x, a, y, b, g, c, z, d, w]
                            s1 = q[0] + q[1] + q[3] + q[4]
                            if s1 == q[1] + q[2] + q[4] + q[5] == q[3] + q[4] + q[6] + q[7] == q[4] + q[5] + q[7] + q[8]:
                                cnt += 1
        return str(cnt)

    def SMALL(r):
        n = r.randint(1, 4)
        return " ".join(map(str, [n] + [r.randint(1, n) for _ in range(4)])) + "\n"

    def G():
        M = 10 ** 5
        return [("boundary", "n=1", "1 1 1 1 1\n"), ("maxSize", "n=1e5 all equal (answer 1e10 overflows 32-bit)", f"{M} 1 1 1 1\n"),
                ("maxSize", "n=1e5 spread", f"{M} 1 {M} {M} 1\n"), ("adversarial", "no valid squares", f"{M} 1 {M} 1 {M}\n".replace(f"{M} 1 {M} 1 {M}", f"{M} {M} {M} 1 1")),
                ("adversarial", "partial overlap", f"{M} 3 70000 1 2\n")]
