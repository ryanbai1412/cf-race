from itertools import product
from math import gcd, isqrt
import random as _random
from lib import *


@problem("689A", "n in [1,9]; string of n digits", 0)
class P689A:
    POS = {"1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2), "7": (2, 0), "8": (2, 1), "9": (2, 2), "0": (3, 1)}

    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(1, 9)])[0]
        x = rows[1].strip()
        need(len(x) == n and x.isdigit())

    def S(s):
        x = lines(s)[1].strip()
        keys = set(P689A.POS.values())
        for dr, dc in product(range(-3, 4), repeat=2):
            if (dr, dc) != (0, 0) and all((P689A.POS[c][0] + dr, P689A.POS[c][1] + dc) in keys for c in x):
                return "NO"
        return "YES"

    def G():
        return [("boundary", "single digit 5 (shiftable)", "1\n5\n"), ("boundary", "single 0", "1\n0\n"),
                ("maxSize", "9 digits covering corners", "9\n123456789\n"), ("adversarial", "1 and 9 and 0 pins", "3\n190\n"),
                ("adversarial", "0 with 7 and 9", "3\n709\n"), ("maxSize", "9 digits 2 and 0", "9\n202020202\n")]


@problem("697B", "a.deb: a digit 0-9; d < 10^100 no trailing zeros (or 0); 0<=b<=100 no leading zeros; a=0 => b=0", 0)
class P697B:
    def V(s):
        import re
        rows = lines(s)
        need(len(rows) == 1)
        m = re.fullmatch(r"([0-9])\.([0-9]+)e([0-9]+)", rows[0].strip())
        need(m)
        a, d, b = m.groups()
        need(len(d) <= 100 and (d == "0" or (not d.endswith("0"))))
        need(b == "0" or not b.startswith("0"))
        need(int(b) <= 100)
        need(not (a == "0" and int(b) != 0))

    def S(s):
        a, rest = s.strip().split(".")
        d, b = rest.split("e")
        b = int(b)
        digits = a + ("" if d == "0" else d)
        ip = digits[:1 + b].ljust(1 + b, "0")
        frac = digits[1 + b:].rstrip("0")
        ip = ip.lstrip("0") or "0"
        return ip + ("." + frac if frac else "")

    def G():
        d100 = "1234567891" * 9 + "123456789"
        return [("boundary", "0.0e0", "0.0e0\n"), ("boundary", "integer 9.0e100", "9.0e100\n"),
                ("maxSize", "100-digit d with b=0", f"1.{d100}e0\n"), ("maxSize", "100-digit d with b=100 integer", f"1.{d100}e100\n"),
                ("adversarial", "b shorter than d by one", f"5.{d100}e98\n"), ("adversarial", "0.d with leading zero digits", "0.0001e0\n"),
                ("adversarial", "trailing zeros produced by shift", "1.5e1\n")]


@problem("698A", "n in [1,100]; n values in [0,3]", 0)
class P698A:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(1, 100)])[0]
        ints_line(rows[1], [(0, 3)] * n)

    def S(s):
        a = list(map(int, s.split()))[1:]
        INF = 10 ** 9
        dp = [0, INF, INF]
        for x in a:
            nd = [min(dp) + 1, INF, INF]
            if x & 1:
                nd[1] = min(dp[0], dp[2])
            if x & 2:
                nd[2] = min(dp[0], dp[1])
            dp = nd
        return str(min(dp))

    def G():
        r = rng("698A")
        return [("boundary", "n=1 closed", "1\n0\n"), ("boundary", "n=1 both", "1\n3\n"),
                ("maxSize", "n=100 all 3", "100\n" + " ".join(["3"] * 100) + "\n"), ("maxSize", "n=100 all 1 (alternating rest)", "100\n" + " ".join(["1"] * 100) + "\n"),
                ("maxSize", "n=100 random", "100\n" + " ".join(str(r.randint(0, 3)) for _ in range(100)) + "\n"),
                ("adversarial", "greedy trap 3 1 3 2", "4\n3 1 3 2\n")]


def _mr(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n):
    if n % 2 == 0:
        return 2
    r = _random.Random(n)
    while True:
        x = y = r.randrange(2, n)
        c, d = r.randrange(1, n), 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


