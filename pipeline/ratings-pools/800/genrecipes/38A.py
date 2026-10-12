from rlib import *

CONSTRAINTS = "n in 2..100; n-1 values d_i in 1..100; 1 <= a < b <= n."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: sum d_a..d_{b-1}."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    n = num(ls[0], 2, 100)
    d = ls[1].split(" ")
    need(len(d) == n - 1, "n-1 values")
    nums(d, 1, 100)
    ab = ls[2].split(" ")
    need(len(ab) == 2, "a b")
    a, b = num(ab[0], 1, n), num(ab[1], 1, n)
    need(a < b, "a < b")


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; d = t[1:n]; a, b = t[n], t[n + 1]
    return str(sum(d[a - 1:b - 1]))


def gen(rng):
    n = rng.choice([2, rng.randint(2, 100), 100])
    a = rng.randint(1, n - 1); b = rng.randint(a + 1, n)
    return f"{n}\n" + joined(rng.randint(1, 100) for _ in range(n - 1)) + f"\n{a} {b}\n"


def extra():
    return [("boundary", "n=2", "2\n1\n1 2\n"), ("adversarial", "adjacent ranks at the end", "4\n5 6 7\n3 4\n"),
            ("maxSize", "n=100 full climb", "100\n" + joined([100] * 99) + "\n1 100\n")]
