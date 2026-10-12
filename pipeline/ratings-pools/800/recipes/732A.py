from rlib import *

CONSTRAINTS = "k in 1..1000, r in 1..9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: smallest i >= 1 with k*i mod 10 in {0, r}."


def validate(inp):
    k, r = exact_tokens(inp, 2)
    num(k, 1, 1000); num(r, 1, 9)


def solve(inp):
    k, r = map(int, inp.split())
    return str(next(i for i in range(1, 11) if k * i % 10 in (0, r)))


def extra():
    return [("boundary", "1 1", "1 1\n"), ("adversarial", "k=3 r=2 needs 4 shovels", "3 2\n"),
            ("maxSize", "k=1000", "1000 9\n"), ("adversarial", "k=999 r=1 -> 9", "999 1\n")]
