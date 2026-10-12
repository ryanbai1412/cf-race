from rlib import *

CONSTRAINTS = "n in 2..1000; n distinct prices in 1..10^4."
UNIQUENESS = "Distinct prices make winner and price unique."
STATEMENT = "Reviewed full statement: winner index (1-based) and second highest price."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 2, 1000)
    p = ls[1].split(" ")
    need(len(p) == n, "n prices")
    need(len(set(nums(p, 1, 10000))) == n, "distinct")


def solve(inp):
    p = list(map(int, inp.split()))[1:]
    w = max(range(len(p)), key=p.__getitem__)
    return f"{w + 1} {sorted(p)[-2]}"


def gen(rng):
    n = rng.choice([2, rng.randint(2, 1000), 1000])
    return f"{n}\n" + joined(rng.sample(range(1, rng.choice([n, 10000]) + 1), n)) + "\n"


def extra():
    return [("boundary", "n=2 winner first", "2\n10000 1\n"), ("adversarial", "winner last, second right before", "4\n1 2 9999 10000\n"),
            ("maxSize", "n=1000 decreasing", "1000\n" + joined(range(10000, 9000, -1)) + "\n")]
