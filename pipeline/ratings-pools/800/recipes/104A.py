from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 25."
UNIQUENESS = "Count of cards is a unique integer."
STATEMENT = "Reviewed full statement: first card queen of spades (10 points); count remaining cards with value n-10 (aces 1 or 11)."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 25)


def solve(inp):
    need_value = int(inp.split()[0]) - 10
    if need_value in (1, 11):
        return "4"
    if 2 <= need_value <= 9:
        return "4"
    if need_value == 10:
        return "15"
    return "0"


def extra():
    return [("boundary", "n=1 -> 0", "1\n"), ("boundary", "n=10 needs 0 -> 0", "10\n"),
            ("adversarial", "n=20 ten-valued cards excluding queen of spades -> 15", "20\n"),
            ("adversarial", "n=21 ace as 11", "21\n"), ("adversarial", "n=11 ace as 1", "11\n"),
            ("maxSize", "maximum n=25", "25\n")]
