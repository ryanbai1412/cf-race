from rlib import *

CONSTRAINTS = "two lines, each a nonempty lowercase word of length <= 100, no extra spaces."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: t must equal reverse(s)."


def validate(inp):
    ls = [l for l in lines(inp)]
    need(len(ls) == 2, "two lines")
    for l in ls:
        word(l, LOWER, 1, 100)


def solve(inp):
    s, t = lines(inp)[:2]
    return yn(t == s[::-1])


def extra():
    r = rng(41)
    a = "".join(r.choice(LOWER) for _ in range(100))
    return [("boundary", "single letters equal", "a\na\n"), ("boundary", "single letters differ", "a\nb\n"),
            ("adversarial", "t equals s (not palindrome) -> NO", "ab\nab\n"),
            ("adversarial", "different lengths, prefix of reverse", "abc\ncb\n"),
            ("maxSize", "length-100 random reversed -> YES", f"{a}\n{a[::-1]}\n"),
            ("maxSize", "length-100 reversed with one char changed -> NO", f"{a}\n{a[::-1][:-1]}{'b' if a[0] != 'b' else 'c'}\n")]
