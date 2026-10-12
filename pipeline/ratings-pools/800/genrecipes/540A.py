from rlib import *

CONSTRAINTS = "n in 1..1000; two digit strings of length n."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: sum of cyclic digit distances min(d, 10-d)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    n = num(ls[0], 1, 1000)
    word(ls[1], DIGITS, n, n); word(ls[2], DIGITS, n, n)


def solve(inp):
    _, a, b = lines(inp)
    return str(sum(min(abs(int(x) - int(y)), 10 - abs(int(x) - int(y))) for x, y in zip(a, b)))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 1000), 1000])
    return f"{n}\n" + "".join(rng.choice(DIGITS) for _ in range(n)) + "\n" + "".join(rng.choice(DIGITS) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "already open", "1\n0\n0\n"), ("adversarial", "wraparound 0/9 and 0/5", "2\n05\n90\n"),
            ("maxSize", "n=1000 all distance 5", "1000\n" + "0" * 1000 + "\n" + "5" * 1000 + "\n")]
