from rlib import *

CONSTRAINTS = "two integers a, b in 1..10^9."
UNIQUENESS = "One of two names."
STATEMENT = "Reviewed full statement: Vladik gives odd amounts, Valera even; first unable loses."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 10 ** 9)


def solve(inp):
    a, b = map(int, inp.split())
    i = 1
    while True:
        if i % 2:
            if a < i:
                return "Vladik"
            a -= i
        else:
            if b < i:
                return "Valera"
            b -= i
        i += 1


def extra():
    return [("boundary", "1 1", "1 1\n"), ("adversarial", "Valera first fails", "7 6\n"),
            ("maxSize", "both 10^9", "1000000000 1000000000\n"), ("maxSize", "a=10^9 b=1", "1000000000 1\n")]
