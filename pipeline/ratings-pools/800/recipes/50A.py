from rlib import *

CONSTRAINTS = "two integers M, N with 1 <= M <= N <= 16."
UNIQUENESS = "Single integer maximum."
STATEMENT = "Reviewed full statement: max 2x1 dominoes on MxN board = floor(MN/2)."


def validate(inp):
    m, n = nums(exact_tokens(inp, 2), 1, 16)
    need(m <= n, "M <= N")


def solve(inp):
    m, n = map(int, inp.split())
    return str(m * n // 2)


def extra():
    return [("boundary", "1x1 board -> 0", "1 1\n"), ("boundary", "1x2 board", "1 2\n"),
            ("adversarial", "odd area 15x15", "15 15\n"), ("maxSize", "16x16 maximum", "16 16\n"),
            ("maxSize", "1x16 thin maximum length", "1 16\n")]
