from collections import deque
from fractions import Fraction
from itertools import permutations
from math import gcd, isqrt
from lib import *

E18 = 10 ** 18


@problem("219B", "one line p d; 1<=p<=1e18; 0<=d<p", 400)
class P219B:
    def V(s):
        p, d = single_ints(s, [(1, E18), (0, E18)])
        need(d < p)

    def nines(x):
        c = 0
        while x % 10 == 9:
            c, x = c + 1, x // 10
        return c

    def S(s):
        p, d = map(int, s.split())
        best = p
        for k in range(1, 20):
            c = (p + 1) // 10 ** k * 10 ** k - 1
            if c >= p - d and c > 0 and P219B.nines(c) > P219B.nines(best):
                best = c
        return str(best)

    def B(s):
        p, d = map(int, s.split())
        return str(max(range(p - d, p + 1), key=lambda q: (P219B.nines(q), q)))

    def SMALL(r):
        p = r.randint(1, 3000)
        return f"{p} {r.randint(0, p - 1)}\n"

    def G():
        return [("boundary", "p=1 d=0", "1 0\n"), ("boundary", "d=0 keeps p", "1000 0\n"),
                ("maxSize", "p=1e18, d=p-1 -> 999999999999999999", f"{E18} {E18 - 1}\n"),
                ("maxSize", "p=1e18 small d", f"{E18} 1\n"),
                ("adversarial", "p already all nines max", f"{E18 - 1} {E18 - 2}\n"),
                ("adversarial", "reduction lands exactly on lower bound", "1000 1\n"),
                ("adversarial", "reduction misses by one", "10000 0\n"),
                ("adversarial", "p ends with 9s but more available", f"{10 ** 17 + 9} {10 ** 17}\n")]


@problem("226A", "one line n m; 1<=n,m<=1e9", 0)
class P226A:
    def V(s):
        single_ints(s, [(1, 10 ** 9), (1, 10 ** 9)])

    def S(s):
        n, m = map(int, s.split())
        return str((pow(3, n, m) - 1) % m)

    def G():
        return [("boundary", "n=1 m=1 answer 0", "1 1\n"), ("boundary", "m=1 large n", "1000000000 1\n"),
                ("maxSize", "both maximum", "1000000000 1000000000\n"),
                ("adversarial", "m divides 3^n so 3^n-1 wraps to m-1", "2 9\n"), ("adversarial", "3^n = 1 mod m so answer 0", "2 8\n"),
                ("adversarial", "m prime near max", "999999999 999999937\n"), ("adversarial", "power of 3 modulus", "5 243\n")]


@problem("233B", "one line n in [1,1e18]", 300)
class P233B:
    def V(s):
        single_ints(s, [(1, E18)])

    def S(s):
        n = int(s)
        best = None
        for sm in range(1, 163):
            disc = sm * sm + 4 * n
            r = isqrt(disc)
            if r * r == disc and (r - sm) % 2 == 0:
                x = (r - sm) // 2
                if x > 0 and sum(map(int, str(x))) == sm and (best is None or x < best):
                    best = x
        return str(-1 if best is None else best)

    def B(s):
        n = int(s)
        for x in range(1, isqrt(n) + 1):
            if x * x + sum(map(int, str(x))) * x == n:
                return str(x)
        return "-1"

    def SMALL(r):
        x = r.randint(1, 3000)
        return f"{x * x + sum(map(int, str(x))) * x + r.choice([0, 0, 1, -1])}\n"

    def G():
        x = 999999000
        y = 10 ** 9 - 10
        return [("boundary", "n=1", "1\n"), ("boundary", "n=2 (x=1)", "2\n"),
                ("maxSize", "n=1e18 no root", f"{E18}\n"),
                ("maxSize", "large root x=999999000 (s=54), n near 1e18", f"{x * x + 54 * x}\n"),
                ("adversarial", "root with digit sum mismatch nearby", f"{y * y + 9 * y}\n"),
                ("adversarial", "n = x^2 + s*x for wrong s only", f"{x * x + 99 * x}\n"),
                ("adversarial", "n one less than valid", f"{x * x + 54 * x - 1}\n")]


@problem("248B", "one line n in [1,1e5]", 0)
class P248B:
    def V(s):
        single_ints(s, [(1, 10 ** 5)])

    def S(s):
        n = int(s)
        if n < 3:
            return "-1"
        if n == 3:
            return "210"
        add = (210 - pow(10, n - 1, 210)) % 210
        tail = str(add).rjust(3, "0")
        return "1" + "0" * (n - 4) + tail

    def G():
        return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("boundary", "n=3", "3\n"),
                ("boundary", "n=4", "4\n"), ("maxSize", "n=1e5 (100000-digit output)", "100000\n"),
                ("maxSize", "n=99999", "99999\n"), ("adversarial", "n where remainder pattern needs 2-digit tail", "8\n")]


