from itertools import permutations, combinations
from math import comb, gcd
from lib import *

E18 = 10 ** 18


@problem("1068A", "one line N M K L; 1<=K<=N<=1e18; 1<=M,L<=1e18", 400)
class P1068A:
    def V(s):
        n, m, k, l = single_ints(s, [(1, E18)] * 4)
        need(k <= n)

    def S(s):
        n, m, k, l = map(int, s.split())
        x = -(-(k + l) // m)
        return str(x if x * m <= n else -1)

    def B(s):
        n, m, k, l = map(int, s.split())
        for x in range(1, n + 1):
            if m * x <= n and m * x - k >= l:
                return str(x)
        return "-1"

    def SMALL(r):
        n = r.randint(1, 30)
        return f"{n} {r.randint(1, 30)} {r.randint(1, n)} {r.randint(1, 30)}\n"

    def G():
        return [("boundary", "all minimum values; K+L exceeds N", "1 1 1 1\n"),
                ("boundary", "single friend exactly fills collection", "2 1 1 1\n"),
                ("maxSize", "all 1e18; ceil((K+L)/M) times M overflows signed 64-bit if computed carelessly", f"{E18} {E18} {E18} {E18}\n"),
                ("maxSize", "N=1e18, M=1: K+L = 1e18 exactly", f"{E18} 1 {E18 // 2} {E18 // 2}\n"),
                ("adversarial", "K+L=2e18-1 with M=1 exceeds N", f"{E18} 1 {E18} {E18 - 1}\n"),
                ("adversarial", "M*x == N exactly with huge values", f"{E18} {E18 // 4} {E18 // 2} {E18 // 4 + 1}\n"),
                ("adversarial", "M*x == N+M-? one past capacity", f"{E18 - 1} {E18 // 4} {E18 // 2} {E18 // 4 + 1}\n"),
                ("adversarial", "huge M with tiny K+L gives x=1 when M<=N", f"{E18} {E18 - 1} 1 1\n"),
                ("adversarial", "huge M just over N", f"{E18 - 1} {E18} 1 1\n"),
                ("boundary", "L exactly equals new coins when x divides", "100 10 50 50\n")]


@problem("1091C", "one line n; 2<=n<=1e9", 60)
class P1091C:
    def V(s):
        single_ints(s, [(2, 10 ** 9)])

    def S(s):
        n = int(s)
        vals = set()
        d = 1
        while d * d <= n:
            if n % d == 0:
                for g in (d, n // d):
                    m = n // g
                    vals.add(m + g * m * (m - 1) // 2)
            d += 1
        return " ".join(map(str, sorted(vals)))

    def B(s):
        n = int(s)
        vals = set()
        for k in range(1, n + 1):
            pos, tot = 1, 1
            while True:
                pos = (pos - 1 + k) % n + 1
                if pos == 1:
                    break
                tot += pos
            vals.add(tot)
        return " ".join(map(str, sorted(vals)))

    def SMALL(r):
        return f"{r.randint(2, 120)}\n"

    def G():
        return [("boundary", "minimum n", "2\n"), ("boundary", "small prime", "3\n"),
                ("maxSize", "maximum n=1e9 (many divisors, large sums)", "1000000000\n"),
                ("maxSize", "largest prime below 1e9", "999999937\n"),
                ("adversarial", "highly composite 735134400 (1344 divisors)", "735134400\n"),
                ("adversarial", "power of two 2^29", "536870912\n"),
                ("adversarial", "square of prime 31607^2", f"{31607 * 31607}\n"),
                ("adversarial", "perfect square 31622^2 near sqrt bound", f"{31622 * 31622}\n")]


@problem("1154C", "one line a b c; 1<=a,b,c<=7e8", 300)
class P1154C:
    PAT = "frcfcrf"

    def V(s):
        single_ints(s, [(1, 7 * 10 ** 8)] * 3)

    def best(a, b, c):
        res = 0
        for st in range(7):
            f = {"f": a, "r": b, "c": c}
            d = 0
            while f[P1154C.PAT[(st + d) % 7]] > 0:
                f[P1154C.PAT[(st + d) % 7]] -= 1
                d += 1
            res = max(res, d)
        return res

    def S(s):
        a, b, c = map(int, s.split())
        w = max(0, min(a // 3, b // 2, c // 2) - 1)
        return str(7 * w + P1154C.best(a - 3 * w, b - 2 * w, c - 2 * w))

    def B(s):
        return str(P1154C.best(*map(int, s.split())))

    def SMALL(r):
        return f"{r.randint(1, 40)} {r.randint(1, 40)} {r.randint(1, 40)}\n"

    def G():
        M = 7 * 10 ** 8
        return [("boundary", "all ones", "1 1 1\n"), ("maxSize", "all maximum", f"{M} {M} {M}\n"),
                ("adversarial", "fish is the bottleneck by one", f"{M - 1} {M} {M}\n"),
                ("adversarial", "rabbit bottleneck at maximum", f"{M} 1 {M}\n"),
                ("adversarial", "chicken bottleneck at maximum", f"{M} {M} 1\n"),
                ("adversarial", "exact weekly multiples plus remainders", f"{3 * 10 ** 8 + 2} {2 * 10 ** 8 + 1} {2 * 10 ** 8 + 1}\n"),
                ("adversarial", "answer exceeds 32-bit? (max weeks)", f"{M} {M - 1} {M - 1}\n")]


@problem("1156A", "n in [2,100]; n values in {1,2,3}; adjacent values differ")
class P1156A:
    def V(s):
        rows = lines(s)
        need(len(rows) == 2)
        n = ints_line(rows[0], [(2, 100)])[0]
        a = ints_line(rows[1], [(1, 3)] * n)
        need(all(a[i] != a[i + 1] for i in range(n - 1)))

    def S(s):
        a = list(map(int, s.split()))[1:]
        tot = 0
        for i in range(len(a) - 1):
            if {a[i], a[i + 1]} == {2, 3}:
                return "Infinite"
            tot += 3 if {a[i], a[i + 1]} == {1, 2} else 4
            if i >= 1 and a[i - 1] == 3 and a[i] == 1 and a[i + 1] == 2:
                tot -= 1
        return f"Finite\n{tot}"

    def G():
        r = rng("1156A")
        alt = " ".join(["3", "1", "2", "1"] * 25)
        rnd = []
        for _ in range(3):
            v = [r.choice([1, 2])]
            while len(v) < 100:
                v.append(r.choice([x for x in (1, 2, 3) if x != v[-1] and {x, v[-1]} != {2, 3}]))
            rnd.append(" ".join(map(str, v)))
        return [("boundary", "minimum n, circle in square", "2\n3 1\n"),
                ("boundary", "minimum n, triangle-square infinite", "2\n2 3\n"),
                ("maxSize", "n=100 repeating 3 1 2 1 (every square-circle-triangle overlap)", f"100\n{alt}\n"),
                ("maxSize", "n=100 alternating 1 3 finite", "100\n" + " ".join(["1", "3"] * 50) + "\n"),
                ("adversarial", "infinite pair appears only at the very end", "100\n" + " ".join(["1", "2"] * 49 + ["3", "2"]) + "\n"),
                ("adversarial", "3 1 2 overlap at start", "3\n3 1 2\n"),
                ("adversarial", "2 1 3 must not subtract", "3\n2 1 3\n")] + [("maxSize", "random n=100 finite", f"100\n{x}\n") for x in rnd]


@problem("1214A", "three lines: n in [1,1e8], d in [30,100], e in [30,100]", 200)
class P1214A:
    def V(s):
        single_ints(s, [(1, 10 ** 8), (30, 100), (30, 100)], one_line=False)

    def S(s):
        n, d, e = map(int, s.split())
        return str(min((n - j) % d for j in range(0, n + 1, 5 * e)))

    def B(s):
        n, d, e = map(int, s.split())
        return str(min(n - x * d - y * 5 * e for x in range(n // d + 1) for y in range((n - x * d) // (5 * e) + 1)))

    def SMALL(r):
        return f"{r.randint(1, 2000)}\n{r.randint(30, 100)}\n{r.randint(30, 100)}\n"

    def G():
        return [("boundary", "minimum n below any bill", "1\n30\n30\n"),
                ("boundary", "n equals one dollar exactly", "100\n100\n100\n"),
                ("maxSize", "maximum n with max prices", "100000000\n100\n100\n"),
                ("maxSize", "maximum n with min prices", "100000000\n30\n30\n"),
                ("adversarial", "euro bill (5e) needed, dollar alone leaves remainder", "499\n100\n99\n"),
                ("adversarial", "prime-ish n with coprime prices", "99999989\n97\n89\n"),
                ("adversarial", "n just below smallest euro bill", "149\n31\n30\n")]


@problem("124B", "n,k in [1,8]; n lines of exactly k digits", 0)
class P124B:
    def V(s):
        rows = lines(s)
        n, k = ints_line(rows[0], [(1, 8), (1, 8)])
        need(len(rows) == n + 1)
        for row in rows[1:]:
            row = row.strip()
            need(len(row) == k and row.isdigit())

    def S(s):
        rows = lines(s)
        n, k = map(int, rows[0].split())
        nums = [r.strip() for r in rows[1:]]
        best = None
        for p in permutations(range(k)):
            v = [int("".join(x[i] for i in p)) for x in nums]
            d = max(v) - min(v)
            best = d if best is None else min(best, d)
        return str(best)

    def G():
        r = rng("124B")
        mk = lambda n, k: f"{n} {k}\n" + "".join("".join(r.choice("0123456789") for _ in range(k)) + "\n" for _ in range(n))
        return [("boundary", "single 1-digit number", "1 1\n7\n"), ("boundary", "single 8-digit number difference 0", "1 8\n12345678\n"),
                ("maxSize", "n=k=8 random digits (40320 permutations)", mk(8, 8)), ("maxSize", "n=k=8 random digits", mk(8, 8)),
                ("adversarial", "all zeros with leading zeros", "8 8\n" + "00000000\n" * 8),
                ("adversarial", "difference near 1e8", "2 8\n99999999\n00000000\n"),
                ("adversarial", "permutation choice matters with leading zeros", "3 8\n09876543\n90000001\n12345670\n")]


@problem("125A", "one line n in [1,10000]", 0)
class P125A:
    def V(s):
        single_ints(s, [(1, 10000)])

    def S(s):
        inch = (int(s) + 1) // 3
        return f"{inch // 12} {inch % 12}"

    def G():
        return [("boundary", "n=1 rounds down to 0 inches", "1\n"), ("boundary", "n=2 rounds up to 1 inch", "2\n"),
                ("maxSize", "maximum n", "10000\n"), ("adversarial", "35 cm rounds up to exactly 1 foot", "35\n"),
                ("adversarial", "34 cm rounds to 11 inches", "34\n"), ("adversarial", "9998 rounds up", "9998\n"),
                ("boundary", "exact foot 36", "36\n")]


@problem("1263C", "t in [1,10], then t lines n in [1,1e9]", 80)
class P1263C:
    def V(s):
        rows = lines(s)
        t = ints_line(rows[0], [(1, 10)])[0]
        need(len(rows) == t + 1)
        for r in rows[1:]:
            ints_line(r, [(1, 10 ** 9)])

    def one(n):
        v, i = {0}, 1
        while i <= n:
            q = n // i
            v.add(q)
            i = n // q + 1
        return sorted(v)

    def S(s):
        out = []
        for n in map(int, lines(s)[1:]):
            v = P1263C.one(n)
            out.append(f"{len(v)}\n" + " ".join(map(str, v)))
        return "\n".join(out)

    def B(s):
        out = []
        for n in map(int, lines(s)[1:]):
            v = sorted({n // k for k in range(1, n + 2)})
            out.append(f"{len(v)}\n" + " ".join(map(str, v)))
        return "\n".join(out)

    def SMALL(r):
        t = r.randint(1, 10)
        return f"{t}\n" + "".join(f"{r.randint(1, 3000)}\n" for _ in range(t))

    def G():
        return [("boundary", "t=1 n=1", "1\n1\n"), ("boundary", "small n 1..10", "10\n" + "".join(f"{i}\n" for i in range(1, 11))),
                ("maxSize", "t=10, all n=1e9 (largest output)", "10\n" + "1000000000\n" * 10),
                ("maxSize", "t=10 near-max perfect squares and primes", "10\n" + "".join(f"{x}\n" for x in [999950884, 999999937, 999999999, 999950883, 999950885, 1000000000, 735134400, 536870912, 999999000, 123456789])),
                ("adversarial", "squares where sqrt duplicates", "4\n16\n15\n17\n999950884\n")]


@problem("130B", "one line, 1..100 chars with ASCII 33..126", 0)
class P130B:
    def V(s):
        rows = lines(s)
        need(len(rows) == 1)
        x = rows[0].rstrip("\r")
        need(1 <= len(x) <= 100 and all(33 <= ord(c) <= 126 for c in x))

    def S(s):
        return lines(s)[0].rstrip("\r")[::-1]

    def G():
        return [("boundary", "single character", "!\n"), ("maxSize", "100 printable characters", "".join(chr(33 + i % 94) for i in range(100)) + "\n"),
                ("adversarial", "palindrome-breaking punctuation", "~a!b\"c#d$\n")]


@problem("131C", "one line n m t; 4<=n<=30, 1<=m<=30, 5<=t<=n+m", 0)
class P131C:
    def V(s):
        n, m, t = single_ints(s, [(4, 30), (1, 30), (5, 60)])
        need(t <= n + m)

    def S(s):
        n, m, t = map(int, s.split())
        return str(sum(comb(n, b) * comb(m, t - b) for b in range(4, t)))

    def G():
        return [("boundary", "minimum n,m,t", "4 1 5\n"), ("maxSize", "all maximum, t=n+m", "30 30 60\n"),
                ("maxSize", "largest count n=m=30 t=30 (exceeds 32-bit)", "30 30 30\n"),
                ("adversarial", "t=n+m-1", "30 30 59\n"), ("adversarial", "only girls bounded", "30 1 31\n"),
                ("boundary", "t=5 n=4 m=30", "4 30 5\n")]


@problem("141B", "one line a x y; 1<=a<=100, -1e6<=x<=1e6, 0<=y<=1e6", 0)
class P141B:
    def V(s):
        single_ints(s, [(1, 100), (-10 ** 6, 10 ** 6), (0, 10 ** 6)])

    def S(s):
        a, x, y = map(int, s.split())
        if y % a == 0:
            return "-1"
        r = y // a
        before = 0 if r == 0 else r + (r - 1) // 2
        if r < 2 or r % 2 == 1:
            return str(before + 1) if 2 * abs(x) < a else "-1"
        if x == 0 or abs(x) >= a:
            return "-1"
        return str(before + (1 if x < 0 else 2))

    def G():
        return [("boundary", "a=1 on bottom border", "1 0 0\n"), ("boundary", "single-square row edge x=a/2 border", "2 1 1\n"),
                ("maxSize", "max y, a=1 interior impossible for integers (border)", "1 0 1000000\n"),
                ("maxSize", "max y with a=100, row 9999 odd single", "100 0 999999\n"),
                ("maxSize", "max y two-square row left", "100 -50 999950\n"),
                ("adversarial", "x=0 in two-square row is border", "3 0 7\n"), ("adversarial", "x=-a in two-square row is border", "3 -3 7\n"),
                ("adversarial", "far outside court", "100 -1000000 1000000\n"), ("adversarial", "odd a single-square interior", "3 1 4\n")]


@problem("175A", "one line of 1..30 digits", 0)
class P175A:
    def V(s):
        rows = lines(s)
        need(len(rows) == 1)
        x = rows[0].strip()
        need(1 <= len(x) <= 30 and x.isdigit())

    def S(s):
        x = s.strip()
        ok = lambda p: p and (p == "0" or p[0] != "0") and len(p) <= 7 and int(p) <= 10 ** 6
        best = -1
        for i in range(1, len(x)):
            for j in range(i + 1, len(x)):
                a, b, c = x[:i], x[i:j], x[j:]
                if ok(a) and ok(b) and ok(c):
                    best = max(best, int(a) + int(b) + int(c))
        return str(best)

    def G():
        return [("boundary", "single digit impossible", "5\n"), ("boundary", "three zeros", "000\n"),
                ("maxSize", "three times 1000000", "100000010000001000000\n"), ("maxSize", "30 digits impossible", "9" * 30 + "\n"),
                ("adversarial", "1000001 must be rejected", "100000110\n"), ("adversarial", "leading zero part", "0012\n"),
                ("adversarial", "huge part over int range", "1999999999999990\n"), ("adversarial", "max with zeros", "1000000000\n")]


@problem("188C", "one line a b; 1<=a,b<=1000", 0)
class P188C:
    def V(s):
        single_ints(s, [(1, 1000), (1, 1000)])

    def S(s):
        a, b = map(int, s.split())
        return str(a * b // gcd(a, b))

    def G():
        return [("boundary", "both 1", "1 1\n"), ("maxSize", "coprime maxima", "999 1000\n"), ("adversarial", "equal", "1000 1000\n")]


@problem("188E", "one line 1..100 chars ASCII 33..126", 0)
class P188E:
    V = P130B.V

    def S(s):
        return "YES" if any(c in "HQ9" for c in lines(s)[0]) else "NO"

    def G():
        return [("boundary", "lowercase h q only", "hq\n"), ("maxSize", "100 plus signs", "+" * 100 + "\n"),
                ("adversarial", "9 at the end", "+" * 99 + "9\n")]


@problem("188F", "one line n in [1,1e6]", 0)
class P188F:
    def V(s):
        single_ints(s, [(1, 10 ** 6)])

    def S(s):
        return bin(int(s))[2:]

    def G():
        return [("boundary", "n=1", "1\n"), ("maxSize", "n=1e6", "1000000\n"), ("adversarial", "power of two", "524288\n")]


@problem("2038L", "one line n in [1,1000]", 25)
class P2038L:
    def V(s):
        single_ints(s, [(1, 1000)])

    def S(s):
        n = int(s)
        best = None
        for u in range(n // 2 + 1):
            sing = n - 2 * u
            for y in range(0, min(sing, n) + 1):
                x = min(n, sing - y)
                a, b = n - x, n - y
                rest = max(-(-(a + b) // 3), -(-b // 2))
                tot = u + sing + rest
                best = tot if best is None else min(best, tot)
        return str(best)

    def B(s):
        import functools
        n = int(s)
        pats = []
        for c18 in range(4):
            for c21 in range(3):
                for c25 in range(3):
                    if 0 < 18 * c18 + 21 * c21 + 25 * c25 <= 60:
                        pats.append((c18, c21, c25))

        @functools.lru_cache(None)
        def f(a, b, c):
            if a == b == c == 0:
                return 0
            return 1 + min(f(max(0, a - p), max(0, b - q), max(0, c - w)) for p, q, w in pats if (p and a) or (q and b) or (w and c))
        return str(f(n, n, n))

    def SMALL(r):
        return f"{r.randint(1, 14)}\n"

    def G():
        return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("maxSize", "n=1000", "1000\n"),
                ("maxSize", "n=999", "999\n"), ("adversarial", "n=997 remainder mod 6", "997\n"), ("adversarial", "n=6", "6\n")]
