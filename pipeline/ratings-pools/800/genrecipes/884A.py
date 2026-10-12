from rlib import *

CONSTRAINTS = "n in 1..100; t in 1..10^6; a_i in 0..86400; answer <= n (guaranteed)."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: first day d with sum(86400 - a_i, i<=d) >= t."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n t")
    n, t = num(p[0], 1, 100), num(p[1], 1, 10 ** 6)
    a = ls[1].split(" ")
    need(len(a) == n, "n days")
    need(sum(86400 - x for x in nums(a, 0, 86400)) >= t, "answer exists")


def solve(inp):
    v = list(map(int, inp.split()))
    t, s = v[1], 0
    for d, a in enumerate(v[2:], 1):
        s += 86400 - a
        if s >= t:
            return str(d)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    a = [rng.choice([0, 86400, 86399, rng.randint(0, 86400)]) for _ in range(n)]
    free = sum(86400 - x for x in a)
    if free == 0:
        a[-1] = 0; free = 86400
    return f"{n} {rng.randint(1, min(10 ** 6, free))}\n{joined(a)}\n"


def extra():
    return [("boundary", "one free second", "1 1\n86399\n"), ("adversarial", "exactly reached at day boundary", "3 86400\n43200 43200 0\n"),
            ("maxSize", "n=100 t=10^6", "100 1000000\n" + joined([76400] * 100) + "\n")]