@problem("279A", "one line x y; |x|,|y|<=100", 0)
class P279A:
    def V(s):
        single_ints(s, [(-100, 100), (-100, 100)])

    def S(s):
        x, y = map(int, s.split())
        cx, cy, length, i = 0, 0, 1, 0
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        while True:
            dx, dy = dirs[i % 4]
            nx, ny = cx + dx * length, cy + dy * length
            if min(cx, nx) <= x <= max(cx, nx) and min(cy, ny) <= y <= max(cy, ny):
                return str(i)
            cx, cy = nx, ny
            i += 1
            if i % 2 == 0:
                length += 1

    def G():
        return [("boundary", "origin", "0 0\n"), ("boundary", "first corner", "1 0\n"), ("maxSize", "corner 100 100", "100 100\n"),
                ("maxSize", "corner -100 -100", "-100 -100\n"), ("maxSize", "corner 100 -100", "100 -100\n"),
                ("maxSize", "corner -100 100", "-100 100\n"), ("adversarial", "just after corner (100,-100)", "100 -99\n"),
                ("adversarial", "mid edge bottom", "0 -100\n")]


@problem("284A", "one line prime p, 2<=p<2000", 0)
class P284A:
    def V(s):
        p = single_ints(s, [(2, 1999)])[0]
        need(all(p % q for q in range(2, isqrt(p) + 1)), "p not prime")

    def S(s):
        n = int(s) - 1
        res, m, q = n, n, 2
        while q * q <= m:
            if m % q == 0:
                while m % q == 0:
                    m //= q
                res -= res // q
            q += 1
        if m > 1:
            res -= res // m
        return str(res)

    def G():
        return [("boundary", "p=2", "2\n"), ("boundary", "p=3", "3\n"), ("maxSize", "largest prime 1999", "1999\n"),
                ("adversarial", "p-1=1800 has several prime factors", "1801\n"), ("adversarial", "Fermat-ish 257", "257\n")]


@problem("334B", "8 lines of x y, 0<=x,y<=1e6", 0)
class P334B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 8)
        for r in rows:
            ints_line(r, [(0, 10 ** 6)] * 2)

    def S(s):
        v = list(map(int, s.split()))
        pts = list(zip(v[::2], v[1::2]))
        xs, ys = sorted(set(v[::2])), sorted(set(v[1::2]))
        if len(set(pts)) != 8 or len(xs) != 3 or len(ys) != 3:
            return "ugly"
        need_set = {(a, b) for a in xs for b in ys} - {(xs[1], ys[1])}
        return "respectable" if set(pts) == need_set else "ugly"

    def G():
        M = 10 ** 6
        good = [(0, 0), (0, 1), (0, M), (1, 0), (1, M), (M, 0), (M, 1), (M, M)]
        f = lambda p: "".join(f"{a} {b}\n" for a, b in p)
        return [("boundary", "respectable at coordinate extremes", f(good)),
                ("adversarial", "duplicate point replaces one", f(good[:7] + [(0, 0)])),
                ("adversarial", "center point instead of a corner", f(good[:7] + [(1, 1)])),
                ("maxSize", "all points identical at max", f([(M, M)] * 8)),
                ("adversarial", "shuffled respectable", f(good[::-1]))]


@problem("337B", "one line a b c d, each in [1,1000]", 0)
class P337B:
    def V(s):
        single_ints(s, [(1, 1000)] * 4)

    def S(s):
        a, b, c, d = map(int, s.split())
        if a * d > b * c:
            f = Fraction(a * d - b * c, a * d)
        else:
            f = Fraction(b * c - a * d, b * c)
        return f"{f.numerator}/{f.denominator}"

    def G():
        return [("boundary", "equal ratios gives 0/1", "1 1 1 1\n"), ("maxSize", "max equal ratios", "1000 1000 1000 1000\n"),
                ("adversarial", "extreme ratio", "1000 1 1 1000\n"), ("adversarial", "extreme reversed", "1 1000 1000 1\n"),
                ("adversarial", "large coprime", "997 991 983 977\n")]


@problem("386B", "n in [1,100]; n values t_i in [1,1000]; T in [1,1000]", 0)
class P386B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 3)
        n = ints_line(rows[0], [(1, 100)])[0]
        ints_line(rows[1], [(1, 1000)] * n)
        ints_line(rows[2], [(1, 1000)])

    def S(s):
        v = list(map(int, s.split()))
        t, T = v[1:-1], v[-1]
        return str(max(sum(a <= b <= a + T for b in t) for a in t))

    def G():
        r = rng("386B")
        return [("boundary", "single student", "1\n1\n1\n"), ("maxSize", "100 random, T=1000 covers all", "100\n" + " ".join(str(r.randint(1, 1000)) for _ in range(100)) + "\n1000\n"),
                ("adversarial", "difference exactly T counts", "2\n1 1000\n999\n"), ("adversarial", "difference T+1 excluded", "2\n1 1000\n998\n"),
                ("maxSize", "100 random tight T=1", "100\n" + " ".join(str(r.randint(1, 1000)) for _ in range(100)) + "\n1\n"),
                ("adversarial", "all equal times", "100\n" + " ".join(["500"] * 100) + "\n1\n")]


