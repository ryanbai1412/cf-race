"""Random valid-input samplers for recipes without SMALL; every draw is still filtered by the recipe validator."""
import string

R = {}


def rand(pid):
    def wrap(f):
        R[pid] = f
        return f
    return wrap


def size(r, hi, small=8):
    return r.choice([r.randint(1, min(hi, small)), r.randint(1, min(hi, 40)), r.randint(max(1, hi // 2), hi)])


@rand("107A")
def _(r):
    n = size(r, 1000)
    perm = list(range(1, n + 1))
    r.shuffle(perm)
    pipes, i = [], 0
    while i < n:
        L = r.randint(1, min(6, n - i))
        chain = perm[i:i + L]
        i += L
        for a, b in zip(chain, chain[1:]):
            pipes.append((a, b, r.choice([r.randint(1, 10), r.randint(1, 10**6)])))
    r.shuffle(pipes)
    return f"{n} {len(pipes)}\n" + "".join(f"{a} {b} {d}\n" for a, b, d in pipes)


@rand("124B")
def _(r):
    n, k = r.randint(1, 8), r.randint(1, 8)
    return f"{n} {k}\n" + "".join("".join(r.choice("0123456789"[:r.randint(1, 10)]) for _ in range(k)) + "\n" for _ in range(n))


@rand("125A")
def _(r):
    return f"{r.choice([r.randint(1, 40), r.randint(1, 10000)])}\n"


@rand("131C")
def _(r):
    n, m = r.randint(4, 30), r.randint(1, 30)
    return f"{n} {m} {r.randint(5, n + m)}\n"


@rand("152C")
def _(r):
    n, m = size(r, 100), size(r, 100)
    alpha = string.ascii_uppercase[:r.randint(1, 26)]
    return f"{n} {m}\n" + "".join("".join(r.choice(alpha) for _ in range(m)) + "\n" for _ in range(n))


@rand("175A")
def _(r):
    L = r.randint(1, 30)
    alpha = r.choice(["0123456789", "0", "019", "1000000"])
    return "".join(r.choice(alpha) for _ in range(L)) + "\n"


@rand("197B")
def _(r):
    n, m = r.randint(0, 100), r.randint(0, 100)
    lim = r.choice([3, 100])

    def poly(k):
        c = [r.randint(-lim, lim) for _ in range(k + 1)]
        while c[0] == 0:
            c[0] = r.randint(-lim, lim)
        return " ".join(map(str, c))
    return f"{n} {m}\n{poly(n)}\n{poly(m)}\n"


@rand("226A")
def _(r):
    return f"{r.choice([r.randint(1, 30), r.randint(1, 10**9)])} {r.choice([r.randint(1, 30), r.randint(1, 10**9)])}\n"


@rand("248B")
def _(r):
    return f"{r.choice([r.randint(1, 30), r.randint(1, 1000), r.randint(1, 10**5)])}\n"


@rand("272B")
def _(r):
    n = size(r, 10**5)
    hi = r.choice([16, 1000, 10**9])
    return f"{n}\n" + " ".join(str(r.randint(1, hi)) for _ in range(n)) + "\n"


@rand("277A")
def _(r):
    n, m = r.randint(2, 100), r.randint(2, 100)
    rows = []
    for _ in range(n):
        k = r.choice([0, 0, 1, r.randint(0, m)])
        rows.append(" ".join(map(str, [k] + r.sample(range(1, m + 1), k))))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"


@rand("279A")
def _(r):
    lim = r.choice([3, 10, 100])
    return f"{r.randint(-lim, lim)} {r.randint(-lim, lim)}\n"


@rand("284A")
def _(r):
    while True:
        p = r.randint(2, 1999)
        if all(p % q for q in range(2, int(p ** .5) + 1)):
            return f"{p}\n"


@rand("289B")
def _(r):
    n, m = size(r, 100), size(r, 100)
    d = r.choice([1, 2, r.randint(1, 10**4)])
    base = r.randint(1, 10**4)
    vals = [base + d * r.randint(0, 20) if r.random() < .8 else r.randint(1, 10**4) for _ in range(n * m)]
    vals = [v if 1 <= v <= 10**4 else r.randint(1, 10**4) for v in vals]
    return f"{n} {m} {d}\n" + "".join(" ".join(map(str, vals[i * m:(i + 1) * m])) + "\n" for i in range(n))


@rand("315A")
def _(r):
    n = size(r, 100)
    hi = r.choice([3, 10, 1000])
    return f"{n}\n" + "".join(f"{r.randint(1, hi)} {r.randint(1, hi)}\n" for _ in range(n))


@rand("334B")
def _(r):
    hi = r.choice([3, 10**6])
    xs = sorted(r.sample(range(hi + 1), 3)) if hi > 3 else [0, 1, 2]
    ys = sorted(r.sample(range(hi + 1), 3)) if hi > 3 else [0, 1, 2]
    pts = [(x, y) for x in xs for y in ys if (x, y) != (xs[1], ys[1])]
    if r.random() < .5:
        pts[r.randrange(8)] = (r.choice(xs), r.choice(ys))
    if r.random() < .2:
        pts[r.randrange(8)] = (r.randint(0, hi), r.randint(0, hi))
    r.shuffle(pts)
    return "".join(f"{x} {y}\n" for x, y in pts)


@rand("337B")
def _(r):
    hi = r.choice([5, 1000])
    return " ".join(str(r.randint(1, hi)) for _ in range(4)) + "\n"


@rand("386B")
def _(r):
    n = size(r, 100)
    hi = r.choice([20, 1000])
    return f"{n}\n" + " ".join(str(r.randint(1, hi)) for _ in range(n)) + f"\n{r.randint(1, r.choice([5, 1000]))}\n"


@rand("388A")
def _(r):
    n = size(r, 100)
    hi = r.choice([2, 10, 100])
    return f"{n}\n" + " ".join(str(r.randint(0, hi)) for _ in range(n)) + "\n"


@rand("38C")
def _(r):
    n, l = size(r, 100), r.randint(1, 100)
    return f"{n} {l}\n" + " ".join(str(r.randint(1, 100)) for _ in range(n)) + "\n"


@rand("430B")
def _(r):
    n, k = size(r, 100), r.randint(1, 100)
    k = min(k, r.choice([2, 3, k]))
    if k == 1:
        n = min(n, 2)
    c = []
    while len(c) < n:
        v = r.randint(1, k)
        if len(c) >= 2 and c[-1] == c[-2] == v:
            continue
        c.append(v)
    return f"{n} {k} {r.randint(1, k)}\n" + " ".join(map(str, c)) + "\n"


@rand("435B")
def _(r):
    L = r.randint(1, 18)
    a = str(r.randint(1, 9)) + "".join(r.choice("0123456789") for _ in range(L - 1))
    if r.random() < .1:
        a = "1" + "0" * 18
    return f"{a} {r.choice([0, 1, r.randint(0, 20), r.randint(0, 100)])}\n"


@rand("437C")
def _(r):
    n = size(r, 1000)
    pairs = [(x, y) for x in range(1, n + 1) for y in range(x + 1, n + 1)] if n <= 64 else None
    if pairs is not None:
        m = r.randint(0, min(2000, len(pairs)))
        es = r.sample(pairs, m)
    else:
        m = r.randint(0, 2000)
        seen = set()
        while len(seen) < m:
            x, y = r.sample(range(1, n + 1), 2)
            seen.add((min(x, y), max(x, y)))
        es = list(seen)
    es = [(y, x) if r.random() < .5 else (x, y) for x, y in sorted(es)]
    r.shuffle(es)
    hi = r.choice([5, 10**5])
    return f"{n} {len(es)}\n" + " ".join(str(r.randint(0, hi)) for _ in range(n)) + "\n" + "".join(f"{x} {y}\n" for x, y in es)


@rand("445B")
def _(r):
    n = r.randint(1, 50)
    pairs = [(x, y) for x in range(1, n + 1) for y in range(x + 1, n + 1)]
    es = r.sample(pairs, r.randint(0, min(len(pairs), r.choice([n, 2 * n, len(pairs)]))))
    r.shuffle(es)
    return f"{n} {len(es)}\n" + "".join(f"{x} {y}\n" for x, y in es)


@rand("448B")
def _(r):
    alpha = string.ascii_lowercase[:r.randint(1, 26)]
    s = "".join(r.choice(alpha) for _ in range(r.randint(1, 100)))
    mode = r.randrange(4)
    if mode == 0:
        t = "".join(r.sample(s, len(s)))
    elif mode == 1:
        t = "".join(c for c in s if r.random() < .5) or s[0]
    elif mode == 2:
        t = "".join(c for c in r.sample(s, len(s)) if r.random() < .6) or s[-1]
    else:
        t = "".join(r.choice(alpha) for _ in range(r.randint(1, 100)))
    return f"{s}\n{t}\n"


@rand("475B")
def _(r):
    n, m = r.randint(2, 20), r.randint(2, 20)
    return f"{n} {m}\n" + "".join(r.choice("<>") for _ in range(n)) + "\n" + "".join(r.choice("^v") for _ in range(m)) + "\n"


@rand("505B")
def _(r):
    n, m = r.randint(2, 100), r.randint(1, 100)
    n = min(n, r.choice([4, 10, n]))
    es = set()
    cmax = min(m, r.choice([3, m]))
    target = r.randint(1, min(100, n * (n - 1) // 2 * cmax))
    while len(es) < target:
        a, b = sorted(r.sample(range(1, n + 1), 2))
        es.add((a, b, r.randint(1, cmax)))
    es = list(es)
    r.shuffle(es)
    q = r.randint(1, 100)
    qs = [r.sample(range(1, n + 1), 2) for _ in range(q)]
    return f"{n} {len(es)}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in es) + f"{q}\n" + "".join(f"{u} {v}\n" for u, v in qs)


@rand("507B")
def _(r):
    lim = r.choice([10, 10**5])
    v = [r.randint(1, lim)] + [r.randint(-lim, lim) for _ in range(4)]
    return " ".join(map(str, v)) + "\n"


@rand("515C")
def _(r):
    n = r.randint(1, 15)
    return f"{n}\n" + "".join(r.choice("0123456789") for _ in range(n)) + "\n"


@rand("520B")
def _(r):
    hi = r.choice([20, 10**4])
    n, m = r.sample(range(1, hi + 1), 2)
    return f"{n} {m}\n"


@rand("550B")
def _(r):
    n = r.randint(1, 15)
    hi = r.choice([20, 10**6])
    c = [r.randint(1, hi) for _ in range(n)]
    l = r.randint(1, max(1, sum(c)))
    rr = r.randint(l, min(10**9, l + sum(c)))
    return f"{n} {l} {rr} {r.randint(1, hi)}\n" + " ".join(map(str, c)) + "\n"


@rand("630H")
def _(r):
    return f"{r.randint(5, 100)}\n"


@rand("630L")
def _(r):
    return f"{r.randint(10000, 99999)}\n"


@rand("689A")
def _(r):
    n = r.randint(1, 9)
    return f"{n}\n" + "".join(r.sample("0123456789", n)) + "\n"


@rand("697B")
def _(r):
    a = r.randint(0, 9)
    b = 0 if a == 0 else r.randint(0, 100)
    if r.random() < .2:
        d = "0"
    else:
        L = r.randint(1, 100)
        d = "".join(r.choice("0123456789") for _ in range(L - 1)) + r.choice("123456789")
    return f"{a}.{d}e{b}\n"


@rand("698A")
def _(r):
    n = size(r, 100)
    alpha = r.choice([[0, 1, 2, 3], [0, 3], [1, 2], [3]])
    return f"{n}\n" + " ".join(str(r.choice(alpha)) for _ in range(n)) + "\n"


@rand("803A")
def _(r):
    n = r.randint(1, 100)
    n = min(n, r.choice([5, n]))
    return f"{n} {r.choice([0, r.randint(0, n * n + 3), r.randint(0, 10**6)])}\n"


@rand("851B")
def _(r):
    lim = r.choice([3, 1000, 10**9])
    if r.random() < .5:
        ax, ay, bx, by = (r.randint(-lim, lim) for _ in range(4))
        dx, dy = bx - ax, by - ay
        k = r.random() < .5
        cx, cy = (bx - dy, by + dx) if k else (r.randint(-lim, lim), r.randint(-lim, lim))
        v = [ax, ay, bx, by, cx, cy]
    else:
        v = [r.randint(-lim, lim) for _ in range(6)]
    return " ".join(map(str, v)) + "\n"


@rand("868B")
def _(r):
    return f"{r.randint(1, 12)} {r.randint(0, 59)} {r.randint(0, 59)} {r.randint(1, 12)} {r.randint(1, 12)}\n"


@rand("8B")
def _(r):
    L = r.randint(1, 100)
    alpha = r.choice(["LRUD", "LU", "RRRU", "UD"])
    return "".join(r.choice(alpha) for _ in range(L)) + "\n"


@rand("954B")
def _(r):
    n = size(r, 100)
    if r.random() < .5:
        p = "".join(r.choice("ab") for _ in range(r.randint(1, max(1, n // 2))))
        s = (p + p + "".join(r.choice("abc") for _ in range(n)))[:n]
    else:
        s = "".join(r.choice(string.ascii_lowercase[:r.randint(1, 26)]) for _ in range(n))
    return f"{n}\n{s}\n"


@rand("958A1")
def _(r):
    n = r.randint(1, 10)
    g = [[r.choice("XO") for _ in range(n)] for _ in range(n)]
    h = [row[:] for row in g]
    for _ in range(r.randint(0, 3)):
        op = r.randrange(3)
        if op == 0:
            h = [list(x) for x in zip(*h[::-1])]
        elif op == 1:
            h = [row[::-1] for row in h]
        else:
            h = h[::-1]
    if r.random() < .3:
        i, j = r.randrange(n), r.randrange(n)
        h[i][j] = "X" if h[i][j] == "O" else "O"
    return f"{n}\n" + "".join("".join(x) + "\n" for x in g) + "".join("".join(x) + "\n" for x in h)


@rand("962C")
def _(r):
    if r.random() < .5:
        k = r.randint(1, 44721)
        n = k * k * r.choice([1, 10, 100, 1000, 10**4]) + r.choice([0, 0, r.randint(0, 9)])
        n = min(max(n, 1), 2 * 10**9)
    else:
        n = r.choice([r.randint(1, 1000), r.randint(1, 2 * 10**9)])
    return f"{n}\n"


@rand("489C")
def _(r):
    m = r.choice([r.randint(1, 4), r.randint(1, 100)])
    return f"{m} {r.choice([r.randint(0, 9 * m + 2), r.randint(0, 900)])}\n"


@rand("19A")
def _(r):
    n = r.choice([2, 4, r.randrange(2, 51, 2)])
    names = set()
    while len(names) < n:
        names.add("".join(r.choice(string.ascii_letters[:r.choice([2, 52])]) for _ in range(r.randint(1, r.choice([3, 30])))))
    names = sorted(names)
    r.shuffle(names)
    hi = r.choice([3, 10, 100])
    ms = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = (names[i], names[j]) if r.random() < .5 else (names[j], names[i])
            ms.append(f"{a}-{b} {r.randint(0, hi)}:{r.randint(0, hi)}")
    r.shuffle(ms)
    return f"{n}\n" + "\n".join(names) + "\n" + "\n".join(ms) + "\n"
