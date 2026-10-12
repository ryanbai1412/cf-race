from rlib import *

CONSTRAINTS = "n in 1..100, then a string of n characters over U/R."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: greedy left-to-right pairing of adjacent distinct moves."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 100)
    word(t[1], "UR", n, n)


def solve(inp):
    s = inp.split()[1]
    i = res = 0
    while i < len(s):
        i += 2 if i + 1 < len(s) and s[i] != s[i + 1] else 1
        res += 1
    return str(res)


def extra():
    return [("boundary", "n=1", "1\nU\n"), ("adversarial", "URRU", "4\nURRU\n"), ("adversarial", "RUR odd", "3\nRUR\n"),
            ("maxSize", "n=100 alternating", "100\n" + "UR" * 50 + "\n"), ("maxSize", "n=100 same", "100\n" + "R" * 100 + "\n")]
