from rlib import *

CONSTRAINTS = "a, b, c in 1..1000, each on its own line."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: 7 * min(a, b//2, c//4)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    for l in ls:
        num(l, 1, 1000)


def solve(inp):
    a, b, c = map(int, inp.split())
    return str(7 * min(a, b // 2, c // 4))


def extra():
    return [("boundary", "all ones -> 0", "1\n1\n1\n"), ("boundary", "exact ratio 1 2 4", "1\n2\n4\n"),
            ("maxSize", "all 1000 -> 1750", "1000\n1000\n1000\n"), ("adversarial", "apples limiting", "1000\n3\n1000\n")]
