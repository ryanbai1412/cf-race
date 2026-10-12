from rlib import *

CONSTRAINTS = "n in 2..100, then a string of n characters over S/F."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: count SF transitions > FS transitions."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 2, 100)
    word(t[1], "SF", n, n)


def solve(inp):
    s = inp.split()[1]
    return yn(s.count("SF") > s.count("FS"))


def extra():
    return [("boundary", "n=2 SF", "2\nSF\n"), ("boundary", "n=2 FS", "2\nFS\n"), ("adversarial", "equal transitions", "4\nSFFS\n"),
            ("maxSize", "n=100 alternating starting S ending F", "100\n" + "SF" * 50 + "\n"), ("maxSize", "n=100 all S", "100\n" + "S" * 100 + "\n")]
