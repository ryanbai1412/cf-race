from rlib import *

CONSTRAINTS = "one string of 1..50 lowercase letters or digits."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: turn vowels and odd digits."


def validate(inp):
    word(exact_tokens(inp, 1)[0], LOWER + DIGITS, 1, 50)


def solve(inp):
    return str(sum(c in "aeiou13579" for c in inp.split()[0]))


def extra():
    return [("boundary", "single even digit", "0\n"), ("boundary", "single vowel", "u\n"), ("adversarial", "y is not a vowel", "y9z8\n"),
            ("maxSize", "50 vowels/odds", ("aeiou13579" * 5) + "\n")]
