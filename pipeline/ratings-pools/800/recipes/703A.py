from rlib import *

CONSTRAINTS = "n in 1..100, then n lines with two integers in 1..6."
UNIQUENESS = "One of three fixed outcomes."
STATEMENT = "Reviewed full statement: compare round win counts."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n rounds")
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 2, "pair")
        nums(p, 1, 6)


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    m = sum(a > b for a, b in zip(t[::2], t[1::2]))
    c = sum(a < b for a, b in zip(t[::2], t[1::2]))
    return "Mishka" if m > c else "Chris" if c > m else "Friendship is magic!^^"


def extra():
    return [("boundary", "n=1 tie round", "1\n3 3\n"), ("boundary", "n=1 Chris", "1\n1 6\n"),
            ("adversarial", "equal wins with ties", "4\n6 1\n1 6\n2 2\n5 5\n"),
            ("maxSize", "n=100 Mishka 51 vs 49", "100\n" + "6 1\n" * 50 + "1 6\n" * 49 + "2 1\n"),
            ("maxSize", "n=100 all ties", "100\n" + "6 6\n" * 100)]