def factor(n, out=None):
    out = {} if out is None else out
    if n == 1:
        return out
    if _mr(n):
        out[n] = out.get(n, 0) + 1
        return out
    d = _rho(n)
    factor(d, out)
    factor(n // d, out)
    return out


@problem("762A", "one line n k; 1<=n<=1e15; 1<=k<=1e9", 300)
class P762A:
    def V(s):
        single_ints(s, [(1, 10 ** 15), (1, 10 ** 9)])

    def S(s):
        n, k = map(int, s.split())
        divs = [1]
        for p, e in factor(n).items():
            divs = [d * p ** i for d in divs for i in range(e + 1)]
        divs.sort()
        return str(divs[k - 1] if k <= len(divs) else -1)

    def B(s):
        n, k = map(int, s.split())
        d = [x for x in range(1, n + 1) if n % x == 0]
        return str(d[k - 1] if k <= len(d) else -1)

    def SMALL(r):
        return f"{r.randint(1, 5000)} {r.randint(1, 20)}\n"

    def G():
        sq = 31622776 ** 2
        return [("boundary", "n=1 k=1", "1 1\n"), ("boundary", "n=1 k=2", "1 2\n"),
                ("maxSize", "n=1e15 last divisor", "1000000000000000 256\n"), ("maxSize", "n=1e15 k=1e9", "1000000000000000 1000000000\n"),
                ("adversarial", "large prime near 1e15, k=2", "999999999999989 2\n"), ("adversarial", "square of large prime, middle divisor", "999966000289 2\n"),
                ("adversarial", "perfect square near max, k=middle", f"{sq} 2\n"), ("adversarial", "semiprime two ~3e7 primes, k=3", "999999999999989 3\n")]


@problem("803A", "one line n k; 1<=n<=100; 0<=k<=1e6", 0)
class P803A:
    def V(s):
        single_ints(s, [(1, 100), (0, 10 ** 6)])

    def S(s):
        n, k = map(int, s.split())
        if k > n * n:
            return "-1"
        g = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j and k >= 1:
                    g[i][j] = 1
                    k -= 1
                elif j > i and k >= 2:
                    g[i][j] = g[j][i] = 1
                    k -= 2
        if k:
            return "-1"
        return "\n".join(" ".join(map(str, r)) for r in g)

    def G():
        return [("boundary", "n=1 k=0", "1 0\n"), ("boundary", "n=1 k=2 impossible", "1 2\n"), ("maxSize", "n=100 k=10000 full", "100 10000\n"),
                ("maxSize", "n=100 k=1e6", "100 1000000\n"), ("adversarial", "n=100 k=9999 odd leftover on diagonal", "100 9999\n"),
                ("adversarial", "n=100 k=10001 one too many", "100 10001\n"), ("adversarial", "n=3 k=4", "3 4\n")]


@problem("851B", "one line ax ay bx by cx cy, |.|<=1e9, points distinct", 0)
class P851B:
    def V(s):
        v = single_ints(s, [(-10 ** 9, 10 ** 9)] * 6)
        need(len({(v[0], v[1]), (v[2], v[3]), (v[4], v[5])}) == 3)

    def S(s):
        ax, ay, bx, by, cx, cy = map(int, s.split())
        same = (ax - bx) ** 2 + (ay - by) ** 2 == (bx - cx) ** 2 + (by - cy) ** 2
        col = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) == 0
        return "Yes" if same and not col else "No"

    def G():
        M = 10 ** 9
        return [("boundary", "collinear equal distances", "0 0 1 0 2 0\n"), ("boundary", "right angle", "0 1 1 1 1 0\n"),
                ("maxSize", "extreme coordinates collinear", f"{-M} {-M} 0 0 {M} {M}\n"), ("maxSize", "extreme yes", f"{-M} 0 0 {M} {M} 0\n"),
                ("adversarial", "squared distance overflows 64-bit if not careful (4e18*2)", f"{-M} {-M} {M} {M} {-M} {M}\n".replace(f"{-M} {M}\n", f"{M} {-M}\n"))]


@problem("868B", "h in [1,12]; m,s in [0,59]; t1,t2 in [1,12] distinct, not on any hand", 0)
class P868B:
    def pos(h, m, s):
        return [(h % 12) * 3600 + m * 60 + s, (m * 60 + s) * 12, s * 720]

    def V(s):
        h, m, sec, t1, t2 = single_ints(s, [(1, 12), (0, 59), (0, 59), (1, 12), (1, 12)])
        need(t1 != t2)
        hands = P868B.pos(h, m, sec)
        need((t1 % 12) * 3600 not in hands and (t2 % 12) * 3600 not in hands)

    def S(s):
        h, m, sec, t1, t2 = map(int, s.split())
        hands = P868B.pos(h, m, sec)
        a, b = (t1 % 12) * 3600, (t2 % 12) * 3600
        inside = lambda x: (x - a) % 43200 < (b - a) % 43200
        cw = sum(inside(x) for x in hands)
        return "YES" if cw in (0, 3) else "NO"

    def G():
        return [("boundary", "all hands at 12:00:00 sweep", "12 0 1 1 2\n".replace("12 0 1", "12 0 1")),
                ("boundary", "hour hand exactly between", "6 0 0 5 7\n"), ("adversarial", "hands split on both sides", "3 47 0 4 9\n"),
                ("adversarial", "minute hand on hour mark t not allowed avoided", "1 1 1 12 6\n"),
                ("maxSize", "max h m s values", "12 59 59 1 11\n"), ("maxSize", "max values, t1>t2 wrap", "12 59 59 11 1\n")]


