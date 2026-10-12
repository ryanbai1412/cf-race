from rlib import *

CONSTRAINTS = "a single integer w with 1 <= w <= 100."
UNIQUENESS = "Decision problem: exactly one of YES/NO is correct."
STATEMENT = "Reviewed full statement, I/O format and samples: split w into two positive even parts."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 100)


def solve(inp):
    w = int(inp.split()[0])
    return yn(w % 2 == 0 and w > 2)


def extra():
    return [("boundary", "minimum w=1", "1\n"), ("boundary", "w=2 is even but cannot split into two positive evens", "2\n"),
            ("adversarial", "smallest YES w=4", "4\n"), ("adversarial", "odd near max w=99", "99\n"),
            ("maxSize", "maximum w=100", "100\n")]
