from rlib import *

CONSTRAINTS = "even n in 2..50, then a digit string of exactly n digits (leading zeros allowed)."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: all digits 4/7 and equal half digit sums."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 2, 50)
    need(n % 2 == 0, "n even")
    word(t[1], DIGITS, n, n)


def solve(inp):
    n, s = inp.split()
    h = int(n) // 2
    return yn(set(s) <= set("47") and sum(map(int, s[:h])) == sum(map(int, s[h:])))


def extra():
    return [("boundary", "n=2 44", "2\n44\n"), ("boundary", "n=2 leading zero 00 (equal sums, not lucky)", "2\n00\n"),
            ("adversarial", "lucky but unequal sums", "4\n4477\n"), ("adversarial", "equal sums but digit 1", "4\n1771\n"),
            ("maxSize", "n=50 lucky balanced", "50\n" + "47" * 25 + "\n"), ("maxSize", "n=50 lucky unbalanced", "50\n" + "4" * 25 + "7" * 25 + "\n")]
