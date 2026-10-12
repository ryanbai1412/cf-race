from collections import Counter, deque
from itertools import permutations, product
from math import gcd
from lib import *

MOD = 10 ** 9 + 7


def nums(s):
    return list(map(int, s.split()))


@problem("1009B", "one line: string over {0,1,2}, length 1..1e5", 300)
class P1009B:
    def V(s):
        L = LR(s)
        L.word("012", 1, 10 ** 5)
        L.done()

    def S(s):
        x = s.split()[0]
        t = x.replace("1", "")
        i = t.find("2")
        i = len(t) if i < 0 else i
        return t[:i] + "1" * x.count("1") + t[i:]

    def B(s):
        x = s.split()[0]
        seen, q = {x}, deque([x])
        while q:
            u = q.popleft()
            for i in range(len(u) - 1):
                if {u[i], u[i + 1]} in ({"0", "1"}, {"1", "2"}):
                    v = u[:i] + u[i + 1] + u[i] + u[i + 2:]
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
        return min(seen)

    def SMALL(r):
        return "".join(r.choice("012") for _ in range(r.randint(1, 8))) + "\n"

    def G():
        r = rng("1009B")
        N = 10 ** 5
        return [("boundary", "single char", "2\n"), ("boundary", "only ones", "111\n"), ("maxSize", "1e5 random", "".join(r.choice("012") for _ in range(N)) + "\n"),
                ("maxSize", "1e5 twos then zeros then ones", "2" * 40000 + "0" * 30000 + "1" * 30000 + "\n"),
                ("adversarial", "no twos", "".join(r.choice("01") for _ in range(N)) + "\n"), ("adversarial", "ones after last two", "02020211\n"),
                ("adversarial", "zero after two cannot cross", "2010\n")]


@problem("107A", "n in [1,1000], 0<=p<=n, pipes a b d (a!=b, d in [1,1e6]), indeg/outdeg <= 1", 0)
class P107A:
    def V(s):
        L = LR(s)
        n, p = L.ints([(1, 1000), (0, 1000)])
        need(p <= n)
        o, i = set(), set()
        for _ in range(p):
            a, b, d = L.ints([(1, n), (1, n), (1, 10 ** 6)])
            need(a != b and a not in o and b not in i)
            o.add(a)
            i.add(b)
        L.done()

    def S(s):
        v = nums(s)
        n, p = v[0], v[1]
        nxt, ins = {}, set()
        for k in range(p):
            a, b, d = v[2 + 3 * k:5 + 3 * k]
            nxt[a] = (b, d)
            ins.add(b)
        res = []
        for t in sorted(nxt):
            if t in ins:
                continue
            u, m = t, 10 ** 9
            while u in nxt:
                u, d = nxt[u]
                m = min(m, d)
            res.append(f"{t} {u} {m}")
        return "\n".join([str(len(res))] + res)

    def G():
        r = rng("107A")
        perm = list(range(1, 1001))
        r.shuffle(perm)
        chain = "\n".join(f"{perm[i]} {perm[i + 1]} {r.randint(1, 10 ** 6)}" for i in range(999))
        cyc = "\n".join(f"{i} {i % 1000 + 1} 1000000" for i in range(1, 1001))
        pairs = "\n".join(f"{2 * i - 1} {2 * i} {i}" for i in range(1, 501))
        return [("boundary", "n=1 p=0", "1 0\n"), ("boundary", "single pipe", "2 1\n2 1 7\n"),
                ("maxSize", "single chain of 1000 random order", f"1000 999\n{chain}\n"), ("maxSize", "full cycle -> 0", f"1000 1000\n{cyc}\n"),
                ("maxSize", "500 disjoint pipes", f"1000 500\n{pairs}\n"), ("adversarial", "cycle plus chain", "6 5\n1 2 5\n2 3 4\n3 1 3\n4 5 9\n5 6 1\n")]


