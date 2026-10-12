from rlib import *

CONSTRAINTS = "a, b in 1..1000 on separate lines, a != b."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: split distance d into floor(d/2) and ceil(d/2), tiredness triangular sums."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    a, b = num(ls[0], 1, 1000), num(ls[1], 1, 1000)
    need(a != b, "distinct")


def solve(inp):
    a, b = map(int, inp.split())
    d = abs(a - b); x, y = d // 2, d - d // 2
    return str(x * (x + 1) // 2 + y * (y + 1) // 2)


def extra():
    return [("boundary", "adjacent", "1\n2\n"), ("maxSize", "1 and 1000", "1\n1000\n"), ("adversarial", "even distance reversed", "1000\n2\n")]
