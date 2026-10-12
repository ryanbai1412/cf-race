from rlib import *

CONSTRAINTS = "n in 1..1000; x in 0..10^9; n lines '+ d' or '- d' with d in 1..10^9."
UNIQUENESS = "Unique pair."
STATEMENT = "Reviewed full statement: carriers add; children take d if enough else distressed."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n x")
    n = num(p[0], 1, 1000); num(p[1], 0, 10 ** 9)
    need(len(ls) == n + 1, "n records")
    for l in ls[1:]:
        q = l.split(" ")
        need(len(q) == 2 and q[0] in ("+", "-"), "record")
        num(q[1], 1, 10 ** 9)


def solve(inp):
    ls = lines(inp)
    x = int(ls[0].split()[1]); sad = 0
    for l in ls[1:]:
        s, d = l.split(); d = int(d)
        if s == "+": x += d
        elif d <= x: x -= d
        else: sad += 1
    return f"{x} {sad}"


def gen(rng):
    n = rng.choice([1, rng.randint(1, 1000), 1000]); hi = rng.choice([10, 10 ** 9])
    return f"{n} {rng.randint(0, hi)}\n" + "".join(f"{rng.choice('+-')} {rng.randint(1, hi)}\n" for _ in range(n))


def extra():
    return [("boundary", "exact take leaves zero", "1 5\n- 5\n"), ("adversarial", "64-bit total", "3 1000000000\n+ 1000000000\n+ 1000000000\n- 1\n"),
            ("maxSize", "1000 carriers of 10^9", "1000 1000000000\n" + "+ 1000000000\n" * 1000)]
