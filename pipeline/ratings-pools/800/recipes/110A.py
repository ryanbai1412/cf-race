from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^18."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: YES iff the count of digits 4/7 is itself a lucky number."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 18)


def solve(inp):
    c = sum(ch in "47" for ch in inp.split()[0])
    return yn(c > 0 and all(ch in "47" for ch in str(c)))


def extra():
    return [("boundary", "minimum n=1", "1\n"), ("boundary", "maximum n=10^18", "1000000000000000000\n"),
            ("adversarial", "count 0 must be NO (not lucky)", "123\n"),
            ("adversarial", "count 7 of lucky digits", "474747712\n"),
            ("maxSize", "18 digits with 14 lucky digits -> NO", "777777777777774412\n"),
            ("maxSize", "18-digit n with exactly 4 lucky digits -> YES", "100000000000004477\n")]
