from rlib import *

CONSTRAINTS = "n in 2..10^5; n-1 distinct episode numbers in 1..n."
UNIQUENESS = "Exactly one missing episode."
STATEMENT = "Reviewed full statement: the missing number."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 2, 100000)
    a = ls[1].split(" ")
    need(len(a) == n - 1, "n-1 values")
    need(len(set(nums(a, 1, n))) == n - 1, "distinct")


def solve(inp):
    t = list(map(int, inp.split()))
    return str(set(range(1, t[0] + 1)).difference(t[1:]).pop())


def gen(rng):
    n = rng.choice([2, 3, rng.randint(2, 100), rng.randint(2, 100), rng.randint(2, 5000)] * 8 + [100000])
    a = list(range(1, n + 1))
    a.pop(rng.choice([0, n - 1, rng.randrange(n)]))
    rng.shuffle(a)
    return f"{n}\n" + joined(a) + "\n"


def extra():
    return [("boundary", "n=2 missing 1", "2\n2\n"), ("boundary", "n=2 missing 2", "2\n1\n"),
            ("adversarial", "missing in the middle, sorted descending", "5\n5 4 2 1\n"),
            ("maxSize", "n=10^5 missing last", "100000\n" + joined(range(1, 100000)) + "\n")]
