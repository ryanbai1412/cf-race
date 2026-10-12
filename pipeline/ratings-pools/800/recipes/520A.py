from rlib import *

CONSTRAINTS = "n in 1..100, then a string of exactly n Latin letters."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: pangram ignoring case."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 100)
    word(t[1], LETTERS, n, n)


def solve(inp):
    return yn(len(set(inp.split()[1].lower())) == 26)


def extra():
    mixed = "".join(c.upper() if i % 2 else c for i, c in enumerate(LOWER))
    return [("boundary", "n=1", "1\na\n"), ("boundary", "n=26 exact pangram mixed case", f"26\n{mixed}\n"),
            ("adversarial", "25 letters missing z", "25\n" + LOWER[:25] + "\n"),
            ("maxSize", "n=100 missing q", "100\n" + (LOWER.replace("q", "") * 4)[:100] + "\n"),
            ("maxSize", "n=100 pangram", "100\n" + (LOWER * 4)[:100] + "\n")]
