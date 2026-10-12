from rlib import *

CONSTRAINTS = "n in 1..10^5; each event is -1 or a recruit count in 1..10."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: crimes with no free officer go untreated."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100000)
    e = ls[1].split(" ")
    need(len(e) == n, "n events")
    need(all(v == -1 or 1 <= v <= 10 for v in nums(e, -1, 10)), "event range")


def solve(inp):
    free = bad = 0
    for v in map(int, inp.split()[1:]):
        if v == -1:
            if free:
                free -= 1
            else:
                bad += 1
        else:
            free += v
    return str(bad)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), rng.randint(1, 100), rng.randint(1, 5000)] * 8 + [100000])
    p = rng.random()
    return f"{n}\n" + joined(-1 if rng.random() < p else rng.randint(1, 10) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "one crime", "1\n-1\n"), ("adversarial", "crime before hiring", "3\n-1 1 -1\n"),
            ("maxSize", "n=10^5 alternating hire/crime pairs", "100000\n" + joined([10, -1] * 50000) + "\n")]
