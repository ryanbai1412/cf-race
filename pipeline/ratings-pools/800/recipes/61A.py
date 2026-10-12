from rlib import *

CONSTRAINTS = "two lines of equal length (1..100) over '0'/'1', may start with 0."
UNIQUENESS = "Bitwise XOR string is unique including leading zeros."
STATEMENT = "Reviewed full statement: output digitwise XOR keeping leading zeros."


def validate(inp):
    t = exact_tokens(inp, 2)
    word(t[0], "01", 1, 100); word(t[1], "01", 1, 100)
    need(len(t[0]) == len(t[1]), "equal lengths")


def solve(inp):
    a, b = inp.split()
    return "".join("1" if x != y else "0" for x, y in zip(a, b))


def extra():
    r = rng(61)
    a = "".join(r.choice("01") for _ in range(100)); b = "".join(r.choice("01") for _ in range(100))
    return [("boundary", "length 1 equal zeros -> '0'", "0\n0\n"), ("boundary", "length 1 differ", "1\n0\n"),
            ("adversarial", "all-equal 100 ones -> 100 zeros (leading zeros kept)", "1" * 100 + "\n" + "1" * 100 + "\n"),
            ("maxSize", "random length 100", f"{a}\n{b}\n")]
