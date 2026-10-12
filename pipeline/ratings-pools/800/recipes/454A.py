from rlib import *

CONSTRAINTS = "odd n in 3..101."
UNIQUENESS = "The drawing is fully determined."
STATEMENT = "Reviewed full statement and samples: row i has D count n-2|i-c| centered, '*' elsewhere."


def validate(inp):
    n = num(exact_tokens(inp, 1)[0], 3, 101)
    need(n % 2 == 1, "odd")


def solve(inp):
    n = int(inp.split()[0]); c = n // 2
    return "\n".join("*" * abs(i - c) + "D" * (n - 2 * abs(i - c)) + "*" * abs(i - c) for i in range(n))


def extra():
    return [("boundary", "minimum n=3", "3\n"), ("adversarial", "n=5", "5\n"), ("maxSize", "maximum n=101", "101\n"),
            ("maxSize", "n=99", "99\n")]
