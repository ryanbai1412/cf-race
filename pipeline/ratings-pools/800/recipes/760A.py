from rlib import *

CONSTRAINTS = "m in 1..12, d in 1..7."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: ceil((days(m) + d - 1) / 7), non-leap year."

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def validate(inp):
    m, d = exact_tokens(inp, 2)
    num(m, 1, 12); num(d, 1, 7)


def solve(inp):
    m, d = map(int, inp.split())
    return str(-(-(DAYS[m - 1] + d - 1) // 7))


def extra():
    return [("boundary", "February starting Monday -> 4", "2 1\n"), ("boundary", "January Sunday -> 6", "1 7\n"),
            ("adversarial", "30-day month starting Saturday -> 5", "4 6\n"), ("maxSize", "December Sunday", "12 7\n")]
