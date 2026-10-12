from rlib import *

CONSTRAINTS = "one string of length 1..200 over '.', '-' that is a valid Borze code ('.'->0, '-.'->1, '--'->2)."
UNIQUENESS = "Borze code is prefix-free, so the decoded ternary string is unique."
STATEMENT = "Reviewed full statement and I/O: decode Borze, leading zeros preserved."


def parse(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == ".":
            out.append("0"); i += 1
        else:
            need(i + 1 < len(s), "dangling '-'")
            out.append("1" if s[i + 1] == "." else "2"); i += 2
    return "".join(out)


def validate(inp):
    t = exact_tokens(inp, 1)[0]
    word(t, ".-", 1, 200)
    parse(t)


def solve(inp):
    return parse(inp.split()[0])


def enc(digits):
    return "".join({"0": ".", "1": "-.", "2": "--"}[d] for d in digits)


def extra():
    r = rng(32)
    return [("boundary", "single '.' -> 0", ".\n"), ("boundary", "single code '--' -> 2", "--\n"),
            ("adversarial", "alternating '-.' and '.' patterns", enc("1010101012012") + "\n"),
            ("adversarial", "all-dash string of length 200 -> 100 twos", "-" * 200 + "\n"),
            ("maxSize", "random length-200 code", enc("".join(r.choice("12") for _ in range(100))) + "\n"),
            ("maxSize", "200 dots -> 200 zeros", "." * 200 + "\n")]