@problem("388A", "n in [1,100]; n values x_i in [0,100]", 0)
class P388A:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(1, 100)])[0]
        ints_line(rows[1], [(0, 100)] * n)

    def S(s):
        x = sorted(map(int, s.split()[1:]))
        for p in range(1, len(x) + 1):
            if all(x[i] >= i // p for i in range(len(x))):
                return str(p)

    def G():
        r = rng("388A")
        return [("boundary", "single box strength 0", "1\n0\n"), ("maxSize", "100 zeros", "100\n" + " ".join(["0"] * 100) + "\n"),
                ("maxSize", "100 boxes strength 100", "100\n" + " ".join(["100"] * 100) + "\n"),
                ("adversarial", "0..99 single pile", "100\n" + " ".join(map(str, range(99, -1, -1))) + "\n"),
                ("maxSize", "100 random small strengths", "100\n" + " ".join(str(r.randint(0, 5)) for _ in range(100)) + "\n")]


@problem("414B", "one line n k, 1<=n,k<=2000", 30)
class P414B:
    MOD = 10 ** 9 + 7

    def V(s):
        single_ints(s, [(1, 2000), (1, 2000)])

    def S(s):
        n, k = map(int, s.split())
        from math import comb
        tot = 0
        for v in range(1, n + 1):
            m, q, prod = v, 2, 1
            while q * q <= m:
                e = 0
                while m % q == 0:
                    m //= q
                    e += 1
                prod *= comb(e + k - 1, k - 1)
                q += 1
            if m > 1:
                prod *= k
            tot += prod
        return str(tot % P414B.MOD)

    def B(s):
        n, k = map(int, s.split())
        dp = [1] * (n + 1)
        dp[0] = 0
        for _ in range(k - 1):
            nd = [0] * (n + 1)
            for v in range(1, n + 1):
                for w in range(v, n + 1, v):
                    nd[w] += dp[v]
            dp = nd
        return str(sum(dp) % P414B.MOD)

    def SMALL(r):
        return f"{r.randint(1, 60)} {r.randint(1, 30)}\n"

    def G():
        return [("boundary", "n=k=1", "1 1\n"), ("maxSize", "n=k=2000", "2000 2000\n"), ("boundary", "n=2000 k=1", "2000 1\n"),
                ("boundary", "n=1 k=2000", "1 2000\n"), ("adversarial", "n=1999 k=1999 modulo wrap", "1999 1999\n")]


@problem("430B", "n,k in [1,100]; 1<=x<=k; c_i in [1,k]; no three equal contiguous", 0)
class P430B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n, k, x = ints_line(rows[0], [(1, 100), (1, 100), (1, 100)])
        need(x <= k)
        c = ints_line(rows[1], [(1, k)] * n)
        need(all(not (c[i] == c[i + 1] == c[i + 2]) for i in range(n - 2)))

    def S(s):
        v = list(map(int, s.split()))
        n, k, x, c = v[0], v[1], v[2], v[3:]
        best = 0
        for pos in range(n + 1):
            row = c[:pos] + [x] + c[pos:]
            while True:
                i, changed = 0, False
                out = []
                while i < len(row):
                    j = i
                    while j < len(row) and row[j] == row[i]:
                        j += 1
                    if j - i >= 3:
                        changed = True
                    else:
                        out.extend(row[i:j])
                    i = j
                row = out
                if not changed:
                    break
            best = max(best, n + 1 - len(row) - 1 if len(row) < n + 1 else 0)
        return str(best)

    def G():
        pal = [1, 1] + [2, 2, 3, 3] * 12
        chain = []
        for c in range(2, 51):
            chain = [c, c] + chain + [c, c]
        chain = chain[:49] + chain[-49:]
        mirror = [1, 1]
        for c in range(2, 51):
            mirror = [c] + mirror + [c]
        return [("boundary", "single ball same color", "1 1 1\n1\n"), ("boundary", "two equal balls destroyed", "2 1 1\n1 1\n"),
                ("maxSize", "n=100 nested chain fully destroyed after inserting 1", f"100 50 1\n{' '.join(map(str, mirror))}\n"),
                ("adversarial", "insertion color absent", "4 3 3\n1 1 2 2\n"),
                ("maxSize", "n=100 alternating no chain", "100 2 1\n" + " ".join(["1", "2"] * 50) + "\n")]


@problem("435B", "one line a k; 1<=a<=1e18 (no leading zeros); 0<=k<=100", 0)
class P435B:
    def V(s):
        single_ints(s, [(1, E18), (0, 100)])

    def S(s):
        a, k = s.split()
        d, k = list(a), int(k)
        for i in range(len(d)):
            if k <= 0:
                break
            j = max(range(i, min(len(d), i + k + 1)), key=lambda t: (d[t], -t))
            k -= j - i
            d[i:j + 1] = [d[j]] + d[i:j]
        return "".join(d)

    def G():
        return [("boundary", "a=1 k=0", "1 0\n"), ("boundary", "k=0 unchanged", "123456789 0\n"),
                ("maxSize", "a=1e18 k=100", f"{E18} 100\n"), ("maxSize", "18 digits ascending k=100", "123456789012345678 100\n"),
                ("adversarial", "limited swaps choose nearest max", "1990 1\n"), ("adversarial", "equal digits prefer leftmost", "9090909090909090 3\n"),
                ("adversarial", "max digit just out of reach", "1000000009 8\n")]


@problem("448B", "two lines of 1..100 lowercase letters, s != t", 0)
class P448B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        a, b = rows[0].strip(), rows[1].strip()
        for w in (a, b):
            need(1 <= len(w) <= 100 and w.isascii() and w.isalpha() and w.islower())
        need(a != b)

    def S(s):
        a, b = lines(s)[0].strip(), lines(s)[1].strip()
        it = iter(a)
        if all(ch in it for ch in b):
            return "automaton"
        if sorted(a) == sorted(b):
            return "array"
        from collections import Counter
        ca, cb = Counter(a), Counter(b)
        if all(ca[ch] >= cb[ch] for ch in cb):
            return "both"
        return "need tree"

    def G():
        return [("boundary", "single letters differ", "a\nb\n"), ("boundary", "single letter delete", "ab\na\n"),
                ("maxSize", "100 letters reversed anagram", "".join(chr(97 + i % 26) for i in range(100)) + "\n" + "".join(chr(97 + i % 26) for i in range(100))[::-1] + "\n"),
                ("maxSize", "100 a's to 99 a's", "a" * 100 + "\n" + "a" * 99 + "\n"),
                ("adversarial", "t longer than s", "abc\nabcd\n"), ("adversarial", "both needed", "abcabc\ncba\n")]


@problem("470A", "one line n in [0,9]", 0)
class P470A:
    def V(s):
        single_ints(s, [(0, 9)])

    def S(s):
        n = int(s)
        return str(3 * n * (n + 1) + 1)

    def G():
        return [("boundary", "n=0", "0\n"), ("maxSize", "n=9", "9\n")]


@problem("475B", "n,m in [2,20]; string of n '<'/'>' ; string of m '^'/'v'", 0)
class P475B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 3)
        n, m = ints_line(rows[0], [(2, 20), (2, 20)])
        h, v = rows[1].strip(), rows[2].strip()
        need(len(h) == n and set(h) <= set("<>") and len(v) == m and set(v) <= set("^v"))

    def S(s):
        rows = lines(s)
        n, m = map(int, rows[0].split())
        h, v = rows[1].strip(), rows[2].strip()

        def nb(i, j):
            res = []
            jj = j + (1 if h[i] == ">" else -1)
            if 0 <= jj < m:
                res.append((i, jj))
            ii = i + (1 if v[j] == "v" else -1)
            if 0 <= ii < n:
                res.append((ii, j))
            return res
        for si in range(n):
            for sj in range(m):
                seen, q = {(si, sj)}, [(si, sj)]
                while q:
                    for w in nb(*q.pop()):
                        if w not in seen:
                            seen.add(w)
                            q.append(w)
                if len(seen) != n * m:
                    return "NO"
        return "YES"

    def G():
        r = rng("475B")
        return [("boundary", "2x2 cycle", "2 2\n<>\nv^\n"), ("boundary", "2x2 not cycle", "2 2\n<>\n^v\n"),
                ("maxSize", "20x20 strongly connected boundary cycle", "20 20\n<" + "".join(r.choice("<>") for _ in range(18)) + ">\nv" + "".join(r.choice("^v") for _ in range(18)) + "^\n"),
                ("maxSize", "20x20 random", "20 20\n" + "".join(r.choice("<>") for _ in range(20)) + "\n" + "".join(r.choice("^v") for _ in range(20)) + "\n"),
                ("adversarial", "20x20 boundary cycle reversed direction", "20 20\n>" + "<" * 18 + "<\n^" + "v" * 18 + "v\n")]
