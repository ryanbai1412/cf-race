from rlib import *

CONSTRAINTS = "n in 1..1000; n distinct integers in 1..1000."
UNIQUENESS = "Two fixed integers."
STATEMENT = "Reviewed full statement: greedy take of the larger end card, Sereja first."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n cards")
    need(len(set(nums(a, 1, 1000))) == n, "distinct")


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    i, j, s, turn = 0, len(a) - 1, [0, 0], 0
    while i <= j:
        if a[i] > a[j]:
            s[turn] += a[i]; i += 1
        else:
            s[turn] += a[j]; j -= 1
        turn ^= 1
    return f"{s[0]} {s[1]}"


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 1000), 1000])
    return f"{n}\n" + joined(rng.sample(range(1, 1001), n)) + "\n"


def extra():
    return [("boundary", "single card", "1\n1000\n"), ("adversarial", "Dima wins with increasing cards", "3\n1 2 3\n"),
            ("maxSize", "n=1000 permutation", "1000\n" + joined(list(range(1, 1001, 2)) + list(range(1000, 0, -2))) + "\n")]
