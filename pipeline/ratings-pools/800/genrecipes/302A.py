from rlib import *

CONSTRAINTS = "n, m in 1..2*10^5; a_i in {-1, 1}; m queries 1 <= l <= r <= n."
UNIQUENESS = "Unique 0/1 per query."
STATEMENT = "Reviewed full statement: 1 iff segment length even and min(count(1), count(-1)) >= len/2."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 200000), num(p[1], 1, 200000)
    a = ls[1].split(" ")
    need(len(a) == n and all(x in ("1", "-1") for x in a), "array")
    need(len(ls) == m + 2, "m queries")
    for l in ls[2:]:
        q = l.split(" ")
        need(len(q) == 2, "l r")
        need(num(q[0], 1, n) <= num(q[1], 1, n), "l <= r")


def solve(inp):
    ls = lines(inp)
    a = ls[1].split()
    pos = a.count("1"); neg = len(a) - pos
    out = []
    for l in ls[2:]:
        x, y = map(int, l.split()); k = y - x + 1
        out.append("1" if k % 2 == 0 and min(pos, neg) >= k // 2 else "0")
    return "\n".join(out)


def gen(rng):
    n, m = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 2000)]), rng.choice([1, rng.randint(1, 100), rng.randint(1, 2000)])
    p = rng.random()
    a = ["1" if rng.random() < p else "-1" for _ in range(n)]
    qs = []
    for _ in range(m):
        x = rng.randint(1, n); qs.append(f"{x} {rng.randint(x, n)}")
    return f"{n} {m}\n" + " ".join(a) + "\n" + "\n".join(qs) + "\n"


def extra():
    return [("boundary", "single element", "1 1\n1\n1 1\n"), ("adversarial", "positions irrelevant, only global counts", "4 2\n1 1 -1 -1\n1 2\n2 3\n"),
            ("maxSize", "n=m=2*10^5", "200000 200000\n" + " ".join(["1", "-1"] * 100000) + "\n" + "".join(f"{i % 1000 + 1} {200000 - i % 997}\n" for i in range(200000)))]