@problem("8B", "one line of 1..100 letters from L,R,U,D", 0)
class P8B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 1)
        x = rows[0].strip()
        need(1 <= len(x) <= 100 and set(x) <= set("LRUD"))

    def S(s):
        mv = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}
        pts = [(0, 0)]
        for c in s.strip():
            x, y = pts[-1]
            dx, dy = mv[c]
            pts.append((x + dx, y + dy))
        for i in range(1, len(pts)):
            for j in range(i - 1):
                if abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1]) <= 1:
                    return "BUG"
        return "OK"

    def G():
        return [("boundary", "single move", "L\n"), ("boundary", "back and forth", "LR\n"), ("maxSize", "100 straight moves", "U" * 100 + "\n"),
                ("adversarial", "U-turn creates shortcut adjacency", "URD\n"), ("maxSize", "staircase 100", "UR" * 50 + "\n"),
                ("adversarial", "spiral touching at the end", "RRUULLDDDR\n")]


@problem("911C", "one line k1 k2 k3 in [1,1500]", 0)
class P911C:
    def V(s):
        single_ints(s, [(1, 1500)] * 3)

    def S(s):
        k = sorted(map(int, s.split()))
        ok = k[0] == 1 or k[:2] == [2, 2] or k == [3, 3, 3] or k == [2, 4, 4]
        return "YES" if ok else "NO"

    def B(s):
        from math import lcm
        k = list(map(int, s.split()))
        L = lcm(*k)
        for x in product(*[range(v) for v in k]):
            T = max(x)
            if all(any(t >= x[i] and (t - x[i]) % k[i] == 0 for i in range(3)) for t in range(T, T + L)):
                return "YES"
        return "NO"

    def SMALL(r):
        return f"{r.randint(1, 7)} {r.randint(1, 7)} {r.randint(1, 7)}\n"

    def G():
        return [("boundary", "all ones", "1 1 1\n"), ("maxSize", "all 1500", "1500 1500 1500\n"), ("adversarial", "2 4 4 special", "4 2 4\n"),
                ("adversarial", "3 3 3", "3 3 3\n"), ("adversarial", "2 3 6 trap", "2 3 6\n"), ("adversarial", "2 2 1500", "1500 2 2\n")]


_PR = [p for p in range(2, 31700) if all(p % q for q in range(2, isqrt(p) + 1))]


@problem("937B", "one line p y; 2<=p<=y<=1e9", 300)
class P937B:
    def V(s):
        p, y = single_ints(s, [(2, 10 ** 9), (2, 10 ** 9)])
        need(p <= y)

    def S(s):
        p, y = map(int, s.split())
        for v in range(y, p, -1):
            lim = min(p, isqrt(v))
            if all(v % q for q in _PR if q <= lim):
                return str(v)
        return "-1"

    def B(s):
        p, y = map(int, s.split())
        for v in range(y, p, -1):
            if all(v % d for d in range(2, p + 1)):
                return str(v)
        return "-1"

    def SMALL(r):
        p = r.randint(2, 300)
        return f"{p} {r.randint(p, 600)}\n"

    def G():
        return [("boundary", "p=y=2", "2 2\n"), ("boundary", "p=2 y=3", "2 3\n"), ("maxSize", "p=2 y=1e9", "2 1000000000\n"),
                ("maxSize", "p=y=1e9", "1000000000 1000000000\n"), ("maxSize", "p=31622 y=1e9 (sqrt bound)", "31622 1000000000\n"),
                ("adversarial", "p=1e9-1 y=1e9", "999999999 1000000000\n"), ("adversarial", "p large, y prime", "100000 999999937\n")]


