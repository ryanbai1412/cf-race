from rlib import *

CONSTRAINTS = "n in 1..10^5; string of n letters from 'AD'."
UNIQUENESS = "Fixed word."
STATEMENT = "Reviewed full statement: Anton / Danik / Friendship by majority."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100000)
    word(ls[1], "AD", n, n)


def solve(inp):
    s = lines(inp)[1]
    a, d = s.count("A"), s.count("D")
    return "Anton" if a > d else "Danik" if d > a else "Friendship"


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 5000)] * 6 + [100000])
    if rng.random() < 0.3 and n % 2 == 0:
        s = list("A" * (n // 2) + "D" * (n // 2)); rng.shuffle(s); s = "".join(s)
    else:
        s = "".join(rng.choice("AD") for _ in range(n))
    return f"{n}\n{s}\n"


def extra():
    return [("boundary", "single D", "1\nD\n"), ("adversarial", "tie", "4\nADDA\n"),
            ("maxSize", "n=10^5 tie", "100000\n" + "AD" * 50000 + "\n")]
