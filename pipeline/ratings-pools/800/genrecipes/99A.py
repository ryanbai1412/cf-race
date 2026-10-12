from rlib import *

CONSTRAINTS = "Single token int.frac, length <= 1000; int part non-empty without leading zero unless single digit; frac non-empty digits."
UNIQUENESS = "Unique output."
STATEMENT = "Reviewed full statement: last integer digit 9 -> 'GOTO Vasilisa.'; otherwise round half up on the first fractional digit."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 1 and len(ls[0]) <= 1000, "single line")
    need(ls[0].count(".") == 1, "one dot")
    a, b = ls[0].split(".")
    word(a, DIGITS, 1, 999); word(b, DIGITS, 1, 999)
    need(len(a) == 1 or a[0] != "0", "no leading zero")


def solve(inp):
    a, b = inp.strip().split(".")
    if a[-1] == "9":
        return "GOTO Vasilisa."
    return a[:-1] + str(int(a[-1]) + 1) if b[0] >= "5" else a


def gen(rng):
    la = rng.choice([1, 2, rng.randint(1, 500)])
    a = rng.choice("123456789") + "".join(rng.choice(DIGITS) for _ in range(la - 1)) if la > 1 else rng.choice(DIGITS)
    b = "".join(rng.choice(DIGITS) for _ in range(rng.randint(1, min(999 - la, rng.choice([1, 3, 500])))))
    return f"{a}.{b}\n"


def extra():
    return [("boundary", "0.0", "0.0\n"), ("adversarial", "exactly half and 9 carry", "8.5000\n"),
            ("maxSize", "1000 chars", "1" + "8" * 498 + "." + "4" * 500 + "\n")]
