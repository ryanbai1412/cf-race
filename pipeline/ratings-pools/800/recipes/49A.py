from rlib import *

CONSTRAINTS = "one line of length <= 100 of Latin letters and spaces ending with the only '?', with at least one letter."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: answer YES iff the last letter (ignoring spaces/?) is a vowel A,E,I,O,U,Y (any case)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 1, "one line")
    s = ls[0]
    need(1 <= len(s) <= 100 and s.endswith("?") and s.count("?") == 1, "question mark last and unique")
    need(all(c in LETTERS + " " for c in s[:-1]), "letters/spaces only")
    need(any(c in LETTERS for c in s), "at least one letter")


def solve(inp):
    s = lines(inp)[0]
    last = [c for c in s if c.isalpha()][-1]
    return yn(last.lower() in "aeiouy")


def extra():
    return [("boundary", "single letter vowel", "a?\n"), ("boundary", "single uppercase consonant", "B?\n"),
            ("adversarial", "spaces between last letter and '?' (Y vowel)", "Is it so   Y   ?\n"),
            ("adversarial", "leading spaces, consonant last", "   ab c d      ?\n"),
            ("maxSize", "length-100 line ending in vowel then spaces", "x" * 50 + " " * 46 + "aE ?\n"),
            ("maxSize", "length-100 letters ending with consonant", "a" * 98 + "z?\n")]