@problem("108B", "n in [2,1e5]; a_i in [1,1e9]", 300)
class P108B:
    def V(s):
        L = LR(s)
        n = L.ints([(2, 10 ** 5)])[0]
        L.same(n, 1, 10 ** 9)
        L.done()

    def S(s):
        u = sorted(set(nums(s)[1:]))
        return "YES" if any(2 * u[i] > u[i + 1] for i in range(len(u) - 1)) else "NO"

    def B(s):
        a = nums(s)[1:]
        for x in a:
            for y in a:
                if x < y and ((1 << x) - 1) ** 2 >= (1 << y):
                    return "YES"
        return "NO"

    def SMALL(r):
        n = r.randint(2, 6)
        return f"{n}\n" + " ".join(str(r.randint(1, 40)) for _ in range(n)) + "\n"

    def G():
        r = rng("108B")
        N = 10 ** 5
        dbl = [1 << i for i in range(30)] + [10 ** 9]
        return [("boundary", "two equal", "2\n5 5\n"), ("boundary", "1 and 2", "2\n1 2\n"),
                ("maxSize", "1e5 doubling chain repeated (NO)", f"{N}\n" + " ".join(str(dbl[i % 31]) for i in range(N)) + "\n"),
                ("maxSize", "1e5 random large", f"{N}\n" + " ".join(str(r.randint(1, 10 ** 9)) for _ in range(N)) + "\n"),
                ("adversarial", "only exact doubles with 1e9 tail", "3\n500000000 1000000000 1000000000\n"),
                ("adversarial", "x and 2x-1", "2\n1000000000 999999999\n")]


@problem("152C", "n,m in [1,100]; n names of exactly m uppercase letters", 0)
class P152C:
    def V(s):
        L = LR(s)
        n, m = L.ints([(1, 100), (1, 100)])
        for _ in range(n):
            need(len(L.word(UPPER)) == m)
        L.done()

    def S(s):
        t = s.split()
        names = t[2:]
        r = 1
        for col in zip(*names):
            r = r * len(set(col)) % MOD
        return str(r)

    def G():
        r = rng("152C")
        return [("boundary", "1x1", "1 1\nA\n"), ("boundary", "one name m=100", "1 100\n" + "Z" * 100 + "\n"),
                ("maxSize", "100x100 random (mod wraps)", "100 100\n" + "\n".join("".join(r.choice(UPPER) for _ in range(100)) for _ in range(100)) + "\n"),
                ("maxSize", "100x100 all 26 letters per column", "100 100\n" + "\n".join("".join(UPPER[(i + j) % 26] for j in range(100)) for i in range(100)) + "\n"),
                ("adversarial", "identical names", "3 4\nABCD\nABCD\nABCD\n")]


def _sim159(s, check):
    L = LR(s) if check else None
    if check:
        k = L.ints([(1, 2000)])[0]
        base = L.word(LOWER, 1, 100)
        q = L.ints([(0, 20000)])[0]
        ops = []
        for _ in range(q):
            row = L.line().split()
            need(len(row) == 2 and len(row[1]) == 1 and row[1] in LOWER)
            ops.append((intok(row[0], 1, 200000), row[1]))
        L.done()
    else:
        t = s.split()
        k, base, q = int(t[0]), t[1], int(t[2])
        ops = [(int(t[3 + 2 * i]), t[4 + 2 * i]) for i in range(q)]
    full = base * k
    pos = {}
    for i, c in enumerate(full):
        pos.setdefault(c, []).append(i)
    fen = {c: [0] * (len(p) + 1) for c, p in pos.items()}
    for c, p in pos.items():
        f = fen[c]
        for i in range(1, len(p) + 1):
            f[i] += 1
            j = i + (i & -i)
            if j <= len(p):
                f[j] += f[i]
    alive = [True] * len(full)
    left = len(full)
    for pth, c in ops:
        f = fen.get(c)
        if check:
            need(f is not None)
        n = len(f) - 1
        idx, rem, step = 0, pth, 1 << n.bit_length()
        while step:
            if idx + step <= n and f[idx + step] < rem:
                idx += step
                rem -= f[idx]
            step >>= 1
        if check:
            need(idx < n, "deleting nonexistent occurrence")
        alive[pos[c][idx]] = False
        i = idx + 1
        while i <= n:
            f[i] -= 1
            i += i & -i
        left -= 1
    if check:
        need(left > 0, "all letters deleted")
    return "".join(ch for ch, a in zip(full, alive) if a)


