from rlib import *

CONSTRAINTS = "n in 1..50, string of n characters over RGB."
UNIQUENESS = "Minimum removals is a unique integer."
STATEMENT = "Reviewed full statement: count adjacent equal pairs."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 50)
    word(t[1], "RGB", n, n)


def solve(inp):
    s = inp.split()[1]
    return str(sum(s[i] == s[i + 1] for i in range(len(s) - 1)))


def extra():
    return [("boundary", "n=1", "1\nR\n"), ("boundary", "n=2 equal", "2\nGG\n"),
            ("adversarial", "alternating no removals", "6\nRGBRGB\n"),
            ("maxSize", "n=50 all equal", "50\n" + "B" * 50 + "\n"), ("maxSize", "n=50 pairs", "50\n" + "RRGGBB" * 8 + "RR\n")]
