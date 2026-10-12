from rlib import *

CONSTRAINTS = "n in 1..10^5; 2n values in 1..n, each exactly twice."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: maximum number of unmatched socks on the table."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100000)
    x = ls[1].split(" ")
    need(len(x) == 2 * n, "2n socks")
    from collections import Counter
    need(set(Counter(nums(x, 1, n)).values()) == {2}, "each pair twice")


def solve(inp):
    on, best = set(), 0
    for x in inp.split()[1:]:
        if x in on: on.remove(x)
        else: on.add(x)
        best = max(best, len(on))
    return str(best)


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 3000)])
    x = list(range(1, n + 1)) * 2
    rng.shuffle(x)
    if rng.random() < 0.2:
        x = sorted(x)
    return f"{n}\n{joined(x)}\n"


def extra():
    return [("boundary", "single pair", "1\n1 1\n"), ("adversarial", "nested pairs", "3\n1 2 3 3 2 1\n"),
            ("maxSize", "n=10^5 all open", "100000\n" + joined(list(range(1, 100001)) * 2) + "\n")]
