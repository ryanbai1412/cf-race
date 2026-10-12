from rlib import *

CONSTRAINTS = "n in 2..2*10^5; a_i in {1, 2}."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max teams of three from singles and inseparable pairs."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 2, 200000)
    a = ls[1].split(" ")
    need(len(a) == n, "n groups")
    nums(a, 1, 2)


def solve(inp):
    a = inp.split()[1:]
    one, two = a.count("1"), a.count("2")
    best = 0
    for k in range(min(one, two) + 1):
        best = max(best, k + (one - k) // 3)
    return str(best)


def gen(rng):
    n = rng.choice([2, 3, rng.randint(2, 100), rng.randint(2, 5000)])
    p = rng.random()
    return f"{n}\n" + joined(1 if rng.random() < p else 2 for _ in range(n)) + "\n"


def extra():
    return [("boundary", "two pairs, no team", "2\n2 2\n"), ("adversarial", "pair+single beats leftover singles", "4\n2 1 1 1\n"),
            ("maxSize", "n=2*10^5 mixed", "200000\n" + joined([1, 2] * 100000) + "\n")]