@problem("159C", "k in [1,2000]; s lowercase len 1..100; n in [0,2e4]; ops 'p c' valid; not all deleted", 300)
class P159C:
    def V(s):
        _sim159(s, True)

    def S(s):
        return _sim159(s, False)

    def B(s):
        t = s.split()
        k, base, q = int(t[0]), t[1], int(t[2])
        x = list(base * k)
        for i in range(q):
            p, c = int(t[3 + 2 * i]), t[4 + 2 * i]
            idx = [j for j, ch in enumerate(x) if ch == c][p - 1]
            del x[idx]
        return "".join(x)

    def SMALL(r):
        base = "".join(r.choice("abc") for _ in range(r.randint(1, 4)))
        k = r.randint(1, 4)
        x = list(base * k)
        ops = []
        for _ in range(r.randint(0, len(x) - 1)):
            c = r.choice(x)
            p = r.randint(1, x.count(c))
            idx = [j for j, ch in enumerate(x) if ch == c][p - 1]
            del x[idx]
            ops.append(f"{p} {c}")
        return f"{k}\n{base}\n{len(ops)}\n" + "".join(o + "\n" for o in ops)

    def G():
        r = rng("159C")
        base = "".join(r.choice(LOWER) for _ in range(100))
        x = Counter(base * 2000)
        ops = []
        for _ in range(20000):
            c = r.choice(sorted(c for c in x if x[c] > 0))
            ops.append(f"{r.randint(1, x[c])} {c}")
            x[c] -= 1
        allA = []
        for i in range(20000):
            allA.append(f"{200000 - i} a")
        return [("boundary", "n=0", "1\na\n0\n"), ("boundary", "delete all but one", "1\nab\n1\n1 a\n"),
                ("maxSize", "k=2000 |s|=100 20000 random ops", f"2000\n{base}\n20000\n" + "\n".join(ops) + "\n"),
                ("maxSize", "200000 a's, delete last occurrence each time", "2000\n" + "a" * 100 + "\n20000\n" + "\n".join(allA) + "\n"),
                ("adversarial", "delete first occurrence repeatedly", "3\nab\n3\n1 a\n1 a\n1 a\n")]


@problem("180C", "one line: letters only, length 1..1e5", 300)
class P180C:
    def V(s):
        L = LR(s)
        L.word(LOWER + UPPER, 1, 10 ** 5)
        L.done()

    def S(s):
        x = s.split()[0]
        up = sum(c.isupper() for c in x)
        best, low, upp = up, 0, up
        for c in x:
            if c.isupper():
                upp -= 1
            else:
                low += 1
            best = min(best, low + upp)
        return str(best)

    def B(s):
        x = s.split()[0]
        return str(min(sum(c.islower() for c in x[:i]) + sum(c.isupper() for c in x[i:]) for i in range(len(x) + 1)))

    def SMALL(r):
        return "".join(r.choice("aAbB") for _ in range(r.randint(1, 10))) + "\n"

    def G():
        r = rng("180C")
        N = 10 ** 5
        return [("boundary", "single lower", "a\n"), ("boundary", "single upper", "Z\n"),
                ("maxSize", "1e5 random", "".join(r.choice("aZ") for _ in range(N)) + "\n"),
                ("maxSize", "1e5 lower then upper (answer 5e4)", "a" * 50000 + "A" * 50000 + "\n"),
                ("adversarial", "alternating", "aA" * 10 + "\n")]


@problem("197B", "n,m in [0,100]; coefficients in [-100,100]; leading nonzero", 0)
class P197B:
    def V(s):
        L = LR(s)
        n, m = L.ints([(0, 100), (0, 100)])
        a = L.same(n + 1, -100, 100)
        b = L.same(m + 1, -100, 100)
        need(a[0] != 0 and b[0] != 0)
        L.done()

    def S(s):
        v = nums(s)
        n, m = v[0], v[1]
        a0, b0 = v[2], v[3 + n]
        if n > m:
            return "Infinity" if a0 * b0 > 0 else "-Infinity"
        if n < m:
            return "0/1"
        g = gcd(a0, b0)
        p, q = a0 // g, b0 // g
        if q < 0:
            p, q = -p, -q
        return f"{p}/{q}"

    def G():
        z100 = " ".join(["0"] * 100)
        return [("boundary", "degree 0 both", "0 0\n-7\n-14\n"), ("boundary", "reduces to integer with negative denominator", "0 0\n100\n-50\n"),
                ("maxSize", "deg 100 both", f"100 100\n-100 {z100}\n100 {z100}\n"), ("maxSize", "deg 100 vs 99 negative", f"100 99\n-1 {z100}\n1 {z100[2:]}\n"),
                ("adversarial", "both negative leading -> +Infinity", "2 1\n-1 0 0\n-3 0\n"), ("adversarial", "zero limit", "0 100\n5\n1 " + z100 + "\n")]


