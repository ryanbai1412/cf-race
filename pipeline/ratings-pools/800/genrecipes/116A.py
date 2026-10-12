from rlib import *

CONSTRAINTS = "n in 2..1000; a_i, b_i in 0..1000; a_1 = 0; b_n = 0; exits never exceed current load."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: maximum running load."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 1000)
    need(len(ls) == n + 1, "n stops")
    load = 0
    for i, l in enumerate(ls[1:]):
        p = l.split(" ")
        need(len(p) == 2, "pair")
        a, b = nums(p, 0, 1000)
        need(a <= load, "exit within load")
        load += b - a
        need(i or a == 0, "a1 = 0")
    need(b == 0 and load == 0, "empty at the end")


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    load = best = 0
    for a, b in zip(t[::2], t[1::2]):
        load += b - a
        best = max(best, load)
    return str(best)


def gen(rng):
    n = rng.choice([2, rng.randint(2, 1000), 1000])
    load, rows = 0, []
    for i in range(n):
        if i == n - 1:
            rows.append((load, 0)); break
        a = 0 if i == 0 else rng.randint(0, load)
        b = rng.randint(0, 1000 - (load - a))
        rows.append((a, b)); load += b - a
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"


def extra():
    return [("boundary", "n=2 empty tram", "2\n0 0\n0 0\n"), ("adversarial", "peak in the middle", "4\n0 5\n2 7\n10 1\n1 0\n"),
            ("maxSize", "n=1000 growing then all exit", "1000\n0 1000\n" + "1 1\n" * 998 + "1000 0\n")]
