from rlib import *

CONSTRAINTS = "n in 1..1000; ids in 0..10^9."
UNIQUENESS = "Unique integer (-1 when any nonzero id appears more than twice)."
STATEMENT = "Reviewed full statement: count nonzero ids occurring exactly twice; -1 if any occurs 3+ times."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n ids")
    nums(a, 0, 10 ** 9)


def solve(inp):
    from collections import Counter
    c = Counter(x for x in inp.split()[1:] if x != "0")
    if any(v > 2 for v in c.values()):
        return "-1"
    return str(sum(v == 2 for v in c.values()))


def gen(rng):
    n = rng.choice([1, 2, 3, rng.randint(1, 1000), 1000])
    hi = rng.choice([1, 3, n, 10 ** 9])
    return f"{n}\n" + joined(rng.randint(0, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single idle", "1\n0\n"), ("adversarial", "many zeros are not a conference", "5\n0 0 0 7 7\n"),
            ("maxSize", "n=1000 500 pairs", "1000\n" + joined(10 ** 9 - i // 2 for i in range(1000)) + "\n")]
