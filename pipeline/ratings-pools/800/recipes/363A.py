from rlib import *

CONSTRAINTS = "a single integer n with 0 <= n < 10^9, no leading zeros."
UNIQUENESS = "The soroban drawing is fully determined (one rod per digit, last digit first)."
STATEMENT = "Reviewed full statement and samples: rod = go-dama ('O-|' or '-O|' if digit>=5) + ichi-damas O*k-O*(4-k)."


def validate(inp):
    t = exact_tokens(inp, 1)[0]
    num(t, 0, 10 ** 9 - 1)
    need(t == str(int(t)), "no leading zeros")


def solve(inp):
    out = []
    for ch in reversed(inp.split()[0]):
        d = int(ch)
        k = d % 5
        out.append(("-O|" if d >= 5 else "O-|") + "O" * k + "-" + "O" * (4 - k))
    return "\n".join(out)


def extra():
    return [("boundary", "n=0", "0\n"), ("boundary", "n=5", "5\n"), ("adversarial", "digits 9 and 4 and zero", "940\n"),
            ("maxSize", "maximum n=999999999", "999999999\n"), ("maxSize", "9 digits all digits", "123456789\n")]