@problem("940B", "four lines n k A B, each in [1,2e9]", 300)
class P940B:
    def V(s):
        single_ints(s, [(1, 2 * 10 ** 9)] * 4, one_line=False)

    def S(s):
        x, k, A, B = map(int, s.split())
        if k == 1:
            return str((x - 1) * A)
        cost = 0
        while x > 1:
            if x < k:
                cost += (x - 1) * A
                break
            r = x % k
            cost += r * A
            x -= r
            cost += min(B, (x - x // k) * A)
            x //= k
        return str(cost)

    def B(s):
        n, k, A, B = map(int, s.split())
        dp = [0] * (n + 1)
        for x in range(2, n + 1):
            dp[x] = dp[x - 1] + A
        for x in range(2, n + 1):
            dp[x] = min(dp[x], dp[x - 1] + A)
            if k > 1 and x % k == 0:
                dp[x] = min(dp[x], dp[x // k] + B)
        return str(dp[n])

    def SMALL(r):
        return f"{r.randint(1, 3000)}\n{r.randint(1, 12)}\n{r.randint(1, 50)}\n{r.randint(1, 500)}\n"

    def G():
        M = 2 * 10 ** 9
        return [("boundary", "n=1", "1\n1\n1\n1\n"), ("maxSize", "k=1 max (answer ~4e18 needs 64-bit)", f"{M}\n1\n{M}\n{M}\n"),
                ("maxSize", "k=2 max", f"{M}\n2\n{M}\n1\n"), ("adversarial", "k>n", f"{M - 1}\n{M}\n1\n1\n"),
                ("adversarial", "division expensive", f"{M}\n2\n1\n{M}\n"), ("adversarial", "k=n", f"{M}\n{M}\n{M}\n1\n")]


@problem("954B", "n in [1,100]; string of n lowercase letters", 0)
class P954B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(1, 100)])[0]
        x = rows[1].strip()
        need(len(x) == n and x.isascii() and x.isalpha() and x.islower())

    def S(s):
        x = lines(s)[1].strip()
        n = len(x)
        best = n
        for i in range(1, n // 2 + 1):
            if x[:i] == x[i:2 * i]:
                best = min(best, n - i + 1)
        return str(best)

    def G():
        return [("boundary", "n=1", "1\na\n"), ("maxSize", "n=100 all same", "100\n" + "a" * 100 + "\n"),
                ("maxSize", "n=100 half repeated", "100\n" + "abcdefghij" * 5 + "zyxwvutsrq" * 5 + "\n"), ("adversarial", "repeat only of short prefix", "7\nababxab\n"),
                ("adversarial", "no repeat", "100\n" + "".join(chr(97 + (i * 7) % 26) for i in range(100)) + "\n")]


@problem("958A1", "N in [1,10]; 2N lines of N chars from X/O", 0)
class P958A1:
    def V(s):
        rows = lines(s)
        n = ints_line(rows[0], [(1, 10)])[0]
        need(len(rows) == 2 * n + 1)
        for r in rows[1:]:
            r = r.strip()
            need(len(r) == n and set(r) <= set("XO"))

    def S(s):
        rows = [r.strip() for r in lines(s)]
        n = int(rows[0])
        a, b = rows[1:n + 1], rows[n + 1:]
        rot = lambda g: ["".join(g[n - 1 - j][i] for j in range(n)) for i in range(n)]
        for g in (a, [r[::-1] for r in a]):
            for _ in range(4):
                if g == b:
                    return "Yes"
                g = rot(g)
        return "No"

    def G():
        r = rng("958A1")
        g = ["".join(r.choice("XO") for _ in range(10)) for _ in range(10)]
        tr = ["".join(g[j][i] for j in range(10)) for i in range(10)]
        g2 = [row[:] for row in g]
        g2[0] = ("O" if g2[0][0] == "X" else "X") + g2[0][1:]
        return [("boundary", "N=1 equal", "1\nX\nX\n"), ("boundary", "N=1 different", "1\nX\nO\n"),
                ("maxSize", "N=10 transpose (flip+rotate)", "10\n" + "\n".join(g + tr) + "\n"),
                ("maxSize", "N=10 one cell differs", "10\n" + "\n".join(g + g2) + "\n"),
                ("adversarial", "N=10 vertical flip", "10\n" + "\n".join(g + [x[::-1] for x in g]) + "\n")]


@problem("962C", "one line n in [1,2e9] without leading zeros", 0)
class P962C:
    def V(s):
        single_ints(s, [(1, 2 * 10 ** 9)])

    def S(s):
        x = s.strip()
        best = -1
        for mask in range(1, 1 << len(x)):
            t = "".join(x[i] for i in range(len(x)) if mask >> i & 1)
            if t[0] != "0":
                v = int(t)
                if isqrt(v) ** 2 == v and (best == -1 or len(x) - len(t) < best):
                    best = len(x) - len(t)
        return str(best)

    def G():
        return [("boundary", "n=1", "1\n"), ("boundary", "n=2 impossible", "2\n"), ("maxSize", "n=2e9", "2000000000\n"),
                ("maxSize", "n=1999999999", "1999999999\n"), ("adversarial", "digits 8 and zeros only: every square subsequence needs leading zero", "800000000\n"),
                ("adversarial", "perfect square 44721^2", f"{44721 ** 2}\n"), ("adversarial", "zeros in middle", "1020304050\n")]
