from rlib import *

CONSTRAINTS = "one nonempty lowercase string of length <= 100."
UNIQUENESS = "Exactly one of the two fixed phrases is correct."
STATEMENT = "Reviewed full statement: even distinct count -> CHAT WITH HER!, odd -> IGNORE HIM!."


def validate(inp):
    word(exact_tokens(inp, 1)[0], LOWER, 1, 100)


def solve(inp):
    return "CHAT WITH HER!" if len(set(inp.split()[0])) % 2 == 0 else "IGNORE HIM!"


def extra():
    return [("boundary", "single letter odd", "a\n"), ("boundary", "two distinct letters", "ab\n"),
            ("adversarial", "many repeats of two letters (even distinct, odd length)", "aabbbaabbba\n"),
            ("maxSize", "length 100 with all 26 letters", (LOWER * 4)[:100] + "\n"),
            ("maxSize", "length 100 with 25 letters", ("abcdefghijklmnopqrstuvwxy" * 4) + "\n")]
