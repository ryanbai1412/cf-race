from rlib import *

CONSTRAINTS = "1 <= b < a < c <= 10^9; n in 1..10^5; x_i in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count banknotes strictly between the guards."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    p = ls[0].split(" ")
    need(len(p) == 3, "a b c")
    a, b, c = (num(t, 1, 10 ** 9) for t in p)
    need(b < a < c, "b < a < c")
    n = num(ls[1], 1, 100000)
    x = ls[2].split(" ")
    need(len(x) == n, "n notes")
    nums(x, 1, 10 ** 9)


def solve(inp):
    t = list(map(int, inp.split()))
    b, c = t[1], t[2]
    return str(sum(b < x < c for x in t[4:]))


def gen(rng):
    hi = rng.choice([10, 1000, 10 ** 9])
    b = rng.randint(1, hi - 2); a = rng.randint(b + 1, hi - 1); c = rng.randint(a + 1, hi)
    n = rng.choice([1, rng.randint(1, 100), rng.randint(1, 3000)])
    return f"{a} {b} {c}\n{n}\n" + joined(rng.choice([b, c, a, rng.randint(1, hi)]) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "notes on guards", "2 1 3\n3\n1 3 2\n"), ("adversarial", "no reachable notes", "5 4 6\n2\n4 6\n"),
            ("maxSize", "n=10^5 widest range", "500000000 1 1000000000\n100000\n" + joined([999999999] * 100000) + "\n")]