def _ninja(n, k, w):
    dist = [[-1] * (n + 1) for _ in range(2)]
    dist[0][1] = 0
    q = deque([(0, 1)])
    while q:
        wall, h = q.popleft()
        d = dist[wall][h]
        for nw, nh in ((wall, h + 1), (wall, h - 1), (1 - wall, h + k)):
            if nh > n:
                return "YES"
            if nh >= 1 and nh > d + 1 and w[nw][nh - 1] == "-" and dist[nw][nh] < 0:
                dist[nw][nh] = d + 1
                q.append((nw, nh))
    return "NO"


@problem("198B", "n,k in [1,1e5]; two wall strings of length n over {X,-}; left[0]=='-'", 300)
class P198B:
    def V(s):
        L = LR(s)
        n, k = L.ints([(1, 10 ** 5), (1, 10 ** 5)])
        a = L.word("X-", n, n)
        L.word("X-", n, n)
        need(a[0] == "-")
        L.done()

    def S(s):
        t = s.split()
        return _ninja(int(t[0]), int(t[1]), t[2:4])

    def B(s):
        t = s.split()
        n, k, w = int(t[0]), int(t[1]), t[2:4]
        cur = {(0, 1)}
        for time in range(1, 2 * n + 3):
            nxt = set()
            for wall, h in cur:
                for nw, nh in ((wall, h + 1), (wall, h - 1), (1 - wall, h + k)):
                    if nh > n:
                        return "YES"
                    if nh >= 1 and nh > time and w[nw][nh - 1] == "-":
                        nxt.add((nw, nh))
            cur = nxt
            if not cur:
                break
        return "NO"

    def SMALL(r):
        n = r.randint(1, 9)
        k = r.randint(1, 5)
        a = "-" + "".join(r.choice("--X") for _ in range(n - 1))
        b = "".join(r.choice("--X") for _ in range(n))
        return f"{n} {k}\n{a}\n{b}\n"

    def G():
        r = rng("198B")
        N = 10 ** 5
        zig = ["-" if (i // 2) % 2 == 0 else "X" for i in range(N)]
        zag = ["X" if c == "-" else "-" for c in zig]
        return [("boundary", "n=1", "1 1\n-\nX\n"), ("boundary", "n=2 blocked", "2 5\n-X\n--\n"),
                ("maxSize", "1e5 all safe k=1e5", f"{N} {N}\n" + "-" * N + "\n" + "-" * N + "\n"),
                ("maxSize", "1e5 k=1 alternating blocks force zigzag", f"{N} 1\n{''.join(zig)}\n{''.join(zag)}\n"),
                ("maxSize", "1e5 random", f"{N} 3\n-" + "".join(r.choice("-----X") for _ in range(N - 1)) + "\n" + "".join(r.choice("-----X") for _ in range(N)) + "\n"),
                ("adversarial", "must go down to beat water? no - water rises", "5 3\n--XXX\n-X-X-\n")]


def _cup(s, check):
    rows = [r.strip() for r in lines(s)]
    if check:
        need(rows[0].isdigit())
    n = int(rows[0])
    if check:
        need(1 <= n <= 50 and n % 2 == 0)
        need(len(rows) == 1 + n + n * (n - 1) // 2)
    names = rows[1:n + 1]
    if check:
        need(all(1 <= len(x) <= 30 and x.isascii() and x.isalpha() for x in names))
        need(len(set(names)) == n)
    st = {x: [0, 0, 0] for x in names}
    seen = set()
    import re
    for row in rows[n + 1:]:
        m = re.fullmatch(r"([A-Za-z]+)-([A-Za-z]+) (\d+):(\d+)", row)
        if check:
            need(m)
        a, b, x, y = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        if check:
            need(a in st and b in st and a != b and 0 <= x <= 100 and 0 <= y <= 100)
            key = frozenset((a, b))
            need(key not in seen)
            seen.add(key)
            need(m.group(3) == str(x) and m.group(4) == str(y))
        for t, f, g in ((a, x, y), (b, y, x)):
            st[t][0] += 3 if f > g else (1 if f == g else 0)
            st[t][1] += f - g
            st[t][2] += f
    order = sorted(names, key=lambda t: (-st[t][0], -st[t][1], -st[t][2]))
    if check:
        keys = [tuple(st[t]) for t in order]
        need(len(set(keys)) == n, "ambiguous standings")
    return "\n".join(sorted(order[:n // 2]))


@problem("19A", "n even in [2,50]; distinct (case-sensitive) letter names <=30; all n(n-1)/2 matches once 'a-b x:y' 0..100; unambiguous", 0)
class P19A:
    def V(s):
        _cup(s, True)

    def S(s):
        return _cup(s, False)

    def G():
        r = rng("19A")

        def make(names, score):
            ms = []
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    x, y = score(i, j)
                    ms.append(f"{names[i]}-{names[j]} {x}:{y}")
            return f"{len(names)}\n" + "\n".join(names) + "\n" + "\n".join(ms) + "\n"
        names50 = ["".join(r.choice(LOWER + UPPER) for _ in range(30)) for _ in range(50)]
        names50 = [x[:28] + LOWER[i // 26] + (UPPER + LOWER)[i % 52] for i, x in enumerate(names50)]
        assert len(set(names50)) == 50
        return [("boundary", "n=2", make(["b", "A"], lambda i, j: (0, 1))),
                ("maxSize", "n=50 strict ordering by index", make(names50, lambda i, j: (100, 0))),
                ("maxSize", "n=50 all draws, ranking by goals scored (case-variant names)", make(["Team" + (UPPER + LOWER)[k] for k in range(50)], lambda i, j: (100 - i, 100 - i))),
                ("adversarial", "names differing only by case; uppercase sorts first", make(["b", "B", "a", "A"], lambda i, j: {(0, 1): (3, 0), (0, 2): (2, 0), (0, 3): (5, 1), (1, 2): (1, 0), (1, 3): (4, 0), (2, 3): (0, 0)}[(i, j)])),
                ("adversarial", "tie on points and difference decided by scored", "4\nA\nB\nC\nD\nA-B 3:3\nA-C 0:0\nA-D 1:1\nB-C 2:2\nB-D 0:0\nC-D 1:1\n")]


@problem("205B", "n in [1,1e5]; a_i in [1,1e9]", 300)
class P205B:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 10 ** 5)])[0]
        L.same(n, 1, 10 ** 9)
        L.done()

    def S(s):
        a = nums(s)[1:]
        return str(sum(max(0, a[i] - a[i + 1]) for i in range(len(a) - 1)))

    def B(s):
        a = nums(s)[1:]
        moves = 0
        while True:
            i = next((i for i in range(len(a) - 1) if a[i] > a[i + 1]), None)
            if i is None:
                return str(moves)
            j = i + 1
            while j + 1 < len(a) and a[j + 1] <= a[j] and a[j + 1] < a[i] + 0 and False:
                j += 1
            a = a[:i + 1] + [x + 1 for x in a[i + 1:]]
            moves += 1

    def SMALL(r):
        n = r.randint(1, 6)
        return f"{n}\n" + " ".join(str(r.randint(1, 6)) for _ in range(n)) + "\n"

    def G():
        r = rng("205B")
        N = 10 ** 5
        return [("boundary", "n=1", "1\n1000000000\n"), ("maxSize", "1e5 alternating 1e9/1 (answer ~5e13 needs 64-bit)", f"{N}\n" + " ".join("1000000000" if i % 2 == 0 else "1" for i in range(N)) + "\n"),
                ("maxSize", "1e5 strictly decreasing", f"{N}\n" + " ".join(str(10 ** 9 - i) for i in range(N)) + "\n"),
                ("maxSize", "1e5 random", f"{N}\n" + " ".join(str(r.randint(1, 10 ** 9)) for _ in range(N)) + "\n"),
                ("adversarial", "already sorted with equals", "5\n1 1 2 2 2\n")]


@problem("245E", "one line of '+'/'-', length 1..300", 300)
class P245E:
    def V(s):
        L = LR(s)
        L.word("+-", 1, 300)
        L.done()

    def S(s):
        cur = mx = mn = 0
        for c in s.split()[0]:
            cur += 1 if c == "+" else -1
            mx, mn = max(mx, cur), min(mn, cur)
        return str(mx - mn)

    def B(s):
        x = s.split()[0]
        for start in range(0, len(x) + 1):
            pass
        best = None
        for start in range(len(x) + 1):
            inside, outside, ok = start, 0, True
            people = start
            for c in x:
                if c == "+":
                    if outside:
                        outside -= 1
                    else:
                        people += 1
                    inside += 1
                else:
                    if inside == 0:
                        ok = False
                        break
                    inside -= 1
                    outside += 1
            if ok:
                best = people if best is None else min(best, people)
        return str(best)

    def SMALL(r):
        return "".join(r.choice("+-") for _ in range(r.randint(1, 12))) + "\n"

    def G():
        return [("boundary", "single +", "+\n"), ("boundary", "single -", "-\n"), ("maxSize", "300 pluses", "+" * 300 + "\n"),
                ("maxSize", "150 - then 150 +", "-" * 150 + "+" * 150 + "\n"), ("adversarial", "oscillating", "+-" * 150 + "\n")]


@problem("24A", "n in [3,100]; n directed roads a b c forming an undirected ring; c in [1,100]", 0)
class P24A:
    def V(s):
        L = LR(s)
        n = L.ints([(3, 100)])[0]
        adj = {i: [] for i in range(1, n + 1)}
        for _ in range(n):
            a, b, c = L.ints([(1, n), (1, n), (1, 100)])
            need(a != b)
            adj[a].append(b)
            adj[b].append(a)
        L.done()
        need(all(len(v) == 2 and v[0] != v[1] for v in adj.values()))
        seen, u = {1}, 1
        prev = None
        while True:
            nx = adj[u][0] if adj[u][0] != prev else adj[u][1]
            if nx == 1:
                break
            need(nx not in seen)
            seen.add(nx)
            prev, u = u, nx
        need(len(seen) == n)

    def S(s):
        v = nums(s)
        n = v[0]
        roads = [tuple(v[1 + 3 * i:4 + 3 * i]) for i in range(n)]
        adj = {i: [] for i in range(1, n + 1)}
        for a, b, c in roads:
            adj[a].append(b)
            adj[b].append(a)
        order, prev, u = [1], None, 1
        while len(order) < n:
            nx = adj[u][0] if adj[u][0] != prev else adj[u][1]
            order.append(nx)
            prev, u = u, nx
        succ = {order[i]: order[(i + 1) % n] for i in range(n)}
        cw = sum(c for a, b, c in roads if succ[a] != b)
        return str(min(cw, sum(c for _, _, c in roads) - cw))

    def G():
        r = rng("24A")
        p = list(range(1, 101))
        r.shuffle(p)
        rr = []
        for i in range(100):
            a, b = p[i], p[(i + 1) % 100]
            if r.random() < 0.5:
                a, b = b, a
            rr.append(f"{a} {b} {r.randint(1, 100)}")
        cw = "\n".join(f"{i} {i % 100 + 1} 100" for i in range(1, 101))
        return [("boundary", "n=3 already strongly connected", "3\n1 2 5\n2 3 5\n3 1 5\n"), ("maxSize", "n=100 random shuffled ring", "100\n" + "\n".join(rr) + "\n"),
                ("maxSize", "n=100 already a directed cycle", f"100\n{cw}\n"), ("adversarial", "one expensive edge against direction", "4\n1 2 1\n2 3 1\n3 4 1\n1 4 100\n")]


@problem("261A", "m in [1,1e5]; q_i in [1,1e5]; n in [1,1e5]; a_i in [1,1e4]", 300)
class P261A:
    def V(s):
        L = LR(s)
        m = L.ints([(1, 10 ** 5)])[0]
        L.same(m, 1, 10 ** 5)
        n = L.ints([(1, 10 ** 5)])[0]
        L.same(n, 1, 10 ** 4)
        L.done()

    def S(s):
        v = nums(s)
        m = v[0]
        q = min(v[1:1 + m])
        a = sorted(v[2 + m:], reverse=True)
        return str(sum(x for i, x in enumerate(a) if i % (q + 2) < q))

    def B(s):
        v = nums(s)
        m = v[0]
        qs = set(v[1:1 + m])
        a = sorted(v[2 + m:], reverse=True)
        n = len(a)
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            dp[i + 1] = min(dp[i + 1], dp[i] + a[i])
            for q in qs:
                if i + q <= n:
                    paid = dp[i] + sum(a[i:i + q])
                    for f in range(3):
                        if i + q + f <= n:
                            dp[i + q + f] = min(dp[i + q + f], paid)
        return str(dp[n])

    def SMALL(r):
        m = r.randint(1, 3)
        n = r.randint(1, 9)
        return f"{m}\n" + " ".join(str(r.randint(1, 5)) for _ in range(m)) + f"\n{n}\n" + " ".join(str(r.randint(1, 20)) for _ in range(n)) + "\n"

    def G():
        r = rng("261A")
        N = 10 ** 5
        return [("boundary", "n=1 m=1", "1\n1\n1\n10000\n"), ("maxSize", "q=1 n=1e5", f"{N}\n" + " ".join(str(r.randint(1, N)) for _ in range(N - 1)) + " 1\n" + f"{N}\n" + " ".join(str(r.randint(1, 10 ** 4)) for _ in range(N)) + "\n"),
                ("maxSize", "q=1e5 > n useless", f"1\n{N}\n{N - 1}\n" + " ".join(["10000"] * (N - 1)) + "\n"),
                ("adversarial", "discount larger than item count", "1\n5\n3\n1 2 3\n")]


@problem("270B", "n in [1,1e5]; a is a permutation of 1..n", 300)
class P270B:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 10 ** 5)])[0]
        a = L.same(n, 1, n)
        need(len(set(a)) == n)
        L.done()

    def S(s):
        a = nums(s)[1:]
        last = max((i + 1 for i in range(len(a) - 1) if a[i] > a[i + 1]), default=0)
        return str(last)

    def B(s):
        a = nums(s)[1:]
        n = len(a)
        for k in range(n + 1):
            if all(a[i] < a[i + 1] for i in range(k, n - 1)):
                return str(k)

    def SMALL(r):
        n = r.randint(1, 8)
        p = list(range(1, n + 1))
        r.shuffle(p)
        return f"{n}\n" + " ".join(map(str, p)) + "\n"

    def G():
        N = 10 ** 5
        return [("boundary", "n=1", "1\n1\n"), ("maxSize", "1e5 reversed", f"{N}\n" + " ".join(str(N - i) for i in range(N)) + "\n"),
                ("maxSize", "1e5 identity", f"{N}\n" + " ".join(str(i + 1) for i in range(N)) + "\n"),
                ("adversarial", "only last pair inverted", f"{N}\n" + " ".join(map(str, list(range(1, N - 1)) + [N, N - 1])) + "\n")]


@problem("272B", "n in [1,1e5]; a_i in [1,1e9]", 0)
class P272B:
    def V(s):
        L = LR(s)
        n = L.ints([(1, 10 ** 5)])[0]
        L.same(n, 1, 10 ** 9)
        L.done()

    def S(s):
        c = Counter(bin(x).count("1") for x in nums(s)[1:])
        return str(sum(v * (v - 1) // 2 for v in c.values()))

    def G():
        r = rng("272B")
        N = 10 ** 5
        return [("boundary", "n=1", "1\n1\n"), ("maxSize", "1e5 powers of two (answer ~5e9 needs 64-bit)", f"{N}\n" + " ".join(str(1 << (i % 30)) for i in range(N)) + "\n"),
                ("maxSize", "1e5 random", f"{N}\n" + " ".join(str(r.randint(1, 10 ** 9)) for _ in range(N)) + "\n"),
                ("adversarial", "max popcount values", "3\n536870911 1073741823 1000000000\n".replace("1073741823", "999999999"))]
