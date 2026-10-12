from rlib import *

CONSTRAINTS = "A, B in 0..10^9; x, y, z in 0..10^9; two lines."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max(0, 2x+y-A) + max(0, y+3z-B)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    a, b = ls[0].split(" "), ls[1].split(" ")
    need(len(a) == 2 and len(b) == 3, "counts")
    nums(a + b, 0, 10 ** 9)


def solve(inp):
    A, B, x, y, z = map(int, inp.split())
    return str(max(0, 2 * x + y - A) + max(0, y + 3 * z - B))


def extra():
    return [("boundary", "all zero", "0 0\n0 0 0\n"), ("adversarial", "surplus yellow cannot cover blue", "1000000000 0\n0 0 1\n"),
            ("maxSize", "max demand no crystals (7e9, 64-bit)", "0 0\n1000000000 1000000000 1000000000\n")]
