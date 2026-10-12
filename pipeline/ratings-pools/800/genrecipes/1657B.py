from rlib import *

CONSTRAINTS = "t in 1..10^4; each case n in 1..2*10^5, B, x, y in 1..10^9; sum n <= 2*10^5."
UNIQUENESS = "Unique integer per case."
STATEMENT = "Reviewed full statement: greedily add x when a+x <= B else subtract y; maximize sum."


def validate(inp):
    ls = lines(inp)
    t = num(ls[0], 1, 10000)
    need(len(ls) == t + 1, "t cases")
    total = 0
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 4, "n B x y")
        total += num(p[0], 1, 200000)
        for q in p[1:]:
            num(q, 1, 10 ** 9)
    need(total <= 200000, "sum n")


def solve(inp):
    v = list(map(int, inp.split()))[1:]
    out = []
    for i in range(0, len(v), 4):
        n, b, x, y = v[i:i + 4]
        a = s = 0
        for _ in range(n):
            a = a + x if a + x <= b else a - y
            s += a
        out.append(str(s))
    return "\n".join(out)


def gen(rng):
    t = rng.choice([1, rng.randint(1, 50), rng.randint(1, 1000)])
    budget, rows = rng.choice([t, 2000, 20000]), []
    for _ in range(t):
        n = rng.randint(1, max(1, budget // t))
        hi = rng.choice([5, 10 ** 9])
        rows.append(f"{n} {rng.randint(1, hi)} {rng.randint(1, hi)} {rng.randint(1, hi)}")
    return f"{t}\n" + "\n".join(rows) + "\n"


def extra():
    return [("boundary", "x exceeds B immediately", "1\n1 1 2 1\n"), ("adversarial", "64-bit sum", "1\n200000 1000000000 1000000000 1\n"),
            ("maxSize", "t=10^4 sum n = 2*10^5", "10000\n" + "20 1000000000 7 1000000000\n" * 10000)]
